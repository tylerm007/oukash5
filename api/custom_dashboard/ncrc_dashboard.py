from email.mime import application
from flask import request, jsonify
from datetime import datetime
from database.models import PLANTADDRESSTB, ProcessDefinition, TaskDefinition, ProcessInstance, WFIngredient, WFProduct, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition
from flask import request, jsonify, session
import logging
import uuid
import safrs

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass


    @app.route('/get_ncrc_data', methods=['GET',"OPTIONS"])
    def get_ncrc_data():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.
        * Returns NCRC data in JSON format

        Test it with:
        
        Invoke-RestMethod -Uri "http://localhost:5656/get_ncrc_data?applicationId=1" -Method GET -ContentType "application/json"
        
        Returns JSON response with application data including:
        - Application info (ID, submission date, status)
        - Company details (name, category, certification status)
        - Plant information (name, location, address)
        - Products list (label names, brands, certifications)
        - Ingredients list (NCRC IDs, manufacturers, certifications)
        """
        application_id = request.args.get('applicationId',1, type=int)
        app_logger.info(f'{application_id}')
        from database.models import CompanyApplication, WFApplication, COMPANYTB, OWNSTB, PLANTTB, PLANTADDRESSTB, LabelTb, MERCHTB, USEDIN1TB
        wf_application = WFApplication.query.filter_by(ApplicationID=application_id).first()
        if not wf_application:
            return jsonify({"error": "WF_Application not found"}), 404
        application = wf_application.to_dict()

        company_application = CompanyApplication.query.filter_by(ID=application['ApplicationNumber']).first()
        if not company_application:
            return jsonify({"error": f"Company application {application['ApplicationNumber']} not found"}), 404

        company_id = application['CompanyID'] if 'CompanyID' in application else None
        if not company_id:
            return jsonify({"error": "Company ID not found for application"}), 404
        
        company = COMPANYTB.query.filter_by(COMPANY_ID=company_id).first()
        if not company:
            return jsonify({"error": "Company not found"}), 404 
        
        owns = OWNSTB.query.filter_by(COMPANY_ID=company_id).all()
        if not owns:
           return jsonify({"error": f"Ownership not found for company ID: {company_id}"}), 404

        plant_id = application['PlantID'] or -9999
        planttb = PLANTTB.query.filter_by(PLANT_ID=plant_id).first()
        #plants = PLANTTB.query.filter(PLANTTB.PLANT_ID.in_(own.PLANT_ID for own in owns)).all()
        if not planttb:
            app.logger.info(f'No plant found for company ID: {company_id} in Application {application_id}')    
        #for plant in plants:
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
        address = PLANTADDRESSTB.query.filter_by(PLANT_ID=plant_id).first()
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
        else:
            plant["address"] = {
                "street": company_application.Street1 if hasattr(company_application, 'Street1') else "Unknown",
                "line2": company_application.Street2 if hasattr(company_application, 'Street2') else "Unknown",
                "city": company_application.City if hasattr(company_application, 'City') else "Unknown",
                "state": company_application.State if hasattr(company_application, 'State') else "Unknown",
                "zip": company_application.Zip if hasattr(company_application, 'Zip') else "Unknown",
                "country": company_application.Country if hasattr(company_application, 'Country') else "Unknown",
                "type": "Unknown"
            }

        plant["contacts"] =  {
                "name": "John Mitchell",
                "title": "Plant Manager",
                "phone": "(585) 555-0123",
                "email": "j.mitchell@happycowmills.com"
            }
        
        application['Plants'] = plant
        products = WFProduct.query.filter_by(ApplicationID=application_id).all()
        application['Products'] = products
        ingredients = WFIngredient.query.filter_by(ApplicationID=application_id).all()
        application['Ingredients'] = ingredients
        result = {
            "applicationId": company_application.ID,
            "submissionDate": company_application.dateSubmitted.strftime('%Y-%m-%d') if hasattr(company_application, 'dateSubmitted') and company_application.dateSubmitted else "UNKNOWN",
            "status": application.Status if hasattr(application, 'Status') else "Pending",
            "kashrusCompanyId": company_application.CompanyID if hasattr(company_application, 'CompanyID') else "NOT ENTERED",
            "kashrusStatus": 'UNKNOWN', # TODO company_application.KashrusStatus if hasattr(company_application, 'KashrusStatus') else "Company Created",
            "primaryContact": f'{company_application.FirstName} {company_application.LastName}' 
        }
        result['company'] = {
            "name": company_application.CompanyName if hasattr(company_application, 'CompanyName') else "Happy Cow Mills Inc.",
            "category": company_application.Category if hasattr(company_application, 'Category') else "Pharmaceutical / Nutraceutical",
            "currentlyCertified": company_application.CurrentlyCertified if hasattr(company_application, 'CurrentlyCertified') else False,
            "everCertified": company_application.EverCertified if hasattr(company_application, 'EverCertified') else False,
            "website": company_application.Website if hasattr(company_application, 'Website') else "www.happycowmills.com",
            "address": {
                "street": company_application.Street if hasattr(company_application, 'Street') else "1250 Industrial Parkway",
                "line2": company_application.Street2 if hasattr(company_application, 'Street2') else "Building A, Suite 100",
                "city": company_application.City if hasattr(company_application, 'City') else "Rochester",
                "state": company_application.State if hasattr(company_application, 'State') else "NY",
                "country": company_application.Country if hasattr(company_application, 'Country') else "USA",
                "zip": company_application.Zip if hasattr(company_application, 'Zip') else "14624"
            }
        }
        result['address'] = {
            "street": application.Address.Street if hasattr(application, 'Address') and hasattr(application.Address, 'Street') else "Unknown",
            "city": application.Address.City if hasattr(application, 'Address') and hasattr(application.Address, 'City') else "Unknown",
            "state": application.Address.State if hasattr(application, 'Address') and hasattr(application.Address, 'State') else "Unknown",
            "country": application.Address.Country if hasattr(application, 'Address') and hasattr(application.Address, 'Country') else "Unknown",
            "zip": application.Address.Zip if hasattr(application, 'Address') and hasattr(application.Address, 'Zip') else "Unknown"
        }
        result['contacts'] = [
            {
            "type": "Primary Contact",
            "name": f'{company_application.FirstName} {company_application.LastName}' if hasattr(company_application, 'FirstName') and hasattr(company_application, 'LastName') else "John Mitchell",
            "phone": company_application.Phone if hasattr(company_application, 'Phone') else "9176966517",
            "email": company_application.Email if hasattr(company_application, 'Email') else "john@happycowmills.com",
            "designated": True,
            "role": "Initial communication and contract negotiations"
            }
        ]
        result['plants'] = [
            {
                "name": planttb.NAME if hasattr(planttb, 'NAME') else "Unknown",
                "location": planttb.LOCATION if hasattr(planttb, 'LOCATION') else "Unknown",
                "address": plant["address"],
            }
            #for plant in plants
        ]
        result['products'] = [
            {
                "source": product.Source if hasattr(product, 'Source') else "Brands File 1",
                "labelName": product.LabelName if hasattr(product, 'LabelName') else "Yecora Rojo Flour",
                "brandName": product.BrandName if hasattr(product, 'BrandName') else "cow Mill",
                "labelCompany": product.LabelCompany if hasattr(product, 'LabelCompany') else "cow Mill",
                "consumerIndustrial": product.ConsumerIndustrial if hasattr(product, 'ConsumerIndustrial') else "Consumer",
                "bulkShipped": product.BulkShipped if hasattr(product, 'BulkShipped') else True,
                "certification": product.Certification if hasattr(product, 'Certification') else "OU"
            }
            for product in application['Products']
        ]
        result['ingredients'] = [
            {
                "ncrcId": ingredient.NcrcId if hasattr(ingredient, 'NcrcId') else "ING-2025-1001",
                "ingredient": ingredient.Ingredient if hasattr(ingredient, 'Ingredient') else "Ryman Rye Grain",
                "manufacturer": ingredient.Manufacturer if hasattr(ingredient, 'Manufacturer') else "Jones Farms Organics",
                "brand": ingredient.Brand if hasattr(ingredient, 'Brand') else "Jones Farms Organics",
                "packaging": ingredient.Packaging if hasattr(ingredient, 'Packaging') else "bulk",
                "certification": ingredient.Certification if hasattr(ingredient, 'Certification') else "OU",
                "source": ingredient.Source if hasattr(ingredient, 'Source') else "File 1",
                "addedDate": ingredient.AddedDate.strftime('%Y-%m-%d') if hasattr(ingredient, 'AddedDate') and ingredient.AddedDate else "2025-07-17",
                "addedBy": ingredient.AddedBy if hasattr(ingredient, 'AddedBy') else "System Import",
                "status": ingredient.Status if hasattr(ingredient, 'Status') else "Original"
            }
            for ingredient in application['Ingredients']    
        ]
        application_info = {}
        application_info["applicationInfo"] = result
        return jsonify(application_info), 200