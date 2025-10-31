#!/usr/bin/env python3
"""
FÖRBÄTTRAD ORC KALKYLATOR - Integrerad med TesTur-data
Inkluderar validering mot TesTur-prestanda och projektunderlag
"""

from CoolProp.CoolProp import PropsSI
import sys

# Fixa encoding för Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ============================================================================
# TESTUR REFERENSDATA FÖR VALIDERING
# ============================================================================

TESTUR_REF = {
    'medium': 'Luft vid 20°C',
    'viskositet': 18.2,  # μPa·s
    'diskavstand': 0.234,  # mm
    'diameter': 254,  # mm
    'antal_diskar': 75,
    'effekt_verifierad': 1200,  # W
    'rpm_drift': 10000,
    'tryck_in': 5.5,  # bar (från video K7qZvq1CMFg)
    'tryck_ut': 1.0,  # bar
    'tryckforhallande': 5.5,
}

def print_testur_ref():
    """Skriv ut TesTur referensdata"""
    print("\n" + "="*70)
    print("TESTUR REFERENSDATA (för validering)")
    print("="*70)
    print(f"Medium:              {TESTUR_REF['medium']}")
    print(f"Viskositet:          {TESTUR_REF['viskositet']} μPa·s")
    print(f"Diskavstånd:         {TESTUR_REF['diskavstand']} mm")
    print(f"Diameter:            {TESTUR_REF['diameter']} mm")
    print(f"Antal diskar:        {TESTUR_REF['antal_diskar']}")
    print(f"Verifierad effekt:   {TESTUR_REF['effekt_verifierad']} W")
    print(f"Drifthastighet:      ~{TESTUR_REF['rpm_drift']} RPM")
    print(f"Tryckförhållande:    {TESTUR_REF['tryckforhallande']}:1")
    print(f"\nKälla: Video K7qZvq1CMFg, Charlie Solis kommentarer")
    print("="*70)

# ============================================================================
# TERMODYNAMISKA FUNKTIONER
# ============================================================================

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

def calc_disc_spacing(mu_medium, mu_ref=18.2, b_ref=0.234):
    """
    Beräknar optimalt diskavstånd från viskositet
    Baserat på gränsskiktsteori och TesTur-data
    
    Formel: b₂ / b₁ = √(μ₂ / μ₁)
    """
    scaling_factor = (mu_medium / mu_ref)**0.5
    b_calc = b_ref * scaling_factor
    return b_calc, scaling_factor

# ============================================================================
# HUVUDBERÄKNINGSFUNKTION
# ============================================================================

