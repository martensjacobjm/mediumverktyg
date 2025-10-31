#!/usr/bin/env python3
"""
Genererar diagram för ORC medium-analys rapporten
"""

import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
import os

# Skapa output-mapp om den inte finns
output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(output_dir, exist_ok=True)

print("\n" + "="*70)
print("GENERERAR ORC DIAGRAM")
print("="*70)

# ============================================================================
# DIAGRAM 1: TRYCK-TEMPERATUR JÄMFÖRELSE
# ============================================================================

print("\nGenererar Diagram 1: Tryck-Temperatur jämförelse...")

# Temperaturer 0-100°C
temps = np.linspace(0, 100, 101)

# Beräkna tryck för varje medium
fluids = {
    'R1233zd(E)': {'color': '#1f77b4', 'marker': 'o'},
    'R245fa': {'color': '#ff7f0e', 'marker': 's'}
}

pressures = {}
for fluid_name in fluids.keys():
    p_list = []
    for T_celsius in temps:
        T_kelvin = T_celsius + 273.15
        try:
            # Mättningstryck vid given temperatur
            p_bar = PropsSI('P', 'T', T_kelvin, 'Q', 1, fluid_name) / 1e5
            p_list.append(p_bar)
        except:
            p_list.append(np.nan)
    pressures[fluid_name] = p_list

# Plotta
fig, ax = plt.subplots(figsize=(10, 6))

for fluid_name, style in fluids.items():
    ax.plot(temps, pressures[fluid_name],
            label=fluid_name,
            color=style['color'],
            linewidth=2.5,
            marker=style['marker'],
            markevery=10,
            markersize=6)

# Markera viktiga temperaturer
important_temps = [10, 20, 50, 80]
for T in important_temps:
    ax.axvline(T, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
    ax.text(T, ax.get_ylim()[1]*0.95, f'{T}°C',
            ha='center', fontsize=9, color='gray')

# Markera viktiga tryck
ax.axhline(3.0, color='red', linestyle=':', alpha=0.4, linewidth=1.0)
ax.text(5, 3.1, '3 bar design limit', fontsize=9, color='red', alpha=0.7)

ax.set_xlabel('Temperatur [°C]', fontsize=12, fontweight='bold')
ax.set_ylabel('Mättningstryck [bar]', fontsize=12, fontweight='bold')
ax.set_title('Tryck-Temperatur Jämförelse: R1233zd(E) vs R245fa',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_xlim(0, 100)
ax.set_ylim(0, 12)

plt.tight_layout()
diagram1_path = os.path.join(output_dir, 'ORC_tryck_temperatur.png')
plt.savefig(diagram1_path, dpi=300, bbox_inches='tight')
print(f"✓ Diagram 1 sparat: {diagram1_path}")
plt.close()

# ============================================================================
# DIAGRAM 2: TERMODYNAMISK 4-PANEL JÄMFÖRELSE
# ============================================================================

print("\nGenererar Diagram 2: Termodynamisk 4-panel jämförelse...")

# Temperaturer för detaljerade egenskaper
temps_detail = np.linspace(10, 80, 36)

# Samla data för alla medier
data = {}
for fluid_name in fluids.keys():
    data[fluid_name] = {
        'pressure': [],
        'hfg': [],
        'viscosity': [],
        'density': []
    }

    for T_celsius in temps_detail:
        T_kelvin = T_celsius + 273.15
        try:
            # Mättningstryck
            p_bar = PropsSI('P', 'T', T_kelvin, 'Q', 1, fluid_name) / 1e5
            data[fluid_name]['pressure'].append(p_bar)

            # Förångningsvärme
            h_vap = PropsSI('H', 'T', T_kelvin, 'Q', 1, fluid_name) / 1000  # kJ/kg
            h_liq = PropsSI('H', 'T', T_kelvin, 'Q', 0, fluid_name) / 1000  # kJ/kg
            hfg = h_vap - h_liq
            data[fluid_name]['hfg'].append(hfg)

            # Viskositet (ånga)
            mu_vap = PropsSI('V', 'T', T_kelvin, 'Q', 1, fluid_name) * 1e6  # μPa·s
            data[fluid_name]['viscosity'].append(mu_vap)

            # Densitet (ånga)
            rho_vap = PropsSI('D', 'T', T_kelvin, 'Q', 1, fluid_name)  # kg/m³
            data[fluid_name]['density'].append(rho_vap)
        except:
            data[fluid_name]['pressure'].append(np.nan)
            data[fluid_name]['hfg'].append(np.nan)
            data[fluid_name]['viscosity'].append(np.nan)
            data[fluid_name]['density'].append(np.nan)

# Skapa 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Termodynamisk Jämförelse: R1233zd(E) vs R245fa',
             fontsize=16, fontweight='bold', y=0.995)

# Panel 1: Mättningstryck
ax1 = axes[0, 0]
for fluid_name, style in fluids.items():
    ax1.plot(temps_detail, data[fluid_name]['pressure'],
             label=fluid_name, color=style['color'], linewidth=2.5,
             marker=style['marker'], markevery=4, markersize=5)
ax1.axvline(50, color='gray', linestyle='--', alpha=0.3)
ax1.text(50, ax1.get_ylim()[1]*0.9, 'Drift\n50°C', ha='center', fontsize=9)
ax1.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax1.set_ylabel('Mättningstryck [bar]', fontsize=11, fontweight='bold')
ax1.set_title('(a) Mättningstryck', fontsize=12, fontweight='bold', pad=10)
ax1.legend(fontsize=10, loc='upper left')
ax1.grid(True, alpha=0.3)

# Panel 2: Förångningsvärme
ax2 = axes[0, 1]
for fluid_name, style in fluids.items():
    ax2.plot(temps_detail, data[fluid_name]['hfg'],
             label=fluid_name, color=style['color'], linewidth=2.5,
             marker=style['marker'], markevery=4, markersize=5)
ax2.axvline(50, color='gray', linestyle='--', alpha=0.3)
ax2.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax2.set_ylabel('Förångningsvärme hfg [kJ/kg]', fontsize=11, fontweight='bold')
ax2.set_title('(b) Förångningsvärme', fontsize=12, fontweight='bold', pad=10)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.3)

