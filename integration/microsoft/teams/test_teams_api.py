#!/usr/bin/env python3
"""
Test script for Teams API integration
Usage: python test_teams_api.py
"""

import requests
import os
import sys
from datetime import datetime
import time

# Configuration
API_URL = "https://devvm01.nyc.ou.org:5656/teams/send_message"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def test_simple_message():
    """Test 1: Simple text message"""
    print("Test 1: Sending simple text message...")
    
    response = requests.post(API_URL, json={
        'message': f'Hello from Python! 🐍 Test at {datetime.now().strftime("%H:%M:%S")}'
    })
    
    if response.status_code == 200:
        print_success(f"Message sent successfully")
        print(f"Response: {response.json()}")
    else:
        print_error(f"Failed with status {response.status_code}")
        print(f"Response: {response.text}")
    
    return response.status_code == 200

def test_success_card():
    """Test 2: Success card (green)"""
    print("\nTest 2: Sending success card (green)...")
    
    response = requests.post(API_URL, json={
        'title': 'System Status',
        'message': f'**All systems operational** ✅\n\nLast checked: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'message_type': 'card',
        'color': '00FF00'
    })
    
    if response.status_code == 200:
        print_success("Success card sent")
    else:
        print_error(f"Failed: {response.text}")
    
    return response.status_code == 200

def test_warning_card():
    """Test 3: Warning card (yellow)"""
    print("\nTest 3: Sending warning card (yellow)...")
    
    response = requests.post(API_URL, json={
        'title': '⚠️ Warning Alert',
        'message': '**Disk space low**\n\nCurrent usage: 85%\nAction required: Clean up old files',
        'message_type': 'card',
        'color': 'FFCC00'
    })
    
    if response.status_code == 200:
        print_success("Warning card sent")
    else:
        print_error(f"Failed: {response.text}")
    
    return response.status_code == 200

def test_error_card():
    """Test 4: Error card (red)"""
    print("\nTest 4: Sending error card (red)...")
    
    response = requests.post(API_URL, json={
        'title': '🚨 Error Alert',
        'message': '**Database connection failed**\n\nError: Connection timeout\nRetrying in 30 seconds...',
        'message_type': 'card',
        'color': 'FF0000'
    })
    
    if response.status_code == 200:
        print_success("Error card sent")
    else:
        print_error(f"Failed: {response.text}")
    
    return response.status_code == 200

def test_report_card():
    """Test 5: Formatted report card"""
    print("\nTest 5: Sending formatted report card...")
    
    report_message = f"""## 📊 Daily Report

**Orders Processed**: 150
**Revenue**: $25,430.50
**New Customers**: 12

---

### Top Products
1. Widget A - 45 units
2. Gadget B - 32 units
3. Tool C - 28 units

---
_Report generated at {datetime.now().strftime('%H:%M:%S')}_
"""
    
    response = requests.post(API_URL, json={
        'title': 'Daily Business Report',
        'message': report_message,
        'message_type': 'card',
        'color': '0076D7'
    })
    
    if response.status_code == 200:
        print_success("Report card sent")
    else:
        print_error(f"Failed: {response.text}")
    
    return response.status_code == 200

def test_with_custom_webhook():
    """Test with custom webhook URL"""
    print("\n" + "="*50)
    custom_webhook = input("Enter custom webhook URL (or press Enter to skip): ").strip()
    
    if not custom_webhook:
        print("Skipped custom webhook test")
        return True
    
    print(f"\nTesting with custom webhook...")
    
    response = requests.post(API_URL, json={
        'message': 'Test message to custom webhook',
        'webhook_url': custom_webhook
    })
    
    if response.status_code == 200:
        print_success("Custom webhook message sent")
    else:
        print_error(f"Failed: {response.text}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print_header("Teams API Test Script")
    
    # Check if environment variable is set
    if not os.getenv('TEAMS_WEBHOOK_URL'):
        print("⚠️  WARNING: TEAMS_WEBHOOK_URL environment variable is not set!")
        print("\nYou can either:")
        print("  1. Set it: export TEAMS_WEBHOOK_URL='your-webhook-url'")
        print("  2. Include webhook_url in the request body")
        
        set_now = input("\nWould you like to set it now? (y/n): ").lower()
        if set_now == 'y':
            webhook_url = input("Enter your Teams webhook URL: ").strip()
            os.environ['TEAMS_WEBHOOK_URL'] = webhook_url
            print_success("Environment variable set for this session\n")
    else:
        print_info(f"TEAMS_WEBHOOK_URL is set\n")
    
    # Check if server is running
    try:
        test_response = requests.get("https://devvm01.nyc.ou.org:5656/hello_world?user=test", timeout=2)
        print_success(f"API server is running {test_response.status_code}\n")
    except requests.exceptions.RequestException:
        print_error("Cannot connect to API server at https://devvm01.nyc.ou.org:5656")
        print("Please make sure the server is running (python api_logic_server_run.py)")
        sys.exit(1)
    
    # Run tests
    results = []
    tests = [
        ("Simple Message", test_simple_message),
        ("Success Card", test_success_card),
        ("Warning Card", test_warning_card),
        ("Error Card", test_error_card),
        ("Report Card", test_report_card),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(2)  # Pause between tests
        except Exception as e:
            print_error(f"Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Custom webhook test
    try:
        custom_result = test_with_custom_webhook()
        if custom_result is not None:
            results.append(("Custom Webhook", custom_result))
    except Exception as e:
        print_error(f"Custom webhook test failed: {e}")
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    print("\n" + "="*50)
    print("Check your Teams channel 'NewAPI Team' for the messages!")
    print("\nFor more examples, see: docs/TEAMS_API_SETUP.md")
    print("="*50 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
