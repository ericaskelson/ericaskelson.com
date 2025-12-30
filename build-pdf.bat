@echo off
echo Building resume PDF...
echo.

set PANDOC="%LOCALAPPDATA%\Pandoc\pandoc.exe"
set PDFLATEX="%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"

%PANDOC% content/resume.md ^
    -o content/resume.pdf ^
    --pdf-engine=%PDFLATEX% ^
    -V geometry:margin=0.75in ^
    -V fontsize=11pt ^
    -V colorlinks=true ^
    -V linkcolor=blue ^
    --metadata title=""

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! PDF created at content/resume.pdf
) else (
    echo.
    echo Error generating PDF. You may need to restart your terminal for MiKTeX to be in PATH.
)

pause
