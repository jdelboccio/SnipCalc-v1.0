@echo off
echo Installing SnippingCalc...
echo.

:: Check if running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo Error: Please run this installer as Administrator
    echo Right-click install.bat and select "Run as administrator"
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Check if Tesseract is installed
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo Installing Tesseract OCR...
    echo This may take a few minutes...
    
    :: Download Tesseract installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe' -OutFile 'tesseract-installer.exe'}"
    
    :: Install Tesseract silently
    tesseract-installer.exe /S
    
    :: Add Tesseract to PATH
    setx PATH "%PATH%;C:\Program Files\Tesseract-OCR" /M
    
    :: Clean up
    del tesseract-installer.exe
)

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

:: Build and install the application
echo Building SnippingCalc...
python build_windows.py
if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo SnippingCalc will start automatically with Windows.
echo Press Ctrl+Shift+S anytime to use the calculator.
echo.

:: Start the application
echo Starting SnippingCalc...
start "" "dist\SnippingCalc\SnippingCalc.exe"

pause
