#!/bin/bash
echo "Cleaning up unnecessary files..."

# Remove test files
rm -f test_numbers.txt
rm -f src/test_app.py
rm -f src/test_numbers.png
rm -f src/test_image.png
rm -f src/create_test_image.py

# Remove old implementation files
rm -f src/web_app.py
rm -f src/desktop_app.py
rm -f src/simple_snip.py
rm -f src/cli_snip.py
rm -f src/background_app.py
rm -f src/elegant_calc.py
rm -f src/elegant_calc.spec
rm -f src/icon_data.py
rm -f src/main.py
rm -f src/config.py
rm -f run_snippingcalc.bat

# Remove old GUI components
rm -rf src/templates
rm -f src/gui/selection.py
rm -f src/gui/results.py
rm -f src/gui/main_window.py
rm -rf src/gui

# Remove old batch files
rm -f cleanup.bat

echo "Cleanup complete! Only essential files remain:"
echo "- src/hotkey_app.py (main application)"
echo "- src/calculator.py (calculation logic)"
echo "- build_windows.py (build script)"
echo "- install.bat (installer)"
echo "- uninstall.bat (uninstaller)"
echo "- requirements.txt (dependencies)"
echo "- README.md (documentation)"
