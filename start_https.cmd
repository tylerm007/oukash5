@echo off
REM Simple batch file to start Flask with HTTPS
REM Usage: start_https.cmd [http] [port]

set DEFAULT_PORT=5656
set USE_PORT=%DEFAULT_PORT%

if "%~2" neq "" set USE_PORT=%2

echo.
echo 🚀 API Logic Server HTTPS Startup
echo.

if /i "%~1"=="http" (
    echo 🌐 Starting in HTTP mode...
    set FLASK_USE_SSL=false
    set APILOGICPROJECT_HTTP_SCHEME=http
) else (
    echo 🔒 Starting in HTTPS mode...
    set FLASK_USE_SSL=true
    set APILOGICPROJECT_HTTP_SCHEME=https
    set FLASK_SSL_CERT=security\ssl\server.crt
    set FLASK_SSL_KEY=security\ssl\server.key
    
    REM Check if certificates exist
    if not exist "security\ssl\server.crt" (
        echo.
        echo ⚠️  SSL certificate not found!
        echo 📝 Generating self-signed certificate...
        echo.
        if exist "security\ssl\generate_cert.ps1" (
            powershell -ExecutionPolicy Bypass -File "security\ssl\generate_cert.ps1"
        ) else (
            echo ❌ Certificate generator not found
            echo 💡 Please run: python security\ssl\generate_cert.py
            pause
            exit /b 1
        )
    )
)

set APILOGICPROJECT_FLASK_HOST=localhost
set APILOGICPROJECT_PORT=%USE_PORT%
set APILOGICPROJECT_SWAGGER_HOST=localhost

echo.
echo 📊 Configuration:
echo   Host: localhost
echo   Port: %USE_PORT%
echo   URL: %APILOGICPROJECT_HTTP_SCHEME%://localhost:%USE_PORT%
echo.

if not "%FLASK_USE_SSL%"=="false" (
    echo ⚠️  Browser Security Notice:
    echo   Your browser will show a security warning for self-signed certificates.
    echo   Click 'Advanced' -^> 'Proceed to localhost (unsafe)' to continue.
    echo.
)

echo 🚀 Starting Flask application...
echo Press Ctrl+C to stop
echo.

python api_logic_server_run.py

if errorlevel 1 (
    echo.
    echo ❌ Error starting Flask application
    echo 💡 Make sure you're in the project root directory  
    echo 💡 Make sure Python environment is activated
    pause
)