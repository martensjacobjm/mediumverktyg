#!/usr/bin/env python3
"""
Termodynamisk data för ORC arbetsmedium
Genererar saturerade ångtabeller för R245fa och R1233zd(E)
"""

from CoolProp.CoolProp import PropsSI
import pandas as pd

def get_saturated_properties(fluid, temp_celsius):
    """Hämtar saturerade egenskaper vid given temperatur"""
    T = temp_celsius + 273.15  # Konvertera till Kelvin
    
    try:
        # Saturerade egenskaper
        p = PropsSI('P', 'T', T, 'Q', 0, fluid) / 1e5  # Pa → bar
        rho_l = PropsSI('D', 'T', T, 'Q', 0, fluid)     # Vätska densitet kg/m³
        rho_v = PropsSI('D', 'T', T, 'Q', 1, fluid)     # Ånga densitet kg/m³
        h_l = PropsSI('H', 'T', T, 'Q', 0, fluid) / 1000  # J/kg → kJ/kg
        h_v = PropsSI('H', 'T', T, 'Q', 1, fluid) / 1000  # J/kg → kJ/kg
        hfg = h_v - h_l
        s_l = PropsSI('S', 'T', T, 'Q', 0, fluid) / 1000  # J/kg·K → kJ/kg·K
        s_v = PropsSI('S', 'T', T, 'Q', 1, fluid) / 1000  # J/kg·K → kJ/kg·K
        mu_v = PropsSI('V', 'T', T, 'Q', 1, fluid) * 1e6  # Pa·s → μPa·s
        
        return {
            'T [°C]': temp_celsius,
            'p [bar]': round(p, 3),
            'ρ_vätska [kg/m³]': round(rho_l, 1),
            'ρ_ånga [kg/m³]': round(rho_v, 2),
            'h_vätska [kJ/kg]': round(h_l, 2),
            'h_ånga [kJ/kg]': round(h_v, 2),
            'hfg [kJ/kg]': round(hfg, 2),
            's_vätska [kJ/kg·K]': round(s_l, 4),
            's_ånga [kJ/kg·K]': round(s_v, 4),
            'μ_ånga [μPa·s]': round(mu_v, 2)
        }
    except Exception as e:
        print(f"Error för {fluid} vid {temp_celsius}°C: {e}")
        return None

def generate_table(fluid_name, fluid_coolprop, temp_range):
    """Genererar komplett tabell för ett medium"""
    print(f"\n{'='*80}")
    print(f"SATURERADE ÅNGTABELLER: {fluid_name}")
    print(f"{'='*80}\n")
    
    data = []
    for T in temp_range:
        props = get_saturated_properties(fluid_coolprop, T)
        if props:
            data.append(props)
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    
    return df

def critical_properties(fluid_name, fluid_coolprop):
    """Hämtar kritiska egenskaper"""
    try:
        T_crit = PropsSI('Tcrit', fluid_coolprop) - 273.15
        p_crit = PropsSI('pcrit', fluid_coolprop) / 1e5
        print(f"\n{fluid_name} - Kritiska egenskaper:")
        print(f"  T_kritisk: {T_crit:.2f}°C")
        print(f"  p_kritisk: {p_crit:.2f} bar")
    except:
        print(f"Kunde inte hämta kritiska egenskaper för {fluid_name}")

# Temperaturområden
temp_orc = list(range(10, 85, 5))  # 10-80°C i 5°C steg

# Generera tabeller
print("\n" + "="*80)
print("TERMODYNAMISK DATA FÖR ORC MALUNG")
print("="*80)

# R245fa
df_r245fa = generate_table("R245fa (HFC-245fa)", "R245fa", temp_orc)
critical_properties("R245fa", "R245fa")

# R1233zd(E)
df_r1233zde = generate_table("R1233zd(E)", "R1233zd(E)", temp_orc)
critical_properties("R1233zd(E)", "R1233zd(E)")

# Spara till CSV
df_r245fa.to_csv('/home/claude/R245fa_saturated.csv', index=False)
df_r1233zde.to_csv('/home/claude/R1233zdE_saturated.csv', index=False)

print("\n" + "="*80)
print("DATA SPARAD:")
print("  - R245fa_saturated.csv")
print("  - R1233zdE_saturated.csv")
print("="*80 + "\n")

# Jämförelse vid nyckeltemperaturer
print("\n" + "="*80)
print("DIREKT JÄMFÖRELSE VID NYCKELTEMPERATURER")
print("="*80 + "\n")

for T in [10, 20, 30, 50, 80]:
    print(f"\n--- {T}°C ---")
    
    r245_props = get_saturated_properties("R245fa", T)
    r1233_props = get_saturated_properties("R1233zd(E)", T)
    
    if r245_props and r1233_props:
        print(f"{'Parameter':<20} {'R245fa':>12} {'R1233zd(E)':>12} {'Skillnad':>12}")
        print("-" * 60)
        print(f"{'Tryck [bar]':<20} {r245_props['p [bar]']:>12.2f} {r1233_props['p [bar]']:>12.2f} {(r1233_props['p [bar]']-r245_props['p [bar]']):>12.2f}")
        print(f"{'hfg [kJ/kg]':<20} {r245_props['hfg [kJ/kg]']:>12.1f} {r1233_props['hfg [kJ/kg]']:>12.1f} {(r1233_props['hfg [kJ/kg]']-r245_props['hfg [kJ/kg]']):>12.1f}")
        print(f"{'μ_ånga [μPa·s]':<20} {r245_props['μ_ånga [μPa·s]']:>12.1f} {r1233_props['μ_ånga [μPa·s]']:>12.1f} {(r1233_props['μ_ånga [μPa·s]']-r245_props['μ_ånga [μPa·s]']):>12.1f}")
        print(f"{'ρ_ånga [kg/m³]':<20} {r245_props['ρ_ånga [kg/m³]']:>12.2f} {r1233_props['ρ_ånga [kg/m³]']:>12.2f} {(r1233_props['ρ_ånga [kg/m³]']-r245_props['ρ_ånga [kg/m³]']):>12.2f}")
