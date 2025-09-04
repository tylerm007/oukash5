# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import Boolean, Column, Computed, DECIMAL, Date, Float, ForeignKey, Index, Integer, LargeBinary, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  August 27, 2025 18:09:13
# Database: mssql+pyodbc://apilogic:2Rtrzc8iLovpU!Hv8gG*@kash-sql-st.nyc.ou.org/dashboard?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no&Encrypt=no
# Dialect:  mssql
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mssql import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class LaneRole(Base):  # type: ignore
    __tablename__ = 'LaneRoles'
    _s_collection_name = 'LaneRole'  # type: ignore

    RoleCode = Column(Unicode(20), primary_key=True)
    RoleDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    LaneDefinitionList : Mapped[List["LaneDefinition"]] = relationship(back_populates="LaneRole1")
class ProcessDefinition(Base):  # type: ignore
    __tablename__ = 'ProcessDefinitions'
    _s_collection_name = 'ProcessDefinition'  # type: ignore

    ProcessId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessName = Column(Unicode(100), nullable=False)
    ProcessVersion = Column(Unicode(10), server_default=text("1.0"), nullable=False)
    Description = Column(Unicode(500))
    IsActive = Column(Boolean, server_default=text("1"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text('system'), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)

    # child relationships (access children)
    LaneDefinitionList : Mapped[List["LaneDefinition"]] = relationship(back_populates="Process")
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="Process")
    ProcessInstanceList : Mapped[List["ProcessInstance"]] = relationship(back_populates="Process")



class ProcessMessageType(Base):  # type: ignore
    __tablename__ = 'ProcessMessageTypes'
    _s_collection_name = 'ProcessMessageType'  # type: ignore

    MessageTypeCode = Column(Unicode(20), primary_key=True)
    MessageTypeDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    ProcessMessageList : Mapped[List["ProcessMessage"]] = relationship(back_populates="ProcessMessageType")



t_ProcessOverview = Table(
    'ProcessOverview', metadata,
    Column('ProcessId', Unicode(100), nullable=False),
    Column('ProcessName', Unicode(255), nullable=False),
    Column('IsExecutable', Boolean, nullable=False),
    Column('LaneCount', Integer),
    Column('NodeCount', Integer),
    Column('FlowCount', Integer)
)


class ProcessPriority(Base):  # type: ignore
    __tablename__ = 'ProcessPriorities'
    _s_collection_name = 'ProcessPriority'  # type: ignore

    PriorityCode = Column(Unicode(10), primary_key=True)
    PriorityDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    ProcessInstanceList : Mapped[List["ProcessInstance"]] = relationship(back_populates="ProcessPriority")



class ProcessStatus(Base):  # type: ignore
    __tablename__ = 'ProcessStatus'
    _s_collection_name = 'ProcessStatus'  # type: ignore

    StatusCode = Column(Unicode(10), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    ProcessInstanceList : Mapped[List["ProcessInstance"]] = relationship(back_populates="ProcessStatu")



class StageStatus(Base):  # type: ignore
    __tablename__ = 'StageStatus'
    _s_collection_name = 'StageStatus'  # type: ignore

    StatusCode = Column(Unicode(20), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="StageStatus")

class TaskCategory(Base):  # type: ignore
    __tablename__ = 'TaskCategories'
    _s_collection_name = 'TaskCategory'  # type: ignore

    TaskCategoryCode = Column(Unicode(20), primary_key=True)
    TaskCategoryDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="TaskCategory1")



class TaskCommentType(Base):  # type: ignore
    __tablename__ = 'TaskCommentTypes'
    _s_collection_name = 'TaskCommentType'  # type: ignore

    CommentTypeCode = Column(Unicode(10), primary_key=True)
    CommentTypeDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    TaskCommentList : Mapped[List["TaskComment"]] = relationship(back_populates="TaskCommentType")



class TaskStatus(Base):  # type: ignore
    __tablename__ = 'TaskStatus'
    _s_collection_name = 'TaskStatus'  # type: ignore

    StatusCode = Column(Unicode(20), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="TaskStatus")



class TaskType(Base):  # type: ignore
    __tablename__ = 'TaskTypes'
    _s_collection_name = 'TaskType'  # type: ignore

    TaskTypeCode = Column(Unicode(20), primary_key=True)
    TaskTypeDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="TaskType1")
