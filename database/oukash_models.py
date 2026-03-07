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
# Created:  March 06, 2026 20:26:21
# Database: mssql+pyodbc://apilogic:2Rtrzc8iLovpU!Hv8gG*@kash-sql-st.nyc.ou.org/dashboardV1?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no&Encrypt=no
# Dialect:  mssql
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Basesubmission = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Basesubmission.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mssql import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')


#======== ou_kash tables===========================================

class CompanyApplication(Base):  # type: ignore
    __tablename__ = 'CompanyApplicationWebRequestFromAPI'
    _s_collection_name = 'CompanyApplication'   # type: ignore
    __bind_key__ = 'ou'
    http_methods = ['GET','POST','PUT','DELETE']

    ID = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
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
    dateSubmitted = Column(DATETIME, server_default=text("getdate()"))
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
        Index('CompStatus', 'STATUS', 'ACTIVE', 'AcquiredFrom'),
        {"implicit_returning": False}  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    COMPANY_ID = Column(Integer, autoincrement=True, primary_key=True)
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
    MoveToGP = Column(String(1), server_default=text("N"))
    DefaultPO = Column(String(75), server_default=text(''))
    POexpiry = Column(DATETIME2)
    PrivateLabelPO = Column(String(50), server_default=text(''))
    PrivateLabelPOexpiry = Column(DATETIME2)
    VisitPO = Column(String(75), server_default=text(''))
    VisitPOexpiry = Column(DATETIME2)
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)
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

    # parent relationships (access parent)

    # child relationships (access children)
    COMPANYADDRESSTBList : Mapped[List["COMPANYADDRESSTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTTBList : Mapped[List["PLANTTB"]] = relationship(back_populates="COMPANY_TB")
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTCERTDETAILList : Mapped[List["PLANTCERTDETAIL"]] = relationship(back_populates="COMPANY_TB")
    PLANTCOMMENTList : Mapped[List["PLANTCOMMENT"]] = relationship(back_populates="COMPANY_TB")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="COMPANY_TB")
    LabelTbList : Mapped[List["LabelTb"]] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates="COMPANY_TB")
    #INVOICEFEEList : Mapped[List["INVOICEFEE"]] = relationship(back_populates="COMPANY_TB")
    PERSON_JOB_TBList : Mapped[List["PERSONJOBTB"]] = relationship(back_populates="COMPANY_TB") 
    CompanyContactList: Mapped[List["CompanyContacts"]] = relationship(back_populates="COMPANY_TB")
    
class COMPANYADDRESSTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_ADDRESS_TB'
    _s_collection_name = 'COMPANYADDRESSTB'  # type: ignore
    __table_args__ = (
        Index('compaddress2', 'COMPANY_ID', 'ADDRESS_SEQ_NUM', 'ACTIVE'),
        {"implicit_returning": False}  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(40))
    ATTN = Column(String(40))
    STREET1 = Column(String(60), server_default=text(""))
    STREET2 = Column(String(60), server_default=text(""))
    STREET3 = Column(String(60))
    CITY = Column(String(40), server_default=text(""))
    STATE = Column(String(25), server_default=text(""))
    ZIP = Column(String(18))
    COUNTRY = Column(String(25), server_default=text(""))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYADDRESSTBList"))

    # child relationships (access children)
class PLANTTB(Base):  # type: ignore
    __tablename__ = 'PLANT_TB'
    _s_collection_name = 'PLANTTB'  # type: ignore
    __table_args__ = (
        {"implicit_returning": False},  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'
    allow_client_generated_ids = True  # PLANT_ID has no IDENTITY - client must supply the PK

    PLANT_ID = Column(Integer, primary_key=True, index=True, autoincrement=False)
    NAME = Column(String(80), nullable=False, index=True)
    GP_NOTIFY = Column(Boolean)
    MULTILINES = Column(String(1))
    PASSOVER = Column(String(1))
    SPECIAL_PROD = Column(String(1), server_default=text("N"), nullable=False)
    JEWISH_OWNED = Column(String(1))
    PLANT_TYPE = Column(String(50))
    PLANT_DIRECTIONS = Column(String(800))
    ACTIVE = Column(Integer)
    USDA_CODE = Column(String(15))
    PlantUID = Column(String(75))
    DoNotAttach = Column(String(1))
    OtherCertification = Column(String(500))
    PrimaryCompany = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    DesignatedRFR = Column(Integer) #Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)
    MaxOnSiteVisits = Column(SMALLINT, server_default=text("0"), nullable=False)
    MaxVirtualVisits = Column(SMALLINT, server_default=text("0"), nullable=False)
    IsDaily = Column(Boolean, server_default=text("0"), nullable=False)
    

     # parent relationships (access parent)
    #PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList"))
    #PERSON_JOB_TB1 : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList1"), overlaps="PERSON_JOB_TB,PLANTTBList")
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTTBList"))

    # child relationships (access children)
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="PLANT_TB")
    # Child Relationships
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="PLANT_TB")
    PLANTCERTDETAILList : Mapped[List["PLANTCERTDETAIL"]] = relationship(back_populates="PLANT_TB")
    PLANTCOMMENTList : Mapped[List["PLANTCOMMENT"]] = relationship(back_populates="PLANT_TB")
    #USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="PLANT_TB")
    #INVOICEFEEList : Mapped[List["INVOICEFEE"]] = relationship(back_populates="PLANT_TB") # s/b ownstb

