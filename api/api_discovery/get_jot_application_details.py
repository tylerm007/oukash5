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
    @jwt_required()
    def get_prelim_application_details():
        """
        Get Application Details from JotForm API
        """

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        import time
        start_time = time.time()
        
        username = Security.current_user().Username
        data = request.args if request.args else {}
        limit = int(data.get('page[limit]', 20))
        offset = int(data.get('page[offset]', 0))
        priority = data.get('priority', None) or data.get('filter[priority]', None)
        name_filter = data.get('name', None) or data.get('filter[name]', None)
        application_id = data.get('application_id', None) or data.get('filter[applicationId]', None)   
        status = data.get('status', None) or data.get('filter[status]', None)
        sql = getSQL()
        params = {
            'application_id': application_id,
            'searchName': name_filter, 
            'status': status, 
            'priority': priority, 
            'limit': limit, 
            'offset': offset,
            #"when_assigned": whenAssigned
        } 
        print(sql,params)
        results = session.execute(text(sql), {}).fetchall()
        
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
     SELECT jfc.*,
    (
            select jfp.*,
            (
                select jfi.* 
                from [dashboard].[dbo].[JotFormIngredients] jfi
                 Where jfi.JotPlantId = jfp.PlantId
                FOR JSON AUTO
            ) as ingredients,
            (
                select jfi.* 
                from [dashboard].[dbo].[JotFormProducts] jfi
                 Where jfi.JotPlantId = jfp.PlantId
                FOR JSON AUTO
            ) as products
            from [dashboard].[dbo].[JotFormPlant] jfp
            where jfc.JotFormId = jfp.JotFormId
           
            FOR JSON AUTO
           
      ) as plants,
      (
        select jff.* 
        FROM [dashboard].[dbo].[JotFormFileLinks] jff
        where jfc.JotFormId = jff.JotFormId

        FOR JSON AUTO
      ) as filelinks
      FROM [dashboard].[dbo].[JotFormCompany] jfc
     
       FOR JSON AUTO
    """