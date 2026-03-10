from database.models import WFFile
from flask import request, jsonify
from datetime import datetime
from flask import request, jsonify, session
import logging
import safrs
import json
from config.config import Config
from sqlalchemy.sql import text
from flask_jwt_extended import get_jwt, jwt_required
 
app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session
_project_dir = None
 
def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    @app.route('/get_application_detail_v2', methods=['GET',"OPTIONS"])
    @jwt_required()
    def get_application_detail_v2():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.
        * Returns NCRC data in JSON format
 
        Test it with:
 
        Invoke-RestMethod -Uri "http://localhost:5656/get_application_detail_v2?applicationId=1" -Method GET -ContentType "application/json"
 
        Returns JSON response with application data including:
        - Application info (ID, submission date, status)
        - Company details (name, category, certification status)
        - Plant information (name, location, address)
        - Products list (label names, brands, certifications)
        - Ingredients list (NCRC IDs, manufacturers, certifications)
        """
        application_id = request.args.get('applicationId',None, type=int)
        app_logger.info(f'{application_id}')
 
       
        import time
        start_time = time.time()
        from database.models import WFApplication, WFFile
        from api.api_discovery.upload_files import _parse_s3_path, generate_presigned_url
        application_id = request.args.get('applicationId',None, type=int)
        app_logger.info(f'{application_id}')
        wf_application = session.query(WFApplication).filter_by(ApplicationID=application_id).first()
        if not wf_application:
            return jsonify({"error": f"Application for id {application_id} not found"}), 404
        try:
            application_type = wf_application.ApplicationType
            params = {"application_id": application_id}
            sql = get_SUBMISSION_SQL() if application_type == "SUBMISSION" else get_SQL()
            results = session.execute(text(sql), params).fetchall()
            if not results or len(results) == 0:
                return jsonify({"error": f"Application details for id {application_id} not found"}), 404 
        except Exception as e:
            app_logger.error(f"Error executing dsql: {e}")
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500

        # SQL Server FOR JSON PATH returns fragmented JSON strings when result is large
        # Concatenate all fragments from the result rows
        json_fragments = []
        for row in results:
            # Each row is a tuple with one element (the JSON fragment)
            if row and row[0]:
                json_fragments.append(row[0])
        
        # Combine all fragments into a single JSON string
        json_string = ''.join(json_fragments)
        
        # Parse the JSON string into a Python object
        try:
            application_data = json.loads(json_string)
            # FOR JSON PATH returns an array, get the first element
            if isinstance(application_data, list) and len(application_data) > 0:
                application_info = application_data[0]
                status = application_data[0]['appplicationinfo']['status']
                files = application_data[0]['appplicationinfo']['files'] if 'files' in application_data[0]['appplicationinfo'] else []
                for _file in files:
                    file = session.query(WFFile).filter_by(FileID=_file['FileID']).first()
                    if file is None:
                        app_logger.warning(f"File with ID {_file['FileID']} not found in database")
                        continue
                    expires = 3600  # URL expiration time in seconds
                    file_path = getattr(file, 'FilePath', None)
                    if file_path and  file_path.startswith('s3://'):
                        bucket, s3_key = _parse_s3_path(file_path)
                        app_logger.info(f"Presigned URL request: bucket={bucket} key={s3_key} (raw FilePath={file_path!r})")
                        url = generate_presigned_url(bucket, s3_key, expires)
                        _file['FilePath'] = url
                application_data[0]['appplicationinfo']['status'] = get_app_status(status)
            else:
                application_info = application_data
        except json.JSONDecodeError as je:
            app_logger.error(f"Error parsing JSON: {je}")
            app_logger.error(f"JSON string: {json_string[:500]}...")  # Log first 500 chars
            return jsonify({"status": "error", "message": f"JSON parsing error: {str(je)}"}), 500
            
        end_time = time.time()
        processing_time = end_time - start_time
        app_logger.info(f"get_application_detail_v2 processed in {processing_time} seconds")
        
        return jsonify(application_info), 200
 
def get_SQL() ->str:
    return '''
        SELECT  app.ApplicationID as 'appplicationinfo.applicationID',
          app.CompanyID as 'appplicationinfo.kashrusCompanyId',
          app.PlantID as 'appplicationinfo.PlantId',
          'UNKNOWN' as 'appplicationinfo.kashrusStatus',
          app.Status as 'appplicationinfo.status',
          app.SubmissionDate as 'appplicationinfo.submissionDate',
        (
                select * 
                from WF_Quotes  
                where WF_Quotes.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.quotes',
        (
                select * 
                from WF_Files 
                where   WF_Files.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.files',
        (
                select *
                from TaskEvents
                where TaskEvents.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.taskEvents',
        (
                select * 
                from WF_ApplicationMessages  
                where WF_ApplicationMessages.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.messages',
        (
                select  CompanyID as companyID,
                        CATEGORY as category,
                        CASE
                            WHEN STATUS = 'Certified ' THEN 'Y'
                            ELSE  'N'
                        END as currentlyCertified,
                        'tbd' as everCertified,
                        NAME as name,
                        'tbd' as website
                from ou_kash.dbo.COMPANY_TB  
                where ou_kash.dbo.COMPANY_TB.COMPANY_ID = app.companyId
                FOR JSON AUTO
        ) as 'appplicationinfo.company',
        (
                select City as city,
                    COUNTRY as country,
                    '' as line2,
                    STATE as state,
                    STREET1 as street,
                    TYPE as type,
                    ZIP as zip
                from ou_kash.dbo.COMPANY_ADDRESS_TB  
                where ou_kash.dbo.COMPANY_ADDRESS_TB.COMPANY_ID = app.companyId
                FOR JSON AUTO
        ) as 'appplicationinfo.companyAddresses',
        ( 
            SELECT TOP (2000) 
                    concat(FirstName, ' ', LastName) as name,
                    EMail as email,
                    Voice as phone,
                    CASE
                        WHEN PrimaryCT = 'Y' THEN 'Primary Contact'
                        ELSE  'Not Primary Contact'
                    END as type,
                    companytitle as role
                FROM [ou_kash].[dbo].[companyContacts] 
                WHERE COMPANY_ID = app.companyId
                    FOR JSON AUTO
        ) as 'appplicationinfo.companyContacts',
        (
                select NAME as name,
                        'Unkown' as location,
                        PLANT_ID  plantID
                from ou_kash.dbo.PLANT_TB  
                where ou_kash.dbo.PLANT_TB.PLANT_ID = app.PlantID
                FOR JSON AUTO
        ) as 'appplicationinfo.plants',
        (
                select City as city,
                    COUNTRY as country,
                    '' as line2,
                    STATE as state,
                    STREET1 as street,
                    TYPE as type,
                    ZIP as zip
                from ou_kash.dbo.PLANT_ADDRESS_TB  
                where ou_kash.dbo.PLANT_ADDRESS_TB.PLANT_ID = app.PlantID
                    FOR JSON AUTO
        ) as 'appplicationinfo.plantAddresses',
        ( 
            SELECT TOP (2000) 
                    concat(FirstName, ' ', LastName) as name,
                    EMail as email,
                    Voice as phone,
                    CASE
                        WHEN PrimaryCT = 'Y' THEN 'Primary Contact'
                        ELSE  'Not Primary Contact'
                    END as type,
                    companytitle as role
                FROM [ou_kash].[dbo].[PlantContacts]
                    WHERE owns_ID IN
                    (select TOP 3 ID from [ou_kash].[dbo].[OWNS_TB] where COMPANY_ID = app.companyId  and PLANT_Id = app.PlantId
                    )
                    FOR JSON AUTO
        ) as 'appplicationinfo.plantContacts',
        (
            SELECT TOP (2000) 
                [INGREDIENT_NAME] as ingredient
                ,[MERCHANDISE_ID] as ncrcId
                ,[BRAND_NAME] as brand
                ,[SYMBOL] as certification
                ,[LABEL_COMPANY] as manufacturer
                ,[BLK] as packaging
                ,[DateAdded] as addedDate
                ,[LabelStatus] as status
                ,[COMPANY_ID] as companyId
                ,[PLANT_ID] as plantId
            FROM [ou_kash].[dbo].[INGREDIENT_GRID_JOIN_USEDIN1]
                    WHERE [COMPANY_ID] = app.CompanyID AND [PLANT_ID] = app.PlantID
                    FOR JSON AUTO
        ) as 'appplicationinfo.ingredients', 
        (

            SELECT TOP (2000)  [PRODUCT_NAME] as labelName,
                [BRAND_NAME] as brandName,
                [LABEL_COMPANY] as labelCompany,
                [INDUSTRIAL] as ConsumerIndustrial,
                [BLK] as bulkShipped,
                [Symbol] as certification,
                [STATUS] as status
            FROM [ou_kash].[dbo].[PRODUCT_GRID]
            where [COMPANY_ID] = app.CompanyID and [PLANT_ID] = app.PlantID
                        FOR JSON AUTO
        ) as 'appplicationinfo.products'
        FROM dashboard.[dbo].[WF_Applications] app

        where :application_id = app.ApplicationID

        FOR JSON PATH
    '''

def get_SUBMISSION_SQL() -> str:
    return '''
        SELECT  app.ApplicationID as 'appplicationinfo.applicationID',
          app.CompanyID as 'appplicationinfo.kashrusCompanyId',
          app.PlantID as 'appplicationinfo.PlantId',
          'UNKNOWN' as 'appplicationinfo.kashrusStatus',
          app.Status as 'appplicationinfo.status',
          app.SubmissionDate as 'appplicationinfo.submissionDate',
        (
                select * 
                from WF_Quotes  
                where WF_Quotes.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.quotes',
        (
                select * 
                from WF_Files 
                where   WF_Files.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.files',
        (
                select * 
                from WF_ApplicationMessages  
                where WF_ApplicationMessages.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as 'appplicationinfo.messages',
        (
                select co.SubmissionAppId as companyID,
                        co.whichCategory as category,
                        co.OUcertified as currentlyCertified,
                        co.everCertified as everCertified,
                        co.companyName as name,
                        co.companyWebsite as website
                from dashboardV1.dbo.SubmissionApplication co  
                where co.SubmissionAppId = app.ExternalAppRef
                FOR JSON AUTO
        ) as 'appplicationinfo.company',
        (
                select coa.companyCity as city,
                    coa.companyCountry as country,
                    coa.companyAddress2 as line2,
                    coa.companyState as state,
                    coa.companyAddress as street,
                    'main' as type,
                    coa.ZipPostalCode as zip
                from dashboardV1.dbo.SubmissionApplication coa  
                where coa.SubmissionAppId = app.ExternalAppRef
                FOR JSON AUTO
        ) as 'appplicationinfo.companyAddresses',
        ( 
            SELECT  
                    concat(coc.contactFirst, ' ', coc.contactLast) as name,
                    coc.contactEmail1 as email,
                    coc.contactPhone as phone,
                    'Primary' as type,
                    coc.jobTitle as role
                FROM dashboardV1.dbo.SubmissionApplication coc  
                where coc.SubmissionAppId = app.ExternalAppRef
                    FOR JSON AUTO
        ) as 'appplicationinfo.companyContacts',
        (
                select jfp.*
                from dashboardV1.dbo.SubmissionPlant jfp  
                where jfp.SubmissionAppId = app.ExternalAppRef
                FOR JSON AUTO
        ) as 'appplicationinfo.plants',
        (
                select jfpa.*
                from dashboardV1.dbo.SubmissionPlant jfpa  
                where jfpa.SubmissionAppId = app.ExternalAppRef
                    FOR JSON AUTO
        ) as 'appplicationinfo.plantAddresses',
        ( 
            SELECT jfpc.*
                FROM dashboardV1.dbo.SubmissionPlant jfpc  
                where jfpc.PlantId = app.SubmissionPlant
                    FOR JSON AUTO
        ) as 'appplicationinfo.plantContacts',
        (
            SELECT TOP (2000) 
                [INGREDIENT_NAME] as ingredient
                ,[MERCHANDISE_ID] as ncrcId
                ,[BRAND_NAME] as brand
                ,[SYMBOL] as certification
                ,[LABEL_COMPANY] as manufacturer
                ,[BLK] as packaging
                ,[DateAdded] as addedDate
                ,[LabelStatus] as status
                ,[COMPANY_ID] as companyId
                ,[PLANT_ID] as plantId
            FROM [ou_kash].[dbo].[INGREDIENT_GRID_JOIN_USEDIN1]
                    WHERE [COMPANY_ID] = app.CompanyID AND [PLANT_ID] = app.PlantID
                    FOR JSON AUTO
        ) as 'appplicationinfo.ingredients', 
        (

            SELECT TOP (2000)  [PRODUCT_NAME] as labelName,
                [BRAND_NAME] as brandName,
                [LABEL_COMPANY] as labelCompany,
                [INDUSTRIAL] as ConsumerIndustrial,
                [BLK] as bulkShipped,
                [Symbol] as certification,
                [STATUS] as status
            FROM [ou_kash].[dbo].[PRODUCT_GRID]
            where [COMPANY_ID] = app.CompanyID and [PLANT_ID] = app.PlantID
                        FOR JSON AUTO
        ) as 'appplicationinfo.products'
        FROM dashboard.[dbo].[WF_Applications] app

        where :application_id = app.ApplicationID

        FOR JSON PATH
    '''

def get_total_count() -> str:
    return '''
    SELECT COUNT(*) as total_count
    FROM WF_Applications  app
         LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
         LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID
     WHERE (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
            (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
    '''


def get_app_status(status_code: str):
    status_map = {
        "NEW": "New",
        "INP": "In Progress",
        "HLD": "On Hold",
        "WTH": "Withdrawn",
        "COMPL": "Certified",
        "REJ": "Rejected",
        "REVIEW": "Inspection Report Submitted to IAR",
        "INSPECTION": "Inspection Scheduled",
        "PAYPEND": "Payment Pending",
        "CONTRACT": "Contract Sent to Customer"
    }
    return status_map.get(status_code, "Unknown Status")