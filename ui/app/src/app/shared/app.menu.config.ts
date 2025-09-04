import { MenuRootItem } from 'ontimize-web-ngx';

import { LaneDefinitionCardComponent } from './LaneDefinition-card/LaneDefinition-card.component';

import { LaneRoleCardComponent } from './LaneRole-card/LaneRole-card.component';

import { ProcessDefinitionCardComponent } from './ProcessDefinition-card/ProcessDefinition-card.component';

import { ProcessInstanceCardComponent } from './ProcessInstance-card/ProcessInstance-card.component';

import { ProcessMessageCardComponent } from './ProcessMessage-card/ProcessMessage-card.component';

import { ProcessMessageTypeCardComponent } from './ProcessMessageType-card/ProcessMessageType-card.component';


import { COMPANYTBCardComponent } from './COMPANYTB-card/COMPANYTB-card.component';
import { ProcessPriorityCardComponent } from './ProcessPriority-card/ProcessPriority-card.component';

import { ProcessStatusCardComponent } from './ProcessStatus-card/ProcessStatus-card.component';

import { StageInstanceCardComponent } from './StageInstance-card/StageInstance-card.component';

import { StageStatusCardComponent } from './StageStatus-card/StageStatus-card.component';

import { SysdiagramCardComponent } from './Sysdiagram-card/Sysdiagram-card.component';

import { TaskCategoryCardComponent } from './TaskCategory-card/TaskCategory-card.component';

import { TaskCommentCardComponent } from './TaskComment-card/TaskComment-card.component';

import { TaskCommentTypeCardComponent } from './TaskCommentType-card/TaskCommentType-card.component';

import { TaskDefinitionCardComponent } from './TaskDefinition-card/TaskDefinition-card.component';

import { TaskFlowCardComponent } from './TaskFlow-card/TaskFlow-card.component';

import { TaskInstanceCardComponent } from './TaskInstance-card/TaskInstance-card.component';

import { TaskStatusCardComponent } from './TaskStatus-card/TaskStatus-card.component';

import { TaskTypeCardComponent } from './TaskType-card/TaskType-card.component';

import { ValidationResultCardComponent } from './ValidationResult-card/ValidationResult-card.component';

import { ValidationRuleCardComponent } from './ValidationRule-card/ValidationRule-card.component';

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

import { PLANTTBCardComponent } from './PLANTTB-card/PLANTTB-card.component';
import { WFFileTypeCardComponent } from './WFFileType-card/WFFileType-card.component';

import { WFIngredientCardComponent } from './WFIngredient-card/WFIngredient-card.component';

