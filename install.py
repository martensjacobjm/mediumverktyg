#!/usr/bin/env python3
"""
TRULY AUTOMATIC INSTALLATION
Finds correct Python version automatically and installs to it
"""

import sys
import subprocess
import os
import platform

def find_compatible_python():
    """Find a compatible Python version (3.8-3.13) on the system"""

    print("="*70)
    print("ORC WORKING FLUID ANALYSIS TOOL - SMART INSTALLATION")
    print("="*70)
    print("\nSearching for compatible Python versions...")
    print("-"*70)

    compatible_pythons = []

    # On Windows, use py launcher to find all versions
    if platform.system() == "Windows":
        try:
            # List all installed Python versions
            result = subprocess.run(
                ["py", "-0"],
                capture_output=True,
                text=True,
                timeout=5
            )

            print("\nInstalled Python versions:")
            print(result.stdout)

            # Try each version from 3.13 down to 3.8
            for minor in range(13, 7, -1):
                version_str = f"-3.{minor}"
                try:
                    check_result = subprocess.run(
                        ["py", version_str, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if check_result.returncode == 0:
                        version = check_result.stdout.strip()
                        print(f"  ✅ Found: {version} (py {version_str})")
                        compatible_pythons.append((f"py {version_str}", version, minor))
                except:
                    pass

        except FileNotFoundError:
            print("  ⚠️  'py' launcher not found (older Python installation)")

    # Also check current python command
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        major, minor = sys.version_info.major, sys.version_info.minor
        if major == 3 and 8 <= minor <= 13:
            version = result.stdout.strip()
            print(f"  ✅ Current python: {version}")
            compatible_pythons.append((sys.executable, version, minor))
    except:
        pass

    print("-"*70)

    if not compatible_pythons:
        print("\n❌ NO COMPATIBLE PYTHON FOUND!")
        print("\nRequired: Python 3.8 - 3.13")
        print("\nSOLUTION:")
        print("  1. Download Python 3.12: https://www.python.org/downloads/release/python-3120/")
        print("  2. Install it")
        print("  3. Run this script again")
        print("="*70)
        return None

    # Use the newest compatible version
    compatible_pythons.sort(key=lambda x: x[2], reverse=True)
    chosen = compatible_pythons[0]

    print(f"\n✅ SELECTED: {chosen[1]}")
    print(f"   Command: {chosen[0]}")
    print("-"*70)

    return chosen[0]

def install_with_python(python_cmd):
    """Install dependencies using the specified Python"""

    print("\nInstalling dependencies...")
    print("-"*70)

    try:
        # Split command if it's like "py -3.12"
        cmd_parts = python_cmd.split()
        install_cmd = cmd_parts + ["-m", "pip", "install", "-r", "requirements.txt"]

        result = subprocess.run(
            install_cmd,
            check=True
        )

        print("-"*70)
        print("\n✅ INSTALLATION COMPLETED SUCCESSFULLY!")
        print("="*70)
        return True

    except subprocess.CalledProcessError as e:
        print("\n❌ Installation failed!")
        print(f"Error: {e}")
        print("="*70)
        return False

def create_start_script(python_cmd):
    """Create a start script that uses the correct Python version"""

    if platform.system() == "Windows":
        # Create start.bat
        with open("start.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"{python_cmd} main.py\n")
            f.write(f"pause\n")

        print("\n✅ Created 'start.bat' - Double-click to run the program!")
        print(f"   (Uses: {python_cmd})")
    else:
        # Create start.sh
        with open("start.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"{python_cmd} main.py\n")

        os.chmod("start.sh", 0o755)
        print("\n✅ Created 'start.sh' - Run: ./start.sh")
        print(f"   (Uses: {python_cmd})")

def main():
    """Main installation flow"""

    # Find compatible Python
    python_cmd = find_compatible_python()
    if not python_cmd:
        sys.exit(1)

    # Install dependencies
    if not install_with_python(python_cmd):
        sys.exit(1)

    # Create start script
    create_start_script(python_cmd)

    print("\n" + "="*70)
    print("READY TO USE!")
    print("="*70)
    if platform.system() == "Windows":
        print("\nTo start the program:")
        print("  • Double-click: start.bat")
        print(f"  • Or run: {python_cmd} main.py")
    else:
        print("\nTo start the program:")
        print("  • Run: ./start.sh")
        print(f"  • Or run: {python_cmd} main.py")
    print("="*70)

if __name__ == "__main__":
    main()