class OWNSTB(Base):  # type: ignore
    __tablename__ = 'OWNS_TB'
    _s_collection_name = 'OWNSTB'  # type: ignore
    __table_args__ = (
        Index('setupby', 'STATUS', 'ACTIVE'),
        Index('XOWNS', 'PLANT_ID', 'STATUS', 'ID', 'ACTIVE', 'Setup_By'),
        Index('idxCompID', 'COMPANY_ID', 'ACTIVE', 'PLANT_ID', unique=True),
        {"implicit_returning": False}  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True, unique=True)
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
    ACTIVE = Column(Integer)
    Setup_By = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    AcquiredFrom = Column(String(50))
    NoRFRneeded = Column(String(1), server_default=text("N"), nullable=False)
    LOCtext = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    MoveToGP = Column(String(1), server_default=text("N"))
    DefaultPO = Column(String(75), server_default=text(""))
    VisitBilling = Column(String(10), server_default=text(""))
    PlantName = Column(String(100), server_default=text(""))
    ShareAB = Column(String(1), server_default=text("N"))
    POexpiry = Column(Date)
    BillingName = Column(String(100))
    PLANT_BILL_TO_NAME = Column(String(80), server_default=text(""))
    AutoCertification = Column(Boolean, server_default=text("0"), nullable=False)
    primaryCompany = Column(Integer)
    Override = Column(Boolean, server_default=text("0"), nullable=False)
    VisitPO = Column(String(75), server_default=text(""))
    VisitPOexpiry = Column(DATETIME)
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)
    BoilerplateInvoiceComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    IsCertBillingOverride = Column(Boolean, server_default=text("0"), nullable=False)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("OWNSTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("OWNSTBList"))
    #PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(back_populates=("OWNSTBList"))
    
    #Children
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="OWNS_TB")
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="OWNS_TB")

class PLANTADDRESSTB(Base):  # type: ignore
    __tablename__ = 'PLANT_ADDRESS_TB'
    _s_collection_name = 'PLANTADDRESSTB'  # type: ignore
    __table_args__ =  ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False, index=True)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(40), nullable=False)
    ATTN = Column(String(40))
    STREET1 = Column(String(60), server_default=text(""))
    STREET2 = Column(String(60))
    STREET3 = Column(String(60))
    CITY = Column(String(40), server_default=text(""))
    STATE = Column(String(25), server_default=text(""))
    ZIP = Column(String(25))
    COUNTRY = Column(String(25), server_default=text(""))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTADDRESSTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTADDRESSTBList"))

    # child relationships (access children)


class USEDIN1TB(Base):  # type: ignore
    __tablename__ = 'USED_IN1_TB'
    _s_collection_name = 'USEDIN1TB'  # type: ignore
    __table_args__ = (
        Index('IdxUsedInLabelIdOwnsIdUidActive', 'LabelID', 'OWNS_ID', 'ID', 'ACTIVE'),
        Index('idxLabelID', 'LabelID', 'OWNS_ID'),
        Index('ix_USED_IN1_TB_ACTIVE_LineItem_includes', 'ACTIVE', 'LineItem'),
        Index('idxSubmissionDetail', 'JobID', 'LineItem', 'ACTIVE'),
        {"implicit_returning": False}  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    BRAND_NAME = Column(String(100))
    PROC_LINE_ID = Column(Integer)
    START_DATE = Column(SMALLDATETIME, server_default=text("getdate()"))
    END_DATE = Column(DATETIME)
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(20))
    COMMENT = Column(String(255), server_default=text(""))
    ACTIVE = Column(Integer, index=True)
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'), index=True)
    RAW_MATERIAL_CODE = Column(String(500), server_default=text(""))
    ENTERED_BY = Column(String(75), server_default=text("suser_sname()"))
    Ing_Name_ps = Column(String(75))
    JobID = Column(Integer)
    Comment_NTA = Column(String(255))
    LineItem = Column(SMALLINT, index=True)
    DoNotDelete = Column(String(1), server_default=text("N"))
    BrokerID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), server_default=text("0"))
    PreferredBrokerContactID = Column(Integer, server_default=text("0"))
    PreferredSourceContactID = Column(Integer, server_default=text("0"))
    PassoverProductionUse = Column(String(15), server_default=text("('Non Passover')"))
    LocReceivedStatus = Column(Integer)
    InternalCode = Column(String(50))
    LabelID = Column(ForeignKey('label_tb.ID'), index=True)
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("USEDIN1TBList"))
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("USEDIN1TBList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("USEDIN1TBList"))
    #PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("USEDIN1TBList"))

    # child relationships (access children)


class MERCHTB(Base):  # type: ignore
    __tablename__ = 'MERCH_TB'
    _s_collection_name = 'MERCHTB'  # type: ignore
    __table_args__ = (
        Index('ix_MERCH_TB_ACTIVE_Reviewed_includes', 'ACTIVE', 'Reviewed'),
        Index('idx_MerchandiseID_Active', 'MERCHANDISE_ID', 'ACTIVE', unique=True),
        Index('idxSymbol', 'Symbol', 'MERCHANDISE_ID', 'ACTIVE'),
        {"implicit_returning": False}  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    MERCHANDISE_ID = Column(Integer, autoincrement=True, primary_key=True)
    NAME = Column(String(225), nullable=False)
    AS_STIPULATED = Column(String(1), server_default=text("N"))
    STIPULATION = Column(String(1000), server_default=text(""))
    CONFIDENTIAL = Column(String(1), server_default=text("N"))
    RETAIL = Column(String(1))
    FOODSERVICE = Column(String(1))
    CONSUMER = Column(String(1))
    INDUSTRIAL = Column(String(1))
    INSTITUTIONAL = Column(String(1), server_default=text("N"))
    OUP_REQUIRED = Column(String(2), server_default=text("N"))
    GENERIC = Column(String(1))
    SPECIFIED_SOURCE = Column(String(1))
    SPECIFIED_SYMBOL = Column(String(1))
    DESCRIPTION = Column(String(80))
    DPM = Column(String(20))
    PESACH = Column(String(1), server_default=text("N"))
    COMMENT = Column(String(250))
    ACTIVE = Column(Integer)
    CONFIDENTIAL_TEXT = Column(String(500))
    GROUP_COMMENT = Column(String(100))
    STATUS = Column(String(25))
    LOC_CATEGORY = Column(String(80), server_default=text(""))
    LOC_SELECTED = Column(String(80))
    COMMENTS_SCHED_B = Column(String(250))
    PROD_NUM = Column(String(25), server_default=text(""))
    INTERMEDIATE_MIX = Column(String(1), server_default=text("N"))
    ALTERNATE_NAME = Column(String(80))
    BrochoCode = Column(SMALLINT, server_default=text("0"))
    Brocho2Code = Column(SMALLINT, server_default=text("0"))
    CAS = Column(String(30), server_default=text(""))
    Symbol = Column(String(50), server_default=text(""))
    LOC = Column(Date)
    UKDdisplay = Column(String(1), server_default=text("('Y')"))
    Reviewed = Column(Boolean)
    TransferredTo = Column(Boolean, server_default=text("0"), nullable=False)
    TransferredMerch = Column(Integer)
    Special_Status = Column(String(255))
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)

    # child relationships (access children)
    FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="MERCH_TB")
    LabelTbList : Mapped[List["LabelTb"]] = relationship(back_populates=("MERCH_TB"))
    FormulaProductList : Mapped[List["FormulaProduct"]] = relationship(back_populates=("MERCH_TB"))


