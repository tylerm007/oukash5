# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, LargeBinary, String, TEXT, Unicode, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import DATETIME2
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



class SubmissionApplication(Base):  # type: ignore
    __tablename__ = 'SubmissionApplication'
    _s_collection_name = 'submission-SubmissionApplication'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["whatWould", "pleaseSpecify"]  # TEXT(max) columns excluded from list responses

    SubmissionAppId = Column(Integer, autoincrement=True, primary_key=True)
    submission_id = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    submission_date = Column(DateTime, server_default=text("getdate()"))
    OUcertified = Column(Boolean, server_default=text("0"))
    everCertified = Column(Boolean, server_default=text("0"))
    agencyName = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyName = Column(Unicode(150, 'SQL_Latin1_General_CP1_CI_AS'))
    companyAddress = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    companyAddress2 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    companyCity = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyCountry = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyState = Column(Unicode(25, 'SQL_Latin1_General_CP1_CI_AS'))
    companyRegion = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyProvince = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyPhone = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ZipPostalCode = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    companyWebsite = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    IsPrimaryContact = Column(Boolean, server_default=text("1"))
    contactFirst = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactLast = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactPhone = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    contactEmail = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    billingContact = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    billingContactFirst = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    billingContactLast = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    billingContactPhone = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    billingContactEmail = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    jobTitle = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactFirst1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactLast1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactPhone1 = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    contactEmail1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    jobTitle1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    whatWould = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    whichCategory = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    whereDidHear = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    pleaseSpecify = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    copack = Column(Unicode(25, 'SQL_Latin1_General_CP1_CI_AS'))
    listInCopack = Column(Boolean, server_default=text("0"))
    veganCert = Column(Boolean, server_default=text("0"))
    areThere = Column(Boolean, server_default=text("0"))
    numberOfPlants = Column(Integer, server_default=text("1"))
    plant1Location = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    formName = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    language = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    status = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text("('New')"))
    kashrusLink = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    submissionurl = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)

    # child relationships (access children)
    SubmissionFileLinkList : Mapped[List["SubmissionFileLink"]] = relationship(back_populates="SubmissionApp")
    SubmissionFileList : Mapped[List["SubmissionFile"]] = relationship(back_populates="SubmissionApp")
    SubmissionMatcherList : Mapped[List["SubmissionMatcher"]] = relationship(back_populates="SubmissionApp")
    SubmissionPlantList : Mapped[List["SubmissionPlant"]] = relationship(back_populates="SubmissionApp")
    SubmissionRawDatumList : Mapped[List["SubmissionRawDatum"]] = relationship(back_populates="SubmissionApp")
    SubmissionRequestList : Mapped[List["SubmissionRequest"]] = relationship(back_populates="SubmissionApp")
    SubmissionValidationList : Mapped[List["SubmissionValidation"]] = relationship(back_populates="SubmissionApp")


class SubmissionFileLink(Base):  # type: ignore
    __tablename__ = 'SubmissionFileLinks'
    _s_collection_name = 'submission-SubmissionFileLink'  # type: ignore
    __bind_key__ = 'submission'

    FileLinkId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    productFileURL = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientURL = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    productFileURL1 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientURL1 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    productFileURL2 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientURL2 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    productFileURL3 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientURL3 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    productFileURL4 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientURL4 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionFileLinkList"))

    # child relationships (access children)



class SubmissionFile(Base):  # type: ignore
    __tablename__ = 'SubmissionFiles'
    _s_collection_name = 'submission-SubmissionFile'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["Content"]  # TEXT(max) binary content excluded from list responses

    FileId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    fileName = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    fileLURL = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    fileType = Column(Unicode(6, 'SQL_Latin1_General_CP1_CI_AS'))
    fileSize = Column(Integer)
    Content = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    uploadDate = Column(DateTime, server_default=text("getdate()"))

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionFileList"))

    # child relationships (access children)



class SubmissionMatcher(Base):  # type: ignore
    __tablename__ = 'SubmissionMatcher'
    _s_collection_name = 'submission-SubmissionMatcher'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["SubbmissionMatches"]  # TEXT(max) column excluded from list responses

    SubmissionMatcherId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    SubmissionType = Column(Unicode(10, 'SQL_Latin1_General_CP1_CI_AS'))
    SubmissionKey = Column(Integer)
    SubbmissionMatches = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    SelectedMatch = Column(Integer)

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionMatcherList"))

    # child relationships (access children)



