# Power Automate Webhook Fix - Summary

## Problem Identified
Your webhook URL is a **Power Automate Flow webhook**, not a traditional Teams Incoming Webhook. They require different JSON payload formats.

Your webhook: `https://defaulteec94eb4840d4d2ca7f105b024e605.80.environment.api.powerplatform.com/...`

## What Was Fixed

### 1. Updated `integration/microsoft/teams_integration.py`
- Added detection for Power Automate webhooks (by checking for 'powerplatform.com' in URL)
- Uses simplified JSON payload for Power Automate:
  ```json
  {
    "title": "Your Title",
    "text": "Your message",
    "color": "00FF00"
  }
  ```
- Traditional Teams webhooks still supported with MessageCard format

### 2. Updated `api/customize_api.py`
- Added better logging
- Added traceback for debugging errors

### 3. Direct Test Confirmed Working
The direct webhook test (`.\test_webhook_direct.ps1`) successfully sent messages!

## Next Steps

### RESTART THE API SERVER (Required!)

The Python code changes won't take effect until you restart:

**Option 1: Use the helper script**
```powershell
.\restart_for_teams.ps1
```

**Option 2: Manual restart**
1. Stop the current server (Ctrl+C)
2. Restart: `python api_logic_server_run.py`
3. Wait 5-10 seconds for startup

### Then Test Again

```powershell
# Set the environment variable
$env:TEAMS_WEBHOOK_URL = "https://defaulteec94eb4840d4d2ca7f105b024e605.80.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/2bce774ace0947e3a3e6d7db26749c78/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=2vjsOgKvgKOY3aFegAJ18ZQQ06We9zx_hX-161sRMXA"

# Run the simple test
.\test_teams_simple.ps1

# Or run the full test suite
.\test_teams_api.ps1
```

## Files Created/Updated

✅ `integration/microsoft/teams_integration.py` - Power Automate support added
✅ `api/customize_api.py` - Better error logging
✅ `test_webhook_direct.ps1` - Direct webhook test (confirmed working!)
✅ `restart_for_teams.ps1` - Helper script to restart server
✅ `config/default.env` - TEAMS_WEBHOOK_URL already added

## Why It Failed Before

1. **Encoding issues** - Fixed by removing emojis and adding UTF-8 encoding
2. **SSL certificate validation** - Fixed by adding certificate bypass
3. **Wrong payload format** - Power Automate expects simpler JSON than Teams MessageCard format
4. **Server not restarted** - Python code changes require restart

## Verification

After restart, you should see in the logs:
```
Sending Teams message: type=card, webhook_type=Power Automate
```

And messages should appear in your Teams channel!

## If Still Having Issues

1. Check server logs for error details
2. Verify environment variable is set: `$env:TEAMS_WEBHOOK_URL`
3. Test webhook directly: `.\test_webhook_direct.ps1`
4. Check Teams channel permissions
5. Verify Power Automate flow is enabled
