from flask import app, request, jsonify
from datetime import datetime
from flask import request, jsonify, session
import logging
import safrs
import json
from sqlalchemy.sql import text
from flask_jwt_extended import get_jwt, jwt_required

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass
   
    @app.route('/reload_cache', methods=['GET'])
    @jwt_required()
    def reload_cache(): 
        claims = get_jwt()
        if 'roles' not in claims:
            return jsonify({"msg": "Missing required roles"}), 403

        try:
            # Call the stored procedure to reload the cache
            from database.cache_service import DatabaseCacheService
            DatabaseCacheService.get_instance().reload()  
            return jsonify({"msg": "Cache reloaded successfully"}), 200
        except Exception as e:
            app_logger.error(f"Error reloading cache: {str(e)}")
            return jsonify({"msg": "Error reloading cache", "error": str(e)}), 500