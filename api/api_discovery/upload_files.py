from flask import request, jsonify
import logging
import os
import json
import requests as http_requests
from database.models import WFFile
from pathlib import Path
from config.config import Args
import safrs  # circular import error if at top
from datetime import datetime
from flask_jwt_extended import get_jwt, jwt_required
from security.system.authorization import Security
from database.models import TaskInstance

app_logger = logging.getLogger("api_logic_server_app")
session = safrs.DB.session

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

            app_logger.info(f"File uploaded successfully: {temp_file_path}")
            application_id = task_instance.ApplicationId
            file_type = filename.split('.')[-1] if '.' in filename else 'txt'
            wf_file = WFFile(
                FileName    = filename,
                FilePath    = str(temp_file_path),
                FileType    = file_type,
                FileSize    = content_length,
                UploadedDate= datetime.now(),
                ApplicationID = application_id,
                Tag         = description or None,
                CreatedBy   = user
            )
            

           
            completed_by = request.form.get("completed_by",user)
            capacity = request.form.get("capacity", None) # "S/B ADMIN, MEMBER, DESIGNATED"
            completion_notes = f"File uploaded: {filename}"
            result = request.form.get("result", None)
            access_token = request.headers.get("Authorization")
            
            #done = write_to_s3(temp_file_path, Args.S3_BUCKET_NAME, f"uploads/{application_id}/{filename}")
            #wf_file.FilePath = f"s3://{Args.S3_BUCKET_NAME}/uploads/{application_id}/{filename}"
            session.add(wf_file)
            #if done:
                #temp_file_path.unlink(missing_ok=True)

            from api.api_discovery.complete_task import _complete_task
            _complete_task(task_instance_id, result=result,  completed_by= completed_by, completion_notes= completion_notes, access_token=access_token, capacity= capacity, depth=0)
            session.commit()


            return jsonify({
                "message"  : "File uploaded successfully",
                "file_path": str(temp_file_path),
                "file_id"  : wf_file.FileID
            }), 200

        except Exception as e:
            app_logger.error(f"Error uploading file: {e}")
            return jsonify({"error": "An error occurred while uploading the file", "detail": str(e)}), 500
        
def write_to_s3(file_path, bucket_name, s3_key):
    """Utility function to upload a file to AWS S3"""
    import boto3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(str(file_path), bucket_name, s3_key)
        app_logger.info(f"File {file_path} uploaded to S3 bucket {bucket_name} with key {s3_key}")
        return True
    except Exception as e:
        app_logger.error(f"Error uploading file to S3: {e}")
        return False    