class FormulaProduct(Base):  # type: ignore
    __tablename__ = 'FormulaProduct'
    _s_collection_name = 'FormulaProduct'  # type: ignore
    __table_args__ =  ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    FormulaID = Column(Integer, nullable=False)
    Merchandise_ID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), nullable=False)

    # parent relationships (access parent)
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("FormulaProductList"))


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
        Index('ix_label_tb_ACTIVE_BRAND_NAME_includes', 'ACTIVE', 'BRAND_NAME'),
        {"implicit_returning": False},  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, server_default=text("0"), primary_key=True, unique=True)
    MERCHANDISE_ID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), nullable=False)
    LABEL_SEQ_NUM = Column(SMALLINT, nullable=False)
    SYMBOL = Column(String(20))
    INSTITUTIONAL = Column(String(1))
    BLK = Column(String(1), Computed("(case when [GRP]='5' OR [GRP]='4' then 'Y' else 'N' end)", persisted=False), nullable=False)
    SEAL_SIGN = Column(String(30), server_default=text("('{NONE}')"))
    GRP = Column(String(10), server_default=text("3"))
    SEAL_SIGN_FLAG = Column(String(1))
    BRAND_NAME = Column(String(100), index=True)
    SRC_MAR_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    LABEL_NAME = Column(String(225), index=True)
    INDUSTRIAL = Column(String(1))
    CONSUMER = Column(String(1))
    LABEL_TYPE = Column(String(20))
    ACTIVE = Column(Integer)
    SPECIAL_PRODUCTION = Column(String(1))
    CREATE_DATE = Column(DATETIME, server_default=text("getdate()"), index=True)
    LAST_MODIFY_DATE = Column(DATETIME, server_default=text("getdate()"), index=True)
    STATUS_DATE = Column(DATETIME)
    JEWISH_ACTION = Column(String(1))
    CREATED_BY = Column(String(100), server_default=text("suser_sname()"))
    MODIFIED_BY = Column(String(100), server_default=text("suser_sname()"))
    LABEL_NUM = Column(String(25))
    NUM_NAME = Column(String(251), Computed("(case when [LABEL_NUM] IS NULL OR [LABEL_NUM]='' then [LABEL_NAME] else ([LABEL_NUM]+' ')+[LABEL_NAME] end)", persisted=False), index=True)
    Confidential = Column(String(1))
    AgencyID = Column(String(50), unique=True)
    LOChold = Column(String(1))
    LOCholdDate = Column(DATETIME)
    PassoverSpecialProduction = Column(String(1), server_default=text("N"))
    COMMENT = Column(String(1000), server_default=text(""))
    DisplayNewlyCertifiedOnWeb = Column(String(1), server_default=text("N"))
    Status = Column(String(25))
    #ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    #ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    #CHANGESET_ID = Column(Integer, index=True)
    LastChangeDate = Column(DATETIME)
    LastChangeReason = Column(String(100))
    LastChangeType = Column(String(100))
    ReplacedByAgencyId = Column(String(50))
    TransferredFromAgencyId = Column(String(50))
    Kitniyot = Column(Boolean)
    IsDairyEquipment = Column(Boolean, server_default=text("0"), nullable=False)
    NameNum = Column(String(251), Computed("(ltrim(isnull(concat(nullif([Label_Name],''),case when [Label_Name]<>'' AND [Label_Num]<>'' then ' '+[Label_Num] else [Label_Num] end),'')", persisted=False))

    # parent relationships (access parent)
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("LabelTbList"))
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList"))
    #COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList1"), overlaps="COMPANY_TB,LabelTbList")

    # child relationships (access children)
    FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="label_tb")
    #ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="label_tb")
    #LabelBarcodeList : Mapped[List["LabelBarcode"]] = relationship(back_populates="label")
    #FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="label_tb")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="label_tb")
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="label_tb")


class PLANTCERTDETAIL(Base):  # type: ignore
    __tablename__ = 'PLANT_CERT_DETAIL'
    _s_collection_name = 'PLANTCERTDETAIL'  # type: ignore
    __table_args__ = (
        Index('IX_PLANT_CERT_DETAIL', 'COMPANY_ID', 'PLANT_ID', 'COMPANY_FEE_ID'),
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False)
    COMPANY_FEE_ID = Column(Integer, nullable=False)
    CERT_DETAIL_SEQ_NUM = Column(SMALLINT, nullable=False)
    CERT_DETAIL_DESCRIPTION = Column(String(80))
    CERT_DETAIL_AMOUNT = Column(MONEY)
    CERT_DETAIL_DATE = Column(DATETIME)
    CERT_DETAIL_PERSON_ID = Column(String(20))
    CERT_DETAIL_COMMENT = Column(String(255))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTCERTDETAILList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTCERTDETAILList"))

    # child relationships (access children)



class PLANTCOMMENT(Base):  # type: ignore
    __tablename__ = 'PLANT_COMMENT'
    _s_collection_name = 'PLANTCOMMENT'  # type: ignore
    __table_args__ = (
        Index('XPKPLANT_COMMENT', 'PLANT_ID', 'COMPANY_ID', 'COMMENT_ID', unique=True),
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMMENT_ID = Column(Integer, nullable=False)
    TIMESTAMP = Column(BINARY(8))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTCOMMENTList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTCOMMENTList"))

    # child relationships (access children)


class FormulaSubmissionComponent(Base):  # type: ignore
    __tablename__ = 'FormulaSubmissionComponents'
    _s_collection_name = 'FormulaSubmissionComponent'  # type: ignore
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    FormulaSubmissionID = Column(Integer, nullable=False)
    UniqueID = Column(String(500))
    RMC = Column(String(500))
    ProductNumber = Column(String(500))
    ComponentName = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ComponentMerchID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'))
    ComponentLabelID = Column(ForeignKey('label_tb.ID'))
    SupplierCode = Column(String(500))
    SupplierName = Column(String(500))
    AgencyName = Column(String(500))
    AgencyID = Column(Integer)
    seq = Column(Integer)

    # parent relationships (access parent)
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("FormulaSubmissionComponentList"))
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("FormulaSubmissionComponentList"))

    # child relationships (access children)

