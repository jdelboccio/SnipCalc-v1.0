import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QSystemTrayIcon, QMenu
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QColor, QPainter, QIcon
import mss
import numpy as np
import pytesseract
from PIL import Image
from calculator import calculate_stats

class SnippingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 100);')
        self.showFullScreen()
        
        self.begin = QPoint()
        self.end = QPoint()
        self.is_snipping = False
        
    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = QColor(0, 0, 0, 100)
            painter = QPainter(self)
            painter.fillRect(0, 0, self.width(), self.height(), brush_color)
            
            if not self.begin.isNull() and not self.end.isNull():
                rect = QRect(self.begin, self.end)
                painter.eraseRect(rect)
                
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.is_snipping = True
        self.update()
        
    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        
    def mouseReleaseEvent(self, event):
        self.capture()
        
    def capture(self):
        if self.begin and self.end:
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            x2 = max(self.begin.x(), self.end.x())
            y2 = max(self.begin.y(), self.end.y())
            
            # Capture the selected region
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
                
                # Perform OCR
                text = pytesseract.image_to_string(img)
                
                # Extract numbers
                import re
                numbers = [float(x) for x in re.findall(r'-?\d*\.?\d+', text)]
                
                if numbers:
                    # Calculate statistics
                    stats = calculate_stats(numbers)
                    
                    # Show results
                    ResultWindow(stats, numbers)
                else:
                    # Show error message
                    from PyQt5.QtWidgets import QMessageBox
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("No numbers found in the selected area")
                    msg.setWindowTitle("No Numbers Detected")
                    msg.exec_()
        
        self.close()

class ResultWindow(QWidget):
    def __init__(self, stats, numbers):
        super().__init__()
        self.stats = stats
        self.numbers = numbers
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Results')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        
        # Add results
        layout.addWidget(QLabel(f"SUM: {self.stats['SUM']:.2f}"))
        layout.addWidget(QLabel(f"AVG: {self.stats['AVG']:.2f}"))
        layout.addWidget(QLabel(f"COUNT: {self.stats['COUNT']}"))
        
        # Add numbers found
        numbers_label = QLabel("Numbers found:")
        numbers_text = ", ".join([f"{n:.2f}" for n in self.numbers])
        numbers_label.setWordWrap(True)
        layout.addWidget(numbers_label)
        layout.addWidget(QLabel(numbers_text))
        
        # Add copy button
        copy_btn = QPushButton('Copy Results')
        copy_btn.clicked.connect(self.copy_results)
        layout.addWidget(copy_btn)
        
        self.setLayout(layout)
        self.show()
        
    def copy_results(self):
        import pyperclip
        text = f"SUM: {self.stats['SUM']:.2f}\n"
        text += f"AVG: {self.stats['AVG']:.2f}\n"
        text += f"COUNT: {self.stats['COUNT']}\n"
        text += f"Numbers: {', '.join([f'{n:.2f}' for n in self.numbers])}"
        pyperclip.copy(text)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip('SnippingCalc')
        
        # Create menu
        menu = QMenu()
        exit_action = menu.addAction('Exit')
        exit_action.triggered.connect(sys.exit)
        
        self.setContextMenu(menu)
        self.show()

def start_snipping():
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)
    
    snipper = SnippingWidget()
    snipper.show()
    app.exec_()

def main():
    app = QApplication(sys.argv)
    
    # Create system tray icon
    tray_icon = SystemTrayIcon()
    
    # Register global hotkey (Ctrl+Shift+S)
    keyboard.add_hotkey('ctrl+shift+s', start_snipping)
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
