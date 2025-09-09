import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime

class TeamsWebhookMessenger:
    """
    Simple Microsoft Teams messenger using incoming webhooks.
    Easy to set up but limited functionality.
    """
    
    def __init__(self, webhook_url: str):
        """
        Initialize with Teams webhook URL.
        
        To get webhook URL:
        1. Go to Teams channel
        2. Click ... > Connectors > Incoming Webhook
        3. Configure and copy the webhook URL
        """
        self.webhook_url = webhook_url
    
    def send_simple_message(self, text: str) -> bool:
        """Send a simple text message to Teams."""
        payload = {
            "text": text
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            return False
    
    def send_card_message(self, title: str, text: str, theme_color: str = "0076D7") -> bool:
        """Send a formatted card message to Teams."""
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": theme_color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": f"Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "text": text,
                "markdown": True
            }]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending card message: {e}")
            return False
    
    def send_actionable_card(self, title: str, text: str, actions: list) -> bool:
        """Send a card with action buttons."""
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "text": text,
                "markdown": True
            }],
            "potentialAction": actions
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending actionable card: {e}")
            return False


class TeamsGraphMessenger:
    """
    Microsoft Teams messenger using Graph API.
    Requires app registration and authentication but provides full functionality.
    """
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize with Azure AD app credentials.
        
        Setup required:
        1. Register app in Azure AD
        2. Add Microsoft Graph permissions: Chat.ReadWrite, ChannelMessage.Send
        3. Get tenant_id, client_id, client_secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
    
    def get_access_token(self) -> Optional[str]:
        """Get OAuth2 access token for Graph API."""
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")
            return None
    
    def send_channel_message(self, team_id: str, channel_id: str, message: str) -> bool:
        """Send message to a specific Teams channel."""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "body": {
                "contentType": "html",
                "content": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending channel message: {e}")
            return False
    
    def send_chat_message(self, chat_id: str, message: str) -> bool:
        """Send message to a Teams chat."""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "body": {
                "contentType": "html",
                "content": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending chat message: {e}")
            return False


# Example usage functions
def webhook_example():
    """Example using webhook (recommended for simple use cases)."""
    # Replace with your actual webhook URL
    webhook_url = "https://outlook.office.com/webhook/YOUR-WEBHOOK-URL"
    
    messenger = TeamsWebhookMessenger(webhook_url)
    
    # Send simple message
    messenger.send_simple_message("Hello from Python! 🐍")
    
    # Send formatted card
    messenger.send_card_message(
        title="System Alert",
        text="**Server Status**: All systems operational ✅\n\nLast checked: " + 
              datetime.now().strftime('%H:%M:%S'),
        theme_color="00FF00"  # Green
    )
    
    # Send actionable card
    actions = [
        {
            "@type": "OpenUri",
            "name": "View Dashboard",
            "targets": [{"os": "default", "uri": "https://your-dashboard.com"}]
        },
        {
            "@type": "OpenUri", 
            "name": "Check Logs",
            "targets": [{"os": "default", "uri": "https://your-logs.com"}]
        }
    ]
    
    messenger.send_actionable_card(
        title="Deployment Complete",
        text="Version 1.2.3 has been successfully deployed to production.",
        actions=actions
    )


def graph_api_example():
    """Example using Graph API (more features, requires app registration)."""
    # Replace with your actual Azure AD app details
    tenant_id = "your-tenant-id"
    client_id = "your-client-id" 
    client_secret = "your-client-secret"
    
    messenger = TeamsGraphMessenger(tenant_id, client_id, client_secret)
    
    # Send to channel
    team_id = "your-team-id"
    channel_id = "your-channel-id"
    messenger.send_channel_message(
        team_id, 
        channel_id, 
        "<h2>📊 Weekly Report</h2><p>Sales are up 15% this week!</p>"
    )
    
    # Send to chat
    chat_id = "your-chat-id"
    messenger.send_chat_message(
        chat_id,
        "<p>Hey team! The new feature is ready for testing. 🚀</p>"
    )


# Utility function for notifications
def send_notification(webhook_url: str, title: str, message: str, 
                     color: str = "0076D7") -> bool:
    """Quick utility function to send notifications."""
    messenger = TeamsWebhookMessenger(webhook_url)
    return messenger.send_card_message(title, message, color)


if __name__ == "__main__":
    # Run examples (uncomment and configure as needed)
    # webhook_example()
    # graph_api_example()
    
    # Quick notification example
    webhook_url = "YOUR-WEBHOOK-URL-HERE"
    send_notification(
        webhook_url,
        "Python Script Complete",
        "The data processing job finished successfully at " + 
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "00FF00"
    )