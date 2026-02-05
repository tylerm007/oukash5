from flask_jwt_extended import get_jwt, jwt_required  
import datetime
from database.models import WFApplication
import database.models as models
from flask import request, jsonify
import logging
import safrs
from sqlalchemy.sql import text
import time
from security.system.authorization import Security

"""
Various endpoints to test workflow functionality and cleanup or reset tests
"""
db = safrs.DB 
session = db.session

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    @app.route('/createSubmissionApplication', methods=['GET','OPTIONS'])
    @jwt_required()
    def createSubmissionApplication():
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        args = request.args
        user = Security.current_user().Username
        jotform_id = args.get('jotform_id') or args.get('jotFormId') or args.get('filter[jotform_id]') or None
        jotform = session.query(models.JotFormCompany).filter(models.JotFormCompany.JotFormId == jotform_id).first() if jotform_id else None
        if jotform is None:
            return jsonify({"result": f'JotFormCompany with ID: {jotform_id} not found'}), 404 
        company_id = jotform.JotFormId
        company_name = jotform.companyName
        plants = jotform.JotFormPlantList
        submission_id = jotform.submission_id
        results = {}
        plant_ids = ""
        join = ""
        for plant in plants:
            plant_id = plant.PlantId
            if company_id is None or plant_id is None:
                return jsonify({"result": 'createSubmissionCompany requires companyId and plantId parameters'}), 400
            if plant.plantName.strip() == '': #No reason to create an empty plant
                continue
        
            application_id = create_new_submission_application(company_id=int(company_id), plant_id=plant_id, submission_id=submission_id, user=user)
            response = start_workflow(application_id, user, None)
            results[application_id] = {"Company": company_name, "company_id": company_id, "plant_ids": plant_ids, "workflow_response": response}
            app_logger.info(f'Application {application_id} created and workflow started with response: {response}')
        return jsonify({"status": f"submission application created successfully {results}"}), 200
    
    @app.route('/createApplication', methods=['GET','OPTIONS'])
    @jwt_required()
    def createApplication():
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        args = request.args
        user = Security.current_user().Username
        owns_id = args.get('owns_id') or args.get('ownsId') or None
        if owns_id is None:
            return jsonify({"result": 'ownsId parameter is required'}), 400
        owns_instance = models.OWNSTB.query.filter(models.OWNSTB.ID == owns_id).first()
        if not owns_instance:
            return jsonify({"result": f'Owns instance with ID: {owns_id} not found'}), 404
    
        companyID = owns_instance.COMPANY_ID
        plant_id = owns_instance.PLANT_ID
        company_plant = session.query(models.WFApplication).filter(models.WFApplication.CompanyID == companyID, models.WFApplication.PlantID == plant_id).first()
        if company_plant:
            return jsonify({"result": f'Application already exists for CompanyID: {companyID} and PlantID: {plant_id}'}), 400   
        access_token = request.headers.get('Authorization', '')
        application_id = create_new_application(companyID, plant_id, user)
        response = start_workflow(application_id, user, access_token)
        app_logger.info(f'Application {application_id} created and workflow started with response: {response}')
        return jsonify({"status": f"application created successfully {application_id} started"}), 200
    
    @app.route('/deleteApplication', methods=['GET','OPTIONS'])
    @jwt_required()
    def deleteApplication():    

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        application_id = request.args.get('application_id') or request.args.get('applicationId') or  request.args.get('applicationID') or None
        if not application_id:
            return jsonify({"result": 'applicationId parameter is required'}), 400
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        do_cleanup(application)
        return jsonify({"result": f'Cleanup completed for Application ID: {application_id} '}), 200

    @app.route('/generateApplications', methods=['GET','OPTIONS'])
    @jwt_required()
    def generateApplications():
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        cnt = request.args.get('app_count')
        offset = request.args.get('page[offset]') or 0
        data =[]
        sql = get_application_sql(int(cnt), int(offset) if cnt else 10)
        results = session.execute(text(sql)).fetchall()
        for result in results:
            owns_id = result.ID
            owns_instance = models.OWNSTB.query.filter(models.OWNSTB.ID == owns_id).first()
            if not owns_instance:
                continue
            companyID = owns_instance.COMPANY_ID
            plant_id = owns_instance.PLANT_ID
            company_plant = session.query(models.WFApplication).filter(models.WFApplication.CompanyID == companyID, models.WFApplication.PlantID == plant_id).first()
            if company_plant:
                continue   
            user = Security.current_user().Username
            application_id = create_new_application(companyID, plant_id, user)
            data.append(application_id)
            access_token = request.headers.get('Authorization', '')
            response = start_workflow(application_id, user, access_token)
            app_logger.info(f'Application {application_id} created and workflow started with response: {response}')
        return jsonify({"status": "applications created successfully", "applications": data}), 200

def create_new_application( company_id: int = 0, plant_id: int = 0, user: str = "admin"):
    #TODO should we validate CompaniID in COMPANYTB and PlantID in PLANTTB (and perhaps OWNSTB)?
    applicationNumber = WFApplication.query.count() + 10000
    application = WFApplication(
            Name="New Application",
            Description="Description of the new application",
            Status="NEW",
            CompanyID=company_id,
            PlantID=plant_id,
            SubmissionDate=datetime.datetime.now(datetime.timezone.utc),
            CreatedBy=user,
            CreatedDate=datetime.datetime.now(datetime.timezone.utc),
            Priority="NORMAL",
            ApplicationType="WORKFLOW",
            ApplicationNumber=applicationNumber,
    )
    session.add(application)
    session.commit()
    application_id = application.ApplicationID
    create_files(application_id)
    return application_id

def create_new_submission_application( company_id: int = 0, plant_id: int = 0, submission_id: str=None,user: str = "admin"):
    applicationNumber = WFApplication.query.count() + 10000
    application = WFApplication(
            Name="New Application",
            Description=f"Submission {submission_id} application",
            Status="NEW",
            CompanyID=0,
            PlantID=0,
            SubmissionCompany=company_id,
            SubmissionPlant=int(plant_id),
            SubmissionDate=datetime.datetime.now(datetime.timezone.utc),
            CreatedBy=user,
            CreatedDate=datetime.datetime.now(datetime.timezone.utc),
            Priority="NORMAL",
            ApplicationType="SUBMISSION",
            ApplicationNumber=applicationNumber,
    )
    session.add(application)
    session.commit()
    create_submission_files(application.ApplicationID)

    return application.ApplicationID
def create_submission_files(application_id:int):
    pass
def create_files(application_id:int):
    # sample recorfds only
    file= models.WFFile(
        ApplicationID=application_id,
        FileName="Application.pdf",
        FileType="PDF",
        UploadedBy="system",
        UploadedDate=datetime.datetime.now(datetime.timezone.utc).date(),
        Description="Test Document for Application",
        FilePath="https://uojca.sharepoint.com/:b:/r/teams/NewAPITeam/Shared%20Documents/NewAPI/dashboard_files/6295465435286943843.pdf?csf=1&web=1&e=Xgiwjd"
    )
    session.add(file)
    file2 = models.WFFile(
        ApplicationID=application_id,
        FileName="Product.pdf",
        FileType="PDF",
        UploadedBy="system",
        UploadedDate=datetime.datetime.now(datetime.timezone.utc).date(),
        Description="Test Document for Product",
        FilePath="https://uojca.sharepoint.com/:b:/r/teams/NewAPITeam/Shared%20Documents/NewAPI/dashboard_files/Bagel%20Chips_Onion_Garlic%20(2).pdf?csf=1&web=1&e=rJAXVr"
    )
    session.add(file2)
    file3 = models.WFFile(
        ApplicationID=application_id,
        FileName="Ingredient.jpg",
        FileType="JPG",
        UploadedBy="system",
        UploadedDate=datetime.datetime.now(datetime.timezone.utc).date(),
        Description="Test Document for Ingredient",
        FilePath="https://uojca.sharepoint.com/:i:/r/teams/NewAPITeam/Shared%20Documents/NewAPI/dashboard_files/Crackers%20Box%207-02%20(2).jpg?csf=1&web=1&e=KK1xRb"
    )
    session.add(file3)
    session.commit()

def start_workflow(application_id: int, start_by: str, access_token: str):
    from api.api_discovery.start_workflow import _start_workflow_async
    process_name = "OU Application Init"
    response = _start_workflow_async(process_name=process_name, application_id=int(application_id), started_by=start_by, priority="NORMAL", access_token=access_token)
    return response


def do_cleanup(application: models.WFApplication):
    application_id = application.ApplicationID
    session.execute(text(f"""
        DELETE FROM EventAction where [TaskInstanceId] IN (
            SELECT TaskInstanceId FROM TaskInstances where ApplicationId = {application_id}
        );
       
      
    """))
    session.commit()

    session.execute(text(f"""
        DELETE FROM TaskInstances where ApplicationId = {application_id};
    """))
    session.commit()
       
    session.execute(text(f"""
        DELETE from RoleAssigment where ApplicationId = {application_id};
        DELETE FROM WF_QuoteItems where QuoteID in (select QuoteID from WF_Quotes where ApplicationID = {application_id});
        DELETE FROM WF_Quotes where ApplicationID = {application_id};
        DELETE FROM WF_Files where ApplicationID = {application_id};
       
    """))
    session.commit()

    session.execute(text(f"""
         DELETE FROM WF_Applications where ApplicationID = {application_id};
    """))
    session.commit()


def get_application_sql(num_of_apps: int = 10, offset: int = 0) -> str:
    #Grab applications with between 5 and 30 ingredients
    sql = f"""
        select count(*) as CNT,ID
        FROM [ou_kash].[dbo].[OWNS_TB] app,
        [ou_kash].[dbo].[INGREDIENT_GRID_JOIN_USEDIN1] i
        WHERE i.[COMPANY_ID] = app.COMPANY_ID AND i.[PLANT_ID] = app.PLANT_ID
        and app.STATUS = 'Certified'
        and app.TYPE = 'Single'
        and app.ACTIVE = 1
        group by app.ID
        having count(*) > 5 and count(*) < 30
        ORDER BY app.ID
        OFFSET {offset} ROWS
        FETCH NEXT {num_of_apps} ROWS ONLY
    """
    return sql