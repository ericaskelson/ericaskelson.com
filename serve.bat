@echo off
echo Starting local server at http://localhost:8000
echo Press Ctrl+C to stop
echo.
start http://localhost:8000
py -m http.server 8000
