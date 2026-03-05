from flask import request, jsonify, send_file
import logging
import os
import re
import json
import io
import mimetypes
import requests as http_requests
from database.models import WFFile
from pathlib import Path
from config.config import Args
import safrs  # circular import error if at top
from datetime import datetime, timezone
from flask_jwt_extended import get_jwt, jwt_required
from security.system.authorization import Security
from database.models import TaskInstance
import boto3

app_logger = logging.getLogger("api_logic_server_app")
session = safrs.DB.session
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'newcompany-documents')

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    pass

    @app.route('/upload_files', methods=['POST','OPTIONS'])
    @jwt_required()
    def upload_files():
        """
        Endpoint to handle file uploads for the NDA process.
        Accepts multipart/form-data with:
          - file            : the uploaded file (binary)
          - file_url        : a URL to a remote file (alternative to binary upload)
          - file_name       : filename to use when file_url is supplied
          - task_instance_id  : the associated TaskInstance ID
          - description     : optional text description / tag for the file
        """
        if request.method == 'OPTIONS':
            return jsonify({"message": "CORS preflight check successful"}), 200
        try:
            task_instance_id = request.form.get("task_instance_id")
            description    = request.form.get("description", '')
            file_url       = request.form.get("file_url", '').strip()
            #data = request.get_json() or {}
            if not task_instance_id:
                return jsonify({"error": "Missing required parameter: task_instance_id"}), 400
            
            task_instance = session.query(TaskInstance).filter_by(TaskInstanceId=task_instance_id).first()
            if not task_instance:
                return jsonify({"error": f"No TaskInstance found with ID {task_instance_id}"}), 404
            
            user = Security.current_user().Username
            temp_dir = Path("temp_uploads")
            temp_dir.mkdir(exist_ok=True)

            # ── Resolve file content ────────────────────────────────────────────
            if 'file' in request.files and request.files['file'].filename != '':
                # Binary upload path
                file = request.files['file']
                filename = file.filename
                temp_file_path = temp_dir / filename
                file.save(temp_file_path)
                content_type   = file.content_type
                content_length = file.content_length or temp_file_path.stat().st_size

            elif file_url:
                # URL-based download path
                filename   = request.form.get("file_name") or file_url.split('/')[-1] or 'linked_file'
                temp_file_path = temp_dir / filename
                resp = http_requests.get(file_url, timeout=30)
                resp.raise_for_status()
                temp_file_path.write_bytes(resp.content)
                content_type   = resp.headers.get('Content-Type', 'application/octet-stream')
                content_length = len(resp.content)

            else:
                return jsonify({"error": "No file or file_url provided in the request"}), 400

            # ── Security validation (runs before S3 upload) ─────────────────────
            validation_error = validate_file(temp_file_path, filename)
            if validation_error:
                temp_file_path.unlink(missing_ok=True)
                app_logger.warning(f"File rejected [{filename}]: {validation_error}")
                return jsonify({"error": f"File rejected: {validation_error}"}), 400

            app_logger.info(f"File uploaded successfully: {temp_file_path}")
            application_id = task_instance.ApplicationId
            file_type = filename.split('.')[-1] if '.' in filename else 'txt'
            wf_file = WFFile(
                FileName    = filename,
                FilePath    = str(temp_file_path),
                FileType    = file_type,
                FileSize    = content_length,
                UploadedDate= datetime.now(),    # Ensure timezone-aware timestamp  
                ApplicationID = application_id,
                Tag         = description or None,
                CreatedBy   = user
            )
                       
            try:
                s3_key = f"uploads/{application_id}/{filename}"
                done = write_to_s3(temp_file_path, S3_BUCKET_NAME, s3_key)
                wf_file.FilePath = f"s3://{S3_BUCKET_NAME}/{s3_key}" if done else str(temp_file_path)
                session.add(wf_file)
                session.flush()  # Get FileID before commit
                if done:
                    temp_file_path.unlink(missing_ok=True)
                task_instance.Result = str(wf_file.FileID)
                task_instance.ResultData = json.dumps({"Filename": filename, "FileId": wf_file.FileID, "filePath": wf_file.FilePath, "Tag": wf_file.Tag})
                session.add(task_instance)
                session.commit()
            
                return jsonify({"message": f"File uploaded and task completed successfully", "file_path": str(temp_file_path)}), 200
            except Exception as e:
                app_logger.error(f"Error completing task after file upload: {e}")
                return jsonify({"error": f"File uploaded but an error occurred while completing the task: {str(e)}"}), 500


        except Exception as e:
            app_logger.error(f"Error uploading file: {e}")
            return jsonify({"error": "An error occurred while uploading the file", "detail": str(e)}), 500

    # ── /download_file/<file_id> ────────────────────────────────────────────────
    @app.route('/download_file/<int:file_id>', methods=['GET', 'OPTIONS'])
    @jwt_required()
    def download_file(file_id):
        """
        Stream a file stored in S3 (or local temp_uploads) directly to the caller.
        The file record is looked up by WFFile.FileID.

        Query params:
          presigned (bool, default false) – return a JSON presigned URL instead of
                                            streaming the bytes.
          expires   (int,  default 3600)  – presigned URL expiry in seconds.
        """
        if request.method == 'OPTIONS':
            return jsonify({"message": "CORS preflight check successful"}), 200

        wf_file = session.query(WFFile).filter_by(FileID=file_id).first()
        if not wf_file:
            return jsonify({"error": f"No file record found with FileID {file_id}"}), 404

        file_path: str = wf_file.FilePath or ''
        filename: str  = wf_file.FileName or f"file_{file_id}"
        mime_type: str = _mime_from_extension(filename)

        use_presigned = request.args.get('presigned', 'false').lower() in ('1', 'true', 'yes')
        expires = int(request.args.get('expires', 3600))

        # ── S3 path ────────────────────────────────────────────────────────────
        if file_path.startswith('s3://'):
            bucket, s3_key = _parse_s3_path(file_path)
            app_logger.info(f"Resolved S3 path: bucket={bucket} key={s3_key} (raw FilePath={file_path!r})")
            if use_presigned:
                url = generate_presigned_url(bucket, s3_key, expires)
                if not url:
                    return jsonify({"error": "Could not generate presigned URL", "bucket": bucket, "key": s3_key}), 500
                return jsonify({"url": url, "expires_in": expires, "filename": filename}), 200
            else:
                file_bytes = download_from_s3(bucket, s3_key)
                if file_bytes is None:
                    return jsonify({"error": "Could not retrieve file from S3", "bucket": bucket, "key": s3_key}), 500
                return send_file(
                    io.BytesIO(file_bytes),
                    mimetype=mime_type,
                    as_attachment=True,
                    download_name=filename
                )

        # ── Local path fallback ────────────────────────────────────────────────
        local_path = Path(file_path)
        if not local_path.exists():
            return jsonify({"error": f"File not found at path: {file_path}"}), 404
        return send_file(local_path, mimetype=mime_type, as_attachment=True, download_name=filename)

    # ── /file_url/<file_id> ────────────────────────────────────────────────────
    @app.route('/file_url/<int:file_id>', methods=['GET', 'OPTIONS'])
    @jwt_required()
    def file_presigned_url(file_id):
        """
        Return a short-lived presigned S3 URL for a WFFile record.
        Useful for embedding in emails, <img> tags, or browser downloads.

        Query params:
          expires (int, default 3600) – URL expiry in seconds (max 604800 = 7 days).
        """
        if request.method == 'OPTIONS':
            return jsonify({"message": "CORS preflight check successful"}), 200

        wf_file = session.query(WFFile).filter_by(FileID=file_id).first()
        if not wf_file:
            return jsonify({"error": f"No file record found with FileID {file_id}"}), 404

        file_path: str = wf_file.FilePath or ''
        if not file_path.startswith('s3://'):
            return jsonify({"error": "File is not stored in S3"}), 400

        expires = int(request.args.get('expires', 3600))
        bucket, s3_key = _parse_s3_path(file_path)
        app_logger.info(f"Presigned URL request: bucket={bucket} key={s3_key} (raw FilePath={file_path!r})")
        url = generate_presigned_url(bucket, s3_key, expires)
        if not url:
            return jsonify({"error": "Could not generate presigned URL", "bucket": bucket, "key": s3_key}), 500

        return jsonify({
            "url"       : url,
            "filename"  : wf_file.FileName,
            "expires_in": expires
        }), 200

    # ── /debug_file/<file_id> ──────────────────────────────────────────────────
    @app.route('/debug_file/<int:file_id>', methods=['GET', 'OPTIONS'])
    @jwt_required()
    def debug_file(file_id):
        """
        Returns the raw FilePath stored in the DB plus the parsed bucket/key,
        so you can verify what S3 object will be accessed.
        Also checks whether the key actually exists in S3.
        """
        if request.method == 'OPTIONS':
            return jsonify({"message": "CORS preflight check successful"}), 200

        wf_file = session.query(WFFile).filter_by(FileID=file_id).first()
        if not wf_file:
            return jsonify({"error": f"No file record found with FileID {file_id}"}), 404

        file_path: str = wf_file.FilePath or ''
        info = {
            "FileID"   : file_id,
            "FileName" : wf_file.FileName,
            "FilePath" : file_path,
        }

        if file_path.startswith('s3://'):
            bucket, s3_key = _parse_s3_path(file_path)
            info["parsed_bucket"] = bucket
            info["parsed_key"]    = s3_key
            info["s3_exists"]     = _s3_key_exists(bucket, s3_key)
        else:
            info["local_exists"] = Path(file_path).exists()

        return jsonify(info), 200