class ValidationRule(Base):  # type: ignore
    __tablename__ = 'ValidationRules'
    _s_collection_name = 'ValidationRule'  # type: ignore

    ValidationId = Column(Integer, autoincrement=True, primary_key=True)
    ValidationName = Column(Unicode(100), nullable=False)
    Category = Column(Unicode(50), nullable=False)
    RuleType = Column(Unicode(50), nullable=False)
    ValidationQuery = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    ErrorMessage = Column(Unicode(500))
    IsActive = Column(Boolean, server_default=text("1"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
   # ValidationResultList : Mapped[List["ValidationResult"]] = relationship(back_populates="Validation")



class WFActivityStatus(Base):  # type: ignore
    __tablename__ = 'WF_ActivityStatus'
    _s_collection_name = 'WFActivityStatus'  # type: ignore

    StatusCode = Column(Unicode(5), primary_key=True)
    StatusDesc = Column(Unicode(50))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFActivityLogList : Mapped[List["WFActivityLog"]] = relationship(back_populates="WF_ActivityStatus")



class WFApplicationStatus(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationStatus'
    _s_collection_name = 'WFApplicationStatus'  # type: ignore

    StatusCode = Column(Unicode(50), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFApplicationList : Mapped[List["WFApplication"]] = relationship(back_populates="WF_ApplicationStatus")



class WFDashboard(Base):  # type: ignore
    __tablename__ = 'WF_Dashboard'
    _s_collection_name = 'WFDashboard'  # type: ignore

    ID = Column(Integer, autoincrement=True, primary_key=True)
    count_new = Column(Integer, server_default=text("0"))
    count_in_progress = Column(Integer, server_default=text("0"))
    count_withdrawn = Column(Integer, server_default=text("0"))
    count_completed = Column(Integer, server_default=text("0"))
    count_overdue = Column(Integer, server_default=text("0"))
    total_count = Column(Integer, server_default=text("0"))

    # parent relationships (access parent)

    # child relationships (access children)
    WFApplicationList : Mapped[List["WFApplication"]] = relationship(back_populates="WFDashboard")



class WFFileType(Base):  # type: ignore
    __tablename__ = 'WF_FileTypes'
    _s_collection_name = 'WFFileType'  # type: ignore

    FileType = Column(Unicode(5), primary_key=True)
    FileTypeName = Column(Unicode(100), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFFileList : Mapped[List["WFFile"]] = relationship(back_populates="WF_FileType")



class WFPriority(Base):  # type: ignore
    __tablename__ = 'WF_Priorities'
    _s_collection_name = 'WFPriority'  # type: ignore

    PriorityCode = Column(Unicode(20), primary_key=True)
    PriorityDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFApplicationList : Mapped[List["WFApplication"]] = relationship(back_populates="WF_Priority")



class WFQuoteStatus(Base):  # type: ignore
    __tablename__ = 'WF_QuoteStatus'
    _s_collection_name = 'WFQuoteStatus'  # type: ignore

    StatusCode = Column(Unicode(10), primary_key=True)
    StatusDesc = Column(Unicode(50))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFQuoteList : Mapped[List["WFQuote"]] = relationship(back_populates="WF_QuoteStatu")



class WFRole(Base):  # type: ignore
    __tablename__ = 'WF_Roles'
    _s_collection_name = 'WFRole'  # type: ignore

    UserRole = Column(Unicode(10), primary_key=True)
    Role = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFUserList : Mapped[List["WFUser"]] = relationship(back_populates="WF_Role")



t_vw_ActiveWorkflows = Table(
    'vw_ActiveWorkflows', metadata,
    Column('InstanceId', Integer, nullable=False),
    Column('ApplicationId', Unicode(50), nullable=False),
    Column('ProcessName', Unicode(100), nullable=False),
    Column('Status', Unicode(10), nullable=False),
    Column('CurrentTask', Unicode(100)),
    Column('StartedDate', DATETIME2, nullable=False),
    Column('StartedBy', Unicode(100), nullable=False),
    Column('Priority', Unicode(10)),
    Column('HoursActive', Integer)
)


t_vw_TaskPerformance = Table(
    'vw_TaskPerformance', metadata,
    Column('TaskName', Unicode(100), nullable=False),
    Column('TaskType', Unicode(50), nullable=False),
    Column('TaskCategory', Unicode(50)),
    Column('TotalExecutions', Integer),
    Column('AvgDurationMinutes', Float(53)),
    Column('EstimatedDurationMinutes', Integer),
    Column('CompletedTasks', Integer),
    Column('FailedTasks', Integer),
    Column('SuccessRate', Float(53))
)


t_vw_ValidationStatus = Table(
    'vw_ValidationStatus', metadata,
    Column('InstanceId', Integer, nullable=False),
    Column('ApplicationId', Unicode(50), nullable=False),
    Column('TotalValidations', Integer),
    Column('PassedValidations', Integer),
    Column('FailedValidations', Integer),
    Column('ValidationStatus', String(12), nullable=False)
)


t_vw_WorkflowDashboard = Table(
    'vw_WorkflowDashboard', metadata,
    Column('Metric', String(25), nullable=False),
    Column('Value', Float(53)),
    Column('Unit', String(5), nullable=False)
)


class LaneDefinition(Base):  # type: ignore
    __tablename__ = 'LaneDefinitions'
    _s_collection_name = 'LaneDefinition'  # type: ignore

    LaneId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessId = Column(ForeignKey('ProcessDefinitions.ProcessId'), nullable=False)
    LaneName = Column(Unicode(100), nullable=False)
    LaneDescription = Column(Unicode(500))
    EstimatedDurationDays = Column(Integer)
    LaneRole = Column(ForeignKey('LaneRoles.RoleCode'), server_default=text("('NCRC')"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("(getutcdate())"), nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    LaneRole1 : Mapped["LaneRole"] = relationship(back_populates=("LaneDefinitionList"))
    Process : Mapped["ProcessDefinition"] = relationship(back_populates=("LaneDefinitionList"))

    # child relationships (access children)
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="Lane")
    StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="Lane")



class TaskDefinition(Base):  # type: ignore
    __tablename__ = 'TaskDefinitions'
    _s_collection_name = 'TaskDefinition'  # type: ignore

    TaskId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessId = Column(ForeignKey('ProcessDefinitions.ProcessId'), nullable=False)
    TaskName = Column(Unicode(100), nullable=False)
    TaskType = Column(ForeignKey('TaskTypes.TaskTypeCode'), nullable=False)
    TaskCategory = Column(ForeignKey('TaskCategories.TaskCategoryCode'))
    Sequence = Column(Integer, nullable=False)
    LaneId = Column(ForeignKey('LaneDefinitions.LaneId'), nullable=False)
    IsParallel = Column(Boolean, server_default=text("0"), nullable=False)
    AssigneeRole = Column(Unicode(20))
    EstimatedDurationMinutes = Column(Integer)
    IsRequired = Column(Boolean, server_default=text("1"), nullable=False)
    AutoComplete = Column(Boolean, server_default=text("0"), nullable=False)
    Description = Column(Unicode(500))
    ConfigurationJson = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    Lane : Mapped["LaneDefinition"] = relationship(back_populates=("TaskDefinitionList"))
    Process : Mapped["ProcessDefinition"] = relationship(back_populates=("TaskDefinitionList"))
    TaskCategory1 : Mapped["TaskCategory"] = relationship(back_populates=("TaskDefinitionList"))
    TaskType1 : Mapped["TaskType"] = relationship(back_populates=("TaskDefinitionList"))

    # child relationships (access children)
    ProcessInstanceList : Mapped[List["ProcessInstance"]] = relationship(back_populates="CurrentTask")
    TaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.FromTaskId]', back_populates="FromTask")
    ToTaskTaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.ToTaskId]', back_populates="ToTask")
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="TaskDef")



class WFApplication(Base):  # type: ignore
    __tablename__ = 'WF_Applications'
    _s_collection_name = 'WFApplication'  # type: ignore

    ApplicationID = Column(Integer, autoincrement=True, primary_key=True, index=True)
    ApplicationNumber = Column(Integer, nullable=False, unique=True)
    CompanyID = Column(Integer, nullable=False, index=True)
    PlantID = Column(Integer)
    SubmissionDate = Column(Date, nullable=False)
    Status = Column(ForeignKey('WF_ApplicationStatus.StatusCode'), server_default=text("NEW"), nullable=False, index=True)
    Priority = Column(ForeignKey('WF_Priorities.PriorityCode'), server_default=text("NORMAL"))
    AssignedTo = Column(Unicode(100))
    AssignedBy = Column(Unicode(100))
    AssignedDate = Column(DATETIME2)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))
    WFDashboardID = Column(ForeignKey('WF_Dashboard.ID'), server_default=text("1"))

    # parent relationships (access parent)
    WF_Priority : Mapped["WFPriority"] = relationship(back_populates=("WFApplicationList"))
    WF_ApplicationStatus : Mapped["WFApplicationStatus"] = relationship(back_populates=("WFApplicationList"))
    WFDashboard : Mapped["WFDashboard"] = relationship(back_populates=("WFApplicationList"))

    # child relationships (access children)
    WFActivityLogList : Mapped[List["WFActivityLog"]] = relationship(back_populates="Application")
    WFApplicationCommentList : Mapped[List["WFApplicationComment"]] = relationship(back_populates="Application")
    WFApplicationMessageList : Mapped[List["WFApplicationMessage"]] = relationship(back_populates="Application")
    WFCompanyList : Mapped[List["WFCompany"]] = relationship(back_populates="Application")
    WFContactList : Mapped[List["WFContact"]] = relationship(back_populates="Application")
    WFFileList : Mapped[List["WFFile"]] = relationship(back_populates="Application")
    WFIngredientList : Mapped[List["WFIngredient"]] = relationship(back_populates="Application")
    WFPlantList : Mapped[List["WFPlant"]] = relationship(back_populates="Application")
    WFProductList : Mapped[List["WFProduct"]] = relationship(back_populates="Application")
    WFQuoteList : Mapped[List["WFQuote"]] = relationship(back_populates="Application")



