#!/usr/bin/env python3
"""
Callback URL Inspector
This script helps inspect what parameters are actually being received in your OAuth callback
"""

from flask import Flask, request, jsonify
import sys
from datetime import datetime

app = Flask(__name__)

# Store callback data for inspection
callback_data = []

@app.route('/auth/callback')
def inspect_callback():
    """Inspect all parameters received in OAuth callback"""
    
    timestamp = datetime.now().isoformat()
    
    # Collect all data
    data = {
        'timestamp': timestamp,
        'method': request.method,
        'url': request.url,
        'base_url': request.base_url,
        'query_params': dict(request.args),
        'form_data': dict(request.form),
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr
    }
    
    # Store for analysis
    callback_data.append(data)
    
    # Print to console
    print("\n" + "="*60)
    print(f"📞 CALLBACK RECEIVED at {timestamp}")
    print("="*60)
    print(f"🌐 Method: {data['method']}")
    print(f"🌐 Full URL: {data['url']}")
    print(f"🌐 Base URL: {data['base_url']}")
    print(f"🌐 Remote Address: {data['remote_addr']}")
    
    print(f"\n📝 Query Parameters ({len(data['query_params'])}):")
    if data['query_params']:
        for key, value in data['query_params'].items():
            print(f"   {key}: {value}")
    else:
        print("   (No query parameters)")
    
    print(f"\n📝 Form Data ({len(data['form_data'])}):")
    if data['form_data']:
        for key, value in data['form_data'].items():
            print(f"   {key}: {value}")
    else:
        print("   (No form data)")
    
    print(f"\n📊 Headers ({len(data['headers'])}):")
    for key, value in data['headers'].items():
        print(f"   {key}: {value}")
    
    # Analysis
    print(f"\n🔍 ANALYSIS:")
    
    # Check for authorization code
    auth_code = data['query_params'].get('code')
    if auth_code:
        print(f"   ✅ Authorization code found: {auth_code[:20]}..." if len(auth_code) > 20 else f"   ✅ Authorization code: {auth_code}")
        print(f"   📏 Code length: {len(auth_code)} characters")
    else:
        print(f"   ❌ No authorization code found in 'code' parameter")
    
    # Check for state
    state = data['query_params'].get('state')
    if state:
        print(f"   ✅ State parameter found: {state[:20]}..." if len(state) > 20 else f"   ✅ State: {state}")
    else:
        print(f"   ❌ No state parameter found")
    
    # Check for errors
    error = data['query_params'].get('error')
    if error:
        error_desc = data['query_params'].get('error_description', 'No description')
        print(f"   ❌ OAuth error: {error}")
        print(f"   📝 Error description: {error_desc}")
    
    # Check for common issues
    all_params = list(data['query_params'].keys())
    expected_params = ['code', 'state']
    missing_params = [p for p in expected_params if p not in all_params]
    unexpected_params = [p for p in all_params if p not in expected_params + ['error', 'error_description']]
    
    if missing_params:
        print(f"   ⚠️  Missing expected parameters: {missing_params}")
    
    if unexpected_params:
        print(f"   ℹ️  Unexpected parameters: {unexpected_params}")
    
    print("="*60)
    
    # Return JSON response
    return jsonify({
        'status': 'callback_received',
        'timestamp': timestamp,
        'query_params': data['query_params'],
        'analysis': {
            'has_code': 'code' in data['query_params'],
            'has_state': 'state' in data['query_params'],
            'has_error': 'error' in data['query_params'],
            'code_length': len(data['query_params'].get('code', '')),
            'missing_params': missing_params,
            'unexpected_params': unexpected_params
        }
    })

@app.route('/auth/debug')
def debug_summary():
    """Show summary of all callbacks received"""
    return jsonify({
        'total_callbacks': len(callback_data),
        'callbacks': callback_data
    })

@app.route('/')
def index():
    """Simple home page"""
    return f"""
    <h1>OAuth Callback Inspector</h1>
    <p>This tool helps debug OAuth callback issues.</p>
    <p>Callbacks received: {len(callback_data)}</p>
    
    <h2>Test URLs:</h2>
    <ul>
        <li><a href="/auth/callback?code=test123&state=test456">Simulate callback with code</a></li>
        <li><a href="/auth/callback?error=access_denied&error_description=User+cancelled">Simulate error callback</a></li>
        <li><a href="/auth/debug">View debug summary</a></li>
    </ul>
    
    <h2>Instructions:</h2>
    <ol>
        <li>Configure your OKTA app to redirect to: <code>http://localhost:5555/auth/callback</code></li>
        <li>Start the OAuth flow</li>
        <li>Check the console output for detailed parameter analysis</li>
        <li>Visit <a href="/auth/debug">/auth/debug</a> to see all callbacks</li>
    </ol>
    """

if __name__ == '__main__':
    print("🔍 OAuth Callback Inspector")
    print("=" * 40)
    print("📞 Listening for OAuth callbacks on http://localhost:5555")
    print("📞 Callback endpoint: http://localhost:5555/auth/callback")
    print("📊 Debug summary: http://localhost:5555/auth/debug")
    print("")
    print("⚙️  Configure your OKTA app redirect URI to:")
    print("   http://localhost:5555/auth/callback")
    print("")
    print("🚀 Starting server...")
    
    app.run(host='localhost', port=5555, debug=True)
