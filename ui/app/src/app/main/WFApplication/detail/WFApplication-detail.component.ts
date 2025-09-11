import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, SnackBarService, OSnackBarConfig, DialogService } from 'ontimize-web-ngx';
import { environment } from '../../../../environments/environment';

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
    protected dialogService: DialogService)
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
    const apiUrl = environment.apiEndpoint.replace('/api', '');
    console.log("API URL: " + apiUrl);
    this.service.doRequest({method: 'POST', url: apiUrl + '/start_workflow', body: { application_id: this.data.ApplicationID }}).subscribe((resp) => {
      console.log("res: " + JSON.stringify(resp));
      if (resp.code === 0) {
        console.log('workflow started successfully')
        this.showInfo();
      } else {
        this.dialogService.info("Error starting workflow: ", resp.message);
      }
    });
  }

  showInfo() {
    if (this.dialogService) {
      this.dialogService.info('Workflow Started',
        'The workflow has been started successfully',);
    }
  }
}