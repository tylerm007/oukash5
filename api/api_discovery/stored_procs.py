from flask import request, jsonify, redirect, url_for, session
import logging
import safrs
from api.api_discovery.auto_discovery import discover_services
from database import models
import uuid


app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    
   
    @app.route('/InvoiceFees_View', methods=['GET','OPTIONS'], strict_slashes=False)
    def InvoiceFees_View():
        """
        Illustrates: 
        
        * #als: "Raw" SQLAlchemy table queries (non-mapped objects), by manual code

        $(venv) ApiLogicServer curl "http://localhost:5656/InvoiceFees_View?id=1"

        Returns:
            json: response
        """

        request_id = request.args.get('id')
        db = safrs.DB
        session = db.session
        #Security.set_user_sa()  # an endpoint that requires no auth header (see also @bypass_security)
        if request_id is None:
            results = session.query(models.t_INVOICE_FEES_DYN_) 
        else:                   # observe filter requires view_name.c
            #results = session.query(models.t_INVOICE_FEES_DYN_) \
            #        .filter(models.t_INVOICE_FEES_DYN_.c.ID == request_id)
            from sqlalchemy import text
            results = session.execute(text(f'select * from INVOICE_FEES_DYN where "ID" = {request_id}'))
        return_result = []
        for each_result in results:
            row = { 'id': each_result.ID, 'Type': each_result.TYPE, 'TOTAL_AMOUNT': each_result.TOTAL_AMOUNT}
            return_result.append(row)
        return jsonify({ "success": True, "result":  return_result})

