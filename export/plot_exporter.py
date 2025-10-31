#!/usr/bin/env python3
"""
Plot Exporter - Export matplotlib plots to PNG/SVG
High-quality exports for reports and presentations
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving
import matplotlib.pyplot as plt
import numpy as np
from typing import List


class PlotExporter:
    """Export thermodynamic plots to image files"""

    def __init__(self):
        self.dpi = 300  # High quality for printing

    def export_pressure_temp(self, fluids: List[str], db, filename: str):
        """Export pressure-temperature plot"""

        fig, ax = plt.subplots(figsize=(10, 6))
        temps = np.linspace(0, 100, 101)

        for fluid in fluids:
            pressures = []
            for T in temps:
                props = db.get_saturation_properties(fluid, T)
                if props:
                    pressures.append(props.pressure)
                else:
                    pressures.append(np.nan)

            ax.plot(temps, pressures, label=fluid, linewidth=2.5, marker='o', markevery=10)

        # Optimal zones
        ax.axhspan(2, 8, alpha=0.1, color='green', label='Optimal pressure (2-8 bar)')

        ax.set_xlabel('Temperature [°C]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Saturation Pressure [bar]', fontsize=12, fontweight='bold')
        ax.set_title('Pressure-Temperature Comparison', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)

        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported pressure-temperature plot to {filename}")
        return filename

    def export_latent_heat(self, fluids: List[str], db, filename: str):
        """Export latent heat plot"""

        fig, ax = plt.subplots(figsize=(10, 6))
        temps = np.linspace(10, 80, 36)

        for fluid in fluids:
            hfg_values = []
            for T in temps:
                props = db.get_saturation_properties(fluid, T)
                if props:
                    hfg_values.append(props.hfg)
                else:
                    hfg_values.append(np.nan)

            ax.plot(temps, hfg_values, label=fluid, linewidth=2.5, marker='s', markevery=4)

        ax.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Design temp (50°C)')

        ax.set_xlabel('Temperature [°C]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latent Heat hfg [kJ/kg]', fontsize=12, fontweight='bold')
        ax.set_title('Latent Heat Comparison', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported latent heat plot to {filename}")
        return filename

    def export_four_panel(self, fluids: List[str], db, filename: str):
        """Export 4-panel comparison plot"""

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        temps = np.linspace(10, 80, 36)

        for fluid in fluids:
            p_vals, hfg_vals, mu_vals, rho_vals = [], [], [], []

            for T in temps:
                props = db.get_saturation_properties(fluid, T)
                if props:
                    p_vals.append(props.pressure)
                    hfg_vals.append(props.hfg)
                    mu_vals.append(props.mu_vapor)
                    rho_vals.append(props.rho_vapor)
                else:
                    p_vals.append(np.nan)
                    hfg_vals.append(np.nan)
                    mu_vals.append(np.nan)
                    rho_vals.append(np.nan)

            # Plot all panels
            axes[0, 0].plot(temps, p_vals, label=fluid, linewidth=2.5)
            axes[0, 1].plot(temps, hfg_vals, label=fluid, linewidth=2.5)
            axes[1, 0].plot(temps, mu_vals, label=fluid, linewidth=2.5)
            axes[1, 1].plot(temps, rho_vals, label=fluid, linewidth=2.5)

        # Configure panels
        axes[0, 0].set_title('(a) Saturation Pressure', fontweight='bold', fontsize=12)
        axes[0, 0].set_ylabel('Pressure [bar]', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()

        axes[0, 1].set_title('(b) Latent Heat', fontweight='bold', fontsize=12)
        axes[0, 1].set_ylabel('hfg [kJ/kg]', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()

        axes[1, 0].set_title('(c) Vapor Viscosity', fontweight='bold', fontsize=12)
        axes[1, 0].set_xlabel('Temperature [°C]', fontweight='bold')
        axes[1, 0].set_ylabel('μ [μPa·s]', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()

        axes[1, 1].set_title('(d) Vapor Density', fontweight='bold', fontsize=12)
        axes[1, 1].set_xlabel('Temperature [°C]', fontweight='bold')
        axes[1, 1].set_ylabel('ρ [kg/m³]', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()

        fig.suptitle('Thermodynamic Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported 4-panel comparison to {filename}")
        return filename

    def export_ts_diagram(self, fluids: List[str], db, filename: str):
        """Export T-s diagram (Temperature-Entropy)"""
        from CoolProp.CoolProp import PropsSI

        fig, ax = plt.subplots(figsize=(10, 6))

        for fluid in fluids:
            try:
                # Get critical point
                T_crit = PropsSI('TCRIT', fluid) - 273.15
                p_crit = PropsSI('PCRIT', fluid) / 1e5

                # Temperature range
                T_min = PropsSI('TTRIPLE', fluid) - 273.15
                T_range = np.linspace(max(T_min, -50), T_crit - 0.5, 100)

                # Calculate saturation dome
                s_liquid, s_vapor, temps_valid = [], [], []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        s_l = PropsSI('S', 'T', T_k, 'Q', 0, fluid) / 1000
                        s_v = PropsSI('S', 'T', T_k, 'Q', 1, fluid) / 1000
                        s_liquid.append(s_l)
                        s_vapor.append(s_v)
                        temps_valid.append(T_c)
                    except:
                        continue

                if len(temps_valid) > 10:
                    ax.plot(s_liquid, temps_valid, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(s_vapor, temps_valid, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Critical point
                    s_crit = PropsSI('S', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000
                    ax.plot(s_crit, T_crit, 'o', markersize=10,
                           label=f'{fluid} critical point', markeredgewidth=2)

            except Exception as e:
                print(f"Warning: Could not plot {fluid} in T-s diagram: {e}")
                continue

        ax.set_xlabel('Entropy s [kJ/(kg·K)]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperature [°C]', fontsize=12, fontweight='bold')
        ax.set_title('T-s Diagram (Temperature-Entropy)', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported T-s diagram to {filename}")
        return filename

    def export_ph_diagram(self, fluids: List[str], db, filename: str):
        """Export P-h diagram (Pressure-Enthalpy)"""
        from CoolProp.CoolProp import PropsSI

        fig, ax = plt.subplots(figsize=(10, 6))

        for fluid in fluids:
            try:
                # Get critical point
                T_crit = PropsSI('TCRIT', fluid) - 273.15
                p_crit = PropsSI('PCRIT', fluid) / 1e5
                h_crit = PropsSI('H', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000

                # Temperature range
                T_min = PropsSI('TTRIPLE', fluid) - 273.15
                T_range = np.linspace(max(T_min, -50), T_crit - 0.5, 100)

                # Calculate saturation dome
                h_liquid, h_vapor, p_sat = [], [], []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        p = PropsSI('P', 'T', T_k, 'Q', 0, fluid) / 1e5
                        h_l = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000
                        h_v = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000
                        h_liquid.append(h_l)
                        h_vapor.append(h_v)
                        p_sat.append(p)
                    except:
                        continue

                if len(p_sat) > 10:
                    ax.plot(h_liquid, p_sat, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(h_vapor, p_sat, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Critical point
                    ax.plot(h_crit, p_crit, 'o', markersize=10,
                           label=f'{fluid} critical point', markeredgewidth=2)

                    # Add isotherms
                    for T_iso in [20, 50, 80]:
                        if T_min < T_iso < T_crit - 5:
                            try:
                                T_k = T_iso + 273.15
                                p_iso = PropsSI('P', 'T', T_k, 'Q', 0, fluid) / 1e5
                                h_l_iso = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000
                                h_v_iso = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000
                                ax.plot([h_l_iso, h_v_iso], [p_iso, p_iso],
                                       'k:', alpha=0.4, linewidth=1)
                                ax.text((h_l_iso + h_v_iso)/2, p_iso, f'{T_iso}°C',
                                       fontsize=8, ha='center', va='bottom', alpha=0.6)
                            except:
                                pass

            except Exception as e:
                print(f"Warning: Could not plot {fluid} in P-h diagram: {e}")
                continue

        ax.set_xlabel('Enthalpy h [kJ/kg]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
        ax.set_title('P-h Diagram (Pressure-Enthalpy)', fontsize=14, fontweight='bold')
        ax.set_yscale('log')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, which='both')

        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported P-h diagram to {filename}")
        return filename

    def export_mollier_diagram(self, fluids: List[str], db, filename: str):
        """Export Mollier diagram (h-s, Enthalpy-Entropy)"""
        from CoolProp.CoolProp import PropsSI

        fig, ax = plt.subplots(figsize=(10, 6))

        for fluid in fluids:
            try:
                # Get critical point
                T_crit = PropsSI('TCRIT', fluid) - 273.15
                p_crit = PropsSI('PCRIT', fluid) / 1e5
                h_crit = PropsSI('H', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000
                s_crit = PropsSI('S', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000

                # Temperature range
                T_min = PropsSI('TTRIPLE', fluid) - 273.15
                T_range = np.linspace(max(T_min, -50), T_crit - 0.5, 100)

                # Calculate saturation dome
                h_liquid, h_vapor, s_liquid, s_vapor = [], [], [], []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        h_l = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000
                        s_l = PropsSI('S', 'T', T_k, 'Q', 0, fluid) / 1000
                        h_v = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000
                        s_v = PropsSI('S', 'T', T_k, 'Q', 1, fluid) / 1000
                        h_liquid.append(h_l)
                        s_liquid.append(s_l)
                        h_vapor.append(h_v)
                        s_vapor.append(s_v)
                    except:
                        continue

                if len(s_liquid) > 10:
                    ax.plot(s_liquid, h_liquid, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(s_vapor, h_vapor, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Critical point
                    ax.plot(s_crit, h_crit, 'o', markersize=10,
                           label=f'{fluid} critical point', markeredgewidth=2)

                    # Add isobars
                    for p_iso_bar in [2, 5, 10]:
                        if p_iso_bar < p_crit:
                            try:
                                T_sat = PropsSI('T', 'P', p_iso_bar * 1e5, 'Q', 0, fluid) - 273.15
                                if T_min < T_sat < T_crit - 5:
                                    h_l_iso = PropsSI('H', 'P', p_iso_bar * 1e5, 'Q', 0, fluid) / 1000
                                    s_l_iso = PropsSI('S', 'P', p_iso_bar * 1e5, 'Q', 0, fluid) / 1000
                                    h_v_iso = PropsSI('H', 'P', p_iso_bar * 1e5, 'Q', 1, fluid) / 1000
                                    s_v_iso = PropsSI('S', 'P', p_iso_bar * 1e5, 'Q', 1, fluid) / 1000
                                    ax.plot([s_l_iso, s_v_iso], [h_l_iso, h_v_iso],
                                           'k:', alpha=0.4, linewidth=1)
                                    ax.text(s_v_iso, h_v_iso, f'{p_iso_bar}bar',
                                           fontsize=8, ha='left', va='bottom', alpha=0.6)
                            except:
                                pass

            except Exception as e:
                print(f"Warning: Could not plot {fluid} in Mollier diagram: {e}")
                continue

        ax.set_xlabel('Entropy s [kJ/(kg·K)]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Enthalpy h [kJ/kg]', fontsize=12, fontweight='bold')
        ax.set_title('Mollier Diagram (Enthalpy-Entropy)', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        print(f"✓ Exported Mollier diagram to {filename}")
        return filename

    def export_all_plots(self, fluids: List[str], db, base_filename: str):
        """
        Export all plot types

        Args:
            fluids: List of fluid names
            db: FluidDatabase instance
            base_filename: Base filename (will append plot type)

        Returns:
            Dictionary with filenames for each plot type
        """

        exports = {}

        # Pressure-temperature
        exports['pressure_temp'] = self.export_pressure_temp(
            fluids, db, f"{base_filename}_pressure_temp.png"
        )

        # Latent heat
        exports['latent_heat'] = self.export_latent_heat(
            fluids, db, f"{base_filename}_latent_heat.png"
        )

        # 4-panel
        exports['four_panel'] = self.export_four_panel(
            fluids, db, f"{base_filename}_four_panel.png"
        )

        # T-s diagram (Temperature-Entropy)
        exports['ts_diagram'] = self.export_ts_diagram(
            fluids, db, f"{base_filename}_ts_diagram.png"
        )

        # P-h diagram (Pressure-Enthalpy)
        exports['ph_diagram'] = self.export_ph_diagram(
            fluids, db, f"{base_filename}_ph_diagram.png"
        )

        # Mollier diagram (h-s)
        exports['mollier_diagram'] = self.export_mollier_diagram(
            fluids, db, f"{base_filename}_mollier_diagram.png"
        )

        print(f"\n✓ Exported {len(exports)} plots")
        return exports


# Test
if __name__ == "__main__":
    from core.fluid_database import FluidDatabase

    print("="*70)
    print("PLOT EXPORTER - Testing")
    print("="*70)

    db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')
    exporter = PlotExporter()

    test_fluids = ['R1233zd(E)', 'R245fa', 'Isopentane']

    print(f"\nExporting plots for: {', '.join(test_fluids)}")

    exports = exporter.export_all_plots(test_fluids, db, 'test_comparison')

    print("\n✓ Test completed. Check generated PNG files:")
    for plot_type, filename in exports.items():
        print(f"  - {filename}")
