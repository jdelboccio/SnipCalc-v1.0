import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab
import pytesseract
import re
from src.calculator import calculate_stats
from src.gui.results import ResultWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SnippingCalc")
        self.geometry("400x150")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        
        self.snip_mode = tk.StringVar(value="Rectangular Snip")
        
        # Toolbar frame
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # New Snip button
        self.new_snip_btn = ttk.Button(toolbar, text="New Snip", command=self.start_snip)
        self.new_snip_btn.pack(side=tk.LEFT, padx=2)
        
        # Snip mode dropdown
        modes = ["Rectangular Snip", "Free-form Snip", "Window Snip", "Full-screen Snip"]
        self.mode_combo = ttk.Combobox(toolbar, values=modes, state="readonly", textvariable=self.snip_mode)
        self.mode_combo.pack(side=tk.LEFT, padx=2)
        
        # Delay option
        delay_label = ttk.Label(toolbar, text="Delay (sec):")
        delay_label.pack(side=tk.LEFT, padx=2)
        self.delay_var = tk.IntVar(value=0)
        self.delay_spin = ttk.Spinbox(toolbar, from_=0, to=10, width=3, textvariable=self.delay_var)
        self.delay_spin.pack(side=tk.LEFT, padx=2)
        
        # Info label
        self.info_label = ttk.Label(self, text="Press 'New Snip' to start snipping.", background="#f0f0f0")
        self.info_label.pack(pady=20)
        
        self.result_window = None
    
    def start_snip(self):
        delay = self.delay_var.get()
        self.info_label.config(text=f"Snipping will start in {delay} seconds...")
        self.after(delay * 1000, self.perform_snip)
    
    def perform_snip(self):
        mode = self.snip_mode.get()
        self.info_label.config(text=f"Performing {mode}...")
        
        # For simplicity, implement only rectangular snip for now
        if mode == "Rectangular Snip":
            self.withdraw()
            self.after(200, self.rectangular_snip)
        else:
            messagebox.showinfo("Info", f"{mode} is not implemented yet.")
            self.info_label.config(text="Press 'New Snip' to start snipping.")
    
    def rectangular_snip(self):
        # Create a fullscreen transparent window for selection
        self.snip_window = tk.Toplevel(self)
        self.snip_window.attributes("-fullscreen", True)
        self.snip_window.attributes("-alpha", 0.3)
        self.snip_window.configure(bg="black")
        self.snip_window.attributes("-topmost", True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas = tk.Canvas(self.snip_window, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.snip_window.bind("<Escape>", self.cancel_snip)
    
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
    
    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
    
    def on_button_release(self, event):
        self.snip_window.destroy()
        self.deiconify()
        
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        bbox = (x1, y1, x2, y2)
        self.process_snip(bbox)
    
    def cancel_snip(self, event):
        self.snip_window.destroy()
        self.deiconify()
        self.info_label.config(text="Snip cancelled. Press 'New Snip' to start again.")
    
    def process_snip(self, bbox):
        try:
            image = ImageGrab.grab(bbox)
            text = pytesseract.image_to_string(image)
            numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
            if not numbers:
                messagebox.showinfo("No numbers found", "No numbers were detected in the selected area.")
                self.info_label.config(text="Press 'New Snip' to start snipping.")
                return
            stats = calculate_stats(numbers)
            if self.result_window:
                self.result_window.destroy()
            self.result_window = ResultWindow(self, stats)
            self.info_label.config(text="Results displayed. Press 'New Snip' to start again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process snip: {e}")
            self.info_label.config(text="Press 'New Snip' to start snipping.")
