# SnippingCalc

A Windows application that combines the functionality of the Microsoft Snipping Tool with automatic calculation features (SUM, AVG, COUNT) for numbers in the selected area.

## Features

- Microsoft Snipping Tool-like interface
- Multiple snipping modes (Rectangular, Free-form, Window, Full-screen)
- Automatic number recognition in snipped areas
- Instant calculation of SUM, AVG, and COUNT
- Delay timer option for snipping
- Copy results to clipboard

## System Requirements

- Windows 10 or later
- Python 3.8 or later
- Tesseract OCR (automatically installed during setup)

## Installation Guide

1. **Install Python:**
   - Download Python 3.8 or later from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation by opening Command Prompt:
     ```
     python --version
     ```

2. **Download and Install SnippingCalc:**
   ```
   # Clone the repository
   git clone https://github.com/yourusername/snippingcalc.git
   cd snippingcalc

   # Install dependencies
   pip install -r requirements.txt

   # Build and install
   python build_windows.py
   ```

   The installer will:
   - Install required dependencies
   - Create desktop and start menu shortcuts
   - Set up auto-start with Windows (optional)

## Using SnippingCalc

### Starting the Application

Choose any method:
1. Double-click the desktop shortcut
2. Find "SnippingCalc" in the Start Menu
3. Press Win+S and search for "SnippingCalc"

### Basic Usage

1. Launch SnippingCalc
2. In the main window:
   - Select snipping mode (Rectangular, Free-form, etc.)
   - Set delay timer if needed (0-10 seconds)
   - Click "New Snip" or use shortcut keys
3. Select the area containing numbers
4. View results in the popup window:
   - SUM: Total of all numbers
   - AVG: Average value
   - COUNT: Number of values found
5. Use "Copy" button to copy results to clipboard

### Tips & Tricks

- Use delay timer when you need to prepare the content before snipping
- Press ESC to cancel a snip
- Results window auto-closes after 5 seconds
- Click and drag results window to move it
- Right-click tray icon for quick access to options

## Troubleshooting

### Common Issues

1. **Application Won't Start:**
   - Run as administrator
   - Check if Python is in PATH
   - Verify all dependencies are installed

2. **Numbers Not Recognized:**
   - Ensure clear contrast in the image
   - Check if numbers are clearly visible
   - Try adjusting screen brightness/contrast

3. **OCR Issues:**
   - Verify Tesseract OCR installation
   - Try reinstalling the application
   - Check Windows Event Viewer for errors

### Uninstalling

Method 1: Using Uninstaller
```
python build_windows.py uninstall
```

Method 2: Manual Removal
1. Delete desktop and start menu shortcuts
2. Remove from Windows startup:
   - Open Task Manager
   - Go to Startup tab
   - Disable SnippingCalc
3. Delete the installation folder

## Development

Want to contribute? Great!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Project Structure
```
snippingcalc/
├── src/
│   ├── gui/
│   │   ├── main_window.py    # Main application window
│   │   ├── results.py        # Results display window
│   │   └── selection.py      # Selection overlay
│   ├── calculator.py         # Calculation logic
│   └── main.py              # Application entry point
├── build_windows.py         # Build script
└── requirements.txt         # Python dependencies
```

## Support

For issues and feature requests:
1. Check the [FAQ](link-to-faq)
2. Search existing issues
3. Create a new issue if needed

## Updates

- Check GitHub releases for updates
- Enable auto-update in settings (recommended)
- Star the repository to get notifications

## License

This project is licensed under the MIT License - see the LICENSE file for details.
