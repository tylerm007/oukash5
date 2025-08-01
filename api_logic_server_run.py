#!/usr/bin/env python3

###############################################################################
# 🚀 API Logic Server - AUTO-GENERATED MICROSERVICE
#
# This file starts a COMPLETE, WORKING microservice with:
#   ✅ Admin Web App at http://localhost:5656 (React-based, multi-table CRUD)
#   ✅ JSON:API endpoints at http://localhost:5656/api/* (auto-generated from database)
#   ✅ Swagger documentation at http://localhost:5656/api
#   ✅ Business logic engine (declarative rules)
#   ✅ Security framework (authentication/authorization)
#
# 🎯 TO RUN:
#    Press F5 in VSCode, or run: python api_logic_server_run.py
#
# 🌐 TO ACCESS:
#    Admin App: http://localhost:5656
#    API Docs:  http://localhost:5656/api
#
# 📝 TO CUSTOMIZE:
#    See docs/COPILOT_GUIDE.md for GitHub Copilot guidance
#    Logic: logic/declare_logic.py
#    API: api/customize_api.py
#    Security: security/declare_security.py
#
#    You typically do not customize this file.
#
#    (v 15.00.38, July 06, 2025 22:11:00)
#
#    See Main Code (at end).
#        Use log messages to understand API and Logic activation.
#
###############################################################################

api_logic_server__version = '15.00.61'
api_logic_server_created__on = 'July 28, 2025 14:48:19'
api_logic_server__host = 'localhost'
api_logic_server__port = '5656'

start_up_message = "normal start"

import os, logging, logging.config, sys, yaml  # failure here means venv probably not set
from flask_sqlalchemy import SQLAlchemy
import json
from pathlib import Path
from config.config import Args  # sets up logging
from config import server_setup

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)
project_name = os.path.basename(os.path.normpath(current_path))

if server_setup.is_docker():
    sys.path.append(os.path.abspath('/home/api_logic_server'))

logic_alerts = True
""" Set False to silence startup message """
declare_logic_message = ""
declare_security_message = "ALERT:  *** Security Not Enabled ***"

os.chdir(project_dir)  # so admin app can find images, code
import api.system.api_utils as api_utils
logic_logger_activate_debug = False
""" True prints all rules on startup """

from typing import TypedDict
import safrs  # fails without venv - see https://apilogicserver.github.io/Docs/Project-Env/
from safrs import ValidationError, SAFRSBase, SAFRSAPI as _SAFRSAPI
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.rule_type.constraint import Constraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket
import warnings
from flask import Flask, redirect, send_from_directory, send_file
from flask_cors import CORS
import ui.admin.admin_loader as AdminLoader
from security.system.authentication import configure_auth
import oracledb

if os.getenv("EXPERIMENT") == '+':
    app_logger = logging.getLogger("api_logic_server_app")
else:
    app_logger = server_setup.logging_setup()



# ==================================
#        MAIN CODE
# ================================== 

flask_app = Flask("API Logic Server", template_folder='ui/templates')  # templates to load ui/admin/admin.yaml

CORS(flask_app, resources=[{r"/api/*": {"origins": "*"}},{r"/ontimizeweb/*": {"origins": "*"}}],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],supports_credentials=True)

args = server_setup.get_args(flask_app)                        # creation defaults

import config.config as config
flask_app.config.from_object(config.Config)
app_logger.debug(f"\nConfig args: \n{args}")                    # config file (e.g., db uri's)

args.get_cli_args(dunder_name=__name__, args=args)
app_logger.debug(f"\nCLI args: \n{args}")                       # api_logic_server_run cl args

flask_app.config.from_prefixed_env(prefix="APILOGICPROJECT")    # env overrides (e.g., docker)
app_logger.debug(f"\nENV args: \n{args}\n\n")

server_setup.validate_db_uri(flask_app)

server_setup.api_logic_server_setup(flask_app, args)

AdminLoader.admin_events(flask_app = flask_app, args = args, validation_error = ValidationError)

if __name__ == "__main__":
    msg = f'API Logic Project loaded (not WSGI), version: 15.00.61\n'
    msg += f'.. startup message: {start_up_message}\n'
    if server_setup.is_docker():
        msg += f' (running from docker container at flask_host: {args.flask_host} - may require refresh)\n'
    else:
        msg += f' (running locally at flask_host: {args.flask_host})\n'
    app_logger.info(f'\n{msg}')

    if args.create_and_run:
        app_logger.info(f'==> Customizable API Logic Project created and running:\n'
                    f'..Open it with your IDE at {project_dir}\n')

    start_up_message = f'{args.http_scheme}://{args.swagger_host}:{args.port}   *'
    if os.getenv('CODESPACES'):
        app_logger.info(f'API Logic Project (name: {project_name}) starting on Codespaces:\n'
                f'..Explore data and API on codespaces, swagger_host: {args.http_scheme}://{args.swagger_host}/\n')
        start_up_message = f'{args.http_scheme}://{args.swagger_host}'
    else:
        app_logger.info(f'API Logic Project (name: {project_name}) starting:\n'
                f'..Explore data and API at http_scheme://swagger_host:port {start_up_message}\n'
                f'.... with flask_host: {args.flask_host}\n'
                f'.... and  swagger_port: {args.swagger_port}')
    if logic_alerts:
        app_logger.info(f'\nAlert: These following are **Critical** to unlocking value for project: {project_name}:')
        app_logger.info(f'.. see logic.declare_logic.py       -- {server_setup.declare_logic_message}')
        app_logger.info(f'.. see security.declare_security.py -- {server_setup.declare_security_message}\n\n')

        app_logger.info(f'*************************************************************************')    
        app_logger.info(f'*   Startup Instructions: Open your Browser at: {start_up_message}')    
        app_logger.info(f'*************************************************************************\n')    

    flask_app.run(host=args.flask_host, threaded=True, port=args.port)
else:
    msg = f'API Logic Project Loaded (WSGI), version 15.00.61\n'
    msg += f'.. startup message: {start_up_message}\n'

    if server_setup.is_docker():
        msg += f' (running from docker container at {args.flask_host} - may require refresh)\n'
    else:
        msg += f' (running locally at flask_host: {args.flask_host})\n'
    app_logger.info(f'\n{msg}')
    app_logger.info(f'API Logic Project (name: {project_name}) starting:\n'
                f'..Explore data and API at http_scheme://swagger_host:port {args.http_scheme}://{args.swagger_host}:{args.port}\n'
                f'.... with flask_host: {args.flask_host}\n'
                f'.... and  swagger_port: {args.swagger_port}')
