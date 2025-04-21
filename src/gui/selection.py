import tkinter as tk
from typing import Callable, Optional, Tuple

class SelectionWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, callback: Callable[[Tuple[int, int, int, int]], None]):
        """
        Initialize the selection window
        
        Args:
            parent: Parent window
            callback: Function to call with selection coordinates
        """
        super().__init__(parent)
        
        self.callback = callback
        self.selection_rect = None
        self.start_x = None
        self.start_y = None
        
        # Configure the window
        self.attributes('-alpha', 0.3)  # Semi-transparent
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)
        
        # Configure the canvas
        self.canvas = tk.Canvas(
            self,
            cursor="cross",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Escape>', self.cancel)
        
        # Add instructions
        self.canvas.create_text(
            self.winfo_screenwidth() // 2,
            self.winfo_screenheight() // 2,
            text="Click and drag to select area",
            fill="white",
            font=("Segoe UI", 24)
        )
    
    def on_press(self, event):
        """Handle mouse press event"""
        self.start_x = event.x
        self.start_y = event.y
        
        # Create selection rectangle
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline='white'
        )
    
    def on_drag(self, event):
        """Handle mouse drag event"""
        if self.selection_rect:
            # Update rectangle as mouse moves
            self.canvas.coords(
                self.selection_rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
    
    def on_release(self, event):
        """Handle mouse release event"""
        if self.selection_rect:
            # Get the final coordinates
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            # Ensure minimum size
            if x2 - x1 > 10 and y2 - y1 > 10:
                self.callback((x1, y1, x2, y2))
            else:
                self.cancel(None)
    
    def cancel(self, event):
        """Cancel the selection"""
        self.callback(None)
        self.destroy()
