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
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="ProcessDefinition")



class StageDefinition(Base):  # type: ignore
    __tablename__ = 'StageDefinitions'
    _s_collection_name = 'StageDefinition'  # type: ignore

    StageId = Column(Integer, autoincrement=True, primary_key=True)
    StageName = Column(Unicode(100), nullable=False)
    StageDescription = Column(Unicode(500))
    EstimatedDurationDays = Column(Integer)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)

    # child relationships (access children)
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="StageDefinition")
    #StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="StageDefinition")



class StageStatus(Base):  # type: ignore
    __tablename__ = 'StageStatus'
    _s_collection_name = 'StageStatus'  # type: ignore

    StatusCode = Column(Unicode(20), primary_key=True)
    StatusDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    #StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="StageStatus")



class TaskCategory(Base):  # type: ignore
    __tablename__ = 'TaskCategories'
    _s_collection_name = 'TaskCategory'  # type: ignore

    TaskCategoryCode = Column(Unicode(20), primary_key=True)
    TaskCategoryDescription = Column(Unicode(255), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    TaskDefinitionList : Mapped[List["TaskDefinition"]] = relationship(back_populates="TaskCategory1")



class TaskRole(Base):  # type: ignore
    __tablename__ = 'TaskRoles'
    _s_collection_name = 'TaskRole'  # type: ignore

    RoleCode = Column(Unicode(20), primary_key=True)
    RoleDescription = Column(Unicode(255), nullable=False)
    groupAssignment = Column(Boolean, server_default=text("0"), nullable=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



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
    WFQuoteList : Mapped[List["WFQuote"]] = relationship(back_populates="WF_QuoteStatus")

"""
class WFRole(Base):  # type: ignore
    __tablename__ = 'WF_Roles'
    _s_collection_name = 'WFRole'  # type: ignore

    UserRole = Column(Unicode(10), primary_key=True)
    Role = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    WFUSERROLEList : Mapped[List["WFUSERROLE"]] = relationship(back_populates="WF_Role")



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
    # WFUSERADMINList : Mapped[List["WFUSERADMIN"]] = relationship(foreign_keys='[WFUSERADMIN.AdminUserName]', back_populates="WF_User")
    #WFUSERADMINList1 : Mapped[List["WFUSERADMIN"]] = relationship(foreign_keys='[WFUSERADMIN.UserName]', back_populates="WF_User1")
    WFUSERROLEList : Mapped[List["WFUSERROLE"]] = relationship(back_populates="WF_User")
"""

class TaskDefinition(Base):  # type: ignore
    __tablename__ = 'TaskDefinitions'
    _s_collection_name = 'TaskDefinition'  # type: ignore

    TaskId = Column(Integer, autoincrement=True, primary_key=True)
    ProcessDefinitionId = Column(ForeignKey('ProcessDefinitions.ProcessId'), nullable=False)
    TaskName = Column(Unicode(100), nullable=False)
    TaskType = Column(ForeignKey('TaskTypes.TaskTypeCode'), nullable=False)
    TaskCategory = Column(ForeignKey('TaskCategories.TaskCategoryCode'))
    Sequence = Column(Integer, nullable=False)
    StageDefinitionId = Column(ForeignKey('StageDefinitions.StageId'), nullable=False)
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
    ProcessDefinition : Mapped["ProcessDefinition"] = relationship(back_populates=("TaskDefinitionList"))
    StageDefinition : Mapped["StageDefinition"] = relationship(back_populates=("TaskDefinitionList"))
    TaskCategory1 : Mapped["TaskCategory"] = relationship(back_populates=("TaskDefinitionList"))
    TaskType1 : Mapped["TaskType"] = relationship(back_populates=("TaskDefinitionList"))

    # child relationships (access children)
    TaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.FromTaskId]', back_populates="FromTask")
    ToTaskTaskFlowList : Mapped[List["TaskFlow"]] = relationship(foreign_keys='[TaskFlow.ToTaskId]', back_populates="ToTask")
    TaskInstanceList : Mapped[List["TaskInstance"]] = relationship(back_populates="TaskDefinition")



class WFApplication(Base):  # type: ignore
    __tablename__ = 'WF_Applications'
    _s_collection_name = 'WFApplication'  # type: ignore

    ApplicationID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationNumber = Column(Integer, unique=True)
    CompanyID = Column(Integer, nullable=False)
    PlantID = Column(Integer)
    SubmissionDate = Column(Date, server_default=text("getdate()"), nullable=False)
    ExternalAppRef = Column(Integer)
    WFLinkedApp = Column(Integer)
    ApplicationType = Column(Unicode(10), server_default=text('WORKFLOW'))
    Status = Column(ForeignKey('WF_ApplicationStatus.StatusCode'), server_default=text("NEW"), nullable=False)
    Priority = Column(ForeignKey('WF_Priorities.PriorityCode'), server_default=text("NORMAL"))
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    WF_Priority : Mapped["WFPriority"] = relationship(back_populates=("WFApplicationList"))
    WF_ApplicationStatus : Mapped["WFApplicationStatus"] = relationship(back_populates=("WFApplicationList"))

    # child relationships (access children)
    RoleAssigmentList : Mapped[List["RoleAssigment"]] = relationship(back_populates="Application")
    #StageInstanceList : Mapped[List["StageInstance"]] = relationship(back_populates="Application")
    WFApplicationMessageList : Mapped[List["WFApplicationMessage"]] = relationship(back_populates="Application")
    WFFileList : Mapped[List["WFFile"]] = relationship(back_populates="Application")
    WFQuoteList : Mapped[List["WFQuote"]] = relationship(back_populates="Application")
    TaskEventList : Mapped[List["TaskEvent"]] = relationship(back_populates="ApplicationInstance")

"""
class WFUSERROLE(Base):  # type: ignore
    __tablename__ = 'WF_USER_ROLE'
    _s_collection_name = 'WFUSERROLE'  # type: ignore

    UserName = Column(ForeignKey('WF_Users.Username'), primary_key=True, nullable=False)
    UserRole = Column(ForeignKey('WF_Roles.UserRole'), primary_key=True, nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    WF_User : Mapped["WFUser"] = relationship(back_populates=("WFUSERROLEList"))
    WF_Role : Mapped["WFRole"] = relationship(back_populates=("WFUSERROLEList"))

    # child relationships (access children)
"""


class RoleAssigment(Base):  # type: ignore
    __tablename__ = 'RoleAssigment'
    _s_collection_name = 'RoleAssigment'  # type: ignore

    RoleAssigmentID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    Role = Column(Unicode(10), nullable=False)
    Assignee = Column(Unicode(100), nullable=False)
    IsPrimary = Column(Boolean, server_default=text("1"), nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(32), server_default=text("System"), nullable=False)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("RoleAssigmentList"))

    # child relationships (access children)


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



