import { MenuRootItem } from 'ontimize-web-ngx';

import { EventActionCardComponent } from './EventAction-card/EventAction-card.component';

import { LaneDefinitionCardComponent } from './LaneDefinition-card/LaneDefinition-card.component';

import { LaneRoleCardComponent } from './LaneRole-card/LaneRole-card.component';

import { ProcessDefinitionCardComponent } from './ProcessDefinition-card/ProcessDefinition-card.component';

import { ProcessMessageTypeCardComponent } from './ProcessMessageType-card/ProcessMessageType-card.component';

import { RoleAssignmentCardComponent } from './RoleAssignment-card/RoleAssignment-card.component';

import { StageDefinitionCardComponent } from './StageDefinition-card/StageDefinition-card.component';

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

import { WFActivityLogCardComponent } from './WFActivityLog-card/WFActivityLog-card.component';

import { WFActivityStatusCardComponent } from './WFActivityStatus-card/WFActivityStatus-card.component';

import { WFApplicationCardComponent } from './WFApplication-card/WFApplication-card.component';

import { WFApplicationMessageCardComponent } from './WFApplicationMessage-card/WFApplicationMessage-card.component';

import { WFApplicationStatusCardComponent } from './WFApplicationStatus-card/WFApplicationStatus-card.component';

import { WFFileCardComponent } from './WFFile-card/WFFile-card.component';

import { WFFileTypeCardComponent } from './WFFileType-card/WFFileType-card.component';

import { WFPriorityCardComponent } from './WFPriority-card/WFPriority-card.component';

import { WFQuoteCardComponent } from './WFQuote-card/WFQuote-card.component';

import { WFQuoteItemCardComponent } from './WFQuoteItem-card/WFQuoteItem-card.component';

import { WFQuoteStatusCardComponent } from './WFQuoteStatus-card/WFQuoteStatus-card.component';

import { WFRoleCardComponent } from './WFRole-card/WFRole-card.component';

import { WFUserCardComponent } from './WFUser-card/WFUser-card.component';

import { WFUserAdminCardComponent } from './WFUserAdmin-card/WFUserAdmin-card.component';

import { WFUserRoleCardComponent } from './WFUserRole-card/WFUserRole-card.component';

import { WorkflowHistoryCardComponent } from './WorkflowHistory-card/WorkflowHistory-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    
    {
    id: 'data', name: ' data', icon: 'remove_red_eye', opened: true,
    items: [
    
        { id: 'EventAction', name: 'EVENTACTION', icon: 'view_list', route: '/main/EventAction' }
    
        ,{ id: 'LaneDefinition', name: 'LANEDEFINITION', icon: 'view_list', route: '/main/LaneDefinition' }
    
        ,{ id: 'LaneRole', name: 'LANEROLE', icon: 'view_list', route: '/main/LaneRole' }
    
        ,{ id: 'ProcessDefinition', name: 'PROCESSDEFINITION', icon: 'view_list', route: '/main/ProcessDefinition' }
    
        ,{ id: 'ProcessMessageType', name: 'PROCESSMESSAGETYPE', icon: 'view_list', route: '/main/ProcessMessageType' }
    
        ,{ id: 'RoleAssignment', name: 'ROLEASSIGNMENT', icon: 'view_list', route: '/main/RoleAssignment' }
    
        ,{ id: 'StageDefinition', name: 'STAGEDEFINITION', icon: 'view_list', route: '/main/StageDefinition' }
    
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
    
        ,{ id: 'WFActivityLog', name: 'WFACTIVITYLOG', icon: 'view_list', route: '/main/WFActivityLog' }
    
        ,{ id: 'WFActivityStatus', name: 'WFACTIVITYSTATUS', icon: 'view_list', route: '/main/WFActivityStatus' }
    
        ,{ id: 'WFApplication', name: 'WFAPPLICATION', icon: 'view_list', route: '/main/WFApplication' }
    
        ,{ id: 'WFApplicationMessage', name: 'WFAPPLICATIONMESSAGE', icon: 'view_list', route: '/main/WFApplicationMessage' }
    
        ,{ id: 'WFApplicationStatus', name: 'WFAPPLICATIONSTATUS', icon: 'view_list', route: '/main/WFApplicationStatus' }
    
        ,{ id: 'WFFile', name: 'WFFILE', icon: 'view_list', route: '/main/WFFile' }
    
        ,{ id: 'WFFileType', name: 'WFFILETYPE', icon: 'view_list', route: '/main/WFFileType' }
    
        ,{ id: 'WFPriority', name: 'WFPRIORITY', icon: 'view_list', route: '/main/WFPriority' }
    
        ,{ id: 'WFQuote', name: 'WFQUOTE', icon: 'view_list', route: '/main/WFQuote' }
    
        ,{ id: 'WFQuoteItem', name: 'WFQUOTEITEM', icon: 'view_list', route: '/main/WFQuoteItem' }
    
        ,{ id: 'WFQuoteStatus', name: 'WFQUOTESTATUS', icon: 'view_list', route: '/main/WFQuoteStatus' }
    
        ,{ id: 'WFRole', name: 'WFROLE', icon: 'view_list', route: '/main/WFRole' }
    
        ,{ id: 'WFUser', name: 'WFUSER', icon: 'view_list', route: '/main/WFUser' }
    
        ,{ id: 'WFUserAdmin', name: 'WFUSERADMIN', icon: 'view_list', route: '/main/WFUserAdmin' }
    
        ,{ id: 'WFUserRole', name: 'WFUSERROLE', icon: 'view_list', route: '/main/WFUserRole' }
    
        ,{ id: 'WorkflowHistory', name: 'WORKFLOWHISTORY', icon: 'view_list', route: '/main/WorkflowHistory' }
    
    ] 
},
    
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings'}
    ,{ id: 'about', name: 'About', icon: 'info', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    EventActionCardComponent

    ,LaneDefinitionCardComponent

    ,LaneRoleCardComponent

    ,ProcessDefinitionCardComponent

    ,ProcessMessageTypeCardComponent

    ,RoleAssignmentCardComponent

    ,StageDefinitionCardComponent

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

    ,WFActivityLogCardComponent

    ,WFActivityStatusCardComponent

    ,WFApplicationCardComponent

    ,WFApplicationMessageCardComponent

    ,WFApplicationStatusCardComponent

    ,WFFileCardComponent

    ,WFFileTypeCardComponent

    ,WFPriorityCardComponent

    ,WFQuoteCardComponent

    ,WFQuoteItemCardComponent

    ,WFQuoteStatusCardComponent

    ,WFRoleCardComponent

    ,WFUserCardComponent

    ,WFUserAdminCardComponent

    ,WFUserRoleCardComponent

    ,WorkflowHistoryCardComponent

];