#!/usr/bin/env python3
"""
Thermodynamic Calculations for ORC Systems
Ported and generalized from orc_kalkylator_enhanced.py
"""

from dataclasses import dataclass
from typing import Dict, Optional
from core.fluid_database import FluidDatabase


@dataclass
class ORCSystemResults:
    """Results from ORC system calculation"""
    # Input parameters
    fluid: str
    T_hot: float  # °C
    T_cold: float  # °C
    P_target_kW: float  # kW

    # Thermodynamic properties
    p_high: float  # bar
    p_low: float  # bar
    pressure_ratio: float
    hfg: float  # kJ/kg
    mu_vapor: float  # μPa·s
    rho_vapor: float  # kg/m³
    rho_liquid: float  # kg/m³

    # Carnot efficiency
    eta_carnot: float

    # Mass flow
    m_dot: float  # kg/s
    m_dot_g_s: float  # g/s

    # Heat exchangers
    Q_evap: float  # kW
    Q_cond: float  # kW

    # Pump
    P_pump: float  # W
    pump_fraction: float  # Pump power as fraction of target

    # Tesla turbine (calculated separately)
    b_disc: Optional[float] = None  # mm

    # System performance
    P_net: float = 0.0  # kW
    eta_system: float = 0.0  # System efficiency


class ThermodynamicCalculator:
    """
    Main calculator for ORC thermodynamic cycles
    """

    def __init__(self):
        self.db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')

    def calculate_orc_system(self,
                            fluid: str,
                            T_hot: float,
                            T_cold: float,
                            P_target_kW: float,
                            eta_turb: float = 0.55,
                            eta_gen: float = 0.93,
                            eta_pump: float = 0.65) -> Optional[ORCSystemResults]:
        """
        Calculate complete ORC system for given fluid and conditions

        Args:
            fluid: Fluid name (CoolProp compatible)
            T_hot: Hot side temperature (evaporation) [°C]
            T_cold: Cold side temperature (condensation) [°C]
            P_target_kW: Target electrical power output [kW]
            eta_turb: Turbine isentropic efficiency (default 0.55 for Tesla turbine)
            eta_gen: Generator efficiency (default 0.93)
            eta_pump: Pump efficiency (default 0.65)

        Returns:
            ORCSystemResults object or None if calculation fails
        """

        # Get thermodynamic properties at hot and cold sides
        props_hot = self.db.get_saturation_properties(fluid, T_hot)
        props_cold = self.db.get_saturation_properties(fluid, T_cold)

        if not props_hot or not props_cold:
            print(f"Error: Could not get properties for {fluid}")
            return None

        # Pressure ratio
        pressure_ratio = props_hot.pressure / props_cold.pressure

        # Latent heat (should be similar at both temperatures, use hot side)
        hfg = props_hot.hfg

        # Carnot efficiency
        T_h_K = T_hot + 273.15
        T_c_K = T_cold + 273.15
        eta_carnot = 1 - (T_c_K / T_h_K)

        # Mass flow rate required for target power
        # P_target = m_dot * eta_turb * eta_gen * hfg
        # m_dot = P_target / (eta_turb * eta_gen * hfg)
        P_target_W = P_target_kW * 1000
        m_dot = P_target_W / (eta_turb * eta_gen * hfg * 1000)  # kg/s
        m_dot_g_s = m_dot * 1000  # g/s

        # Heat exchanger duties
        Q_evap = m_dot * hfg  # kW
        Q_cond = Q_evap + (P_target_W / 1000)  # kW (evap + electrical losses)

        # Pump power
        delta_p = (props_hot.pressure - props_cold.pressure) * 1e5  # bar → Pa
        P_pump = m_dot * delta_p / (props_cold.rho_liquid * eta_pump)  # W
        pump_fraction = P_pump / P_target_W

        # Net power and system efficiency
        P_net = (P_target_W - P_pump) / 1000  # kW
        eta_system = P_net / Q_evap  # Both in kW, so no conversion needed

        return ORCSystemResults(
            fluid=fluid,
            T_hot=T_hot,
            T_cold=T_cold,
            P_target_kW=P_target_kW,
            p_high=props_hot.pressure,
            p_low=props_cold.pressure,
            pressure_ratio=pressure_ratio,
            hfg=hfg,
            mu_vapor=props_hot.mu_vapor,
            rho_vapor=props_hot.rho_vapor,
            rho_liquid=props_cold.rho_liquid,
            eta_carnot=eta_carnot,
            m_dot=m_dot,
            m_dot_g_s=m_dot_g_s,
            Q_evap=Q_evap,
            Q_cond=Q_cond,
            P_pump=P_pump,
            pump_fraction=pump_fraction,
            P_net=P_net,
            eta_system=eta_system
        )

    def compare_fluids(self,
                      fluids: list,
                      T_hot: float,
                      T_cold: float,
                      P_target_kW: float) -> Dict[str, ORCSystemResults]:
        """
        Compare multiple fluids under same conditions

        Args:
            fluids: List of fluid names
            T_hot: Hot side temperature [°C]
            T_cold: Cold side temperature [°C]
            P_target_kW: Target power [kW]

        Returns:
            Dictionary mapping fluid name to results
        """
        results = {}

        for fluid in fluids:
            result = self.calculate_orc_system(fluid, T_hot, T_cold, P_target_kW)
            if result:
                results[fluid] = result

        return results

    def print_results(self, result: ORCSystemResults, detailed: bool = True):
        """Pretty print ORC system results"""

        print(f"\n{'='*70}")
        print(f"ORC SYSTEM: {result.fluid}")
        print(f"{'='*70}")

        print(f"\n--- OPERATING CONDITIONS ---")
        print(f"Evaporation:        {result.T_hot}°C at {result.p_high:.2f} bar")
        print(f"Condensation:       {result.T_cold}°C at {result.p_low:.2f} bar")
        print(f"Pressure ratio:     {result.pressure_ratio:.2f}:1")
        print(f"Latent heat:        {result.hfg:.1f} kJ/kg")
        print(f"Vapor viscosity:    {result.mu_vapor:.1f} μPa·s")

        print(f"\n--- EFFICIENCIES ---")
        print(f"Carnot (max):       {result.eta_carnot*100:.2f}%")
        print(f"System (actual):    {result.eta_system*100:.2f}%")
        print(f"Efficiency ratio:   {result.eta_system/result.eta_carnot*100:.1f}% of Carnot")

        print(f"\n--- MASS FLOW ---")
        print(f"For {result.P_target_kW} kW output:")
        print(f"  Mass flow:        {result.m_dot_g_s:.1f} g/s ({result.m_dot:.5f} kg/s)")

        print(f"\n--- HEAT EXCHANGERS ---")
        print(f"Evaporator duty:    {result.Q_evap:.2f} kW")
        print(f"Condenser duty:     {result.Q_cond:.2f} kW")

        print(f"\n--- PUMP ---")
        print(f"Pressure rise:      {(result.p_high - result.p_low):.2f} bar")
        print(f"Pump power:         {result.P_pump:.1f} W ({result.pump_fraction*100:.2f}% of target)")

        if result.b_disc:
            print(f"\n--- TESLA TURBINE ---")
            print(f"Disc spacing:       {result.b_disc:.3f} mm")
            print(f"Tolerance:          {result.b_disc*0.95:.3f} - {result.b_disc*1.05:.3f} mm (±5%)")

        print(f"\n--- SYSTEM SUMMARY ---")
        print(f"Target power:       {result.P_target_kW:.1f} kW")
        print(f"Pump loss:          {result.P_pump/1000:.3f} kW")
        print(f"Net power:          {result.P_net:.2f} kW")
        print(f"System efficiency:  {result.eta_system*100:.2f}%")

        print(f"\n{'='*70}\n")