class WFUser(Base):  # type: ignore
    __tablename__ = 'WF_Users'
    _s_collection_name = 'WFUser'  # type: ignore

    UserID = Column(Integer, autoincrement=True, primary_key=True)
    Username = Column(Unicode(100), nullable=False, unique=True)
    FullName = Column(Unicode(200), nullable=False)
    Email = Column(Unicode(255), nullable=False, unique=True)
    Role = Column(ForeignKey('WF_Roles.UserRole'), server_default=text('ADMIN'), nullable=False)
    IsActive = Column(Boolean, server_default=text("1"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    LastLoginDate = Column(DATETIME2)

    # parent relationships (access parent)
    WF_Role : Mapped["WFRole"] = relationship(back_populates=("WFUserList"))

    # child relationships (access children)



class ProcessInstance(Base):  # type: ignore
    __tablename__ = 'ProcessInstances'
    _s_collection_name = 'ProcessInstance'  # type: ignore

    InstanceId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessId = Column(ForeignKey('ProcessDefinitions.ProcessId'), nullable=False)
    ApplicationId = Column(Unicode(50), nullable=False, index=True)
    Status = Column(ForeignKey('ProcessStatus.StatusCode'), server_default=text("NEW"), nullable=False, index=True)
    CurrentTaskId = Column(ForeignKey('TaskDefinitions.TaskId'))
    StartedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False, index=True)
    StartedBy = Column(Unicode(100), nullable=False)
    CompletedDate = Column(DATETIME2)
    CompletedBy = Column(Unicode(100))
    Priority = Column(ForeignKey('ProcessPriorities.PriorityCode'), server_default=text('NORMAL'))
    ContextData = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    CurrentTask : Mapped["TaskDefinition"] = relationship(back_populates=("ProcessInstanceList"))
    ProcessPriority : Mapped["ProcessPriority"] = relationship(back_populates=("ProcessInstanceList"))
    Process : Mapped["ProcessDefinition"] = relationship(back_populates=("ProcessInstanceList"))
    ProcessStatu : Mapped["ProcessStatus"] = relationship(back_populates=("ProcessInstanceList"))

    # child relationships (access children)
    ProcessMessageList : Mapped[List["ProcessMessage"]] = relationship(back_populates="Instance")
    StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="ProcessInstance")
    TaskCommentList : Mapped[List["TaskComment"]] = relationship(back_populates="ProcessInstance")
    WorkflowHistoryList : Mapped[List["WorkflowHistory"]] = relationship(back_populates="Instance")



class TaskFlow(Base):  # type: ignore
    __tablename__ = 'TaskFlow'
    _s_collection_name = 'TaskFlow'  # type: ignore

    FlowId = Column(Integer, autoincrement=True, primary_key=True)
    FromTaskId = Column(ForeignKey('TaskDefinitions.TaskId'))
    ToTaskId = Column(ForeignKey('TaskDefinitions.TaskId'), nullable=False)
    Condition = Column(Unicode(500))
    IsDefault = Column(Boolean, server_default=text("0"), nullable=False)

    # parent relationships (access parent)
    FromTask : Mapped["TaskDefinition"] = relationship(foreign_keys='[TaskFlow.FromTaskId]', back_populates=("TaskFlowList"))
    ToTask : Mapped["TaskDefinition"] = relationship(foreign_keys='[TaskFlow.ToTaskId]', back_populates=("ToTaskTaskFlowList"))

    # child relationships (access children)



class WFActivityLog(Base):  # type: ignore
    __tablename__ = 'WF_ActivityLog'
    _s_collection_name = 'WFActivityLog'  # type: ignore

    ActivityID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    ActionType = Column(Unicode(200), nullable=False)
    ActionDetails = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    UserName = Column(Unicode(200), nullable=False)
    ActivityType = Column(Unicode(100), nullable=False)
    Status = Column(ForeignKey('WF_ActivityStatus.StatusCode'), server_default=text('APP'), nullable=False)
    Category = Column(Unicode(100))
    ActivityDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False, index=True)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFActivityLogList"))
    WF_ActivityStatus: Mapped["WFActivityStatus"] = relationship(back_populates=("WFActivityLogList"))

    # child relationships (access children)



