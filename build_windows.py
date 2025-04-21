import os
import sys
import platform
import subprocess
import base64
import winreg
from pathlib import Path

def check_windows():
    """Check if running on Windows"""
    if platform.system() != "Windows":
        print("Error: This script must be run on Windows")
        print("Current platform:", platform.system())
        return False
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import winreg
        import win32com.client
        return True
    except ImportError as e:
        print(f"Error: Missing Windows dependencies - {e}")
        print("Please run: pip install pywin32")
        return False

def create_icon():
    """Create icon file from icon_data.py"""
    try:
        from src.icon_data import ICON_DATA
        icon_path = os.path.join('src', 'icon.ico')
        if not os.path.exists(icon_path):
            with open(icon_path, 'wb') as icon_file:
                icon_file.write(base64.b64decode(ICON_DATA.strip()))
        return icon_path
    except Exception as e:
        print(f"Warning: Could not create icon: {e}")
        return None

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        # Create icon
        icon_path = create_icon()
        
        # Build command
        cmd = [
            'pyinstaller',
            '--noconfirm',
            '--clean',
            '--windowed',
            '--uac-admin',
            '--name=SnippingCalc',
            'src/elegant_calc.py'
        ]
        
        # Add icon if available
        if icon_path and os.path.exists(icon_path):
            cmd.append(f'--icon={icon_path}')
        
        # Run PyInstaller
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def create_shortcut():
    """Create desktop and start menu shortcuts"""
    try:
        import win32com.client
        
        # Get paths
        exe_path = os.path.abspath(os.path.join('dist', 'SnippingCalc', 'SnippingCalc.exe'))
        if not os.path.exists(exe_path):
            print(f"Error: Executable not found at {exe_path}")
            return False
        
        # Create shell object
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Desktop shortcut
        desktop = shell.SpecialFolders("Desktop")
        shortcut_path = os.path.join(desktop, "SnippingCalc.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.Description = "Quick Calculator for Screen Numbers"
        shortcut.IconLocation = exe_path
        shortcut.save()
        
        # Start Menu shortcut
        start_menu = shell.SpecialFolders("StartMenu")
        start_menu_path = os.path.join(start_menu, "Programs", "SnippingCalc.lnk")
        os.makedirs(os.path.dirname(start_menu_path), exist_ok=True)
        shortcut = shell.CreateShortCut(start_menu_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.Description = "Quick Calculator for Screen Numbers"
        shortcut.IconLocation = exe_path
        shortcut.save()
        
        return True
    except Exception as e:
        print(f"Error creating shortcuts: {e}")
        return False

def setup_registry():
    """Add to startup registry"""
    try:
        exe_path = os.path.abspath(os.path.join('dist', 'SnippingCalc', 'SnippingCalc.exe'))
        
        # Add to registry for startup
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "SnippingCalc", 0, winreg.REG_SZ, exe_path)
        
        return True
    except Exception as e:
        print(f"Error setting up registry: {e}")
        return False

def main():
    print("SnippingCalc Build Script")
    print("------------------------")
    
    # Check platform
    if not check_windows():
        sys.exit(1)
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nPlease install required dependencies and try again:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("\nBuilding SnippingCalc...")
    try:
        # Build executable
        if not build_executable():
            print("Failed to build executable")
            return
        
        print("Creating shortcuts...")
        if not create_shortcut():
            return
        
        print("Setting up auto-start...")
        if not setup_registry():
            print("Failed to setup auto-start")
            return
        
        print("\nSnippingCalc has been successfully installed!")
        print("\nFeatures:")
        print("- Press Ctrl+Shift+S to activate")
        print("- Click and drag to select numbers")
        print("- Results appear automatically")
        print("- Sum is copied to clipboard")
        print("- Starts automatically with Windows")
        print("\nShortcuts created on Desktop and Start Menu")
        print("You can now use SnippingCalc!")
        
    except Exception as e:
        print(f"\nError during build: {str(e)}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