class FormulaSubmissionPlant(Base):  # type: ignore
    __tablename__ = 'FormulaSubmissionPlants'
    _s_collection_name = 'FormulaSubmissionPlant'  # type: ignore
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    FormulaSubmissionID = Column(Integer, nullable=False)
    PlantName = Column(String(100))
    PlantCode = Column(String(100))
    Owns_ID = Column(Integer)
    ActionTaken = Column(String(500))
    ProductionMode = Column(String(50))

    # parent relationships (access parent)

    # child relationships (access children)
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="FormulaSubmissionPlant")
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="FormulaSubmissionPlant")

class ProducedIn1Tb(Base):  # type: ignore
    __tablename__ = 'produced_in1_tb'
    _s_collection_name = 'ProducedIn1Tb'  # type: ignore
    __table_args__ = (
        Index('idxPin1ActiveStatusOwns', 'ACTIVE', 'STATUS', 'OWNS_ID'),
        Index('MerchClust', 'ACTIVE', 'LabelID'),
        Index('idxPin1StatusActiveOwns', 'STATUS', 'ACTIVE', 'OWNS_ID'),
        Index('gbg3', 'STATUS', 'ACTIVE'),
        Index('ix_produced_in1_tb_END_DATE_STATUS_ACTIVE_includes', 'END_DATE', 'STATUS', 'ACTIVE'),
        Index('idxPin1StatusActive', 'STATUS', 'ACTIVE'),
        Index('EyePR', 'LabelID', 'STATUS', 'OWNS_ID', 'ACTIVE', 'DIST'),
        Index('idxProducedIn1EndDate', 'END_DATE', 'ACTIVE')
    )
    __bind_key__ = 'ou'
    
    ID = Column(Integer, autoincrement=True, primary_key=True, index=True)
    PROC_LINE_ID = Column(Integer, server_default=text("1"))
    START_DATE = Column(DATETIME)
    END_DATE = Column(DATETIME)
    REGULAR = Column(String(1), server_default=text(""))
    SPECIAL = Column(String(1))
    PASSOVER = Column(String(20))
    PRIVATE_LABEL_FEE = Column(SMALLMONEY)
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(20))
    SPECIAL_STATUS_1 = Column(String(40), server_default=text(""))
    RC_1 = Column(String(80))
    DATE_1 = Column(DATETIME)
    SPECIAL_STATUS_2 = Column(String(40), server_default=text(""))
    RC_2 = Column(String(80))
    DATE_2 = Column(DATETIME)
    SPECIAL_STATUS_3 = Column(String(40), server_default=text(""))
    RC_3 = Column(String(80))
    DATE_3 = Column(DATETIME)
    SPECIAL_STATUS_4 = Column(String(40), server_default=text(""))
    RC_4 = Column(String(80))
    DATE_4 = Column(DATETIME)
    ACTIVE = Column(Integer)
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'), index=True)
    DATE_CERTIFIED = Column(SMALLDATETIME)
    DATE_LAST_REV = Column(SMALLDATETIME)
    CREATE_DATE = Column(DATETIME, server_default=text("getdate()"), index=True)
    CREATED_BY = Column(String(75))
    MODIFIED_DATE = Column(DATETIME)
    MODIFIED_BY = Column(String(75))
    DIST = Column(Boolean)
    MEHADRIN = Column(Boolean)
    LOTNUM = Column(String(500))
    LabelID = Column(ForeignKey('label_tb.ID'))
    FormulaSubmissionPlantID = Column(ForeignKey('FormulaSubmissionPlants.ID'))
    ProductPlantsID = Column(Integer)
    BatchSheetName = Column(String(40))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    LatestPesachSeason = Column(Integer)

    # parent relationships (access parent)
    FormulaSubmissionPlant : Mapped["FormulaSubmissionPlant"] = relationship(back_populates=("ProducedIn1TbList"))
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("ProducedIn1TbList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("ProducedIn1TbList"))

    # child relationships (access children)
    #ProductJobLineItemList : Mapped[List["ProductJobLineItem"]] = relationship(back_populates="pr")
 
 
 # -------------------------------------- VIEWS -------------------------------------------

class v_PLANT_ADDRESS(Base):
    __tablename__ = 'PLANT_ADDRESS'
    _s_collection_name = 'PLANT_ADDRESS'  # type: ignore
    http_methods = ['GET']
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    PLANT_ID = Column(Integer, nullable=False)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(40), nullable=False)
    ATTN = Column(String(40))
    STREET1 = Column(String(60))
    STREET2 = Column(String(60))
    STREET3 = Column(String(60))
    CITY = Column(String(40))
    STATE = Column(String(25))
    ZIP = Column(String(15))
    COUNTRY = Column(String(25))
    TIMESTAMP = Column(BINARY(8))
    COMPANY_ID = Column(Integer)


class v_CompanyContactsAndAddresses(Base):
    __tablename__ = 'CompanyContactsAndAddresses'
    _s_collection_name = 'CompanyContactsAndAddresses'  # type: ignore
    http_methods= ['GET']
    __bind_key__ = 'ou'

    Company = Column(String(120), nullable=False, primary_key=True)
    Industry = Column(String(50))
    Status = Column(String(40))
    RC = Column(String(255))
    CompanyTitle = Column(String(50))
    Title = Column(String(50))
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Voice = Column(String(50))
    Fax = Column(String(50))
    Email = Column(String(100))
    ContactType = Column(String(23), nullable=False)
    Street1 = Column(String(60))
    Street2 = Column(String(60))
    City = Column(String(40))
    State = Column(String(25))
    Zip = Column(String(18))