def calc_system_enhanced(fluid_name, fluid_coolprop, T_hot, T_cold, P_target_kW, 
                        eta_turb=0.55, eta_gen=0.93, eta_pump=0.65,
                        show_testur_comparison=True):
    """
    Beräknar komplett ORC-system med TesTur-validering
    """
    
    print(f"\n{'='*70}")
    print(f"ORC SYSTEMBERÄKNING: {fluid_name}")
    print(f"{'='*70}")
    
    # Termodynamiska egenskaper
    props = get_props(fluid_coolprop, T_hot, T_cold)
    
    print(f"\n--- DRIFTFÖRHÅLLANDEN ---")
    print(f"Förångning:        {T_hot}°C vid {props['p_high']:.2f} bar")
    print(f"Kondensering:      {T_cold}°C vid {props['p_low']:.2f} bar")
    print(f"Tryckförhållande:  {props['PR']:.2f}:1", end="")
    
    # Jämför med TesTur
    if show_testur_comparison:
        pr_ratio = props['PR'] / TESTUR_REF['tryckforhallande']
        if 0.3 < pr_ratio < 0.7:
            print(" (✓ Liknande TesTur, bra för Tesla-turbin)")
        elif pr_ratio >= 0.7:
            print(" (⚠ Högre än TesTur, kan ge högre effekt)")
        else:
            print(" (⚠ Lägre än TesTur, kan begränsa effekt)")
    else:
        print()
    
    print(f"Förångningsvärme:  {props['hfg']:.1f} kJ/kg")
    print(f"Viskositet ånga:   {props['mu_vap']:.1f} μPa·s", end="")
    
    # Jämför viskositet med TesTur
    if show_testur_comparison:
        mu_ratio = props['mu_vap'] / TESTUR_REF['viskositet']
        print(f" ({mu_ratio:.1%} av TesTur luft)")
    else:
        print()
    
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
    Q_cond = Q_evap + (P_target_W / 1000)  # kW
    
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
    b_calc, scaling = calc_disc_spacing(props['mu_vap'])
    
    print(f"\n--- TESLA-TURBIN DIMENSIONERING ---")
    print(f"Viskositetsskalning från TesTur:")
    print(f"  μ_medium / μ_TesTur = {props['mu_vap']:.1f} / {TESTUR_REF['viskositet']} = {scaling:.3f}")
    print(f"  Skalningsfaktor √(μ_ratio) = {scaling**2:.3f}^0.5 = {scaling:.3f}")
    print(f"\nOptimalt diskavstånd:  {b_calc:.3f} mm")
    print(f"  (från TesTur {TESTUR_REF['diskavstand']} mm × {scaling:.3f})")
    print(f"\nToleransintervall:     {b_calc*0.95:.3f} - {b_calc*1.05:.3f} mm (±5%)")
    print(f"Rekommenderad start:   {round(b_calc, 2):.2f} mm")
    
    # TesTur geometri som referens
    if show_testur_comparison:
        print(f"\nÖvrig TesTur-geometri (använd som referens):")
        print(f"  Disktjocklek:      0,254 mm (th/b ≈ {0.254/b_calc:.2f})")
        print(f"  Antal diskar:      {TESTUR_REF['antal_diskar']}")
        print(f"  Diameter:          {TESTUR_REF['diameter']} mm")
        print(f"  Munstycken:        12 st (verifierad konfiguration)")
        print(f"  RPM drift:         ~{TESTUR_REF['rpm_drift']} (vid {TESTUR_REF['effekt_verifierad']}W)")
    
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
        'eta_system': eta_system,
        'mu_vap': props['mu_vap'],
        'PR': props['PR']
    }

