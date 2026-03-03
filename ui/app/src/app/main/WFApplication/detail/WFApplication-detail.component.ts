import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, SnackBarService, OSnackBarConfig, DialogService } from 'ontimize-web-ngx';
import { MatDialog } from '@angular/material/dialog';
import { environment } from '../../../../environments/environment';
import { FileUploadDialogComponent } from '../../../shared/file-upload-dialog/file-upload-dialog.component';

@Component({
  selector: 'WFApplication-detail',
  templateUrl: './WFApplication-detail.component.html',
  styleUrls: ['./WFApplication-detail.component.scss']
})
export class WFApplicationDetailComponent implements OnInit  {
  protected service: OntimizeService;
  public data: any;
  public snackBarService: SnackBarService;
  public snackBarConfig: OSnackBarConfig;
  
  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector,
    protected dialogService: DialogService,
    protected matDialog: MatDialog)
  {
    this.service = this.injector.get(OntimizeService);
    this.snackBarService = this.injector.get(SnackBarService);
    this.snackBarConfig = this.injector.get(OSnackBarConfig);
  }

  ngOnInit() {
    this.configureService();
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/WFApplication';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    this.data = e;
    console.log(JSON.stringify(e));
  }
  start_workflow() {
    // Implement workflow start logic here
    console.log("Starting workflow...");
    const configuration: OSnackBarConfig = {
      action: 'Ok',
      milliseconds: 8000,
      icon: 'check_circle',
      iconPosition: 'left'
    }
    this.snackBarService.open("Please wait, Starting Workflow ...", configuration);
    const isProduction = environment.production;
    console.log("Environment is production: " + isProduction);
    //const apiEndpoint = isProduction ? environment.apiEndpoint : environment.prod;
    const apiUrl = environment.apiEndpoint.replace('/api', '');
    const payload =  { 
      "application_id": this.data.ApplicationID, 
      "process_name": "OU Application Init",
      "priority": this.data.Priority 
    }
    console.log("API URL: " + apiUrl, " Payload: " + JSON.stringify(payload));
    this.service.doRequest({method: 'POST', url: apiUrl + '/start_workflow_fast', body:JSON.stringify(payload)}).subscribe(
      (resp) => {
      console.log("res: " + JSON.stringify(resp));
      if (resp.code === 200) {
        console.log('workflow started successfully')
        this.showInfo();
      } else {
        this.dialogService.info("Error starting workflow: ", resp.message);
      }
      },
      (error) => {
      console.error("Error: " + JSON.stringify(error));
      const errorMessage = error.status === 500 ? 'Server error occurred. Please try again later.' : error.error.message;
      this.dialogService.info("Error starting workflow: ", errorMessage);
      }
    );
  }

  showInfo() {
    if (this.dialogService) {
      this.dialogService.info('Workflow Started',
        'The workflow has been started successfully',);
    }
  }

  openUploadDialog(): void {
    const dialogRef = this.matDialog.open(FileUploadDialogComponent, {
      width: '560px',
      disableClose: false,
      data: {
        appId: this.data?.ApplicationID ?? '',
        description: ''
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result?.success) {
        const config: OSnackBarConfig = {
          action: 'Ok',
          milliseconds: 6000,
          icon: 'check_circle',
          iconPosition: 'left'
        };
        this.snackBarService.open('File uploaded successfully.', config);
      }
    });
  }
}