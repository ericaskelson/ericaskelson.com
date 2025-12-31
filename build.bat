@echo off
echo Building site...
echo.
echo Usage: build.bat [target]
echo   (no args)  - Build everything
echo   blog       - Build blog posts only
echo   pages      - Build about/resume HTML only
echo   pdf        - Build resume PDF only
echo.
py build.py %*
echo.
pause
