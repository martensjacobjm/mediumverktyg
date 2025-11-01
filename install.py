#!/usr/bin/env python3
"""
AUTOMATIC INSTALLATION SCRIPT
Checks Python version FIRST, then installs dependencies

Usage:
    python install.py
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    major = sys.version_info.major
    minor = sys.version_info.minor

    print("="*70)
    print("ORC WORKING FLUID ANALYSIS TOOL - AUTOMATIC INSTALLATION")
    print("="*70)
    print(f"\nStep 1/2: Checking Python version...")
    print(f"Current Python: {major}.{minor}")

    # Too old
    if major < 3 or (major == 3 and minor < 8):
        print("\n❌ ERROR: Python version too old!")
        print(f"\n   Current:  Python {major}.{minor}")
        print(f"   Required: Python 3.8 - 3.13")
        print("\nSOLUTION:")
        print("  Download Python 3.12 from https://www.python.org/downloads/")
        print("="*70)
        return False

    # Too new
    if major > 3 or (major == 3 and minor >= 14):
        print("\n❌ ERROR: Python 3.14+ is not yet supported!")
        print(f"\n   Current:  Python {major}.{minor}")
        print(f"   Required: Python 3.8 - 3.13")
        print("\n   Problem: CoolProp does not have packages for Python 3.14+ yet.")
        print("\nSOLUTION:")
        print("  1. Download Python 3.12: https://www.python.org/downloads/")
        print("  2. In VSCode: Ctrl+Shift+P → 'Python: Select Interpreter' → Python 3.12")
        print("  3. Run this script again: python install.py")
        print("="*70)
        return False

    # Compatible
    print(f"✅ Python {major}.{minor} is compatible!\n")
    return True

def install_dependencies():
    """Install all dependencies"""
    print("Step 2/2: Installing dependencies...")
    print("-"*70)

    try:
        # Run pip install
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=False,
            text=True
        )

        print("-"*70)
        print("\n✅ Installation completed successfully!")
        print("\nYou can now run the application:")
        print("  python main.py")
        print("="*70)
        return True

    except subprocess.CalledProcessError as e:
        print("\n❌ Installation failed!")
        print(f"\nError: {e}")
        print("\nTry installing manually:")
        print("  pip install -r requirements.txt")
        print("="*70)
        return False

def main():
    """Main installation flow"""

    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)

    # Step 2: Install dependencies
    if not install_dependencies():
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