class WFApplicationComment(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationComments'
    _s_collection_name = 'WFApplicationComment'  # type: ignore

    CommentID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    Author = Column(Unicode(200), nullable=False)
    CommentText = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CommentType = Column(Unicode(50), server_default=text('internal'), nullable=False)
    Category = Column(Unicode(100))
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFApplicationCommentList"))

    # child relationships (access children)



class WFApplicationMessage(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationMessages'
    _s_collection_name = 'WFApplicationMessage'  # type: ignore

    MessageID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    FromUser = Column(Unicode(200), nullable=False)
    ToUser = Column(Unicode(200), nullable=False)
    MessageText = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MessageType = Column(Unicode(50), server_default=text('outgoing'), nullable=False)
    Priority = Column(Unicode(20), server_default=text('normal'), nullable=False)
    SentDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFApplicationMessageList"))

    # child relationships (access children)



class WFCompany(Base):  # type: ignore
    __tablename__ = 'WF_Companies'
    _s_collection_name = 'WFCompany'  # type: ignore

    CompanyID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    KashrusCompanyID = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFCompanyList"))

    # child relationships (access children)



class WFContact(Base):  # type: ignore
    __tablename__ = 'WF_Contacts'
    _s_collection_name = 'WFContact'  # type: ignore

    ContactID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFContactList"))

    # child relationships (access children)



class WFFile(Base):  # type: ignore
    __tablename__ = 'WF_Files'
    _s_collection_name = 'WFFile'  # type: ignore

    FileID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    FileName = Column(Unicode(500), nullable=False)
    FileType = Column(ForeignKey('WF_FileTypes.FileType'), nullable=False)
    FileSize = Column(Unicode(20))
    UploadedDate = Column(Date, nullable=False)
    Tag = Column(Unicode(200))
    IsProcessed = Column(Boolean, server_default=text("0"), nullable=False)
    RecordCount = Column(Integer)
    FilePath = Column(Unicode(1000))
    CCreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False) #TODO
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFFileList"))
    WF_FileType : Mapped["WFFileType"] = relationship(back_populates=("WFFileList"))

    # child relationships (access children)



class WFPlant(Base):  # type: ignore
    __tablename__ = 'WF_Plants'
    _s_collection_name = 'WFPlant'  # type: ignore

    PlantID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    PlantNumber = Column(Unicode(50))
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFPlantList"))

    # child relationships (access children)
   # WFProductList : Mapped[List["WFProduct"]] = relationship(back_populates="Plant")



class WFQuote(Base):  # type: ignore
    __tablename__ = 'WF_Quotes'
    _s_collection_name = 'WFQuote'  # type: ignore

    QuoteID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    QuoteNumber = Column(Unicode(50), nullable=False, unique=True)
    TotalAmount : DECIMAL = Column(DECIMAL(10, 2), nullable=False)
    ValidUntil = Column(Date, nullable=False)
    Status = Column(ForeignKey('WF_QuoteStatus.StatusCode'), server_default=text('PEND'), nullable=False)
    LastUpdatedDate = Column(Date, nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFQuoteList"))
    WF_QuoteStatu : Mapped["WFQuoteStatus"] = relationship(back_populates=("WFQuoteList"))

    # child relationships (access children)
    WFQuoteItemList : Mapped[List["WFQuoteItem"]] = relationship(back_populates="Quote")



class ProcessMessage(Base):  # type: ignore
    __tablename__ = 'ProcessMessages'
    _s_collection_name = 'ProcessMessage'  # type: ignore

    MessageId = Column(Integer, autoincrement=True, primary_key=True)
    InstanceId = Column(ForeignKey('ProcessInstances.InstanceId'), nullable=False)
    FromUser = Column(Unicode(100), nullable=False)
    ToUser = Column(Unicode(100), index=True)
    ToRole = Column(Unicode(50))
    MessageType = Column(ForeignKey('ProcessMessageTypes.MessageTypeCode'), server_default=text('Standard'))
    Subject = Column(Unicode(200))
    MessageBody = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SentDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    ReadDate = Column(DATETIME2)
    IsRead = Column(Boolean, server_default=text("0"), nullable=False, index=True)

    # parent relationships (access parent)
    Instance : Mapped["ProcessInstance"] = relationship(back_populates=("ProcessMessageList"))
    ProcessMessageType : Mapped["ProcessMessageType"] = relationship(back_populates=("ProcessMessageList"))

    # child relationships (access children)



class StageInstance(Base):  # type: ignore
    __tablename__ = 'StageInstance'
    _s_collection_name = 'StageInstance'  # type: ignore

    StageInstanceId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessInstanceId = Column(ForeignKey('ProcessInstances.InstanceId'), nullable=False)
    LaneId = Column(ForeignKey('LaneDefinitions.LaneId'), nullable=False)
    Status = Column(ForeignKey('StageStatus.StatusCode'), server_default=text("NEW"), nullable=False)
    StartedDate = Column(DATETIME2)
    CompletedDate = Column(DATETIME2)
    DurationDays = Column(Integer, Computed('(datediff(day,[StartedDate],[CompletedDate]))', persisted=False))
    RetryCount = Column(Integer)
    AssignedTo = Column(Unicode(100))
    AssignedBy = Column(Unicode(100))
    AssignedDate = Column(DATETIME2)
    CompletedCount = Column(Integer)
    TotalCount = Column(Integer)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), default_text=text('system'), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Lane : Mapped["LaneDefinition"] = relationship(back_populates=("StageInstanceList"))
    ProcessInstance : Mapped["ProcessInstance"] = relationship(back_populates=("StageInstanceList"))
    StageStatus : Mapped["StageStatus"] = relationship(back_populates=("StageInstanceList"))

    # child relationships (access children)
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="Stage")



class TaskInstance(Base):  # type: ignore
    __tablename__ = 'TaskInstances'
    _s_collection_name = 'TaskInstance'  # type: ignore

    TaskInstanceId = Column(Integer, autoincrement=True, primary_key=True)
    TaskId = Column(ForeignKey('TaskDefinitions.TaskId'), nullable=False)
    StageId = Column(ForeignKey('StageInstance.StageInstanceId'), nullable=False)
    Status = Column(ForeignKey('TaskStatus.StatusCode'), server_default=text('Pending'), nullable=False, index=True)
    AssignedTo = Column(Unicode(100), index=True)
    StartedDate = Column(DATETIME2, index=True)
    CompletedDate = Column(DATETIME2)
    DurationMinutes = Column(Integer, Computed('(datediff(minute,[StartedDate],[CompletedDate]))', persisted=False))
    Result = Column(Unicode(50))
    ResultData = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    ErrorMessage = Column(Unicode(1000))
    RetryCount = Column(Integer, server_default=text("0"))

    # parent relationships (access parent)
    Stage : Mapped["StageInstance"] = relationship(back_populates=("TaskInstanceList"))
    TaskStatus : Mapped["TaskStatus"] = relationship(back_populates=("TaskInstanceList"))
    TaskDef : Mapped["TaskDefinition"] = relationship(back_populates=("TaskInstanceList"))

    # child relationships (access children)
    TaskCommentList : Mapped[List["TaskComment"]] = relationship(back_populates="TaskInstance")
    WorkflowHistoryList : Mapped[List["WorkflowHistory"]] = relationship(back_populates="TaskInstance")



