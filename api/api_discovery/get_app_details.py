from pipes import quote
from flask import request, jsonify
from datetime import datetime
from database.models import COMPANYADDRESSTB, PLANTADDRESSTB, ProcessDefinition, TaskDefinition, ProcessInstance, WFApplicationMessage, WFFile, WFIngredient, WFProduct, WFQuote, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, WFContact
from flask import request, jsonify, session
import logging
import uuid
import safrs
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

    @app.route('/get_application_detail', methods=['GET',"OPTIONS"])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_application_detail():
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
        application = wf_application.to_dict()

        company_application = CompanyApplication.query.filter_by(ID=application['ApplicationNumber']).first()
        #if not company_application:
        #    return jsonify({"error": f"Company application {application['ApplicationNumber']} not found"}), 404

        company_id = application['CompanyID'] if 'CompanyID' in application else None
        if not company_id:
            return jsonify({"error": "Company ID not found for application"}), 404
        
        company = COMPANYTB.query.filter_by(COMPANY_ID=company_id).first()
        if not company:
            return jsonify({"error": "Company not found"}), 404 
        
        company_address = get_company_address(company_id)
        owns = OWNSTB.query.filter_by(COMPANY_ID=company_id).all()
        if not owns:
           app_logger.error(f"Ownership not found for company ID: {company_id}")

        plant_id = application['PlantID'] or -9999
        planttb = PLANTTB.query.filter_by(PLANT_ID=plant_id).first()
        #plants = PLANTTB.query.filter(PLANTTB.PLANT_ID.in_(own.PLANT_ID for own in owns)).all()
        if not planttb:
            app.logger.info(f'No plant found for company ID: {company_id} in Application {application_id}')    
        #
        plant_address = get_plant_address(plant_id)
        products = get_products(company_id, plant_id)
        ingredients = get_ingredients(company_id, plant_id)
        primary_contact = ""
        plant = {}
        plant['address'] = {}
        plant["manufacturing"] = {} 
        '''
            "manufacturing": {
            "process": "Grain cleaning, milling, and flour production. Raw grains are received in bulk, cleaned using mechanical separators, ground using stone mills, sifted through mesh screens, and packaged in food-grade containers. All processes follow HACCP guidelines.",
            "closestMajorCity": "Rochester, NY (15 miles)"
            },
            "otherProducts": true,
            "otherProductsList": "Animal feed supplements, grain storage services",
            "otherPlantsProducing": true,
            "otherPlantsLocation": "Secondary facility at 425a Commerce Drive, Rochester NY"
            }
        '''
        address = get_plant_address(plant_id)
        plant["address"] = {}
        if address:
            plant["address"] = {
                "street": address.STREET1, 
                'line2': address.STREET2,
                "city": address.CITY ,
                "state": address.STATE ,
                "zip": address.ZIP ,
                "country": address.COUNTRY ,
                "type": address.TYPE
            }

           
        #TO DO how to get contacts for plant? or use origin app?
        contacts = get_contacts(company_id, plant_id)
        plant_contacts = [
            {
                "name": f'{contact["FirstName"]} {contact["LastName"]}',
                "title": contact["Title"],
                "phone": contact["Voice"],
                "email": contact["EMail"],
                "isPrimary": bool(contact["PrimaryCT"] == 'Y')
            }
            for contact in contacts
        ]
        for pc in plant_contacts:
            if pc.get("isPrimary", False):
                primary_contact = pc.get("name", "")
                break
        plant["contacts"] = plant_contacts
        application['Plants'] = plant

        result = {
            "applicationId": application["ApplicationID"],
            "submissionDate": application["CreatedDate"] if "CreatedDate" in application else None,
            "status": get_app_status(application["Status"]),
            "kashrusCompanyId": company_id,
            "kashrusStatus": 'UNKNOWN', # TODO company_application.KashrusStatus if hasattr(company_application, 'KashrusStatus') else "Company Created",
            "primaryContact": primary_contact
        }
        if company_address:
             address =  {
                    "street": company_address.STREET1,
                    "line2": company_address.STREET2,
                    "city": company_address.CITY,
                    "state": company_address.STATE,
                    "country": company_address.COUNTRY,
                    "zip": company_address.ZIP
                }
        else:
            address = {}
        result['company'] = {
            "name": company.NAME if hasattr(company, 'NAME') else "Unknown",
            "category": company.CATEGORY if hasattr(company, 'CATEGORY') else "Unknown",
            "currentlyCertified": company.CurrentlyCertified if hasattr(company, 'CurrentlyCertified') else False,
            "everCertified": company.EverCertified if hasattr(company, 'EverCertified') else False,
            "website": company.Website if hasattr(company, 'Website') else f"www.{company.NAME.strip()}.com",
            "address": address
        }
        result['address'] = {
            "street": plant_address.STREET1 if hasattr(plant_address, 'STREET1') else "Unknown",
            "line2": plant_address.STREET2 if hasattr(plant_address, 'STREET2') else "Unknown",
            "city": plant_address.CITY if hasattr(plant_address, 'CITY') else "Unknown",
            "state": plant_address.STATE if hasattr(plant_address, 'STATE') else "Unknown",
            "country": plant_address.COUNTRY if hasattr(plant_address, 'COUNTRY') else "Unknown",
            "zip": plant_address.ZIP if hasattr(plant_address, 'ZIP') else "Unknown"
        }
        result['contacts'] = [
            {
            "type": "Primary Contact",
            "name": f'{company_application.FirstName} {company_application.LastName}' if hasattr(company_application, 'FirstName') and hasattr(company_application, 'LastName') else "",
            "phone": company_application.Phone if hasattr(company_application, 'Phone') else "",
            "email": company_application.Email if hasattr(company_application, 'Email') else "",
            "designated": True,
            "role": "Initial communication and contract negotiations"
            }
        ]
        result['plants'] = [
            {
                "name": planttb.NAME if hasattr(planttb, 'NAME') else "Unknown",
                "location": plant_address.CITY if hasattr(plant_address, 'CITY') else "Unknown",
                "address": plant["address"],
            }
            #for plant in plants
        ]
        result['products'] = [
            {
            "source": "Source Temp",
            "labelName": product.get("PRODUCT_NAME"),
            "brandName": product.get("BRAND_NAME"),
            "labelCompany": product.get("LABEL_COMPANY"),
            "ConsumerIndustrial": "Industrial" if bool(product.get("INDUSTRIAL")) else "Consumer",
            "bulkShipped": bool(product.get("BLK")),
            "certification": product.get("Symbol") or product.get("SYMBOL"),
            "status": product.get("STATUS")
            }
            for product in products
        ]
        result['ingredients'] = [
            {

            "addedBy": "System Import",
            "addedDate": ingredient.get("DateAdded"),
            "brand": ingredient.get("BRAND_NAME"),
            "certification": ingredient.get("SYMBOL"),
            "ingredient": ingredient.get("INGREDIENT_NAME"),
            "manufacturer": ingredient.get("LABEL_COMPANY"),
            "ncrcId": ingredient.get("MERCHANDISE_ID"),
            "packaging": 'bulk' if bool(ingredient.get("BLK")) else 'non-bulk',
            "source": "Source temp",
            "status": ingredient.get("LabelStatus")

            }
            for ingredient in ingredients
        ]
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
        '''
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
        files = WFFile.query.filter(WFFile.ApplicationID == application_id).all()
        result['files'] = [
            {
                "fileId": file.FileID if hasattr(file, 'FileID') else 1,
                "fileName": file.FileName if hasattr(file, 'FileName') else None,
                "fileType": file.FileType if hasattr(file, 'FileType') else None,
                "filePath": file.FilePath if hasattr(file, 'FilePath') else None,
                "uploadedDate": file.UploadedDate.strftime('%Y-%m-%d') if hasattr(file, 'UploadedDate') else None,
                "description": file.Description if hasattr(file, 'Description') else None
            }
            for file in files
        ]
        messages = WFApplicationMessage.query.filter(WFApplicationMessage.ApplicationID == application_id).all()
        result['messages'] = [
            {
                "messageId": getattr(message, "MessageID", None),
                "fromUser": getattr(message, "FromUser", None),
                "toUser": getattr(message, "ToUser", None),
                "task_id": getattr(message, "TaskID", None),
                "task_instance_id": getattr(message, "TaskInstanceId", None),
                "messageText": getattr(message, "MessageText", None),
                "messageType": getattr(message, "MessageType", None),
                "priority": getattr(message, "Priority", None),
                "sentDate": message.SentDate.strftime("%Y-%m-%dT%H:%M:%S") if getattr(message, "SentDate", None) else None
            }
            for message in messages
        ]
        application_info = {}
        application_info["applicationInfo"] = result
        return jsonify(application_info), 200


def get_products(company_id: int, plant_id: int) -> list:
    sql = f"""
      SELECT TOP (10) [PRODUCT_NAME]
        ,[TOP_LEVEL_PRODUCT_NAME]
        ,[MERCHANDISE_ID]
        ,[BRAND_NAME]
        ,[Symbol]
        ,[STATUS]
        ,[LABEL_COMPANY]
        ,[INDUSTRIAL]
        ,[PESACH]
        ,[KITNIYOT]
        ,[CATEGORY_NAME]
        ,[LABEL_TYPE]
        ,[BLK]
        ,[SEAL_SIGN]
        ,[LABEL_SEQ_NUM]
        ,[DPM]
        ,[COMPANY_ID]
        ,[COMPANY_NAME]
        ,[PLANT_ID]
        ,[PLANT_NAME]
        ,[SRC_MAR_ID]
        ,[SRC_STREET1]
        ,[SRC_CITY]
        ,[SRC_STATE]
        ,[SRC_ZIP]
        ,[SRC_COUNTRY]
        ,[Plant_Country]
        ,[owns_id]
        ,[LABEL_ID]
        ,[PRODUCED_IN1_ID]
        ,[ACTIVE]
        ,[AS_STIPULATED]
        ,[GRP]
        ,[Confidential]
        ,[CONFIDENTIAL_TEXT]
        ,[OUP_REQUIRED]
        ,[Consumer]
        ,[LOChold]
        ,[Repack]
        ,[LOC_SELECTED]
        ,[CAS]
        ,[PassoverSpecialProduction]
        ,[PLANT_STATUS]
        ,[IsDairyEquipment]
        ,[RC]
    FROM [ou_kash].[dbo].[PRODUCT_GRID]
        where [COMPANY_ID] = {company_id}
        and [PLANT_ID] = {plant_id}
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
        SELECT TOP (20) [LOC]
            ,[LabelID]
            ,[INGREDIENT_NAME]
            ,[MERCHANDISE_ID]
            ,[BRAND_NAME]
            ,[SRC_MAR_ID]
            ,[LABEL_COMPANY]
            ,[SYMBOL]
            ,[GRP]
            ,[DPM]
            ,[BLK]
            ,[UKDID]
            ,[SEAL_SIGN]
            ,[PESACH]
            ,[AS_STIPULATED]
            ,[LABEL_SEQ_NUM]
            ,[COMPANY_ID]
            ,[PLANT_ID]
            ,[OWNS_ID]
            ,[LABEL_ID]
            ,[USED_IN1_ID]
            ,[SRC_STREET]
            ,[SRC_CITY]
            ,[SRC_STATE]
            ,[SRC_ZIP]
            ,[SRC_COUNTRY]
            ,[ACTIVE]
            ,[RAW_MATERIAL_CODE]
            ,[ALTERNATE_NAME]
            ,[AgencyID]
            ,[JobID]
            ,[CAS]
            ,[CTA]
            ,[CNTA]
            ,[LabelStatus]
            ,[Special_Status]
            ,[CompanyName]
            ,[PlantName]
            ,[PlantStatus]
            ,[IngredientInPlantStatus]
            ,[DateAdded]
            ,[PassoverProductionUse]
            ,[PlantCTA]
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