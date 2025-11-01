#!/usr/bin/env python3
"""
Setup script for ORC Working Fluid Analysis Tool
Ensures correct Python version before installation
"""

import sys
from setuptools import setup, find_packages

# Check Python version BEFORE attempting to install anything
if sys.version_info < (3, 8):
    sys.exit("Error: Python 3.8 or higher is required (you have Python {}.{})".format(
        sys.version_info.major, sys.version_info.minor))

if sys.version_info >= (3, 14):
    sys.exit("""
Error: Python 3.14+ is not yet supported!

CoolProp (required dependency) does not have pre-built packages for Python 3.14.

SOLUTION:
  1. Install Python 3.12 or 3.13 from https://www.python.org/downloads/
  2. Select that Python version in VSCode (Ctrl+Shift+P → "Python: Select Interpreter")
  3. Run: pip install -r requirements.txt

Current Python version: {}.{}
Required: Python 3.8 - 3.13
""".format(sys.version_info.major, sys.version_info.minor))

# Read requirements from requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="orc-fluid-analysis-tool",
    version="1.0.0",
    description="Dynamic ORC Working Fluid Analysis Tool with Tesla Turbine Design",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/martensjacobjm/mediumverktyg",
    packages=find_packages(),
    python_requires=">=3.8,<3.14",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'orc-tool=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
