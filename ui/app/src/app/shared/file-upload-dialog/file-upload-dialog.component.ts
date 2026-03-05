import {
  Component,
  Inject,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';

export interface FileUploadDialogData {
  appId?: number | string;
  description?: string;
}

@Component({
  selector: 'app-file-upload-dialog',
  templateUrl: './file-upload-dialog.component.html',
  styleUrls: ['./file-upload-dialog.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class FileUploadDialogComponent implements OnInit {

  appId: number | string = '';
  description: string = '';
  fileUrl: string = '';
  selectedFile: File | null = null;
  isDragging = false;
  isUploading = false;
  errorMessage = '';

  constructor(
    public dialogRef: MatDialogRef<FileUploadDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: FileUploadDialogData,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    if (this.data) {
      this.appId = this.data.appId ?? '';
      this.description = this.data.description ?? '';
    }
  }

  // ── Drag & Drop ─────────────────────────────────────────────────────────────

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
    this.errorMessage = '';
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.fileUrl = '';
    }
  }

  // ── Browse (click) ───────────────────────────────────────────────────────────

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.fileUrl = '';
      this.errorMessage = '';
    }
  }

  // ── URL input ────────────────────────────────────────────────────────────────

  onUrlChange(): void {
    if (this.fileUrl.trim()) {
      this.selectedFile = null;
      this.errorMessage = '';
    }
  }

  // ── Helpers ──────────────────────────────────────────────────────────────────

  formatFileSize(bytes: number): string {
    if (bytes === 0) { return '0 B'; }
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  // ── Submit ───────────────────────────────────────────────────────────────────

  onSubmit(): void {
    this.errorMessage = '';

    if (!this.selectedFile && !this.fileUrl.trim()) {
      this.errorMessage = 'Please select a file or provide a URL.';
      return;
    }

    this.isUploading = true;

    const apiBase = environment.apiEndpoint.replace('/api', '');
    const uploadUrl = `${apiBase}/upload_files`;

    const formData = new FormData();

    if (this.selectedFile) {
      formData.append('file', this.selectedFile, this.selectedFile.name);
    } else {
      // URL-based: create a synthetic Blob that the backend can handle
      // by passing the URL as a form field so the backend can fetch it
      formData.append('file_url', this.fileUrl.trim());
      // Also append a placeholder file name derived from the URL
      const urlFileName = this.fileUrl.trim().split('/').pop() || 'linked_file';
      formData.append('file_name', urlFileName);
    }

    if (this.appId !== '' && this.appId !== null && this.appId !== undefined) {
      formData.append('task_instance_id', String(this.appId));
    }

    if (this.description.trim()) {
      formData.append('description', this.description.trim());
    }

    // Auth token is injected automatically by AuthInterceptor
    this.http.post(uploadUrl, formData).subscribe({
      next: (response: any) => {
        this.isUploading = false;
        this.dialogRef.close({ success: true, response });
      },
      error: (err) => {
        this.isUploading = false;
        this.errorMessage =
          err?.error?.error || err?.message || 'Upload failed. Please try again.';
      }
    });
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