# ============================================================================
# HUVUDPROGRAM
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*70)
    print(" "*15 + "ORC MALUNG - FÖRBÄTTRAD KALKYLATOR")
    print(" "*10 + "Integrerad med TesTur-data och projektunderlag")
    print("="*70)
    
    # Visa TesTur referensdata
    print_testur_ref()
    
    # Scenario 1: R1233zd(E) grunddimensionering
    print("\n\n### SCENARIO 1: R1233zd(E) GRUNDDIMENSIONERING ###")
    print("Drift: 50°C → 20°C, Mål: 1 kW")
    print("(Jämförs automatiskt med TesTur-data)")
    result_1 = calc_system_enhanced("R1233zd(E)", "R1233zd(E)", 50, 20, 1.0)
    
    # Scenario 2: R1233zd(E) högre effekt
    print("\n### SCENARIO 2: R1233zd(E) HÖGRE EFFEKT ###")
    print("Drift: 50°C → 20°C, Mål: 2 kW")
    result_2 = calc_system_enhanced("R1233zd(E)", "R1233zd(E)", 50, 20, 2.0, 
                                   show_testur_comparison=False)
    
    # Scenario 3: R1233zd(E) maximal prestanda
    print("\n### SCENARIO 3: R1233zd(E) MAXIMAL PRESTANDA (SOMMARDRIFT) ###")
    print("Drift: 80°C → 10°C, Mål: 2 kW")
    print("(Solfångare 80°C + Köldbärare 10°C)")
    result_3 = calc_system_enhanced("R1233zd(E)", "R1233zd(E)", 80, 10, 2.0,
                                   show_testur_comparison=False)
    
    # Scenario 4: R245fa jämförelse
    print("\n### SCENARIO 4: R245fa JÄMFÖRELSE ###")
    print("Drift: 50°C → 20°C, Mål: 1 kW")
    result_4 = calc_system_enhanced("R245fa", "R245fa", 50, 20, 1.0,
                                   show_testur_comparison=False)
    
    # Sammanfattande jämförelsetabell
    print("\n" + "="*70)
    print("JÄMFÖRELSETABELL - ALLA SCENARION")
    print("="*70)
    print(f"\n{'Scenario':<35} {'m_dot':<10} {'b_disc':<10} {'μ':<10} {'PR':<10}")
    print(f"{'':35} {'[g/s]':<10} {'[mm]':<10} {'[μPa·s]':<10} {'[-]':<10}")
    print("-"*70)
    
    scenarios = [
        ("1: R1233zd(E) 50→20°C 1kW", result_1),
        ("2: R1233zd(E) 50→20°C 2kW", result_2),
        ("3: R1233zd(E) 80→10°C 2kW", result_3),
        ("4: R245fa 50→20°C 1kW", result_4),
    ]
    
    for name, res in scenarios:
        print(f"{name:<35} {res['m_dot']*1000:<10.1f} {res['b_disc']:<10.3f} "
              f"{res['mu_vap']:<10.1f} {res['PR']:<10.2f}")
    
    print("="*70)
    
    # Kritiska slutsatser
    print("\n" + "="*70)
    print("KRITISKA SLUTSATSER")
    print("="*70)
    print("\n1. DISKAVSTÅND:")
    print(f"   R1233zd(E):  {result_1['b_disc']:.3f} mm (31% lägre μ än TesTur)")
    print(f"   R245fa:      {result_4['b_disc']:.3f} mm (praktiskt identisk)")
    print(f"   TesTur ref:  {TESTUR_REF['diskavstand']:.3f} mm")
    print(f"\n   → Båda medier behöver MINDRE gap än TesTur (korrekt!)")
    
    print("\n2. TRYCKFÖRHÅLLANDE:")
    print(f"   R1233zd(E):  {result_1['PR']:.2f}:1 (49% av TesTur)")
    print(f"   R245fa:      {result_4['PR']:.2f}:1 (51% av TesTur)")
    print(f"   TesTur ref:  {TESTUR_REF['tryckforhallande']:.2f}:1")
    print(f"\n   → Lägre PR kompenseras av högre densitet och hfg")
    
    print("\n3. VISKOSITET:")
    print(f"   R1233zd(E):  {result_1['mu_vap']:.1f} μPa·s ({result_1['mu_vap']/TESTUR_REF['viskositet']:.1%} av TesTur)")
    print(f"   R245fa:      {result_4['mu_vap']:.1f} μPa·s ({result_4['mu_vap']/TESTUR_REF['viskositet']:.1%} av TesTur)")
    print(f"   TesTur luft: {TESTUR_REF['viskositet']:.1f} μPa·s")
    print(f"\n   → Lägre μ motiverar mindre diskavstånd enligt b ∝ √μ")
    
    print("\n4. PRAKTISK REKOMMENDATION:")
    print(f"   → Använd 0,19 mm som startpunkt för R1233zd(E)")
    print(f"   → Tolerans ±0,01 mm (0,18-0,20 mm intervall)")
    print(f"   → Samma turbin-design fungerar för båda medier")
    print(f"   → TesTur-geometri (75 diskar, 254mm, 12 munstycken) som bas")
    
    print("\n" + "="*70)
    print("NÄSTA STEG:")
    print("="*70)
    print("1. Detaljdesign turbin med b=0,19mm, th=0,25mm, N=75, D=254mm")
    print("2. CAD-modell och FEM-analys (stress vid 10,000 RPM)")
    print("3. Laserskärning diskar (316L, tol ±0,01mm)")
    print("4. Dynamisk balansering (kritiskt!)")
    print("5. Testbänk med tryckluft först (som TesTur)")
    print("6. ORC-test med R1233zd(E) gradvis ökande effekt")
    print("="*70 + "\n")
    
    print("KÄLLOR:")
    print("- TesTur Video K7qZvq1CMFg (lufttest 1200W)")
    print("- Charlie Solis kommentarer (ORC-erfarenhet)")
    print("- Viskositet_och_Diskavstand_KORRIGERAD.md")
    print("- CoolProp 7.1.0 termodynamisk databas")
    print("="*70 + "\n")
