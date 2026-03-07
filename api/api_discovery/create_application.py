from re import sub
from unittest import result
import flask
from flask_jwt_extended import get_jwt, jwt_required  
import datetime
import database.models as models
from database.models import WFApplication
import database.oukash_models as oukash_models
import database.submission_models as submission_models
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

    @app.route('/createSubmissionApplication', methods=['GET','OPTIONS'])
    @jwt_required()
    def createSubmissionApplication():
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        args = request.args
        user = Security.current_user().Username
        application_id = args.get('application_id') or args.get('applicationId') or args.get('filter[application_id]') or None
        application = session.query(submission_models.SubmissionApplication).filter(submission_models.SubmissionApplication.SubmissionAppId == application_id).first() if application_id else None
        if application is None:
            return jsonify({"result": f'SubmissionApplication with application_id: {application_id} not found'}), 404 
        company_id = application.SubmissionAppId
        company_name = application.companyName
        plants = application.SubmissionPlantList
        submission_id = application.submission_id
        
        
        if company_id is None:
            return jsonify({"result": 'create Submission Application requires companyId parameters'}), 400
        
        application_id = create_new_submission_application(company_id=int(company_id), submission_id=submission_id, user=user)
        response = start_workflow(application_id, user, None)
        result = {"Company": company_name, "company_id": company_id, "workflow_response": response}
        app_logger.info(f'Application {application_id} created and workflow started with response: {response}')
        return jsonify({"status": f"submission application created successfully {result}"}), 200
    
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
        owns_instance = oukash_models.OWNSTB.query.filter(oukash_models.OWNSTB.ID == owns_id).first()
        if not owns_instance:
            return jsonify({"result": f'Owns instance with ID: {owns_id} not found'}), 404
        
        submission_id = args.get('submission_id') or args.get('submissionId') or None
        companyID = owns_instance.COMPANY_ID
        plant_id = owns_instance.PLANT_ID
        company_plant = session.query(models.WFApplication).filter(models.WFApplication.CompanyID == companyID, models.WFApplication.PlantID == plant_id).first()
        if company_plant:
            return jsonify({"result": f'Application already exists for CompanyID: {companyID} and PlantID: {plant_id}'}), 400   
        access_token = request.headers.get('Authorization', '')
        application_id = create_new_application(companyID, plant_id, int(owns_id), submission_id, user)
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
            owns_instance = oukash_models.OWNSTB.query.filter(oukash_models.OWNSTB.ID == owns_id).first()
            if not owns_instance:
                continue
            companyID = owns_instance.COMPANY_ID
            plant_id = owns_instance.PLANT_ID
            company_plant = session.query(models.WFApplication).filter(models.WFApplication.CompanyID == companyID, models.WFApplication.PlantID == plant_id).first()
            if company_plant:
                continue   
            user = Security.current_user().Username
            application_id = create_new_application(companyID, plant_id=plant_id, owns_id=owns_id, user=user)
            data.append(application_id)
            access_token = request.headers.get('Authorization', '')
            response = start_workflow(application_id, user, access_token)
            app_logger.info(f'Application {application_id} created and workflow started with response: {response}')
        return jsonify({"status": "applications created successfully", "applications": data}), 200

def create_new_application( company_id: int = 0, plant_id: int = 0, owns_id:int = 0, submission_id: str=None, user: str = "admin"):
    applicationNumber = owns_id if owns_id != 0 else WFApplication.query.count() + 10000
    # ExternalAppRef is INT - safely convert submission_id string to int, or None
    try:
        external_ref = int(submission_id) if submission_id is not None else None
    except (ValueError, TypeError):
        external_ref = None
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
            ExternalAppRef=external_ref
    )
    session.add(application)
    session.commit()
    application_id = application.ApplicationID
    link_submission_to_application(application_id, company_id, plant_id, owns_id, submission_id)
    #create_files(application_id)
    return application_id

