#!/usr/bin/env python3
"""
ORC DIMENSIONERINGS-KALKYLATOR
Interaktiv beräkning för ORC Malung Tesla-Turbin projekt
"""

from CoolProp.CoolProp import PropsSI

def get_props(fluid, T_hot, T_cold):
    """Hämtar termodynamiska egenskaper vid drifttemperaturer"""
    T_h = T_hot + 273.15
    T_c = T_cold + 273.15
    
    # Högtryckssida (förångning)
    p_high = PropsSI('P', 'T', T_h, 'Q', 1, fluid) / 1e5  # bar
    h_vap = PropsSI('H', 'T', T_h, 'Q', 1, fluid) / 1000  # kJ/kg
    rho_vap = PropsSI('D', 'T', T_h, 'Q', 1, fluid)  # kg/m³
    mu_vap = PropsSI('V', 'T', T_h, 'Q', 1, fluid) * 1e6  # μPa·s
    
    # Lågtryckssida (kondensering)
    p_low = PropsSI('P', 'T', T_c, 'Q', 0, fluid) / 1e5  # bar
    h_liq = PropsSI('H', 'T', T_c, 'Q', 0, fluid) / 1000  # kJ/kg
    rho_liq = PropsSI('D', 'T', T_c, 'Q', 0, fluid)  # kg/m³
    
    hfg = h_vap - h_liq
    
    return {
        'p_high': p_high,
        'p_low': p_low,
        'h_vap': h_vap,
        'h_liq': h_liq,
        'hfg': hfg,
        'rho_vap': rho_vap,
        'rho_liq': rho_liq,
        'mu_vap': mu_vap,
        'PR': p_high / p_low
    }

def calc_system(fluid_name, fluid_coolprop, T_hot, T_cold, P_target_kW, 
                eta_turb=0.55, eta_gen=0.93, eta_pump=0.65):
    """Beräknar komplett ORC-system"""
    
    print(f"\n{'='*70}")
    print(f"ORC SYSTEMBERÄKNING: {fluid_name}")
    print(f"{'='*70}")
    
    # Termodynamiska egenskaper
    props = get_props(fluid_coolprop, T_hot, T_cold)
    
    print(f"\n--- DRIFTFÖRHÅLLANDEN ---")
    print(f"Förångning:        {T_hot}°C vid {props['p_high']:.2f} bar")
    print(f"Kondensering:      {T_cold}°C vid {props['p_low']:.2f} bar")
    print(f"Tryckförhållande:  {props['PR']:.2f}:1")
    print(f"Förångningsvärme:  {props['hfg']:.1f} kJ/kg")
    print(f"Viskositet ånga:   {props['mu_vap']:.1f} μPa·s")
    
    # Carnot verkningsgrad
    T_h_K = T_hot + 273.15
    T_c_K = T_cold + 273.15
    eta_carnot = 1 - (T_c_K / T_h_K)
    
    print(f"\n--- VERKNINGSGRADER ---")
    print(f"Carnot (teoretisk max): {eta_carnot*100:.2f}%")
    print(f"Turbin isentropisk:     {eta_turb*100:.1f}%")
    print(f"Generator:              {eta_gen*100:.1f}%")
    print(f"Total förväntad:        {eta_carnot*eta_turb*eta_gen*100:.2f}%")
    
    # Massflöde för måleffekt
    P_target_W = P_target_kW * 1000
    m_dot = P_target_W / (eta_turb * eta_gen * props['hfg'] * 1000)
    
    print(f"\n--- MASSFLÖDE ---")
    print(f"För {P_target_kW} kW eleffekt:")
    print(f"  Massflöde behövt: {m_dot*1000:.1f} g/s ({m_dot:.5f} kg/s)")
    
    # Värmeväxlare
    Q_evap = m_dot * props['hfg']  # kW
    Q_cond = Q_evap + (P_target_W / 1000)  # kW (förångningsvärme + elförluster)
    
    print(f"\n--- VÄRMEVÄXLARE ---")
    print(f"Förångare värmebehov:  {Q_evap:.2f} kW")
    print(f"Kondensor kylbehov:    {Q_cond:.2f} kW")
    
    # Pump
    delta_p = (props['p_high'] - props['p_low']) * 1e5  # Pa
    P_pump = m_dot * delta_p / (props['rho_liq'] * eta_pump)
    
    print(f"\n--- PUMP ---")
    print(f"Tryckskillnad:     {delta_p/1000:.0f} kPa")
    print(f"Pumpeffekt:        {P_pump:.1f} W ({P_pump/P_target_W*100:.2f}% av eleffekt)")
    
    # Diskavstånd (skalning från TesTur)
    mu_ref = 18.2  # μPa·s för luft
    b_ref = 0.234  # mm för TesTur
    b_calc = b_ref * (props['mu_vap'] / mu_ref)**0.5
    
    print(f"\n--- TESLA-TURBIN ---")
    print(f"Optimalt diskavstånd:  {b_calc:.3f} mm")
    print(f"  (skalat från TesTur {b_ref} mm med μ={mu_ref} μPa·s)")
    
    # Köldbärare (sommardrift)
    Q_KB = Q_cond  # kW
    c_p_water = 4.18  # kJ/kg·K
    dT_KB = 5  # K temperaturökning i köldbärare
    m_dot_KB = Q_KB / (c_p_water * dT_KB)  # kg/s
    
    print(f"\n--- KÖLDBÄRARE (sommardrift vid {T_cold}°C) ---")
    print(f"Värmebortförsel:   {Q_KB:.2f} kW")
    print(f"Köldbärare flöde:  {m_dot_KB*1000:.0f} g/s = {m_dot_KB*60:.1f} L/min")
    print(f"  (vid ΔT={dT_KB}K, {T_cold}°C → {T_cold+dT_KB}°C)")
    
    # Nettoeffekt
    P_net = P_target_W - P_pump
    eta_system = P_net / (Q_evap * 1000)
    
    print(f"\n--- SYSTEMSAMMANFATTNING ---")
    print(f"Måleffekt (brutto):    {P_target_kW:.1f} kW")
    print(f"Pumpförlust:           {P_pump/1000:.3f} kW")
    print(f"Nettoeffekt:           {P_net/1000:.2f} kW")
    print(f"Systemverkningsgrad:   {eta_system*100:.2f}%")
    
    print(f"\n{'='*70}\n")
    
    return {
        'm_dot': m_dot,
        'Q_evap': Q_evap,
        'Q_cond': Q_cond,
        'P_pump': P_pump,
        'b_disc': b_calc,
        'eta_system': eta_system
    }