def _parse_s3_path(s3_path: str):
    """Parse 's3://bucket/key/path' → (bucket, key)"""
    without_scheme = s3_path[len('s3://'):]
    bucket, _, key = without_scheme.partition('/')
    return bucket, key


def _s3_key_exists(bucket_name: str, s3_key: str) -> bool:
    """Return True if the key exists in the bucket, False otherwise."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        return True
    except Exception:
        return False


def _mime_from_extension(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or 'application/octet-stream'


def download_from_s3(bucket_name: str, s3_key: str) -> bytes | None:
    """Download a file from S3 and return its raw bytes, or None on error."""

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        return response['Body'].read()
    except Exception as e:
        app_logger.error(f"Error downloading from S3 bucket={bucket_name} key={s3_key}: {e}")
        return None


def generate_presigned_url(bucket_name: str, s3_key: str, expires: int = 3600) -> str | None:
    """Generate a presigned GET URL for an S3 object, or None on error."""

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=expires
        )
        app_logger.info(f"Presigned URL generated for s3://{bucket_name}/{s3_key}")
        return url
    except Exception as e:
        app_logger.error(f"Error generating presigned URL: {e}")
        return None # (file_path, bucket_name, s3_key:str=None):

def write_to_s3(file_path: Path, bucket_name: str, s3_key: str) -> bool:
    """Utility function to upload a file to AWS S3"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        s3_client.upload_file(str(file_path), bucket_name, s3_key)
        app_logger.info(f"File {file_path} uploaded to S3 bucket {bucket_name} with key {s3_key}")
        return True
    except Exception as e:
        app_logger.error(f"Error uploading file to S3: {e}")
        return False


