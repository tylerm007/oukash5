import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent, DialogService } from 'ontimize-web-ngx';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'TaskInstance-detail',
  templateUrl: './TaskInstance-detail.component.html',
  styleUrls: ['./TaskInstance-detail.component.scss']
})
export class TaskInstanceDetailComponent implements OnInit  {
  protected service: OntimizeService;
  public data: any;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector,
     protected dialogService: DialogService)
  {
    this.service = this.injector.get(OntimizeService);
  }

  ngOnInit() {
    this.configureService();
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/TaskInstance';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    this.data = e
    console.log(JSON.stringify(e));
  }

  complete_task() {
    // Logic to complete the task
    console.log("Completing task...");
    const apiUrl = environment.apiEndpoint.replace('/api', '');
    console.log("API URL: " + apiUrl);
    this.service.doRequest({method: 'POST', url: apiUrl + '/complete_task', body: {task_instance_id: this.data.TaskInstanceId, result: this.data.Result}})
      .subscribe({
      next: (resp) => {
        console.log("res: " + JSON.stringify(resp));
        if (resp.code === 0) {
        console.log('task completed successfully');
        } else {
          console.error("Error completing task: " + JSON.stringify(resp.message));
          this.dialogService.info("Error completing task: ", resp.message);
        }
      },
      error: (err) => {
        if (err.status >= 400) {
          console.error("Error completing task: " + JSON.stringify(err));
          this.dialogService.info( "Unable to COMPLETE the TaskInstance.", err.error.message);
        } else {
          this.dialogService.info("Error", "An unexpected error occurred.", err);
        }
      }
      });
  }
}