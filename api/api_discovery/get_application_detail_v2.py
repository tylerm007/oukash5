from flask import request, jsonify
from datetime import datetime
from flask import request, jsonify, session
import logging
import safrs
import json
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from sqlalchemy.sql import text
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
 
app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session
_project_dir = None
 
def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass
   
    def admin_required():
        """
        Support option to bypass security (see cats, below).
        """
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.instance.security_enabled == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                return fn(*args, **kwargs)
            return decorator
        return wrapper
    @app.route('/get_application_detail_v2', methods=['GET',"OPTIONS"])
    #@cross_origin()
    @admin_required()
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
        
        application_id = request.args.get('applicationId',None, type=int)
        app_logger.info(f'{application_id}')
        #if not wf_application:
        #    return jsonify({"error": f"Application for id {application_id} not found"}), 404
        try:
            params = {"application_id": application_id}
            sql = get_SQL()
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
            select CATEGORY as category,
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
                    'Unkown' as location
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
    where app.ApplicationID = :application_id
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