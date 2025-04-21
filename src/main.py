import tkinter as tk
from PIL import ImageGrab, ImageTk
import keyboard
import numpy as np
import pytesseract
from calculator import calculate_stats
from gui.selection import SelectionWindow
from gui.results import ResultWindow

class SnippingCalc:
    def __init__(self):
        # Initialize the root window (will be hidden)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
        # Initialize selection and result windows as None
        self.selection_window = None
        self.result_window = None
        
        # Register the global hotkey (default: ctrl+shift+s)
        keyboard.add_hotkey('ctrl+shift+s', self.start_selection)
        
        # Create system tray icon
        self.setup_system_tray()
    
    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        self.root.title("SnippingCalc")
        self.root.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)
    
    def start_selection(self):
        """Start the selection process when hotkey is pressed"""
        if self.selection_window is None:
            self.selection_window = SelectionWindow(self.root, callback=self.on_selection)
    
    def on_selection(self, bbox):
        """Handle the selection area and process it"""
        if bbox:
            # Capture the selected area
            image = ImageGrab.grab(bbox=bbox)
            
            # Process the image with OCR
            try:
                numbers = self.process_image(image)
                if numbers:
                    stats = calculate_stats(numbers)
                    self.show_results(stats)
                else:
                    self.show_error("No numbers found in selection")
            except Exception as e:
                self.show_error(f"Error processing image: {str(e)}")
        
        # Clean up selection window
        if self.selection_window:
            self.selection_window.destroy()
            self.selection_window = None
    
    def process_image(self, image):
        """Process the image using OCR and extract numbers"""
        # Convert image to text using pytesseract
        text = pytesseract.image_to_string(image)
        
        # Extract numbers from text
        import re
        numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
        return numbers
    
    def show_results(self, stats):
        """Display the results window"""
        if self.result_window:
            self.result_window.destroy()
        self.result_window = ResultWindow(self.root, stats)
    
    def show_error(self, message):
        """Show error message"""
        tk.messagebox.showerror("Error", message)
    
    def minimize_to_tray(self):
        """Minimize the application to system tray"""
        self.root.withdraw()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SnippingCalc()
    app.run()