class v_Labels(Base):
    __tablename__ = 'v_labels'
    _s_collection_name = 'v_labels'  # type: ignore
    __bind_key__ = 'ou'
    http_methods = ['GET']

    ID = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    MERCHANDISE_ID = Column(Integer, nullable=False)
    LABEL_SEQ_NUM = Column(Integer, nullable=False)
    SYMBOL = Column(String(40), nullable=False)
    INSTITUTIONAL = Column(String(40), nullable=False)
    BLK = Column(String(40), nullable=False)
    SEAL_SIGN = Column(String(40), nullable=False)
    GRP = Column(String(40), nullable=False)
    SEAL_SIGN_FLAG = Column(String(40), nullable=False)
    BRAND_NAME = Column(String(40), nullable=False)
    SRC_MAR_ID = Column(Integer, nullable=False)
    LABEL_NAME = Column(String(40), nullable=False)
    INDUSTRIAL = Column(String(40), nullable=False)
    CONSUMER = Column(String(40), nullable=False)
    LABEL_TYPE = Column(String(40), nullable=False)
    ACTIVE = Column(String(40), nullable=False)
    SPECIAL_PRODUCTION = Column(String(40), nullable=False)
    CREATE_DATE = Column(DATETIME2, nullable=False)
    LAST_MODIFY_DATE = Column(DATETIME2, nullable=False)
    STATUS_DATE = Column(DATETIME2, nullable=False)
    JEWISH_ACTION = Column(String(40), nullable=False)
    CREATED_BY = Column(String(40), nullable=False)
    MODIFIED_BY = Column(String(40), nullable=False)
    LABEL_NUM = Column(String(40), nullable=False)
    NUM_NAME = Column(String(40), nullable=False)
    Confidential = Column(String(40), nullable=False)
    AgencyID = Column(Integer, nullable=False)
    LOChold = Column(String(40), nullable=False)
    LOCholdDate = Column(DATETIME2, nullable=False)
    PassoverSpecialProduction = Column(String(40), nullable=False)
    COMMENT = Column(String(255), nullable=False)
    DisplayNewlyCertifiedOnWeb = Column(String(40), nullable=False)
    Status = Column(String(40), nullable=False)
    ValidFromTime = Column(DATETIME2, nullable=False)
    LastChangeDate = Column(DATETIME2, nullable=False)
    LastChangeReason = Column(String(255), nullable=False)
    LastChangeType = Column(String(40), nullable=False)
    ReplacedByAgencyId = Column(Integer, nullable=False)
    TransferredFromAgencyId = Column(Integer, nullable=False)
    Kitniyot = Column(String(40), nullable=False)
    IsDairyEquipment = Column(String(40), nullable=False)
    NameNum = Column(String(40), nullable=False)
    AS_STIPULATED = Column(String(40), nullable=False)
    STIPULATION = Column(String(40), nullable=False)
    RETAIL = Column(String(40), nullable=False)
    FOODSERVICE = Column(String(40), nullable=False)
    OUP_REQUIRED = Column(String(40), nullable=False)
    GENERIC = Column(String(40), nullable=False)
    SPECIFIED_SOURCE = Column(String(40), nullable=False)
    SPECIFIED_SYMBOL = Column(String(40), nullable=False)
    DESCRIPTION = Column(String(255), nullable=False)
    DPM = Column(String(40), nullable=False)
    PESACH = Column(String(40), nullable=False)
    COMMENT = Column(String(255), nullable=False)
    CONFIDENTIAL_TEXT = Column(String(255), nullable=False)
    GROUP_COMMENT = Column(String(255), nullable=False)
    LOC_CATEGORY = Column(String(40), nullable=False)
    LOC_SELECTED = Column(String(40), nullable=False)
    COMMENTS_SCHED_B = Column(String(40), nullable=False)
    PROD_NUM = Column(String(40), nullable=False)
    INTERMEDIATE_MIX = Column(String(40), nullable=False)
    ALTERNATE_NAME = Column(String(40), nullable=False)
    BrochoCode = Column(String(40), nullable=False)
    Brocho2Code = Column(String(40), nullable=False)
    CAS = Column(String(40), nullable=False)
    LOC = Column(String(40), nullable=False)
    UKDdisplay = Column(String(40), nullable=False)
    Reviewed = Column(String(40), nullable=False)
    TransferredTo = Column(Integer, nullable=False)
    TransferredMerch = Column(Integer, nullable=False)
    Special_Status = Column(String(40), nullable=False)

    #Parent Relationships
    Company = relationship("COMPANYTB", primaryjoin="foreign(v_Labels.SRC_MAR_ID)==COMPANYTB.COMPANY_ID", viewonly=True)
    Merch = relationship("MERCHTB", primaryjoin="foreign(v_Labels.MERCHANDISE_ID)==MERCHTB.MERCHANDISE_ID", viewonly=True)
    #LabelBarcode = relationship("LabelBarcode", primaryjoin="foreign(v_Labels.ID)==LabelBarcode.LabelID", viewonly=True)
    #FormulaSubmissionComponent = relationship("FormulaSubmissionComponent", primaryjoin="foreign(v_Labels.ID)==FormulaSubmissionComponent.ComponentLabelID", viewonly=True)
    #ProducedIn1Tb = relationship("ProducedIn1Tb", primaryjoin="foreign(v_Labels.ID)==ProducedIn1Tb.LabelID", viewonly=True)
    USEDIN1TB = relationship("USEDIN1TB", primaryjoin="foreign(v_Labels.ID)==USEDIN1TB.LabelID", viewonly=True) 
   
