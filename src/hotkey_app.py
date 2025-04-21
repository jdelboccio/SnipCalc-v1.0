import keyboard
import tkinter as tk
from PIL import ImageGrab
import pytesseract
import re
from tkinter import messagebox

class SnippingTool:
    def __init__(self):
        # Initialize state
        self.is_snipping = False
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        # Register hotkey
        keyboard.add_hotkey('ctrl+shift+s', self.start_snip, suppress=True)
        
        # Create hidden root window
        self.root = tk.Tk()
        self.root.withdraw()
        
        print("SnippingCalc is running. Press Ctrl+Shift+S to start snipping.")
    
    def start_snip(self):
        if self.is_snipping:
            return
        
        self.is_snipping = True
        
        # Create fullscreen transparent window
        self.snip_window = tk.Toplevel(self.root)
        self.snip_window.attributes('-fullscreen', True, '-alpha', 0.3, '-topmost', True)
        self.snip_window.configure(bg='black')
        
        # Create canvas for drawing selection
        self.canvas = tk.Canvas(
            self.snip_window,
            cursor="cross",
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.snip_window.bind('<Escape>', self.cancel_snip)
        
        # Add instruction text
        self.canvas.create_text(
            self.snip_window.winfo_screenwidth() // 2,
            self.snip_window.winfo_screenheight() // 2,
            text="Click and drag to select area with numbers",
            fill="white",
            font=("Arial", 24)
        )
    
    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )
    
    def on_mouse_move(self, event):
        if self.current_rect:
            self.canvas.coords(
                self.current_rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
    
    def on_mouse_up(self, event):
        if self.start_x is None or self.start_y is None:
            return
        
        # Get coordinates
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        # Clean up
        self.snip_window.destroy()
        self.is_snipping = False
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        # Process the snip
        self.process_snip((x1, y1, x2, y2))
    
    def cancel_snip(self, event=None):
        self.snip_window.destroy()
        self.is_snipping = False
        self.start_x = None
        self.start_y = None
        self.current_rect = None
    
    def process_snip(self, bbox):
        try:
            # Capture the area
            image = ImageGrab.grab(bbox=bbox)
            
            # Extract text
            text = pytesseract.image_to_string(image)
            
            # Find numbers
            numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
            
            if not numbers:
                messagebox.showinfo("No Numbers", "No numbers were found in the selected area.")
                return
            
            # Calculate statistics
            total = sum(numbers)
            avg = total / len(numbers)
            count = len(numbers)
            
            # Show results
            result_text = f"SUM: {total:.2f}\nAVG: {avg:.2f}\nCOUNT: {count}"
            
            # Create results window
            result_window = tk.Toplevel(self.root)
            result_window.attributes('-topmost', True)
            result_window.title("Results")
            
            # Position near mouse
            mouse_x = self.root.winfo_pointerx()
            mouse_y = self.root.winfo_pointery()
            result_window.geometry(f"+{mouse_x + 10}+{mouse_y + 10}")
            
            # Add results
            label = tk.Label(
                result_window,
                text=result_text,
                font=("Arial", 12),
                padx=20,
                pady=10
            )
            label.pack()
            
            # Add copy button
            copy_button = tk.Button(
                result_window,
                text="Copy",
                command=lambda: [self.root.clipboard_clear(), 
                               self.root.clipboard_append(result_text),
                               result_window.destroy()]
            )
            copy_button.pack(pady=(0, 10))
            
            # Auto-close after 5 seconds
            result_window.after(5000, result_window.destroy)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process selection: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SnippingTool()
    app.run()
