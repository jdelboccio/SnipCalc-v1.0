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
import sys
from config import setup_tesseract

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
        
        # Add instructions label
        instructions = tk.Label(
            self.root,
            text="Click and drag to select area with numbers\nPress Esc to cancel",
            font=('Arial', 14),
            bg='grey',
            fg='white'
        )
        instructions.pack(pady=20)
        
        # Create canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # Bind escape key to cancel
        self.root.bind('<Escape>', lambda e: self.cancel_capture())
        
        # Center the window on screen
        self.root.update_idletasks()
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
            
            # Ensure minimum selection size
            if x2 - x1 < 10 or y2 - y1 < 10:
                messagebox.showwarning("Selection Too Small", 
                    "Please select a larger area")
                self.cancel_capture()
                return
            
            self.root.withdraw()  # Hide window before taking screenshot
            
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
                    self.process_image(img)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture screen: {str(e)}")
        
        self.cancel_capture()
    
    def draw_selection(self):
        """Draw the selection rectangle"""
        self.canvas.delete('selection')
        self.canvas.create_rectangle(
            self.start_pos[0], self.start_pos[1],
            self.current_pos[0], self.current_pos[1],
            outline='blue', width=2, tags='selection'
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
                messagebox.showwarning("No Numbers Found", 
                    "No numbers were detected in the selected area.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
    
    def show_results(self, stats, numbers):
        """Show results in a floating window"""
        results_window = tk.Tk()
        results_window.title("SnippingCalc Results")
        results_window.geometry("400x300")
        
        # Style
        results_window.configure(bg='white')
        style = {
            'bg': 'white',
            'pady': 5,
            'font': ('Arial', 12)
        }
        
        # Add results
        tk.Label(results_window, text="Results", font=('Arial', 16, 'bold'), **style).pack(pady=10)
        
        # Create frame for statistics
        stats_frame = tk.Frame(results_window, bg='white')
        stats_frame.pack(fill='x', padx=20)
        
        # Add statistics with better formatting
        stats_text = {
            'SUM': f"{stats['SUM']:,.2f}",
            'AVG': f"{stats['AVG']:,.2f}",
            'COUNT': str(stats['COUNT'])
        }
        
        for label, value in stats_text.items():
            stat_frame = tk.Frame(stats_frame, bg='white')
            stat_frame.pack(fill='x', pady=5)
            tk.Label(stat_frame, text=f"{label}:", font=('Arial', 12, 'bold'), **style).pack(side='left')
            tk.Label(stat_frame, text=value, **style).pack(side='right')
        
        # Add numbers found
        tk.Label(results_window, text="Numbers found:", font=('Arial', 12, 'bold'), **style).pack(pady=(20,5))
        numbers_text = ", ".join(f"{n:,.2f}" for n in numbers)
        numbers_label = tk.Label(results_window, text=numbers_text, wraplength=350, **style)
        numbers_label.pack(padx=20)
        
        # Add copy button
        def copy_to_clipboard():
            text = f"SUM: {stats['SUM']:,.2f}\n"
            text += f"AVG: {stats['AVG']:,.2f}\n"
            text += f"COUNT: {stats['COUNT']}\n"
            text += f"Numbers: {numbers_text}"
            results_window.clipboard_clear()
            results_window.clipboard_append(text)
            messagebox.showinfo("Copied", "Results copied to clipboard!")
        
        copy_btn = tk.Button(
            results_window,
            text="Copy to Clipboard",
            command=copy_to_clipboard,
            font=('Arial', 11),
            bg='#007bff',
            fg='white',
            padx=20,
            pady=5
        )
        copy_btn.pack(pady=20)
    
    def save_results(self, stats, numbers):
        """Save results to a JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {
            'timestamp': timestamp,
            'stats': stats,
            'numbers': numbers
        }
        
        # Create results directory if it doesn't exist
        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        filename = os.path.join(results_dir, f'results_{timestamp}.json')
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

def on_activate():
    """Handle hotkey activation"""
    if not hasattr(on_activate, 'snipper'):
        on_activate.snipper = SnippingTool()
    
    if not on_activate.snipper.is_capturing:
        threading.Thread(target=on_activate.snipper.start_capture).start()

def main():
    # Check Tesseract installation
    if not setup_tesseract():
        sys.exit(1)
    
    print("SnippingCalc is running!")
    print("Press Ctrl+Shift+S to start capture")
    print("Press Ctrl+C to exit")
    
    try:
        # Setup hotkey listener
        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+s': on_activate
        }) as h:
            h.join()  # Keep the script running
    except Exception as e:
        print(f"Error: {str(e)}")
        if sys.platform.startswith('win'):
            print("\nTry running the script as Administrator")
        sys.exit(1)

if __name__ == "__main__":
    main()