class v_Plants(Base):
    __tablename__ = 'v_plants'
    _s_collection_name = 'v_plants'  # type: ignore
    __bind_key__ = 'ou'
    http_methods = ['GET']

    PLANT_ID = Column(Integer, nullable=False, primary_key=True)
    NAME = Column(String(255), nullable=False)
    GP_NOTIFY = Column(String(40), nullable=False)
    MULTILINES = Column(String(40), nullable=False)
    PASSOVER = Column(String(40), nullable=False)
    SPECIAL_PROD = Column(String(40), nullable=False)
    JEWISH_OWNED = Column(String(40), nullable=False)
    PLANT_TYPE = Column(String(40), nullable=False)
    PLANT_DIRECTIONS = Column(String(255), nullable=False)
    ACTIVE = Column(String(40), nullable=False)
    USDA_CODE = Column(String(40), nullable=False)
    PlantUID = Column(String(40), nullable=False)
    DoNotAttach = Column(String(40), nullable=False)
    OtherCertification = Column(String(255), nullable=False)
    PrimaryCompany = Column(String(255), nullable=False)
    DesignatedRFR = Column(String(255), nullable=False)
    ValidFromTime = Column(DATETIME2, nullable=False)
    MaxOnSiteVisits = Column(Integer, nullable=False)
    MaxVirtualVisits = Column(Integer, nullable=False)
    IsDaily = Column(String(40), nullable=False)
    PrimaryCompanyName = Column(String(255), nullable=False)
    DesignatedRFRName = Column(String(255), nullable=False)
    STATUS = Column(String(40), nullable=False)

    # Parent Relationships
    Plant = relationship("PLANTTB", primaryjoin="foreign(v_Plants.PLANT_ID)==PLANTTB.PLANT_ID", viewonly=True)
    Company = relationship("COMPANYTB", primaryjoin="foreign(v_Plants.PrimaryCompany)==COMPANYTB.COMPANY_ID", viewonly=True)
    #RFR = relationship("PERSONJOBTB", primaryjoin="foreign(v_Plants.DesignatedRFR)==PERSONJOBTB.PERSON_JOB_ID", viewonly=True)
    PlantAddress = relationship("PLANTADDRESSTB", primaryjoin="foreign(v_Plants.PLANT_ID)==PLANTADDRESSTB.PLANT_ID", viewonly=True)
    PlantComment = relationship("PLANTCOMMENT", primaryjoin="foreign(v_Plants.PLANT_ID)==PLANTCOMMENT.PLANT_ID", viewonly=True)
    PlantCertDetail = relationship("PLANTCERTDETAIL", primaryjoin="foreign(v_Plants.PLANT_ID)==PLANTCERTDETAIL.PLANT_ID", viewonly=True)
    Owns = relationship("OWNSTB", primaryjoin="foreign(v_Plants.PLANT_ID)==OWNSTB.PLANT_ID", viewonly=True)
    '''    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="PLANT_TB")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="PLANT_TB")
    LabelTbList : Mapped[List["LabelTb"]] = relationship(back_populates=("PLANT_TB"))
    MERCH_TBList : Mapped[List["MERCHTB"]] = relationship(back_populates=("PLANT_TB"))
    FormulaProductList : Mapped[List["FormulaProduct"]] = relationship(back_populates=("PLANT_TB"))
    FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates=("PLANT_TB"))
    FormulaSubmissionPlantList : Mapped[List["FormulaSubmissionPlant"]] = relationship(back_populates=("PLANT_TB"))
    ProductJobLineItemList : Mapped[List["ProductJobLineItem"]] = relationship(back_populates=("PLANT_TB"))
    ProductList : Mapped[List["Product"]] = relationship(back_populates=("PLANT_TB"))
    '''


class INVOICEFEE(Base):  # type: ignore
    __tablename__ = 'INVOICE_FEES'
    _s_collection_name = 'INVOICEFEE'  # type: ignore
    __table_args__ = (
        Index('INVOICE_FEES_INVOICE_ID', 'INVOICE_ID', 'COMPANY_ID', 'TYPE', 'INVOICE_DATE', 'TOTAL_AMOUNT', 'STATUS', 'BILL_TO_CO_ID', 'BILL_TO_PLANT_ID', unique=True),
    )
    __bind_key__ = 'ou'

    INVOICE_ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(Integer, nullable=False) #Column(ForeignKey('COMPANYTB.COMPANY_ID'), nullable=False, index=True)
    TYPE = Column(String(4), nullable=False, index=True)
    INVOICE_TYPE = Column(String(20))
    INVOICE_DATE = Column(DATETIME, index=True)
    FREQ = Column(String(20))
    TOTAL_AMOUNT = Column(MONEY)
    DATE_POSTED = Column(DATETIME)
    STATUS = Column(String(20))
    REPLACED_BY = Column(Integer)
    PAYMENT = Column(MONEY)
    CHECK_NO = Column(String(255))
    CHECK_DATE = Column(DATETIME)
    CHECK_RECEIVED = Column(DATETIME)
    BILL_TO_CO_ID = Column(Integer)
    BILL_TO_PLANT_ID = Column(Integer) # Column(ForeignKey('PLANT_TB.PLANT_ID'), index=True)
    OK_TO_POST = Column(String(1))
    WHO = Column(String(40))
    REPLACEMENT_FOR = Column(Integer)
    BATCH_ID_S36 = Column(String(7))
    BATCH_DATE = Column(DATETIME)
    TRANSFER_FLAG = Column(String(1))
    PRINT_FLAG = Column(String(1))
    HOLD_FLAG = Column(String(1))
    ATTACHED_LETTER = Column(String(20))
    TIMESTAMP = Column(BINARY(8))
    ID = Column(Integer)
    COMMENT = Column(String(255))
    INVOICE_LEVEL = Column(Integer)
    PurchaseOrder = Column(String(75), server_default=text(""))
    DeliveryMethod = Column(String(30), server_default=text(""))
    DeliveryDate = Column(Date)
    OriginalInvoiceAmount = Column(MONEY)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    achPaid = Column(Boolean, server_default=text("0"), nullable=False)
    BatchId = Column(Integer)
    PeriodStart = Column(DATETIME)
    PeriodEnd = Column(DATETIME)
    BalanceInAccounting : DECIMAL = Column(DECIMAL(18, 2), server_default=text("0"))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    #PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("INVOICEFEEList"))
    #COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("INVOICEFEEList"))

    # Child relationships
    #INVOICEFEESDETAILList = Mapped[List["INVOICEFEESDETAIL"]] = relationship(back_populates=("INVOICEFEE"))

