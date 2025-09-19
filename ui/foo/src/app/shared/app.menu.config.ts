import { MenuRootItem } from 'ontimize-web-ngx';

import { COMPANYADDRESSTBCardComponent } from './COMPANYADDRESSTB-card/COMPANYADDRESSTB-card.component';

import { COMPANYTBCardComponent } from './COMPANYTB-card/COMPANYTB-card.component';

import { CompanyApplicationCardComponent } from './CompanyApplication-card/CompanyApplication-card.component';

import { FormulaProductCardComponent } from './FormulaProduct-card/FormulaProduct-card.component';

import { FormulaSubmissionComponentCardComponent } from './FormulaSubmissionComponent-card/FormulaSubmissionComponent-card.component';

import { FormulaSubmissionPlantCardComponent } from './FormulaSubmissionPlant-card/FormulaSubmissionPlant-card.component';

import { LabelTbCardComponent } from './LabelTb-card/LabelTb-card.component';

import { LaneDefinitionCardComponent } from './LaneDefinition-card/LaneDefinition-card.component';

import { MERCHTBCardComponent } from './MERCHTB-card/MERCHTB-card.component';

import { OWNSTBCardComponent } from './OWNSTB-card/OWNSTB-card.component';

import { PLANTADDRESSTBCardComponent } from './PLANTADDRESSTB-card/PLANTADDRESSTB-card.component';

import { PLANTCERTDETAILCardComponent } from './PLANTCERTDETAIL-card/PLANTCERTDETAIL-card.component';

import { PLANTCOMMENTCardComponent } from './PLANTCOMMENT-card/PLANTCOMMENT-card.component';

import { PLANTTBCardComponent } from './PLANTTB-card/PLANTTB-card.component';

import { ProcessDefinitionCardComponent } from './ProcessDefinition-card/ProcessDefinition-card.component';

import { ProcessInstanceCardComponent } from './ProcessInstance-card/ProcessInstance-card.component';

import { ProcessMessageCardComponent } from './ProcessMessage-card/ProcessMessage-card.component';

import { ProcessMessageTypeCardComponent } from './ProcessMessageType-card/ProcessMessageType-card.component';

import { ProcessPriorityCardComponent } from './ProcessPriority-card/ProcessPriority-card.component';

import { ProcessStatusCardComponent } from './ProcessStatus-card/ProcessStatus-card.component';

import { ProducedIn1TbCardComponent } from './ProducedIn1Tb-card/ProducedIn1Tb-card.component';

import { RoleAssigmentCardComponent } from './RoleAssigment-card/RoleAssigment-card.component';

import { StageInstanceCardComponent } from './StageInstance-card/StageInstance-card.component';

import { StageStatusCardComponent } from './StageStatus-card/StageStatus-card.component';

import { TaskCategoryCardComponent } from './TaskCategory-card/TaskCategory-card.component';

import { TaskCommentCardComponent } from './TaskComment-card/TaskComment-card.component';

import { TaskCommentTypeCardComponent } from './TaskCommentType-card/TaskCommentType-card.component';

import { TaskDefinitionCardComponent } from './TaskDefinition-card/TaskDefinition-card.component';

import { TaskFlowCardComponent } from './TaskFlow-card/TaskFlow-card.component';

import { TaskInstanceCardComponent } from './TaskInstance-card/TaskInstance-card.component';

import { TaskStatusCardComponent } from './TaskStatus-card/TaskStatus-card.component';

import { TaskTypeCardComponent } from './TaskType-card/TaskType-card.component';

import { USEDIN1TBCardComponent } from './USEDIN1TB-card/USEDIN1TB-card.component';

import { WFActivityLogCardComponent } from './WFActivityLog-card/WFActivityLog-card.component';

import { WFActivityStatusCardComponent } from './WFActivityStatus-card/WFActivityStatus-card.component';

import { WFApplicationCardComponent } from './WFApplication-card/WFApplication-card.component';

