from pipes import quote
from flask import request, jsonify
from datetime import datetime
from database.models import COMPANYADDRESSTB, PLANTADDRESSTB, ProcessDefinition, TaskDefinition, ProcessInstance, WFApplicationMessage, WFFile, WFIngredient, WFProduct, WFQuote, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, WFContact
from flask import request, jsonify, session
import logging
import uuid
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

    @app.route('/get_application_detail_v1', methods=['GET',"OPTIONS"])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_application_detail_v1():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.
        * Returns NCRC data in JSON format

        Test it with:

        Invoke-RestMethod -Uri "http://localhost:5656/get_application_detail?applicationId=1" -Method GET -ContentType "application/json"

        Returns JSON response with application data including:
        - Application info (ID, submission date, status)
        - Company details (name, category, certification status)
        - Plant information (name, location, address)
        - Products list (label names, brands, certifications)
        - Ingredients list (NCRC IDs, manufacturers, certifications)
        """
        application_id = request.args.get('applicationId',None, type=int)
        app_logger.info(f'{application_id}')

       
        from database.models import CompanyApplication, WFApplication, COMPANYTB, OWNSTB, PLANTTB, PLANTADDRESSTB, LabelTb, MERCHTB, USEDIN1TB
        wf_application = WFApplication.query.filter_by(ApplicationID=application_id).first()
        if not wf_application:
            return jsonify({"error": f"Application for id {application_id} not found"}), 404
        sql = get_SQL()
        params = {"application_id": application_id}
        results = session.execute(text(sql), params).fetchall()
        if not results or len(results) == 0:
            return jsonify({"error": f"Application details for id {application_id} not found"}), 404

        fields = results[0]._fields if len(results) > 0 else []
        data = []
        # Convert tasks to dictionaries and add to result
        for result in results:
            row = dict(zip(fields, result))
            company = row.get('company')
            company_address = row.get('company_address')
            ingredients = row.get('ingredients')
            products = row.get('products')
            plant_address = row.get('plantAddress')
            plant = row.get('plant')
            contacts = row.get('contacts') or []
            messages = row.get('messages') or []
            quotes = row.get('quotes') or []
            files = row.get('files') or []
            row['company'] = json.loads(company) if company else {}
            row['company_address'] = json.loads(company_address) if company_address else {}
            row['ingredients'] = json.loads(ingredients) if ingredients else []
            row['products'] = json.loads(products) if products else []
            row['plantAddress'] = json.loads(plant_address) if plant_address else {}    
            row['plant'] = json.loads(plant) if plant else {}
            row['files'] = json.loads(files) if files else []
            row['messages'] = json.loads(messages) if messages else []
            row['quotes'] = json.loads(quotes) if quotes else []
            row['contacts'] = json.loads(contacts) if contacts else []
            data.append(row)

        '''
        #quotes = WFQuote.query.filter_by(ApplicationID=application_id).all()
        #quote_items = []
        result['quotes'] = [{
            "quoteId": 1,
            "QuoteNumber": "Q-0001",
            "QuoteDate": "2025-10-10",
            "TotalAmount": 1500.00,
            "Status": "Pending Acceptance",
            "validUntil": "2025-12-15",
            "items": [
                {
                    "itemId": 1,
                    "Description": "Application Processing Fee",
                    "Amount": 500.00
                },
                {
                    "itemId": 2,
                    "Description": "Product Review Fee",
                    "Amount": 1000.00
                }
            ]
        }]
        
        for quote in quotes:
                items = quote.WFQuoteItemList if hasattr(quote, 'WFQuoteItemList') else []
                for item in items:
                    quote_items.append(
                    {
                        "itemId": item.QuoteItemID if hasattr(item, 'QuoteItemID') else 1,
                        "description": item.Description if hasattr(item, 'Description') else "",
                        "amount": float(item.Amount) if hasattr(item, 'Amount') else 0.0,
                    })
                result['quotes'].append(
                  {
                    "quoteId": quote.QuoteID,
                    "quoteNumber": quote.QuoteNumber if hasattr(quote, 'QuoteNumber') else str(uuid.uuid4())[:8],
                    "quoteDate": quote.CreatedDate.strftime('%Y-%m-%d') if hasattr(quote, 'CreatedDate') else None,
                    "totalAmount": float(quote.TotalAmount) if hasattr(quote, 'TotalAmount') else 0.0,
                    "status": quote.Status if hasattr(quote, 'Status') else "Pending",
                    "validUntil": quote.ValidUntil.strftime('%Y-%m-%d') if hasattr(quote, 'ValidUntil') else None,
                    "items": quote_items
                 }
                )
        '''
        result = data[0] if len(data) > 0 else {}
        application_info = {}
        application_info["applicationInfo"] = result
        return jsonify(application_info), 200


def get_products(company_id: int, plant_id: int) -> list:
    sql = f"""
        SELECT TOP (100) 
            [PRODUCT_NAME] as labelName,
            [BRAND_NAME] as brandName,
            [LABEL_COMPANY] as labelCompany,
            [INDUSTRIAL] as ConsumerIndustrial,
            [BLK] as bulkShipped,
            [Symbol] as certification,
            [STATUS] as status
        FROM [ou_kash].[dbo].[PRODUCT_GRID]
        WHERE [COMPANY_ID] = {company_id}
        AND [PLANT_ID] = {plant_id}
    """
    result = session.execute(text(sql))
    products = result.fetchall()
    if not products or len(products) == 0:
        app_logger.info(f'No products found for company {company_id}: {plant_id}')
        return []
    rows = [dict(zip(row._fields, row)) for row in products]
    return rows

def get_ingredients(company_id:int, plant_id: int) -> list:
    sql = f"""
        SELECT TOP (100) 
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
        WHERE [COMPANY_ID] = {company_id}
        AND [PLANT_ID] = {plant_id}
    """
    result = session.execute(text(sql))
    ingredients = result.fetchall()
    
    if not ingredients or len(ingredients) == 0:
        app_logger.info(f'No ingredients found for company {company_id}: {plant_id}')
        return []
    rows = [dict(zip(row._fields, row)) for row in ingredients]
    return rows

def get_company_address(company_id: int):
    company = session.query(COMPANYADDRESSTB).filter(COMPANYADDRESSTB.COMPANY_ID == company_id).first()
    if not company:
        app_logger.error(f'Company not found: {company_id}')
        return None
    address = f"{company.STREET1},{company.STREET2}, {company.CITY}, {company.STATE} {company.ZIP}"
    app_logger.info(f'Company Address: {address}')
    return company

def get_plant_address(plant_id: int):
    plant = session.query(PLANTADDRESSTB).filter(PLANTADDRESSTB.PLANT_ID == plant_id).first()
    if not plant:
        app_logger.error(f'Plant Address not found: {plant_id}')
        return None
    address = f"{plant.STREET1}, {plant.STREET2}, {plant.CITY}, {plant.STATE} {plant.ZIP}"
    app_logger.info(f'Plant Address: {address}')
    return plant

def get_contacts(company_id: int, plant_id: int) -> list:
    sql = f"""
        SELECT TOP (3) [pcID]
            ,[companytitle]
            ,[owns_ID]
            ,[Title]
            ,[FirstName]
            ,[LastName]
            ,[Voice]
            ,[Fax]
            ,[EMail]
            ,[Cell]
            ,[PrimaryCT]
            ,[BillingCT]
            ,[WebCT]
            FROM [ou_kash].[dbo].[PlantContacts]
                WHERE owns_ID IN
                (select TOP 3 OWNS_ID from [ou_kash].[dbo].[OWNS_TB] where COMPANY_ID = {company_id} and PLANT_ID = {plant_id})
    """
    result = session.execute(text(sql))
    contacts = result.fetchall()
    if not contacts:
        app_logger.error(f'Contact not found: {company_id} {plant_id}')
        return []
    rows = [dict(zip(row._fields, row)) for row in contacts]
    app_logger.info(f'Contact Info: {rows}')
    return rows

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

def get_SQL() ->str:
    return ''' 
      SELECT 
        app.ApplicationID,
        app.ApplicationNumber,
        app.CompanyID,
        app.PlantID,
        app.SubmissionDate,
        app.Status,
        app.Priority,
        app.AssignedTo,
        app.AssignedBy,
        app.AssignedDate,
        app.CreatedDate,
        app.CreatedBy,
        app.ModifiedDate,
      (
            select q.*,
            (
                select *
                from WF_QuoteItems qi
                where qi.QuoteID = q.QuoteID
                for JSON AUTO
            ) as quote_items
            from WF_Quotes q
            where q.ApplicationID = app.ApplicationID
            FOR JSON AUTO
      ) as quotes,
      (
            select * 
            from WF_Files 
            where   WF_Files.ApplicationID = app.ApplicationID
            FOR JSON AUTO
      ) as "files",
      (
            select * 
            from WF_ApplicationMessages  
            where WF_ApplicationMessages.ApplicationID = app.ApplicationID
            FOR JSON AUTO
      ) as "messages",
      (
            select * 
            from ou_kash.dbo.COMPANY_ADDRESS_TB  
            where ou_kash.dbo.COMPANY_ADDRESS_TB.COMPANY_ID = app.companyId
            FOR JSON AUTO
      ) as company_address,
      (
            select * 
            from ou_kash.dbo.COMPANY_TB  
            where ou_kash.dbo.COMPANY_TB.COMPANY_ID = app.companyId
            FOR JSON AUTO
      ) as company,
      (
            select * 
            from ou_kash.dbo.PLANT_TB  
            where ou_kash.dbo.PLANT_TB.PLANT_ID = app.PlantID
            FOR JSON AUTO
      ) as plant,
      (
            select 
                STREET1 as street, 
                STREET2 as line2,
                CITY as city,
                STATE as state,
                ZIP as zip,
                COUNTRY as country,
                TYPE as type
            from ou_kash.dbo.PLANT_ADDRESS_TB  
            where ou_kash.dbo.PLANT_ADDRESS_TB.PLANT_ID = app.PlantID
                FOR JSON AUTO
      ) as plantAddress,
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
     ) as ingredients, 
     (
        SELECT TOP (2000) 
            [PRODUCT_NAME] as labelName,
            [BRAND_NAME] as brandName,
            [LABEL_COMPANY] as labelCompany,
            [INDUSTRIAL] as ConsumerIndustrial,
            [BLK] as bulkShipped,
            [Symbol] as certification,
            [STATUS] as status
        FROM [ou_kash].[dbo].[PRODUCT_GRID]
        where [COMPANY_ID] = app.CompanyID and [PLANT_ID] = app.PlantID
                    FOR JSON AUTO
     ) as products,
      ( 
        SELECT TOP (2000) 
            [pcID]
            ,[companytitle]
            ,[owns_ID]
            ,[Title]
            ,[FirstName]
            ,[LastName]
            ,[Voice]
            ,[Fax]
            ,[EMail]
            ,[Cell]
            ,[PrimaryCT]
            ,[BillingCT]
            ,[WebCT]
            FROM [ou_kash].[dbo].[PlantContacts]
            WHERE owns_ID IN
            (select TOP 3 ID from [ou_kash].[dbo].[OWNS_TB] where COMPANY_ID = app.companyId  and PLANT_Id = app.PlantId
            )
            FOR JSON AUTO
     ) as contacts
    FROM dashboard.[dbo].[WF_Applications] app
    where app.ApplicationID = :application_id
    '''