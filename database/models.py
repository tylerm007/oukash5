# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import Boolean, Column, Computed, DECIMAL, Date, Float, ForeignKey, Index, Integer, LargeBinary, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 11, 2025 09:08:33
# Database: mssql+pyodbc://sa:Posey3861@localhost:1433/new_dashboard?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no
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
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)

    # child relationships (access children)
    LaneDefinitionList : Mapped[List["LaneDefinition"]] = relationship(back_populates="Process")



class ProcessMessageType(Base):  # type: ignore
    __tablename__ = 'ProcessMessageTypes'
    _s_collection_name = 'ProcessMessageType'  # type: ignore

    MessageTypeCode = Column(Unicode(20), primary_key=True)
    MessageTypeDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



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



class WFActivityStatus(Base):  # type: ignore
    __tablename__ = 'WF_ActivityStatus'
    _s_collection_name = 'WFActivityStatus'  # type: ignore

    StatusCode = Column(Unicode(5), primary_key=True)
    StatusDesc = Column(Unicode(50))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFActivityLogList : Mapped[List["WFActivityLog"]] = relationship(back_populates="WF_ActivityStatu")



class WFApplicationStatus(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationStatus'
    _s_collection_name = 'WFApplicationStatus'  # type: ignore

    StatusCode = Column(Unicode(50), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFApplicationList : Mapped[List["WFApplication"]] = relationship(back_populates="WF_ApplicationStatus")



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
    WFApplicationMessageList : Mapped[List["WFApplicationMessage"]] = relationship(back_populates="WF_Priority")



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
    WFUserRoleList : Mapped[List["WFUserRole"]] = relationship(back_populates="WF_Role")
    RoleAssignmentList : Mapped[List["RoleAssignment"]] = relationship(back_populates="WF_Role")



class WFUser(Base):  # type: ignore
    __tablename__ = 'WF_Users'
    _s_collection_name = 'WFUser'  # type: ignore

    Username = Column(Unicode(100), primary_key=True)
    Email = Column(Unicode(255), nullable=False, unique=True)
    FullName = Column(Unicode(200), nullable=False)
    IsActive = Column(Boolean, server_default=text("1"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    LastLoginDate = Column(DATETIME2)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFUserAdminList : Mapped[List["WFUserAdmin"]] = relationship(foreign_keys='[WFUserAdmin.AdminUserName]', back_populates="WF_User")
    WFUserAdminList1 : Mapped[List["WFUserAdmin"]] = relationship(foreign_keys='[WFUserAdmin.UserName]', back_populates="WF_User1")
    WFUserRoleList : Mapped[List["WFUserRole"]] = relationship(back_populates="WF_User")
    RoleAssignmentList : Mapped[List["RoleAssignment"]] = relationship(back_populates="WF_User")
    WFApplicationMessageList : Mapped[List["WFApplicationMessage"]] = relationship(foreign_keys='[WFApplicationMessage.FromUser]', back_populates="WF_User")
    WFApplicationMessageList1 : Mapped[List["WFApplicationMessage"]] = relationship(foreign_keys='[WFApplicationMessage.ToUser]', back_populates="WF_User1")



class LaneDefinition(Base):  # type: ignore
    __tablename__ = 'LaneDefinitions'
    _s_collection_name = 'LaneDefinition'  # type: ignore

    LaneId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessId = Column(ForeignKey('ProcessDefinitions.ProcessId'), nullable=False)
    LaneName = Column(Unicode(100), nullable=False)
    LaneDescription = Column(Unicode(500))
    EstimatedDurationDays = Column(Integer)
    LaneRole = Column(ForeignKey('LaneRoles.RoleCode'), server_default=text("NCRC"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    LaneRole1 : Mapped["LaneRole"] = relationship(back_populates=("LaneDefinitionList"))
    Process : Mapped["ProcessDefinition"] = relationship(back_populates=("LaneDefinitionList"))

    # child relationships (access children)



class StageDefinition(Base):  # type: ignore
    __tablename__ = 'StageDefinitions'
    _s_collection_name = 'StageDefinition'  # type: ignore

    StageId = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    StageName = Column(Unicode(100), nullable=False)
    StageDescription = Column(Unicode(500))
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("StageDefinitionList"))

    # child relationships (access children)
    StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="Stage")
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="Stage")



class WFApplication(Base):  # type: ignore
    __tablename__ = 'WF_Applications'
    _s_collection_name = 'WFApplication'  # type: ignore

    ApplicationID = Column(Integer, autoincrement=True, primary_key=True, index=True)
    ApplicationNumber = Column(Integer, unique=True)
    CompanyID = Column(Integer, nullable=False, index=True)
    PlantID = Column(Integer)
    Status = Column(ForeignKey('WF_ApplicationStatus.StatusCode'), server_default=text("('NEW')"), nullable=False, index=True)
    Priority = Column(ForeignKey('WF_Priorities.PriorityCode'), server_default=text("('NORMAL')"))

    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("('System')"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    WF_Priority : Mapped["WFPriority"] = relationship(back_populates=("WFApplicationList"))
    WF_ApplicationStatus : Mapped["WFApplicationStatus"] = relationship(back_populates=("WFApplicationList"))

    # child relationships (access children)
    RoleAssignmentList : Mapped[List["RoleAssignment"]] = relationship(back_populates="Application")
    StageDefinitionList : Mapped[List["StageDefinition"]] = relationship(back_populates="Application")
    StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="Application")
    WFActivityLogList : Mapped[List["WFActivityLog"]] = relationship(back_populates="Application")
    WFApplicationMessageList : Mapped[List["WFApplicationMessage"]] = relationship(back_populates="Application")
    WFFileList : Mapped[List["WFFile"]] = relationship(back_populates="Application")
    WFQuoteList : Mapped[List["WFQuote"]] = relationship(back_populates="Application")
    TaskCommentList : Mapped[List["TaskComment"]] = relationship(back_populates="Application")



class WFUserAdmin(Base):  # type: ignore
    __tablename__ = 'WF_UserAdmins'
    _s_collection_name = 'WFUserAdmin'  # type: ignore

    UserName = Column(ForeignKey('WF_Users.Username'), primary_key=True, nullable=False)
    AdminUserName = Column(ForeignKey('WF_Users.Username'), primary_key=True, nullable=False)
    IsPrimary = Column(Boolean, server_default=text("0"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    WF_User : Mapped["WFUser"] = relationship(foreign_keys='[WFUserAdmin.AdminUserName]', back_populates=("WFUserAdminList"))
    WF_User1 : Mapped["WFUser"] = relationship(foreign_keys='[WFUserAdmin.UserName]', back_populates=("WFUserAdminList1"))

    # child relationships (access children)



class WFUserRole(Base):  # type: ignore
    __tablename__ = 'WF_UserRole'
    _s_collection_name = 'WFUserRole'  # type: ignore

    UserName = Column(ForeignKey('WF_Users.Username'), primary_key=True, nullable=False)
    UserRole = Column(ForeignKey('WF_Roles.UserRole'), primary_key=True, nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    WF_User : Mapped["WFUser"] = relationship(back_populates=("WFUserRoleList"))
    WF_Role : Mapped["WFRole"] = relationship(back_populates=("WFUserRoleList"))

    # child relationships (access children)



class RoleAssignment(Base):  # type: ignore
    __tablename__ = 'RoleAssignment'
    _s_collection_name = 'RoleAssignment'  # type: ignore

    RoleAssignmentID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    Role = Column(ForeignKey('WF_Roles.UserRole'), nullable=False)
    Assignee = Column(ForeignKey('WF_Users.Username'), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(32), server_default=text("System"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("RoleAssignmentList"))
    WF_User : Mapped["WFUser"] = relationship(back_populates=("RoleAssignmentList"))
    WF_Role : Mapped["WFRole"] = relationship(back_populates=("RoleAssignmentList"))

    # child relationships (access children)

class StageInstance(Base):  # type: ignore
    __tablename__ = 'StageInstance'
    _s_collection_name = 'StageInstance'  # type: ignore

    StageInstanceId = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(Integer, ForeignKey("WF_Applications.ApplicationID"), nullable=False)
    StageId = Column(ForeignKey('StageDefinitions.StageId'), nullable=False, index=True)
    Status = Column(ForeignKey('StageStatus.StatusCode'), server_default=text("NEW"), nullable=False, index=True)
    StartedDate = Column(DATETIME2) # status IN_PROCESS
    CompletedDate = Column(DATETIME2) # Status COMPLETED
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("StageInstanceList"))
    Stage : Mapped["StageDefinition"] = relationship(back_populates=("StageInstanceList"))
    StageStatus : Mapped["StageStatus"] = relationship(back_populates=("StageInstanceList"))

    # child relationships (access children)
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="Stage")



class TaskDefinition(Base):  # type: ignore
    __tablename__ = 'TaskDefinitions'
    _s_collection_name = 'TaskDefinition'  # type: ignore

    TaskId = Column(Integer, autoincrement=True, primary_key=True)
    StageId = Column(ForeignKey('StageDefinitions.StageId'), nullable=False)
    TaskName = Column(Unicode(100), nullable=False)
    TaskType = Column(ForeignKey('TaskTypes.TaskTypeCode'), nullable=False)
    TaskCategory = Column(ForeignKey('TaskCategories.TaskCategoryCode'))
    Sequence = Column(Integer, nullable=False)
    IsParallel = Column(Boolean, server_default=text("0"), nullable=False)
    AssigneeRole = Column(Unicode(20))
    EstimatedDurationMinutes = Column(Integer)
    IsRequired = Column(Boolean, server_default=text("1"), nullable=False)
    AutoComplete = Column(Boolean, server_default=text("0"), nullable=False)
    Description = Column(Unicode(500))
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))
    PreScriptJson = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    PostScriptJson = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    Stage : Mapped["StageDefinition"] = relationship(back_populates=("TaskDefinitionList"))
    TaskCategory1 : Mapped["TaskCategory"] = relationship(back_populates=("TaskDefinitionList"))
    TaskType1 : Mapped["TaskType"] = relationship(back_populates=("TaskDefinitionList"))

    # child relationships (access children)
    TaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.FromTaskId]', back_populates="FromTask")
    ToTaskTaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.ToTaskId]', back_populates="ToTask")
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="TaskDef")



