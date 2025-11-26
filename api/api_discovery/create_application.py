from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from api.api_discovery.assign_role import _assign_role   
import datetime
from database.models import CompanyApplication, StageInstance, WFApplication, TaskInstance, TaskDefinition, ProcessInstance, WFUser
import database.models as models
from flask import request, jsonify
import logging
import safrs
from sqlalchemy.sql import text
from types import SimpleNamespace
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
    
    @app.route('/createApplication', methods=['GET','OPTIONS'])
    @admin_required()
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
        access_token = request.headers.get('Authorization', '')
        application_id = create_new_application(companyID, plant_id, user)
        response = start_workflow(application_id, user, access_token)
        app_logger.info(f'Application {application_id} created and workflow started with process instance ID: {response["process_instance_id"]}')
        return jsonify({"status": f"application created successfully {application_id} started"}), 200
    
    @app.route('/deleteApplication', methods=['GET','OPTIONS'])
    @admin_required()
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
        process_instance = session.query(models.ProcessInstance).filter(models.ProcessInstance.ApplicationId == application_id).first()
       
        if not process_instance:
            return jsonify({"result": f'Workflow Process ID: {process_id} not found for Application ID: {application_id}'}), 404 
        process_id = process_instance.InstanceId if process_instance else None
        do_cleanup(application_id, process_id)
        return jsonify({"result": f'Cleanup completed for Application ID: {application_id}, Process ID: {process_id}'}), 200


def create_new_application( company_id: int = 0, plant_id: int = 0, user: str = "admin"):
    #TODO should we validate CompaniID in COMPANYTB and PlantID in PLANTTB (and perhaps OWNSTB)?
    applicationNumber = WFApplication.query.count() + 1000
    application = WFApplication(
            Name="New Application",
            Description="Description of the new application",
            Status="NEW",
            CompanyID=company_id,
            PlantID=plant_id,
            SubmissionDate=datetime.datetime.now(datetime.timezone.utc),
            CreatedBy=user,
            CreatedDate=datetime.datetime.now(datetime.timezone.utc),
            Priority="HIGH",
            ApplicationNumber=applicationNumber,
    )
    session.add(application)
    session.commit()
    application_id = application.ApplicationID
    create_files(application_id)
    return application_id


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
        FileType="JPEG",
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

def find_all_stages_for_process(process_id):
    stages = StageInstance.query.filter(StageInstance.ProcessInstanceId == process_id).order_by(StageInstance.LaneId).all()
    return [stage for stage in stages]

def do_cleanup(application_id, process_id):
    session.execute(text(f"""
        DELETE FROM EventAction where [TaskInstanceId] IN (
            SELECT TaskInstanceId FROM TaskInstances where StageId IN ( 
                SELECT StageInstanceId FROM StageInstance where ProcessInstanceId = {process_id}
            )
        );
        DELETE FROM TaskComments where [ProcessInstanceId] = {process_id};
        DELETE FROM WorkflowHistory where [InstanceId] = {process_id};
      
    """))
    session.commit()
    stage_list = find_all_stages_for_process(process_id)
    for stage in stage_list:
        session.execute(text(f"""
            DELETE FROM TaskInstances where StageId = {stage.StageInstanceId};
        """))
        session.commit()
        session.execute(text(f"""
            DELETE FROM StageInstance where StageInstanceId = {stage.StageInstanceId};
        """))
        session.commit()
    session.execute(text(f"""
        DELETE from RoleAssigment where ApplicationId = {application_id};
        DELETE FROM ProcessInstances where ApplicationId = {application_id};
        DELETE FROM WF_ApplicationComments where ApplicationID = {application_id};
        DELETE FROM WF_ApplicationMessages where ApplicationID = {application_id};
        DELETE FROM WF_Products where ApplicationId = {application_id};
        DELETE FROM WF_Ingredients where ApplicationId = {application_id};   
        DELETE FROM WF_Contacts where ApplicationId = {application_id};
        DELETE FROM WF_QuoteItems where QuoteID in (select QuoteID from WF_Quotes where ApplicationID = {application_id});
        DELETE FROM WF_Quotes where ApplicationId = {application_id};
        DELETE FROM WF_Files where ApplicationId = {application_id};
        DELETE FROM WF_Applications where ApplicationId = {application_id};
       
    """))
    session.commit()