import { WFApplicationCommentCardComponent } from './WFApplicationComment-card/WFApplicationComment-card.component';

import { WFApplicationMessageCardComponent } from './WFApplicationMessage-card/WFApplicationMessage-card.component';

import { WFApplicationStatusCardComponent } from './WFApplicationStatus-card/WFApplicationStatus-card.component';

import { WFCompanyCardComponent } from './WFCompany-card/WFCompany-card.component';

import { WFContactCardComponent } from './WFContact-card/WFContact-card.component';

import { WFDashboardCardComponent } from './WFDashboard-card/WFDashboard-card.component';

import { WFFileCardComponent } from './WFFile-card/WFFile-card.component';

import { WFFileTypeCardComponent } from './WFFileType-card/WFFileType-card.component';

import { WFIngredientCardComponent } from './WFIngredient-card/WFIngredient-card.component';

import { WFPriorityCardComponent } from './WFPriority-card/WFPriority-card.component';

import { WFProductCardComponent } from './WFProduct-card/WFProduct-card.component';

import { WFQuoteCardComponent } from './WFQuote-card/WFQuote-card.component';

import { WFQuoteItemCardComponent } from './WFQuoteItem-card/WFQuoteItem-card.component';

import { WFQuoteStatusCardComponent } from './WFQuoteStatus-card/WFQuoteStatus-card.component';

import { WFRoleCardComponent } from './WFRole-card/WFRole-card.component';

import { WFUserCardComponent } from './WFUser-card/WFUser-card.component';

