# SnippingCalc

A versatile tool for extracting and calculating numbers from images, with both CLI and GUI options.

## Features

- Extract numbers from images using OCR (Optical Character Recognition)
- Calculate SUM, AVERAGE, and COUNT of detected numbers
- Multiple operation modes:
  - CLI mode for processing existing images
  - Background mode with global hotkey for screen capture (requires desktop environment)
- Save results to JSON files for later reference
- Support for various image formats (PNG, JPG, etc.)

## Requirements

- Python 3.7 or higher
- Tesseract OCR engine
- Required Python packages (installed via pip)
- For background mode: X server (Linux) or Windows/macOS desktop environment

## Installation

1. Install Tesseract OCR:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr

   # macOS
   brew install tesseract

   # Windows
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Mode
Process existing image files:

```bash
python src/cli_snip.py <image_path>
```

Example:
```bash
python src/cli_snip.py test_numbers.png
```

### Background Mode (Desktop Environment Required)
Run as a background application with global hotkey:

```bash
python src/background_app.py
```

Features:
- Global hotkey (Ctrl+Shift+S) to activate screen capture
- Click and drag to select area
- Results shown in floating window
- Copy results to clipboard
- Auto-save results to JSON file

### Test Image Creation
Create a test image with known numbers:

```bash
python src/create_test_image.py
```

## Operation Modes

1. CLI Mode (`cli_snip.py`):
   - Best for processing existing images
   - Works in any environment
   - Ideal for automation and scripting

2. Background Mode (`background_app.py`):
   - Requires desktop environment (X server on Linux, or Windows/macOS)
   - Global hotkey activation
   - Interactive screen capture
   - Floating results window
   - Clipboard integration

## Output

The tool provides:
- Console output with calculations
- JSON file with detailed results
- (Background mode) GUI window with results and copy option

Example output:
```
Results:
SUM: 2583.81
AVG: 516.76
COUNT: 5
Numbers found: 123.45, 678.90, 1234.56, 90.12, 456.78
```

## System Requirements

### For CLI Mode:
- Any operating system with Python support
- Terminal/Command Prompt access
- Tesseract OCR installed

### For Background Mode:
- Linux: X server and DISPLAY environment variable set
- Windows: No additional requirements
- macOS: No additional requirements

## Troubleshooting

### CLI Mode Issues:
1. Verify Tesseract OCR installation
2. Check image quality and contrast
3. Ensure proper file paths

### Background Mode Issues:
1. Linux: Ensure X server is running and DISPLAY is set
2. Permission issues: Run with appropriate permissions
3. Hotkey conflicts: Check for other applications using same hotkey

## Development Notes

- `background_app.py`: Full-featured GUI application with global hotkey
- `cli_snip.py`: Command-line interface for basic functionality
- `create_test_image.py`: Test image generator for verification

## License

This project is licensed under the MIT License - see the LICENSE file for details.
