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

        # Plot type selections (for combination diagrams)
        self.plot_selections = {
            'Tryck-Temperatur': tk.BooleanVar(value=True),
            'Förångningsvärme': tk.BooleanVar(value=False),
            'Viskositet': tk.BooleanVar(value=False),
            'Densitet (ånga)': tk.BooleanVar(value=False),
            'T-s diagram': tk.BooleanVar(value=False),
            'P-h diagram': tk.BooleanVar(value=False),
            'Mollier diagram (h-s)': tk.BooleanVar(value=False)
        }

        self._create_widgets()

    def _create_widgets(self):
        """Create plot controls and canvas"""

        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(
            control_frame,
            text="DIAGRAM - Välj diagram att visa:",
            font=('Arial', 12, 'bold')
        ).pack(side=tk.LEFT)

        # Refresh button
        ttk.Button(
            control_frame,
            text="Uppdatera",
            command=self._refresh_plot
        ).pack(side=tk.RIGHT, padx=5)

        # Checkbox frame for plot type selection
        checkbox_frame = ttk.LabelFrame(self, text="Välj diagramtyper (kombinationsdiagram)", padding=10)
        checkbox_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Create checkboxes in rows
        row1_frame = ttk.Frame(checkbox_frame)
        row1_frame.pack(fill=tk.X, pady=2)

        row2_frame = ttk.Frame(checkbox_frame)
        row2_frame.pack(fill=tk.X, pady=2)

        # Row 1: Basic property plots
        for plot_type in ['Tryck-Temperatur', 'Förångningsvärme', 'Viskositet', 'Densitet (ånga)']:
            ttk.Checkbutton(
                row1_frame,
                text=plot_type,
                variable=self.plot_selections[plot_type],
                command=self._on_selection_change
            ).pack(side=tk.LEFT, padx=10)

        # Row 2: Thermodynamic diagrams
        for plot_type in ['T-s diagram', 'P-h diagram', 'Mollier diagram (h-s)']:
            ttk.Checkbutton(
                row2_frame,
                text=plot_type,
                variable=self.plot_selections[plot_type],
                command=self._on_selection_change
            ).pack(side=tk.LEFT, padx=10)

        # Selection control buttons
        btn_frame = ttk.Frame(checkbox_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(
            btn_frame,
            text="Välj alla",
            command=self._select_all_plots,
            width=12
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            btn_frame,
            text="Avmarkera alla",
            command=self._deselect_all_plots,
            width=14
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            btn_frame,
            text="Endast termodynamiska (T-s, P-h, Mollier)",
            command=self._select_thermo_only,
            width=35
        ).pack(side=tk.LEFT, padx=2)

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
        """Plot comparison for selected fluids - supports multiple plots"""
        self.current_fluids = fluids
        self.db = db

        if not fluids or not db:
            self._plot_empty()
            return

        # Get selected plot types
        selected_plots = [
            plot_type for plot_type, var in self.plot_selections.items()
            if var.get()
        ]

        if not selected_plots:
            self._plot_empty()
            return

        # Clear figure
        self.figure.clear()

        # Determine grid layout
        n_plots = len(selected_plots)
        if n_plots == 1:
            rows, cols = 1, 1
        elif n_plots == 2:
            rows, cols = 1, 2
        elif n_plots <= 4:
            rows, cols = 2, 2
        elif n_plots <= 6:
            rows, cols = 2, 3
        else:
            rows, cols = 3, 3

        # Create subplots
        for idx, plot_type in enumerate(selected_plots):
            ax = self.figure.add_subplot(rows, cols, idx + 1)

            if plot_type == 'Tryck-Temperatur':
                self._plot_pressure_temp_ax(ax)
            elif plot_type == 'Förångningsvärme':
                self._plot_latent_heat_ax(ax)
            elif plot_type == 'Viskositet':
                self._plot_viscosity_ax(ax)
            elif plot_type == 'Densitet (ånga)':
                self._plot_density_ax(ax)
            elif plot_type == 'T-s diagram':
                self._plot_ts_diagram_ax(ax)
            elif plot_type == 'P-h diagram':
                self._plot_ph_diagram_ax(ax)
            elif plot_type == 'Mollier diagram (h-s)':
                self._plot_mollier_diagram_ax(ax)

        self.figure.tight_layout()
        self.canvas.draw()

    def _plot_empty(self):
        """Plot empty placeholder"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5,
            'Välj medier från listan ovan för jämförelse\n\n'
            'Markera checkboxarna för att välja diagram',
            ha='center', va='center',
            fontsize=14, color='gray'
        )
        ax.axis('off')
        self.canvas.draw()

    def _on_selection_change(self):
        """Handle plot type selection change"""
        if self.current_fluids and self.db:
            self.plot_comparison(self.current_fluids, self.db)

    def _select_all_plots(self):
        """Select all plot types"""
        for var in self.plot_selections.values():
            var.set(True)
        self._on_selection_change()

    def _deselect_all_plots(self):
        """Deselect all plot types"""
        for var in self.plot_selections.values():
            var.set(False)
        self._on_selection_change()

    def _select_thermo_only(self):
        """Select only thermodynamic diagrams (T-s, P-h, Mollier)"""
        thermo_plots = ['T-s diagram', 'P-h diagram', 'Mollier diagram (h-s)']
        for plot_type, var in self.plot_selections.items():
            var.set(plot_type in thermo_plots)
        self._on_selection_change()

    def _plot_pressure_temp_ax(self, ax):
        """Plot pressure vs temperature on given axes"""
        temps = np.linspace(0, 100, 101)

        for fluid in self.current_fluids:
            pressures = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    pressures.append(props.pressure)
                else:
                    pressures.append(np.nan)

            ax.plot(temps, pressures, label=fluid, linewidth=1.5, marker='o', markevery=20)

        # Optimal zones
        ax.axhspan(2, 8, alpha=0.1, color='green')
        ax.axvspan(10, 30, alpha=0.05, color='blue')
        ax.axvspan(40, 80, alpha=0.05, color='red')

        ax.set_xlabel('Temp [°C]', fontsize=9)
        ax.set_ylabel('Tryck [bar]', fontsize=9)
        ax.set_title('Tryck-Temperatur', fontsize=10, fontweight='bold')
        ax.legend(loc='upper left', fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)

    def _plot_latent_heat_ax(self, ax):
        """Plot latent heat vs temperature on given axes"""
        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            hfg_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    hfg_values.append(props.hfg)
                else:
                    hfg_values.append(np.nan)

            ax.plot(temps, hfg_values, label=fluid, linewidth=1.5, marker='s', markevery=8)

        ax.axvline(50, color='gray', linestyle='--', alpha=0.5)

        ax.set_xlabel('Temp [°C]', fontsize=9)
        ax.set_ylabel('hfg [kJ/kg]', fontsize=9)
        ax.set_title('Förångningsvärme', fontsize=10, fontweight='bold')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    def _plot_viscosity_ax(self, ax):
        """Plot vapor viscosity vs temperature on given axes"""
        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            mu_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    mu_values.append(props.mu_vapor)
                else:
                    mu_values.append(np.nan)

            ax.plot(temps, mu_values, label=fluid, linewidth=1.5, marker='o', markevery=8)

        # TesTur reference
        ax.axhline(18.2, color='purple', linestyle=':', alpha=0.5, linewidth=1.5)

        ax.set_xlabel('Temp [°C]', fontsize=9)
        ax.set_ylabel('μ [μPa·s]', fontsize=9)
        ax.set_title('Viskositet', fontsize=10, fontweight='bold')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    def _plot_density_ax(self, ax):
        """Plot vapor density vs temperature on given axes"""
        temps = np.linspace(10, 80, 36)

        for fluid in self.current_fluids:
            rho_values = []
            for T in temps:
                props = self.db.get_saturation_properties(fluid, T)
                if props:
                    rho_values.append(props.rho_vapor)
                else:
                    rho_values.append(np.nan)

            ax.plot(temps, rho_values, label=fluid, linewidth=1.5, marker='d', markevery=8)

        ax.set_xlabel('Temp [°C]', fontsize=9)
        ax.set_ylabel('ρ [kg/m³]', fontsize=9)
        ax.set_title('Densitet (ånga)', fontsize=10, fontweight='bold')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    def _plot_ts_diagram_ax(self, ax):
        """Plot T-s diagram (Temperature-Entropy) on given axes"""
        from CoolProp.CoolProp import PropsSI

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
                    ax.plot(s_liquid, temps_valid, linewidth=1.5, label=f'{fluid}')
                    ax.plot(s_vapor, temps_valid, linewidth=1.5, linestyle='--')

                    # Mark critical point
                    s_crit = PropsSI('S', 'T', T_crit + 273.15, 'P', p_crit * 1e5, fluid) / 1000
                    ax.plot(s_crit, T_crit, 'o', markersize=6, markeredgewidth=1)

            except Exception as e:
                print(f"Could not plot T-s diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('s [kJ/(kg·K)]', fontsize=9)
        ax.set_ylabel('T [°C]', fontsize=9)
        ax.set_title('T-s Diagram', fontsize=10, fontweight='bold')
        ax.legend(loc='best', fontsize=7)
        ax.grid(True, alpha=0.3)

    def _plot_ph_diagram_ax(self, ax):
        """Plot P-h diagram (Pressure-Enthalpy) on given axes"""
        from CoolProp.CoolProp import PropsSI

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
                    ax.plot(h_liquid, p_sat, linewidth=1.5, label=f'{fluid}')
                    ax.plot(h_vapor, p_sat, linewidth=1.5, linestyle='--')

                    # Mark critical point
                    ax.plot(h_crit, p_crit, 'o', markersize=6, markeredgewidth=1)

                    # Add isotherms (simplified for combination view)
                    for T_iso in [50]:
                        if T_min < T_iso < T_crit - 5:
                            try:
                                T_k = T_iso + 273.15
                                p_iso = PropsSI('P', 'T', T_k, 'Q', 0, fluid) / 1e5
                                h_l_iso = PropsSI('H', 'T', T_k, 'Q', 0, fluid) / 1000
                                h_v_iso = PropsSI('H', 'T', T_k, 'Q', 1, fluid) / 1000
                                ax.plot([h_l_iso, h_v_iso], [p_iso, p_iso],
                                       'k:', alpha=0.3, linewidth=1)
                                ax.text((h_l_iso + h_v_iso)/2, p_iso, f'{T_iso}°C',
                                       fontsize=7, ha='center', va='bottom', alpha=0.6)
                            except:
                                pass

            except Exception as e:
                print(f"Could not plot P-h diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('h [kJ/kg]', fontsize=9)
        ax.set_ylabel('P [bar]', fontsize=9)
        ax.set_title('P-h Diagram', fontsize=10, fontweight='bold')
        ax.set_yscale('log')
        ax.legend(loc='best', fontsize=7)
        ax.grid(True, alpha=0.3, which='both')

    def _plot_mollier_diagram_ax(self, ax):
        """Plot Mollier diagram (h-s, Enthalpy-Entropy) on given axes"""
        from CoolProp.CoolProp import PropsSI

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
                    ax.plot(s_liquid, h_liquid, linewidth=1.5, label=f'{fluid}')
                    ax.plot(s_vapor, h_vapor, linewidth=1.5, linestyle='--')

                    # Mark critical point
                    ax.plot(s_crit, h_crit, 'o', markersize=6, markeredgewidth=1)

                    # Add isobars (simplified for combination view)
                    for p_iso_bar in [5]:
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
                                           'k:', alpha=0.3, linewidth=1)
                                    ax.text(s_v_iso, h_v_iso, f'{p_iso_bar}bar',
                                           fontsize=7, ha='left', va='bottom', alpha=0.6)
                            except:
                                pass

            except Exception as e:
                print(f"Could not plot Mollier diagram for {fluid}: {e}")
                continue

        ax.set_xlabel('s [kJ/(kg·K)]', fontsize=9)
        ax.set_ylabel('h [kJ/kg]', fontsize=9)
        ax.set_title('Mollier Diagram', fontsize=10, fontweight='bold')
        ax.legend(loc='best', fontsize=7)
        ax.grid(True, alpha=0.3)

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
