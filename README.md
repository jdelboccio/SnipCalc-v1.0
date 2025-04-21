# SnippingCalc

A versatile tool for extracting and calculating numbers from images, with both CLI and GUI options.

## Windows Installation Guide

1. **Install Python:**
   - Download Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening Command Prompt and typing:
     ```
     python --version
     ```

2. **Install Tesseract OCR:**
   - Download the Tesseract installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Run the installer (e.g., `tesseract-ocr-w64-setup-5.3.1.20230401.exe`)
   - During installation:
     - Choose your installation path (remember this path!)
     - Select "English" under "Additional language data"
   - Add Tesseract to System PATH:
     1. Search for "Environment Variables" in Windows search
     2. Click "Environment Variables"
     3. Under "System Variables", find and select "Path"
     4. Click "Edit" → "New"
     5. Add your Tesseract installation path (e.g., `C:\Program Files\Tesseract-OCR`)
     6. Click "OK" to save

3. **Setup SnippingCalc:**
   - Extract the downloaded ZIP file
   - Open Command Prompt as Administrator
   - Navigate to the extracted folder:
     ```
     cd path\to\extracted\snippingcalc
     ```
   - Install required Python packages:
     ```
     pip install -r requirements.txt
     ```

4. **Test the Installation:**
   ```
   cd src
   python create_test_image.py
   python cli_snip.py test_numbers.png
   ```
   If you see the results, the basic functionality is working!

5. **Run the Background Application:**
   ```
   python background_app.py
   ```
   - Press Ctrl+Shift+S to activate the screen capture
   - Click and drag to select an area with numbers
   - Results will appear in a floating window

## Troubleshooting (Windows)

### If Tesseract is not found:
1. Verify Tesseract installation:
   - Open Command Prompt
   - Run: `tesseract --version`
   - If not found, check System PATH

2. Set TESSERACT_CMD environment variable:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
   Add this to the start of any Python script if needed.

### If hotkey doesn't work:
1. Run as Administrator:
   - Right-click `background_app.py`
   - Select "Run as Administrator"

2. Check for conflicts:
   - Ensure no other application uses Ctrl+Shift+S
   - Try changing the hotkey in `background_app.py`

### If screen capture fails:
1. Check display scaling:
   - Windows Settings → Display → Scale and layout
   - Try setting to 100%

2. Run with compatibility mode:
   - Right-click `background_app.py`
   - Properties → Compatibility
   - Check "Run this program in compatibility mode"

## Features

- Extract numbers from images using OCR
- Calculate SUM, AVERAGE, and COUNT
- Multiple operation modes:
  - CLI mode for processing existing images
  - Background mode with global hotkey
- Save results to JSON files
- Support for various image formats

## Usage Examples

### CLI Mode
```bash
# Process a specific image
python src/cli_snip.py path/to/your/image.png

# Create and process a test image
python src/create_test_image.py
python src/cli_snip.py test_numbers.png
```

### Background Mode
```bash
# Start the background application
python src/background_app.py

# Use Ctrl+Shift+S to capture
# Click and drag to select area
```

## Output Format

The tool provides results in multiple formats:
1. Console output
2. JSON file (saved automatically)
3. Floating window (in background mode)
4. Clipboard (in background mode)

Example output:
```
Results:
SUM: 2583.81
AVG: 516.76
COUNT: 5
Numbers found: 123.45, 678.90, 1234.56, 90.12, 456.78
```

## Creating a Desktop Shortcut (Windows)

1. Right-click on the desktop → New → Shortcut
2. Enter the command:
   ```
   pythonw path\to\snippingcalc\src\background_app.py
   ```
3. Name it "SnippingCalc"
4. Right-click the shortcut → Properties
5. Add icon (optional):
   - Click "Change Icon"
   - Browse to Python installation
   - Select python.exe for its icon

## License

This project is licensed under the MIT License - see the LICENSE file for details.
