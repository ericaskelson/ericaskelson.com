@echo off
echo Building resume PDF...
echo.

set PANDOC="%LOCALAPPDATA%\Pandoc\pandoc.exe"
set PDFLATEX="%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"

:: Generate date string (YYYY-MM-DD format)
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set DATESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

set OUTFILE=content\Eric_Askelson_Resume_%DATESTAMP%.pdf

%PANDOC% content/resume.md ^
    -o %OUTFILE% ^
    --pdf-engine=%PDFLATEX% ^
    -V geometry:margin=0.75in ^
    -V fontsize=11pt ^
    -V colorlinks=true ^
    -V linkcolor=blue ^
    --metadata title=""

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! PDF created: %OUTFILE%

    :: Also create a copy for the website download link
    copy /Y %OUTFILE% content\Eric_Askelson_Resume.pdf >nul
    echo Also copied to: content\Eric_Askelson_Resume.pdf
) else (
    echo.
    echo Error generating PDF.
)

pause
