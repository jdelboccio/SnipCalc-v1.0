import tkinter as tk
from tkinter import ttk
import pyperclip
from typing import Dict

class ResultWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, stats: Dict[str, float]):
        """
        Initialize the results window
        
        Args:
            parent: Parent window
            stats: Dictionary containing SUM, AVG, and COUNT values
        """
        super().__init__(parent)
        
        # Configure the window
        self.title("Results")
        self.configure(bg='#2C2C2C')
        self.attributes('-topmost', True)
        
        # Remove window decorations and add custom styling
        self.overrideredirect(True)
        self.configure(bd=2, relief='solid')
        
        # Calculate position (center of screen)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 250
        window_height = 180
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame
        self.main_frame = tk.Frame(self, bg='#2C2C2C', padx=15, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add title
        title = tk.Label(
            self.main_frame,
            text="Calculation Results",
            font=("Segoe UI", 12, "bold"),
            fg='white',
            bg='#2C2C2C'
        )
        title.pack(pady=(0, 10))
        
        # Add results
        self.create_result_label("SUM", stats['SUM'])
        self.create_result_label("AVG", stats['AVG'])
        self.create_result_label("COUNT", stats['COUNT'])
        
        # Add buttons
        button_frame = tk.Frame(self.main_frame, bg='#2C2C2C')
        button_frame.pack(pady=(10, 0), fill=tk.X)
        
        # Copy button
        copy_btn = tk.Button(
            button_frame,
            text="Copy",
            command=lambda: self.copy_to_clipboard(stats),
            bg='#404040',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self.destroy,
            bg='#404040',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bind mouse events for window dragging
        self.bind('<Button-1>', self.start_move)
        self.bind('<B1-Motion>', self.on_move)
        
        # Auto-close timer (5 seconds)
        self.after(5000, self.destroy)
    
    def create_result_label(self, label: str, value: float):
        """Create a label-value pair for results"""
        frame = tk.Frame(self.main_frame, bg='#2C2C2C')
        frame.pack(fill=tk.X, pady=2)
        
        # Label
        tk.Label(
            frame,
            text=f"{label}:",
            font=("Segoe UI", 10),
            fg='#CCCCCC',
            bg='#2C2C2C',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        # Value
        tk.Label(
            frame,
            text=str(value),
            font=("Segoe UI", 10, "bold"),
            fg='white',
            bg='#2C2C2C'
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    def copy_to_clipboard(self, stats: Dict[str, float]):
        """Copy results to clipboard"""
        text = f"SUM: {stats['SUM']}\nAVG: {stats['AVG']}\nCOUNT: {stats['COUNT']}"
        pyperclip.copy(text)
    
    def start_move(self, event):
        """Start window drag"""
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        """Handle window drag"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