def submsisson_request_process( app: flask = None):
    # Placeholder for any specific processing needed for submission applications before linking to main application
    from flask import current_app, has_request_context

    if not app:
        try:
            app = current_app._get_current_object()
        except RuntimeError:
            app_logger.error("❌ No Flask app context available for submsisson_request_process - background task may fail")
            return

    with app.app_context():
        submission_requests = session.query(submission_models.SubmissionRequest).filter(submission_models.SubmissionRequest.SubmissionStatus == 'New', submission_models.SubmissionRequest.SubmissionType=='INTAKE').all()
        for submission_request in submission_requests:
            submission_app_id = submission_request.SubmissionAppId
            submission_application = session.query(submission_models.SubmissionApplication).filter(submission_models.SubmissionApplication.SubmissionAppId == submission_app_id).first()

            if not submission_application:
                submission_request.SubmissionStatus= 'Failed'
                submission_request.SubmissionMessage = f"No SubmissionApplication found for SubmissionAppId: {submission_id}"
                submission_request.update_date = datetime.datetime.now(datetime.timezone.utc)
                session.add(submission_request)
                session.commit()
            else:
                try:
                    submission_request.SubmissionStatus= 'Processed'
                    company_id = submission_application.SubmissionAppId
                    submission_id = submission_application.submission_id
                    application_id = create_new_submission_application(company_id=company_id, submission_id=submission_id, user="system")
                    submission_request.ApplicationId = application_id
                    session.add(submission_request)
                    session.commit()
                    session.flush()
                    from api.api_discovery.start_workflow import _start_workflow_async
                    process_name = "OU Application Init"
                    response = _start_workflow_async(process_name=process_name, application_id=int(application_id), started_by='system', priority="NORMAL", access_token=None)
                    submission_request.update_date = datetime.datetime.now(datetime.timezone.utc)
                    submission_request.SubmissionMessage = f"SubmissionApplication with ID: {submission_application.SubmissionAppId} found for SubmissionAppId: {submission_id} created WFApplication with ID: {application_id} Start Workflow respomse: {response}"
                    session.add(submission_request)
                    session.commit()
                except Exception as e:
                    submission_request.SubmissionStatus = 'Failed'
                    submission_request.SubmissionMessage = f"Error creating submission application: {e}"
                    session.add(submission_request)
                    session.commit()
    

def create_new_submission_application( company_id: int = 0, submission_id: str=None,user: str = "admin"):
    # ApplicationNumber is INT - never assign submission_id (string) directly as it causes arithmetic overflow
    # submission_id is stored in ExternalAppRef if it's a valid int, otherwise use count-based number
    applicationNumber =  WFApplication.query.count() + 10000
    application = WFApplication(
            Name="New Application",
            Description=f"Submission {submission_id} application",
            Status="NEW",
            CompanyID=0,
            PlantID=0,
            ExternalAppRef=company_id,
            WFLinkedApp=0,
            SubmissionDate=datetime.datetime.now(datetime.timezone.utc),
            CreatedBy=user,
            CreatedDate=datetime.datetime.now(datetime.timezone.utc),
            Priority="NORMAL",
            ApplicationType="SUBMISSION",
            ApplicationNumber=applicationNumber,
    )
    session.add(application)
    session.commit()
    try:
        create_submission_files(application.ApplicationID)
    except Exception as e:
        app_logger.error(f"Error in submission application and matchers creation: {e}")

    return application.ApplicationID

def create_submission_files(application_id:int):
    # TODO use actual SubmissionFiles
    file_links = session.query(SubmissionFileLink).filter(SubmissionFileLLink.SubmissionAppId == application_id).all()
    for file_link in file_links:
        productFileURL = file_link.productFileURL
        ingredientFileURL = file_link.ingredientFileURL
        if productFileURL:
            filename = productFileURL.split("/")[-1]
            filetype = filename.split(".")[-1].upper()
            file= models.WFFile(
                ApplicationID=application_id,
                FileName=filename,
                FileType=filetype,
                UploadedBy="system",
                UploadedDate=datetime.datetime.now(datetime.timezone.utc).date(),
                Description="Customer Provided",
                FilePath=productFileURL
            )
            session.add(file)
        if ingredientFileURL:
            filename = ingredientFileURL.split("/")[-1]
            filetype = filename.split(".")[-1].upper()
            file= models.WFFile(
                ApplicationID=application_id,
                FileName=filename,
                FileType=filetype,
                UploadedBy="system",
                UploadedDate=datetime.datetime.now(datetime.timezone.utc).date(),
                Description="Customer Provided",
                FilePath=ingredientFileURL
            )
            session.add(file)
        
    session.commit()

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
        DELETE FROM TaskEvents where [ApplicationId] = {application_id};
        
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

def link_submission_to_application(application_id:int, company_id:int, plant_id:int,owns_id: int,  submission_id: str):
    if submission_id is None:
        return
    submission_application = session.query(models.WFApplication).filter(models.WFApplication.ExternalAppRef == submission_id, models.WFApplication.ApplicationType == 'SUBMISSION').first()
    if submission_application:
        submission_application.CompanyID = company_id
        session.add(submission_application)
        session.commit()
        task_instances = session.query(models.TaskInstance).filter(models.TaskInstance.ApplicationId == submission_id).all()
        for task_instance in task_instances:
            task_def = task_instance.task_definition
            if "ResolvePlant" in task_def['TaskName'] and task_instance.Result == submission_id:
                result_data = task_instance.ResultData
                if isinstance(result_data, str) and result_data.startswith('{'):
                    result_data = json.loads(result_data.replace("'", '"',1000))
                    result_data['CompanyID'] = company_id
                    result_data['PlantID'] = plant_id
                    result_data['OwnsID'] = owns_id
                    result_data['WFID'] = application_id
                    task_instance.ResultData = json.dumps(result_data)
                    session.add(task_instance)
                    session.commit()
                    return

        