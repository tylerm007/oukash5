import logging
import api.system.api_utils as api_utils
import safrs
from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from safrs import jsonapi_rpc
import safrs
from sqlalchemy import false, text, or_, and_
from database import models
import os
from security.system.authorization import Security
from datetime import datetime

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)

db = safrs.DB 
session = db.session 

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger.debug("api/api_discovery/get_application_data.py - expose JotForm JSON get_application_data services")


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    pass

    @app.route('/get_prelim_application_details', methods=['GET','OPTIONS'])
    #@jwt_required()
    def get_prelim_application_details():
        """
        Get Application Details from JotForm API
        """

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        import time
        start_time = time.time()
        
        username = None # Security.current_user().Username
        data = request.args if request.args else {}
        limit = int(data.get('page[limit]', 20))
        offset = int(data.get('page[offset]', 0))
        name_filter = data.get('name', None) or data.get('filter[name]', None)
        external_reference_id = data.get('externalReferenceId', None) or data.get('filter[externalReferenceId]', None)   
        status = data.get('status', None) or data.get('filter[status]', None)
        sql = getSQL()
        params = {
            'application_id': external_reference_id,
            'searchName': name_filter, 
            'status': status, 
            'limit': limit, 
            'offset': offset,
            #"when_assigned": whenAssigned
        } 
        print(sql,params)
        results = session.execute(text(sql), params).fetchall()
        
        # SQL Server FOR JSON AUTO returns JSON as a single string column
        # Concatenate all fragments (in case result is large and fragmented)
        import json
        json_string = ''
        for row in results:
            if row and row[0]:  # First column contains JSON fragment
                json_string += row[0]
        
        # Parse the JSON string to Python objects
        json_data = json.loads(json_string) if json_string else []
        
        return jsonify({
            'data': json_data,
            'meta': {
                'execution_time_seconds': time.time() - start_time
            }
        }), 200

def getSQL():
    return """
     SELECT jfc.companyName,
        jfc.SubmissionAppId as externalReferenceId,
        jfc.companyWebsite,
        jfc.companyPhone,
        jfc.OUCertified,
        jfc.everCertified,
        jfc.submission_date as submissionDate,
        jfc.whichCategory,
        jfc.copack,
        jfc.status,
        (
            select jfca.companyAddress,
                   jfca.companyAddress2,
                    jfca.companyCity,
                    jfca.companyState,
                    jfca.ZipPostalCode,
                    jfca.companyRegion,
                    jfca.companyProvince,
                    jfca.companyCountry
            from [dashboardV1].[dbo].[SubmissionApplication] jfca
            where jfc.SubmissionAppId = jfca.SubmissionAppId
            FOR JSON AUTO
        ) as companyAdresses,
        (
            select jfcc.isPrimaryContact,
                     jfcc.contactFirst,
                     jfcc.contactLast,
                     jfcc.contactEmail,
                     jfcc.contactPhone,
                     jfcc.jobTitle,
                     jfcc.billingContact,
                     jfcc.billingContactFirst,
                     jfcc.billingContactLast,
                     jfcc.billingContactPhone,
                     jfcc.billingContactEmail

            from [dashboardV1].[dbo].[SubmissionApplication] jfcc
            where jfc.SubmissionAppId = jfcc.SubmissionAppId
            FOR JSON AUTO
        ) as companyContacts,

    (
            select jfp.*,
            (
                select jfi.* 
                from [dashboardV1].[dbo].[SubmissionIngredients] jfi
                 Where jfi.SubmissionPlantId = jfp.PlantId
                FOR JSON AUTO
            ) as ingredients,
            (
                select jfi.* 
                from [dashboardV1].[dbo].[SubmissionProducts] jfi
                 Where jfi.SubmissionPlantId = jfp.PlantId
                FOR JSON AUTO
            ) as products
            from [dashboardV1].[dbo].[SubmissionPlant] jfp
            where jfc.SubmissionAppId = jfp.SubmissionAppId
           

            FOR JSON AUTO
            
           
      ) as plants,
     
      (
        select jff.* 
        FROM [dashboardV1].[dbo].[SubmissionFileLinks] jff
        where jfc.SubmissionAppId = jff.SubmissionAppId

        FOR JSON AUTO
      ) as filelinks
      FROM [dashboardV1].[dbo].[SubmissionApplication] jfc
        WHERE 
            (:application_id IS NULL OR jfc.SubmissionAppId = :application_id) AND
            (:status IS NULL OR jfc.status = :status) AND
            (:searchName IS NULL OR jfc.companyName LIKE CONCAT('%', :searchName, '%'))
        ORDER BY jfc.submission_date DESC   
        OFFSET :offset ROWS
        FETCH NEXT :limit ROWS ONLY
       FOR JSON AUTO
    """