class INVOICEFEESDETAIL(Base):  # type: ignore
    __tablename__ = 'INVOICE_FEES_DETAIL'
    _s_collection_name = 'INVOICEFEESDETAIL'  # type: ignore
    __table_args__ = (
        Index('invoiceIdVisitID', 'INVOICE_ID', 'VISIT_ID'),
        Index('XPK_INVOICE_FEES_DET', 'INVOICE_ID', 'INVOICE_LINE'),
        Index('infd', 'INVOICE_ID', 'PERIOD_START_DATE')
    )
    __bind_key__ = 'ou'

    ID = Column(Integer, primary_key=True)
    INVOICE_ID = Column(Integer, nullable=False)
    INVOICE_LINE = Column(Integer, nullable=False)
    VISIT_ID = Column(Integer)
    DESTINATION_TYPE = Column(String(1))
    DESTINATION_ID = Column(Integer, index=True)
    FEE = Column(MONEY)
    EXPENSES = Column(MONEY)
    VISIT_TYPE = Column(String(100))
    VISIT_DATE = Column(DATETIME)
    VISIT_PERSON_JOB_ID = Column(Integer)
    PERIOD_START_DATE = Column(DATETIME)
    PERIOD_END_DATE = Column(DATETIME)
    REASON = Column(String(50))
    TIMESTAMP = Column(BINARY(8))
    ownsID = Column(Integer)
    voided = Column(Boolean, server_default=text("0"), nullable=False)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    allow_client_generated_ids = True

    # Parent relationships (access parent)
    #INVOICEFEE = Mapped["INVOICEFEE"] = relationship(back_populates=("INVOICEFEESDETAILList"))

    class USERTABLE(Base):  # type: ignore
        __tablename__ = 'USER_TABLE'
        _s_collection_name = 'USERTABLE'  # type: ignore
        __bind_key__ = 'ou'

        ID = Column(Integer, autoincrement=True, primary_key=True)
        LOGIN_ID = Column(String(100), nullable=False)
        USER_FNAME = Column(String(40), nullable=False)
        USER_TITLE = Column(String(15))
        USER_LNAME = Column(String(40), nullable=False)
        GROUP_ID = Column(Integer, nullable=False)
        PASSWORD = Column(String(8))
        APPLN_PRIV = Column(String(2), nullable=False)
        SECURITY_PRIV = Column(String(2), nullable=False)
        PERSON_ID = Column(Integer)
        COMMENTS = Column(String(500))
        ACTIVE = Column(String(1))
        email = Column(String(50))
        phone = Column(String(30))
        OUdirectlogin = Column(String(50))
        ValidFromTime = Column(DATETIME2, server_default=text("CONVERT([datetime2](7),'1900-01-01 00:00:00')"), nullable=False)
        ValidToTime = Column(DATETIME2, server_default=text("CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999')"), nullable=False)
        CHANGESET_ID = Column(Integer, index=True)
        allow_client_generated_ids = True

        # parent relationships (access parent)

        # child relationships (access children)
    
    #PERSON_JOB_TB
class PERSONJOBTB(Base):  # type: ignore
    __tablename__ = 'PERSON_JOB_TB'
    _s_collection_name = 'PERSONJOBTB'  # type: ignore
    __table_args__ =  ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    __bind_key__ = 'ou'

    PERSON_JOB_ID = Column(Integer, autoincrement=True, primary_key=True)
    FIRST_NAME = Column(String(50))
    LAST_NAME = Column(String(50))
    TITLE = Column(String(50))
    VOICE = Column(String(50))
    FAX = Column(String(50))
    EMAIL = Column(String(100))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), index=True)
    ACTIVE = Column(String(1))
    CREATED_BY = Column(String(100))
    CREATE_DATE = Column(DATETIME, server_default=text("getdate()"))
    MODIFIED_BY = Column(String(100))
    MODIFY_DATE = Column(DATETIME, server_default=text("getdate()"))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PERSON_JOB_TBList"))

    # child relationships (access children)
    #PERSONTB : Mapped["PERSONTB"] = relationship(back_populates=("PERSON_JOB_TBList"))

class PERSONTB(Base):
    __tablename__ = 'PERSON_TB'
    _s_collection_name = 'person_tb'  # type: ignore
    __table_args__ =  ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    _bind_key__ = 'ou'

    PERSON_ID = Column(Integer, autoincrement=True, primary_key=True)
    FIRST = Column(String(100), nullable=True)
    LAST = Column(String(100), nullable=True)
    MIDDLE = Column(String(50), nullable=True)
    PREFIX = Column(String(50), nullable=True)
    VENDOR_ID = Column(Integer, nullable=True)
    SUFFIX = Column(String(12), nullable=True)
    HIRE_DATE = Column(DATETIME, nullable=True)
    SSN = Column(String(11), nullable=True)
    TIMESTAMP = Column(String(8), nullable=True)
    ACTIVE = Column(Integer, nullable=True)
    SENDTICKETTO = Column(String(255), nullable=True)
    ACCTS_PAY_NUM = Column(String(30), nullable=True)
    MaxPay = Column(String(30), nullable=True)
    MileageRate = Column(String(30), nullable=True)
    WebAccess = Column(String(5), nullable=True)
    GroupLeader = Column(String(40), nullable=True)
    AdministrativeAssistant = Column(Integer, nullable=True)
    KashLogIn = Column(String(75), nullable=True)
    IsGroupLeader = Column(String(1), nullable=True)
    HiddenSSN = Column(String(50), nullable=True)
    WorkflowEmails = Column(String(1), nullable=True)
    Password = Column(String(30), nullable=True)
    PasswordQuestion = Column(String(500), nullable=True)
    PasswordAnswer = Column(String(500), nullable=True)
    #ValidFromTime = Column(DATETIME2, nullable=False)
    #ValidToTime = Column(DATETIME2, nullable=False)
    #CHANGESET_ID = Column(Integer, nullable=True)
    IncludeInIngWFAssignmentList = Column(Boolean, nullable=True)
    TempRfr = Column(Boolean, nullable=False)
    IsBillForMileageDifferential = Column(Boolean, nullable=False)
    AllowCopackerManagement = Column(Boolean, nullable=True)

    # Child Relationships
    #PersonContactList : Mapped[List["PersonContact"]] = relationship(back_populates="PERSONTB")
    #PERSON_JOB_TBList : Mapped[List["PERSONJOBTB"]] = relationship(back_populates=("PERSONTB"))
    
