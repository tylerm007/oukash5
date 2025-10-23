from functools import wraps
from api.api_discovery import assign_role
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from api.api_discovery.assign_role import _assign_role   
import datetime
from urllib import response
from database.models import StageInstance, WFApplication, TaskInstance, TaskDefinition, ProcessInstance
import database.models as models
from flask import request, jsonify
import requests
import logging
import safrs
from sqlalchemy.sql import text
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

    @app.route('/hello_newer_service')
    def hello_newer_service():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/hello_newer_service?user=ApiLogicServer
        """
        user = request.args.get('user')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello from even_newer_service! from {user}'})
    
    @app.route('/test_parser', methods=['GET'])
    #jwt_required()
    def test_parser():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/test_parser?filter={"and":[{"name":{"like":"%a%"}}]}
                Invoke-RestMethod -Uri "http://localhost:5656/test_parser" -Method GET -ContentType "application/json"
        """
        filter = request.args.get('filter')
        app_logger.info(f'filter: {filter}')
        import requests
        filter1 =  '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"CATEGORY","op":"ilike","val":"%Nut%"},{"name":"NAME","op":"ilike","val":"%Company%"}]'
        endpoint = "COMPANYTB"
        response = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter1}')

        endpoint = "PLANTTB"
        filter2 =  '[{"name":"ACTIVE","op":"eq","val":1},{"name":"LABEL_SEQ_NUM","op":"gt","val":1}]'
        response2 = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter2}')

        endpoint = "COMPANYTB" 
        filter3 = '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"STATUS","op":"eq","val":"Certified"}]'
        response3 = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter3}')
        return jsonify({"result": f'filter: {filter}', "response": response.json(), "response2": response2.json(), "response3": response3.json()})

    @app.route('/create_application', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def create_application_endpoint():

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        args = request.args
        user = get_jwt().get("sub", "admin")
        applicationNumber = int(args.get('applicationNumber'))
        plant_id = args.get('plant_id', None)
        jot_application = session.query(models.CompanyApplication).filter(models.CompanyApplication.ID == applicationNumber).first()
        if jot_application is None:
            return jsonify({"result": f'Application with ApplicationNumber: {applicationNumber} does not exist with ID: {applicationNumber}'}), 400
        companyID = jot_application.CompanyID
        
        plant = session.query(models.PLANTTB).filter(models.PLANTTB.PLANT_ID == plant_id).first()
        if not plant:
            return jsonify({"result": f'Plant with PlantID: {plant_id} not found'}), 404
        application_id = create_new_application(applicationNumber, companyID, plant_id)
        process_id = start_workflow(application_id, user)
        #jot_application.PlantName = plant.NAME
        return jsonify({"result": f'Created application with ID: {application_id}, started process ID: {process_id}'})

    @app.route('/run_workflow_to_completion', methods=['GET','POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def run_workflow_to_completion_endpoint():
        '''
        Invoke-RestMethod -Uri "http://localhost:5656/run_workflow_to_completion?applicationNumber=1" -Method GET -ContentType "application/json" -Headers @{Authorization = "Bearer {<your_jwt_token>}
        '''
        access_token = request.headers.get("Authorization")
        args = request.args
        user = get_jwt().get("sub", "admin")
        applicationNumber = args.get('applicationNumber')
        scenario = args.get('scenario', 1)      
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationNumber == applicationNumber).first()
        if not application:
            return jsonify({"result": f'Application with ApplicationNumber: {applicationNumber} not found'}), 404
        run_workflow_to_completion(application, user=user, scenario=scenario, access_token=access_token)
        return jsonify({"result": f'Workflow run to completion'})

    @app.route('/reset_task_instances/<application_id>', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def reset_task_instances(application_id):
        # Implement reset logic here
        access_token = request.headers.get("Authorization")
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        do_reset(application_id)
        from datetime import datetime
        from api.api_discovery.complete_task import _complete_task
        start_instance_id = get_start_task(application_id)
        if not start_instance_id:
            return jsonify({"result": f'Start TaskInstance not found for Application ID: {application_id}'}), 404   
        _complete_task(start_instance_id, 'Started', 'system', 'Workflow started', access_token)
    
        role_assignment = models.RoleAssigment(
            ApplicationId=application.ApplicationID,
            Role="DISPATCH",
            Assignee="system",
            CreatedDate=datetime.utcnow()
        )
        session.add(role_assignment)
        session.commit()
        return jsonify({"result": f'Reset initiated for Application ID: {application_id}'})

    @app.route('/cleanup_workflow_data/<application_id>', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def cleanup_workflow_data(application_id):
        # Implement cleanup logic here
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        process_instance = session.query(models.ProcessInstance).filter(models.ProcessInstance.ApplicationId == application_id).first()
        process_id = process_instance.InstanceId if process_instance else None
        if not process_instance:
            return jsonify({"result": f'Process ID: {process_id} not found for Application ID: {application_id}'}), 404 
        do_cleanup(application_id, process_id)
        return jsonify({"result": f'Cleanup initiated for Application ID: {application_id}, Process ID: {process_id}'})

def create_new_application(applicationNumber: int, company_id: int, plant_id: int):
    from datetime import datetime
    #TODO should we validate CompaniID in COMPANYTB and PlantID in PLANTTB (and perhaps OWNSTB)?
    application = WFApplication(
            Name="New Application",
            Description="Description of the new application",
            Status="NEW",
            CompanyID=company_id,
            PlantID=plant_id,
            SubmissionDate=datetime.now().isoformat(),
            CreatedBy="tband",
            CreatedDate=datetime.now().isoformat(),
            Priority="HIGH",
            ApplicationNumber=applicationNumber,
            WFDashboardID=1
    )
    session.add(application)
    session.commit()
    application_id = application.ApplicationID
    create_products(application_id, company_id, plant_id)
    create_ingredients(application_id, company_id, plant_id)
    create_contacts(application_id, company_id, plant_id)
    create_files(application_id)
    get_company_address(company_id)
    get_plant_address(plant_id)
    app_logger.info(f'Created new application with ID: {application.ApplicationID}')
    return application.ApplicationID

def create_products(application_id: int, company_id: int, plant_id: int):
    sql = f"""
      SELECT TOP (1000) [PRODUCT_NAME]
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
    if not products:
        app_logger.info(f'No products found for company {company_id}: {plant_id}')
    rows = [dict(zip(row._fields, row)) for row in products]
    for row in rows:
        product = models.WFProduct(
            ApplicationID=application_id,
            # basic / legacy ids
            legacyId=row.get('MERCHANDISE_ID'),
            action='Add',
            doNotImport=False,
            message=row.get('CONFIDENTIAL_TEXT') or None,
            # label / product info
            labelType=row.get('LABEL_TYPE') or '',
            labelName=row.get('PRODUCT_NAME') or '',
            brandName=row.get('BRAND_NAME') or '',
            labelCompanyId=str(row.get('LABEL_COMPANY') or ''),
            distributorName=str(row.get('LABEL_COMPANY') or ''),
            group=row.get('GRP') or '',
            symbol=row.get('Symbol') or '',
            dpm=row.get('DPM') or '',
            category=row.get('CATEGORY_NAME') or '',
            # statuses / flags
            usePlantStatus=bool(row.get('PLANT_STATUS')),
            status=str(row.get('STATUS') or row.get('ACTIVE') or ''),
            legacyStatus=row.get('RC') or None,
            consumer=bool(row.get('Consumer')),
            industrial=bool(row.get('INDUSTRIAL')),
            finalized=bool(row.get('OUP_REQUIRED')),
            # processing metadata
            processedBy='system',
            processedDate=datetime.datetime.utcnow().date(),
            notes=row.get('CONFIDENTIAL_TEXT') or ''
        )
        session.add(product)
    session.commit()
    return rows

def create_ingredients(application_id:int, company_id:int, plant_id: int):
    sql = f"""
        SELECT TOP (1000) [LOC]
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
    
    if not ingredients:
        app_logger.info(f'No ingredients found for company {company_id}: {plant_id}')
    rows = [dict(zip(row._fields, row)) for row in ingredients]
    for row in rows:
        ingredient = models.WFIngredient(
            ApplicationID=application_id,
            Source = '',
            UKDId = row['UKDID'],
            IngredientName=row['INGREDIENT_NAME'],
            Manufacturer=row['LABEL_COMPANY'],
            Brand = row['BRAND_NAME'],
            Packaging = '',
            Agency = '',
            AddedDate = datetime.datetime.utcnow().date(),
            AddedBy = 'system',
            Status= row['IngredientInPlantStatus'],
            NCRCId = row['LabelID']
        )
        session.add(ingredient)
    session.commit()
    return rows

def get_company_address(company_id: int):
    company = session.query(models.COMPANYADDRESSTB).filter(models.COMPANYADDRESSTB.COMPANY_ID == company_id).first()
    if not company:
        app_logger.error(f'Company not found: {company_id}')
        return None
    address = f"{company.STREET1},{company.STREET2}, {company.CITY}, {company.STATE} {company.ZIP}"
    app_logger.info(f'Company Address: {address}')
    return company

def get_plant_address(plant_id: int):
    plant = session.query(models.PLANTADDRESSTB).filter(models.PLANTADDRESSTB.PLANT_ID == plant_id).first()
    if not plant:
        app_logger.error(f'Plant Address not found: {plant_id}')
        return None
    address = f"{plant.STREET1}, {plant.STREET2}, {plant.CITY}, {plant.STATE} {plant.ZIP}"
    app_logger.info(f'Plant Address: {address}')
    return plant

def create_contacts(application_id: int, company_id: int, plant_id: int):
    sql = f"""
        SELECT TOP (2) [pcID]
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
                (select TOP 2 OWNS_ID from [ou_kash].[dbo].[OWNS_TB] where COMPANY_ID = {company_id} and PLANT_ID = {plant_id})
    """
    result = session.execute(text(sql))
    contacts = result.fetchall()
    if not contacts:
        app_logger.error(f'Contact not found: {company_id} {plant_id}')
        return None
    rows = [dict(zip(row._fields, row)) for row in contacts]
    primary = True
    for row in rows:
        contact = models.WFContact(
            ApplicationID=application_id,
            ContactName=f"{row['FirstName']} {row['LastName']}",
            Title=row['Title'],
            ContactEmail=row['EMail'],
            ContactPhone=row['Voice'],
            CompanyID=company_id,
            CreatedDate=datetime.datetime.utcnow().date(),
            IsPrimary =  primary
        )
        session.add(contact)
        primary = False
    session.commit()
    app_logger.info(f'Contact Info: {rows}')
    return rows

def create_files(application_id:int):
    pass
    file= models.WFFile(
        ApplicationID=application_id,
        FileName="Application.pdf",
        FileType="PDF",
        UploadedBy="system",
        UploadedDate=datetime.datetime.utcnow().date(),
        Description="Test Document for Application",
        FilePath="/path/to/Application.pdf"
    )
    session.add(file)
    file2 = models.WFFile(
        ApplicationID=application_id,
        FileName="Product.pdf",
        FileType="PDF",
        UploadedBy="system",
        UploadedDate=datetime.datetime.utcnow().date(),
        Description="Test Document for Product",
        FilePath="/path/to/Product.pdf"
    )
    session.add(file2)
    file3 = models.WFFile(
        ApplicationID=application_id,
        FileName="Ingredient.pdf",
        FileType="PDF",
        UploadedBy="system",
        UploadedDate=datetime.datetime.utcnow().date(),
        Description="Test Document for Ingredient",
        FilePath="/path/to/Ingredient.pdf"
    )
    session.add(file3)
    session.commit()
def start_workflow(application_id: int, start_by: str):
    from api.api_discovery.start_workflow import _start_workflow
    process_name = "OU Application Init"
    response = _start_workflow(process_name, int(application_id), start_by, "NORMAL")
    return response['process_instance_id']


def find_all_stages_for_process(process_id):
    stages = StageInstance.query.filter(StageInstance.ProcessInstanceId == process_id).all()
    return [stage for stage in stages]

def find_all_pending_tasks(stage_id: int):
    """
    Find all pending tasks for a given stage, excluding SYSTEM (internal) tasks.
    
    """
    pending_tasks = []
    response = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id, models.TaskInstance.Status == 'PENDING').all()
    pending_tasks.extend([task for task in response])
    for task_instance in pending_tasks:
        taskDef = task_instance.TaskDef
        task_name = taskDef.TaskName if taskDef else 'Unknown'
        if task_instance and taskDef and taskDef.AssigneeRole.upper() == 'SYSTEM':
            print(f'Skipping System Task {task_name} - {task_instance} Role: {taskDef.AssigneeRole}')
            pending_tasks.remove(task_instance)
    return pending_tasks

def find_lane_end(stage_id: int):
    stage = session.query(models.StageInstance).filter(models.StageInstance.StageInstanceId == stage_id).first()
    if not stage:
        app_logger.error(f'StageInstance not found: {stage_id}')
        return 'NONE'
    task_instances = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id).all()
    for task_instance in task_instances:
        if task_instance.TaskDef.TaskType == 'LANEEND':
            return task_instance.Status
    return "NEW"

def find_task_flow(task_instance:TaskInstance):
    #task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
    if not task_instance:
        app_logger.error(f'TaskInstance not found: {task_instance.TaskInstanceId}')
        return []

    # Go To TaskFlow from TaskId and check to see if all the prior states are completed
    task_def = task_instance.TaskDef
    if not task_def:
        app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
        return []

    task_name = task_def.TaskName
    #stages_list = find_all_stages_for_process(task_instance.Stage.ProcessInstance.ProcessId)
    app_logger.info(f'Completing TaskInstance: {task_instance.TaskInstanceId} - {task_name}')
    task_flows_from = task_def.ToTaskTaskFlowList or []
    task_flows_to = task_def.TaskFlowList or []
    return task_flows_to

def complete_task(task_instance, scenario: int = 1):
    from api.api_discovery.complete_task import _complete_task
    task_instance_id = task_instance.TaskInstanceId
    task_name = task_instance.TaskDef.TaskName
    access_token = request.headers.get("Authorization")
    result = result_scenario(task_name, scenario)
    response = _complete_task(task_instance_id=task_instance_id, result=result, completed_by='tband', completion_notes='Task completed successfully', access_token=access_token, depth=0)
    app_logger.info(f'Complete Task {task_name}: {task_instance_id} response: {response}')

def result_scenario(task_name, scenario: int = 1) -> str:
    if scenario == 2:
        result = 'YES' if "to Withdrawn Y/N" in task_name else None
    else:
        result = 'NO' if "to Withdrawn Y/N" in task_name else None
    result = 'NO' if "Withdraw Application" in task_name else result
    result = 'YES' if "Needs NDA" in task_name else result
    result = 'YES' if "Is Inspection Needed" in task_name else result
    result = '2025-11-01' if "Schedule" in task_name else result
    result = 1000 if "Assign Invoice Amount" in task_name else result
    return result

def run_workflow_to_completion(application: WFApplication, user: str, scenario: int = 1, access_token: str = None):
    application_id = application.ApplicationID
    process_instance = session.query(models.ProcessInstance).filter(models.ProcessInstance.ApplicationId == application_id).first()
    if not process_instance:
        app_logger.error(f'ProcessInstance not found for Application ID: {application_id}')
        return
    process_id = process_instance.InstanceId
    stages_list = find_all_stages_for_process(process_id)
    completed_tasks = []
    for stage in stages_list:
        stage_id = stage.StageInstanceId
        stage_state = session.query(models.StageInstance).filter(models.StageInstance.StageInstanceId == stage_id).first()
        status = stage_state.Status # "'IN_PROGRESS'"
        name = stage.Lane.LaneName if stage.Lane else 'Unknown'
        app_logger.info(f'Start Processing Stage: {name} - {stage_id} Status: {status}')
        if status == 'IN_PROGRESS' and name == 'Initial':
            pending_tasks = find_all_pending_tasks(stage_id)
            for task_instance in pending_tasks:
                if task_instance.TaskDef.TaskName == 'AssignNCRC':
                    _assign_role(task_instance.TaskInstanceId, 'NCRC', user, application_id)
                    print(f'  Assign Role: {task_instance.TaskDef.TaskName}')
                next_pending_tasks = find_all_pending_tasks(stage_id)
                while len(next_pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                    for next_task_instance in next_pending_tasks:
                        complete_task(next_task_instance, scenario)
                        completed_tasks.append(next_task_instance.TaskInstanceId)
                        next_pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'NDA':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Inspection':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    if task_instance.TaskDef.TaskName == 'Mark Invoice Paid':
                        from api.api_discovery.event_action import _resolve_event
                        event_key = "INVOICE_98286" 
                        _resolve_event(event_key, user, access_token)
                        print(f'  Resolving EventAction for Task: {task_instance.TaskDef.TaskName} EventKey: {event_key}')
                    else:
                        # For testing, we auto-complete the scheduling task
                        print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                        complete_task(task_instance)
                        completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Ingredients':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Products':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Contract':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Certification':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

    stage_list = find_all_stages_for_process(process_id)
    for stage in stage_list:
        print(f'Stage {stage.Lane.LaneName} Status {stage.Status}')
    print(f"Workflow for application {application_id} completed {completed_tasks}.")
    app_logger.info(f"Workflow for application {application_id} completed {completed_tasks}.")

def process_task_flow(task_instance, stage_instance_id, completed_tasks):
    task_flow_instances = find_task_flow(task_instance)
    for task_flow in task_flow_instances:
        next_task_def = session.query(models.TaskDefinition).filter(models.TaskDefinition.TaskId == task_flow.ToTaskId).first()
        if next_task_def and next_task_def.AssigneeRole != 'SYSTEM' and task_instance.Status == 'COMPLETED':
            next_task_instance = session.query(models.TaskInstance).filter(models.TaskInstance.TaskId == next_task_def.TaskId, models.TaskInstance.StageId == stage_instance_id).first()
            if next_task_instance and next_task_instance.Status in ['NEW','PENDING'] and next_task_instance.TaskInstanceId not in completed_tasks:
                print(f'      Next Task to complete: {next_task_def.TaskName} Status: {next_task_instance.Status}')
                complete_task(next_task_instance)
                completed_tasks.append(next_task_instance.TaskInstanceId)
                process_task_flow(next_task_instance, stage_instance_id, completed_tasks)
def do_reset(application_id):
    session.execute(text(f"""
        UPDATE TaskInstances SET Status = 'NEW', Result = NULL, ResultData = NULL, ErrorMessage = NULL 
        WHERE StageId IN (SELECT StageInstanceId FROM StageInstance WHERE ProcessInstanceId = 
            (SELECT InstanceId FROM ProcessInstances WHERE ApplicationId = {application_id})
        );
       
        UPDATE StageInstance SET Status = 'NEW' 
        WHERE ProcessInstanceId IN 
            (SELECT InstanceId FROM ProcessInstances WHERE ApplicationId = {application_id});
        

        UPDATE ProcessInstances SET Status = 'NEW' 
        WHERE ApplicationId = {application_id};
        

        UPDATE WFApplication SET Status = 'NEW' 
        WHERE ApplicationId = {application_id};
       
    """))
    session.commit()

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

def get_start_task(application_id):
    #start_task = session.query(models.TaskDefinition).filter(models.TaskDefinition.ProcessId == process_id, models.TaskDefinition.AssigneeRole == 'SYSTEM').first()
    response = session.execute(text(f"""
        select TaskInstanceId
            FROM [dashboard].[dbo].[TaskInstances] ti,
            [dashboard].[dbo].[TaskDefinitions] td
            where ti.TaskId = td.TaskId
            and td.TaskType = 'START'
            and  ti.StageId in (
                Select StageInstanceId from StageInstance where ProcessInstanceId = 
                (Select InstanceId from ProcessInstances where ApplicationId = {application_id})
            )
    """))
    row = response.fetchone()
    return row[0] if row else None