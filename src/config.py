import os
import sys
import pytesseract

def setup_tesseract():
    """Setup Tesseract path for Windows"""
    if sys.platform.startswith('win'):
        # Common Tesseract installation paths
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Tesseract-OCR', 'tesseract.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Tesseract-OCR', 'tesseract.exe')
        ]
        
        # Try to find Tesseract executable
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        
        # If not found in common locations, check PATH
        from shutil import which
        tesseract_path = which('tesseract')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            return True
            
        print("ERROR: Tesseract not found!")
        print("Please install Tesseract OCR and add it to your system PATH")
        print("Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("\nExpected locations:")
        for path in possible_paths:
            print(f"- {path}")
        return False
    
    return True  # Non-Windows platforms don't need this configuration

if __name__ == "__main__":
    # Test Tesseract configuration
    if setup_tesseract():
        try:
            print("Tesseract path:", pytesseract.pytesseract.tesseract_cmd)
            print("Tesseract version:", pytesseract.get_tesseract_version())
            print("\nTesseract is properly configured!")
        except Exception as e:
            print(f"Error testing Tesseract: {str(e)}")
    else:
        sys.exit(1)
