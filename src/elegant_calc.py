import os
import sys
import json
from datetime import datetime
import threading
from pynput import keyboard
import mss
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import tkinter as tk
from config import setup_tesseract
import win32clipboard
import win32con

class ElegantSnip:
    def __init__(self):
        self.is_capturing = False
        self.start_pos = None
        self.current_pos = None
        self.root = None
        self.canvas = None
        self.results_banner = None
        
    def start_capture(self):
        """Initialize the capture window"""
        if self.is_capturing:
            return
            
        self.is_capturing = True
        
        # Main window
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True, '-alpha', 0.2, '-topmost', True)
        self.root.configure(bg='black')
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.root.bind('<Escape>', lambda e: self.cancel_capture())
        
        self.root.mainloop()
    
    def on_mouse_down(self, event):
        self.start_pos = (event.x, event.y)
        self.current_pos = (event.x, event.y)
        
    def on_mouse_move(self, event):
        if self.start_pos:
            self.current_pos = (event.x, event.y)
            self.draw_selection()
    
    def draw_selection(self):
        """Draw the selection area with elegant styling"""
        self.canvas.delete('selection')
        
        # Calculate coordinates
        x1 = min(self.start_pos[0], self.current_pos[0])
        y1 = min(self.start_pos[1], self.current_pos[1])
        x2 = max(self.start_pos[0], self.current_pos[0])
        y2 = max(self.start_pos[1], self.current_pos[1])
        
        # Draw semi-transparent overlay
        self.canvas.create_rectangle(0, 0, self.root.winfo_width(), self.root.winfo_height(),
                                   fill='black', alpha=0.5, tags='selection')
        
        # Draw selection window
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                   outline='#007AFF', width=2,
                                   fill='white', alpha=0.1,
                                   tags='selection')
        
        # Draw corner indicators
        corner_size = 8
        corners = [
            (x1, y1, x1 + corner_size, y1, x1, y1 + corner_size),  # Top-left
            (x2 - corner_size, y1, x2, y1, x2, y1 + corner_size),  # Top-right
            (x1, y2 - corner_size, x1, y2, x1 + corner_size, y2),  # Bottom-left
            (x2 - corner_size, y2, x2, y2, x2, y2 - corner_size)   # Bottom-right
        ]
        
        for corner in corners:
            self.canvas.create_line(*corner, fill='#007AFF', width=2, tags='selection')
    
    def on_mouse_up(self, event):
        if not self.start_pos or not self.current_pos:
            self.cancel_capture()
            return
            
        # Calculate coordinates
        x1 = min(self.start_pos[0], self.current_pos[0])
        y1 = min(self.start_pos[1], self.current_pos[1])
        x2 = max(self.start_pos[0], self.current_pos[0])
        y2 = max(self.start_pos[1], self.current_pos[1])
        
        # Ensure minimum selection size
        if x2 - x1 < 30 or y2 - y1 < 30:
            self.cancel_capture()
            return
        
        # Hide main window
        self.root.withdraw()
        
        try:
            # Capture the selected area
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab({
                    'top': y1,
                    'left': x1,
                    'width': x2 - x1,
                    'height': y2 - y1
                })
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Process the image
                self.process_image(img, (x1, y1, x2, y2))
        except Exception as e:
            print(f"Error capturing screen: {str(e)}")
        
        self.cancel_capture()
    
    def process_image(self, img, coords):
        """Process the captured image and show elegant results"""
        try:
            # Perform OCR
            text = pytesseract.image_to_string(img)
            
            # Extract numbers
            import re
            numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
            
            if numbers:
                # Calculate statistics
                total = sum(numbers)
                avg = total / len(numbers)
                count = len(numbers)
                
                # Copy sum to clipboard
                self.copy_to_clipboard(f"{total:,.2f}")
                
                # Show elegant results banner
                self.show_elegant_results(coords, total, avg, count)
                
                # Save results quietly
                self.save_results(total, avg, count, numbers)
        except Exception as e:
            print(f"Error processing image: {str(e)}")
    
    def show_elegant_results(self, coords, total, avg, count):
        """Show an elegant floating results banner"""
        x1, y1, x2, y2 = coords
        
        # Create banner window
        banner = tk.Tk()
        banner.overrideredirect(True)
        banner.attributes('-topmost', True, '-alpha', 0.95)
        
        # Calculate banner position
        banner_width = min(300, x2 - x1)
        banner_x = x1 + (x2 - x1 - banner_width) // 2
        banner_y = y2 + 10
        
        # Position the banner
        banner.geometry(f"{banner_width}x60+{banner_x}+{banner_y}")
        
        # Style
        banner.configure(bg='#2C2C2C')
        frame = tk.Frame(banner, bg='#2C2C2C', padx=15, pady=8)
        frame.pack(fill='both', expand=True)
        
        # Results with elegant formatting
        results_text = f"Σ {total:,.2f}  •  μ {avg:,.2f}  •  n {count}"
        label = tk.Label(
            frame,
            text=results_text,
            font=('SF Pro Display', 12),
            fg='white',
            bg='#2C2C2C'
        )
        label.pack()
        
        # Auto-hide banner after 2 seconds
        banner.after(2000, banner.destroy)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard using win32clipboard"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Error copying to clipboard: {str(e)}")
    
    def save_results(self, total, avg, count, numbers):
        """Quietly save results to JSON"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results = {
                'timestamp': timestamp,
                'sum': total,
                'average': avg,
                'count': count,
                'numbers': numbers
            }
            
            # Save in user's documents folder
            docs_path = os.path.expanduser('~/Documents/SnippingCalc')
            os.makedirs(docs_path, exist_ok=True)
            
            filename = os.path.join(docs_path, f'results_{timestamp}.json')
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            print(f"Error saving results: {str(e)}")
    
    def cancel_capture(self):
        """Cancel the capture process"""
        if self.root:
            self.root.destroy()
            self.root = None
        self.is_capturing = False
        self.start_pos = None
        self.current_pos = None

def on_activate():
    """Handle hotkey activation"""
    if not hasattr(on_activate, 'snipper'):
        on_activate.snipper = ElegantSnip()
    
    if not on_activate.snipper.is_capturing:
        threading.Thread(target=on_activate.snipper.start_capture).start()

def run_in_background():
    """Run the application in the background"""
    # Check Tesseract installation
    if not setup_tesseract():
        sys.exit(1)
    
    try:
        # Setup hotkey listener
        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+s': on_activate
        }) as h:
            h.join()
    except Exception as e:
        print(f"Error: {str(e)}")
        if sys.platform.startswith('win'):
            print("\nTry running as Administrator")
        sys.exit(1)

if __name__ == "__main__":
    run_in_background()
