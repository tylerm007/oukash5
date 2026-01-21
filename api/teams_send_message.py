import logging
import api.system.api_utils as api_utils
import safrs
from flask import request, jsonify
from safrs import jsonapi_rpc
from database import models
from sqlalchemy import text
import json


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
    
    @app.route('/teams/send_message', methods=['POST'], strict_slashes=False)
    def send_teams_message():
        """
        Send a message to Microsoft Teams channel via webhook.
        
        Request body:
        {
            "message": "Your text message",
            "title": "Optional Card Title",
            "webhook_url": "optional - overrides config default",
            "color": "0076D7",  // optional theme color
            "message_type": "simple"  // or "card"
        }
        
        PowerShell test:
        $body = @{
            title = "API Notification"
            message = "Hello from API Logic Server!"
            message_type = "card"
            color = "00FF00"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5656/teams/send_message" -Method POST -Body $body -ContentType "application/json"
        """
        try:
            from integration.microsoft.teams.teams_integration import TeamsWebhookMessenger
            import os
            import traceback
            
            data = request.get_json()
            
            if not data:
                return jsonify({"status": "error", "message": "No JSON data provided"}), 400
            
            message = data.get('message')
            if not message:
                return jsonify({"status": "error", "message": "message field is required"}), 400
            
            # Get webhook URL from request or environment variable
            webhook_url = data.get('webhook_url') or os.getenv('TEAMS_WEBHOOK_URL')
            if not webhook_url:
                return jsonify({
                    "status": "error", 
                    "message": "webhook_url not provided and TEAMS_WEBHOOK_URL not set in environment"
                }), 400
            
            app_logger.info(f"Sending Teams message: type={data.get('message_type', 'simple')}, webhook_type={'Power Automate' if 'powerplatform' in webhook_url else 'Teams Incoming Webhook'}")
            
            messenger = TeamsWebhookMessenger(webhook_url)
            
            message_type = data.get('message_type', 'simple')
            
            if message_type == 'card':
                title = data.get('title', 'API Notification')
                color = data.get('color', '0076D7')
                success = messenger.send_card_message(title, message, color)
            else:
                success = messenger.send_simple_message(message)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": "Message sent to Teams channel",
                    "message_type": message_type
                })
            else:
                app_logger.error(f"Teams webhook returned failure")
                return jsonify({
                    "status": "error",
                    "message": "Failed to send message to Teams - webhook returned failure"
                }), 500
                
        except Exception as e:
            app_logger.error(f"Error sending Teams message: {e}")
            app_logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                "status": "error",
                "message": f"Error: {str(e)}"
            }), 500

