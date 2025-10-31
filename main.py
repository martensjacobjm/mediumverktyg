#!/usr/bin/env python3
"""
ORC Working Fluid Analysis Tool - Main Application
Dynamic tool for comparing 79+ working fluids for Tesla turbine ORC systems
"""

import sys
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
