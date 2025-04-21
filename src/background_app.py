import os
import json
from datetime import datetime
import threading
from pynput import keyboard, mouse
import mss
import numpy as np
from PIL import Image
import pytesseract
from calculator import calculate_stats
import tkinter as tk
from tkinter import messagebox

class SnippingTool:
    def __init__(self):
        self.is_capturing = False
        self.start_pos = None
        self.current_pos = None
        self.root = None
        self.canvas = None
        self.screenshot = None
        
    def start_capture(self):
        """Initialize the capture window"""
        if self.is_capturing:
            return
            
        self.is_capturing = True
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True, '-alpha', 0.3)
        self.root.configure(background='grey')
        
        # Create canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # Bind escape key to cancel
        self.root.bind('<Escape>', lambda e: self.cancel_capture())
        
        self.root.mainloop()
    
    def on_mouse_down(self, event):
        """Handle mouse button press"""
        self.start_pos = (event.x, event.y)
        self.current_pos = (event.x, event.y)
        
    def on_mouse_move(self, event):
        """Handle mouse movement"""
        if self.start_pos:
            self.current_pos = (event.x, event.y)
            self.draw_selection()
    
    def on_mouse_up(self, event):
        """Handle mouse button release"""
        if self.start_pos and self.current_pos:
            x1 = min(self.start_pos[0], self.current_pos[0])
            y1 = min(self.start_pos[1], self.current_pos[1])
            x2 = max(self.start_pos[0], self.current_pos[0])
            y2 = max(self.start_pos[1], self.current_pos[1])
            
            self.root.withdraw()  # Hide window before taking screenshot
            
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
                self.process_image(img)
        
        self.cancel_capture()
    
    def draw_selection(self):
        """Draw the selection rectangle"""
        self.canvas.delete('selection')
        self.canvas.create_rectangle(
            self.start_pos[0], self.start_pos[1],
            self.current_pos[0], self.current_pos[1],
            outline='blue', tags='selection'
        )
    
    def cancel_capture(self):
        """Cancel the capture process"""
        if self.root:
            self.root.destroy()
            self.root = None
        self.is_capturing = False
        self.start_pos = None
        self.current_pos = None
    
    def process_image(self, img):
        """Process the captured image and extract numbers"""
        try:
            # Perform OCR
            text = pytesseract.image_to_string(img)
            
            # Extract numbers
            import re
            numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
            
            if numbers:
                # Calculate statistics
                stats = calculate_stats(numbers)
                
                # Create results window
                self.show_results(stats, numbers)
                
                # Save results
                self.save_results(stats, numbers)
            else:
                messagebox.showwarning("No Numbers Found", "No numbers were detected in the selected area.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
    
    def show_results(self, stats, numbers):
        """Show results in a floating window"""
        results_window = tk.Tk()
        results_window.title("Results")
        results_window.geometry("300x200")
        
        # Add results
        tk.Label(results_window, text="Results", font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Label(results_window, text=f"SUM: {stats['SUM']:.2f}").pack()
        tk.Label(results_window, text=f"AVG: {stats['AVG']:.2f}").pack()
        tk.Label(results_window, text=f"COUNT: {stats['COUNT']}").pack()
        
        # Add numbers found
        tk.Label(results_window, text="Numbers found:").pack()
        numbers_text = ", ".join(f"{n:.2f}" for n in numbers)
        tk.Label(results_window, text=numbers_text, wraplength=250).pack()
        
        # Add copy button
        def copy_to_clipboard():
            text = f"SUM: {stats['SUM']:.2f}\n"
            text += f"AVG: {stats['AVG']:.2f}\n"
            text += f"COUNT: {stats['COUNT']}\n"
            text += f"Numbers: {numbers_text}"
            results_window.clipboard_clear()
            results_window.clipboard_append(text)
            messagebox.showinfo("Copied", "Results copied to clipboard!")
        
        tk.Button(results_window, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)
    
    def save_results(self, stats, numbers):
        """Save results to a JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {
            'timestamp': timestamp,
            'stats': stats,
            'numbers': numbers
        }
        
        filename = f'results_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

def on_activate():
    """Handle hotkey activation"""
    if not hasattr(on_activate, 'snipper'):
        on_activate.snipper = SnippingTool()
    
    if not on_activate.snipper.is_capturing:
        threading.Thread(target=on_activate.snipper.start_capture).start()

def main():
    print("SnippingCalc is running!")
    print("Press Ctrl+Shift+S to start capture")
    print("Press Ctrl+C to exit")
    
    # Setup hotkey listener
    with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+s': on_activate
    }) as h:
        h.join()  # Keep the script running

if __name__ == "__main__":
    main()