class WFApplicationMessage(Base):  # type: ignore
    __tablename__ = 'WF_ApplicationMessages'
    _s_collection_name = 'WFApplicationMessage'  # type: ignore

    MessageID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    FromUser = Column(Unicode(100), nullable=False)
    ToUser = Column(Unicode(100))
    MessageText = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MessageType = Column(Unicode(50), server_default=text("internal"), nullable=False)
    Priority = Column(ForeignKey('WF_Priorities.PriorityCode'), server_default=text("NORMAL"), nullable=False)
    SentDate = Column(DATETIME2, server_default=text("getdate()"), nullable=False)
    TaskInstanceId = Column(Integer)

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFApplicationMessageList"))
    WF_Priority : Mapped["WFPriority"] = relationship(back_populates=("WFApplicationMessageList"))

    # child relationships (access children)



class WFFile(Base):  # type: ignore
    __tablename__ = 'WF_Files'
    _s_collection_name = 'WFFile'  # type: ignore

    FileID = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    FileName = Column(Unicode(500), nullable=False)
    FileType = Column(ForeignKey('WF_FileTypes.FileType'), nullable=False)
    FileSize = Column(Unicode(20))
    UploadedDate = Column(DATETIME2, nullable=False)
    Tag = Column(Unicode(200))
    IsProcessed = Column(Boolean, server_default=text("0"), nullable=False)
    RecordCount = Column(Integer)
    FilePath = Column(Unicode(1000))
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
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
    ApplicationID = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    QuoteNumber = Column(Unicode(50), nullable=False, unique=True)
    TotalAmount : DECIMAL = Column(DECIMAL(10, 2), nullable=False)
    ValidUntil = Column(Date, nullable=False)
    Status = Column(ForeignKey('WF_QuoteStatus.StatusCode'), server_default=text("PEND"), nullable=False)
    LastUpdatedDate = Column(Date, nullable=False)
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    CreatedBy = Column(Unicode(100), server_default=text("System"), nullable=False)
    ModifiedDate = Column(DATETIME2)
    ModifiedBy = Column(Unicode(100))

    # parent relationships (access parent)
    Application : Mapped["WFApplication"] = relationship(back_populates=("WFQuoteList"))
    WF_QuoteStatus : Mapped["WFQuoteStatus"] = relationship(back_populates=("WFQuoteList"))

    # child relationships (access children)
    WFQuoteItemList : Mapped[List["WFQuoteItem"]] = relationship(back_populates="Quote")