# ── File Security Validation ────────────────────────────────────────────────────

# Allowed extensions and their expected magic-byte signatures
_ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'txt', 'csv', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',
    'zip', 'msg', 'eml', 'rtf', 'odt', 'ods'
}

# Dangerous extensions that must never be accepted regardless of content
_BLOCKED_EXTENSIONS = {
    'exe', 'bat', 'cmd', 'com', 'msi', 'ps1', 'psm1', 'psd1',
    'vbs', 'vbe', 'js', 'jse', 'wsf', 'wsh', 'hta',
    'sh', 'bash', 'zsh', 'csh',
    'php', 'php3', 'php4', 'php5', 'phtml',
    'asp', 'aspx', 'cfm', 'cgi', 'pl', 'py', 'rb',
    'jar', 'war', 'ear', 'class',
    'dll', 'so', 'dylib', 'sys', 'drv',
    'scr', 'pif', 'lnk', 'reg', 'inf'
}

# Magic byte signatures: extension → list of (offset, bytes) tuples
_MAGIC_SIGNATURES: dict[str, list[tuple[int, bytes]]] = {
    'pdf':  [(0, b'%PDF')],
    'png':  [(0, b'\x89PNG\r\n\x1a\n')],
    'jpg':  [(0, b'\xff\xd8\xff')],
    'jpeg': [(0, b'\xff\xd8\xff')],
    'gif':  [(0, b'GIF87a'), (0, b'GIF89a')],
    'bmp':  [(0, b'BM')],
    'zip':  [(0, b'PK\x03\x04')],   # docx/xlsx/pptx/odt/ods are ZIP-based too
    'docx': [(0, b'PK\x03\x04')],
    'xlsx': [(0, b'PK\x03\x04')],
    'pptx': [(0, b'PK\x03\x04')],
    'odt':  [(0, b'PK\x03\x04')],
    'ods':  [(0, b'PK\x03\x04')],
    'doc':  [(0, b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1')],  # OLE2
    'xls':  [(0, b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1')],
    'ppt':  [(0, b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1')],
    'msg':  [(0, b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1')],
}

# Patterns that indicate script/injection content in text files
_INJECTION_PATTERNS = [
    re.compile(r'<\s*script[\s>]', re.IGNORECASE),
    re.compile(r'javascript\s*:', re.IGNORECASE),
    re.compile(r'vbscript\s*:', re.IGNORECASE),
    re.compile(r'on\w+\s*=\s*["\']', re.IGNORECASE),          # onclick=, onerror=, etc.
    re.compile(r'<\s*(iframe|object|embed|applet)', re.IGNORECASE),
    re.compile(r'\beval\s*\(', re.IGNORECASE),
    re.compile(r'\bexec\s*\(', re.IGNORECASE),
    re.compile(r'\bsystem\s*\(', re.IGNORECASE),
    re.compile(r'(?:union|select|insert|update|delete|drop|truncate)\s+\w+', re.IGNORECASE),  # SQL
    re.compile(rb'\x00{4}', re.IGNORECASE),                    # NUL byte runs (binary disguised as text)
]

# Max allowed size: 50 MB
_MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024

# Text-based extensions to scan for injection patterns
_TEXT_EXTENSIONS = {'txt', 'csv', 'rtf', 'eml', 'xml', 'html', 'htm'}


def validate_file(file_path: Path, filename: str) -> str | None:
    """
    Validate a file for security threats before uploading to S3.

    Returns None if the file is safe, or a human-readable error string if rejected.

    Checks performed:
      1. Filename sanitisation (path traversal, null bytes, suspicious chars)
      2. Blocked extension check
      3. Allowed-extension allowlist
      4. File size limit (50 MB)
      5. Magic-byte / file signature verification (type ≠ extension spoofing)
      6. Injection pattern scan for text-based files (XSS, SQLi, shell)
      7. optional - ClamAV antivirus scan ( — used only if clamd is running)
    """
    # 1. Filename sanitisation
    safe_name_check = _check_filename(filename)
    if safe_name_check:
        return safe_name_check

    ext = Path(filename).suffix.lstrip('.').lower()

    # 2. Blocked extension hard-deny
    if ext in _BLOCKED_EXTENSIONS:
        return f"File type '.{ext}' is not permitted"

    # 3. Allowlist check
    if ext not in _ALLOWED_EXTENSIONS:
        return f"File type '.{ext}' is not in the list of allowed types"

    # 4. Size check
    size = file_path.stat().st_size
    if size == 0:
        return "File is empty"
    if size > _MAX_FILE_SIZE_BYTES:
        return f"File size {size // (1024*1024)} MB exceeds the 50 MB limit"

    # 5. Magic-byte verification
    magic_error = _check_magic_bytes(file_path, ext)
    if magic_error:
        return magic_error

    # 6. Injection scan for text files
    if ext in _TEXT_EXTENSIONS:
        injection_error = _scan_for_injection(file_path)
        if injection_error:
            return injection_error

    # 7. ClamAV (optional)
    #clam_error = _scan_with_clamav(file_path)
    #if clam_error:
    #    return clam_error

    return None  # ✅ file is safe


def _check_filename(filename: str) -> str | None:
    """Reject filenames with path traversal, null bytes, or suspicious characters."""
    if not filename or filename.strip() == '':
        return "Filename is empty"
    if '\x00' in filename:
        return "Filename contains null bytes"
    if '..' in filename or '/' in filename or '\\' in filename:
        return "Filename contains path traversal characters"
    # Only allow safe characters
    if not re.match(r'^[\w\-. ()]+$', filename):
        return f"Filename contains invalid characters: {filename!r}"
    return None


def _check_magic_bytes(file_path: Path, ext: str) -> str | None:
    """Verify the file's magic bytes match its declared extension."""
    signatures = _MAGIC_SIGNATURES.get(ext)
    if not signatures:
        return None  # no signature defined for this type — skip

    try:
        header = file_path.read_bytes()[:16]
    except OSError as e:
        return f"Could not read file for signature check: {e}"

    for offset, magic in signatures:
        if header[offset: offset + len(magic)] == magic:
            return None  # matched

    return f"File content does not match declared type '.{ext}' (magic-byte mismatch)"


def _scan_for_injection(file_path: Path) -> str | None:
    """Scan a text file for XSS, SQL injection, and shell injection patterns."""
    try:
        raw = file_path.read_bytes()
        # Check binary patterns first
        for pattern in _INJECTION_PATTERNS:
            if isinstance(pattern.pattern, bytes):
                if pattern.search(raw):
                    return "File contains suspicious binary patterns"
        # Decode and check text patterns
        text = raw.decode('utf-8', errors='replace')
        for pattern in _INJECTION_PATTERNS:
            if isinstance(pattern.pattern, str) and pattern.search(text):
                return f"File contains potentially malicious content (matched: {pattern.pattern!r})"
    except OSError as e:
        return f"Could not read file for injection scan: {e}"
    return None


def _scan_with_clamav(file_path: Path) -> str | None:
    """
    Optional ClamAV antivirus scan via clamd (Unix socket or TCP).
    Silently skipped if clamd is not available.
    """
    try:
        import clamd  # pip install clamd
        # Try Unix socket first, then TCP
        try:
            cd = clamd.ClamdUnixSocket()
            cd.ping()
        except Exception:
            cd = clamd.ClamdNetworkSocket(host='127.0.0.1', port=3310)
            cd.ping()

        result = cd.scan(str(file_path))
        # result = {path: ('FOUND', 'Eicar-Test-Signature')} or {path: ('OK', None)}
        for _, (status, virus_name) in result.items():
            if status == 'FOUND':
                app_logger.warning(f"ClamAV detected virus in {file_path}: {virus_name}")
                return f"Virus detected: {virus_name}"
    except ImportError:
        pass  # clamd not installed — skip
    except Exception as e:
        app_logger.debug(f"ClamAV scan skipped (daemon unavailable): {e}")
    return None