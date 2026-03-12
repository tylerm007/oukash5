import { Injector, ViewChild, Component, OnInit } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent } from 'ontimize-web-ngx';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

const IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'];

@Component({
  selector: 'WFFile-detail',
  templateUrl: './WFFile-detail.component.html',
  styleUrls: ['./WFFile-detail.component.scss']
})
export class WFFileDetailComponent implements OnInit  {
  protected service: OntimizeService;

  @ViewChild('oDetailForm') form: OFormComponent;

  constructor(protected injector: Injector, private http: HttpClient) {
    this.service = this.injector.get(OntimizeService);
  }

  ngOnInit() {
    this.configureService();
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/WFFile';
    this.service.configureService(conf);
  }

  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
  }

  openFileUrl() {
    const fileId = this.form.getFieldValue('FileID');
    if (!fileId) {
      return;
    }
    const filename: string = this.form.getFieldValue('FileName') || '';
    const ext = filename.split('.').pop()?.toLowerCase() ?? '';
    const apiUrl = environment.apiEndpoint.replace('/api', '');
    const token = localStorage.getItem('cognito_access_token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    console.log("Extension:", ext)
    // Open the tab synchronously (before the async HTTP call) so popup
    // blockers don't suppress it — then navigate it once the blob arrives.
    const tab = window.open('', '_blank');
    if (!tab) {
      console.error('Popup blocked — allow popups for this site and try again.');
      return;
    }
    tab.document.write('<html><body style="background:#111;color:#fff;font-family:sans-serif;padding:2rem;">Loading file…</body></html>');

    // Fetch via HttpClient so the auth interceptor / manual header is sent,
    // then create a local blob URL the browser can display without CORS issues.
    this.http.get(`${apiUrl}/file_proxy/${fileId}`, { headers, responseType: 'blob' })
      .subscribe({
        next: (blob) => {
          console.log('File blob received from proxy:', blob);
          const objectUrl = URL.createObjectURL(blob);

          if (ext === 'pdf') {
            tab.location.href = objectUrl;
          } else if (IMAGE_EXTENSIONS.includes(ext)) {
            console.log('Displaying image in new tab');
            tab.document.open();
            tab.document.write(
              `<html><head><title>${filename}</title></head>` +
              `<body style="margin:0;background:#111;display:flex;justify-content:center;align-items:center;min-height:100vh;">` +
              `<img src="${objectUrl}" alt="${filename}" style="max-width:100%;max-height:100vh;object-fit:contain;">` +
              `</body></html>`
            );
            tab.document.close();
          } else {
            console.log('Triggering download for non-viewable file');
            // Non-viewable (Word, Excel, zip…) — trigger download via temp <a>
            tab.document.open();
            tab.document.write('<html><body></body></html>');
            tab.document.close();
            const a = tab.document.createElement('a');
            a.href = objectUrl;
            a.download = filename;
            tab.document.body.appendChild(a);
            a.click();
          }
        },
        error: (err) => {
          console.error('Failed to fetch file via proxy:', err);
          tab.document.open();
          tab.document.write('<html><body style="color:red;font-family:sans-serif;padding:2rem;">Failed to load file. Please try again.</body></html>');
          tab.document.close();
        }
      });
  }

}