class WFActivityLog(Base):  # type: ignore
    __tablename__ = 'WF_ActivityLog'
    _s_collection_name = 'WFActivityLog'  # type: ignore

    ActivityID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    ActionType = Column(Unicode(200), nullable=False)
    ActionDetails = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    UserName = Column(Unicode(200), nullable=False)
    ActivityType = Column(Unicode(100), nullable=False)
    Status = Column(ForeignKey('WF_ActivityStatus.StatusCode'), server_default=text("('APP')"), nullable=False)
    Category = Column(Unicode(100))
    ActivityDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False, index=True)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFActivityLogList"))
    WF_ActivityStatu : Mapped["WFActivityStatus"] = relationship(back_populates=("WFActivityLogList"))

    # child relationships (access children)



class WFApplicationMessage(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationMessages'
    _s_collection_name = 'WFApplicationMessage'  # type: ignore

    MessageID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    FromUser = Column(ForeignKey('WF_Users.Username'), nullable=False)
    ToUser = Column(ForeignKey('WF_Users.Username'))
    TaskInstanceId = Column(Integer)
    MessageText = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MessageType = Column(Unicode(50), server_default=text("('internal')"), nullable=False)
    Priority = Column(ForeignKey('WF_Priorities.PriorityCode'), server_default=text("('NORMAL')"), nullable=False)
    SentDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFApplicationMessageList"))
    WF_User : Mapped["WFUser"] = relationship(foreign_keys='[WFApplicationMessage.FromUser]', back_populates=("WFApplicationMessageList"))
    WF_Priority : Mapped["WFPriority"] = relationship(back_populates=("WFApplicationMessageList"))
    WF_User1 : Mapped["WFUser"] = relationship(foreign_keys='[WFApplicationMessage.ToUser]', back_populates=("WFApplicationMessageList1"))

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
    CCreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("('System')"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFFileList"))
    WF_FileType : Mapped["WFFileType"] = relationship(back_populates=("WFFileList"))

    # child relationships (access children)



class WFQuote(Base):  # type: ignore
    __tablename__ = 'WF_Quotes'
    _s_collection_name = 'WFQuote'  # type: ignore

    QuoteID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False, index=True)
    QuoteNumber = Column(Unicode(50), nullable=False, unique=True)
    TotalAmount : DECIMAL = Column(DECIMAL(10, 2), nullable=False)
    ValidUntil = Column(Date, nullable=False)
    Status = Column(ForeignKey('WF_QuoteStatus.StatusCode'), server_default=text("('PEND')"), nullable=False)
    LastUpdatedDate = Column(Date, nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("('System')"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFQuoteList"))
    WF_QuoteStatu : Mapped["WFQuoteStatus"] = relationship(back_populates=("WFQuoteList"))

    # child relationships (access children)
    WFQuoteItemList : Mapped[List["WFQuoteItem"]] = relationship(back_populates="Quote")



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



class TaskInstance(Base):  # type: ignore
    __tablename__ = 'TaskInstances'
    _s_collection_name = 'TaskInstance'  # type: ignore

    TaskInstanceId = Column(Integer, autoincrement=True, primary_key=True)
    TaskId = Column(ForeignKey('TaskDefinitions.TaskId'), nullable=False)
    StageId = Column(ForeignKey('StageInstance.StageInstanceId'), nullable=False, index=True)
    Status = Column(ForeignKey('TaskStatus.StatusCode'), server_default=text("('Pending')"), nullable=False, index=True)
    AssignedTo = Column(Unicode(100), index=True)
    StartedDate = Column(DATETIME2, index=True)
    CompletedDate = Column(DATETIME2)
    Result = Column(Unicode(50))
    ResultData = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    ErrorMessage = Column(Unicode(1000))
    RetryCount = Column(Integer, server_default=text("0"))

    # parent relationships (access parent)
    Stage : Mapped["StageInstance"] = relationship(back_populates=("TaskInstanceList"))
    TaskStatus : Mapped["TaskStatus"] = relationship(back_populates=("TaskInstanceList"))
    TaskDef : Mapped["TaskDefinition"] = relationship(back_populates=("TaskInstanceList"))

    # child relationships (access children)
    EventActionList : Mapped[List["EventAction"]] = relationship(back_populates="TaskInstance")
    TaskCommentList : Mapped[List["TaskComment"]] = relationship(back_populates="TaskInstance")
    WorkflowHistoryList : Mapped[List["WorkflowHistory"]] = relationship(back_populates="TaskInstance")



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



class EventAction(Base):  # type: ignore
    __tablename__ = 'EventAction'
    _s_collection_name = 'EventAction'  # type: ignore

    EventId = Column(Integer, autoincrement=True, primary_key=True)
    EventKey = Column(Unicode(250), nullable=False)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'), nullable=False)
    EventStatus = Column(Unicode(20), server_default=text("('PENDING')"), nullable=False)
    EventType = Column(Unicode(20), server_default=text("('External')"), nullable=False)
    EventMessage = Column(Unicode(500), nullable=False)
    StartDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    DueDate = Column(DATETIME2)
    IsResolved = Column(Boolean, server_default=text("0"), nullable=False)
    ResolvedDate = Column(DATETIME2)

    # parent relationships (access parent)
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("EventActionList"))

    # child relationships (access children)



class TaskComment(Base):  # type: ignore
    __tablename__ = 'TaskComments'
    _s_collection_name = 'TaskComment'  # type: ignore

    CommentId = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(Integer, ForeignKey("WF_Applications.ApplicationID"), nullable=False)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'))
    CommentType = Column(ForeignKey('TaskCommentTypes.CommentTypeCode'), server_default=text("('Internal')"))
    CommentText = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Author = Column(Unicode(100), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    IsVisible = Column(Boolean, server_default=text("1"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("TaskCommentList"))
    TaskCommentType : Mapped["TaskCommentType"] = relationship(back_populates=("TaskCommentList"))
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("TaskCommentList"))

    # child relationships (access children)



class WorkflowHistory(Base):  # type: ignore
    __tablename__ = 'WorkflowHistory'
    _s_collection_name = 'WorkflowHistory'  # type: ignore

    HistoryId = Column(Integer, autoincrement=True, primary_key=True)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'))
    Action = Column(Unicode(100), nullable=False)
    PreviousStatus = Column(Unicode(50))
    NewStatus = Column(Unicode(50))
    ActionBy = Column(Unicode(100), nullable=False)
    ActionDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False, index=True)
    ActionReason = Column(Unicode(500))
    Details = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("WorkflowHistoryList"))

    # child relationships (access children)
