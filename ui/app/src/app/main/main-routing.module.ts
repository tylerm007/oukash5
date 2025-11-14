import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main.component';

export const routes: Routes = [
  {
    path: '', component: MainComponent,
    children: [
        { path: '', redirectTo: 'home', pathMatch: 'full' },
        { path: 'about', loadChildren: () => import('./about/about.module').then(m => m.AboutModule) },
        { path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomeModule) },
        { path: 'settings', loadChildren: () => import('./settings/settings.module').then(m => m.SettingsModule) },
      
    
        { path: 'EventAction', loadChildren: () => import('./EventAction/EventAction.module').then(m => m.EventActionModule) },
    
        { path: 'LaneDefinition', loadChildren: () => import('./LaneDefinition/LaneDefinition.module').then(m => m.LaneDefinitionModule) },
    
        { path: 'LaneRole', loadChildren: () => import('./LaneRole/LaneRole.module').then(m => m.LaneRoleModule) },
    
        { path: 'ProcessDefinition', loadChildren: () => import('./ProcessDefinition/ProcessDefinition.module').then(m => m.ProcessDefinitionModule) },
    
        { path: 'ProcessMessageType', loadChildren: () => import('./ProcessMessageType/ProcessMessageType.module').then(m => m.ProcessMessageTypeModule) },
    
        { path: 'RoleAssignment', loadChildren: () => import('./RoleAssignment/RoleAssignment.module').then(m => m.RoleAssignmentModule) },
    
        { path: 'StageDefinition', loadChildren: () => import('./StageDefinition/StageDefinition.module').then(m => m.StageDefinitionModule) },
    
        { path: 'StageInstance', loadChildren: () => import('./StageInstance/StageInstance.module').then(m => m.StageInstanceModule) },
    
        { path: 'StageStatus', loadChildren: () => import('./StageStatus/StageStatus.module').then(m => m.StageStatusModule) },
    
        { path: 'TaskCategory', loadChildren: () => import('./TaskCategory/TaskCategory.module').then(m => m.TaskCategoryModule) },
    
        { path: 'TaskComment', loadChildren: () => import('./TaskComment/TaskComment.module').then(m => m.TaskCommentModule) },
    
        { path: 'TaskCommentType', loadChildren: () => import('./TaskCommentType/TaskCommentType.module').then(m => m.TaskCommentTypeModule) },
    
        { path: 'TaskDefinition', loadChildren: () => import('./TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule) },
    
        { path: 'TaskFlow', loadChildren: () => import('./TaskFlow/TaskFlow.module').then(m => m.TaskFlowModule) },
    
        { path: 'TaskInstance', loadChildren: () => import('./TaskInstance/TaskInstance.module').then(m => m.TaskInstanceModule) },
    
        { path: 'TaskStatus', loadChildren: () => import('./TaskStatus/TaskStatus.module').then(m => m.TaskStatusModule) },
    
        { path: 'TaskType', loadChildren: () => import('./TaskType/TaskType.module').then(m => m.TaskTypeModule) },
    
        { path: 'WFActivityLog', loadChildren: () => import('./WFActivityLog/WFActivityLog.module').then(m => m.WFActivityLogModule) },
    
        { path: 'WFActivityStatus', loadChildren: () => import('./WFActivityStatus/WFActivityStatus.module').then(m => m.WFActivityStatusModule) },
    
        { path: 'WFApplication', loadChildren: () => import('./WFApplication/WFApplication.module').then(m => m.WFApplicationModule) },
    
        { path: 'WFApplicationMessage', loadChildren: () => import('./WFApplicationMessage/WFApplicationMessage.module').then(m => m.WFApplicationMessageModule) },
    
        { path: 'WFApplicationStatus', loadChildren: () => import('./WFApplicationStatus/WFApplicationStatus.module').then(m => m.WFApplicationStatusModule) },
    
        { path: 'WFFile', loadChildren: () => import('./WFFile/WFFile.module').then(m => m.WFFileModule) },
    
        { path: 'WFFileType', loadChildren: () => import('./WFFileType/WFFileType.module').then(m => m.WFFileTypeModule) },
    
        { path: 'WFPriority', loadChildren: () => import('./WFPriority/WFPriority.module').then(m => m.WFPriorityModule) },
    
        { path: 'WFQuote', loadChildren: () => import('./WFQuote/WFQuote.module').then(m => m.WFQuoteModule) },
    
        { path: 'WFQuoteItem', loadChildren: () => import('./WFQuoteItem/WFQuoteItem.module').then(m => m.WFQuoteItemModule) },
    
        { path: 'WFQuoteStatus', loadChildren: () => import('./WFQuoteStatus/WFQuoteStatus.module').then(m => m.WFQuoteStatusModule) },
    
        { path: 'WFRole', loadChildren: () => import('./WFRole/WFRole.module').then(m => m.WFRoleModule) },
    
        { path: 'WFUser', loadChildren: () => import('./WFUser/WFUser.module').then(m => m.WFUserModule) },
    
        { path: 'WFUserAdmin', loadChildren: () => import('./WFUserAdmin/WFUserAdmin.module').then(m => m.WFUserAdminModule) },
    
        { path: 'WFUserRole', loadChildren: () => import('./WFUserRole/WFUserRole.module').then(m => m.WFUserRoleModule) },
    
        { path: 'WorkflowHistory', loadChildren: () => import('./WorkflowHistory/WorkflowHistory.module').then(m => m.WorkflowHistoryModule) },
    
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }