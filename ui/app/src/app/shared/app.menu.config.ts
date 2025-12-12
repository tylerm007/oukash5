import { MenuRootItem } from 'ontimize-web-ngx';

import { EventActionCardComponent } from './EventAction-card/EventAction-card.component';

import { COMPANYADDRESSTBCardComponent } from './COMPANYADDRESSTB-card/COMPANYADDRESSTB-card.component';

import { COMPANYTBCardComponent } from './COMPANYTB-card/COMPANYTB-card.component';

import { CompanyApplicationCardComponent } from './CompanyApplication-card/CompanyApplication-card.component';

import { FormulaProductCardComponent } from './FormulaProduct-card/FormulaProduct-card.component';

import { FormulaSubmissionComponentCardComponent } from './FormulaSubmissionComponent-card/FormulaSubmissionComponent-card.component';

import { FormulaSubmissionPlantCardComponent } from './FormulaSubmissionPlant-card/FormulaSubmissionPlant-card.component';

import { LabelTbCardComponent } from './LabelTb-card/LabelTb-card.component';

import { StageDefinitionCardComponent } from './StageDefinition-card/StageDefinition-card.component';

import { MERCHTBCardComponent } from './MERCHTB-card/MERCHTB-card.component';

import { OWNSTBCardComponent } from './OWNSTB-card/OWNSTB-card.component';

import { PLANTADDRESSTBCardComponent } from './PLANTADDRESSTB-card/PLANTADDRESSTB-card.component';

import { PLANTCERTDETAILCardComponent } from './PLANTCERTDETAIL-card/PLANTCERTDETAIL-card.component';

import { PLANTCOMMENTCardComponent } from './PLANTCOMMENT-card/PLANTCOMMENT-card.component';

import { PLANTTBCardComponent } from './PLANTTB-card/PLANTTB-card.component';
import { ProcessDefinitionCardComponent } from './ProcessDefinition-card/ProcessDefinition-card.component';

import { ProcessPriorityCardComponent } from './ProcessPriority-card/ProcessPriority-card.component';

import { ProcessStatusCardComponent } from './ProcessStatus-card/ProcessStatus-card.component';

import { ProducedIn1TbCardComponent } from './ProducedIn1Tb-card/ProducedIn1Tb-card.component';

import { RoleAssigmentCardComponent } from './RoleAssigment-card/RoleAssigment-card.component';

import { StageInstanceCardComponent } from './StageInstance-card/StageInstance-card.component';

import { StageStatusCardComponent } from './StageStatus-card/StageStatus-card.component';

import { TaskCategoryCardComponent } from './TaskCategory-card/TaskCategory-card.component';

import { TaskDefinitionCardComponent } from './TaskDefinition-card/TaskDefinition-card.component';

import { TaskFlowCardComponent } from './TaskFlow-card/TaskFlow-card.component';

import { TaskInstanceCardComponent } from './TaskInstance-card/TaskInstance-card.component';

import { TaskRoleCardComponent } from './TaskRole-card/TaskRole-card.component';

import { TaskStatusCardComponent } from './TaskStatus-card/TaskStatus-card.component';

import { TaskTypeCardComponent } from './TaskType-card/TaskType-card.component';

import { USEDIN1TBCardComponent } from './USEDIN1TB-card/USEDIN1TB-card.component';

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

import { WFUSERADMINCardComponent } from './WFUSERADMIN-card/WFUSERADMIN-card.component';

import { WFUSERROLECardComponent } from './WFUSERROLE-card/WFUSERROLE-card.component';
import { WFUserCardComponent } from './WFUser-card/WFUser-card.component';