class WFProduct(Base):  # type: ignore
    __tablename__ = 'WF_Products'
    _s_collection_name = 'WFProduct'  # type: ignore

    ProductID = Column(Integer, server_default=text("0"), primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    action = Column(Unicode(100), server_default=text("('Add')"), nullable=False)
    legacyId = Column(Unicode(50), nullable=False)
    doNotImport = Column(Boolean, server_default=text("((0))"), nullable=False)
    message = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    labelType = Column(Unicode(100), nullable=False)
    labelName = Column(Unicode(100), nullable=False)
    brandName = Column(Unicode(100), nullable=False)
    labelCompanyId = Column(Unicode(50), nullable=False)
    distributorName = Column(Unicode(150), nullable=False)
    group = Column(Unicode(10), nullable=False, index=True)
    symbol = Column(Unicode(20), nullable=False)
    dpm = Column(Unicode(50), nullable=False, index=True)
    category = Column(Unicode(100), nullable=False)
    usePlantStatus = Column(Boolean, nullable=False)
    status = Column(Unicode(50), nullable=False, index=True)
    legacyStatus = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    consumer = Column(Boolean, nullable=False)
    industrial = Column(Boolean, nullable=False)
    finalized = Column(Boolean, nullable=False)
    processedBy = Column(Unicode(100), nullable=False)
    processedDate = Column(Date, nullable=False, index=True)
    notes = Column(Unicode(255), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFProductList"))

    # child relationships (access children)




class WFQuoteItem(Base):  # type: ignore
    __tablename__ = 'WF_QuoteItems'
    _s_collection_name = 'WFQuoteItem'  # type: ignore

    QuoteItemID = Column(Integer, autoincrement=True, primary_key=True)
    QuoteID = Column(ForeignKey('WF_Quotes.QuoteID'), nullable=False)
    Description = Column(Unicode(500), nullable=False)
    Amount : DECIMAL = Column(DECIMAL(10, 2), nullable=False)
    SortOrder = Column(Integer, server_default=text("1"), nullable=False)

    # parent relationships (access parent)
    Quote : Mapped["WFQuote"] = relationship(back_populates=("WFQuoteItemList"))

    # child relationships (access children)



class TaskComment(Base):  # type: ignore
    __tablename__ = 'TaskComments'
    _s_collection_name = 'TaskComment'  # type: ignore

    CommentId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessInstanceId = Column(ForeignKey('ProcessInstances.InstanceId'), nullable=False)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'))
    CommentType = Column(ForeignKey('TaskCommentTypes.CommentTypeCode'), server_default=text('Internal'))
    CommentText = Column(Unicode(250), nullable=False)
    Author = Column(Unicode(100), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    IsVisible = Column(Boolean, server_default=text("1"), nullable=False)

    # parent relationships (access parent)
    TaskCommentType : Mapped["TaskCommentType"] = relationship(back_populates=("TaskCommentList"))
    ProcessInstance : Mapped["ProcessInstance"] = relationship(back_populates=("TaskCommentList"))
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("TaskCommentList"))

    # child relationships (access children)



class ValidationResult(Base):  # type: ignore
    __tablename__ = 'ValidationResults'
    _s_collection_name = 'ValidationResult'  # type: ignore

    ValidationResultId = Column(Integer, autoincrement=True, primary_key=True)
    InstanceId = Column(ForeignKey('ProcessInstances.InstanceId'), nullable=False, index=True)
    ValidationId = Column(ForeignKey('ValidationRules.ValidationId'), nullable=False)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'))
    IsValid = Column(Boolean, nullable=False, index=True)
    ValidationMessage = Column(Unicode(500))
    ValidationDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    ValidatedBy = Column(Unicode(100))

    # parent relationships (access parent)
    #Instance : Mapped["ProcessInstance"] = relationship(back_populates=("ValidationResultList"))
    #TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("ValidationResultList"))
    #Validation : Mapped["ValidationRule"] = relationship(back_populates=("ValidationResultList"))

    # child relationships (access children)



class WFIngredient(Base):  # type: ignore
    __tablename__ = 'WF_Ingredients'
    _s_collection_name = 'WFIngredient'  # type: ignore

    IngredientID = Column(Integer, server_default=text("0"), primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    Source = Column(Unicode(100), nullable=False)
    UKDId = Column(Unicode(50))
    RMC = Column(Unicode(50))
    IngredientName = Column(Unicode(200), nullable=False)
    Manufacturer = Column(Unicode(200), nullable=False)
    Brand = Column(Unicode(200), nullable=False)
    Packaging = Column(Unicode(50), nullable=False)
    Agency = Column(Unicode(20), nullable=False, index=True)
    AddedDate = Column(Date, nullable=False, index=True)
    AddedBy = Column(Unicode(100), nullable=False)
    Status = Column(Unicode(50), nullable=False, index=True)
    NCRCId = Column(Unicode(50), nullable=False, index=True)
    CreatedDate = Column(DATETIME2, server_default=text("(getdate())"))
    ModifiedDate = Column(DATETIME2, server_default=text("(getdate())"))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFIngredientList"))

    # child relationships (access children)





class WorkflowHistory(Base):  # type: ignore
    __tablename__ = 'WorkflowHistory'
    _s_collection_name = 'WorkflowHistory'  # type: ignore

    HistoryId = Column(Integer, autoincrement=True, primary_key=True)
    InstanceId = Column(ForeignKey('ProcessInstances.InstanceId'), nullable=False, index=True)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'))
    Action = Column(Unicode(100), nullable=False)
    PreviousStatus = Column(Unicode(50))
    NewStatus = Column(Unicode(50))
    ActionBy = Column(Unicode(100), server_default=text('system'), nullable=False)
    ActionDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False, index=True)
    ActionReason = Column(Unicode(500))
    Details = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    Instance : Mapped["ProcessInstance"] = relationship(back_populates=("WorkflowHistoryList"))
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("WorkflowHistoryList"))

    # child relationships (access children)
#======== ou_kash tables===========================================

class CompanyApplication(Base):  # type: ignore
    __tablename__ = 'CompanyApplicationWebRequestFromAPI'
    _s_collection_name = 'CompanyApplication'   # type: ignore
    __bind_key__ = 'ou'
    http_methods = ['GET']

    ID = Column(Integer, server_default=text("0"), primary_key=True, nullable=False)
    PreviousCertification = Column(NCHAR(1), server_default=text("N"))
    OUCertified = Column(NCHAR(1), server_default=text("N"))
    CurrentlyCertified = Column(NCHAR(1), server_default=text("N"))
    CompanyID = Column(Integer, server_default=text("0"), index=True)
    CompanyName = Column(Unicode(120), server_default=text(''))
    PlantName = Column(Unicode(120), server_default=text(''))
    Street1 = Column(Unicode(60), server_default=text(''))
    Street2 = Column(Unicode(60), server_default=text(''))
    City = Column(Unicode(40), server_default=text(''))
    State = Column(Unicode(25), server_default=text(''))
    Zip = Column(Unicode(18), server_default=text(''))
    Country = Column(Unicode(25), server_default=text(''))
    title = Column(Unicode(50), server_default=text(''))
    FirstName = Column(Unicode(50), server_default=text(''))
    LastName = Column(Unicode(50), server_default=text(''))
    email = Column(Unicode(100), server_default=text(''))
    phone = Column(Unicode(50), server_default=text(''))
    NatureOfProducts = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    HowHeardAboutUs = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    Comments = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    Description = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    OtherCertification = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    gclid = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    utm_source = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    utm_medium = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    utm_campaign = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text(''))
    dateSubmitted = Column(DATETIME, server_default=text("(getdate())"))
    Utm_Term = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    Version = Column(Unicode(60))
    Language = Column(Unicode(60))
    Oukosher_source = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    JotFormSubmissionID = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    #ApplicationCompany = relationship("COMPANYTB", back_populates="CompanyApplicationList")
    
    # child relationships (access children)

    

class COMPANYTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_TB'
    _s_collection_name = 'COMPANYTB'  # type: ignore
    __table_args__ = (
        Index('idxRC', 'STATUS', 'ACTIVE', 'COMPANY_ID'),
        Index('CompStatus', 'STATUS', 'ACTIVE', 'AcquiredFrom')
    )
    __bind_key__ = 'ou'

    COMPANY_ID = Column(Integer, server_default=text("0"), primary_key=True)
    NAME = Column(String(120), nullable=False)
    LIST = Column(String(1), server_default=text('Y'))
    GP_NOTIFY = Column(TINYINT, server_default=text("0"))
    PRODUCER = Column(Boolean)
    MARKETER = Column(Boolean)
    SOURCE = Column(Boolean)
    IN_HOUSE = Column(String(1))
    PRIVATE_LABEL = Column(String(1))
    COPACKER = Column(String(1))
    JEWISH_OWNED = Column(String(1))
    CORPORATE = Column(String(1))
    COMPANY_TYPE = Column(String(30), server_default=text(""))
    INVOICE_TYPE = Column(String(20), server_default=text("Company Summary"))
    INVOICE_FREQUENCY = Column(String(20))
    INVOICE_DTL = Column(String(20))
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(40))
    RC = Column(String(255))
    PARENT_CO = Column(String(80))
    INVOICE_LAST_DATE = Column(DATETIME2)
    COMPANY_BILL_TO_NAME = Column(String(255))
    ACTIVE = Column(Integer)
    AcquiredFrom = Column(String(50))
    UID = Column(String(50))
    MoveToGP = Column(String(1), server_default=text("('N')"))
    DefaultPO = Column(String(75), server_default=text(''))
    POexpiry = Column(DATETIME2)
    PrivateLabelPO = Column(String(50), server_default=text(''))
    PrivateLabelPOexpiry = Column(DATETIME2)
    VisitPO = Column(String(75), server_default=text(''))
    VisitPOexpiry = Column(DATETIME2)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    CATEGORY = Column(String(50))
    OLDCOMPANYTYPE = Column(String(50))
    BoilerplateInvoiceComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    IsPoRequired = Column(Boolean, server_default=text("0"), nullable=False)
    ShouldPropagateCompanyPo = Column(Boolean, server_default=text("0"), nullable=False)
    ShouldPropagateKscPoToPlants = Column(Boolean, server_default=text("0"), nullable=False)
    ShouldPropagateVisitPoToPlants = Column(Boolean, server_default=text("0"), nullable=False)
    PoReason = Column(String(2000))
    On3rdPartyBilling = Column(Boolean, server_default=text("0"), nullable=False)
    IsTest = Column(Boolean, server_default=text("0"), nullable=False)
    ChometzEmailSentDate = Column(DATETIME2)
    allow_client_generated_ids = True

    # Child relationships (access children)
    #CompanyApplicationList : Mapped[List["CompanyApplication"]] = relationship(back_populates="ApplicationCompany")
    PLANTTBList : Mapped[List["PLANTTB"]] = relationship(back_populates="COMPANY_TB")
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="COMPANY_TB")
    #USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="COMPANY_TB")
    #LabelTbList : Mapped[List["LabelTb"]] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates="COMPANY_TB")

class PLANTTB(Base):  # type: ignore
    __tablename__ = 'PLANT_TB'
    _s_collection_name = 'PLANTTB'  # type: ignore
    __bind_key__ = 'ou'

    PLANT_ID = Column(Integer, primary_key=True, index=True)
    NAME = Column(String(80), nullable=False, index=True)
    GP_NOTIFY = Column(Boolean)
    MULTILINES = Column(String(1))
    PASSOVER = Column(String(1))
    SPECIAL_PROD = Column(String(1), server_default=text("('N')"), nullable=False)
    JEWISH_OWNED = Column(String(1))
    PLANT_TYPE = Column(String(50))
    PLANT_DIRECTIONS = Column(String(800))
    ACTIVE = Column(Integer)
    USDA_CODE = Column(String(15))
    PlantUID = Column(String(75))
    DoNotAttach = Column(String(1))
    OtherCertification = Column(String(500))
    PrimaryCompany = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    DesignatedRFR = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'), ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    MaxOnSiteVisits = Column(SMALLINT, server_default=text("((0))"), nullable=False)
    MaxVirtualVisits = Column(SMALLINT, server_default=text("((0))"), nullable=False)
    IsDaily = Column(Boolean, server_default=text("((0))"), nullable=False)
    allow_client_generated_ids = True

     # parent relationships (access parent)
    #PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList"))
    #PERSON_JOB_TB1 : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList1"), overlaps="PERSON_JOB_TB,PLANTTBList")
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTTBList"))

    # child relationships (access children)
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="PLANT_TB")
    # Child Relationships
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="PLANT_TB")


class OWNSTB(Base):  # type: ignore
    __tablename__ = 'OWNS_TB'
    _s_collection_name = 'OWNSTB'  # type: ignore
    __table_args__ = (
        Index('setupby', 'STATUS', 'ACTIVE'),
        Index('XOWNS', 'PLANT_ID', 'STATUS', 'ID', 'ACTIVE', 'Setup_By'),
        Index('idxCompID', 'COMPANY_ID', 'ACTIVE', 'PLANT_ID', unique=True)
    )
    __bind_key__ = 'ou'

    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False)
    START_DATE = Column(DATETIME)
    END_DATE = Column(DATETIME)
    TYPE = Column(String(10))
    VISIT_FREQUENCY = Column(SMALLINT)
    INVOICE_TYPE = Column(String(20))
    INVOICE_FREQUENCY = Column(String(20))
    INVOICE_DTL = Column(String(20))
    HOLD = Column(String(1))
    ROYALTIES = Column(String(1))
    SPECIAL_TICKET = Column(String(1))
    STATUS = Column(String(40))
    ID = Column(Integer, server_default=text("0"), primary_key=True, unique=True)
    ACTIVE = Column(Integer)
    Setup_By = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    AcquiredFrom = Column(String(50))
    NoRFRneeded = Column(String(1), server_default=text("('N')"), nullable=False)
    LOCtext = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    MoveToGP = Column(String(1), server_default=text("('N')"))
    DefaultPO = Column(String(75), server_default=text("('')"))
    VisitBilling = Column(String(10), server_default=text("('')"))
    PlantName = Column(String(100), server_default=text("('')"))
    ShareAB = Column(String(1), server_default=text("('N')"))
    POexpiry = Column(Date)
    BillingName = Column(String(100))
    PLANT_BILL_TO_NAME = Column(String(80), server_default=text("('')"))
    AutoCertification = Column(Boolean, server_default=text("((0))"), nullable=False)
    primaryCompany = Column(Integer)
    Override = Column(Boolean, server_default=text("((0))"), nullable=False)
    VisitPO = Column(String(75), server_default=text("('')"))
    VisitPOexpiry = Column(DATETIME)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    BoilerplateInvoiceComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    IsCertBillingOverride = Column(Boolean, server_default=text("((0))"), nullable=False)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("OWNSTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("OWNSTBList"))
    #PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(back_populates=("OWNSTBList"))
    

class PLANTADDRESSTB(Base):  # type: ignore
    __tablename__ = 'PLANT_ADDRESS_TB'
    _s_collection_name = 'PLANTADDRESSTB'  # type: ignore
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False, index=True)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(40), nullable=False)
    ATTN = Column(String(40))
    STREET1 = Column(String(60), server_default=text("('')"))
    STREET2 = Column(String(60))
    STREET3 = Column(String(60))
    CITY = Column(String(40), server_default=text("('')"))
    STATE = Column(String(25), server_default=text("('')"))
    ZIP = Column(String(25))
    COUNTRY = Column(String(25), server_default=text("('')"))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTADDRESSTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTADDRESSTBList"))