# Example usage and validation
if __name__ == "__main__":
    print("="*70)
    print("THERMODYNAMIC CALCULATOR - Testing")
    print("="*70)

    calc = ThermodynamicCalculator()

    # Test with R1233zd(E) - should match legacy calculator
    print("\n### Test 1: R1233zd(E) at 50°C → 20°C, 1 kW ###")
    result = calc.calculate_orc_system('R1233zd(E)', 50, 20, 1.0)
    if result:
        calc.print_results(result)

        # Validate against legacy values
        print("\nValidation against legacy orc_kalkylator_enhanced.py:")
        print(f"  Pressure @ 50°C: {result.p_high:.2f} bar (expected ~2.93 bar)")
        print(f"  Viscosity:       {result.mu_vapor:.1f} μPa·s (expected ~12.1 μPa·s)")
        print(f"  System η:        {result.eta_system*100:.2f}% (expected ~4.85%)")

    # Test with R245fa for comparison
    print("\n### Test 2: R245fa at 50°C → 20°C, 1 kW ###")
    result_r245 = calc.calculate_orc_system('R245fa', 50, 20, 1.0)
    if result_r245:
        calc.print_results(result_r245, detailed=False)

    # Compare multiple fluids
    print("\n### Test 3: Compare top 5 ORC fluids ###")
    fluids_to_compare = ['R1233zd(E)', 'R245fa', 'R1234ze(E)', 'Isopentane', 'n-Pentane']
    comparison = calc.compare_fluids(fluids_to_compare, 50, 20, 1.0)

    print(f"\n{'='*90}")
    print(f"{'Fluid':<15} {'P_high':<10} {'hfg':<12} {'μ_vapor':<12} {'η_sys':<10} {'m_dot':<10}")
    print(f"{'':15} {'[bar]':<10} {'[kJ/kg]':<12} {'[μPa·s]':<12} {'[%]':<10} {'[g/s]':<10}")
    print(f"{'='*90}")

    for fluid, res in comparison.items():
        print(f"{fluid:<15} {res.p_high:<10.2f} {res.hfg:<12.1f} {res.mu_vapor:<12.1f} "
              f"{res.eta_system*100:<10.2f} {res.m_dot_g_s:<10.1f}")

    print(f"{'='*90}\n")