# Panel 3: Viskositet
ax3 = axes[1, 0]
for fluid_name, style in fluids.items():
    ax3.plot(temps_detail, data[fluid_name]['viscosity'],
             label=fluid_name, color=style['color'], linewidth=2.5,
             marker=style['marker'], markevery=4, markersize=5)
ax3.axvline(50, color='gray', linestyle='--', alpha=0.3)
ax3.axhline(18.2, color='purple', linestyle=':', alpha=0.5, linewidth=1.5)
ax3.text(15, 18.5, 'Luft (TesTur ref)', fontsize=9, color='purple')
ax3.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax3.set_ylabel('Viskositet ånga [μPa·s]', fontsize=11, fontweight='bold')
ax3.set_title('(c) Viskositet (påverkar diskavstånd)', fontsize=12, fontweight='bold', pad=10)
ax3.legend(fontsize=10, loc='upper left')
ax3.grid(True, alpha=0.3)

# Panel 4: Densitet
ax4 = axes[1, 1]
for fluid_name, style in fluids.items():
    ax4.plot(temps_detail, data[fluid_name]['density'],
             label=fluid_name, color=style['color'], linewidth=2.5,
             marker=style['marker'], markevery=4, markersize=5)
ax4.axvline(50, color='gray', linestyle='--', alpha=0.3)
ax4.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax4.set_ylabel('Ångdensitet [kg/m³]', fontsize=11, fontweight='bold')
ax4.set_title('(d) Ångdensitet', fontsize=12, fontweight='bold', pad=10)
ax4.legend(fontsize=10, loc='upper left')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
diagram2_path = os.path.join(output_dir, 'ORC_termo_jamforelse.png')
plt.savefig(diagram2_path, dpi=300, bbox_inches='tight')
print(f"✓ Diagram 2 sparat: {diagram2_path}")
plt.close()

# ============================================================================
# SAMMANFATTNING
# ============================================================================

print("\n" + "="*70)
print("DIAGRAM GENERERING KLAR!")
print("="*70)
print(f"\nOutput-mapp: {output_dir}")
print(f"\nGenererade filer:")
print(f"  1. ORC_tryck_temperatur.png (Tryck vs Temp)")
print(f"  2. ORC_termo_jamforelse.png (4-panel jämförelse)")
print("\nDessa diagram kan nu användas i Word-rapporten.")
print("="*70 + "\n")
