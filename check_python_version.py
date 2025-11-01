#!/usr/bin/env python3
"""
Python Version Check Script
Run this before installing dependencies to verify Python version compatibility
"""

import sys

def check_python_version():
    """Check if Python version is compatible with this project"""

    major = sys.version_info.major
    minor = sys.version_info.minor
    current_version = f"{major}.{minor}"

    print("="*70)
    print("ORC WORKING FLUID ANALYSIS TOOL - Python Version Check")
    print("="*70)
    print(f"\nCurrent Python version: {current_version}")
    print(f"Full version: {sys.version}")

    # Check if Python is too old
    if major < 3 or (major == 3 and minor < 8):
        print("\n❌ ERROR: Python version too old!")
        print(f"\n   Current:  Python {current_version}")
        print(f"   Required: Python 3.8 or higher")
        print("\nSOLUTION:")
        print("  1. Download Python 3.12 from https://www.python.org/downloads/")
        print("  2. Install and add to PATH")
        print("  3. Restart your terminal/VSCode")
        return False

    # Check if Python is too new
    if major > 3 or (major == 3 and minor >= 14):
        print("\n❌ ERROR: Python version too new!")
        print(f"\n   Current:  Python {current_version}")
        print(f"   Required: Python 3.8 - 3.13")
        print("\n   Problem: CoolProp (required dependency) does not have")
        print("            pre-built packages for Python 3.14+ yet.")
        print("\nSOLUTION:")
        print("  1. Download Python 3.12 from https://www.python.org/downloads/")
        print("  2. Install (keep Python 3.14 if you want - you can have both)")
        print("  3. In VSCode:")
        print("     - Press Ctrl+Shift+P")
        print("     - Type: 'Python: Select Interpreter'")
        print("     - Choose Python 3.12")
        print("  4. Run installation again")
        return False

    # Version is compatible
    print(f"\n✅ Python {current_version} is compatible!")
    print("\nYou can now install dependencies:")
    print("  pip install -e .")
    print("\nOr run the application:")
    print("  python main.py")
    print("="*70)
    return True

if __name__ == "__main__":
    success = check_python_version()
    sys.exit(0 if success else 1)
