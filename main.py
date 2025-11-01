#!/usr/bin/env python3
"""
ORC Working Fluid Analysis Tool - Main Application
Dynamic tool for comparing 79+ working fluids for Tesla turbine ORC systems
"""

import sys

# Check Python version BEFORE importing anything else
if sys.version_info < (3, 8):
    print("\n" + "="*70)
    print("ERROR: Python 3.8 or higher is required!")
    print("="*70)
    print(f"\nCurrent version: Python {sys.version_info.major}.{sys.version_info.minor}")
    print("Required: Python 3.8 - 3.13")
    print("\nPlease install Python 3.12 from https://www.python.org/downloads/")
    print("="*70)
    sys.exit(1)

if sys.version_info >= (3, 14):
    print("\n" + "="*70)
    print("ERROR: Python 3.14+ is not yet supported!")
    print("="*70)
    print(f"\nCurrent version: Python {sys.version_info.major}.{sys.version_info.minor}")
    print("Required: Python 3.8 - 3.13")
    print("\nProblem: CoolProp (required dependency) does not have")
    print("         pre-built packages for Python 3.14+ yet.")
    print("\nSOLUTION:")
    print("  1. Install Python 3.12 from https://www.python.org/downloads/")
    print("  2. In VSCode: Ctrl+Shift+P → 'Python: Select Interpreter' → Python 3.12")
    print("  3. Run installation: pip install -e .")
    print("="*70)
    sys.exit(1)

import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindow


def main():
    """Main entry point for the application"""

    # Create root window
    root = tk.Tk()

    # Set window properties
    root.title("ORC Working Fluid Analysis Tool - Tesla Turbine")
    root.geometry("1600x900")
    root.minsize(1200, 700)

    # Try to set icon (optional)
    try:
        # root.iconbitmap('assets/icon.ico')  # Uncomment if icon available
        pass
    except:
        pass

    # Create main application window
    try:
        app = MainWindow(root)
    except Exception as e:
        messagebox.showerror(
            "Initialization Error",
            f"Failed to initialize application:\n{str(e)}\n\n"
            f"Please ensure all dependencies are installed:\n"
            f"pip install -r requirements.txt"
        )
        sys.exit(1)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    print("="*70)
    print("ORC WORKING FLUID ANALYSIS TOOL")
    print("Dynamic comparison of 79+ fluids for Tesla turbine ORC systems")
    print("="*70)
    print("\nStarting GUI...")

    main()
