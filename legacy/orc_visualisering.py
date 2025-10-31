#!/usr/bin/env python3
"""
Visualisering av termodynamiska egenskaper för ORC-medier
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Läs in data
df_r245fa = pd.read_csv('/home/claude/R245fa_saturated.csv')
df_r1233zde = pd.read_csv('/home/claude/R1233zdE_saturated.csv')

# Skapa figur med subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Termodynamisk Jämförelse: R245fa vs R1233zd(E)\nORC Malung 10-80°C', 
             fontsize=16, fontweight='bold')

# Plot 1: Tryck vs Temperatur
ax1 = axes[0, 0]
ax1.plot(df_r245fa['T [°C]'], df_r245fa['p [bar]'], 'b-o', linewidth=2, label='R245fa', markersize=6)
ax1.plot(df_r1233zde['T [°C]'], df_r1233zde['p [bar]'], 'r-s', linewidth=2, label='R1233zd(E)', markersize=6)
ax1.axhspan(2, 10, alpha=0.1, color='green', label='Önskat tryck 2-10 bar')
ax1.axvspan(10, 30, alpha=0.1, color='blue', label='Kondensering 10-30°C')
ax1.axvspan(30, 80, alpha=0.1, color='red', label='Förångning 30-80°C')
ax1.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax1.set_ylabel('Mättningstryck [bar]', fontsize=11, fontweight='bold')
ax1.set_title('Saturationstryck', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9)

# Plot 2: Förångningsvärme vs Temperatur
ax2 = axes[0, 1]
ax2.plot(df_r245fa['T [°C]'], df_r245fa['hfg [kJ/kg]'], 'b-o', linewidth=2, label='R245fa', markersize=6)
ax2.plot(df_r1233zde['T [°C]'], df_r1233zde['hfg [kJ/kg]'], 'r-s', linewidth=2, label='R1233zd(E)', markersize=6)
ax2.axvline(50, color='green', linestyle='--', alpha=0.5, label='Drift 50°C')
ax2.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax2.set_ylabel('Förångningsvärme hfg [kJ/kg]', fontsize=11, fontweight='bold')
ax2.set_title('Förångningsvärme (Latent Heat)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=9)

# Plot 3: Viskositet vs Temperatur
ax3 = axes[1, 0]
ax3.plot(df_r245fa['T [°C]'], df_r245fa['μ_ånga [μPa·s]'], 'b-o', linewidth=2, label='R245fa', markersize=6)
ax3.plot(df_r1233zde['T [°C]'], df_r1233zde['μ_ånga [μPa·s]'], 'r-s', linewidth=2, label='R1233zd(E)', markersize=6)
ax3.axhline(12, color='gray', linestyle='--', alpha=0.5, label='Referens 12 μPa·s')
ax3.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax3.set_ylabel('Dynamisk viskositet ånga [μPa·s]', fontsize=11, fontweight='bold')
ax3.set_title('Viskositet (påverkar diskavstånd)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(fontsize=9)

# Plot 4: Ångdensitet vs Temperatur
ax4 = axes[1, 1]
ax4.plot(df_r245fa['T [°C]'], df_r245fa['ρ_ånga [kg/m³]'], 'b-o', linewidth=2, label='R245fa', markersize=6)
ax4.plot(df_r1233zde['T [°C]'], df_r1233zde['ρ_ånga [kg/m³]'], 'r-s', linewidth=2, label='R1233zd(E)', markersize=6)
ax4.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
ax4.set_ylabel('Ångdensitet [kg/m³]', fontsize=11, fontweight='bold')
ax4.set_title('Densitet i ångfas', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(fontsize=9)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/ORC_termo_jamforelse.png', dpi=300, bbox_inches='tight')
print("\n✓ Diagram sparat: ORC_termo_jamforelse.png")

# Skapa separat diagram för tryck-temperatur med optimal zon markerad
fig2, ax = plt.subplots(figsize=(12, 8))
ax.plot(df_r245fa['T [°C]'], df_r245fa['p [bar]'], 'b-o', linewidth=3, label='R245fa', markersize=8)
ax.plot(df_r1233zde['T [°C]'], df_r1233zde['p [bar]'], 'r-s', linewidth=3, label='R1233zd(E)', markersize=8)

# Markera viktiga zoner
ax.axhspan(2, 10, alpha=0.15, color='green')
ax.text(45, 5.5, 'ÖNSKAT TRYCK\n2-10 bar', fontsize=12, fontweight='bold', 
        ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

ax.axvspan(10, 30, alpha=0.1, color='blue')
ax.text(20, 0.5, 'KONDENSERING\n10-30°C', fontsize=11, fontweight='bold', ha='center')

ax.axvspan(30, 80, alpha=0.1, color='red')
ax.text(55, 0.5, 'FÖRÅNGNING\n30-80°C', fontsize=11, fontweight='bold', ha='center')

# Nyckeltemperaturer
for T in [10, 20, 30, 50, 80]:
    p_r245 = df_r245fa[df_r245fa['T [°C]'] == T]['p [bar]'].values[0]
    p_r1233 = df_r1233zde[df_r1233zde['T [°C]'] == T]['p [bar]'].values[0]
    ax.plot([T, T], [p_r245, p_r1233], 'k--', alpha=0.3, linewidth=1)
    ax.text(T, max(p_r245, p_r1233) + 0.3, f'{T}°C', fontsize=9, ha='center')

ax.set_xlabel('Temperatur [°C]', fontsize=14, fontweight='bold')
ax.set_ylabel('Mättningstryck [bar]', fontsize=14, fontweight='bold')
ax.set_title('Tryck-Temperatur Jämförelse: R245fa vs R1233zd(E)\nORC Malung Tesla-Turbin', 
             fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=12, loc='upper left')
ax.set_ylim(0, 9)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/ORC_tryck_temperatur.png', dpi=300, bbox_inches='tight')
print("✓ Diagram sparat: ORC_tryck_temperatur.png")

print("\n" + "="*60)
print("ALLA FILER GENERERADE:")
print("  1. R245fa_saturated.csv")
print("  2. R1233zdE_saturated.csv")
print("  3. ORC_termo_jamforelse.png")
print("  4. ORC_tryck_temperatur.png")
print("="*60)