class PersonContact(Base):
    __tablename__ = 'PersonContacts'
    _s_collection_name = 'PersonContacts'  # type: ignore
    #__table_args__ =  ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    Person_ID = Column(ForeignKey('PERSON_TB.PERSON_ID'), index=True)
    BusinessPhone = Column(String(50))
    BusinessEmail = Column(String(100))
    BusinessCell = Column(String(50))
    BusinessFax = Column(String(50))
    HomePhone = Column(String(50))
    HomeEmail = Column(String(100))
    HomeCell = Column(String(50))
    HomeFax = Column(String(50))
    Misc = Column(String(500))

    #Parent Relationships
    #PERSONTB: Mapped["PERSONTB"] = relationship(back_populates="PersonContactList")

class vUserRole(Base):
    __tablename__ = 'UserRoles'
    _s_collection_name = 'vUserRoles'  # type: ignore
    __bind_key__ = 'ou'
    http_methods = ['GET']

    Name = Column(String(100), nullable=False, primary_key=True)
    PERSON_JOB_ID = Column(Integer, nullable=False)
    role = Column(String(100), nullable=False)

    #Parent Relationships
    PERSONJOBTB = relationship("PERSONJOBTB", primaryjoin="foreign(vUserRole.PERSON_JOB_ID)==PERSONJOBTB.PERSON_JOB_ID", viewonly=True)  

class vSelectRFR(Base):
    __tablename__ = 'v_selectRFR'
    _s_collection_name = 'vSelectRFR'  # type: ignore  
    http_methods = ['GET']
    __bind_key__ = 'ou'

    PERSON_ID = Column(Integer, primary_key=True)
    userName = Column(String(100))
    BusinessEmail = Column(String(255))
    fullName = Column(String(200))
    pct_of_total_apps = Column(DECIMAL(5,2))
    pct_of_total_apps_at_work = Column(DECIMAL(5,2))

class vSelectNCRC(Base):
    __tablename__ = 'v_selectNCRC'
    _s_collection_name = 'vSelectNCRC'  # type: ignore  
    http_methods = ['GET']
    __bind_key__ = 'ou'

    PERSON_ID = Column(Integer, primary_key=True)
    userName = Column(String(100))
    BusinessEmail = Column(String(255))
    fullName = Column(String(200))
    pct_of_total_apps = Column(DECIMAL(5,2))
    pct_of_total_apps_at_work = Column(DECIMAL(5,2))

class Contacts(Base):
    __tablename__ = 'contacts'
    _s_collection_name = 'Contacts'  # type: ignore
    __table_args__ = ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause  
    __bind_key__ = 'ou'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    Title = Column(String(50), nullable=True)
    FirstName = Column(String(50), nullable=True)
    LastName = Column(String(50), nullable=True)
    Voice = Column(String(50), nullable=True)
    Fax = Column(String(50), nullable=True)
    Email = Column(String(100), nullable=True)
    Cell = Column(String(50), nullable=True)
    EnteredBy = Column(String(50), nullable=True)
    DateEntered = Column(DATETIME, nullable=True)
    ModifiedBy = Column(String(50), nullable=True)
    DateModified = Column(DATETIME, nullable=True)
    Active = Column(Integer, nullable=True)
    OtherInfo = Column(String(100), nullable=True)

class CompanyContacts(Base):
    __tablename__ = 'companycontacts_tb'
    _s_collection_name = 'CompanyContacts'  # type: ignore
    __table_args__ = ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause  
    __bind_key__ = 'ou'

    ccID = Column(Integer, autoincrement=True, primary_key=True)
    Company_ID = Column(Integer, ForeignKey('COMPANY_TB.COMPANY_ID'), index=True, nullable=False)
    CompanyTitle = Column(String(50))
    PrimaryCT = Column(String(1), nullable=False)
    BillingCT = Column(String(1), nullable=False)
    WebCT = Column(String(1), nullable=False)
    OtherCT = Column(String(1), nullable=False)
    EnteredBy = Column(String(50))
    DateEntered = Column(SMALLDATETIME)
    ModifiedBy = Column(String(50))
    DateModified = Column(DATETIME)
    Active = Column(SMALLINT)
    StatementType = Column(String(1), nullable=False)
    InvoiceType = Column(String(1), nullable=False)
    UserVendorID = Column(String(200))
    UsedInComment = Column(String(500))
    ContactID = Column(Integer, nullable=False)
    LOAtype = Column(String(1))
    EIREmail = Column(String(1))
    ScheduleBEmail = Column(String(1))
    FormulaEmail = Column(String(1))
    PoCT = Column(Boolean, nullable=False)
    CopackerCT = Column(Boolean, nullable=False)
    # Parent Relationships
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("CompanyContactList"))
    #Contacts : Mapped["Contacts"] = relationship(back_populates=("CompanyContactList"))

class PlantContacts(Base):
    __tablename__ = 'plantcontacts_tb'
    _s_collection_name = 'PlantContacts'  # type: ignore
    __table_args__ = ({"implicit_returning": False},)  # MSSQL: table has triggers, cannot use OUTPUT inserted. clause  
    __bind_key__ = 'ou'

    pcID = Column(Integer, autoincrement=True, primary_key=True)
    Owns_ID = Column(Integer)
    CompanyTitle = Column(String(50))
    PrimaryCT = Column(String(1), nullable=False)
    BillingCT = Column(String(1), nullable=False)
    WebCT = Column(String(1), nullable=False)
    OtherCT = Column(String(1), nullable=False)
    EnteredBy = Column(String(50))
    DateEntered = Column(SMALLDATETIME)
    ModifiedBy = Column(String(50))
    DateModified = Column(DATETIME)
    Active = Column(SMALLINT, nullable=False)
    InvoiceType = Column(String(1), nullable=False)
    ContactID = Column(Integer, nullable=False)
    LOAtype = Column(String(1))
    GPC = Column(String(1))
    EIREmail = Column(String(1))
    ScheduleBEmail = Column(String(1))
    FormulaEmail = Column(String(1))
    PoCT = Column(Boolean, nullable=False)