export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },


    {
        id: 'application', name: 'Application', icon: 'edit_square', opened: false,
        items: [

            { id: 'WFApplication', name: 'Application', icon: 'view_list', route: '/main/WFApplication' }
                        
            , { id: 'WFQuote', name: 'Quote', icon: 'view_list', route: '/main/WFQuote' }

            , { id: 'WFQuoteItem', name: 'Quote Item', icon: 'view_list', route: '/main/WFQuoteItem' }

            , { id: 'WFFile', name: 'Files', icon: 'view_list', route: '/main/WFFile' }

            , { id: 'WFApplicationMessage', name: 'Application Message', icon: 'view_list', route: '/main/WFApplicationMessage' }

            , { id: 'WFRole', name: 'Role', icon: 'view_list', route: '/main/WFRole' }

            , { id: 'WFUser', name: 'User', icon: 'view_list', route: '/main/WFUser' }
	        ,{ id: 'WFUSERROLE', name: 'User Role', icon: 'view_list', route: '/main/WFUSERROLE' }
            ,{ id: 'WFUSERADMIN', name: 'User Admins', icon: 'view_list', route: '/main/WFUSERADMIN' }
	    
	    ,{ id: 'RoleAssigment', name: 'Role Assignment', icon: 'view_list', route: '/main/RoleAssigment' }
    
        ]
    },
    {
        id: 'data', name: ' WorkFlow Definition', icon: 'remove_red_eye', opened: false,
        items: [

            { id: 'WFApplication', name: 'Application', icon: 'view_list', route: '/main/WFApplication' }
            , { id: 'ProcessDefinition', name: 'Process Definition', icon: 'view_list', route: '/main/ProcessDefinition' }
            , { id: 'StageDefinition', name: 'Stage Definition', icon: 'view_list', route: '/main/StageDefinition' }
            , { id: 'TaskDefinition', name: 'Task Definition', icon: 'view_list', route: '/main/TaskDefinition' }
            , { id: 'TaskFlow', name: 'Task Flow', icon: 'view_list', route: '/main/TaskFlow' }
            , { id: 'TaskInstance', name: 'Task Instance', icon: 'view_list', route: '/main/TaskInstance' }
        ]

    },
    {
        id: 'wfinstance', name: ' WorkFlow Instance', icon: 'remove_red_eye', opened: false,
        items: [
             { id: 'StageInstance', name: 'Stage Instance', icon: 'view_list', route: '/main/StageInstance' }
            , { id: 'TaskInstance', name: 'Task Instance', icon: 'view_list', route: '/main/TaskInstance' }
          
        ]
    },
    {
        id: 'lookup', name: ' Lookup Tables', icon: 'remove_red_eye', opened: false,
        items: [
           { id: 'LaneRole', name: 'Lane Role', icon: 'view_list', route: '/main/LaneRole' }
            , { id: 'WFApplicationStatus', name: 'Application Status', icon: 'view_list', route: '/main/WFApplicationStatus' }
           , { id: 'ProcessPriority', name: 'Process Priority', icon: 'view_list', route: '/main/ProcessPriority' }
            , { id: 'ProcessStatus', name: 'Process Status', icon: 'view_list', route: '/main/ProcessStatus' }
            , { id: 'TaskStatus', name: 'Task Status', icon: 'view_list', route: '/main/TaskStatus' }
            , { id: 'TaskType', name: 'Task Type', icon: 'view_list', route: '/main/TaskType' }
            , { id: 'StageStatus', name: 'Stage Status', icon: 'view_list', route: '/main/StageStatus' }
            , { id: 'WFQuoteStatus', name: 'WF Quote Status', icon: 'view_list', route: '/main/WFQuoteStatus' }

            //,{ id: 'Sysdiagram', name: 'SYSDIAGRAM', icon: 'view_list', route: '/main/Sysdiagram' }

            , { id: 'TaskCategory', name: 'Task Category', icon: 'view_list', route: '/main/TaskCategory' }

            , { id: 'WFFileType', name: 'WF File Type', icon: 'view_list', route: '/main/WFFileType' }

            , { id: 'WFPriority', name: 'WF Priority', icon: 'view_list', route: '/main/WFPriority' }
        ]
    },
    
    {id: 'legacy', name: ' Legacy Tables', icon: 'remove_red_eye', opened: false,
        items: [
        { id: 'COMPANYTB', name: 'COMPANYTB', icon: 'view_list', route: '/main/COMPANYTB' }
        ,{ id: 'PLANTTB', name: 'PLANTTB', icon: 'view_list', route: '/main/PLANTTB' }
    
        ,{ id: 'CompanyApplication', name: 'COMPANYAPPLICATION', icon: 'view_list', route: '/main/CompanyApplication' }
	, { id: 'COMPANYADDRESSTB', name: 'COMPANYADDRESSTB', icon: 'view_list', route: '/main/COMPANYADDRESSTB' }
   
        ,{ id: 'CompanyApplication', name: 'COMPANYAPPLICATION', icon: 'view_list', route: '/main/CompanyApplication' }
    
        ,{ id: 'FormulaProduct', name: 'FORMULAPRODUCT', icon: 'view_list', route: '/main/FormulaProduct' }
    
        ,{ id: 'FormulaSubmissionComponent', name: 'FORMULASUBMISSIONCOMPONENT', icon: 'view_list', route: '/main/FormulaSubmissionComponent' }
    
        ,{ id: 'FormulaSubmissionPlant', name: 'FORMULASUBMISSIONPLANT', icon: 'view_list', route: '/main/FormulaSubmissionPlant' }
    
        ,{ id: 'LabelTb', name: 'LABELTB', icon: 'view_list', route: '/main/LabelTb' }
         ,{ id: 'FormulaProduct', name: 'FORMULAPRODUCT', icon: 'view_list', route: '/main/FormulaProduct' }
    
        ,{ id: 'FormulaSubmissionComponent', name: 'FORMULASUBMISSIONCOMPONENT', icon: 'view_list', route: '/main/FormulaSubmissionComponent' }
    
        ,{ id: 'FormulaSubmissionPlant', name: 'FORMULASUBMISSIONPLANT', icon: 'view_list', route: '/main/FormulaSubmissionPlant' }
    
	,{ id: 'MERCHTB', name: 'MERCHTB', icon: 'view_list', route: '/main/MERCHTB' }
    
        ,{ id: 'OWNSTB', name: 'OWNSTB', icon: 'view_list', route: '/main/OWNSTB' }
    
        ,{ id: 'PLANTADDRESSTB', name: 'PLANTADDRESSTB', icon: 'view_list', route: '/main/PLANTADDRESSTB' }
    
        ,{ id: 'PLANTCERTDETAIL', name: 'PLANTCERTDETAIL', icon: 'view_list', route: '/main/PLANTCERTDETAIL' }
    
        ,{ id: 'PLANTCOMMENT', name: 'PLANTCOMMENT', icon: 'view_list', route: '/main/PLANTCOMMENT' }
    
        ,{ id: 'PLANTTB', name: 'PLANTTB', icon: 'view_list', route: '/main/PLANTTB' }
	
	,{ id: 'ProducedIn1Tb', name: 'PRODUCEDIN1TB', icon: 'view_list', route: '/main/ProducedIn1Tb' }
    
    	 ,{ id: 'USEDIN1TB', name: 'USEDIN1TB', icon: 'view_list', route: '/main/USEDIN1TB' }
    
        ]
    },
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings' }
    , { id: 'about', name: 'About', icon: 'info', route: '/main/about' }
    , { id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    COMPANYADDRESSTBCardComponent

    ,COMPANYTBCardComponent

    ,CompanyApplicationCardComponent

    ,FormulaProductCardComponent

    ,FormulaSubmissionComponentCardComponent

    ,FormulaSubmissionPlantCardComponent

    ,LabelTbCardComponent

    ,MERCHTBCardComponent

    ,OWNSTBCardComponent

    ,PLANTADDRESSTBCardComponent

    ,PLANTCERTDETAILCardComponent

    ,PLANTCOMMENTCardComponent

    ,PLANTTBCardComponent

    ,ProcessDefinitionCardComponent


    , ProcessPriorityCardComponent

    , ProcessStatusCardComponent

    ,ProducedIn1TbCardComponent

    ,RoleAssigmentCardComponent

    ,StageDefinitionCardComponent

    ,StageInstanceCardComponent

    , StageStatusCardComponent


    , TaskCategoryCardComponent

    , TaskDefinitionCardComponent

    , TaskFlowCardComponent

    , TaskInstanceCardComponent

    ,TaskRoleCardComponent

    ,TaskStatusCardComponent

    , TaskTypeCardComponent

    ,USEDIN1TBCardComponent

    , WFApplicationCardComponent

    , WFApplicationMessageCardComponent

    , WFApplicationStatusCardComponent

    ,WFFileCardComponent

    , WFFileTypeCardComponent

    , WFPriorityCardComponent

    , WFQuoteCardComponent

    , WFQuoteItemCardComponent

    , WFQuoteStatusCardComponent

    , WFRoleCardComponent

    ,WFUSERADMINCardComponent

    ,WFUSERROLECardComponent

    ,WFUserCardComponent

];