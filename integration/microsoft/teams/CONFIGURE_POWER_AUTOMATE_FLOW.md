# Power Automate Flow Configuration Guide

## Problem
The webhook is receiving messages (tests succeed), but messages aren't appearing in your Teams channel. This means your Power Automate Flow needs to be configured to post to Teams.

## Solution: Configure Your Power Automate Flow

### Step 1: Access Your Flow

1. Go to **Power Automate**: https://make.powerautomate.com
2. Click **My flows** in the left menu
3. Find your flow (it's using workflow ID: `2bce774ace0947e3a3e6d7db26749c78`)
4. Click **Edit** on the flow

### Step 2: Check Flow Trigger

Your flow should have:
- **Trigger**: "When a HTTP request is received"
- This trigger is already working (your tests succeed)

### Step 3: Add/Update Teams Action

You need to add an action to post to Teams:

1. Click **+ New step** (or edit existing Teams action)
2. Search for **"Post message in a chat or channel"** or **"Post card in a chat or channel"**
3. Select **Microsoft Teams** connector
4. Choose **"Post message in a chat or channel"**

### Step 4: Configure Teams Action

Fill in these fields:

**Post as**: `Flow bot` or `User`

**Post in**: `Channel`

**Team**: Select your team (find "NewAPI Team" or your team name)

**Channel**: Select your channel

**Message**: Add dynamic content from the HTTP request:

#### Option A: Simple Message
```
@{triggerBody()?['title']}

@{triggerBody()?['text']}
```

#### Option B: Formatted Adaptive Card
Click "Show advanced options" and use:

**Message** (in Adaptive Card format):
```json
{
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "@{triggerBody()?['title']}",
      "weight": "Bolder",
      "size": "Medium"
    },
    {
      "type": "TextBlock",
      "text": "@{triggerBody()?['text']}",
      "wrap": true
    }
  ]
}
```

### Step 5: Save and Test

1. Click **Save** in Power Automate
2. The flow should now be enabled
3. Run your test again:

```powershell
.\test_teams_simple.ps1
```

4. Check your Teams channel - you should now see the message!

---

## Alternative: Create a New Flow From Scratch

If you can't find your flow or want to start fresh:

### 1. Create New Flow

1. Go to Power Automate: https://make.powerautomate.com
2. Click **+ Create**
3. Choose **Automated cloud flow**
4. Name it: "API to Teams Notifications"
5. Skip choosing a trigger (we'll add it manually)

### 2. Add HTTP Trigger

1. Search for **"When a HTTP request is received"**
2. Add it as the trigger
3. Click **"Use sample payload to generate schema"**
4. Paste this JSON:

```json
{
  "title": "Test Message",
  "text": "This is a test message",
  "color": "0076D7"
}
```

5. Click **Done**

### 3. Add Teams Action

1. Click **+ New step**
2. Search for **"Post message"**
3. Choose **Microsoft Teams** > **"Post message in a chat or channel"**
4. Configure:
   - **Post as**: Flow bot
   - **Post in**: Channel
   - **Team**: Your team
   - **Channel**: Your channel (e.g., "General" or specific channel)
   - **Message**: 
   ```
   **@{triggerBody()?['title']}**

   @{triggerBody()?['text']}
   ```

### 4. Save and Get URL

1. Click **Save**
2. Go back to the HTTP trigger
3. Copy the **HTTP POST URL**
4. Update your environment variable:

```powershell
$env:TEAMS_WEBHOOK_URL = "paste-new-url-here"
```

5. Update `config/default.env` with the new URL

---

## Quick Troubleshooting

### Check 1: Is the Flow Enabled?

1. Go to Power Automate > My flows
2. Make sure your flow shows as **"On"** (not "Off")
3. If it's off, click it and turn it on

### Check 2: View Flow Run History

1. Click on your flow
2. Click **28-day run history** at the top
3. You should see recent runs from your tests
4. Click on a run to see details
5. Check if the Teams action succeeded

### Check 3: Flow Permissions

1. Edit your flow
2. Check the Teams action
3. Make sure it's signed in with an account that has permission to post to the channel
4. You may need to re-authenticate the Teams connector

### Check 4: Test Direct from Power Automate

1. In your flow, click **Test** (top right)
2. Choose **Manually**
3. Click **Test** then **Run flow**
4. Provide test data:
   ```json
   {
     "title": "Test from Power Automate",
     "text": "If you see this, the flow works!"
   }
   ```
5. Check your Teams channel

---

## Expected Flow Structure

```
┌─────────────────────────────────────┐
│ When HTTP request is received       │
│ (Your webhook URL)                  │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Post message in a chat or channel   │
│ Team: [Your Team]                   │
│ Channel: [Your Channel]             │
│ Message: {dynamic content}          │
└─────────────────────────────────────┘
```

---

## After Configuration

Once configured correctly, run:

```powershell
# Test simple message
.\test_teams_simple.ps1

# Or full test suite
.\test_teams_api.ps1
```

You should now see messages appear in your Teams channel!

---

## Need Help?

If you're still not seeing messages:

1. Share the flow run history status
2. Check if there are any errors in the flow runs
3. Verify the Teams channel exists and you have permission to post
4. Try testing directly from Power Automate first

The key is: **Your webhook works, now you just need to connect it to post to Teams!**
