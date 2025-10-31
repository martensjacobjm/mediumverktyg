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
