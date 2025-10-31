#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER-SKRIPT: Genererar komplett ORC-rapport med diagram
Kör i rätt ordning: Diagram först, sedan Word-rapport
"""

import os
import sys
from datetime import datetime

# Fixa encoding för Windows konsol
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("\n" + "="*80)
print(" "*20 + "ORC MALUNG - RAPPORT-GENERATOR")
print("="*80)
print(f"\nStartad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Arbetsmapp: {os.path.dirname(os.path.abspath(__file__))}")
print("\n" + "="*80)

# Kontrollera att nödvändiga moduler finns
required_modules = ['CoolProp', 'matplotlib', 'docx', 'numpy']
missing_modules = []

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print("\n[!] SAKNADE MODULER:")
    for module in missing_modules:
        print(f"   - {module}")
    print("\nInstallera med: pip install " + " ".join(missing_modules))
    print("="*80 + "\n")
    sys.exit(1)

print("\n[OK] Alla noedvaendiga moduler aer installerade")

# ============================================================================
# STEG 1: GENERERA DIAGRAM
# ============================================================================

print("\n" + "-"*80)
print("STEG 1/2: GENERERAR DIAGRAM")
print("-"*80)

try:
    import generate_diagrams
    print("\n[OK] Diagram genererade framgangsrikt!")
except Exception as e:
    print(f"\n[FEL] FEL vid generering av diagram: {e}")
    print("\nFortsaetter aendaa med rapport (diagram kommer att saknas)...")

# ============================================================================
# STEG 2: GENERERA WORD-RAPPORT
# ============================================================================

print("\n" + "-"*80)
print("STEG 2/2: GENERERAR WORD-RAPPORT")
print("-"*80)

try:
    import generate_rapport
    print("\n[OK] Word-rapport genererad framgangsrikt!")
except Exception as e:
    print(f"\n[FEL] FEL vid generering av rapport: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# SAMMANFATTNING
# ============================================================================

output_dir = os.path.join(os.path.dirname(__file__), 'outputs')

print("\n" + "="*80)
print(" "*25 + "GENERERING KLAR!")
print("="*80)

print(f"\nOutput-mapp: {os.path.abspath(output_dir)}")

print("\nGenererade filer:")

# Lista alla filer i output-mappen
if os.path.exists(output_dir):
    files = os.listdir(output_dir)

    # Sortera så att .docx kommer först, sedan .png
    docx_files = [f for f in files if f.endswith('.docx')]
    png_files = [f for f in files if f.endswith('.png')]
    other_files = [f for f in files if not (f.endswith('.docx') or f.endswith('.png'))]

    for f in docx_files:
        size = os.path.getsize(os.path.join(output_dir, f))
        print(f"   [OK] {f} ({size/1024:.1f} KB) - WORD-RAPPORT")

    for f in png_files:
        size = os.path.getsize(os.path.join(output_dir, f))
        print(f"   [OK] {f} ({size/1024:.1f} KB) - Diagram")

    for f in other_files:
        size = os.path.getsize(os.path.join(output_dir, f))
        print(f"   [OK] {f} ({size/1024:.1f} KB)")

    if not files:
        print("   (Inga filer genererade)")
else:
    print("   [!] Output-mappen finns inte")

print("\n" + "="*80)
print("\nNaesta steg:")
print("   1. Oeppna Word-rapporten i outputs-mappen")
print("   2. Granska diagram och tabeller")
print("   3. Justera formatering vid behov")
print("   4. Exportera till PDF foer slutgiltig version")

print("\n" + "="*80)
print(f"Avslutad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80 + "\n")
