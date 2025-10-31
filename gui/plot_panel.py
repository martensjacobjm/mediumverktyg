#!/usr/bin/env python3
"""
Plot Panel - Dynamic matplotlib plots
Displays thermodynamic comparison plots for selected fluids
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


class PlotPanel(ttk.Frame):
    """Plot panel with embedded matplotlib"""

    def __init__(self, parent):
        super().__init__(parent)

        self.db = None  # Will be set when plotting
        self.current_fluids = []

        self._create_widgets()

    def _create_widgets(self):
        """Create plot controls and canvas"""

        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(
            control_frame,
            text="DIAGRAM",
            font=('Arial', 12, 'bold')
        ).pack(side=tk.LEFT)

        # Plot type selector
        ttk.Label(control_frame, text="Typ:").pack(side=tk.LEFT, padx=(20, 5))

        self.plot_type = ttk.Combobox(
            control_frame,
            values=[
                'Tryck-Temperatur',
                'Förångningsvärme',
                'Viskositet',
                'Densitet (ånga)',
                'Jämförelse 4-panel',
                'T-s diagram',
                'P-h diagram',
                'Mollier diagram (h-s)'
            ],
            state='readonly',
            width=22
        )
        self.plot_type.set('Tryck-Temperatur')
        self.plot_type.pack(side=tk.LEFT, padx=5)
        self.plot_type.bind('<<ComboboxSelected>>', self._on_plot_type_change)

        # Refresh button
        ttk.Button(
            control_frame,
            text="Uppdatera",
            command=self._refresh_plot
        ).pack(side=tk.LEFT, padx=5)

        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        # Initial empty plot
        self._plot_empty()

    def plot_comparison(self, fluids, db):
        """Plot comparison for selected fluids"""
        self.current_fluids = fluids
        self.db = db

        if not fluids or not db:
            self._plot_empty()
            return

        plot_type = self.plot_type.get()

        if plot_type == 'Tryck-Temperatur':
            self._plot_pressure_temp()
        elif plot_type == 'Förångningsvärme':
            self._plot_latent_heat()
        elif plot_type == 'Viskositet':
            self._plot_viscosity()
        elif plot_type == 'Densitet (ånga)':
            self._plot_density()
        elif plot_type == 'Jämförelse 4-panel':
            self._plot_four_panel()
        elif plot_type == 'T-s diagram':
            self._plot_ts_diagram()
        elif plot_type == 'P-h diagram':
            self._plot_ph_diagram()
        elif plot_type == 'Mollier diagram (h-s)':
            self._plot_mollier_diagram()

        self.canvas.draw()

    def _plot_empty(self):
        """Plot empty placeholder"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5,
            'Välj medier från listan ovan för jämförelse\n\n'
            '(Ctrl+klick för multival)',
            ha='center', va='center',
            fontsize=14, color='gray'
        )
        ax.axis('off')
        self.canvas.draw()

    def _plot_pressure_temp(self):
        """Plot pressure vs temperature"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        temps = np.linspace(0, 100, 101)

        for fluid in self.current_fluids:
            pressures = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    pressures.append(props.pressure)
                else:
                    pressures.append(np.nan)

            ax.plot(temps, pressures, label=fluid, linewidth=2, marker='o', markevery=10)

        # Optimal zones
        ax.axhspan(2, 8, alpha=0.1, color='green', label='Optimal tryck (2-8 bar)')
        ax.axvspan(10, 30, alpha=0.05, color='blue')
        ax.axvspan(40, 80, alpha=0.05, color='red')

        ax.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Mättningstryck [bar]', fontsize=11, fontweight='bold')
        ax.set_title('Tryck-Temperatur Jämförelse', fontsize=13, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)

        self.figure.tight_layout()

    def _plot_latent_heat(self):
        """Plot latent heat vs temperature"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            hfg_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    hfg_values.append(props.hfg)
                else:
                    hfg_values.append(np.nan)

            ax.plot(temps, hfg_values, label=fluid, linewidth=2, marker='s', markevery=4)

        ax.axvline(50, color='gray', linestyle='--', alpha=0.5, label='Design temp (50°C)')

        ax.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Förångningsvärme hfg [kJ/kg]', fontsize=11, fontweight='bold')
        ax.set_title('Förångningsvärme Jämförelse', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()

    def _plot_viscosity(self):
        """Plot vapor viscosity vs temperature"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            mu_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    mu_values.append(props.mu_vapor)
                else:
                    mu_values.append(np.nan)

            ax.plot(temps, mu_values, label=fluid, linewidth=2, marker='o', markevery=4)

        # TesTur reference
        ax.axhline(18.2, color='purple', linestyle=':', alpha=0.5, linewidth=2,
                  label='TesTur ref (luft, 18.2 μPa·s)')

        ax.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Viskositet ånga [μPa·s]', fontsize=11, fontweight='bold')
        ax.set_title('Viskositet Jämförelse (påverkar diskavstånd)', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()

    def _plot_density(self):
        """Plot vapor density vs temperature"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            rho_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    rho_values.append(props.rho_vapor)
                else:
                    rho_values.append(np.nan)

            ax.plot(temps, rho_values, label=fluid, linewidth=2, marker='d', markevery=4)

        ax.set_xlabel('Temperatur [°C]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Ångdensitet [kg/m³]', fontsize=11, fontweight='bold')
        ax.set_title('Densitet Jämförelse', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()

    def _plot_four_panel(self):
        """Plot 4-panel comparison"""
        self.figure.clear()

        temps = np.linspace(10, 80, 36)

        # Create 2x2 subplots
        axes = self.figure.subplots(2, 2)

        for fluid in self.current_fluids:
            p_vals, hfg_vals, mu_vals, rho_vals = [], [], [], []

            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
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

            # Plot 1: Pressure
            axes[0, 0].plot(temps, p_vals, label=fluid, linewidth=2)
            # Plot 2: Latent heat
            axes[0, 1].plot(temps, hfg_vals, label=fluid, linewidth=2)
            # Plot 3: Viscosity
            axes[1, 0].plot(temps, mu_vals, label=fluid, linewidth=2)
            # Plot 4: Density
            axes[1, 1].plot(temps, rho_vals, label=fluid, linewidth=2)

        # Configure subplots
        axes[0, 0].set_title('(a) Mättningstryck', fontweight='bold')
        axes[0, 0].set_ylabel('Tryck [bar]')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend(fontsize=8)

        axes[0, 1].set_title('(b) Förångningsvärme', fontweight='bold')
        axes[0, 1].set_ylabel('hfg [kJ/kg]')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend(fontsize=8)

        axes[1, 0].set_title('(c) Viskositet', fontweight='bold')
        axes[1, 0].set_xlabel('Temperatur [°C]')
        axes[1, 0].set_ylabel('μ [μPa·s]')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend(fontsize=8)

        axes[1, 1].set_title('(d) Ångdensitet', fontweight='bold')
        axes[1, 1].set_xlabel('Temperatur [°C]')
        axes[1, 1].set_ylabel('ρ [kg/m³]')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend(fontsize=8)

        self.figure.suptitle('Termodynamisk Jämförelse', fontsize=14, fontweight='bold')
        self.figure.tight_layout()

    def _plot_ts_diagram(self):
        """Plot T-s diagram (Temperature-Entropy)"""
        from CoolProp.CoolProp import PropsSI

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for fluid in self.current_fluids:
            try:
                # Get critical point
                T_crit = PropsSI('TCRIT', fluid) - 273.15  # Convert to Celsius
                p_crit = PropsSI('PCRIT', fluid) / 1e5     # Convert to bar

                # Temperature range from triple point to critical point
                T_min = PropsSI('TTRIPLE', fluid) - 273.15
                T_range = np.linspace(max(T_min, -50), T_crit - 0.5, 100)

                # Calculate saturation dome
                s_liquid = []
                s_vapor = []
                temps_valid = []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        # Liquid saturation entropy
                        s_l = PropsSI('S', 'T', T_k, 'Q', 0, fluid) / 1000  # kJ/(kg·K)
                        # Vapor saturation entropy
                        s_v = PropsSI('S', 'T', T_k, 'Q', 1, fluid) / 1000  # kJ/(kg·K)

                        s_liquid.append(s_l)
                        s_vapor.append(s_v)
                        temps_valid.append(T_c)
                    except:
                        continue

                if len(temps_valid) > 10:
                    # Plot saturation dome
                    ax.plot(s_liquid, temps_valid, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(s_vapor, temps_valid, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Mark critical point
                    s_crit = PropsSI('S', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000
                    ax.plot(s_crit, T_crit, 'o', markersize=10,
                           label=f'{fluid} kritisk punkt', markeredgewidth=2)

            except Exception as e:
                print(f"Could not plot T-s diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('Entropi s [kJ/(kg·K)]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Temperatur [°C]', fontsize=11, fontweight='bold')
        ax.set_title('T-s Diagram (Temperatur-Entropi)', fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()

    def _plot_ph_diagram(self):
        """Plot P-h diagram (Pressure-Enthalpy)"""
        from CoolProp.CoolProp import PropsSI

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for fluid in self.current_fluids:
            try:
                # Get critical point
                T_crit = PropsSI('TCRIT', fluid) - 273.15
                p_crit = PropsSI('PCRIT', fluid) / 1e5
                h_crit = PropsSI('H', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000

                # Temperature range
                T_min = PropsSI('TTRIPLE', fluid) - 273.15
                T_range = np.linspace(max(T_min, -50), T_crit - 0.5, 100)

                # Calculate saturation dome
                h_liquid = []
                h_vapor = []
                p_sat = []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        # Get saturation pressure
                        p = PropsSI('P', 'T', T_k, 'Q', 0, fluid) / 1e5  # bar
                        # Liquid saturation enthalpy
                        h_l = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000  # kJ/kg
                        # Vapor saturation enthalpy
                        h_v = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000  # kJ/kg

                        h_liquid.append(h_l)
                        h_vapor.append(h_v)
                        p_sat.append(p)
                    except:
                        continue

                if len(p_sat) > 10:
                    # Plot saturation dome
                    ax.plot(h_liquid, p_sat, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(h_vapor, p_sat, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Mark critical point
                    ax.plot(h_crit, p_crit, 'o', markersize=10,
                           label=f'{fluid} kritisk punkt', markeredgewidth=2)

                    # Add isotherms (constant temperature lines) in two-phase region
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
                print(f"Could not plot P-h diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('Entalpi h [kJ/kg]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Tryck [bar]', fontsize=11, fontweight='bold')
        ax.set_title('P-h Diagram (Tryck-Entalpi)', fontsize=13, fontweight='bold')
        ax.set_yscale('log')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3, which='both')

        self.figure.tight_layout()

    def _plot_mollier_diagram(self):
        """Plot Mollier diagram (h-s, Enthalpy-Entropy)"""
        from CoolProp.CoolProp import PropsSI

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for fluid in self.current_fluids:
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
                h_liquid = []
                h_vapor = []
                s_liquid = []
                s_vapor = []

                for T_c in T_range:
                    try:
                        T_k = T_c + 273.15
                        # Liquid saturation properties
                        h_l = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000  # kJ/kg
                        s_l = PropsSI('S', 'T', T_k, 'Q', 0, fluid) / 1000  # kJ/(kg·K)
                        # Vapor saturation properties
                        h_v = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000  # kJ/kg
                        s_v = PropsSI('S', 'T', T_k, 'Q', 1, fluid) / 1000  # kJ/(kg·K)

                        h_liquid.append(h_l)
                        s_liquid.append(s_l)
                        h_vapor.append(h_v)
                        s_vapor.append(s_v)
                    except:
                        continue

                if len(s_liquid) > 10:
                    # Plot saturation dome
                    ax.plot(s_liquid, h_liquid, linewidth=2.5, label=f'{fluid} (liquid)')
                    ax.plot(s_vapor, h_vapor, linewidth=2.5, label=f'{fluid} (vapor)', linestyle='--')

                    # Mark critical point
                    ax.plot(s_crit, h_crit, 'o', markersize=10,
                           label=f'{fluid} kritisk punkt', markeredgewidth=2)

                    # Add isobars (constant pressure lines) in two-phase region
                    for p_iso_bar in [2, 5, 10]:
                        if p_iso_bar < p_crit:
                            try:
                                # Find temperature at this pressure
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
                print(f"Could not plot Mollier diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('Entropi s [kJ/(kg·K)]', fontsize=11, fontweight='bold')
        ax.set_ylabel('Entalpi h [kJ/kg]', fontsize=11, fontweight='bold')
        ax.set_title('Mollier Diagram (Entalpi-Entropi)', fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()

    def _on_plot_type_change(self, event):
        """Handle plot type change"""
        if self.current_fluids and self.db:
            self.plot_comparison(self.current_fluids, self.db)

    def _refresh_plot(self):
        """Refresh current plot"""
        if self.current_fluids and self.db:
            self.plot_comparison(self.current_fluids, self.db)


# Test standalone
if __name__ == "__main__":
    from core.fluid_database import FluidDatabase

    root = tk.Tk()
    root.title("Plot Panel Test")
    root.geometry("1000x700")

    panel = PlotPanel(root)
    panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Load database and plot some fluids
    db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')
    panel.plot_comparison(['R1233zd(E)', 'R245fa', 'Isopentane'], db)

    root.mainloop()