import { WFPlantCardComponent } from './WFPlant-card/WFPlant-card.component';

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
        id: 'application', name: 'Application', icon: 'edit_square', opened: false,
        items: [

            { id: 'WFApplication', name: 'Application', icon: 'view_list', route: '/main/WFApplication' }
                        
            , { id: 'WFCompany', name: 'Company', icon: 'view_list', route: '/main/WFCompany' }

            , { id: 'WFContact', name: 'Contact', icon: 'view_list', route: '/main/WFContact' }

             , { id: 'WFPlant', name: 'Plant', icon: 'view_list', route: '/main/WFPlant' }

             , { id: 'WFProduct', name: 'Product', icon: 'view_list', route: '/main/WFProduct' }

            , { id: 'WFIngredient', name: 'Ingredients', icon: 'view_list', route: '/main/WFIngredient' }

            , { id: 'WFQuote', name: 'Quote', icon: 'view_list', route: '/main/WFQuote' }

            , { id: 'WFQuoteItem', name: 'Quote Item', icon: 'view_list', route: '/main/WFQuoteItem' }

            , { id: 'WFFile', name: 'Files', icon: 'view_list', route: '/main/WFFile' }

            , { id: 'WFApplicationComment', name: 'Application Comment', icon: 'view_list', route: '/main/WFApplicationComment' }

            , { id: 'WFApplicationMessage', name: 'Application Message', icon: 'view_list', route: '/main/WFApplicationMessage' }

            , { id: 'WFApplicationStatus', name: 'Application Status', icon: 'view_list', route: '/main/WFApplicationStatus' }

            , { id: 'WFDashboard', name: 'Dashboard', icon: 'view_list', route: '/main/WFDashboard' }

            , { id: 'WFActivityLog', name: 'Activity Log', icon: 'view_list', route: '/main/WFActivityLog' }

            , { id: 'WFRole', name: 'Role', icon: 'view_list', route: '/main/WFRole' }

            , { id: 'WFUser', name: 'User', icon: 'view_list', route: '/main/WFUser' }
        ]
    },
    {
        id: 'data', name: ' WorkFlow Definition', icon: 'remove_red_eye', opened: false,
        items: [

           // { id: 'WFDashboard', name: 'Dashboard', icon: 'view_list', route: '/main/WFDashboard' }
          
             { id: 'ProcessDefinition', name: 'Process Definition', icon: 'view_list', route: '/main/ProcessDefinition' }
            , { id: 'LaneDefinition', name: 'Lane Definition', icon: 'view_list', route: '/main/LaneDefinition' }
            , { id: 'TaskDefinition', name: 'Task Definition', icon: 'view_list', route: '/main/TaskDefinition' }
            , { id: 'TaskFlow', name: 'Task Flow', icon: 'view_list', route: '/main/TaskFlow' }

            // ,{ id: 'ValidationResult', name: 'VALIDATIONRESULT', icon: 'view_list', route: '/main/ValidationResult' }
            //,{ id: 'ValidationRule', name: 'VALIDATIONRULE', icon: 'view_list', route: '/main/ValidationRule' }
        ]
    },
    {
        id: 'wfinstance', name: ' WorkFlow Instance', icon: 'remove_red_eye', opened: false,
        items: [
                {id:'WFDashboard', name: 'Dashboard', icon: 'view_list', route: '/main/WFDashboard'}
            , { id: 'ProcessInstance', name: 'Process Instance', icon: 'view_list', route: '/main/ProcessInstance' }
            , { id: 'StageInstance', name: 'Stage Instance', icon: 'view_list', route: '/main/StageInstance' }
            , { id: 'TaskInstance', name: 'Task Instance', icon: 'view_list', route: '/main/TaskInstance' }
            , { id: 'WorkflowHistory', name: 'Workflow History', icon: 'view_list', route: '/main/WorkflowHistory' }            
            , { id: 'ProcessMessage', name: 'Process Message', icon: 'view_list', route: '/main/ProcessMessage' }
            , { id: 'TaskComment', name: 'Task Comment', icon: 'view_list', route: '/main/TaskComment' }
        ]
    },
    {
        id: 'lookup', name: ' Lookup Tables', icon: 'remove_red_eye', opened: false,
        items: [
            { id: 'ProcessMessageType', name: 'Process Message Type', icon: 'view_list', route: '/main/ProcessMessageType' }
            
            , { id: 'LaneRole', name: 'Lane Role', icon: 'view_list', route: '/main/LaneRole' }

            , { id: 'WFActivityStatus', name: 'WF Activity Status', icon: 'view_list', route: '/main/WFActivityStatus' }

            , { id: 'ProcessPriority', name: 'Process Priority', icon: 'view_list', route: '/main/ProcessPriority' }

            , { id: 'ProcessStatus', name: 'Process Status', icon: 'view_list', route: '/main/ProcessStatus' }

            , { id: 'TaskStatus', name: 'Task Status', icon: 'view_list', route: '/main/TaskStatus' }

            , { id: 'TaskType', name: 'Task Type', icon: 'view_list', route: '/main/TaskType' }

            , { id: 'StageStatus', name: 'Stage Status', icon: 'view_list', route: '/main/StageStatus' }

            , { id: 'WFQuoteStatus', name: 'WF Quote Status', icon: 'view_list', route: '/main/WFQuoteStatus' }

            //,{ id: 'Sysdiagram', name: 'SYSDIAGRAM', icon: 'view_list', route: '/main/Sysdiagram' }

            , { id: 'TaskCategory', name: 'Task Category', icon: 'view_list', route: '/main/TaskCategory' }

            , { id: 'WFFileType', name: 'WF File Type', icon: 'view_list', route: '/main/WFFileType' }


            , { id: 'TaskCommentType', name: 'Task Comment Type', icon: 'view_list', route: '/main/TaskCommentType' }

            , { id: 'WFPriority', name: 'WF Priority', icon: 'view_list', route: '/main/WFPriority' }
        ]
    },
    
    {id: 'legacy', name: ' Legacy Tables', icon: 'remove_red_eye', opened: false,
        items: [
	        { id: 'COMPANYTB', name: 'COMPANYTB', icon: 'view_list', route: '/main/COMPANYTB' }
            ,{ id: 'PLANTTB', name: 'PLANTTB', icon: 'view_list', route: '/main/PLANTTB' }
    
        ]
    },
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings' }
    , { id: 'about', name: 'About', icon: 'info', route: '/main/about' }
    , { id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    LaneDefinitionCardComponent

    , LaneRoleCardComponent

    , ProcessDefinitionCardComponent

    , ProcessInstanceCardComponent

    , ProcessMessageCardComponent

    ,COMPANYTBCardComponent
    , ProcessMessageTypeCardComponent

    , ProcessPriorityCardComponent

    , ProcessStatusCardComponent

    , StageInstanceCardComponent

    , StageStatusCardComponent

    , SysdiagramCardComponent

    , TaskCategoryCardComponent

    , TaskCommentCardComponent

    , TaskCommentTypeCardComponent

    , TaskDefinitionCardComponent

    , TaskFlowCardComponent

    , TaskInstanceCardComponent

    , TaskStatusCardComponent

    , TaskTypeCardComponent

    , ValidationResultCardComponent

    , ValidationRuleCardComponent

    , WFActivityLogCardComponent

    , WFActivityStatusCardComponent

    , WFApplicationCardComponent

    , WFApplicationCommentCardComponent

    , WFApplicationMessageCardComponent

    , WFApplicationStatusCardComponent

    , WFCompanyCardComponent

    , WFContactCardComponent

    , WFDashboardCardComponent

    ,PLANTTBCardComponent
    , WFFileCardComponent

    , WFFileTypeCardComponent

    , WFIngredientCardComponent

    , WFPlantCardComponent

    , WFPriorityCardComponent

    , WFProductCardComponent

    , WFQuoteCardComponent

    , WFQuoteItemCardComponent

    , WFQuoteStatusCardComponent

    , WFRoleCardComponent

    , WFUserCardComponent

    , WorkflowHistoryCardComponent

];