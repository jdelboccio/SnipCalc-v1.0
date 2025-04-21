@echo off
echo Starting SnippingCalc...
echo Press Ctrl+Shift+S to capture numbers from screen
echo The application will run in the background

cd src
pythonw background_app.py

echo If the application didn't start, please check the troubleshooting section in README.md
pause
