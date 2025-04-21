@echo off
echo Uninstalling SnippingCalc...
echo.

:: Remove desktop shortcut
echo Removing desktop shortcut...
del /F /Q "%USERPROFILE%\Desktop\SnippingCalc.lnk" 2>nul
if exist "%USERPROFILE%\Desktop\SnippingCalc.lnk" (
    echo Warning: Could not remove desktop shortcut
) else (
    echo Desktop shortcut removed
)

:: Remove start menu shortcut
echo Removing start menu shortcut...
del /F /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\SnippingCalc.lnk" 2>nul
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\SnippingCalc.lnk" (
    echo Warning: Could not remove start menu shortcut
) else (
    echo Start menu shortcut removed
)

:: Remove from startup registry
echo Removing from startup...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SnippingCalc" /f 2>nul
if errorlevel 1 (
    echo Warning: Could not remove registry entry
) else (
    echo Removed from startup registry
)

:: Clean up build directories
echo Cleaning up build files...
rmdir /S /Q "dist" 2>nul
rmdir /S /Q "build" 2>nul
del /F /Q "src\*.spec" 2>nul
del /F /Q "src\icon.ico" 2>nul

echo.
echo Uninstallation complete!
echo You may now delete this folder if you wish.
echo.
pause
