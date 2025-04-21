import keyboard
import mss
import numpy as np
from PIL import Image
import pytesseract
from calculator import calculate_stats
import time
import os
import json
from datetime import datetime

class SnippingTool:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.is_capturing = False
        
    def on_press(self, key):
        try:
            # Start capture when left mouse button is pressed
            self.start_pos = (key.x, key.y)
            self.is_capturing = True
        except:
            pass
            
    def on_release(self, key):
        try:
            if self.is_capturing:
                self.end_pos = (key.x, key.y)
                self.capture_area()
                self.is_capturing = False
                return False  # Stop listener
        except:
            pass
            
    def capture_area(self):
        if not self.start_pos or not self.end_pos:
            return
            
        # Calculate coordinates
        x1 = min(self.start_pos[0], self.end_pos[0])
        y1 = min(self.start_pos[1], self.end_pos[1])
        x2 = max(self.start_pos[0], self.end_pos[0])
        y2 = max(self.start_pos[1], self.end_pos[1])
        
        # Capture the screen area
        with mss.mss() as sct:
            # Get the screen
            monitor = sct.monitors[1]  # Primary monitor
            
            # The region to capture
            region = {
                'top': y1,
                'left': x1,
                'width': x2 - x1,
                'height': y2 - y1
            }
            
            # Capture the area
            screenshot = sct.grab(region)
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Save temporary image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_path = f'temp_capture_{timestamp}.png'
            img.save(temp_path)
            
            try:
                # Perform OCR
                text = pytesseract.image_to_string(img)
                
                # Extract numbers
                import re
                numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
                
                if numbers:
                    # Calculate statistics
                    stats = calculate_stats(numbers)
                    
                    # Save results
                    results = {
                        'timestamp': timestamp,
                        'stats': stats,
                        'numbers': numbers
                    }
                    
                    with open(f'results_{timestamp}.json', 'w') as f:
                        json.dump(results, f, indent=2)
                    
                    # Print results
                    print("\nResults:")
                    print(f"SUM: {stats['SUM']:.2f}")
                    print(f"AVG: {stats['AVG']:.2f}")
                    print(f"COUNT: {stats['COUNT']}")
                    print(f"Numbers found: {', '.join(map(str, numbers))}")
                    
                else:
                    print("No numbers found in the selected area")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

def start_capture():
    print("Starting capture... Click and drag to select an area.")
    from pynput import mouse
    
    snipper = SnippingTool()
    with mouse.Listener(on_click=snipper.on_press, on_release=snipper.on_release) as listener:
        listener.join()

def main():
    print("SnippingCalc is running!")
    print("Press Ctrl+Shift+S to start capture")
    
    # Register hotkey
    keyboard.add_hotkey('ctrl+shift+s', start_capture)
    
    # Keep the script running
    keyboard.wait('esc')  # Exit on ESC key

if __name__ == "__main__":
    main()