class USEDIN1TB(Base):  # type: ignore
    __tablename__ = 'USED_IN1_TB'
    _s_collection_name = 'USEDIN1TB'  # type: ignore
    __table_args__ = (
        Index('IdxUsedInLabelIdOwnsIdUidActive', 'LabelID', 'OWNS_ID', 'ID', 'ACTIVE'),
        Index('idxLabelID', 'LabelID', 'OWNS_ID'),
        Index('ix_USED_IN1_TB_ACTIVE_LineItem_includes', 'ACTIVE', 'LineItem'),
        Index('idxSubmissionDetail', 'JobID', 'LineItem', 'ACTIVE')
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    BRAND_NAME = Column(String(100))
    PROC_LINE_ID = Column(Integer)
    START_DATE = Column(SMALLDATETIME, server_default=text("(getdate())"))
    END_DATE = Column(DATETIME)
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(20))
    COMMENT = Column(String(255), server_default=text("('')"))
    ACTIVE = Column(Integer, index=True)
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'), index=True)
    RAW_MATERIAL_CODE = Column(String(500), server_default=text("('')"))
    ENTERED_BY = Column(String(75), server_default=text("(suser_sname())"))
    Ing_Name_ps = Column(String(75))
    JobID = Column(Integer)
    Comment_NTA = Column(String(255))
    LineItem = Column(SMALLINT, index=True)
    DoNotDelete = Column(String(1), server_default=text("('N')"))
    BrokerID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), server_default=text("((0))"))
    PreferredBrokerContactID = Column(Integer, server_default=text("((0))"))
    PreferredSourceContactID = Column(Integer, server_default=text("((0))"))
    PassoverProductionUse = Column(String(15), server_default=text("('Non Passover')"))
    LocReceivedStatus = Column(Integer)
    InternalCode = Column(String(50))
    LabelID = Column(ForeignKey('label_tb.ID'), index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    #COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("USEDIN1TBList"))
    #label_tb : Mapped["LabelTb"] = relationship(back_populates=("USEDIN1TBList"))
    #OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("USEDIN1TBList"))

    # child relationships (access children)


class MERCHTB(Base):  # type: ignore
    __tablename__ = 'MERCH_TB'
    _s_collection_name = 'MERCHTB'  # type: ignore
    __table_args__ = (
        Index('ix_MERCH_TB_ACTIVE_Reviewed_includes', 'ACTIVE', 'Reviewed'),
        Index('idx_MerchandiseID_Active', 'MERCHANDISE_ID', 'ACTIVE', unique=True),
        Index('idxSymbol', 'Symbol', 'MERCHANDISE_ID', 'ACTIVE')
    )
    __bind_key__ = 'ou'

    MERCHANDISE_ID = Column(Integer, server_default=text("0"), primary_key=True)
    NAME = Column(String(225), nullable=False)
    AS_STIPULATED = Column(String(1), server_default=text("('N')"))
    STIPULATION = Column(String(1000), server_default=text("('')"))
    CONFIDENTIAL = Column(String(1), server_default=text("('N')"))
    RETAIL = Column(String(1))
    FOODSERVICE = Column(String(1))
    CONSUMER = Column(String(1))
    INDUSTRIAL = Column(String(1))
    INSTITUTIONAL = Column(String(1), server_default=text("('N')"))
    OUP_REQUIRED = Column(String(2), server_default=text("('N')"))
    GENERIC = Column(String(1))
    SPECIFIED_SOURCE = Column(String(1))
    SPECIFIED_SYMBOL = Column(String(1))
    DESCRIPTION = Column(String(80))
    DPM = Column(String(20))
    PESACH = Column(String(1), server_default=text("('N')"))
    COMMENT = Column(String(250))
    ACTIVE = Column(Integer)
    CONFIDENTIAL_TEXT = Column(String(500))
    GROUP_COMMENT = Column(String(100))
    STATUS = Column(String(25))
    LOC_CATEGORY = Column(String(80), server_default=text("('')"))
    LOC_SELECTED = Column(String(80))
    COMMENTS_SCHED_B = Column(String(250))
    PROD_NUM = Column(String(25), server_default=text("('')"))
    INTERMEDIATE_MIX = Column(String(1), server_default=text("('N')"))
    ALTERNATE_NAME = Column(String(80))
    BrochoCode = Column(SMALLINT, server_default=text("((0))"))
    Brocho2Code = Column(SMALLINT, server_default=text("((0))"))
    CAS = Column(String(30), server_default=text("('')"))
    Symbol = Column(String(50), server_default=text("('')"))
    LOC = Column(Date)
    UKDdisplay = Column(String(1), server_default=text("('Y')"))
    Reviewed = Column(Boolean)
    TransferredTo = Column(Boolean, server_default=text("((0))"), nullable=False)
    TransferredMerch = Column(Integer)
    Special_Status = Column(String(255))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)

    # child relationships (access children)
    #FormulaProductList : Mapped[List["FormulaProduct"]] = relationship(back_populates="MERCH_TB")
    #MERCHOTHERNAMEList : Mapped[List["MERCHOTHERNAME"]] = relationship(back_populates="MERCH_TB")
    #YoshonInfoList : Mapped[List["YoshonInfo"]] = relationship(back_populates="Merch")
    #LabelTbList : Mapped[List["LabelTb"]] = relationship(back_populates="MERCH_TB")
    #FormulaComponentList : Mapped[List["FormulaComponent"]] = relationship(back_populates="MERCH_TB")
    #FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="MERCH_TB")