# ============================================================================
# HUVUDBERÄKNINGAR
# ============================================================================

print("\n" + "="*70)
print("ORC MALUNG - DIMENSIONERINGSKALKYLATORN")
print("="*70)

# Scenario 1: R1233zd(E) vid 50°C → 20°C, 1 kW
print("\n### SCENARIO 1: GRUNDDIMENSIONERING ###")
print("Medium: R1233zd(E), Drift: 50°C → 20°C, Mål: 1 kW")
result_1 = calc_system("R1233zd(E)", "R1233zd(E)", 50, 20, 1.0)

# Scenario 2: R1233zd(E) vid 50°C → 20°C, 2 kW
print("\n### SCENARIO 2: HÖGRE EFFEKT ###")
print("Medium: R1233zd(E), Drift: 50°C → 20°C, Mål: 2 kW")
result_2 = calc_system("R1233zd(E)", "R1233zd(E)", 50, 20, 2.0)

# Scenario 3: R1233zd(E) vid 80°C → 10°C, 2 kW (högtemp sommardrift)
print("\n### SCENARIO 3: MAXIMAL PRESTANDA (SOMMARDRIFT) ###")
print("Medium: R1233zd(E), Drift: 80°C → 10°C, Mål: 2 kW")
result_3 = calc_system("R1233zd(E)", "R1233zd(E)", 80, 10, 2.0)

# Scenario 4: R245fa jämförelse
print("\n### SCENARIO 4: R245fa JÄMFÖRELSE ###")
print("Medium: R245fa, Drift: 50°C → 20°C, Mål: 1 kW")
result_4 = calc_system("R245fa", "R245fa", 50, 20, 1.0)

# Sammanfattning
print("\n" + "="*70)
print("JÄMFÖRELSETABELL - ALLA SCENARION")
print("="*70)
print(f"\n{'Scenario':<30} {'m_dot':<12} {'Q_evap':<12} {'Q_cond':<12} {'η_sys':<12}")
print(f"{'':30} {'[g/s]':<12} {'[kW]':<12} {'[kW]':<12} {'[%]':<12}")
print("-"*70)
print(f"{'1: R1233zd(E) 50→20°C 1kW':<30} {result_1['m_dot']*1000:<12.1f} {result_1['Q_evap']:<12.2f} {result_1['Q_cond']:<12.2f} {result_1['eta_system']*100:<12.2f}")
print(f"{'2: R1233zd(E) 50→20°C 2kW':<30} {result_2['m_dot']*1000:<12.1f} {result_2['Q_evap']:<12.2f} {result_2['Q_cond']:<12.2f} {result_2['eta_system']*100:<12.2f}")
print(f"{'3: R1233zd(E) 80→10°C 2kW':<30} {result_3['m_dot']*1000:<12.1f} {result_3['Q_evap']:<12.2f} {result_3['Q_cond']:<12.2f} {result_3['eta_system']*100:<12.2f}")
print(f"{'4: R245fa 50→20°C 1kW':<30} {result_4['m_dot']*1000:<12.1f} {result_4['Q_evap']:<12.2f} {result_4['Q_cond']:<12.2f} {result_4['eta_system']*100:<12.2f}")
print("="*70 + "\n")