class TaskInstance(Base):  # type: ignore
    __tablename__ = 'TaskInstances'
    _s_collection_name = 'TaskInstance'  # type: ignore

    TaskInstanceId = Column(Integer, autoincrement=True, primary_key=True)
    TaskDefinitionId = Column(ForeignKey('TaskDefinitions.TaskId'), nullable=False)
    ApplicationId = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    StageId = Column(ForeignKey('StageDefinitions.StageId'), nullable=False)
    Status = Column(ForeignKey('TaskStatus.StatusCode'), server_default=text("Pending"), nullable=False)
    AssignedTo = Column(Unicode(100))
    CompletedBy = Column(Unicode(100))
    CompletedCapacity = Column(Unicode(100))
    StartedDate = Column(DATETIME2)
    CompletedDate = Column(DATETIME2)
    IsVisible = Column(Boolean, server_default=text("1"), nullable=False)
    #_DurationMinutes = Column('#DurationMinutes', Integer, Computed('(datediff(minute,[StartedDate],[CompletedDate]))', persisted=False))
    Result = Column(Unicode(50))
    ResultData = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    ErrorMessage = Column(Unicode(1000))
    RetryCount = Column(Integer, server_default=text("0"))
    ActiveStartDate = Column(DATETIME2)

    # parent relationships (access parent)
    Stage : Mapped["StageDefinition"] = relationship(foreign_keys=[StageId])
    TaskStatus: Mapped["TaskStatus"] = relationship(back_populates=("TaskInstanceList"))
    TaskDefinition : Mapped["TaskDefinition"] = relationship(back_populates=("TaskInstanceList"))

    # child relationships (access children)
    EventActionList : Mapped[List["EventAction"]] = relationship(back_populates="TaskInstance")
    TaskEventList : Mapped[List["TaskEvent"]] = relationship(back_populates="TaskInstance")


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
    EventStatus = Column(Unicode(20), server_default=text("PENDING"), nullable=False)
    EventType = Column(Unicode(20), server_default=text("External"), nullable=False)
    EventMessage = Column(Unicode(500), nullable=False)
    StartDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    DueDate = Column(DATETIME2)
    IsResolved = Column(Boolean, server_default=text("0"), nullable=False)
    ResolvedDate = Column(DATETIME2)

    # parent relationships (access parent)
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("EventActionList"))

class WFUserProfile(Base):
    __tablename__ = 'WF_UserProfile'
    _s_collection_name = 'WFUserProfile'  # type: ignore

    Username = Column(Unicode(100), primary_key=True, nullable=False)
    Profile = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    CreatedDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    LastModDate = Column(DATETIME2)
    allow_client_generated_ids = True

    # parent relationships (access parent)


class TaskEvent(Base):
    __tablename__ = 'TaskEvents'
    _s_collection_name = 'TaskEvent'  # type: ignore

    TaskEventId = Column(Integer, autoincrement=True, primary_key=True)
    ApplicationId = Column(ForeignKey('WF_Applications.ApplicationID'), nullable=False)
    TaskInstanceId = Column(ForeignKey('TaskInstances.TaskInstanceId'), nullable=False)
    Action = Column(Unicode(100), nullable=False)
    PreviousStatus = Column(Unicode(50))
    NewStatus = Column(Unicode(50))
    ActionBy = Column(Unicode(100), nullable=False)
    ActionDate = Column(DATETIME2, server_default=text("getutcdate()"), nullable=False)
    ActionReason = Column(Unicode(250))
    Details = Column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    TaskInstance : Mapped["TaskInstance"] = relationship(back_populates=("TaskEventList"))
    ApplicationInstance : Mapped['WFApplication'] = relationship(back_populates=("TaskEventList"))

    # child relationships (access children)
