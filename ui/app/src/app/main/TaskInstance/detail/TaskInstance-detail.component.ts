import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, ORealPipe, ONIFInputComponent } from 'ontimize-web-ngx';


@Component({
  selector: 'TaskInstance-detail',
  templateUrl: './TaskInstance-detail.component.html',
  styleUrls: ['./TaskInstance-detail.component.scss']
})
export class TaskInstanceDetailComponent implements OnInit  {
  protected service: OntimizeService;
  public data: any;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector) {
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
    this.service.doRequest({method: 'POST', url: 'http://localhost:5656/complete_task', body: {taskId: this.data.TaskId}}).subscribe((resp) => {
      console.log("res: " + JSON.stringify(resp));
      if (resp.code === 0) {
        console.log('task completed successfully')
      }
    });
  }
}