class FormulaProduct(Base):  # type: ignore
    __tablename__ = 'FormulaProduct'
    _s_collection_name = 'FormulaProduct'  # type: ignore
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    FormulaID = Column(Integer, nullable=False)
    Merchandise_ID = Column(Integer, nullable=False)

    # parent relationships (access parent)
    #MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("FormulaProductList"))


class LabelTb(Base):  # type: ignore
    __tablename__ = 'label_tb'
    _s_collection_name = 'LabelTb'  # type: ignore
    __table_args__ = (
        Index('<idxLBL', 'ACTIVE', 'SRC_MAR_ID'),
        Index('idx_test', 'LABEL_SEQ_NUM', 'ACTIVE'),
        Index('ix_label_tb_ACTIVE_LABEL_SEQ_NUM_AgencyID_includes', 'ACTIVE', 'LABEL_SEQ_NUM', 'AgencyID'),
        Index('labelidx4', 'SRC_MAR_ID', 'ID'),
        Index('cidxLBL', 'ACTIVE', 'SRC_MAR_ID'),
        Index('LabelMerchStat', 'MERCHANDISE_ID', 'ACTIVE'),
        Index('idxlabelmidbrnd', 'MERCHANDISE_ID', 'LABEL_SEQ_NUM'),
        Index('ix_label_tb_ACTIVE_LABEL_SEQ_NUM_includes', 'ACTIVE', 'LABEL_SEQ_NUM'),
        Index('MerchLSN', 'MERCHANDISE_ID', 'LABEL_SEQ_NUM', 'LABEL_TYPE', 'SRC_MAR_ID', 'ACTIVE', 'BRAND_NAME', 'AgencyID', 'SEAL_SIGN', 'NUM_NAME', 'BLK'),
        Index('CompListWithLOC', 'ACTIVE', 'LABEL_SEQ_NUM'),
        Index('ix_label_tb_ACTIVE_LABEL_TYPE_includes', 'ACTIVE', 'LABEL_TYPE'),
        Index('MerchSrc', 'MERCHANDISE_ID', 'SRC_MAR_ID', 'ACTIVE', 'LABEL_SEQ_NUM', 'GRP'),
        Index('idxLSNAgencyIDBLKBrandConfConsGRPetc', 'ACTIVE', 'LABEL_SEQ_NUM'),
        Index('ix_label_tb_LOChold_ACTIVE_AgencyID_LOCholdDate', 'LOChold', 'ACTIVE', 'AgencyID', 'LOCholdDate'),
        Index('IDX_NUM', 'LABEL_NUM', 'MERCHANDISE_ID', 'LABEL_SEQ_NUM', 'SRC_MAR_ID', 'LABEL_TYPE', 'LOChold'),
        Index('IX_Label_OrderAndFilter', 'LABEL_NAME', 'BRAND_NAME', 'LABEL_SEQ_NUM'),
        Index('ix_label_tb_ACTIVE_BRAND_NAME_includes', 'ACTIVE', 'BRAND_NAME')
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True, unique=True)
    MERCHANDISE_ID = Column(Integer, nullable=False)
    LABEL_SEQ_NUM = Column(SMALLINT, nullable=False)
    SYMBOL = Column(String(20))
    INSTITUTIONAL = Column(String(1))
    BLK = Column(String(1), Computed("(case when [GRP]='5' OR [GRP]='4' then 'Y' else 'N' end)", persisted=False), nullable=False)
    SEAL_SIGN = Column(String(30), server_default=text("('{NONE}')"))
    GRP = Column(String(10), server_default=text("((3))"))
    SEAL_SIGN_FLAG = Column(String(1))
    BRAND_NAME = Column(String(100), index=True)
    SRC_MAR_ID = Column(Integer, nullable=False)
    LABEL_NAME = Column(String(225), index=True)
    INDUSTRIAL = Column(String(1))
    CONSUMER = Column(String(1))
    LABEL_TYPE = Column(String(20))
    ACTIVE = Column(Integer)
    SPECIAL_PRODUCTION = Column(String(1))
    CREATE_DATE = Column(DATETIME, server_default=text("(getdate())"), index=True)
    LAST_MODIFY_DATE = Column(DATETIME, server_default=text("(getdate())"), index=True)
    STATUS_DATE = Column(DATETIME)
    JEWISH_ACTION = Column(String(1))
    CREATED_BY = Column(String(100), server_default=text("(suser_sname())"))
    MODIFIED_BY = Column(String(100), server_default=text("(suser_sname())"))
    LABEL_NUM = Column(String(25))
    NUM_NAME = Column(String(251), Computed("(case when [LABEL_NUM] IS NULL OR [LABEL_NUM]='' then [LABEL_NAME] else ([LABEL_NUM]+' ')+[LABEL_NAME] end)", persisted=False), index=True)
    Confidential = Column(String(1))
    AgencyID = Column(String(50), unique=True)
    LOChold = Column(String(1))
    LOCholdDate = Column(DATETIME)
    PassoverSpecialProduction = Column(String(1), server_default=text("('N')"))
    COMMENT = Column(String(1000), server_default=text("('')"))
    DisplayNewlyCertifiedOnWeb = Column(String(1), server_default=text("('N')"))
    Status = Column(String(25))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    LastChangeDate = Column(DATETIME)
    LastChangeReason = Column(String(100))
    LastChangeType = Column(String(100))
    ReplacedByAgencyId = Column(String(50))
    TransferredFromAgencyId = Column(String(50))
    Kitniyot = Column(Boolean)
    IsDairyEquipment = Column(Boolean, server_default=text("((0))"), nullable=False)
    NameNum = Column(String(251), Computed("(ltrim(isnull(concat(nullif([Label_Name],''),case when [Label_Name]<>'' AND [Label_Num]<>'' then ' '+[Label_Num] else [Label_Num] end),'')))", persisted=False))

    # parent relationships (access parent)
    #MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("LabelTbList"))
    #COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList"))
    #COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList1"), overlaps="COMPANY_TB,LabelTbList")

    # child relationships (access children)
    #FormulaComponentList : Mapped[List["FormulaComponent"]] = relationship(back_populates="label_tb")
    #LabelCommentList : Mapped[List["LabelComment"]] = relationship(back_populates="Label")
    #LabelOptionList : Mapped[List["LabelOption"]] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates="label_tb")
    #LabelOptionList1 : Mapped[List["LabelOption"]] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates="label_tb1", overlaps="LabelOptionList")
    #LabelBarcodeList : Mapped[List["LabelBarcode"]] = relationship(back_populates="label")
    #FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="label_tb")
    #USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="label_tb")
    #ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="label_tb")


