import logging
import api.system.api_utils as api_utils
import safrs
from flask import request, jsonify
from safrs import jsonapi_rpc
from database import models


# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ Customize API - new end points for services 
    
        Brief background: see readme_customize_api.md

        Your Code Goes Here
    
    """
    
    app_logger.debug("api/customize_api.py - expose custom services")

    from api.api_discovery.auto_discovery import discover_services
    discover_services(app, api, project_dir, swagger_host, PORT)

    @app.route('/plant_details', methods=['GET','OPTIONS'], strict_slashes=False)
    def plant_details():
        """
        Illustrates: 
        
        * #als: "Raw" SQLAlchemy table queries (non-mapped objects), by manual code

        PS> Invoke-RestMethod -Uri "http://localhost:5656/plant_details?plant_id=1"

        Returns:
            json: response
        """
        from database import models
        plant_id = request.args.get('plant_id',2539001)
        
        #Security.set_user_sa()  # an endpoint that requires no auth header (see also @bypass_security)
        if plant_id is None:
            return jsonify('plant_id is required'), 400
        plant = models.PLANTTB.query.filter(models.PLANTTB.PLANT_ID == plant_id).first()
        if plant is None:
            return jsonify(f'Plant not found for plant_id {plant_id}'), 400
        
        address = models.PLANTADDRESSTB.query.filter(models.PLANTADDRESSTB.PLANT_ID == plant_id).first()
        owns = models.OWNSTB.query.filter(models.OWNSTB.PLANT_ID == plant_id).all()
        for own in owns:
            usedin_list = own.USEDIN1TBList
            produced_in_list = own.ProducedIn1TbList
        result = { "plant": plant.to_dict(), 
                    "address": address.to_dict() if address else None,
                    "owns": [ own.to_dict() for own in owns ],
                    "used_in": [ used_in.to_dict() for used_in in usedin_list ],
                    "produced_in": [ produced_in.to_dict() for produced_in in produced_in_list ]
                    }  
        return jsonify({ "success": True, "result":  result})
    
    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost::5656/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://apilogicserver.github.io/Docs/API-Customize/

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})


    @app.route('/stop')
    def stop():  # test it with: http://localhost:5656/stop?msg=API stop - Stop API Logic Server
        """
        Use this to stop the server from the Browser.

        See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """

        import os, signal

        if not os.getenv('APILOGICPROJECT_STOP_OK'):
            return jsonify({ "success": False, "message": "Shutdown not enabled" })

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })