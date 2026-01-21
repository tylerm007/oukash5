# Teams API Integration - Setup Complete! 🎉

Your API Logic Server now has a custom endpoint to POST messages to your Microsoft Teams channel "NewAPI Team".

## What Was Created

### 1. API Endpoint
- **File**: `api/customize_api.py`
- **Endpoint**: `POST /teams/send_message`
- **Location in code**: Lines added before `hello_world` route

### 2. Documentation
- **`docs/TEAMS_API_SETUP.md`** - Complete guide with examples
- **`docs/TEAMS_API_QUICKREF.md`** - Quick reference for common tasks

### 3. Test Scripts
- **`test_teams_api.ps1`** - PowerShell test script
- **`test_teams_api.py`** - Python test script

### 4. Existing Teams Integration
- **`integration/microsoft/teams_integration.py`** - Core Teams functionality (already existed)

## Quick Start (3 Steps)

### Step 1: Get Your Webhook URL

1. Open Microsoft Teams
2. Go to "NewAPI Team" channel
3. Click **...** → **Connectors** or **Workflows**
4. Add **"Incoming Webhook"**
5. Configure and **copy the URL**

### Step 2: Set Environment Variable

**PowerShell:**
```powershell
$env:TEAMS_WEBHOOK_URL = "paste-your-webhook-url-here"
```

**Or add to `.env` file:**
```
TEAMS_WEBHOOK_URL=your-webhook-url-here
```

### Step 3: Test It!

**PowerShell:**
```powershell
# Run the test script
.\test_teams_api.ps1

# Or test manually
$body = @{
    message = "Hello from API Logic Server!"
    message_type = "card"
    title = "Test Message"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5656/teams/send_message" -Method POST -Body $body -ContentType "application/json"
```

**Python:**
```bash
# Run the test script
python test_teams_api.py

# Or test manually
python -c "import requests; print(requests.post('http://localhost:5656/teams/send_message', json={'message': 'Hello Teams!'}).json())"
```

## API Usage

### Simple Message
```json
POST /teams/send_message
{
  "message": "Your message here"
}
```

### Formatted Card
```json
POST /teams/send_message
{
  "title": "Alert Title",
  "message": "**Bold text** and _italic_ with ✅ emojis",
  "message_type": "card",
  "color": "00FF00"
}
```

### Common Colors
- 🟢 Green (success): `00FF00`
- 🔴 Red (error): `FF0000`
- 🟡 Yellow (warning): `FFCC00`
- 🔵 Blue (info): `0076D7`

## Integration Examples

### From Business Logic Rules

Add to `logic/declare_logic.py`:

```python
from integration.microsoft.teams_integration import TeamsWebhookMessenger
import os

def notify_large_order(row: models.Order, old_row: models.Order, logic_row: LogicRow):
    if row.amount_total > 10000:
        webhook = TeamsWebhookMessenger(os.getenv('TEAMS_WEBHOOK_URL'))
        webhook.send_card_message(
            title="🔔 Large Order",
            text=f"Order #{row.Id}: ${row.amount_total:,.2f}",
            theme_color="FFCC00"
        )

Rule.commit_row_event(on_class=models.Order, calling=notify_large_order)
```

### From API Endpoint

```python
import requests

# In any Python code
requests.post('http://localhost:5656/teams/send_message', json={
    'title': 'Process Complete',
    'message': 'Data processing finished successfully',
    'message_type': 'card',
    'color': '00FF00'
})
```

### From PowerShell Script

```powershell
# In any PowerShell script
$notification = @{
    title = "Backup Complete"
    message = "Database backup completed at $(Get-Date)"
    message_type = "card"
    color = "00FF00"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5656/teams/send_message" `
    -Method POST -Body $notification -ContentType "application/json"
```

## Testing

### Run PowerShell Tests
```powershell
.\test_teams_api.ps1
```

This will send 5 test messages:
1. Simple text message
2. Success card (green)
3. Warning card (yellow)
4. Error card (red)
5. Formatted report card

### Run Python Tests
```bash
python test_teams_api.py
```

## Troubleshooting

### "webhook_url not provided"
- Set `TEAMS_WEBHOOK_URL` environment variable, OR
- Include `webhook_url` in request body

### "Failed to send message"
- Verify webhook URL is correct
- Check webhook still exists in Teams
- Test network connectivity

### Messages not appearing
- Verify you're in the correct Teams channel
- Refresh Teams
- Check webhook configuration

## Next Steps

1. ✅ Get webhook URL from Teams
2. ✅ Set environment variable
3. ✅ Run test script to verify
4. ✅ Integrate into your workflows

## Documentation

- **Full Guide**: `docs/TEAMS_API_SETUP.md`
- **Quick Reference**: `docs/TEAMS_API_QUICKREF.md`
- **Teams Integration Code**: `integration/microsoft/teams_integration.py`
- **API Endpoint**: `api/customize_api.py` (search for `teams/send_message`)

## Support

For issues or questions:
1. Check the full documentation in `docs/TEAMS_API_SETUP.md`
2. Review test scripts for working examples
3. Verify webhook URL and environment variables

---

**Ready to go!** 🚀 Just get your webhook URL, set the environment variable, and start sending messages to Teams!