class SubmissionPlant(Base):  # type: ignore
    __tablename__ = 'SubmissionPlant'
    _s_collection_name = 'submission-SubmissionPlant'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["brieflySummarize", "productDesc", "otherProductCompany"]  # TEXT(max) columns excluded from list responses

    PlantId = Column(Integer, autoincrement=True, primary_key=True)
    plantNumber = Column(Integer, nullable=False)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    plantName = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    plantAddress = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    plantAddress1 = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    plantCity = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    plantState = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    plantZip = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    plantCountry = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    plantRegion = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    plantProvince = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    contactSameAsCompany = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactFirst = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactLast = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactPhone = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    contactEmail = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    jobTitle = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactFirst1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactLast1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    contactPhone1 = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    contactEmail1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    jobTitle1 = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    majorCity = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    brieflySummarize = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    productDesc = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    otherProducts = Column(Boolean, server_default=text("1"))
    areAny = Column(Boolean, server_default=text("0"))
    otherProductCompany = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionPlantList"))

    # child relationships (access children)
    SubmissionIngredientList : Mapped[List["SubmissionIngredient"]] = relationship(back_populates="SubmissionPlant")
    SubmissionProductList : Mapped[List["SubmissionProduct"]] = relationship(back_populates="SubmissionPlant")



class SubmissionRawDatum(Base):  # type: ignore
    __tablename__ = 'SubmissionRawData'
    _s_collection_name = 'submission-SubmissionRawDatum'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["answer"]  # TEXT(max) column excluded from list responses

    SubmissionRawDataId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    entryorder = Column(Integer, nullable=False)
    prompt = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    control_type = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    answer = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionRawDatumList"))

    # child relationships (access children)



class SubmissionRequest(Base):  # type: ignore
    __tablename__ = 'SubmissionRequest'
    _s_collection_name = 'submission-SubmissionRequest'  # type: ignore
    __bind_key__ = 'submission'
    _s_expunge = ["SubmissionMessage"]  # TEXT(max) column excluded from list responses

    SubmissionRequestId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'))
    SubmissionStatus = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text("('NEW')"), nullable=False)
    SubmissionType = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ApplicationId = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    SubmissionMessage = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    created_date = Column(DATETIME2, server_default=text("getdate()"))
    updated_date = Column(DATETIME2)

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionRequestList"))

    # child relationships (access children)



class SubmissionValidation(Base):  # type: ignore
    __tablename__ = 'SubmissionValidations'
    _s_collection_name = 'submission-SubmissionValidation'  # type: ignore
    __bind_key__ = 'submission'

    ValidationId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionAppId = Column(ForeignKey('SubmissionApplication.SubmissionAppId'), nullable=False)
    SubmissionValue = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    isError = Column(Boolean, server_default=text("0"))
    validationMessage = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionApp : Mapped["SubmissionApplication"] = relationship(back_populates=("SubmissionValidationList"))

    # child relationships (access children)



class SubmissionIngredient(Base):  # type: ignore
    __tablename__ = 'SubmissionIngredients'
    _s_collection_name = 'submission-SubmissionIngredient'  # type: ignore
    __bind_key__ = 'submission'

    SubmissionIngredientId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionPlantId = Column(ForeignKey('SubmissionPlant.PlantId'), nullable=False)
    UKDID = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    rawMaterialCode = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ingredientLabelName = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    manufacturer = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    brandName = Column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    packagedOrBulk = Column(Unicode(15, 'SQL_Latin1_General_CP1_CI_AS'))
    certifyingAgency = Column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionPlant : Mapped["SubmissionPlant"] = relationship(back_populates=("SubmissionIngredientList"))

    # child relationships (access children)



class SubmissionProduct(Base):  # type: ignore
    __tablename__ = 'SubmissionProducts'
    _s_collection_name = 'submission-SubmissionProduct'  # type: ignore
    __bind_key__ = 'submission'

    SubmissionProductId = Column(Integer, autoincrement=True, primary_key=True)
    SubmissionPlantId = Column(ForeignKey('SubmissionPlant.PlantId'), nullable=False)
    productName = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Retail = Column(Boolean, server_default=text("1"))
    Industrial = Column(Boolean, server_default=text("0"))
    BrandName = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))
    inHouse = Column(Boolean, server_default=text("1"))
    privateLabel = Column(Boolean, server_default=text("0"))
    privateLabelCo = Column(Unicode(250, 'SQL_Latin1_General_CP1_CI_AS'))

    # parent relationships (access parent)
    SubmissionPlant : Mapped["SubmissionPlant"] = relationship(back_populates=("SubmissionProductList"))

    # child relationships (access children)
