# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import BINARY, BigInteger, Boolean, CHAR, Column, Computed, DECIMAL, Date, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, SmallInteger, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2, MONEY, SMALLDATETIME, SMALLMONEY, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  July 28, 2025 14:37:03
# Database: mssql+pyodbc://apilogic:2Rtrzc8iLovpU!Hv8gG*@kash-sql-st.nyc.ou.org/ou_kash?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no&Encrypt=no
# Dialect:  mssql
#
# mypy: ignore-errors
########################################################################################################################
 
import os
from typing import List

from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType

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



t_ASSIGNED_MASHGIACH = Table(
    'ASSIGNED_MASHGIACH', metadata,
    Column('ID', Integer, nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('PERSON_JOB_ID', Integer),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('VIST_TYPE', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OnSiteVisits', TINYINT, nullable=False),
    Column('VirtualVisits', TINYINT, nullable=False),
    Column('IsDaily', Boolean, nullable=False),
    Column('IsAsNeeded', Boolean, nullable=False),
    Column('SEASONAL_START', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SEASONAL_END', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TIMESTAMP', DateTime),
    Column('OWNS_ID', Integer, nullable=False),
    Column('company_id', Integer, nullable=False),
    Column('OwnsStatus', String(40, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_ASSIGNED_MASHGIACH_OLD = Table(
    'ASSIGNED_MASHGIACH_OLD', metadata,
    Column('ID', Integer, nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('PERSON_JOB_ID', Integer, nullable=False),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('VIST_TYPE', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD1', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD2', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD3', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD_SEASONAL', String(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SEASONAL_START', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SEASONAL_END', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DESIGNATED_MASHGIACH_FLAG', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TIMESTAMP', BINARY(8)),
    Column('DESIGNATED_MASHGIACH', String(150, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OWNS_ID', Integer),
    Column('company_id', Integer, nullable=False)
)


class ASSIGNEDMASHGIACHTB(Base):  # type: ignore
    __tablename__ = 'ASSIGNED_MASHGIACH_TB'
    _s_collection_name = 'ASSIGNEDMASHGIACHTB'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    PLANT_ID = Column(Integer)
    PERSON_JOB_ID = Column(Integer)
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    VIST_TYPE = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    VISIT_PERIOD1 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    VISIT_PERIOD2 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    VISIT_PERIOD3 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    VISIT_PERIOD_SEASONAL = Column(String(1, 'SQL_Latin1_General_CP1_CI_AS'))
    SEASONAL_START = Column(String(3, 'SQL_Latin1_General_CP1_CI_AS'))
    SEASONAL_END = Column(String(3, 'SQL_Latin1_General_CP1_CI_AS'))
    DESIGNATED_MASHGIACH_FLAG = Column(String(1, 'SQL_Latin1_General_CP1_CI_AS'))
    ACTIVE = Column(Integer)
    DESIGNATED_MASHGIACH = Column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    OWNS_ID = Column(Integer)
    company_id = Column(Integer)
    TimestampDateTime = Column(DateTime)
    Timestamp = Column(DateTime)
    CreatedBy = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CreatedDate = Column(DateTime)
    Discriminator = Column(String(1, 'SQL_Latin1_General_CP1_CI_AS'))
    Zone = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer)
    OnSiteVisits = Column(TINYINT, nullable=False)
    VirtualVisits = Column(TINYINT, nullable=False)
    IsDaily = Column(Boolean, nullable=False)
    IsAsNeeded = Column(Boolean, nullable=False)
    SeasonalStart = Column(TINYINT, server_default=text("((1))"), nullable=False)
    SeasonalEnd = Column(TINYINT, server_default=text("((12))"), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)



t_ASSIGNED_MASHGIACH_TB_history_temporal = Table(
    'ASSIGNED_MASHGIACH_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('PLANT_ID', Integer),
    Column('PERSON_JOB_ID', Integer),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('VIST_TYPE', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD1', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD2', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD3', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_PERIOD_SEASONAL', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SEASONAL_START', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SEASONAL_END', String(3, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DESIGNATED_MASHGIACH_FLAG', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ACTIVE', Integer),
    Column('DESIGNATED_MASHGIACH', String(150, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OWNS_ID', Integer),
    Column('company_id', Integer),
    Column('TimestampDateTime', DateTime),
    Column('Timestamp', DateTime),
    Column('CreatedBy', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreatedDate', DateTime),
    Column('Discriminator', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Zone', String(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Column('OnSiteVisits', TINYINT, nullable=False),
    Column('VirtualVisits', TINYINT, nullable=False),
    Column('IsDaily', Boolean, nullable=False),
    Column('IsAsNeeded', Boolean, nullable=False),
    Column('SeasonalStart', TINYINT, server_default=text("((1))"), nullable=False),
    Column('SeasonalEnd', TINYINT, server_default=text("((12))"), nullable=False),
    Index('ASSIGNED_MASHGIACH_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_AchAuthToken_history_temporal = Table(
    'AchAuthToken_history_temporal', metadata,
    Column('company_id', Integer, nullable=False),
    Column('userLogin', String(100), nullable=False),
    Column('link_session_id', String(100), nullable=False),
    Column('public_token', String(100), nullable=False),
    Column('accountID', String(100), nullable=False),
    Column('institutionName', String(100), nullable=False),
    Column('institutionId', String(100), nullable=False),
    Column('accountName', String(100), nullable=False),
    Column('accountMask', String(100), nullable=False),
    Column('accountType', String(100), nullable=False),
    Column('Id', Integer, nullable=False, index=True),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('agreedBy', String(255)),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_AchAuthToken_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_AchPlaidLambdaResponse_history_temporal = Table(
    'AchPlaidLambdaResponse_history_temporal', metadata,
    Column('Id', Integer, nullable=False, index=True),
    Column('company_id', Integer, nullable=False),
    Column('userLogin', String(100), nullable=False),
    Column('stripe_bank_account_token', String(100), nullable=False),
    Column('access_token', String(100)),
    Column('request_id', String(100), nullable=False),
    Column('status_code', String(100), nullable=False),
    Column('accountID', String(100), nullable=False),
    Column('public_token', String(100), nullable=False),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_AchPlaidLambdaResponse_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_AchStripePaymentDetail_history_temporal = Table(
    'AchStripePaymentDetail_history_temporal', metadata,
    Column('Id', Integer, nullable=False, index=True),
    Column('AchStripePaymentId', Integer, nullable=False),
    Column('DocumentNumber', String(100)),
    Column('Amount', DECIMAL(12, 2)),
    Column('TransactionBalance', DECIMAL(12, 2)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_AchStripePaymentDetail_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_AchStripePayment_history_temporal = Table(
    'AchStripePayment_history_temporal', metadata,
    Column('Id', Integer, nullable=False, index=True),
    Column('company_id', Integer, nullable=False),
    Column('UserLogin', String(100)),
    Column('Amount', BigInteger),
    Column('Currency', String(100)),
    Column('Description', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ReceiptEmail', String(100)),
    Column('JsonRet', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('StripeId', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('CHANGESET_ID', Integer, index=True),
    Column('ProcessorType', String(50), nullable=False),
    Column('FeeAmount', BigInteger),
    Column('Comments', String(255)),
    Column('CardKnoxId', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('CustomerFeeWaived', Boolean, nullable=False),
    Index('ix_AchStripePayment_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_Billing_history_temporal = Table(
    'Billing_history_temporal', metadata,
    Column('Id', Integer, nullable=False),
    Column('Kind', String(255)),
    Column('VisitType', String(50)),
    Column('PayType', String(50)),
    Column('Amount', SMALLMONEY, nullable=False),
    Column('VirtualAmount', SMALLMONEY, nullable=False),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Column('COMPANY_ID', Integer),
    Column('OWNS_ID', Integer),
    Column('PFSO_ID', Integer),
    Index('ix_Billing_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_CODE_TB_history_temporal = Table(
    'CODE_TB_history_temporal', metadata,
    Column('CodeId', Integer, nullable=False, index=True),
    Column('TABLE_NAME', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FIELD_NAME', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('VALUE_SEQ_NUM', SmallInteger),
    Column('FIELD_VALUE', String(500, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('VALUE_DESCRIPTION', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PERSON_ID', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TIMESTAMP', DateTime),
    Column('ACTIVE', Integer),
    Column('AdditionalParameters', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IsDefaultValue', Boolean),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('CODE_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_COMPANY_ADDRESS = Table(
    'COMPANY_ADDRESS', metadata,
    Column('ID', Integer, nullable=False),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('ADDRESS_SEQ_NUM', Integer, nullable=False),
    Column('TYPE', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ATTN', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET1', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET2', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET3', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CITY', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STATE', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ZIP', String(18, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('COUNTRY', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TIMESTAMP', BINARY(8))
)


t_COMPANY_ADDRESS_TB_history_temporal = Table(
    'COMPANY_ADDRESS_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('ADDRESS_SEQ_NUM', Integer, nullable=False),
    Column('TYPE', String(40)),
    Column('ATTN', String(40)),
    Column('STREET1', String(60)),
    Column('STREET2', String(60)),
    Column('STREET3', String(60)),
    Column('CITY', String(40)),
    Column('STATE', String(25)),
    Column('ZIP', String(18)),
    Column('COUNTRY', String(25)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('COMPANY_ADDRESS_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_COMPANY_FEE_STRUCTURE_history_temporal = Table(
    'COMPANY_FEE_STRUCTURE_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('COMPANY_FEE_ID', SmallInteger, nullable=False),
    Column('EFFECTIVE_DATE', DateTime),
    Column('APPROVAL', String(1), nullable=False),
    Column('APPROVAL_DATE', DateTime),
    Column('APPROVAL_PERSON_ID', Integer),
    Column('CERT_FEE', MONEY),
    Column('EXPENSE_TYPE', String(15)),
    Column('EXPENSE_AMT', MONEY),
    Column('EXPENSE_PERCENT', Float(53)),
    Column('VISIT_FEE_TYPE', String(20)),
    Column('FREE_VISITS_NUM', Integer),
    Column('VISIT_FEE', MONEY),
    Column('SPECIAL_PRODUCTION_TYPE', String(20)),
    Column('SPECIAL_PRODUCTION_FEE', SMALLMONEY),
    Column('UNIT_BASE', Integer),
    Column('PASSOVER_FEE_TYPE', String(25)),
    Column('PASSOVER_FEE', SMALLMONEY),
    Column('PASSOVER_VISIT_FEE', SMALLMONEY),
    Column('PASSOVER_UNIT_RATE', SMALLMONEY),
    Column('PASSOVER_UNIT_BASE', String(20)),
    Column('PRIVATE_LABEL_TYPE', String(20)),
    Column('PRIVATE_LABEL_FEE1', SMALLMONEY),
    Column('PRIVATE_LABEL_BASE1', Integer),
    Column('PRIVATE_LABEL_FEE2', SMALLMONEY),
    Column('PRIVATE_LABEL_BASE2', Integer),
    Column('PRIVATE_LABEL_FEE3', SMALLMONEY),
    Column('PRIVATE_LABEL_BASE3', Integer),
    Column('SPECIAL_PRODUCTION_FEE1', SMALLMONEY),
    Column('UNIT_BASE1', Integer),
    Column('SPECIAL_PRODUCTION_FEE2', SMALLMONEY),
    Column('UNIT_BASE2', Integer),
    Column('VISIT_FEE1', MONEY),
    Column('FREE_VISITS_NUM1', Integer),
    Column('VISIT_FEE2', MONEY),
    Column('FREE_VISITS_NUM2', Integer),
    Column('CERT_FREQ', String(20)),
    Column('CERT_DATE', DateTime),
    Column('PASSOVER_RATE_FEE1', SMALLMONEY),
    Column('PASSOVER_FOR_FEE1', Integer),
    Column('PASSOVER_RATE_FEE2', SMALLMONEY),
    Column('PASSOVER_FOR_FEE2', Integer),
    Column('PASSOVER_RATE_FEE3', SMALLMONEY),
    Column('PASSOVER_FOR_FEE3', Integer),
    Column('BILL_REG_VISIT_TYPEx', String(20)),
    Column('BILL_REG_VISIT_AMTx', String(20)),
    Column('BILL_SPEC_PROD_TYPEx', String(20)),
    Column('BILL_SPEC_PROD_AMTx', String(20)),
    Column('BILL_PASSOVER_TYPEx', String(20)),
    Column('BILL_PASSOVER_AMTx', String(20)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('LockPerDistributorRate', Boolean, nullable=False),
    Column('PRIVATE_LABEL_COMMENT', String(500)),
    Index('COMPANY_FEE_STRUCTURE_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_COMPANY_HOLD_TB_history_temporal = Table(
    'COMPANY_HOLD_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('COMPANY_SEQ_NUM', SmallInteger, nullable=False),
    Column('HOLD_TYPE', String(4)),
    Column('START_PERSON_ID', String(20), nullable=False),
    Column('START_DATE', DateTime),
    Column('START_REASON', String(100), nullable=False),
    Column('END_PERSON_ID', String(20)),
    Column('END_DATE', DateTime),
    Column('END_REASON', String(100)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('XAKCOMPANY_HOLD_1', 'COMPANY_ID', 'ID'),
    Index('COMPANY_HOLD_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_COMPANY_STATUS_TB_history_temporal = Table(
    'COMPANY_STATUS_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer),
    Column('ROLE', String(1)),
    Column('STATUS', String(40)),
    Column('ACTIVE_FLAG', Boolean),
    Column('START_DATE', DateTime),
    Column('START_PERSON_ID', String(20)),
    Column('START_REASON', String(100)),
    Column('END_DATE', DateTime),
    Column('END_PERSON_ID', String(20)),
    Column('END_REASON', String(100)),
    Column('ACTIVE', Integer),
    Column('DateDone', DateTime),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('COMPANY_STATUS_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_COMPANY_TB_history_temporal = Table(
    'COMPANY_TB_history_temporal', metadata,
    Column('COMPANY_ID', Integer, nullable=False, index=True),
    Column('NAME', String(120), nullable=False),
    Column('LIST', String(1)),
    Column('GP_NOTIFY', TINYINT),
    Column('PRODUCER', Boolean),
    Column('MARKETER', Boolean),
    Column('SOURCE', Boolean),
    Column('IN_HOUSE', String(1)),
    Column('PRIVATE_LABEL', String(1)),
    Column('COPACKER', String(1)),
    Column('JEWISH_OWNED', String(1)),
    Column('CORPORATE', String(1)),
    Column('COMPANY_TYPE', String(30)),
    Column('INVOICE_TYPE', String(20)),
    Column('INVOICE_FREQUENCY', String(20)),
    Column('INVOICE_DTL', String(20)),
    Column('TIMESTAMP', BINARY(8)),
    Column('STATUS', String(40)),
    Column('RC', String(255)),
    Column('PARENT_CO', String(80)),
    Column('INVOICE_LAST_DATE', DateTime),
    Column('COMPANY_BILL_TO_NAME', String(255)),
    Column('ACTIVE', Integer),
    Column('AcquiredFrom', String(50)),
    Column('UID', String(50)),
    Column('MoveToGP', String(1)),
    Column('DefaultPO', String(75)),
    Column('POexpiry', Date),
    Column('PrivateLabelPO', String(50)),
    Column('PrivateLabelPOexpiry', Date),
    Column('VisitPO', String(75)),
    Column('VisitPOexpiry', Date),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('CATEGORY', String(50)),
    Column('OLDCOMPANYTYPE', String(50)),
    Column('BoilerplateInvoiceComment', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('IsPoRequired', Boolean, nullable=False),
    Column('ShouldPropagateCompanyPo', Boolean, nullable=False),
    Column('ShouldPropagateKscPoToPlants', Boolean, nullable=False),
    Column('ShouldPropagateVisitPoToPlants', Boolean, nullable=False),
    Column('PoReason', String(2000)),
    Column('On3rdPartyBilling', Boolean, nullable=False),
    Column('IsTest', Boolean, nullable=False),
    Column('ChometzEmailSentDate', DateTime),
    Index('COMPANY_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_CO_PRIVATE_LABEL_FEE_DETAIL_history_temporal = Table(
    'CO_PRIVATE_LABEL_FEE_DETAIL_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('COMPANY_FEE_ID', Integer, nullable=False),
    Column('PL_DETAIL_SEQ_NUM', SmallInteger, nullable=False),
    Column('PL_DETAIL_DESCRIPTION', String(80)),
    Column('PL_DETAIL_AMOUNT', MONEY),
    Column('PL_DETAIL_DATE', DateTime),
    Column('PL_DETAIL_PERSON_ID', String(20), nullable=False),
    Column('PL_DETAIL_COMMENT', String(255)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('CO_PRIVATE_LABEL_FEE_DETAIL_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_CoPackerFacilitiesCategory_history_temporal = Table(
    'CoPackerFacilitiesCategory_history_temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('CoPackerId', Integer, nullable=False),
    Column('Category', String(500), nullable=False),
    Column('CategoryParent', String(500)),
    Column('CategoryChild', String(500)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Index('ix_CoPackerFacilitiesCategory_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_CoPackerFacilitiesLocation_history_temporal = Table(
    'CoPackerFacilitiesLocation_history_temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('CoPackerId', Integer, nullable=False),
    Column('Location', String(500), nullable=False),
    Column('LocationCity', String(200)),
    Column('LocationState', String(200)),
    Column('LocationProvince', String(200)),
    Column('LocationCountry', String(200)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Index('ix_CoPackerFacilitiesLocation_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_CoPackerFacilities_history_temporal = Table(
    'CoPackerFacilities_history_temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('CompanyId', Integer, nullable=False),
    Column('WebsiteURL', String(500)),
    Column('Description', String(500)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Index('ix_CoPackerFacilities_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_CompanyContacts = Table(
    'CompanyContacts', metadata,
    Column('ccID', Integer, nullable=False),
    Column('companytitle', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Company_ID', Integer),
    Column('Title', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FirstName', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LastName', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Voice', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fax', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMail', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cell', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PrimaryCT', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('BillingCT', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('WebCT', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('OtherCT', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EnteredBy', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DateEntered', SMALLDATETIME),
    Column('ModifiedBy', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DateModified', DateTime),
    Column('Active', SmallInteger),
    Column('OtherInfo', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('StatementType', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('InvoiceType', String(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('LOAtype', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EIREmail', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ScheduleBEmail', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FormulaEmail', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UserVendorID', String(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UsedInComment', String(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ContactID', Integer, nullable=False)
)


t_CompanyContactsAndAddresses = Table(
    'CompanyContactsAndAddresses', metadata,
    Column('Company', String(120, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Industry', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Status', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RC', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CompanyTitle', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Title', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FirstName', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LastName', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Voice', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fax', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Email', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ContactType', String(23, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Street1', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Street2', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('City', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('State', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Zip', String(18, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_CompanyPlantOptions_history_temporal = Table(
    'CompanyPlantOptions_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('Company_ID', Integer),
    Column('Plant_id', Integer),
    Column('OwnsID', Integer),
    Column('OptionName', String(75)),
    Column('OptionValue', String(75)),
    Column('OptIn', String(1)),
    Column('rcApproved', String(1)),
    Column('glApproved', String(1)),
    Column('ModifiedBy', String(250)),
    Column('ModifiedDate', DateTime),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('CompanyPlantOptions_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_FormulaComponents_history_temporal = Table(
    'FormulaComponents_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('FormulaID', Integer, nullable=False),
    Column('ComponentMerchID', Integer),
    Column('ComponentLabelID', Integer),
    Column('Component', String(50), nullable=False),
    Column('ComponentIDType', String(50), nullable=False),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('FormulaComponents_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_INVOICE_FEES_DETAIL_history_temporal = Table(
    'INVOICE_FEES_DETAIL_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('INVOICE_ID', Integer, nullable=False),
    Column('INVOICE_LINE', Integer, nullable=False),
    Column('VISIT_ID', Integer),
    Column('DESTINATION_TYPE', String(1)),
    Column('DESTINATION_ID', Integer),
    Column('FEE', MONEY),
    Column('EXPENSES', MONEY),
    Column('VISIT_TYPE', String(100)),
    Column('VISIT_DATE', DateTime),
    Column('VISIT_PERSON_JOB_ID', Integer),
    Column('PERIOD_START_DATE', DateTime),
    Column('PERIOD_END_DATE', DateTime),
    Column('REASON', String(50)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ownsID', Integer),
    Column('voided', Boolean, nullable=False),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('INVOICE_FEES_DETAIL_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_INVOICE_FEES_DYN_ = Table(
    'INVOICE_FEES_DYN_', metadata,
    Column('INVOICE_ID', String(15), nullable=False),
    Column('COMPANY_ID', String(15)),
    Column('TYPE', String(4), nullable=False),
    Column('INVOICE_DATE', String(12)),
    Column('TOTAL_AMOUNT', String(15)),
    Column('BILL_TO_CO_ID', String(15)),
    Column('BILL_TO_PLANT_ID', String(15)),
    Column('REPLACEMENT_FOR', String(15)),
    Column('BATCH_ID', String(15)),
    Column('ID', String(15))
)


t_INVOICE_FEES_history_temporal = Table(
    'INVOICE_FEES_history_temporal', metadata,
    Column('INVOICE_ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('TYPE', String(4), nullable=False),
    Column('INVOICE_TYPE', String(20)),
    Column('INVOICE_DATE', DateTime),
    Column('FREQ', String(20)),
    Column('TOTAL_AMOUNT', MONEY),
    Column('DATE_POSTED', DateTime),
    Column('STATUS', String(20)),
    Column('REPLACED_BY', Integer),
    Column('PAYMENT', MONEY),
    Column('CHECK_NO', String(255)),
    Column('CHECK_DATE', DateTime),
    Column('CHECK_RECEIVED', DateTime),
    Column('BILL_TO_CO_ID', Integer),
    Column('BILL_TO_PLANT_ID', Integer),
    Column('OK_TO_POST', String(1)),
    Column('WHO', String(40)),
    Column('REPLACEMENT_FOR', Integer),
    Column('BATCH_ID_S36', String(7)),
    Column('BATCH_DATE', DateTime),
    Column('TRANSFER_FLAG', String(1)),
    Column('PRINT_FLAG', String(1)),
    Column('HOLD_FLAG', String(1)),
    Column('ATTACHED_LETTER', String(20)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ID', Integer),
    Column('COMMENT', String(255)),
    Column('INVOICE_LEVEL', Integer),
    Column('PurchaseOrder', String(75)),
    Column('DeliveryMethod', String(30)),
    Column('DeliveryDate', Date),
    Column('OriginalInvoiceAmount', MONEY),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('achPaid', Boolean, nullable=False),
    Column('BatchId', Integer),
    Column('PeriodStart', DateTime),
    Column('PeriodEnd', DateTime),
    Column('BalanceInAccounting', DECIMAL(18, 2)),
    Index('INVOICE_FEES_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_LabelComment_History_Temporal = Table(
    'LabelComment_History_Temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('CommentID', Integer, nullable=False, index=True),
    Column('LabelId', Integer, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Index('ix_LabelComment_History_Temporal', 'ValidFromTime', 'ValidToTime')
)


t_MERCH_COMMENT_history_temporal = Table(
    'MERCH_COMMENT_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('MERCHANDISE_ID', Integer, nullable=False),
    Column('COMMENT_ID', Integer, nullable=False),
    Column('TIMESTAMP', BINARY(8)),
    Column('CommentType', String(20)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('MERCH_COMMENT_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_MERCH_TB_history_temporal = Table(
    'MERCH_TB_history_temporal', metadata,
    Column('MERCHANDISE_ID', Integer, nullable=False, index=True),
    Column('NAME', String(225), nullable=False),
    Column('AS_STIPULATED', String(1)),
    Column('STIPULATION', String(1000)),
    Column('CONFIDENTIAL', String(1)),
    Column('RETAIL', String(1)),
    Column('FOODSERVICE', String(1)),
    Column('CONSUMER', String(1)),
    Column('INDUSTRIAL', String(1)),
    Column('INSTITUTIONAL', String(1)),
    Column('OUP_REQUIRED', String(2)),
    Column('GENERIC', String(1)),
    Column('SPECIFIED_SOURCE', String(1)),
    Column('SPECIFIED_SYMBOL', String(1)),
    Column('DESCRIPTION', String(80)),
    Column('DPM', String(20)),
    Column('PESACH', String(1)),
    Column('COMMENT', String(250)),
    Column('ACTIVE', Integer),
    Column('CONFIDENTIAL_TEXT', String(500)),
    Column('GROUP_COMMENT', String(100)),
    Column('STATUS', String(25)),
    Column('LOC_CATEGORY', String(80)),
    Column('LOC_SELECTED', String(80)),
    Column('COMMENTS_SCHED_B', String(250)),
    Column('PROD_NUM', String(25)),
    Column('INTERMEDIATE_MIX', String(1)),
    Column('ALTERNATE_NAME', String(80)),
    Column('BrochoCode', SmallInteger),
    Column('Brocho2Code', SmallInteger),
    Column('CAS', String(30)),
    Column('Symbol', String(50)),
    Column('LOC', Date),
    Column('UKDdisplay', String(1)),
    Column('Reviewed', Boolean),
    Column('TransferredTo', Boolean, nullable=False),
    Column('TransferredMerch', Integer),
    Column('Special_Status', String(255)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('idx_NCI_status_dpm', 'STATUS', 'DPM'),
    Index('idx_NCI_id_status_dpm', 'MERCHANDISE_ID', 'STATUS', 'DPM'),
    Index('MERCH_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime'),
    Index('idx_NCI_status_time', 'STATUS', 'ValidToTime')
)


t_MiniCRMActions_history_temporal = Table(
    'MiniCRMActions_history_temporal', metadata,
    Column('ID', Integer, nullable=False),
    Column('CreatedDate', DateTime, nullable=False),
    Column('CreatedBy', Integer),
    Column('ModifiedDate', DateTime),
    Column('ModifiedBy', Integer),
    Column('ActivityDate', DateTime),
    Column('Modality', String(250)),
    Column('ContactId', Integer, nullable=False),
    Column('CompanyId', Integer, nullable=False),
    Column('Result', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ReminderDate', DateTime),
    Column('Comment', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Index('ix_MiniCRMActions_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_OWNS_TB_history_temporal = Table(
    'OWNS_TB_history_temporal', metadata,
    Column('COMPANY_ID', Integer, nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('TYPE', String(10)),
    Column('VISIT_FREQUENCY', SmallInteger),
    Column('INVOICE_TYPE', String(20)),
    Column('INVOICE_FREQUENCY', String(20)),
    Column('INVOICE_DTL', String(20)),
    Column('HOLD', String(1)),
    Column('ROYALTIES', String(1)),
    Column('SPECIAL_TICKET', String(1)),
    Column('STATUS', String(40)),
    Column('ID', Integer, nullable=False, index=True),
    Column('ACTIVE', Integer),
    Column('Setup_By', Integer),
    Column('AcquiredFrom', String(50)),
    Column('NoRFRneeded', String(1), nullable=False),
    Column('LOCtext', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('MoveToGP', String(1)),
    Column('DefaultPO', String(75)),
    Column('VisitBilling', String(10)),
    Column('PlantName', String(100)),
    Column('ShareAB', String(1)),
    Column('POexpiry', Date),
    Column('BillingName', String(100)),
    Column('PLANT_BILL_TO_NAME', String(80)),
    Column('AutoCertification', Boolean, nullable=False),
    Column('primaryCompany', Integer),
    Column('Override', Boolean, nullable=False),
    Column('VisitPO', String(75)),
    Column('VisitPOexpiry', Date),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('BoilerplateInvoiceComment', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('IsCertBillingOverride', Boolean, nullable=False),
    Index('OWNS_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PENDING_INFO_TB_history_temporal = Table(
    'PENDING_INFO_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('IINVOICEFEE', String(25)),
    Column('IINVOICEEXPENSE', String(25)),
    Column('IINVOICEDATE', String(10)),
    Column('IINVOICENUMBER', String(25)),
    Column('VOID', String(1)),
    Column('PAID', String(1)),
    Column('TERMSCERTFEE', String(25)),
    Column('SPECIALCLAUSES', String(255)),
    Column('ANNUALFEE', String(25)),
    Column('ANNUALEXPENSES', String(25)),
    Column('CINVOICEDATE', String(10)),
    Column('COMPANY_ID', Integer),
    Column('PLANT_ID', Integer),
    Column('ACTIVE', Integer),
    Column('IINVOICEAMOUNT', String(25)),
    Column('PROEXPENSES', String(25)),
    Column('PROFEE', String(25)),
    Column('PRODATE', String(10)),
    Column('CONTRACTFEE', String(25)),
    Column('CONTRACTEXPENSE', String(25)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PENDING_INFO_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PERSON_ADDRESS_TB_history_temporal = Table(
    'PERSON_ADDRESS_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('PERSON_ID', Integer, nullable=False),
    Column('ADDRESS_SEQ_NUM', Integer, nullable=False),
    Column('TYPE', String(20)),
    Column('ATTN', String(40)),
    Column('STREET1', String(40)),
    Column('STREET2', String(40)),
    Column('STREET3', String(40)),
    Column('CITY', String(40)),
    Column('STATE', String(25)),
    Column('ZIP', String(15)),
    Column('COUNTRY', String(25)),
    Column('ACTIVE', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PERSON_ADDRESS_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


class PERSONJOBSTATUSTB(Base):  # type: ignore
    __tablename__ = 'PERSON_JOB_STATUS_TB'
    _s_collection_name = 'PERSONJOBSTATUSTB'  # type: ignore
    __table_args__ = (
        Index('XPKPERSON_JOB_STATUS', 'PERSON_JOB_ID', 'STATUS_SEQ_NUM', unique=True),
    )

    ID = Column(Integer, primary_key=True)
    PERSON_JOB_ID = Column(Integer, nullable=False)
    STATUS_SEQ_NUM = Column(SmallInteger, nullable=False)
    STATUS = Column(String(20), nullable=False)
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    ACTIVE = Column(Integer)
    REASON = Column(String(100))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



class PERSONJOBTB(Base):  # type: ignore
    __tablename__ = 'PERSON_JOB_TB'
    _s_collection_name = 'PERSONJOBTB'  # type: ignore
    __table_args__ = (
        Index('personid', 'PERSON_ID', 'PERSON_JOB_ID'),
        Index('PRSNJOB1', 'PERSON_JOB_ID', 'PERSON_ID', unique=True)
    )

    PERSON_JOB_ID = Column(Integer, server_default=text("0"), primary_key=True)
    PERSON_ID = Column(ForeignKey('PERSON_TB.PERSON_ID'), nullable=False)
    FUNCTION = Column(String(40), nullable=False)
    EMPLOYER_ID = Column(Integer)
    TITLE = Column(String(40))
    ON_PAYROLL = Column(String(1))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    STATUS = Column(String(40))
    ACCT_PAYROLL_NUM = Column(String(20))
    OUDirectRFRTerminationHold = Column(String(1), server_default=text("('')"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    TeamId = Column(Integer, index=True)
    StatusEffectiveStartDate = Column(DateTime)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    PERSON_TB : Mapped["PERSONTB"] = relationship(foreign_keys='[PERSONJOBTB.PERSON_ID]', back_populates=("PERSONJOBTBList"))

    # child relationships (access children)
    PERSONTBList : Mapped[List["PERSONTB"]] = relationship(foreign_keys='[PERSONTB.AdministrativeAssistant]', back_populates="PERSON_JOB_TB")
    PLANTTBList : Mapped[List["PLANTTB"]] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates="PERSON_JOB_TB")
    PLANTTBList1 : Mapped[List["PLANTTB"]] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates="PERSON_JOB_TB1", overlaps="PLANTTBList")
    RCTBList : Mapped[List["RCTB"]] = relationship(back_populates="PERSON_JOB_TB")
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="PERSON_JOB_TB")
    VISITList : Mapped[List["VISIT"]] = relationship(foreign_keys='[VISIT.ACTUAL_PERSON_JOB_ID]', back_populates="PERSON_JOB_TB")
    VISITList1 : Mapped[List["VISIT"]] = relationship(foreign_keys='[VISIT.ASSIGNED_PERSON_JOB_ID]', back_populates="PERSON_JOB_TB1")
    ProductJobLineItemList : Mapped[List["ProductJobLineItem"]] = relationship(back_populates="PERSON_JOB_TB")



t_PERSON_JOB_TB_history_temporal = Table(
    'PERSON_JOB_TB_history_temporal', metadata,
    Column('PERSON_JOB_ID', Integer, nullable=False, index=True),
    Column('PERSON_ID', Integer, nullable=False),
    Column('function', String(40), nullable=False),
    Column('EMPLOYER_ID', Integer),
    Column('TITLE', String(40)),
    Column('ON_PAYROLL', String(1)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('STATUS', String(40)),
    Column('ACCT_PAYROLL_NUM', String(20)),
    Column('OUDirectRFRTerminationHold', String(1)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('TeamId', Integer),
    Column('StatusEffectiveStartDate', DateTime),
    Index('PERSON_JOB_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


class PERSONTB(Base):  # type: ignore
    __tablename__ = 'PERSON_TB'
    _s_collection_name = 'PERSONTB'  # type: ignore
    __table_args__ = (
        Index('ix_PERSON_TB_ACTIVE_KashLogIn', 'ACTIVE', 'KashLogIn'),
    )

    PERSON_ID = Column(Integer, server_default=text("0"), primary_key=True)
    FIRST = Column(String(100))
    LAST = Column(String(100))
    MIDDLE = Column(String(50), server_default=text("('')"))
    PREFIX = Column(String(50), server_default=text("('')"))
    VENDOR_ID = Column(Integer)
    SUFFIX = Column(String(12))
    HIRE_DATE = Column(DateTime)
    SSN = Column(String(11))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    SENDTICKETTO = Column(String(255), server_default=text("('')"))
    ACCTS_PAY_NUM = Column(String(30))
    MaxPay = Column(SMALLMONEY, server_default=text("((500))"))
    MileageRate = Column(SMALLMONEY)
    WebAccess = Column(String(5))
    GroupLeader = Column(String(40), index=True)
    AdministrativeAssistant = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    KashLogIn = Column(String(75))
    IsGroupLeader = Column(String(1))
    HiddenSSN = Column(String(50), server_default=text("((0))"))
    WorkflowEmails = Column(String(1))
    Password = Column(String(30))
    PasswordQuestion = Column(String(500))
    PasswordAnswer = Column(String(500))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    IncludeInIngWFAssignmentList = Column(Boolean)
    TempRfr = Column(Boolean, server_default=text("((0))"), nullable=False)
    IsBillForMileageDifferential = Column(Boolean, server_default=text("((0))"), nullable=False)
    AllowCopackerManagement = Column(Boolean, server_default=text("((0))"))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PERSONTB.AdministrativeAssistant]', back_populates=("PERSONTBList"))

    # child relationships (access children)
    PERSONJOBTBList : Mapped[List["PERSONJOBTB"]] = relationship(foreign_keys='[PERSONJOBTB.PERSON_ID]', back_populates="PERSON_TB")
    PERSONADDRESSTBList : Mapped[List["PERSONADDRESSTB"]] = relationship(back_populates="PERSON_TB")



t_PERSON_TB_history_temporal = Table(
    'PERSON_TB_history_temporal', metadata,
    Column('PERSON_ID', Integer, nullable=False, index=True),
    Column('FIRST', String(100)),
    Column('LAST', String(100)),
    Column('MIDDLE', String(50)),
    Column('PREFIX', String(50)),
    Column('VENDOR_ID', Integer),
    Column('SUFFIX', String(12)),
    Column('HIRE_DATE', DateTime),
    Column('SSN', String(11)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('SENDTICKETTO', String(255)),
    Column('ACCTS_PAY_NUM', String(30)),
    Column('MaxPay', SMALLMONEY),
    Column('MileageRate', SMALLMONEY),
    Column('WebAccess', String(5)),
    Column('GroupLeader', String(40)),
    Column('AdministrativeAssistant', Integer),
    Column('KashLogIn', String(75)),
    Column('IsGroupLeader', String(1)),
    Column('HiddenSSN', String(50)),
    Column('WorkflowEmails', String(1)),
    Column('Password', String(30)),
    Column('PasswordQuestion', String(500)),
    Column('PasswordAnswer', String(500)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('IncludeInIngWFAssignmentList', Boolean),
    Column('TempRfr', Boolean, nullable=False),
    Column('IsBillForMileageDifferential', Boolean, nullable=False),
    Column('AllowCopackerManagement', Boolean),
    Index('PERSON_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PLANT = Table(
    'PLANT', metadata,
    Column('PLANT_ID', Integer, nullable=False),
    Column('NAME', String(80, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GP_NOTIFY', Boolean),
    Column('MULTILINES', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PASSOVER', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SPECIAL_PROD', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('JEWISH_OWNED', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PLANT_TYPE', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PLANT_DIRECTIONS', String(800, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('USDA_CODE', String(15, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PlantUID', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DoNotAttach', String(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OtherCertification', String(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PrimaryCompany', Integer),
    Column('DesignatedRFR', Integer)
)


t_PLANT_ADDRESS = Table(
    'PLANT_ADDRESS', metadata,
    Column('ID', Integer, server_default=text("0"), nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('ADDRESS_SEQ_NUM', Integer, nullable=False),
    Column('TYPE', String(40, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ATTN', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET1', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET2', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STREET3', String(60, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CITY', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STATE', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ZIP', String(15, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('COUNTRY', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TIMESTAMP', BINARY(8)),
    Column('COMPANY_ID', Integer)
)


t_PLANT_ADDRESS_TB_history_temporal = Table(
    'PLANT_ADDRESS_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('PLANT_ID', Integer, nullable=False),
    Column('ADDRESS_SEQ_NUM', Integer, nullable=False),
    Column('TYPE', String(40), nullable=False),
    Column('ATTN', String(40)),
    Column('STREET1', String(60)),
    Column('STREET2', String(60)),
    Column('STREET3', String(60)),
    Column('CITY', String(40)),
    Column('STATE', String(25)),
    Column('ZIP', String(25)),
    Column('COUNTRY', String(25)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('COMPANY_ID', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PLANT_ADDRESS_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PLANT_FEE_STRUCTURE_OUT_history_temporal = Table(
    'PLANT_FEE_STRUCTURE_OUT_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('PLANT_ID', Integer),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('PERSON_JOB_ID', Integer),
    Column('OUT_VISIT_FEE_TYPEx', String(20)),
    Column('OUT_VISIT_FEEx', MONEY),
    Column('OUT_FREE_VISITS_NUM', Integer),
    Column('OUT_VISIT_FEE1', MONEY),
    Column('OUT_FREE_VISITS_NUM1', Integer),
    Column('OUT_VISIT_FEE2', MONEY),
    Column('OUT_FREE_VISITS_NUM2', Integer),
    Column('OUT_FREE_VISITS_OVERNIGHTPAY', MONEY),
    Column('OUT_SPECIAL_PRODUCTION_TYPEx', String(20)),
    Column('OUT_SPECIAL_PRODUCTION_FEEx', SMALLMONEY),
    Column('OUT_UNIT_BASE', Integer),
    Column('OUT_SPECIAL_PRODUCTION_FEE1', SMALLMONEY),
    Column('OUT_UNIT_BASE1', Integer),
    Column('OUT_SPECIAL_PRODUCTION_FEE2', SMALLMONEY),
    Column('OUT_UNIT_BASE2', Integer),
    Column('OUT_SPEC_PRODN_OVERNIGHTPAY', MONEY),
    Column('OUT_PASSOVER_FEE_TYPEx', String(25)),
    Column('OUT_PASSOVER_RATE_FEE1x', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE1', Integer),
    Column('OUT_PASSOVER_RATE_FEE2', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE2', Integer),
    Column('OUT_PASSOVER_RATE_FEE3', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE3', Integer),
    Column('OUT_PASSOVER_OVERNIGHTPAY', MONEY),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PLANT_FEE_STRUCTURE_OUT_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PLANT_FEE_STRUCTURE_history_temporal = Table(
    'PLANT_FEE_STRUCTURE_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('PLANT_ID', Integer),
    Column('COMPANY_ID', Integer),
    Column('COMPANY_FEE_ID', SmallInteger),
    Column('EFFECTIVE_DATE', DateTime),
    Column('APPROVAL', String(1)),
    Column('APPROVAL_DATE', DateTime),
    Column('APPROVAL_PERSON_ID', Integer),
    Column('IN_CERT_FEE', MONEY),
    Column('IN_EXPENSE_TYPE', String(15)),
    Column('IN_EXPENSE_AMT', MONEY),
    Column('IN_EXPENSE_PERCENT', Float(53)),
    Column('IN_VISIT_FEE_TYPEx', String(20)),
    Column('IN_FREE_VISITS_NUM', Integer),
    Column('IN_VISIT_FEEx', MONEY),
    Column('IN_SPECIAL_PRODUCTION_TYPEx', String(20)),
    Column('IN_SPECIAL_PRODUCTION_FEEx', SMALLMONEY),
    Column('IN_UNIT_BASE', Integer),
    Column('IN_PASSOVER_FEE_TYPEx', String(25)),
    Column('IN_PASSOVER_FEEx', SMALLMONEY),
    Column('IN_PASSOVER_VISIT_FEE', SMALLMONEY),
    Column('IN_PASSOVER_UNIT_RATE', SMALLMONEY),
    Column('IN_PASSOVER_UNIT_BASE', String(20)),
    Column('IN_PRIVATE_LABEL_TYPE', String(20)),
    Column('IN_PRIVATE_LABEL_FEE1', SMALLMONEY),
    Column('IN_PRIVATE_LABEL_BASE1', Integer),
    Column('IN_PRIVATE_LABEL_FEE2', SMALLMONEY),
    Column('IN_PRIVATE_LABEL_BASE2', Integer),
    Column('IN_PRIVATE_LABEL_FEE3', SMALLMONEY),
    Column('IN_PRIVATE_LABEL_BASE3', Integer),
    Column('IN_SPECIAL_PRODUCTION_FEE1', SMALLMONEY),
    Column('IN_UNIT_BASE1', Integer),
    Column('IN_SPECIAL_PRODUCTION_FEE2', SMALLMONEY),
    Column('IN_UNIT_BASE2', Integer),
    Column('IN_VISIT_FEE1', MONEY),
    Column('IN_FREE_VISITS_NUM1', Integer),
    Column('IN_VISIT_FEE2', MONEY),
    Column('IN_FREE_VISITS_NUM2', Integer),
    Column('IN_CERT_FREQ', String(20)),
    Column('IN_CERT_DATE', DateTime),
    Column('IN_PASSOVER_RATE_FEE1', SMALLMONEY),
    Column('IN_PASSOVER_FOR_FEE1', Integer),
    Column('IN_PASSOVER_RATE_FEE2', SMALLMONEY),
    Column('IN_PASSOVER_FOR_FEE2', Integer),
    Column('IN_PASSOVER_RATE_FEE3', SMALLMONEY),
    Column('IN_PASSOVER_FOR_FEE3', Integer),
    Column('IN_BILL_REG_VISIT_TYPEx', String(20)),
    Column('IN_BILL_REG_VISIT_AMTx', String(20)),
    Column('IN_BILL_SPEC_PROD_TYPEx', String(20)),
    Column('IN_BILL_SPEC_PROD_AMTx', String(20)),
    Column('IN_BILL_PASSOVER_TYPEx', String(20)),
    Column('IN_BILL_PASSOVER_AMTx', String(20)),
    Column('OUT_CERT_FEE', MONEY),
    Column('OUT_EXPENSE_TYPE', String(15)),
    Column('OUT_EXPENSE_AMT', MONEY),
    Column('OUT_EXPENSE_PERCENT', Float(53)),
    Column('OUT_VISIT_FEE_TYPE', String(20)),
    Column('OUT_FREE_VISITS_NUM', Integer),
    Column('OUT_VISIT_FEE', MONEY),
    Column('OUT_SPECIAL_PRODUCTION_TYPE', String(20)),
    Column('OUT_SPECIAL_PRODUCTION_FEE', SMALLMONEY),
    Column('OUT_UNIT_BASE', Integer),
    Column('OUT_PASSOVER_FEE_TYPE', String(25)),
    Column('OUT_PASSOVER_FEE', SMALLMONEY),
    Column('OUT_PASSOVER_VISIT_FEE', SMALLMONEY),
    Column('OUT_PASSOVER_UNIT_RATE', SMALLMONEY),
    Column('OUT_PASSOVER_UNIT_BASE', String(20)),
    Column('OUT_PRIVATE_LABEL_TYPE', String(20)),
    Column('OUT_PRIVATE_LABEL_FEE1', SMALLMONEY),
    Column('OUT_PRIVATE_LABEL_BASE1', Integer),
    Column('OUT_PRIVATE_LABEL_FEE2', SMALLMONEY),
    Column('OUT_PRIVATE_LABEL_BASE2', Integer),
    Column('OUT_PRIVATE_LABEL_FEE3', SMALLMONEY),
    Column('OUT_PRIVATE_LABEL_BASE3', Integer),
    Column('OUT_SPECIAL_PRODUCTION_FEE1', SMALLMONEY),
    Column('OUT_UNIT_BASE1', Integer),
    Column('OUT_SPECIAL_PRODUCTION_FEE2', SMALLMONEY),
    Column('OUT_UNIT_BASE2', Integer),
    Column('OUT_VISIT_FEE1', MONEY),
    Column('OUT_FREE_VISITS_NUM1', Integer),
    Column('OUT_VISIT_FEE2', MONEY),
    Column('OUT_FREE_VISITS_NUM2', Integer),
    Column('OUT_CERT_FREQ', String(20)),
    Column('OUT_CERT_DATE', DateTime),
    Column('OUT_PASSOVER_RATE_FEE1', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE1', Integer),
    Column('OUT_PASSOVER_RATE_FEE2', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE2', Integer),
    Column('OUT_PASSOVER_RATE_FEE3', SMALLMONEY),
    Column('OUT_PASSOVER_FOR_FEE3', Integer),
    Column('OUT_BILL_REG_VISIT_TYPE', String(20)),
    Column('OUT_BILL_REG_VISIT_AMT', String(20)),
    Column('OUT_BILL_SPEC_PROD_TYPE', String(20)),
    Column('OUT_BILL_SPEC_PROD_AMT', String(20)),
    Column('OUT_BILL_PASSOVER_TYPE', String(20)),
    Column('OUT_BILL_PASSOVER_AMT', String(20)),
    Column('OUT_FREE_VISITS_OVERNIGHTPAY', MONEY),
    Column('OUT_SPECIAL_PRODN_OVERNIGHTPAY', MONEY),
    Column('OUT_PASSOVER_RATE_OVERNIGHTPAY', MONEY),
    Column('PERSON_JOB_ID', Integer),
    Column('OwnsID', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PLANT_FEE_STRUCTURE_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PLANT_HOLD_TB_history_temporal = Table(
    'PLANT_HOLD_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('HOLD_SEQ_NUM', SmallInteger, nullable=False),
    Column('HOLD_TYPE', String(4), nullable=False),
    Column('START_PERSON_ID', String(30), nullable=False),
    Column('START_DATE', DateTime),
    Column('START_REASON', String(100)),
    Column('END_PERSON_ID', String(30)),
    Column('END_DATE', DateTime),
    Column('END_REASON', String(100)),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('OwnsID', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('PLANT_HOLD_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime'),
    Index('idx_Comp_Plant', 'COMPANY_ID', 'PLANT_ID')
)


t_PLANT_TB_history_temporal = Table(
    'PLANT_TB_history_temporal', metadata,
    Column('PLANT_ID', Integer, nullable=False, index=True),
    Column('NAME', String(80), nullable=False),
    Column('GP_NOTIFY', Boolean),
    Column('MULTILINES', String(1)),
    Column('PASSOVER', String(1)),
    Column('SPECIAL_PROD', String(1), nullable=False),
    Column('JEWISH_OWNED', String(1)),
    Column('PLANT_TYPE', String(50)),
    Column('PLANT_DIRECTIONS', String(800)),
    Column('ACTIVE', Integer),
    Column('USDA_CODE', String(15)),
    Column('PlantUID', String(75)),
    Column('DoNotAttach', String(1)),
    Column('OtherCertification', String(500)),
    Column('PrimaryCompany', Integer),
    Column('DesignatedRFR', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('MaxOnSiteVisits', SmallInteger, nullable=False),
    Column('MaxVirtualVisits', SmallInteger, nullable=False),
    Column('IsDaily', Boolean, nullable=False),
    Index('PLANT_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PRIVATE_LABEL_BILL_history_temporal = Table(
    'PRIVATE_LABEL_BILL_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('SRC_MAR_ID', Integer, nullable=False),
    Column('MAN_ENTERED', Boolean, nullable=False),
    Column('DATE_UPDATE', DateTime),
    Column('PRIV_LABEL_FEE', MONEY),
    Column('BILL_TO_CO_ID', Integer),
    Column('BILL_TO_PLANT_ID', Integer),
    Column('PRO_RATED', MONEY),
    Column('TIMESTAMP', BINARY(8)),
    Column('LAST_BIILED', DateTime),
    Column('AGREEMENT_RECEIVED_DATE', DateTime),
    Column('CHANGESET_ID', Integer, index=True),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Index('PRIVATE_LABEL_BILL_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_ProductJobLineItems_history_temporal = Table(
    'ProductJobLineItems_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('JobID', String(50)),
    Column('LineItem', Integer),
    Column('RequestedLabelName', Unicode(225)),
    Column('RequestedBrand', Unicode(100)),
    Column('RequestedLabelNumber', Unicode(25)),
    Column('WorkflowStatus', String(50)),
    Column('LineItemComment', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('prid', Integer),
    Column('AssignedTo', Integer),
    Column('ownsID', Integer),
    Column('requestedProductNumber', String(50)),
    Column('requestedProductName', String(1000)),
    Column('requestedSymbol', String(20)),
    Column('requestedDPM', String(20)),
    Column('requestedGRP', String(20)),
    Column('requestedConsumer', String(2)),
    Column('requestedIndustrial', String(2)),
    Column('requestedPesach', String(2)),
    Column('requestedSealSign', String(100)),
    Column('requestedStipulation', String(1000)),
    Column('requestedCommentsScheduleB', String(1000)),
    Column('requestedConfidential', String(50)),
    Column('requestedLabelType', String(20)),
    Column('requestedCategory', String(255)),
    Column('requestedShipping', String(100)),
    Column('requestedTerminationDate', DateTime),
    Column('requestedForInternalUseOnly', Integer),
    Column('LineInstructions', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ProductInCartID', Integer),
    Column('requestedAgencyID', String(50)),
    Column('PreSubmissionProductApproved', String(1)),
    Column('ProductValidationComments', String(300)),
    Column('DistributorName', String(250)),
    Column('DistributorAddress', String(400)),
    Column('DistributorContactName', String(100)),
    Column('DistributorContactEmail', String(100)),
    Column('DistributorContactPhone', String(100)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('coPackProductPL', Boolean, nullable=False),
    Column('barcodes', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('ingredientsAllApproved', Boolean),
    Column('oldPrid', Integer),
    Index('ProductJobLineItems_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_ProductJobs_history_temporal = Table(
    'ProductJobs_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('SubmissionDate', SMALLDATETIME),
    Column('company_id', Integer),
    Column('RequestedBy', String(50)),
    Column('RequestType', String(50)),
    Column('JobComment', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('DueDate', SMALLDATETIME),
    Column('UserEmail', String(200)),
    Column('Source', String(100)),
    Column('ImportSource', String(250)),
    Column('jobid', String(34)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('ActualLogin', String(100)),
    Index('ProductJobs_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_PurchaseOrder_history_temporal = Table(
    'PurchaseOrder_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('discriminator', Unicode(255)),
    Column('PO', String(255)),
    Column('Expires', DATETIME2),
    Column('FeeType', String(255), nullable=False),
    Column('OWNS_ID', Integer),
    Column('COMPANY_ID', Integer),
    Column('Required', Boolean, nullable=False),
    Column('Inherits', Boolean, nullable=False),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_PurchaseOrder_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_RC_TB_history_temporal = Table(
    'RC_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('COMPANY_ID', Integer, nullable=False),
    Column('PERSON_JOB_ID', Integer, nullable=False),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('NCRC', String(1), nullable=False),
    Column('TIMESTAMP', BINARY(8)),
    Column('ACTIVE', Integer),
    Column('EnteredBy', String(75)),
    Column('EnteredOn', Date),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('RC_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_StripeCustomer_history_temporal = Table(
    'StripeCustomer_history_temporal', metadata,
    Column('Id', Integer, nullable=False, index=True),
    Column('company_id', Integer, nullable=False),
    Column('userLogin', String(100), nullable=False),
    Column('customerId', String(100)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_StripeCustomer_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_ThirdPartyBillingCompany_history_temporal = Table(
    'ThirdPartyBillingCompany_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('Dis', String(1)),
    Column('Name', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('Account', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('Comments', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('DeliveryNote', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('OWNS_ID', Integer),
    Column('COMPANY_ID', Integer),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('ix_ThirdPartyBillingCompany_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_USED_IN1_TB_history_temporal = Table(
    'USED_IN1_TB_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('BRAND_NAME', String(100)),
    Column('PROC_LINE_ID', Integer),
    Column('START_DATE', SMALLDATETIME),
    Column('END_DATE', DateTime),
    Column('TIMESTAMP', BINARY(8)),
    Column('STATUS', String(20)),
    Column('COMMENT', String(255)),
    Column('ACTIVE', Integer),
    Column('OWNS_ID', Integer),
    Column('RAW_MATERIAL_CODE', String(500)),
    Column('ENTERED_BY', String(75)),
    Column('Ing_Name_ps', String(75)),
    Column('JobID', Integer),
    Column('Comment_NTA', String(255)),
    Column('LineItem', SmallInteger),
    Column('DoNotDelete', String(1)),
    Column('BrokerID', Integer),
    Column('PreferredBrokerContactID', Integer),
    Column('PreferredSourceContactID', Integer),
    Column('PassoverProductionUse', String(15)),
    Column('LocReceivedStatus', Integer),
    Column('InternalCode', String(50)),
    Column('LabelID', Integer),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Index('USED_IN1_TB_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


class VISITSCOMMENT(Base):  # type: ignore
    __tablename__ = 'VISITS_COMMENT'
    _s_collection_name = 'VISITSCOMMENT'  # type: ignore
    __table_args__ = (
        Index('VisitIDID', 'VISIT_REC_ID', 'ID', 'COMMENT_TYPE'),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True, index=True)
    VISIT_REC_ID = Column(Integer, nullable=False, index=True)
    COMMENT_TYPE = Column(String(20), nullable=False)
    COMMENT = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    WHO = Column(String(50), server_default=text("(suser_sname())"))
    DATE_ENTERED = Column(DateTime, server_default=text("(getdate())"))
    CHANGESET_ID = Column(Integer, index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(sysutcdatetime())"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2],'9999-12-31 23:59:59.9999999',(0)))"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



t_VISITS_history_temporal = Table(
    'VISITS_history_temporal', metadata,
    Column('VISIT_ID', Integer, nullable=False, index=True),
    Column('ASSIGNMENT_DATE', DateTime),
    Column('VISIT_TYPE', String(40), nullable=False),
    Column('VISIT_PURPOSE', String(500)),
    Column('DESTINATION_TYPE', String(1), nullable=False),
    Column('DESTINATION_ID', Integer),
    Column('VISIT_FOR_TYPE', String(collation='SQL_Latin1_General_CP1_CI_AS')),
    Column('VISIT_FOR_ID', Integer),
    Column('BILL_TO_TYPE', String(1)),
    Column('BILL_TO_ID', Integer),
    Column('PERIOD', String(20)),
    Column('PERIOD_START_DATE', SMALLDATETIME),
    Column('PERIOD_END_DATE', SMALLDATETIME),
    Column('ACTUAL_VISIT_DATE', SMALLDATETIME),
    Column('ACTUAL_VISIT_DAYS', Float(24)),
    Column('ASSIGNED_PERSON_JOB_ID', Integer, nullable=False),
    Column('ACTUAL_PERSON_JOB_ID', Integer),
    Column('DEFAULT_BILL_AMOUNT', SMALLMONEY),
    Column('DEFAULT_EXPENSES', String(10)),
    Column('DEFAULT_PAYMENT_AMOUNY', SMALLMONEY),
    Column('OU_RENTAL_CAR', SMALLMONEY),
    Column('OU_PLANE', SMALLMONEY),
    Column('OU_OTHER', SMALLMONEY),
    Column('OU_Mileage_Differential', SMALLMONEY),
    Column('TOTAL_EXPENSES_PAID', SMALLMONEY),
    Column('TOTAL_MASHGIACH_PAY', SMALLMONEY),
    Column('TOTAL_MASHGIACH_EXPENSE', SMALLMONEY),
    Column('TOTAL_MASHGIACH_ADVANCES', SMALLMONEY),
    Column('TOTAL_BILLABLE_FEE', SMALLMONEY),
    Column('TOTAL_BILLABLE_EXPENSES', SMALLMONEY),
    Column('TOTAL_BILLABLE_PAYMENT', SMALLMONEY),
    Column('PAY_TYPE', String(20)),
    Column('PAY_AMOUNT', SMALLMONEY),
    Column('PAY_OVERTIME', SMALLMONEY),
    Column('PAY_OVERNIGHT', SMALLMONEY),
    Column('NUMBER_SHIFTS', Float(24)),
    Column('PAY_TOTAL', SMALLMONEY),
    Column('MILEAGE_NOT_PAID', Float(53)),
    Column('RATE_PER_MILEAGE', SMALLMONEY),
    Column('PLANE_NOT_PAID', SMALLMONEY),
    Column('RENTAL_CAR_NOT_PAID', SMALLMONEY),
    Column('TOLLS_NOT_PAID', SMALLMONEY),
    Column('PARKING_NOT_PAID', SMALLMONEY),
    Column('GAS_NOT_PAID', SMALLMONEY),
    Column('TAXI_NOT_PAID', SMALLMONEY),
    Column('MOTEL_NOT_PAID', SMALLMONEY),
    Column('TELEPHONE_NOT_PAID', SMALLMONEY),
    Column('MISC_NOT_PAID', SMALLMONEY),
    Column('BILLABLE_FEE', SMALLMONEY),
    Column('BILLABLE_OVERTIME_FEE', SMALLMONEY),
    Column('BILLABLE_OVERNIGHT_FEE', SMALLMONEY),
    Column('APPROVAL', String(1)),
    Column('APPROVAL_DATE', DateTime),
    Column('APPROVAL_PERSON_ID', Integer),
    Column('INV_ID', Integer),
    Column('TRIP_ID', Float(24)),
    Column('GP_BILL_TO_ID', String(7)),
    Column('GP_GO', Boolean),
    Column('AP_BATCH', Integer),
    Column('AP_DATE', DateTime),
    Column('AP_DONE', Boolean),
    Column('AR_BATCH', Integer),
    Column('AR_DATE', DateTime),
    Column('AR_DONE', Boolean),
    Column('PAY_BATCH', Integer),
    Column('PAY_DATE', DateTime),
    Column('PAY_DONE', Boolean),
    Column('GL_BATCH', Integer),
    Column('GL_DATE', DateTime),
    Column('GL_DONE', Boolean),
    Column('ID', Integer),
    Column('NUMBER_OVERTIME_SHIFTS', SmallInteger),
    Column('NO_OVERTIME_HRS', SMALLMONEY),
    Column('ACTUAL_MASH_COST', String(20)),
    Column('AssignmentID', Integer),
    Column('OnHold', DateTime),
    Column('ProcessedBy', String(50)),
    Column('VisitStatus', String(25)),
    Column('CreatedBy', String(100)),
    Column('CreatedDate', DateTime),
    Column('PurchaseOrder', String(75)),
    Column('OnHoldModifiedBy', String(100)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('TeamId', Integer),
    Column('MainVisit', Integer),
    Column('TotalVisitsInTrip', Integer),
    Index('VISITS_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_companycontacts_tb_history_temporal = Table(
    'companycontacts_tb_history_temporal', metadata,
    Column('ccID', Integer, nullable=False, index=True),
    Column('Company_ID', Integer),
    Column('CompanyTitle', String(50)),
    Column('PrimaryCT', String(1), server_default=text("('N')"), nullable=False),
    Column('BillingCT', String(1), server_default=text("('N')"), nullable=False),
    Column('WebCT', String(1), server_default=text("('N')"), nullable=False),
    Column('OtherCT', String(1), server_default=text("('N')"), nullable=False),
    Column('EnteredBy', String(50)),
    Column('DateEntered', SMALLDATETIME),
    Column('ModifiedBy', String(50)),
    Column('DateModified', DateTime),
    Column('Active', SmallInteger),
    Column('StatementType', String(1), server_default=text("('N')"), nullable=False),
    Column('InvoiceType', String(1), server_default=text("('N')"), nullable=False),
    Column('UserVendorID', String(200)),
    Column('UsedInComment', String(500)),
    Column('ContactID', Integer, nullable=False),
    Column('LOAtype', String(1)),
    Column('EIREmail', String(1)),
    Column('ScheduleBEmail', String(1)),
    Column('FormulaEmail', String(1)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('PoCT', Boolean, nullable=False),
    Column('CopackerCT', Boolean, server_default=text("((0))"), nullable=False),
    Column('UsedByCompID', Integer),
    Index('companycontacts_tb_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime')
)


t_label_barcode_history_temporal = Table(
    'label_barcode_history_temporal', metadata,
    Column('labelId', Integer, nullable=False),
    Column('barcodeId', String(255), nullable=False),
    Column('type', String(100)),
    Column('ValidFromTime', DATETIME2, nullable=False),
    Column('ValidToTime', DATETIME2, nullable=False),
    Column('CHANGESET_ID', Integer),
    Index('ix_label_barcode_history_temporal', 'ValidFromTime', 'ValidToTime')
)


t_label_tb_history_temporal = Table(
    'label_tb_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('MERCHANDISE_ID', Integer, nullable=False),
    Column('LABEL_SEQ_NUM', SmallInteger, nullable=False),
    Column('SYMBOL', String(20)),
    Column('INSTITUTIONAL', String(1)),
    Column('BLK', String(1), nullable=False),
    Column('SEAL_SIGN', String(30)),
    Column('GRP', String(10)),
    Column('SEAL_SIGN_FLAG', String(1)),
    Column('BRAND_NAME', String(100)),
    Column('SRC_MAR_ID', Integer, nullable=False, index=True),
    Column('LABEL_NAME', String(225)),
    Column('INDUSTRIAL', String(1)),
    Column('CONSUMER', String(1)),
    Column('LABEL_TYPE', String(20)),
    Column('ACTIVE', Integer),
    Column('SPECIAL_PRODUCTION', String(1)),
    Column('CREATE_DATE', DateTime),
    Column('LAST_MODIFY_DATE', DateTime),
    Column('STATUS_DATE', DateTime),
    Column('JEWISH_ACTION', String(1)),
    Column('CREATED_BY', String(100)),
    Column('MODIFIED_BY', String(100)),
    Column('LABEL_NUM', String(25)),
    Column('NUM_NAME', String(251)),
    Column('Confidential', String(1)),
    Column('AgencyID', String(50), index=True),
    Column('LOChold', String(1)),
    Column('LOCholdDate', DateTime),
    Column('PassoverSpecialProduction', String(1)),
    Column('COMMENT', String(1000)),
    Column('DisplayNewlyCertifiedOnWeb', String(1)),
    Column('Status', String(25)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('LastChangeDate', DateTime),
    Column('LastChangeReason', String(100)),
    Column('LastChangeType', String(100)),
    Column('ReplacedByAgencyId', String(50)),
    Column('TransferredFromAgencyId', String(50)),
    Column('Kitniyot', Boolean),
    Column('IsDairyEquipment', Boolean, nullable=False),
    Column('NameNum', String(251)),
    Index('label_tb_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime'),
    Index('idx_NCI_id,mid,label', 'ID', 'MERCHANDISE_ID', 'LABEL_SEQ_NUM'),
    Index('idx_NCI_label_grp', 'GRP', 'LABEL_SEQ_NUM')
)


t_produced_in1_tb_history_temporal = Table(
    'produced_in1_tb_history_temporal', metadata,
    Column('ID', Integer, nullable=False, index=True),
    Column('PROC_LINE_ID', Integer),
    Column('START_DATE', DateTime),
    Column('END_DATE', DateTime),
    Column('REGULAR', String(1)),
    Column('SPECIAL', String(1)),
    Column('PASSOVER', String(20)),
    Column('PRIVATE_LABEL_FEE', SMALLMONEY),
    Column('TIMESTAMP', BINARY(8)),
    Column('STATUS', String(20), index=True),
    Column('SPECIAL_STATUS_1', String(40)),
    Column('RC_1', String(80)),
    Column('DATE_1', DateTime),
    Column('SPECIAL_STATUS_2', String(40)),
    Column('RC_2', String(80)),
    Column('DATE_2', DateTime),
    Column('SPECIAL_STATUS_3', String(40)),
    Column('RC_3', String(80)),
    Column('DATE_3', DateTime),
    Column('SPECIAL_STATUS_4', String(40)),
    Column('RC_4', String(80)),
    Column('DATE_4', DateTime),
    Column('ACTIVE', Integer),
    Column('OWNS_ID', Integer, index=True),
    Column('DATE_CERTIFIED', SMALLDATETIME),
    Column('DATE_LAST_REV', SMALLDATETIME),
    Column('CREATE_DATE', DateTime),
    Column('CREATED_BY', String(75)),
    Column('MODIFIED_DATE', DateTime),
    Column('MODIFIED_BY', String(75)),
    Column('DIST', Boolean),
    Column('MEHADRIN', Boolean),
    Column('LOTNUM', String(500)),
    Column('LabelID', Integer),
    Column('FormulaSubmissionPlantID', Integer),
    Column('ProductPlantsID', Integer),
    Column('BatchSheetName', String(40)),
    Column('ValidFromTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False),
    Column('ValidToTime', DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False),
    Column('CHANGESET_ID', Integer, index=True),
    Column('LatestPesachSeason', Integer),
    Index('produced_in1_tb_history_temporal_STATUS_LABELID_INDEX', 'STATUS', 'LabelID'),
    Index('produced_in1_tb_history_temporal_TIME_INDEX', 'ValidFromTime', 'ValidToTime'),
    Index('produced_in1_tb_history_temporal_ID_ACTIVE_INDEX', 'ID', 'ACTIVE')
)


class CODETB(Base):  # type: ignore
    __tablename__ = 'CODE_TB'
    _s_collection_name = 'CODETB'  # type: ignore

    CodeId = Column(Integer, server_default=text("0"), primary_key=True)
    TABLE_NAME = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    FIELD_NAME = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    VALUE_SEQ_NUM = Column(SmallInteger)
    FIELD_VALUE = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    VALUE_DESCRIPTION = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text("('')"))
    PERSON_ID = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TIMESTAMP = Column(DateTime)
    ACTIVE = Column(Integer, server_default=text("((1))"))
    AdditionalParameters = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IsDefaultValue = Column(Boolean, server_default=text("((0))"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)

    # child relationships (access children)



class COMPANYTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_TB'
    _s_collection_name = 'COMPANYTB'  # type: ignore
    __table_args__ = (
        Index('idxRC', 'STATUS', 'ACTIVE', 'COMPANY_ID'),
        Index('CompStatus', 'STATUS', 'ACTIVE', 'AcquiredFrom')
    )

    COMPANY_ID = Column(Integer, server_default=text("0"), primary_key=True)
    NAME = Column(String(120), nullable=False)
    LIST = Column(String(1), server_default=text("('Y')"))
    GP_NOTIFY = Column(TINYINT, server_default=text("((0))"))
    PRODUCER = Column(Boolean)
    MARKETER = Column(Boolean)
    SOURCE = Column(Boolean)
    IN_HOUSE = Column(String(1))
    PRIVATE_LABEL = Column(String(1))
    COPACKER = Column(String(1))
    JEWISH_OWNED = Column(String(1))
    CORPORATE = Column(String(1))
    COMPANY_TYPE = Column(String(30), server_default=text("('')"))
    INVOICE_TYPE = Column(String(20), server_default=text("('Company Summary')"))
    INVOICE_FREQUENCY = Column(String(20))
    INVOICE_DTL = Column(String(20))
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(40))
    RC = Column(String(255))
    PARENT_CO = Column(String(80))
    INVOICE_LAST_DATE = Column(DateTime)
    COMPANY_BILL_TO_NAME = Column(String(255))
    ACTIVE = Column(Integer)
    AcquiredFrom = Column(String(50))
    UID = Column(String(50))
    MoveToGP = Column(String(1), server_default=text("('N')"))
    DefaultPO = Column(String(75), server_default=text("('')"))
    POexpiry = Column(Date)
    PrivateLabelPO = Column(String(50), server_default=text("('')"))
    PrivateLabelPOexpiry = Column(Date)
    VisitPO = Column(String(75), server_default=text("('')"))
    VisitPOexpiry = Column(Date)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    CATEGORY = Column(String(50))
    OLDCOMPANYTYPE = Column(String(50))
    BoilerplateInvoiceComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    IsPoRequired = Column(Boolean, server_default=text("((0))"), nullable=False)
    ShouldPropagateCompanyPo = Column(Boolean, server_default=text("((0))"), nullable=False)
    ShouldPropagateKscPoToPlants = Column(Boolean, server_default=text("((0))"), nullable=False)
    ShouldPropagateVisitPoToPlants = Column(Boolean, server_default=text("((0))"), nullable=False)
    PoReason = Column(String(2000))
    On3rdPartyBilling = Column(Boolean, server_default=text("((0))"), nullable=False)
    IsTest = Column(Boolean, server_default=text("((0))"), nullable=False)
    ChometzEmailSentDate = Column(DateTime)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    AchAuthTokenList : Mapped[List["AchAuthToken"]] = relationship(back_populates="company")
    AchPlaidLambdaResponseList : Mapped[List["AchPlaidLambdaResponse"]] = relationship(back_populates="company")
    AchStripePaymentList : Mapped[List["AchStripePayment"]] = relationship(back_populates="company")
    BarCodeList : Mapped[List["BarCode"]] = relationship(back_populates="COMPANY_TB")
    COMPANYADDRESSTBList : Mapped[List["COMPANYADDRESSTB"]] = relationship(back_populates="COMPANY_TB")
    COMPANYCERTDETAILList : Mapped[List["COMPANYCERTDETAIL"]] = relationship(back_populates="COMPANY_TB")
    COMPANYCOMMENTList : Mapped[List["COMPANYCOMMENT"]] = relationship(back_populates="COMPANY_TB")
    COMPANYFEECOMMENTList : Mapped[List["COMPANYFEECOMMENT"]] = relationship(back_populates="COMPANY_TB")
    COMPANYFEESTRUCTUREList : Mapped[List["COMPANYFEESTRUCTURE"]] = relationship(foreign_keys='[COMPANYFEESTRUCTURE.COMPANY_ID]', back_populates="COMPANY_TB")
    COMPANYFEESTRUCTUREList1 : Mapped[List["COMPANYFEESTRUCTURE"]] = relationship(foreign_keys='[COMPANYFEESTRUCTURE.COMPANY_ID]', back_populates="COMPANY_TB1", overlaps="COMPANYFEESTRUCTUREList")
    COMPANYHOLDTBList : Mapped[List["COMPANYHOLDTB"]] = relationship(foreign_keys='[COMPANYHOLDTB.COMPANY_ID]', back_populates="COMPANY_TB")
    COMPANYHOLDTBList1 : Mapped[List["COMPANYHOLDTB"]] = relationship(foreign_keys='[COMPANYHOLDTB.COMPANY_ID]', back_populates="COMPANY_TB1", overlaps="COMPANYHOLDTBList")
    COMPANYOTHERNAMEList : Mapped[List["COMPANYOTHERNAME"]] = relationship(back_populates="COMPANY_TB")
    COMPANYSTATUSTBList : Mapped[List["COMPANYSTATUSTB"]] = relationship(foreign_keys='[COMPANYSTATUSTB.COMPANY_ID]', back_populates="COMPANY_TB")
    COMPANYSTATUSTBList1 : Mapped[List["COMPANYSTATUSTB"]] = relationship(foreign_keys='[COMPANYSTATUSTB.COMPANY_ID]', back_populates="COMPANY_TB1", overlaps="COMPANYSTATUSTBList")
    COPRIVATELABELFEEDETAILList : Mapped[List["COPRIVATELABELFEEDETAIL"]] = relationship(back_populates="COMPANY_TB")
    CoPackerFacilityList : Mapped[List["CoPackerFacility"]] = relationship(back_populates="Company")
    MiniCRMActionList : Mapped[List["MiniCRMAction"]] = relationship(back_populates="Company")
    PLANTTBList : Mapped[List["PLANTTB"]] = relationship(back_populates="COMPANY_TB")
    PrivateLabelTemplateList : Mapped[List["PrivateLabelTemplate"]] = relationship(back_populates="COMPANY_TB")
    ProductJobList : Mapped[List["ProductJob"]] = relationship(back_populates="company")
    RCTBList : Mapped[List["RCTB"]] = relationship(back_populates="COMPANY_TB")
    StripeCustomerList : Mapped[List["StripeCustomer"]] = relationship(back_populates="company")
    CompanycontactsTbList : Mapped[List["CompanycontactsTb"]] = relationship(back_populates="COMPANY_TB")
    LabelTbList : Mapped[List["LabelTb"]] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates="COMPANY_TB")
    LabelTbList1 : Mapped[List["LabelTb"]] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates="COMPANY_TB1", overlaps="LabelTbList")
    INVOICEFEEList : Mapped[List["INVOICEFEE"]] = relationship(back_populates="COMPANY_TB")
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="COMPANY_TB")
    PENDINGINFOTBList : Mapped[List["PENDINGINFOTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="COMPANY_TB")
    PLANTCERTDETAILList : Mapped[List["PLANTCERTDETAIL"]] = relationship(back_populates="COMPANY_TB")
    PLANTCOMMENTList : Mapped[List["PLANTCOMMENT"]] = relationship(back_populates="COMPANY_TB")
    PLANTFEECOMMENTList : Mapped[List["PLANTFEECOMMENT"]] = relationship(back_populates="COMPANY_TB")
    PLANTFEESTRUCTUREOUTList : Mapped[List["PLANTFEESTRUCTUREOUT"]] = relationship(back_populates="COMPANY_TB")
    PRIVATELABELBILLList : Mapped[List["PRIVATELABELBILL"]] = relationship(foreign_keys='[PRIVATELABELBILL.BILL_TO_CO_ID]', back_populates="COMPANY_TB")
    PRIVATELABELBILLList1 : Mapped[List["PRIVATELABELBILL"]] = relationship(foreign_keys='[PRIVATELABELBILL.COMPANY_ID]', back_populates="COMPANY_TB1")
    PRIVATELABELBILLList2 : Mapped[List["PRIVATELABELBILL"]] = relationship(foreign_keys='[PRIVATELABELBILL.SRC_MAR_ID]', back_populates="COMPANY_TB2")
    VISITList : Mapped[List["VISIT"]] = relationship(back_populates="COMPANY_TB")
    BillingList : Mapped[List["Billing"]] = relationship(back_populates="COMPANY_TB")
    CompanyPlantOptionList : Mapped[List["CompanyPlantOption"]] = relationship(back_populates="COMPANY_TB")
    PLANTFEESTRUCTUREList : Mapped[List["PLANTFEESTRUCTURE"]] = relationship(back_populates="COMPANY_TB")
    PLANTHOLDTBList : Mapped[List["PLANTHOLDTB"]] = relationship(back_populates="COMPANY_TB")
    PurchaseOrderList : Mapped[List["PurchaseOrder"]] = relationship(back_populates="COMPANY_TB")
    ThirdPartyBillingCompanyList : Mapped[List["ThirdPartyBillingCompany"]] = relationship(back_populates="COMPANY_TB")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="COMPANY_TB")



class INVOICEFEESDETAIL(Base):  # type: ignore
    __tablename__ = 'INVOICE_FEES_DETAIL'
    _s_collection_name = 'INVOICEFEESDETAIL'  # type: ignore
    __table_args__ = (
        Index('invoiceIdVisitID', 'INVOICE_ID', 'VISIT_ID'),
        Index('XPK_INVOICE_FEES_DET', 'INVOICE_ID', 'INVOICE_LINE'),
        Index('infd', 'INVOICE_ID', 'PERIOD_START_DATE')
    )

    ID = Column(Integer, primary_key=True)
    INVOICE_ID = Column(Integer, nullable=False)
    INVOICE_LINE = Column(Integer, nullable=False)
    VISIT_ID = Column(Integer)
    DESTINATION_TYPE = Column(String(1))
    DESTINATION_ID = Column(Integer, index=True)
    FEE = Column(MONEY)
    EXPENSES = Column(MONEY)
    VISIT_TYPE = Column(String(100))
    VISIT_DATE = Column(DateTime)
    VISIT_PERSON_JOB_ID = Column(Integer)
    PERIOD_START_DATE = Column(DateTime)
    PERIOD_END_DATE = Column(DateTime)
    REASON = Column(String(50))
    TIMESTAMP = Column(BINARY(8))
    ownsID = Column(Integer)
    voided = Column(Boolean, server_default=text("((0))"), nullable=False)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



class MERCHCOMMENT(Base):  # type: ignore
    __tablename__ = 'MERCH_COMMENT'
    _s_collection_name = 'MERCHCOMMENT'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    MERCHANDISE_ID = Column(Integer, nullable=False, index=True)
    COMMENT_ID = Column(Integer, nullable=False, index=True)
    TIMESTAMP = Column(BINARY(8))
    CommentType = Column(String(20), server_default=text("('CNTA')"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)

    # child relationships (access children)



class MERCHTB(Base):  # type: ignore
    __tablename__ = 'MERCH_TB'
    _s_collection_name = 'MERCHTB'  # type: ignore
    __table_args__ = (
        Index('ix_MERCH_TB_ACTIVE_Reviewed_includes', 'ACTIVE', 'Reviewed'),
        Index('idx_MerchandiseID_Active', 'MERCHANDISE_ID', 'ACTIVE', unique=True),
        Index('idxSymbol', 'Symbol', 'MERCHANDISE_ID', 'ACTIVE')
    )

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
    BrochoCode = Column(SmallInteger, server_default=text("((0))"))
    Brocho2Code = Column(SmallInteger, server_default=text("((0))"))
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
    FormulaProductList : Mapped[List["FormulaProduct"]] = relationship(back_populates="MERCH_TB")
    MERCHOTHERNAMEList : Mapped[List["MERCHOTHERNAME"]] = relationship(back_populates="MERCH_TB")
    YoshonInfoList : Mapped[List["YoshonInfo"]] = relationship(back_populates="Merch")
    LabelTbList : Mapped[List["LabelTb"]] = relationship(back_populates="MERCH_TB")
    FormulaComponentList : Mapped[List["FormulaComponent"]] = relationship(back_populates="MERCH_TB")
    FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="MERCH_TB")



class PERSONADDRESSTB(Base):  # type: ignore
    __tablename__ = 'PERSON_ADDRESS_TB'
    _s_collection_name = 'PERSONADDRESSTB'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    PERSON_ID = Column(ForeignKey('PERSON_TB.PERSON_ID'), nullable=False, index=True)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(20))
    ATTN = Column(String(40))
    STREET1 = Column(String(40))
    STREET2 = Column(String(40))
    STREET3 = Column(String(40))
    CITY = Column(String(40))
    STATE = Column(String(25))
    ZIP = Column(String(15))
    COUNTRY = Column(String(25), server_default=text("('')"))
    ACTIVE = Column(Integer)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    PERSON_TB : Mapped["PERSONTB"] = relationship(back_populates=("PERSONADDRESSTBList"))

    # child relationships (access children)



class AchAuthToken(Base):  # type: ignore
    __tablename__ = 'AchAuthToken'
    _s_collection_name = 'AchAuthToken'  # type: ignore

    company_id = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    userLogin = Column(String(100), nullable=False)
    link_session_id = Column(String(100), nullable=False)
    public_token = Column(String(100), nullable=False)
    accountID = Column(String(100), nullable=False)
    institutionName = Column(String(100), nullable=False)
    institutionId = Column(String(100), nullable=False)
    accountName = Column(String(100), nullable=False)
    accountMask = Column(String(100), nullable=False)
    accountType = Column(String(100), nullable=False)
    Id = Column(Integer, server_default=text("0"), primary_key=True)
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    agreedBy = Column(String(255))
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    company : Mapped["COMPANYTB"] = relationship(back_populates=("AchAuthTokenList"))

    # child relationships (access children)



class AchPlaidLambdaResponse(Base):  # type: ignore
    __tablename__ = 'AchPlaidLambdaResponse'
    _s_collection_name = 'AchPlaidLambdaResponse'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True)
    company_id = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    userLogin = Column(String(100), nullable=False)
    stripe_bank_account_token = Column(String(100), nullable=False)
    access_token = Column(String(100))
    request_id = Column(String(100), nullable=False)
    status_code = Column(String(100), nullable=False)
    accountID = Column(String(100), nullable=False)
    public_token = Column(String(100), nullable=False)
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    company : Mapped["COMPANYTB"] = relationship(back_populates=("AchPlaidLambdaResponseList"))

    # child relationships (access children)



class AchStripePayment(Base):  # type: ignore
    __tablename__ = 'AchStripePayment'
    _s_collection_name = 'AchStripePayment'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True)
    company_id = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    UserLogin = Column(String(100))
    Amount = Column(BigInteger)
    Currency = Column(String(100))
    Description = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ReceiptEmail = Column(String(100))
    JsonRet = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    StripeId = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    CHANGESET_ID = Column(Integer, index=True)
    ProcessorType = Column(String(50), nullable=False)
    FeeAmount = Column(BigInteger, server_default=text("((0))"))
    Comments = Column(String(255))
    CardKnoxId = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    CustomerFeeWaived = Column(Boolean, server_default=text("((0))"), nullable=False)

    # parent relationships (access parent)
    company : Mapped["COMPANYTB"] = relationship(back_populates=("AchStripePaymentList"))

    # child relationships (access children)
    AchStripePaymentDetailList : Mapped[List["AchStripePaymentDetail"]] = relationship(back_populates="AchStripePayment")



class BarCode(Base):  # type: ignore
    __tablename__ = 'BarCode'
    _s_collection_name = 'BarCode'  # type: ignore

    Id = Column(String(255), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("BarCodeList"))

    # child relationships (access children)
    LabelBarcodeList : Mapped[List["LabelBarcode"]] = relationship(back_populates="barcode")



class COMPANYADDRESSTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_ADDRESS_TB'
    _s_collection_name = 'COMPANYADDRESSTB'  # type: ignore
    __table_args__ = (
        Index('compaddress2', 'COMPANY_ID', 'ADDRESS_SEQ_NUM', 'ACTIVE'),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    ADDRESS_SEQ_NUM = Column(Integer, nullable=False)
    TYPE = Column(String(40))
    ATTN = Column(String(40))
    STREET1 = Column(String(60), server_default=text("('')"))
    STREET2 = Column(String(60), server_default=text("('')"))
    STREET3 = Column(String(60))
    CITY = Column(String(40), server_default=text("('')"))
    STATE = Column(String(25), server_default=text("('')"))
    ZIP = Column(String(18))
    COUNTRY = Column(String(25), server_default=text("('')"))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYADDRESSTBList"))

    # child relationships (access children)



class COMPANYCERTDETAIL(Base):  # type: ignore
    __tablename__ = 'COMPANY_CERT_DETAIL'
    _s_collection_name = 'COMPANYCERTDETAIL'  # type: ignore

    ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMPANY_FEE_ID = Column(Integer, nullable=False, index=True)
    CERT_DETAIL_SEQ_NUM = Column(SmallInteger, nullable=False)
    CERT_DETAIL_DESCRIPTION = Column(String(80))
    CERT_DETAIL_AMOUNT = Column(MONEY)
    CERT_DETAIL_DATE = Column(DateTime)
    CERT_DETAIL_PERSON_ID = Column(String(20))
    CERT_DETAIL_COMMENT = Column(String(255))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYCERTDETAILList"))

    # child relationships (access children)



class COMPANYCOMMENT(Base):  # type: ignore
    __tablename__ = 'COMPANY_COMMENT'
    _s_collection_name = 'COMPANYCOMMENT'  # type: ignore
    __table_args__ = (
        Index('XPKCOMPANY_COMMENT', 'COMPANY_ID', 'COMMENT_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMMENT_ID = Column(Integer, nullable=False)
    TIMESTAMP = Column(BINARY(8))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYCOMMENTList"))

    # child relationships (access children)



class COMPANYFEECOMMENT(Base):  # type: ignore
    __tablename__ = 'COMPANY_FEE_COMMENT'
    _s_collection_name = 'COMPANYFEECOMMENT'  # type: ignore
    __table_args__ = (
        Index('XPKCOMPANY_FEE_COMMENT', 'COMPANY_ID', 'COMMENT_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMMENT_ID = Column(Integer, nullable=False)
    TIMESTAMP = Column(BINARY(8))
    CHANGESET_ID = Column(Integer)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYFEECOMMENTList"))

    # child relationships (access children)



class COMPANYFEESTRUCTURE(Base):  # type: ignore
    __tablename__ = 'COMPANY_FEE_STRUCTURE'
    _s_collection_name = 'COMPANYFEESTRUCTURE'  # type: ignore
    __table_args__ = (
        Index('XPKCOMPANY_FEE_STRUCTURE', 'COMPANY_ID', 'COMPANY_FEE_ID'),
    )

    ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMPANY_FEE_ID = Column(SmallInteger, server_default=text("((1))"), nullable=False)
    EFFECTIVE_DATE = Column(DateTime)
    APPROVAL = Column(String(1), nullable=False)
    APPROVAL_DATE = Column(DateTime)
    APPROVAL_PERSON_ID = Column(Integer)
    CERT_FEE = Column(MONEY)
    EXPENSE_TYPE = Column(String(15))
    EXPENSE_AMT = Column(MONEY)
    EXPENSE_PERCENT = Column(Float(53))
    VISIT_FEE_TYPE = Column(String(20))
    FREE_VISITS_NUM = Column(Integer)
    VISIT_FEE = Column(MONEY)
    SPECIAL_PRODUCTION_TYPE = Column(String(20))
    SPECIAL_PRODUCTION_FEE = Column(SMALLMONEY)
    UNIT_BASE = Column(Integer)
    PASSOVER_FEE_TYPE = Column(String(25))
    PASSOVER_FEE = Column(SMALLMONEY)
    PASSOVER_VISIT_FEE = Column(SMALLMONEY)
    PASSOVER_UNIT_RATE = Column(SMALLMONEY)
    PASSOVER_UNIT_BASE = Column(String(20))
    PRIVATE_LABEL_TYPE = Column(String(20))
    PRIVATE_LABEL_FEE1 = Column(SMALLMONEY)
    PRIVATE_LABEL_BASE1 = Column(Integer)
    PRIVATE_LABEL_FEE2 = Column(SMALLMONEY)
    PRIVATE_LABEL_BASE2 = Column(Integer)
    PRIVATE_LABEL_FEE3 = Column(SMALLMONEY)
    PRIVATE_LABEL_BASE3 = Column(Integer)
    SPECIAL_PRODUCTION_FEE1 = Column(SMALLMONEY)
    UNIT_BASE1 = Column(Integer)
    SPECIAL_PRODUCTION_FEE2 = Column(SMALLMONEY)
    UNIT_BASE2 = Column(Integer)
    VISIT_FEE1 = Column(MONEY)
    FREE_VISITS_NUM1 = Column(Integer)
    VISIT_FEE2 = Column(MONEY)
    FREE_VISITS_NUM2 = Column(Integer)
    CERT_FREQ = Column(String(20))
    CERT_DATE = Column(DateTime)
    PASSOVER_RATE_FEE1 = Column(SMALLMONEY)
    PASSOVER_FOR_FEE1 = Column(Integer)
    PASSOVER_RATE_FEE2 = Column(SMALLMONEY)
    PASSOVER_FOR_FEE2 = Column(Integer)
    PASSOVER_RATE_FEE3 = Column(SMALLMONEY)
    PASSOVER_FOR_FEE3 = Column(Integer)
    BILL_REG_VISIT_TYPEx = Column(String(20))
    BILL_REG_VISIT_AMTx = Column(String(20))
    BILL_SPEC_PROD_TYPEx = Column(String(20))
    BILL_SPEC_PROD_AMTx = Column(String(20))
    BILL_PASSOVER_TYPEx = Column(String(20))
    BILL_PASSOVER_AMTx = Column(String(20))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    LockPerDistributorRate = Column(Boolean, server_default=text("((0))"), nullable=False)
    PRIVATE_LABEL_COMMENT = Column(String(500))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYFEESTRUCTURE.COMPANY_ID]', back_populates=("COMPANYFEESTRUCTUREList"))
    COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYFEESTRUCTURE.COMPANY_ID]', back_populates=("COMPANYFEESTRUCTUREList1"), overlaps="COMPANYFEESTRUCTUREList,COMPANY_TB")

    # child relationships (access children)



class COMPANYHOLDTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_HOLD_TB'
    _s_collection_name = 'COMPANYHOLDTB'  # type: ignore
    __table_args__ = (
        Index('XAKCOMPANY_HOLD_1', 'ID', 'COMPANY_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMPANY_SEQ_NUM = Column(SmallInteger, nullable=False)
    HOLD_TYPE = Column(String(4))
    START_PERSON_ID = Column(String(20), nullable=False)
    START_DATE = Column(DateTime)
    START_REASON = Column(String(100), nullable=False)
    END_PERSON_ID = Column(String(20))
    END_DATE = Column(DateTime)
    END_REASON = Column(String(100))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYHOLDTB.COMPANY_ID]', back_populates=("COMPANYHOLDTBList"))
    COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYHOLDTB.COMPANY_ID]', back_populates=("COMPANYHOLDTBList1"), overlaps="COMPANYHOLDTBList,COMPANY_TB")

    # child relationships (access children)



class COMPANYOTHERNAME(Base):  # type: ignore
    __tablename__ = 'COMPANY_OTHER_NAMES'
    _s_collection_name = 'COMPANYOTHERNAME'  # type: ignore
    __table_args__ = (
        Index('XPKCOMPANY_OTHERNAMES', 'COMPANY_ID', 'ALIAS_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    ALIAS_ID = Column(Integer)
    LEGAL_NAME = Column(Boolean)
    DBA = Column(Boolean)
    CONTRACT_NAME = Column(Boolean)
    TIMESTAMP = Column(BINARY(8))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COMPANYOTHERNAMEList"))

    # child relationships (access children)



class COMPANYSTATUSTB(Base):  # type: ignore
    __tablename__ = 'COMPANY_STATUS_TB'
    _s_collection_name = 'COMPANYSTATUSTB'  # type: ignore
    __table_args__ = (
        Index('XFKCOMPANY_STATUS_1', 'ID', 'COMPANY_ID', 'STATUS', 'START_DATE', 'END_DATE', 'ACTIVE', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), ForeignKey('COMPANY_TB.COMPANY_ID'))
    ROLE = Column(String(1))
    STATUS = Column(String(40))
    ACTIVE_FLAG = Column(Boolean)
    START_DATE = Column(DateTime)
    START_PERSON_ID = Column(String(20), server_default=text("(substring(suser_sname(),(0),(20)))"))
    START_REASON = Column(String(100))
    END_DATE = Column(DateTime, index=True)
    END_PERSON_ID = Column(String(20))
    END_REASON = Column(String(100))
    ACTIVE = Column(Integer)
    DateDone = Column(DateTime, server_default=text("(getdate())"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYSTATUSTB.COMPANY_ID]', back_populates=("COMPANYSTATUSTBList"))
    COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[COMPANYSTATUSTB.COMPANY_ID]', back_populates=("COMPANYSTATUSTBList1"), overlaps="COMPANYSTATUSTBList,COMPANY_TB")

    # child relationships (access children)



class COPRIVATELABELFEEDETAIL(Base):  # type: ignore
    __tablename__ = 'CO_PRIVATE_LABEL_FEE_DETAIL'
    _s_collection_name = 'COPRIVATELABELFEEDETAIL'  # type: ignore

    ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMPANY_FEE_ID = Column(Integer, nullable=False, index=True)
    PL_DETAIL_SEQ_NUM = Column(SmallInteger, nullable=False)
    PL_DETAIL_DESCRIPTION = Column(String(80))
    PL_DETAIL_AMOUNT = Column(MONEY)
    PL_DETAIL_DATE = Column(DateTime)
    PL_DETAIL_PERSON_ID = Column(String(20), nullable=False)
    PL_DETAIL_COMMENT = Column(String(255))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("COPRIVATELABELFEEDETAILList"))

    # child relationships (access children)



class CoPackerFacility(Base):  # type: ignore
    __tablename__ = 'CoPackerFacilities'
    _s_collection_name = 'CoPackerFacility'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    CompanyId = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    WebsiteURL = Column(String(500))
    Description = Column(String(500))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer)

    # parent relationships (access parent)
    Company : Mapped["COMPANYTB"] = relationship(back_populates=("CoPackerFacilityList"))

    # child relationships (access children)
    CoPackerFacilitiesCategoryList : Mapped[List["CoPackerFacilitiesCategory"]] = relationship(back_populates="CoPacker")
    CoPackerFacilitiesLocationList : Mapped[List["CoPackerFacilitiesLocation"]] = relationship(back_populates="CoPacker")



class FormulaProduct(Base):  # type: ignore
    __tablename__ = 'FormulaProduct'
    _s_collection_name = 'FormulaProduct'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    FormulaID = Column(Integer, nullable=False)
    Merchandise_ID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), nullable=False)

    # parent relationships (access parent)
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("FormulaProductList"))

    # child relationships (access children)



class MERCHOTHERNAME(Base):  # type: ignore
    __tablename__ = 'MERCH_OTHER_NAMES'
    _s_collection_name = 'MERCHOTHERNAME'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    ALIAS_ID = Column(Integer, index=True)
    MERCHANDISE_ID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), index=True)
    TYPE = Column(String(40))
    TIMESTAMP = Column(BINARY(8))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("MERCHOTHERNAMEList"))

    # child relationships (access children)



class MiniCRMAction(Base):  # type: ignore
    __tablename__ = 'MiniCRMActions'
    _s_collection_name = 'MiniCRMAction'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    CreatedDate = Column(DateTime, server_default=text("(getdate())"), nullable=False)
    CreatedBy = Column(Integer)
    ModifiedDate = Column(DateTime)
    ModifiedBy = Column(Integer)
    ActivityDate = Column(DateTime)
    Modality = Column(String(250))
    ContactId = Column(Integer, nullable=False)
    CompanyId = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    Result = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ReminderDate = Column(DateTime)
    Comment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer)

    # parent relationships (access parent)
    Company : Mapped["COMPANYTB"] = relationship(back_populates=("MiniCRMActionList"))

    # child relationships (access children)



class PLANTTB(Base):  # type: ignore
    __tablename__ = 'PLANT_TB'
    _s_collection_name = 'PLANTTB'  # type: ignore

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
    MaxOnSiteVisits = Column(SmallInteger, server_default=text("((0))"), nullable=False)
    MaxVirtualVisits = Column(SmallInteger, server_default=text("((0))"), nullable=False)
    IsDaily = Column(Boolean, server_default=text("((0))"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList"))
    PERSON_JOB_TB1 : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[PLANTTB.DesignatedRFR]', back_populates=("PLANTTBList1"), overlaps="PERSON_JOB_TB,PLANTTBList")
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTTBList"))

    # child relationships (access children)
    INVOICEFEEList : Mapped[List["INVOICEFEE"]] = relationship(back_populates="PLANT_TB")
    OWNSTBList : Mapped[List["OWNSTB"]] = relationship(back_populates="PLANT_TB")
    PENDINGINFOTBList : Mapped[List["PENDINGINFOTB"]] = relationship(back_populates="PLANT_TB")
    PLANTADDRESSTBList : Mapped[List["PLANTADDRESSTB"]] = relationship(back_populates="PLANT_TB")
    PLANTCERTDETAILList : Mapped[List["PLANTCERTDETAIL"]] = relationship(back_populates="PLANT_TB")
    PLANTCOMMENTList : Mapped[List["PLANTCOMMENT"]] = relationship(back_populates="PLANT_TB")
    PLANTFEECOMMENTList : Mapped[List["PLANTFEECOMMENT"]] = relationship(back_populates="PLANT_TB")
    PLANTFEESTRUCTUREOUTList : Mapped[List["PLANTFEESTRUCTUREOUT"]] = relationship(back_populates="PLANT_TB")
    PLANTOTHERNAMEList : Mapped[List["PLANTOTHERNAME"]] = relationship(back_populates="PLANT_TB")
    PRIVATELABELBILLList : Mapped[List["PRIVATELABELBILL"]] = relationship(back_populates="PLANT_TB")
    VISITList : Mapped[List["VISIT"]] = relationship(back_populates="PLANT_TB")
    CompanyPlantOptionList : Mapped[List["CompanyPlantOption"]] = relationship(back_populates="Plant")
    PLANTHOLDTBList : Mapped[List["PLANTHOLDTB"]] = relationship(back_populates="PLANT_TB")



class PrivateLabelTemplate(Base):  # type: ignore
    __tablename__ = 'PrivateLabelTemplate'
    _s_collection_name = 'PrivateLabelTemplate'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    Template = Column(LargeBinary)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    AddedBy = Column(String(30))
    DateAdded = Column(DateTime)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PrivateLabelTemplateList"))

    # child relationships (access children)



class ProductJob(Base):  # type: ignore
    __tablename__ = 'ProductJobs'
    _s_collection_name = 'ProductJob'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    SubmissionDate = Column(SMALLDATETIME, server_default=text("(getdate())"))
    company_id = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    RequestedBy = Column(String(50), server_default=text("(suser_name())"))
    RequestType = Column(String(50))
    JobComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    DueDate = Column(SMALLDATETIME, server_default=text("(getdate()+(7))"))
    UserEmail = Column(String(200))
    Source = Column(String(100))
    ImportSource = Column(String(250))
    jobid = Column(String(34), Computed("(case when [requesttype]='Formula' then CONVERT([varchar],[ID],(0))+'-002' when [ImportSource]='ProductImport' then CONVERT([varchar],[ID],(0))+'-003' else CONVERT([varchar],[ID],(0))+'-001' end)", persisted=False), index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    ActualLogin = Column(String(100))

    # parent relationships (access parent)
    company : Mapped["COMPANYTB"] = relationship(back_populates=("ProductJobList"))

    # child relationships (access children)



class RCTB(Base):  # type: ignore
    __tablename__ = 'RC_TB'
    _s_collection_name = 'RCTB'  # type: ignore
    __table_args__ = (
        Index('ByRC', 'COMPANY_ID', 'PERSON_JOB_ID'),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PERSON_JOB_ID = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'), nullable=False, index=True)
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    NCRC = Column(String(1), nullable=False)
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    EnteredBy = Column(String(75), server_default=text("(suser_sname())"))
    EnteredOn = Column(Date, server_default=text("(getdate())"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("RCTBList"))
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(back_populates=("RCTBList"))

    # child relationships (access children)



class StripeCustomer(Base):  # type: ignore
    __tablename__ = 'StripeCustomer'
    _s_collection_name = 'StripeCustomer'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True)
    company_id = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    userLogin = Column(String(100), nullable=False)
    customerId = Column(String(100))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    company : Mapped["COMPANYTB"] = relationship(back_populates=("StripeCustomerList"))

    # child relationships (access children)



class YoshonInfo(Base):  # type: ignore
    __tablename__ = 'YoshonInfo'
    _s_collection_name = 'YoshonInfo'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True, index=True)
    Description = Column(String(200))
    Comment = Column(String(5000))
    Value = Column(String(500))
    MerchId = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), nullable=False)
    OuCertified = Column(Boolean, server_default=text("((0))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(sysutcdatetime())"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2],'9999-12-31 23:59:59.9999999'))"), nullable=False)

    # parent relationships (access parent)
    Merch : Mapped["MERCHTB"] = relationship(back_populates=("YoshonInfoList"))

    # child relationships (access children)



class CompanycontactsTb(Base):  # type: ignore
    __tablename__ = 'companycontacts_tb'
    _s_collection_name = 'CompanycontactsTb'  # type: ignore
    __table_args__ = (
        Index('id', 'ccID', 'Company_ID', unique=True),
    )

    ccID = Column(Integer, server_default=text("0"), primary_key=True)
    Company_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), index=True)
    CompanyTitle = Column(String(50))
    PrimaryCT = Column(String(1), server_default=text("('N')"), nullable=False)
    BillingCT = Column(String(1), server_default=text("('N')"), nullable=False)
    WebCT = Column(String(1), server_default=text("('N')"), nullable=False)
    OtherCT = Column(String(1), server_default=text("('N')"), nullable=False)
    EnteredBy = Column(String(50), server_default=text("(suser_sname())"))
    DateEntered = Column(SMALLDATETIME, server_default=text("(getdate())"))
    ModifiedBy = Column(String(50))
    DateModified = Column(DateTime)
    Active = Column(SmallInteger)
    StatementType = Column(String(1), server_default=text("('N')"), nullable=False)
    InvoiceType = Column(String(1), server_default=text("('N')"), nullable=False)
    UserVendorID = Column(String(200), server_default=text("('')"))
    UsedInComment = Column(String(500), server_default=text("('')"))
    ContactID = Column(Integer, nullable=False)
    LOAtype = Column(String(1))
    EIREmail = Column(String(1))
    ScheduleBEmail = Column(String(1))
    FormulaEmail = Column(String(1))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    PoCT = Column(Boolean, server_default=text("((0))"), nullable=False)
    CopackerCT = Column(Boolean, server_default=text("((0))"), nullable=False)
    UsedByCompID = Column(Integer, server_default=text("((0))"))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("CompanycontactsTbList"))

    # child relationships (access children)



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

    ID = Column(Integer, server_default=text("0"), primary_key=True, unique=True)
    MERCHANDISE_ID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'), nullable=False)
    LABEL_SEQ_NUM = Column(SmallInteger, nullable=False)
    SYMBOL = Column(String(20))
    INSTITUTIONAL = Column(String(1))
    BLK = Column(String(1), Computed("(case when [GRP]='5' OR [GRP]='4' then 'Y' else 'N' end)", persisted=False), nullable=False)
    SEAL_SIGN = Column(String(30), server_default=text("('{NONE}')"))
    GRP = Column(String(10), server_default=text("((3))"))
    SEAL_SIGN_FLAG = Column(String(1))
    BRAND_NAME = Column(String(100), index=True)
    SRC_MAR_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    LABEL_NAME = Column(String(225), index=True)
    INDUSTRIAL = Column(String(1))
    CONSUMER = Column(String(1))
    LABEL_TYPE = Column(String(20))
    ACTIVE = Column(Integer)
    SPECIAL_PRODUCTION = Column(String(1))
    CREATE_DATE = Column(DateTime, server_default=text("(getdate())"), index=True)
    LAST_MODIFY_DATE = Column(DateTime, server_default=text("(getdate())"), index=True)
    STATUS_DATE = Column(DateTime)
    JEWISH_ACTION = Column(String(1))
    CREATED_BY = Column(String(100), server_default=text("(suser_sname())"))
    MODIFIED_BY = Column(String(100), server_default=text("(suser_sname())"))
    LABEL_NUM = Column(String(25))
    NUM_NAME = Column(String(251), Computed("(case when [LABEL_NUM] IS NULL OR [LABEL_NUM]='' then [LABEL_NAME] else ([LABEL_NUM]+' ')+[LABEL_NAME] end)", persisted=False), index=True)
    Confidential = Column(String(1))
    AgencyID = Column(String(50), unique=True)
    LOChold = Column(String(1))
    LOCholdDate = Column(DateTime)
    PassoverSpecialProduction = Column(String(1), server_default=text("('N')"))
    COMMENT = Column(String(1000), server_default=text("('')"))
    DisplayNewlyCertifiedOnWeb = Column(String(1), server_default=text("('N')"))
    Status = Column(String(25))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    LastChangeDate = Column(DateTime)
    LastChangeReason = Column(String(100))
    LastChangeType = Column(String(100))
    ReplacedByAgencyId = Column(String(50))
    TransferredFromAgencyId = Column(String(50))
    Kitniyot = Column(Boolean)
    IsDairyEquipment = Column(Boolean, server_default=text("((0))"), nullable=False)
    NameNum = Column(String(251), Computed("(ltrim(isnull(concat(nullif([Label_Name],''),case when [Label_Name]<>'' AND [Label_Num]<>'' then ' '+[Label_Num] else [Label_Num] end),'')))", persisted=False))

    # parent relationships (access parent)
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("LabelTbList"))
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList"))
    COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[LabelTb.SRC_MAR_ID]', back_populates=("LabelTbList1"), overlaps="COMPANY_TB,LabelTbList")

    # child relationships (access children)
    FormulaComponentList : Mapped[List["FormulaComponent"]] = relationship(back_populates="label_tb")
    LabelCommentList : Mapped[List["LabelComment"]] = relationship(back_populates="Label")
    LabelOptionList : Mapped[List["LabelOption"]] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates="label_tb")
    LabelOptionList1 : Mapped[List["LabelOption"]] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates="label_tb1", overlaps="LabelOptionList")
    LabelBarcodeList : Mapped[List["LabelBarcode"]] = relationship(back_populates="label")
    FormulaSubmissionComponentList : Mapped[List["FormulaSubmissionComponent"]] = relationship(back_populates="label_tb")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="label_tb")
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="label_tb")



class AchStripePaymentDetail(Base):  # type: ignore
    __tablename__ = 'AchStripePaymentDetail'
    _s_collection_name = 'AchStripePaymentDetail'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True)
    AchStripePaymentId = Column(ForeignKey('AchStripePayment.Id'), nullable=False)
    DocumentNumber = Column(String(100))
    Amount : DECIMAL = Column(DECIMAL(12, 2))
    TransactionBalance : DECIMAL = Column(DECIMAL(12, 2))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    AchStripePayment : Mapped["AchStripePayment"] = relationship(back_populates=("AchStripePaymentDetailList"))

    # child relationships (access children)



class CoPackerFacilitiesCategory(Base):  # type: ignore
    __tablename__ = 'CoPackerFacilitiesCategory'
    _s_collection_name = 'CoPackerFacilitiesCategory'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    CoPackerId = Column(ForeignKey('CoPackerFacilities.ID'), nullable=False)
    Category = Column(String(500), nullable=False)
    CategoryParent = Column(String(500), Computed("(case when [category] like '%-%' then left([category],charindex('-',[category])-(1)) else [category] end)", persisted=False))
    CategoryChild = Column(String(500), Computed("(case when [category] like '%-%' then substring([category],charindex('-',[category])+(1),len([category])-charindex('-',[category])) else '' end)", persisted=False))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer)

    # parent relationships (access parent)
    CoPacker : Mapped["CoPackerFacility"] = relationship(back_populates=("CoPackerFacilitiesCategoryList"))

    # child relationships (access children)



class CoPackerFacilitiesLocation(Base):  # type: ignore
    __tablename__ = 'CoPackerFacilitiesLocation'
    _s_collection_name = 'CoPackerFacilitiesLocation'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    CoPackerId = Column(ForeignKey('CoPackerFacilities.ID'), nullable=False)
    Location = Column(String(500), nullable=False)
    LocationCity = Column(String(200))
    LocationState = Column(String(200))
    LocationProvince = Column(String(200))
    LocationCountry = Column(String(200))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer)

    # parent relationships (access parent)
    CoPacker : Mapped["CoPackerFacility"] = relationship(back_populates=("CoPackerFacilitiesLocationList"))

    # child relationships (access children)



class FormulaComponent(Base):  # type: ignore
    __tablename__ = 'FormulaComponents'
    _s_collection_name = 'FormulaComponent'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    FormulaID = Column(Integer, nullable=False)
    ComponentMerchID = Column(ForeignKey('MERCH_TB.MERCHANDISE_ID'))
    ComponentLabelID = Column(ForeignKey('label_tb.ID'))
    Component = Column(String(50), nullable=False)
    ComponentIDType = Column(String(50), nullable=False)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("FormulaComponentList"))
    MERCH_TB : Mapped["MERCHTB"] = relationship(back_populates=("FormulaComponentList"))

    # child relationships (access children)



class INVOICEFEE(Base):  # type: ignore
    __tablename__ = 'INVOICE_FEES'
    _s_collection_name = 'INVOICEFEE'  # type: ignore
    __table_args__ = (
        Index('INVOICE_FEES_INVOICE_ID', 'INVOICE_ID', 'COMPANY_ID', 'TYPE', 'INVOICE_DATE', 'TOTAL_AMOUNT', 'STATUS', 'BILL_TO_CO_ID', 'BILL_TO_PLANT_ID', unique=True),
    )

    INVOICE_ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False, index=True)
    TYPE = Column(String(4), nullable=False, index=True)
    INVOICE_TYPE = Column(String(20))
    INVOICE_DATE = Column(DateTime, index=True)
    FREQ = Column(String(20))
    TOTAL_AMOUNT = Column(MONEY)
    DATE_POSTED = Column(DateTime)
    STATUS = Column(String(20))
    REPLACED_BY = Column(Integer)
    PAYMENT = Column(MONEY)
    CHECK_NO = Column(String(255))
    CHECK_DATE = Column(DateTime)
    CHECK_RECEIVED = Column(DateTime)
    BILL_TO_CO_ID = Column(Integer)
    BILL_TO_PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), index=True)
    OK_TO_POST = Column(String(1))
    WHO = Column(String(40))
    REPLACEMENT_FOR = Column(Integer)
    BATCH_ID_S36 = Column(String(7))
    BATCH_DATE = Column(DateTime)
    TRANSFER_FLAG = Column(String(1))
    PRINT_FLAG = Column(String(1))
    HOLD_FLAG = Column(String(1))
    ATTACHED_LETTER = Column(String(20))
    TIMESTAMP = Column(BINARY(8))
    ID = Column(Integer)
    COMMENT = Column(String(255))
    INVOICE_LEVEL = Column(Integer)
    PurchaseOrder = Column(String(75), server_default=text("('')"))
    DeliveryMethod = Column(String(30), server_default=text("('')"))
    DeliveryDate = Column(Date)
    OriginalInvoiceAmount = Column(MONEY)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    achPaid = Column(Boolean, server_default=text("((0))"), nullable=False)
    BatchId = Column(Integer)
    PeriodStart = Column(DateTime)
    PeriodEnd = Column(DateTime)
    BalanceInAccounting : DECIMAL = Column(DECIMAL(18, 2), server_default=text("((0))"))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("INVOICEFEEList"))
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("INVOICEFEEList"))

    # child relationships (access children)



class LabelComment(Base):  # type: ignore
    __tablename__ = 'LabelComment'
    _s_collection_name = 'LabelComment'  # type: ignore

    ID = Column(Integer, server_default=text("0"), nullable=False)
    CommentID = Column(Integer, primary_key=True)
    LabelId = Column(ForeignKey('label_tb.ID'), nullable=False, index=True)
    CHANGESET_ID = Column(Integer, index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2],'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2],'9999-12-31 23:59:59.9999999'))"), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    Label : Mapped["LabelTb"] = relationship(back_populates=("LabelCommentList"))

    # child relationships (access children)



class LabelOption(Base):  # type: ignore
    __tablename__ = 'LabelOptions'
    _s_collection_name = 'LabelOption'  # type: ignore

    LabelID = Column(ForeignKey('label_tb.ID'), ForeignKey('label_tb.ID'), primary_key=True)
    IncludeInParentCompanyLOC = Column(String(1))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    label_tb : Mapped["LabelTb"] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates=("LabelOptionList"))
    label_tb1 : Mapped["LabelTb"] = relationship(foreign_keys='[LabelOption.LabelID]', back_populates=("LabelOptionList1"), overlaps="LabelOptionList,label_tb")

    # child relationships (access children)



class OWNSTB(Base):  # type: ignore
    __tablename__ = 'OWNS_TB'
    _s_collection_name = 'OWNSTB'  # type: ignore
    __table_args__ = (
        Index('setupby', 'STATUS', 'ACTIVE'),
        Index('XOWNS', 'PLANT_ID', 'STATUS', 'ID', 'ACTIVE', 'Setup_By'),
        Index('idxCompID', 'COMPANY_ID', 'ACTIVE', 'PLANT_ID', unique=True)
    )

    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False)
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    TYPE = Column(String(10))
    VISIT_FREQUENCY = Column(SmallInteger)
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
    VisitPOexpiry = Column(Date)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    BoilerplateInvoiceComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    IsCertBillingOverride = Column(Boolean, server_default=text("((0))"), nullable=False)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("OWNSTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("OWNSTBList"))
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(back_populates=("OWNSTBList"))

    # child relationships (access children)
    BillingList : Mapped[List["Billing"]] = relationship(back_populates="OWNS_TB")
    CompanyPlantOptionList : Mapped[List["CompanyPlantOption"]] = relationship(back_populates="OWNS_TB")
    PLANTFEESTRUCTUREList : Mapped[List["PLANTFEESTRUCTURE"]] = relationship(back_populates="OWNS_TB")
    PLANTHOLDTBList : Mapped[List["PLANTHOLDTB"]] = relationship(back_populates="OWNS_TB")
    PLANTSTATUSTBList : Mapped[List["PLANTSTATUSTB"]] = relationship(back_populates="OWNS_TB")
    PurchaseOrderList : Mapped[List["PurchaseOrder"]] = relationship(back_populates="OWNS_TB")
    ThirdPartyBillingCompanyList : Mapped[List["ThirdPartyBillingCompany"]] = relationship(back_populates="OWNS_TB")
    USEDIN1TBList : Mapped[List["USEDIN1TB"]] = relationship(back_populates="OWNS_TB")
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="OWNS_TB")
    ProductJobLineItemList : Mapped[List["ProductJobLineItem"]] = relationship(back_populates="OWNS_TB")



class PENDINGINFOTB(Base):  # type: ignore
    __tablename__ = 'PENDING_INFO_TB'
    _s_collection_name = 'PENDINGINFOTB'  # type: ignore
    __table_args__ = (
        Index('idx_CompanyID_PlantID', 'COMPANY_ID', 'PLANT_ID'),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    IINVOICEFEE = Column(String(25))
    IINVOICEEXPENSE = Column(String(25))
    IINVOICEDATE = Column(String(10))
    IINVOICENUMBER = Column(String(25))
    VOID = Column(String(1))
    PAID = Column(String(1))
    TERMSCERTFEE = Column(String(25))
    SPECIALCLAUSES = Column(String(255))
    ANNUALFEE = Column(String(25))
    ANNUALEXPENSES = Column(String(25))
    CINVOICEDATE = Column(String(10))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    ACTIVE = Column(Integer)
    IINVOICEAMOUNT = Column(String(25))
    PROEXPENSES = Column(String(25))
    PROFEE = Column(String(25))
    PRODATE = Column(String(10))
    CONTRACTFEE = Column(String(25))
    CONTRACTEXPENSE = Column(String(25))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PENDINGINFOTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PENDINGINFOTBList"))

    # child relationships (access children)



class PLANTADDRESSTB(Base):  # type: ignore
    __tablename__ = 'PLANT_ADDRESS_TB'
    _s_collection_name = 'PLANTADDRESSTB'  # type: ignore

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

    # child relationships (access children)



class PLANTCERTDETAIL(Base):  # type: ignore
    __tablename__ = 'PLANT_CERT_DETAIL'
    _s_collection_name = 'PLANTCERTDETAIL'  # type: ignore
    __table_args__ = (
        Index('IX_PLANT_CERT_DETAIL', 'COMPANY_ID', 'PLANT_ID', 'COMPANY_FEE_ID'),
    )

    ID = Column(Integer, primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False)
    COMPANY_FEE_ID = Column(Integer, nullable=False)
    CERT_DETAIL_SEQ_NUM = Column(SmallInteger, nullable=False)
    CERT_DETAIL_DESCRIPTION = Column(String(80))
    CERT_DETAIL_AMOUNT = Column(MONEY)
    CERT_DETAIL_DATE = Column(DateTime)
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

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    COMMENT_ID = Column(Integer, nullable=False)
    TIMESTAMP = Column(BINARY(8))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTCOMMENTList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTCOMMENTList"))

    # child relationships (access children)



class PLANTFEECOMMENT(Base):  # type: ignore
    __tablename__ = 'PLANT_FEE_COMMENT'
    _s_collection_name = 'PLANTFEECOMMENT'  # type: ignore
    __table_args__ = (
        Index('XPKPLANT_FEE_COMMENT', 'COMPANY_ID', 'PLANT_ID', 'PLANT_FEE_ID', 'COMMENT_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    PLANT_FEE_ID = Column(Integer)
    COMMENT_ID = Column(Integer, nullable=False)
    Type = Column(String(25))
    Expires = Column(DateTime)
    RfrPay : DECIMAL = Column(DECIMAL(19, 4))
    BillingCompanyFee : DECIMAL = Column(DECIMAL(19, 4))
    VisitType = Column(String(255))
    CHANGESET_ID = Column(Integer)
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTFEECOMMENTList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTFEECOMMENTList"))

    # child relationships (access children)



class PLANTFEESTRUCTUREOUT(Base):  # type: ignore
    __tablename__ = 'PLANT_FEE_STRUCTURE_OUT'
    _s_collection_name = 'PLANTFEESTRUCTUREOUT'  # type: ignore
    __table_args__ = (
        Index('PlantCompanyPersonNoDups', 'PLANT_ID', 'PERSON_JOB_ID', 'COMPANY_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PERSON_JOB_ID = Column(Integer)
    OUT_VISIT_FEE_TYPEx = Column(String(20))
    OUT_VISIT_FEEx = Column(MONEY)
    OUT_FREE_VISITS_NUM = Column(Integer)
    OUT_VISIT_FEE1 = Column(MONEY)
    OUT_FREE_VISITS_NUM1 = Column(Integer)
    OUT_VISIT_FEE2 = Column(MONEY)
    OUT_FREE_VISITS_NUM2 = Column(Integer)
    OUT_FREE_VISITS_OVERNIGHTPAY = Column(MONEY)
    OUT_SPECIAL_PRODUCTION_TYPEx = Column(String(20))
    OUT_SPECIAL_PRODUCTION_FEEx = Column(SMALLMONEY)
    OUT_UNIT_BASE = Column(Integer)
    OUT_SPECIAL_PRODUCTION_FEE1 = Column(SMALLMONEY)
    OUT_UNIT_BASE1 = Column(Integer)
    OUT_SPECIAL_PRODUCTION_FEE2 = Column(SMALLMONEY)
    OUT_UNIT_BASE2 = Column(Integer)
    OUT_SPEC_PRODN_OVERNIGHTPAY = Column(MONEY)
    OUT_PASSOVER_FEE_TYPEx = Column(String(25))
    OUT_PASSOVER_RATE_FEE1x = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE1 = Column(Integer)
    OUT_PASSOVER_RATE_FEE2 = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE2 = Column(Integer)
    OUT_PASSOVER_RATE_FEE3 = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE3 = Column(Integer)
    OUT_PASSOVER_OVERNIGHTPAY = Column(MONEY)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTFEESTRUCTUREOUTList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTFEESTRUCTUREOUTList"))

    # child relationships (access children)
    BillingList : Mapped[List["Billing"]] = relationship(back_populates="PLANT_FEE_STRUCTURE_OUT")



class PLANTOTHERNAME(Base):  # type: ignore
    __tablename__ = 'PLANT_OTHER_NAMES'
    _s_collection_name = 'PLANTOTHERNAME'  # type: ignore
    __table_args__ = (
        Index('XPKPLANT_OTHER_NAMES', 'PLANT_ID', 'ALIAS_ID'),
    )

    ID = Column(Integer)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    ALIAS_ID = Column(Integer, primary_key=True)
    TIMESTAMP = Column(BINARY(8))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTOTHERNAMEList"))

    # child relationships (access children)



class PRIVATELABELBILL(Base):  # type: ignore
    __tablename__ = 'PRIVATE_LABEL_BILL'
    _s_collection_name = 'PRIVATELABELBILL'  # type: ignore
    __table_args__ = (
        Index('PRVT_CO', 'COMPANY_ID', 'SRC_MAR_ID', unique=True),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True, index=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    SRC_MAR_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    MAN_ENTERED = Column(Boolean, nullable=False)
    DATE_UPDATE = Column(DateTime)
    PRIV_LABEL_FEE = Column(MONEY)
    BILL_TO_CO_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), index=True)
    BILL_TO_PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    PRO_RATED = Column(MONEY)
    TIMESTAMP = Column(BINARY(8))
    LAST_BIILED = Column(DateTime)
    AGREEMENT_RECEIVED_DATE = Column(DateTime)
    CHANGESET_ID = Column(Integer, index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(foreign_keys='[PRIVATELABELBILL.BILL_TO_CO_ID]', back_populates=("PRIVATELABELBILLList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PRIVATELABELBILLList"))
    COMPANY_TB1 : Mapped["COMPANYTB"] = relationship(foreign_keys='[PRIVATELABELBILL.COMPANY_ID]', back_populates=("PRIVATELABELBILLList1"))
    COMPANY_TB2 : Mapped["COMPANYTB"] = relationship(foreign_keys='[PRIVATELABELBILL.SRC_MAR_ID]', back_populates=("PRIVATELABELBILLList2"))

    # child relationships (access children)



class VISIT(Base):  # type: ignore
    __tablename__ = 'VISITS'
    _s_collection_name = 'VISIT'  # type: ignore
    __table_args__ = (
        Index('GroupTicketsNew', 'MainVisit', 'VISIT_ID'),
        Index('TripDate', 'TRIP_ID', 'ACTUAL_VISIT_DATE'),
        Index('tripID', 'VISIT_ID', 'TRIP_ID'),
        Index('apBatch', 'AP_BATCH', 'VISIT_ID'),
        Index('GroupTickets', 'VISIT_PURPOSE', 'VISIT_ID')
    )

    VISIT_ID = Column(Integer, server_default=text("0"), primary_key=True)
    ASSIGNMENT_DATE = Column(DateTime, server_default=text("(getdate())"), index=True)
    VISIT_TYPE = Column(String(40), nullable=False)
    VISIT_PURPOSE = Column(String(500))
    DESTINATION_TYPE = Column(String(1), server_default=text("('P')"), nullable=False)
    DESTINATION_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), index=True)
    VISIT_FOR_TYPE = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'), server_default=text("('C')"))
    VISIT_FOR_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), index=True)
    BILL_TO_TYPE = Column(String(1))
    BILL_TO_ID = Column(Integer)
    PERIOD = Column(String(20))
    PERIOD_START_DATE = Column(SMALLDATETIME, server_default=text("(getdate())"))
    PERIOD_END_DATE = Column(SMALLDATETIME)
    ACTUAL_VISIT_DATE = Column(SMALLDATETIME, index=True)
    ACTUAL_VISIT_DAYS = Column(Float(24), server_default=text("((1))"))
    ASSIGNED_PERSON_JOB_ID = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'), nullable=False, index=True)
    ACTUAL_PERSON_JOB_ID = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    DEFAULT_BILL_AMOUNT = Column(SMALLMONEY, server_default=text("((0))"))
    DEFAULT_EXPENSES = Column(String(10), server_default=text("((0))"))
    DEFAULT_PAYMENT_AMOUNY = Column(SMALLMONEY, server_default=text("((0))"))
    OU_RENTAL_CAR = Column(SMALLMONEY, server_default=text("((0))"))
    OU_PLANE = Column(SMALLMONEY, server_default=text("((0))"))
    OU_OTHER = Column(SMALLMONEY, server_default=text("((0))"))
    OU_Mileage_Differential = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_EXPENSES_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_MASHGIACH_PAY = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_MASHGIACH_EXPENSE = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_MASHGIACH_ADVANCES = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_BILLABLE_FEE = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_BILLABLE_EXPENSES = Column(SMALLMONEY, server_default=text("((0))"))
    TOTAL_BILLABLE_PAYMENT = Column(SMALLMONEY, server_default=text("((0))"))
    PAY_TYPE = Column(String(20), server_default=text("('Per Visit')"))
    PAY_AMOUNT = Column(SMALLMONEY, server_default=text("((0))"))
    PAY_OVERTIME = Column(SMALLMONEY, server_default=text("((0))"))
    PAY_OVERNIGHT = Column(SMALLMONEY, server_default=text("((0))"))
    NUMBER_SHIFTS = Column(Float(24), server_default=text("((1))"))
    PAY_TOTAL = Column(SMALLMONEY, server_default=text("((0))"))
    MILEAGE_NOT_PAID = Column(Float(53), server_default=text("((0))"))
    RATE_PER_MILEAGE = Column(SMALLMONEY, server_default=text("((0))"))
    PLANE_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    RENTAL_CAR_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    TOLLS_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    PARKING_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    GAS_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    TAXI_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    MOTEL_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    TELEPHONE_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    MISC_NOT_PAID = Column(SMALLMONEY, server_default=text("((0))"))
    BILLABLE_FEE = Column(SMALLMONEY, server_default=text("((0))"))
    BILLABLE_OVERTIME_FEE = Column(SMALLMONEY, server_default=text("((0))"))
    BILLABLE_OVERNIGHT_FEE = Column(SMALLMONEY, server_default=text("((0))"))
    APPROVAL = Column(String(1))
    APPROVAL_DATE = Column(DateTime)
    APPROVAL_PERSON_ID = Column(Integer)
    INV_ID = Column(Integer)
    TRIP_ID = Column(Float(24))
    GP_BILL_TO_ID = Column(String(7))
    GP_GO = Column(Boolean, server_default=text("((0))"))
    AP_BATCH = Column(Integer)
    AP_DATE = Column(DateTime, index=True)
    AP_DONE = Column(Boolean, server_default=text("((0))"))
    AR_BATCH = Column(Integer)
    AR_DATE = Column(DateTime)
    AR_DONE = Column(Boolean, server_default=text("((0))"))
    PAY_BATCH = Column(Integer)
    PAY_DATE = Column(DateTime)
    PAY_DONE = Column(Boolean, server_default=text("((0))"))
    GL_BATCH = Column(Integer)
    GL_DATE = Column(DateTime)
    GL_DONE = Column(Boolean, server_default=text("((0))"))
    ID = Column(Integer)
    NUMBER_OVERTIME_SHIFTS = Column(SmallInteger)
    NO_OVERTIME_HRS = Column(SMALLMONEY)
    ACTUAL_MASH_COST = Column(String(20))
    AssignmentID = Column(Integer)
    OnHold = Column(DateTime)
    ProcessedBy = Column(String(50))
    VisitStatus = Column(String(25), server_default=text("('')"), index=True)
    CreatedBy = Column(String(100), server_default=text("(suser_sname())"))
    CreatedDate = Column(DateTime, server_default=text("(getdate())"))
    PurchaseOrder = Column(String(75))
    OnHoldModifiedBy = Column(String(100))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    TeamId = Column(Integer)
    MainVisit = Column(ForeignKey('VISITS.VISIT_ID'), index=True)
    TotalVisitsInTrip = Column(Integer)

    # parent relationships (access parent)
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[VISIT.ACTUAL_PERSON_JOB_ID]', back_populates=("VISITList"))
    PERSON_JOB_TB1 : Mapped["PERSONJOBTB"] = relationship(foreign_keys='[VISIT.ASSIGNED_PERSON_JOB_ID]', back_populates=("VISITList1"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("VISITList"))
    VISIT : Mapped["VISIT"] = relationship(remote_side=[VISIT_ID], back_populates=("VISITList"))
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("VISITList"))

    # child relationships (access children)
    VISITList : Mapped[List["VISIT"]] = relationship(back_populates="VISIT")



class LabelBarcode(Base):  # type: ignore
    __tablename__ = 'label_barcode'
    _s_collection_name = 'LabelBarcode'  # type: ignore

    labelId = Column(ForeignKey('label_tb.ID'), primary_key=True, nullable=False)
    barcodeId = Column(ForeignKey('BarCode.Id'), primary_key=True, nullable=False)
    type = Column(String(100))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    barcode : Mapped["BarCode"] = relationship(back_populates=("LabelBarcodeList"))
    label : Mapped["LabelTb"] = relationship(back_populates=("LabelBarcodeList"))

    # child relationships (access children)



class Billing(Base):  # type: ignore
    __tablename__ = 'Billing'
    _s_collection_name = 'Billing'  # type: ignore

    Id = Column(Integer, server_default=text("0"), primary_key=True)
    Kind = Column(String(255))
    VisitType = Column(String(50))
    PayType = Column(String(50))
    Amount = Column(SMALLMONEY, server_default=text("((0))"), nullable=False)
    VirtualAmount = Column(SMALLMONEY, server_default=text("((0))"), nullable=False)
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'))
    PFSO_ID = Column(ForeignKey('PLANT_FEE_STRUCTURE_OUT.ID'))

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("BillingList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("BillingList"))
    PLANT_FEE_STRUCTURE_OUT : Mapped["PLANTFEESTRUCTUREOUT"] = relationship(back_populates=("BillingList"))

    # child relationships (access children)



class CompanyPlantOption(Base):  # type: ignore
    __tablename__ = 'CompanyPlantOptions'
    _s_collection_name = 'CompanyPlantOption'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    Company_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    Plant_id = Column(ForeignKey('PLANT_TB.PLANT_ID'))
    OwnsID = Column(ForeignKey('OWNS_TB.ID'))
    OptionName = Column(String(75))
    OptionValue = Column(String(75))
    OptIn = Column(String(1))
    rcApproved = Column(String(1))
    glApproved = Column(String(1))
    ModifiedBy = Column(String(250), server_default=text("(suser_sname())"))
    ModifiedDate = Column(DateTime, server_default=text("(getdate())"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("CompanyPlantOptionList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("CompanyPlantOptionList"))
    Plant : Mapped["PLANTTB"] = relationship(back_populates=("CompanyPlantOptionList"))

    # child relationships (access children)



class FormulaSubmissionComponent(Base):  # type: ignore
    __tablename__ = 'FormulaSubmissionComponents'
    _s_collection_name = 'FormulaSubmissionComponent'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
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

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    FormulaSubmissionID = Column(Integer, nullable=False)
    PlantName = Column(String(100))
    PlantCode = Column(String(100))
    Owns_ID = Column(Integer)
    ActionTaken = Column(String(500))
    ProductionMode = Column(String(50))

    # parent relationships (access parent)

    # child relationships (access children)
    ProducedIn1TbList : Mapped[List["ProducedIn1Tb"]] = relationship(back_populates="FormulaSubmissionPlant")



class PLANTFEESTRUCTURE(Base):  # type: ignore
    __tablename__ = 'PLANT_FEE_STRUCTURE'
    _s_collection_name = 'PLANTFEESTRUCTURE'  # type: ignore

    ID = Column(Integer, primary_key=True)
    PLANT_ID = Column(Integer)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    COMPANY_FEE_ID = Column(SmallInteger, server_default=text("((1))"))
    EFFECTIVE_DATE = Column(DateTime)
    APPROVAL = Column(String(1), server_default=text("((0))"))
    APPROVAL_DATE = Column(DateTime)
    APPROVAL_PERSON_ID = Column(Integer)
    IN_CERT_FEE = Column(MONEY)
    IN_EXPENSE_TYPE = Column(String(15))
    IN_EXPENSE_AMT = Column(MONEY)
    IN_EXPENSE_PERCENT = Column(Float(53))
    IN_VISIT_FEE_TYPEx = Column(String(20))
    IN_FREE_VISITS_NUM = Column(Integer)
    IN_VISIT_FEEx = Column(MONEY)
    IN_SPECIAL_PRODUCTION_TYPEx = Column(String(20))
    IN_SPECIAL_PRODUCTION_FEEx = Column(SMALLMONEY)
    IN_UNIT_BASE = Column(Integer)
    IN_PASSOVER_FEE_TYPEx = Column(String(25))
    IN_PASSOVER_FEEx = Column(SMALLMONEY)
    IN_PASSOVER_VISIT_FEE = Column(SMALLMONEY)
    IN_PASSOVER_UNIT_RATE = Column(SMALLMONEY)
    IN_PASSOVER_UNIT_BASE = Column(String(20))
    IN_PRIVATE_LABEL_TYPE = Column(String(20))
    IN_PRIVATE_LABEL_FEE1 = Column(SMALLMONEY)
    IN_PRIVATE_LABEL_BASE1 = Column(Integer)
    IN_PRIVATE_LABEL_FEE2 = Column(SMALLMONEY)
    IN_PRIVATE_LABEL_BASE2 = Column(Integer)
    IN_PRIVATE_LABEL_FEE3 = Column(SMALLMONEY)
    IN_PRIVATE_LABEL_BASE3 = Column(Integer)
    IN_SPECIAL_PRODUCTION_FEE1 = Column(SMALLMONEY)
    IN_UNIT_BASE1 = Column(Integer)
    IN_SPECIAL_PRODUCTION_FEE2 = Column(SMALLMONEY)
    IN_UNIT_BASE2 = Column(Integer)
    IN_VISIT_FEE1 = Column(MONEY)
    IN_FREE_VISITS_NUM1 = Column(Integer)
    IN_VISIT_FEE2 = Column(MONEY)
    IN_FREE_VISITS_NUM2 = Column(Integer)
    IN_CERT_FREQ = Column(String(20))
    IN_CERT_DATE = Column(DateTime)
    IN_PASSOVER_RATE_FEE1 = Column(SMALLMONEY)
    IN_PASSOVER_FOR_FEE1 = Column(Integer)
    IN_PASSOVER_RATE_FEE2 = Column(SMALLMONEY)
    IN_PASSOVER_FOR_FEE2 = Column(Integer)
    IN_PASSOVER_RATE_FEE3 = Column(SMALLMONEY)
    IN_PASSOVER_FOR_FEE3 = Column(Integer)
    IN_BILL_REG_VISIT_TYPEx = Column(String(20))
    IN_BILL_REG_VISIT_AMTx = Column(String(20))
    IN_BILL_SPEC_PROD_TYPEx = Column(String(20))
    IN_BILL_SPEC_PROD_AMTx = Column(String(20))
    IN_BILL_PASSOVER_TYPEx = Column(String(20), server_default=text("('Percent')"))
    IN_BILL_PASSOVER_AMTx = Column(String(20), server_default=text("((100))"))
    OUT_CERT_FEE = Column(MONEY)
    OUT_EXPENSE_TYPE = Column(String(15))
    OUT_EXPENSE_AMT = Column(MONEY)
    OUT_EXPENSE_PERCENT = Column(Float(53))
    OUT_VISIT_FEE_TYPE = Column(String(20))
    OUT_FREE_VISITS_NUM = Column(Integer)
    OUT_VISIT_FEE = Column(MONEY)
    OUT_SPECIAL_PRODUCTION_TYPE = Column(String(20))
    OUT_SPECIAL_PRODUCTION_FEE = Column(SMALLMONEY)
    OUT_UNIT_BASE = Column(Integer)
    OUT_PASSOVER_FEE_TYPE = Column(String(25))
    OUT_PASSOVER_FEE = Column(SMALLMONEY)
    OUT_PASSOVER_VISIT_FEE = Column(SMALLMONEY)
    OUT_PASSOVER_UNIT_RATE = Column(SMALLMONEY)
    OUT_PASSOVER_UNIT_BASE = Column(String(20))
    OUT_PRIVATE_LABEL_TYPE = Column(String(20))
    OUT_PRIVATE_LABEL_FEE1 = Column(SMALLMONEY)
    OUT_PRIVATE_LABEL_BASE1 = Column(Integer)
    OUT_PRIVATE_LABEL_FEE2 = Column(SMALLMONEY)
    OUT_PRIVATE_LABEL_BASE2 = Column(Integer)
    OUT_PRIVATE_LABEL_FEE3 = Column(SMALLMONEY)
    OUT_PRIVATE_LABEL_BASE3 = Column(Integer)
    OUT_SPECIAL_PRODUCTION_FEE1 = Column(SMALLMONEY)
    OUT_UNIT_BASE1 = Column(Integer)
    OUT_SPECIAL_PRODUCTION_FEE2 = Column(SMALLMONEY)
    OUT_UNIT_BASE2 = Column(Integer)
    OUT_VISIT_FEE1 = Column(MONEY)
    OUT_FREE_VISITS_NUM1 = Column(Integer)
    OUT_VISIT_FEE2 = Column(MONEY)
    OUT_FREE_VISITS_NUM2 = Column(Integer)
    OUT_CERT_FREQ = Column(String(20))
    OUT_CERT_DATE = Column(DateTime)
    OUT_PASSOVER_RATE_FEE1 = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE1 = Column(Integer)
    OUT_PASSOVER_RATE_FEE2 = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE2 = Column(Integer)
    OUT_PASSOVER_RATE_FEE3 = Column(SMALLMONEY)
    OUT_PASSOVER_FOR_FEE3 = Column(Integer)
    OUT_BILL_REG_VISIT_TYPE = Column(String(20))
    OUT_BILL_REG_VISIT_AMT = Column(String(20))
    OUT_BILL_SPEC_PROD_TYPE = Column(String(20))
    OUT_BILL_SPEC_PROD_AMT = Column(String(20))
    OUT_BILL_PASSOVER_TYPE = Column(String(20))
    OUT_BILL_PASSOVER_AMT = Column(String(20))
    OUT_FREE_VISITS_OVERNIGHTPAY = Column(MONEY)
    OUT_SPECIAL_PRODN_OVERNIGHTPAY = Column(MONEY)
    OUT_PASSOVER_RATE_OVERNIGHTPAY = Column(MONEY)
    PERSON_JOB_ID = Column(Integer)
    OwnsID = Column(ForeignKey('OWNS_TB.ID'), unique=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTFEESTRUCTUREList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("PLANTFEESTRUCTUREList"))

    # child relationships (access children)



class PLANTHOLDTB(Base):  # type: ignore
    __tablename__ = 'PLANT_HOLD_TB'
    _s_collection_name = 'PLANTHOLDTB'  # type: ignore
    __table_args__ = (
        Index('idx_Comp_Plant', 'COMPANY_ID', 'PLANT_ID'),
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'), nullable=False)
    PLANT_ID = Column(ForeignKey('PLANT_TB.PLANT_ID'), nullable=False)
    HOLD_SEQ_NUM = Column(SmallInteger, nullable=False)
    HOLD_TYPE = Column(String(4), nullable=False)
    START_PERSON_ID = Column(String(30), nullable=False)
    START_DATE = Column(DateTime)
    START_REASON = Column(String(100))
    END_PERSON_ID = Column(String(30))
    END_DATE = Column(DateTime)
    END_REASON = Column(String(100))
    TIMESTAMP = Column(BINARY(8))
    ACTIVE = Column(Integer)
    OwnsID = Column(ForeignKey('OWNS_TB.ID'), index=True)
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PLANTHOLDTBList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("PLANTHOLDTBList"))
    PLANT_TB : Mapped["PLANTTB"] = relationship(back_populates=("PLANTHOLDTBList"))

    # child relationships (access children)



t_PLANT_INSPECTION_TB = Table(
    'PLANT_INSPECTION_TB', metadata,
    Column('COMPANY_ID', Integer, nullable=False),
    Column('PLANT_ID', Integer, nullable=False),
    Column('OWNS_ID', ForeignKey('OWNS_TB.ID')),
    Column('QUESTION_ID', Float(24), nullable=False),
    Column('DESCRIPTION', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('WHO', String(40, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DATE_POSTED', DateTime),
    Column('ID', Integer, nullable=False),
    Column('ACTIVE', Integer),
    Index('PLANT_INSPECTION_1', 'COMPANY_ID', 'PLANT_ID', 'ID')
)


class PLANTSTATUSTB(Base):  # type: ignore
    __tablename__ = 'PLANT_STATUS_TB'
    _s_collection_name = 'PLANTSTATUSTB'  # type: ignore
    __table_args__ = (
        Index('PlantCompanyStatusSeqNum', 'OwnsID', 'COMPANY_ID', 'PLANT_ID', 'ACTIVE'),
        Index('ID', 'COMPANY_ID', 'PLANT_ID', 'ID'),
        Index('XPKPLANT_STATUS', 'ID', 'COMPANY_ID', 'PLANT_ID', 'STATUS', 'START_DATE', 'ACTIVE', 'DateDone', 'OwnsID', unique=True)
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True, index=True)
    COMPANY_ID = Column(Integer, nullable=False)
    PLANT_ID = Column(Integer, nullable=False)
    ROLE = Column(String(1, 'SQL_Latin1_General_CP1_CI_AS'))
    STATUS = Column(String(25, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    START_DATE = Column(DateTime)
    START_PERSON_ID = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text("('')"), nullable=False)
    START_REASON = Column(String(120, 'SQL_Latin1_General_CP1_CI_AS'))
    END_DATE = Column(DateTime)
    END_PERSON_ID = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'))
    END_REASON = Column(String(80, 'SQL_Latin1_General_CP1_CI_AS'))
    ACTIVE = Column(Integer)
    DateDone = Column(SMALLDATETIME, server_default=text("(getdate())"))
    OwnsID = Column(ForeignKey('OWNS_TB.ID'), server_default=text("((0))"))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("PLANTSTATUSTBList"))

    # child relationships (access children)



class PurchaseOrder(Base):  # type: ignore
    __tablename__ = 'PurchaseOrder'
    _s_collection_name = 'PurchaseOrder'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    discriminator = Column(Unicode(255))
    PO = Column(String(255))
    Expires = Column(DATETIME2)
    FeeType = Column(String(255), nullable=False)
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    Required = Column(Boolean, server_default=text("((0))"), nullable=False)
    Inherits = Column(Boolean, server_default=text("((0))"), nullable=False)
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("PurchaseOrderList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("PurchaseOrderList"))

    # child relationships (access children)



class ThirdPartyBillingCompany(Base):  # type: ignore
    __tablename__ = 'ThirdPartyBillingCompany'
    _s_collection_name = 'ThirdPartyBillingCompany'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    Dis = Column(String(1))
    Name = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    Account = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    Comments = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    DeliveryNote = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'))
    COMPANY_ID = Column(ForeignKey('COMPANY_TB.COMPANY_ID'))
    ValidFromTime = Column(DATETIME2, nullable=False)
    ValidToTime = Column(DATETIME2, nullable=False)
    CHANGESET_ID = Column(Integer, index=True)

    # parent relationships (access parent)
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("ThirdPartyBillingCompanyList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("ThirdPartyBillingCompanyList"))

    # child relationships (access children)



class USEDIN1TB(Base):  # type: ignore
    __tablename__ = 'USED_IN1_TB'
    _s_collection_name = 'USEDIN1TB'  # type: ignore
    __table_args__ = (
        Index('IdxUsedInLabelIdOwnsIdUidActive', 'LabelID', 'OWNS_ID', 'ID', 'ACTIVE'),
        Index('idxLabelID', 'LabelID', 'OWNS_ID'),
        Index('ix_USED_IN1_TB_ACTIVE_LineItem_includes', 'ACTIVE', 'LineItem'),
        Index('idxSubmissionDetail', 'JobID', 'LineItem', 'ACTIVE')
    )

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    BRAND_NAME = Column(String(100))
    PROC_LINE_ID = Column(Integer)
    START_DATE = Column(SMALLDATETIME, server_default=text("(getdate())"))
    END_DATE = Column(DateTime)
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
    LineItem = Column(SmallInteger, index=True)
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
    COMPANY_TB : Mapped["COMPANYTB"] = relationship(back_populates=("USEDIN1TBList"))
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("USEDIN1TBList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("USEDIN1TBList"))

    # child relationships (access children)



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

    ID = Column(Integer, server_default=text("0"), primary_key=True, index=True)
    PROC_LINE_ID = Column(Integer, server_default=text("((1))"))
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    REGULAR = Column(String(1), server_default=text("('')"))
    SPECIAL = Column(String(1))
    PASSOVER = Column(String(20))
    PRIVATE_LABEL_FEE = Column(SMALLMONEY)
    TIMESTAMP = Column(BINARY(8))
    STATUS = Column(String(20))
    SPECIAL_STATUS_1 = Column(String(40), server_default=text("('')"))
    RC_1 = Column(String(80))
    DATE_1 = Column(DateTime)
    SPECIAL_STATUS_2 = Column(String(40), server_default=text("('')"))
    RC_2 = Column(String(80))
    DATE_2 = Column(DateTime)
    SPECIAL_STATUS_3 = Column(String(40), server_default=text("('')"))
    RC_3 = Column(String(80))
    DATE_3 = Column(DateTime)
    SPECIAL_STATUS_4 = Column(String(40), server_default=text("('')"))
    RC_4 = Column(String(80))
    DATE_4 = Column(DateTime)
    ACTIVE = Column(Integer)
    OWNS_ID = Column(ForeignKey('OWNS_TB.ID'), index=True)
    DATE_CERTIFIED = Column(SMALLDATETIME)
    DATE_LAST_REV = Column(SMALLDATETIME)
    CREATE_DATE = Column(DateTime, server_default=text("(getdate())"), index=True)
    CREATED_BY = Column(String(75))
    MODIFIED_DATE = Column(DateTime)
    MODIFIED_BY = Column(String(75))
    DIST = Column(Boolean)
    MEHADRIN = Column(Boolean)
    LOTNUM = Column(String(500))
    LabelID = Column(ForeignKey('label_tb.ID'))
    FormulaSubmissionPlantID = Column(ForeignKey('FormulaSubmissionPlants.ID'))
    ProductPlantsID = Column(Integer)
    BatchSheetName = Column(String(40))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    LatestPesachSeason = Column(Integer)

    # parent relationships (access parent)
    FormulaSubmissionPlant : Mapped["FormulaSubmissionPlant"] = relationship(back_populates=("ProducedIn1TbList"))
    label_tb : Mapped["LabelTb"] = relationship(back_populates=("ProducedIn1TbList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("ProducedIn1TbList"))

    # child relationships (access children)
    ProductJobLineItemList : Mapped[List["ProductJobLineItem"]] = relationship(back_populates="pr")



class ProductJobLineItem(Base):  # type: ignore
    __tablename__ = 'ProductJobLineItems'
    _s_collection_name = 'ProductJobLineItem'  # type: ignore

    ID = Column(Integer, server_default=text("0"), primary_key=True)
    JobID = Column(String(50), index=True)
    LineItem = Column(Integer)
    RequestedLabelName = Column(Unicode(225))
    RequestedBrand = Column(Unicode(100))
    RequestedLabelNumber = Column(Unicode(25))
    WorkflowStatus = Column(String(50), server_default=text("('Open')"))
    LineItemComment = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    prid = Column(ForeignKey('produced_in1_tb.ID'))
    AssignedTo = Column(ForeignKey('PERSON_JOB_TB.PERSON_JOB_ID'))
    ownsID = Column(ForeignKey('OWNS_TB.ID'))
    requestedProductNumber = Column(String(50))
    requestedProductName = Column(String(1000))
    requestedSymbol = Column(String(20))
    requestedDPM = Column(String(20))
    requestedGRP = Column(String(20))
    requestedConsumer = Column(String(2))
    requestedIndustrial = Column(String(2))
    requestedPesach = Column(String(2))
    requestedSealSign = Column(String(100))
    requestedStipulation = Column(String(1000))
    requestedCommentsScheduleB = Column(String(1000))
    requestedConfidential = Column(String(50))
    requestedLabelType = Column(String(20))
    requestedCategory = Column(String(255))
    requestedShipping = Column(String(100))
    requestedTerminationDate = Column(DateTime)
    requestedForInternalUseOnly = Column(Integer)
    LineInstructions = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ProductInCartID = Column(Integer)
    requestedAgencyID = Column(String(50))
    PreSubmissionProductApproved = Column(String(1))
    ProductValidationComments = Column(String(300))
    DistributorName = Column(String(250))
    DistributorAddress = Column(String(400))
    DistributorContactName = Column(String(100))
    DistributorContactEmail = Column(String(100))
    DistributorContactPhone = Column(String(100))
    ValidFromTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'1900-01-01 00:00:00'))"), nullable=False)
    ValidToTime = Column(DATETIME2, server_default=text("(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"), nullable=False)
    CHANGESET_ID = Column(Integer, index=True)
    coPackProductPL = Column(Boolean, server_default=text("((0))"), nullable=False)
    barcodes = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ingredientsAllApproved = Column(Boolean, server_default=text("((0))"))
    oldPrid = Column(Integer)

    # parent relationships (access parent)
    PERSON_JOB_TB : Mapped["PERSONJOBTB"] = relationship(back_populates=("ProductJobLineItemList"))
    OWNS_TB : Mapped["OWNSTB"] = relationship(back_populates=("ProductJobLineItemList"))
    pr : Mapped["ProducedIn1Tb"] = relationship(back_populates=("ProductJobLineItemList"))

    # child relationships (access children)