import { WorkflowHistoryCardComponent } from './WorkflowHistory-card/WorkflowHistory-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    
    {
    id: 'data', name: ' data', icon: 'remove_red_eye', opened: true,
    items: [
    
        { id: 'COMPANYADDRESSTB', name: 'COMPANYADDRESSTB', icon: 'view_list', route: '/main/COMPANYADDRESSTB' }
    
        ,{ id: 'COMPANYTB', name: 'COMPANYTB', icon: 'view_list', route: '/main/COMPANYTB' }
    
        ,{ id: 'CompanyApplication', name: 'COMPANYAPPLICATION', icon: 'view_list', route: '/main/CompanyApplication' }
    
        ,{ id: 'FormulaProduct', name: 'FORMULAPRODUCT', icon: 'view_list', route: '/main/FormulaProduct' }
    
        ,{ id: 'FormulaSubmissionComponent', name: 'FORMULASUBMISSIONCOMPONENT', icon: 'view_list', route: '/main/FormulaSubmissionComponent' }
    
        ,{ id: 'FormulaSubmissionPlant', name: 'FORMULASUBMISSIONPLANT', icon: 'view_list', route: '/main/FormulaSubmissionPlant' }
    
        ,{ id: 'LabelTb', name: 'LABELTB', icon: 'view_list', route: '/main/LabelTb' }
    
        ,{ id: 'LaneDefinition', name: 'LANEDEFINITION', icon: 'view_list', route: '/main/LaneDefinition' }
    
        ,{ id: 'MERCHTB', name: 'MERCHTB', icon: 'view_list', route: '/main/MERCHTB' }
    
        ,{ id: 'OWNSTB', name: 'OWNSTB', icon: 'view_list', route: '/main/OWNSTB' }
    
        ,{ id: 'PLANTADDRESSTB', name: 'PLANTADDRESSTB', icon: 'view_list', route: '/main/PLANTADDRESSTB' }
    
        ,{ id: 'PLANTCERTDETAIL', name: 'PLANTCERTDETAIL', icon: 'view_list', route: '/main/PLANTCERTDETAIL' }
    
        ,{ id: 'PLANTCOMMENT', name: 'PLANTCOMMENT', icon: 'view_list', route: '/main/PLANTCOMMENT' }
    
        ,{ id: 'PLANTTB', name: 'PLANTTB', icon: 'view_list', route: '/main/PLANTTB' }
    
        ,{ id: 'ProcessDefinition', name: 'PROCESSDEFINITION', icon: 'view_list', route: '/main/ProcessDefinition' }
    
        ,{ id: 'ProcessInstance', name: 'PROCESSINSTANCE', icon: 'view_list', route: '/main/ProcessInstance' }
    
        ,{ id: 'ProcessMessage', name: 'PROCESSMESSAGE', icon: 'view_list', route: '/main/ProcessMessage' }
    
        ,{ id: 'ProcessMessageType', name: 'PROCESSMESSAGETYPE', icon: 'view_list', route: '/main/ProcessMessageType' }
    
        ,{ id: 'ProcessPriority', name: 'PROCESSPRIORITY', icon: 'view_list', route: '/main/ProcessPriority' }
    
        ,{ id: 'ProcessStatus', name: 'PROCESSSTATUS', icon: 'view_list', route: '/main/ProcessStatus' }
    
        ,{ id: 'ProducedIn1Tb', name: 'PRODUCEDIN1TB', icon: 'view_list', route: '/main/ProducedIn1Tb' }
    
        ,{ id: 'RoleAssigment', name: 'ROLEASSIGMENT', icon: 'view_list', route: '/main/RoleAssigment' }
    
        ,{ id: 'StageInstance', name: 'STAGEINSTANCE', icon: 'view_list', route: '/main/StageInstance' }
    
        ,{ id: 'StageStatus', name: 'STAGESTATUS', icon: 'view_list', route: '/main/StageStatus' }
    
        ,{ id: 'TaskCategory', name: 'TASKCATEGORY', icon: 'view_list', route: '/main/TaskCategory' }
    
        ,{ id: 'TaskComment', name: 'TASKCOMMENT', icon: 'view_list', route: '/main/TaskComment' }
    
        ,{ id: 'TaskCommentType', name: 'TASKCOMMENTTYPE', icon: 'view_list', route: '/main/TaskCommentType' }
    
        ,{ id: 'TaskDefinition', name: 'TASKDEFINITION', icon: 'view_list', route: '/main/TaskDefinition' }
    
        ,{ id: 'TaskFlow', name: 'TASKFLOW', icon: 'view_list', route: '/main/TaskFlow' }
    
        ,{ id: 'TaskInstance', name: 'TASKINSTANCE', icon: 'view_list', route: '/main/TaskInstance' }
    
        ,{ id: 'TaskStatus', name: 'TASKSTATUS', icon: 'view_list', route: '/main/TaskStatus' }
    
        ,{ id: 'TaskType', name: 'TASKTYPE', icon: 'view_list', route: '/main/TaskType' }
    
        ,{ id: 'USEDIN1TB', name: 'USEDIN1TB', icon: 'view_list', route: '/main/USEDIN1TB' }
    
        ,{ id: 'WFActivityLog', name: 'WFACTIVITYLOG', icon: 'view_list', route: '/main/WFActivityLog' }
    
        ,{ id: 'WFActivityStatus', name: 'WFACTIVITYSTATUS', icon: 'view_list', route: '/main/WFActivityStatus' }
    
        ,{ id: 'WFApplication', name: 'WFAPPLICATION', icon: 'view_list', route: '/main/WFApplication' }
    
        ,{ id: 'WFApplicationComment', name: 'WFAPPLICATIONCOMMENT', icon: 'view_list', route: '/main/WFApplicationComment' }
    
        ,{ id: 'WFApplicationMessage', name: 'WFAPPLICATIONMESSAGE', icon: 'view_list', route: '/main/WFApplicationMessage' }
    
        ,{ id: 'WFApplicationStatus', name: 'WFAPPLICATIONSTATUS', icon: 'view_list', route: '/main/WFApplicationStatus' }
    
        ,{ id: 'WFCompany', name: 'WFCOMPANY', icon: 'view_list', route: '/main/WFCompany' }
    
        ,{ id: 'WFContact', name: 'WFCONTACT', icon: 'view_list', route: '/main/WFContact' }
    
        ,{ id: 'WFDashboard', name: 'WFDASHBOARD', icon: 'view_list', route: '/main/WFDashboard' }
    
        ,{ id: 'WFFile', name: 'WFFILE', icon: 'view_list', route: '/main/WFFile' }
    
        ,{ id: 'WFFileType', name: 'WFFILETYPE', icon: 'view_list', route: '/main/WFFileType' }
    
        ,{ id: 'WFIngredient', name: 'WFINGREDIENT', icon: 'view_list', route: '/main/WFIngredient' }
    
        ,{ id: 'WFPriority', name: 'WFPRIORITY', icon: 'view_list', route: '/main/WFPriority' }
    
        ,{ id: 'WFProduct', name: 'WFPRODUCT', icon: 'view_list', route: '/main/WFProduct' }
    
        ,{ id: 'WFQuote', name: 'WFQUOTE', icon: 'view_list', route: '/main/WFQuote' }
    
        ,{ id: 'WFQuoteItem', name: 'WFQUOTEITEM', icon: 'view_list', route: '/main/WFQuoteItem' }
    
        ,{ id: 'WFQuoteStatus', name: 'WFQUOTESTATUS', icon: 'view_list', route: '/main/WFQuoteStatus' }
    
        ,{ id: 'WFRole', name: 'WFROLE', icon: 'view_list', route: '/main/WFRole' }
    
        ,{ id: 'WFUser', name: 'WFUSER', icon: 'view_list', route: '/main/WFUser' }
    
        ,{ id: 'WorkflowHistory', name: 'WORKFLOWHISTORY', icon: 'view_list', route: '/main/WorkflowHistory' }
    
    ] 
},
    
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings'}
    ,{ id: 'about', name: 'About', icon: 'info', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    COMPANYADDRESSTBCardComponent

    ,COMPANYTBCardComponent

    ,CompanyApplicationCardComponent

    ,FormulaProductCardComponent

    ,FormulaSubmissionComponentCardComponent

    ,FormulaSubmissionPlantCardComponent

    ,LabelTbCardComponent

    ,LaneDefinitionCardComponent

    ,MERCHTBCardComponent

    ,OWNSTBCardComponent

    ,PLANTADDRESSTBCardComponent

    ,PLANTCERTDETAILCardComponent

    ,PLANTCOMMENTCardComponent

    ,PLANTTBCardComponent

    ,ProcessDefinitionCardComponent

    ,ProcessInstanceCardComponent

    ,ProcessMessageCardComponent

    ,ProcessMessageTypeCardComponent

    ,ProcessPriorityCardComponent

    ,ProcessStatusCardComponent

    ,ProducedIn1TbCardComponent

    ,RoleAssigmentCardComponent

    ,StageInstanceCardComponent

    ,StageStatusCardComponent

    ,TaskCategoryCardComponent

    ,TaskCommentCardComponent

    ,TaskCommentTypeCardComponent

    ,TaskDefinitionCardComponent

    ,TaskFlowCardComponent

    ,TaskInstanceCardComponent

    ,TaskStatusCardComponent

    ,TaskTypeCardComponent

    ,USEDIN1TBCardComponent

    ,WFActivityLogCardComponent

    ,WFActivityStatusCardComponent

    ,WFApplicationCardComponent

    ,WFApplicationCommentCardComponent

    ,WFApplicationMessageCardComponent

    ,WFApplicationStatusCardComponent

    ,WFCompanyCardComponent

    ,WFContactCardComponent

    ,WFDashboardCardComponent

    ,WFFileCardComponent

    ,WFFileTypeCardComponent

    ,WFIngredientCardComponent

    ,WFPriorityCardComponent

    ,WFProductCardComponent

    ,WFQuoteCardComponent

    ,WFQuoteItemCardComponent

    ,WFQuoteStatusCardComponent

    ,WFRoleCardComponent

    ,WFUserCardComponent

    ,WorkflowHistoryCardComponent

];