@echo off
cd /d "%~dp0"
echo Starting Django Development Server...
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
py manage.py runserver
pause

