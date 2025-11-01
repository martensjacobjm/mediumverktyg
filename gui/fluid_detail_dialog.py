#!/usr/bin/env python3
"""
Fluid Detail Dialog - Comprehensive fluid information viewer
Shows ALL available properties for a selected fluid
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import CoolProp.CoolProp as CP
from core.fluid_database import FluidDatabase
import numpy as np


class FluidDetailDialog(tk.Toplevel):
    """Dialog showing comprehensive fluid information"""

    def __init__(self, parent, fluid_name: str, db: FluidDatabase):
        super().__init__(parent)

        self.fluid_name = fluid_name
        self.db = db

        self.title(f"Komplett information - {fluid_name}")
        self.geometry("900x700")

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_fluid_data()

    def _create_widgets(self):
        """Create dialog widgets"""

        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(
            header,
            text=f"KOMPLETT MEDIUMINFORMATION",
            font=('Arial', 14, 'bold')
        ).pack(side=tk.LEFT)

        ttk.Label(
            header,
            text=self.fluid_name,
            font=('Arial', 16, 'bold'),
            foreground='#0066cc'
        ).pack(side=tk.RIGHT)

        # Create notebook with tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Tab 1: Basic properties
        self.basic_frame = self._create_scrollable_frame()
        self.notebook.add(self.basic_frame, text="Grundegenskaper")

        # Tab 2: Thermodynamic properties
        self.thermo_frame = self._create_scrollable_frame()
        self.notebook.add(self.thermo_frame, text="Termodynamik")

        # Tab 3: Safety & Environment
        self.safety_frame = self._create_scrollable_frame()
        self.notebook.add(self.safety_frame, text="Säkerhet & Miljö")

        # Tab 4: Transport properties
        self.transport_frame = self._create_scrollable_frame()
        self.notebook.add(self.transport_frame, text="Transportegenskaper")

        # Tab 5: Saturation table
        self.table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="Mättnadstabell")

        # Close button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(
            btn_frame,
            text="Stäng",
            command=self.destroy,
            width=15
        ).pack(side=tk.RIGHT)

        ttk.Button(
            btn_frame,
            text="Kopiera all data",
            command=self._copy_all_data,
            width=15
        ).pack(side=tk.RIGHT, padx=5)

    def _create_scrollable_frame(self):
        """Create a scrollable frame for property display"""
        container = ttk.Frame(self.notebook)

        # Create canvas with scrollbar
        canvas = tk.Canvas(container, bg='white')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store reference to scrollable_frame
        container.scrollable_frame = scrollable_frame

        return container

    def _add_section(self, parent, title):
        """Add a section header"""
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(fill=tk.X, padx=5, pady=5)
        return frame

    def _add_property(self, parent, label, value, unit=""):
        """Add a property row"""
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=2)

        ttk.Label(
            row,
            text=label + ":",
            width=35,
            font=('Arial', 9)
        ).pack(side=tk.LEFT)

        value_text = f"{value} {unit}".strip() if value is not None else "N/A"

        ttk.Label(
            row,
            text=value_text,
            font=('Arial', 9, 'bold'),
            foreground='#333333'
        ).pack(side=tk.LEFT, padx=10)

    def _get_brandklass(self, ashrae_class, flammable):
        """Determine fire/flammability class based on ASHRAE classification"""
        if not ashrae_class or ashrae_class == 'Unknown':
            return "Okänd"

        # ASHRAE flammability ratings:
        # 1 = No flame propagation
        # 2 = Lower flammability
        # 2L = Lower flammability, low burning velocity
        # 3 = Higher flammability

        if ashrae_class.endswith('1'):
            return "Icke brännbar (klass 1)"
        elif ashrae_class.endswith('2L'):
            return "Låg brännbarhet, låg flamhastighet (klass 2L)"
        elif ashrae_class.endswith('2'):
            return "Låg brännbarhet (klass 2)"
        elif ashrae_class.endswith('3'):
            return "Hög brännbarhet (klass 3)"
        elif flammable:
            return "Brännbar (klass okänd)"
        else:
            return "Icke brännbar"

    def _load_fluid_data(self):
        """Load all available fluid data"""
        try:
            # Get metadata
            meta = self.db.get_metadata(self.fluid_name)

            # Get CoolProp properties
            self._load_basic_properties(meta)
            self._load_thermodynamic_properties(meta)
            self._load_safety_environmental(meta)
            self._load_transport_properties()
            self._create_saturation_table()

        except Exception as e:
            error_label = ttk.Label(
                self.basic_frame.scrollable_frame,
                text=f"Fel vid laddning av data: {e}",
                foreground='red',
                font=('Arial', 10, 'bold')
            )
            error_label.pack(pady=20)

    def _load_basic_properties(self, meta):
        """Load basic identifying properties"""
        frame = self.basic_frame.scrollable_frame

        # Identification section
        id_section = self._add_section(frame, "Identifiering")

        self._add_property(id_section, "Fullständigt namn", self.fluid_name)

        # Try to get chemical formula from CoolProp
        try:
            formula = CP.get_fluid_param_string(self.fluid_name, "formula")
            self._add_property(id_section, "Molekylformel", formula)
        except:
            self._add_property(id_section, "Molekylformel", "N/A")

        # Try to get CAS number
        try:
            cas = CP.get_fluid_param_string(self.fluid_name, "CAS")
            self._add_property(id_section, "CAS-nummer", cas)
        except:
            self._add_property(id_section, "CAS-nummer", "N/A")

        # Molecular weight
        try:
            molar_mass = CP.PropsSI('MOLAR_MASS', self.fluid_name) * 1000  # kg/mol -> g/mol
            self._add_property(id_section, "Molmassa", f"{molar_mass:.3f}", "g/mol")
        except:
            self._add_property(id_section, "Molmassa", "N/A")

        # Critical properties section
        crit_section = self._add_section(frame, "Kritiska egenskaper")

        if meta:
            self._add_property(crit_section, "Kritisk temperatur (Tc)", f"{meta.T_critical:.2f}", "°C")
            self._add_property(crit_section, "Kritiskt tryck (Pc)", f"{meta.p_critical:.2f}", "bar")
        else:
            try:
                T_crit = CP.PropsSI('TCRIT', self.fluid_name) - 273.15
                p_crit = CP.PropsSI('PCRIT', self.fluid_name) / 1e5
                self._add_property(crit_section, "Kritisk temperatur (Tc)", f"{T_crit:.2f}", "°C")
                self._add_property(crit_section, "Kritiskt tryck (Pc)", f"{p_crit:.2f}", "bar")
            except:
                pass

        try:
            rho_crit = CP.PropsSI('RHOCRIT', self.fluid_name)
            self._add_property(crit_section, "Kritisk densitet (ρc)", f"{rho_crit:.2f}", "kg/m³")
        except:
            pass

        try:
            acentric = CP.PropsSI('ACENTRIC', self.fluid_name)
            self._add_property(crit_section, "Acentrisk faktor", f"{acentric:.4f}", "")
        except:
            pass

        # Triple point section
        triple_section = self._add_section(frame, "Trippelpunkt")

        try:
            T_triple = CP.PropsSI('TTRIPLE', self.fluid_name) - 273.15
            self._add_property(triple_section, "Trippelpunktstemperatur", f"{T_triple:.2f}", "°C")
        except:
            self._add_property(triple_section, "Trippelpunktstemperatur", "N/A")

        try:
            p_triple = CP.PropsSI('PTRIPLE', self.fluid_name) / 1e5
            self._add_property(triple_section, "Trippelpunktstryck", f"{p_triple:.6f}", "bar")
        except:
            self._add_property(triple_section, "Trippelpunktstryck", "N/A")

        # Additional thermodynamic limits
        limits_section = self._add_section(frame, "Temperatur- och tryckgränser")

        try:
            T_min = CP.PropsSI('TMIN', self.fluid_name) - 273.15
            self._add_property(limits_section, "Minsta giltig temperatur", f"{T_min:.2f}", "°C")
        except:
            pass

        try:
            T_max = CP.PropsSI('TMAX', self.fluid_name) - 273.15
            self._add_property(limits_section, "Maximal giltig temperatur", f"{T_max:.2f}", "°C")
        except:
            pass

        try:
            p_max = CP.PropsSI('PMAX', self.fluid_name) / 1e5
            self._add_property(limits_section, "Maximalt giltigt tryck", f"{p_max:.2f}", "bar")
        except:
            pass

    def _load_thermodynamic_properties(self, meta):
        """Load thermodynamic properties"""
        frame = self.thermo_frame.scrollable_frame

        # Boiling/phase change section
        phase_section = self._add_section(frame, "Fasövergångar vid olika tryck")

        if meta and meta.T_boiling_1atm:
            self._add_property(phase_section, "Kokpunkt/Daggpunkt @ 1 atm (1.013 bar)", f"{meta.T_boiling_1atm:.2f}", "°C")

        # Show dew/boiling points at different pressures
        pressures_bar = [0.5, 1.0, 2.0, 5.0, 10.0]
        for p_bar in pressures_bar:
            try:
                # For pure substances, dew point = boiling point at given pressure
                T_sat = CP.PropsSI('T', 'P', p_bar * 1e5, 'Q', 0, self.fluid_name) - 273.15
                self._add_property(phase_section, f"Kokpunkt/Daggpunkt @ {p_bar} bar", f"{T_sat:.2f}", "°C")
            except:
                pass

        # Properties at standard conditions (25°C)
        std_section = self._add_section(frame, "Egenskaper vid 25°C")

        try:
            props_25 = self.db.get_saturation_properties(self.fluid_name, 25.0)
            if props_25:
                self._add_property(std_section, "Mättningstryck", f"{props_25.pressure:.3f}", "bar")
                self._add_property(std_section, "Förångningsvärme (hfg)", f"{props_25.hfg:.2f}", "kJ/kg")
                self._add_property(std_section, "Vätskdensitet", f"{props_25.rho_liquid:.2f}", "kg/m³")
                self._add_property(std_section, "Ångdensitet", f"{props_25.rho_vapor:.2f}", "kg/m³")
                self._add_property(std_section, "Specifik värmekapacitet (vätska)", f"{props_25.cp_liquid:.3f}", "kJ/(kg·K)")
        except:
            self._add_property(std_section, "Data ej tillgänglig", "N/A")

        # Properties at operating conditions (50°C)
        op_section = self._add_section(frame, "Egenskaper vid 50°C (drifttemperatur)")

        try:
            props_50 = self.db.get_saturation_properties(self.fluid_name, 50.0)
            if props_50:
                self._add_property(op_section, "Mättningstryck", f"{props_50.pressure:.3f}", "bar")
                self._add_property(op_section, "Förångningsvärme (hfg)", f"{props_50.hfg:.2f}", "kJ/kg")
                self._add_property(op_section, "Vätskdensitet", f"{props_50.rho_liquid:.2f}", "kg/m³")
                self._add_property(op_section, "Ångdensitet", f"{props_50.rho_vapor:.2f}", "kg/m³")
                self._add_property(op_section, "Specifik värmekapacitet (vätska)", f"{props_50.cp_liquid:.3f}", "kJ/(kg·K)")
                self._add_property(op_section, "Viskositet (ånga)", f"{props_50.mu_vapor:.2f}", "μPa·s")
        except:
            self._add_property(op_section, "Data ej tillgänglig", "N/A")

    def _load_safety_environmental(self, meta):
        """Load safety and environmental properties"""
        frame = self.safety_frame.scrollable_frame

        # Safety section
        safety_section = self._add_section(frame, "Säkerhetsklassificering")

        if meta:
            self._add_property(safety_section, "ASHRAE säkerhetsklass", meta.ashrae_class or "N/A")

            # Brandklass based on ASHRAE classification
            brandklass = self._get_brandklass(meta.ashrae_class, meta.flammable)
            self._add_property(safety_section, "Brandklass", brandklass)

            self._add_property(safety_section, "Brännbar", "Ja" if meta.flammable else "Nej")
            self._add_property(safety_section, "Giftig", "Ja" if meta.toxic else "Nej")

        # Environmental section
        env_section = self._add_section(frame, "Miljöpåverkan")

        if meta:
            self._add_property(env_section, "GWP (Global Warming Potential)", str(meta.gwp) if meta.gwp else "N/A")
            self._add_property(env_section, "ODP (Ozone Depletion Potential)", f"{meta.odp:.4f}" if meta.odp is not None else "N/A")

            if hasattr(meta, 'alt') and meta.alt:
                self._add_property(env_section, "Atmosfärisk livstid (ALT)", str(meta.alt), "år")

        # ORC suitability
        if meta and meta.orc_suitability:
            orc_section = self._add_section(frame, "ORC-lämplighet")
            self._add_property(orc_section, "Lämplighet för ORC", meta.orc_suitability)
            self._add_property(orc_section, "Anmärkningar", meta.notes or "Inga anmärkningar")

        # Economic section
        if meta:
            econ_section = self._add_section(frame, "Ekonomi & Tillgänglighet")
            self._add_property(econ_section, "Kostnadsindex (rel. R245fa)", f"{meta.cost_index:.2f}" if meta.cost_index else "N/A")
            self._add_property(econ_section, "Tillgänglighet", meta.availability or "N/A")

    def _load_transport_properties(self):
        """Load transport properties at various temperatures"""
        frame = self.transport_frame.scrollable_frame

        temperatures = [0, 10, 20, 30, 40, 50, 60, 70, 80]

        for temp in temperatures:
            section = self._add_section(frame, f"Transportegenskaper vid {temp}°C")

            try:
                props = self.db.get_saturation_properties(self.fluid_name, float(temp))
                if props:
                    self._add_property(section, "Viskositet (ånga)", f"{props.mu_vapor:.3f}", "μPa·s")
                    self._add_property(section, "Värmeledningsförmåga (ånga)", f"{props.k_vapor:.4f}", "W/(m·K)")
                    self._add_property(section, "Värmeledningsförmåga (vätska)", f"{props.k_liquid:.4f}", "W/(m·K)")
                    self._add_property(section, "Ytspänning", f"{props.surface_tension:.6f}", "N/m")

                    # Prandtl number (calculated)
                    if props.mu_vapor > 0 and props.k_vapor > 0 and props.cp_vapor > 0:
                        Pr = (props.cp_vapor * 1000 * props.mu_vapor * 1e-6) / props.k_vapor
                        self._add_property(section, "Prandtl-tal (ånga)", f"{Pr:.3f}", "")
            except Exception as e:
                self._add_property(section, "Data ej tillgänglig", str(e))

    def _create_saturation_table(self):
        """Create saturation property table"""
        # Create treeview
        columns = ('T', 'P', 'rho_l', 'rho_v', 'hfg', 'cp_l', 'mu_v', 'sigma')

        tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=20)

        # Define headings
        tree.heading('T', text='T [°C]')
        tree.heading('P', text='P [bar]')
        tree.heading('rho_l', text='ρ_väts [kg/m³]')
        tree.heading('rho_v', text='ρ_ånga [kg/m³]')
        tree.heading('hfg', text='hfg [kJ/kg]')
        tree.heading('cp_l', text='cp_l [kJ/kg·K]')
        tree.heading('mu_v', text='μ_v [μPa·s]')
        tree.heading('sigma', text='σ [N/m]')

        # Column widths
        for col in columns:
            tree.column(col, width=100, anchor='center')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Fill with data
        temperatures = range(-50, 101, 5)  # -50 to 100°C in 5°C steps

        for T in temperatures:
            try:
                props = self.db.get_saturation_properties(self.fluid_name, float(T))
                if props:
                    tree.insert('', 'end', values=(
                        f"{T}",
                        f"{props.pressure:.3f}",
                        f"{props.rho_liquid:.2f}",
                        f"{props.rho_vapor:.3f}",
                        f"{props.hfg:.2f}",
                        f"{props.cp_liquid:.3f}",
                        f"{props.mu_vapor:.2f}",
                        f"{props.surface_tension:.6f}"
                    ))
            except:
                # Skip temperatures where properties can't be calculated
                continue

    def _copy_all_data(self):
        """Copy all fluid data to clipboard"""
        # TODO: Implement clipboard copy functionality
        print(f"Copying data for {self.fluid_name}")


# Test standalone
if __name__ == "__main__":
    from core.fluid_database import FluidDatabase

    root = tk.Tk()
    root.withdraw()  # Hide main window

    db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')

    dialog = FluidDetailDialog(root, 'Water', db)
    dialog.mainloop()
