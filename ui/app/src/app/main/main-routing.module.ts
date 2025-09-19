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
      
    
        { path: 'COMPANYADDRESSTB', loadChildren: () => import('./COMPANYADDRESSTB/COMPANYADDRESSTB.module').then(m => m.COMPANYADDRESSTBModule) },
    
        { path: 'COMPANYTB', loadChildren: () => import('./COMPANYTB/COMPANYTB.module').then(m => m.COMPANYTBModule) },
    
        { path: 'CompanyApplication', loadChildren: () => import('./CompanyApplication/CompanyApplication.module').then(m => m.CompanyApplicationModule) },
    
        { path: 'FormulaProduct', loadChildren: () => import('./FormulaProduct/FormulaProduct.module').then(m => m.FormulaProductModule) },
    
        { path: 'FormulaSubmissionComponent', loadChildren: () => import('./FormulaSubmissionComponent/FormulaSubmissionComponent.module').then(m => m.FormulaSubmissionComponentModule) },
    
        { path: 'FormulaSubmissionPlant', loadChildren: () => import('./FormulaSubmissionPlant/FormulaSubmissionPlant.module').then(m => m.FormulaSubmissionPlantModule) },
    
        { path: 'LabelTb', loadChildren: () => import('./LabelTb/LabelTb.module').then(m => m.LabelTbModule) },
    
        { path: 'LaneDefinition', loadChildren: () => import('./LaneDefinition/LaneDefinition.module').then(m => m.LaneDefinitionModule) },
    
        { path: 'LaneRole', loadChildren: () => import('./LaneRole/LaneRole.module').then(m => m.LaneRoleModule) },
        { path: 'MERCHTB', loadChildren: () => import('./MERCHTB/MERCHTB.module').then(m => m.MERCHTBModule) },
    
        { path: 'OWNSTB', loadChildren: () => import('./OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule) },
    
        { path: 'PLANTADDRESSTB', loadChildren: () => import('./PLANTADDRESSTB/PLANTADDRESSTB.module').then(m => m.PLANTADDRESSTBModule) },
    
        { path: 'PLANTCERTDETAIL', loadChildren: () => import('./PLANTCERTDETAIL/PLANTCERTDETAIL.module').then(m => m.PLANTCERTDETAILModule) },
    
        { path: 'PLANTCOMMENT', loadChildren: () => import('./PLANTCOMMENT/PLANTCOMMENT.module').then(m => m.PLANTCOMMENTModule) },
    
        { path: 'PLANTTB', loadChildren: () => import('./PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule) },
    
    
        { path: 'ProcessDefinition', loadChildren: () => import('./ProcessDefinition/ProcessDefinition.module').then(m => m.ProcessDefinitionModule) },
    
        { path: 'ProcessInstance', loadChildren: () => import('./ProcessInstance/ProcessInstance.module').then(m => m.ProcessInstanceModule) },
    
        { path: 'ProcessMessage', loadChildren: () => import('./ProcessMessage/ProcessMessage.module').then(m => m.ProcessMessageModule) },
    
        { path: 'ProcessMessageType', loadChildren: () => import('./ProcessMessageType/ProcessMessageType.module').then(m => m.ProcessMessageTypeModule) },
    
        { path: 'ProcessPriority', loadChildren: () => import('./ProcessPriority/ProcessPriority.module').then(m => m.ProcessPriorityModule) },
    
        { path: 'ProcessStatus', loadChildren: () => import('./ProcessStatus/ProcessStatus.module').then(m => m.ProcessStatusModule) },
    
        { path: 'ProducedIn1Tb', loadChildren: () => import('./ProducedIn1Tb/ProducedIn1Tb.module').then(m => m.ProducedIn1TbModule) },
    
        { path: 'RoleAssigment', loadChildren: () => import('./RoleAssigment/RoleAssigment.module').then(m => m.RoleAssigmentModule) },
    
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
    
        { path: 'USEDIN1TB', loadChildren: () => import('./USEDIN1TB/USEDIN1TB.module').then(m => m.USEDIN1TBModule) },
    
        { path: 'WFActivityLog', loadChildren: () => import('./WFActivityLog/WFActivityLog.module').then(m => m.WFActivityLogModule) },
    
        { path: 'WFActivityStatus', loadChildren: () => import('./WFActivityStatus/WFActivityStatus.module').then(m => m.WFActivityStatusModule) },
    
        { path: 'WFApplication', loadChildren: () => import('./WFApplication/WFApplication.module').then(m => m.WFApplicationModule) },
    
        { path: 'WFApplicationComment', loadChildren: () => import('./WFApplicationComment/WFApplicationComment.module').then(m => m.WFApplicationCommentModule) },
    
        { path: 'WFApplicationMessage', loadChildren: () => import('./WFApplicationMessage/WFApplicationMessage.module').then(m => m.WFApplicationMessageModule) },
    
        { path: 'WFApplicationStatus', loadChildren: () => import('./WFApplicationStatus/WFApplicationStatus.module').then(m => m.WFApplicationStatusModule) },
    
        { path: 'WFCompany', loadChildren: () => import('./WFCompany/WFCompany.module').then(m => m.WFCompanyModule) },
    
        { path: 'WFContact', loadChildren: () => import('./WFContact/WFContact.module').then(m => m.WFContactModule) },
    
        { path: 'WFDashboard', loadChildren: () => import('./WFDashboard/WFDashboard.module').then(m => m.WFDashboardModule) },
    
        { path: 'WFFile', loadChildren: () => import('./WFFile/WFFile.module').then(m => m.WFFileModule) },
    
        { path: 'WFFileType', loadChildren: () => import('./WFFileType/WFFileType.module').then(m => m.WFFileTypeModule) },
    
        { path: 'WFIngredient', loadChildren: () => import('./WFIngredient/WFIngredient.module').then(m => m.WFIngredientModule) },
    
        { path: 'WFPriority', loadChildren: () => import('./WFPriority/WFPriority.module').then(m => m.WFPriorityModule) },
    
        { path: 'WFProduct', loadChildren: () => import('./WFProduct/WFProduct.module').then(m => m.WFProductModule) },
    
        { path: 'WFQuote', loadChildren: () => import('./WFQuote/WFQuote.module').then(m => m.WFQuoteModule) },
    
        { path: 'WFQuoteItem', loadChildren: () => import('./WFQuoteItem/WFQuoteItem.module').then(m => m.WFQuoteItemModule) },
    
        { path: 'WFQuoteStatus', loadChildren: () => import('./WFQuoteStatus/WFQuoteStatus.module').then(m => m.WFQuoteStatusModule) },
    
        { path: 'WFRole', loadChildren: () => import('./WFRole/WFRole.module').then(m => m.WFRoleModule) },
    
        { path: 'WFUser', loadChildren: () => import('./WFUser/WFUser.module').then(m => m.WFUserModule) },
    
        { path: 'WorkflowHistory', loadChildren: () => import('./WorkflowHistory/WorkflowHistory.module').then(m => m.WorkflowHistoryModule) },
    
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }