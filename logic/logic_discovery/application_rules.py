from datetime import datetime
from database.models import TaskDefinition, TaskInstance
from integration.workflow import python_engine
from flask import app, request, jsonify, session
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import logging
import safrs
from config.config import Args
from config.config import Config
import datetime, os
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.logic_bank import Rule
import database.models as models

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session
def verify_requests(row: models.WFApplication, old_row: models.WFApplication, logic_row: LogicRow):
    '''
    Verify that the number of requests for an application does not exceed the allowed limit.
    '''
    if logic_row.ins_upd_dlt == 'upd':
        company_id = row.CompanyID
        plant_id = row.PlantID
        if row.verify_company == 1 and old_row.verify_company == 0:    
            if company_id is None:
                logic_row.log("CompanyID is None; cannot verify requests.")
                raise Exception("CompanyID is required for verification.")
                # COMPANYTB has CompanyID
            company = models.COMPANYTB.query.filter_by(COMPANY_ID=company_id).first()
            if not company:
                logic_row.log(f"Company with ID {company_id} does not exist in Company Table.")
                raise Exception(f"Company with ID {company_id} does not exist in Company Table.")
        if row.verify_plant == 1 and old_row.verify_plant == 0:
            if plant_id is None:
                logic_row.log("PlantID is None; cannot verify requests.")
                raise Exception("PlantID is required for verification.")
            # PLANTTB has PlantID - should check OWNSTB Company-Plant
            plant = models.PLANTTB.query.filter_by(PLANT_ID=plant_id).first()
            if not plant:
                logic_row.log(f"Plant with ID {plant_id} does not exist in Plant Table.")
                raise Exception(f"Plant with ID {plant_id} does not exist in Plant Table.")
            if company_id is not None and plant_id is not None:
                ownstb = models.OWNSTB.query.filter_by(COMPANY_ID=company_id, PLANT_ID=plant_id).first()
                if not ownstb:
                    logic_row.log(f"Company ID {company_id} does not own Plant ID {plant_id} in OWNSTB.")
                    raise Exception(f"Company ID {company_id} does not own Plant ID {plant_id} in OWNSTB.")
    return True
def declare_logic():
    pass

    Rule.row_event(on_class=models.WFApplication, calling=verify_requests)