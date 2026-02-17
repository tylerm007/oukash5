from config.config import Args
from flask_jwt_extended import get_jwt, jwt_required  
import datetime
from database.models import WFApplication
import database.models as models
from flask import request, jsonify
import logging
import safrs
from sqlalchemy.sql import text
import time
import json
from security.system.authorization import Security

"""
Various endpoints to test workflow functionality and cleanup or reset tests
"""
db = safrs.DB 
session = db.session

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):

    pass


    @app.route('/get_CompanyDetailsFromKASH', methods=['GET','OPTIONS'])
    @jwt_required()
    def get_company_details_from_kash():    
        args = request.args
        company_id = args.get('company_id') or args.get('CompanyId') or args.get('companyID')
        if not company_id:
            return jsonify({"message": "company_id, CompanyId, or companyID is required"}), 400
        sql = get_company_details_sql(company_id)
        results = session.execute(text(sql)).fetchall()
        
        # SQL Server's FOR JSON AUTO returns a single row with JSON string
        if len(results) == 0:
            return jsonify({"message": "Company not found", "company_id": company_id}), 404
        
        # Extract the JSON string from the first column of the first row
        json_string = results[0][0] if results[0] else None
        
        if json_string:
            # Parse the JSON string to proper Python dict/list
            json_data = json.loads(json_string)
            return jsonify(json_data), 200
        else:
            return jsonify({"message": "No data found for company", "company_id": company_id}), 404


    @app.route('/get_PlantDetailsFromKASH', methods=['GET','OPTIONS'])
    @jwt_required()
    def get_plant_details_from_kash() -> str:    
        args = request.args
        plant_id = args.get('plant_id') or  args.get('PlantId')
        if not plant_id:
            return jsonify({"message": "plant_id is required"}), 400
        sql = get_plant_details_sql(plant_id)
        results = session.execute(text(sql)).fetchall()
        
        # SQL Server's FOR JSON AUTO returns a single row with JSON string
        if len(results) == 0:
            return jsonify({"message": "Plant not found", "plant_id": plant_id}), 404
        
        # Extract the JSON string from the first column of the first row
        json_string = results[0][0] if results[0] else None
        
        if json_string:
            # Parse the JSON string to proper Python dict/list
            json_data = json.loads(json_string)
            return jsonify(json_data), 200
        else:
            return jsonify({"message": "No data found for plant", "plant_id": plant_id}), 404

def get_company_details_sql(company_id: int) -> str:
    return f'''
        SELECT co.NAME as companyName,
        (
        select co1.*
        FROM [ou_kash].[dbo].[COMPANY_TB] co1
        where co1.COMPANY_ID = co.COMPANY_ID
        FOR JSON AUTO
        ) as companytdetails,
        (
        select *
        from [ou_kash].[dbo].[COMPANY_ADDRESS] ca
        WHERE ca.COMPANY_ID = co.COMPANY_ID
        FOR JSON AUTO

        ) as companyAddresses,
        (
        select *
        from [ou_kash].[dbo].[companycontacts_tb] cc
        WHERE cc.COMPANY_ID = co.COMPANY_ID
        FOR JSON AUTO

        ) as companyContacts
        FROM [ou_kash].[dbo].[COMPANY_TB] co
        where COMPANY_ID ={company_id}
    FOR JSON AUTO
    '''


def get_plant_details_sql(plant_id: int) -> str:
    return f'''
        SELECT pl.NAME as plantName,
        (
            select co1.*
            FROM [ou_kash].[dbo].[PLANT_TB] co1
            where co1.PLANT_ID = pl.PLANT_ID
            FOR JSON AUTO
        ) as plantdetails,
        (
            select *
            from [ou_kash].[dbo].[PLANT_ADDRESS_TB] pa
            WHERE pa.PLANT_ID = pl.PLANT_ID
            FOR JSON AUTO
        ) as plantAddresses,
        (
            select *
            from [ou_kash].[dbo].[plantContacts_TB] pc
            WHERE pc.pcID = pl.PLANT_ID
            FOR JSON AUTO
        ) as plantContacts
        FROM [ou_kash].[dbo].PLANT_TB pl
        where pl.PLANT_ID = {plant_id}
        FOR JSON AUTO
    '''