#!/usr/bin/env python3
"""
Fluid Database - CoolProp Integration
Manages all 124+ working fluids with thermodynamic properties and metadata
"""

import CoolProp.CoolProp as CP
from functools import lru_cache
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class FluidProperties:
    """Thermodynamic properties at a given state"""
    temperature: float  # °C
    pressure: float  # bar
    h_liquid: float  # kJ/kg
    h_vapor: float  # kJ/kg
    hfg: float  # kJ/kg (latent heat)
    s_liquid: float  # kJ/kg·K
    s_vapor: float  # kJ/kg·K
    rho_liquid: float  # kg/m³
    rho_vapor: float  # kg/m³
    mu_vapor: float  # μPa·s
    cp_liquid: float  # kJ/kg·K
    cp_vapor: float  # kJ/kg·K


@dataclass
class FluidMetadata:
    """Static metadata for a fluid"""
    name: str
    coolprop_name: str
    formula: str = ""
    molar_mass: float = 0.0  # g/mol
    T_critical: float = 0.0  # °C
    p_critical: float = 0.0  # bar
    T_boiling_1atm: float = 0.0  # °C

    # Environmental
    gwp: int = 0  # Global Warming Potential
    odp: float = 0.0  # Ozone Depletion Potential

    # Safety
    ashrae_class: str = "Unknown"  # A1, A2L, B1, B2L
    flammable: bool = False
    toxic: bool = False

    # ORC suitability
    orc_suitability: str = "UNKNOWN"  # EXCELLENT/GOOD/MODERATE/POOR

    # Economic
    cost_index: float = 1.0  # Relative to R245fa
    availability: str = "UNKNOWN"  # EXCELLENT/GOOD/MODERATE/LIMITED

    # Notes
    notes: str = ""


class FluidDatabase:
    """
    Main database class for managing all working fluids
    Integrates CoolProp for thermodynamic properties
    """

    def __init__(self, metadata_file: Optional[str] = None):
        """
        Initialize database

        Args:
            metadata_file: Path to JSON file with manual metadata (optional)
        """
        self.all_fluids = self._discover_coolprop_fluids()
        self.metadata_cache: Dict[str, FluidMetadata] = {}

        # ALWAYS generate basic metadata first (for ALL fluids)
        self._generate_basic_metadata()

        # Then load manual metadata to override/enhance basic data
        if metadata_file and os.path.exists(metadata_file):
            self._load_metadata(metadata_file)

    def _discover_coolprop_fluids(self) -> List[str]:
        """Discover ALL available fluids from CoolProp - no filtering!"""
        all_fluids = CP.FluidsList()

        # Return ALL fluids - let the USER decide what's suitable via filters!
        # Previously filtered for "ORC-suitable" but that removed Water, Air, etc.
        # Now we show everything and let GUI filters do the work.

        valid_fluids = []
        for fluid in all_fluids:
            try:
                # Just verify we can get basic properties (fluid is usable)
                T_crit = CP.PropsSI('Tcrit', fluid)
                p_crit = CP.PropsSI('pcrit', fluid)

                # If we got here, fluid is valid
                valid_fluids.append(fluid)
            except:
                # Skip fluids that cause errors (corrupted data, etc)
                # This is the ONLY filtering - technical errors only
                pass

        return sorted(valid_fluids)

    def _generate_basic_metadata(self):
        """Generate basic metadata from CoolProp for all fluids"""
        for fluid in self.all_fluids:
            try:
                T_crit = CP.PropsSI('Tcrit', fluid) - 273.15
                p_crit = CP.PropsSI('pcrit', fluid) / 1e5
                M = CP.PropsSI('M', fluid) * 1000  # kg/mol → g/mol

                # Try to get boiling point at 1 atm
                try:
                    T_boil = CP.PropsSI('T', 'P', 101325, 'Q', 0, fluid) - 273.15
                except:
                    T_boil = None

                self.metadata_cache[fluid] = FluidMetadata(
                    name=fluid,
                    coolprop_name=fluid,
                    molar_mass=M,
                    T_critical=T_crit,
                    p_critical=p_crit,
                    T_boiling_1atm=T_boil if T_boil else 0.0
                )
            except Exception as e:
                print(f"Warning: Could not get metadata for {fluid}: {e}")

    def _load_metadata(self, filename: str):
        """Load manual metadata from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)

        for fluid_name, meta_dict in data.items():
            if fluid_name in self.all_fluids:
                # Get existing metadata or create basic one
                existing = self.metadata_cache.get(fluid_name)

                if existing:
                    # Update existing metadata with manual data
                    for key, value in meta_dict.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                else:
                    # Create new metadata with name and coolprop_name
                    meta_dict['name'] = fluid_name
                    meta_dict['coolprop_name'] = fluid_name
                    self.metadata_cache[fluid_name] = FluidMetadata(**meta_dict)

    @lru_cache(maxsize=10000)
    def get_saturation_properties(self, fluid: str, T_celsius: float) -> Optional[FluidProperties]:
        """
        Get saturated properties at given temperature
        Uses LRU cache for performance

        Args:
            fluid: Fluid name (CoolProp compatible)
            T_celsius: Temperature in °C

        Returns:
            FluidProperties object or None if error
        """
        T_kelvin = T_celsius + 273.15

        try:
            # Pressure
            p_bar = CP.PropsSI('P', 'T', T_kelvin, 'Q', 0, fluid) / 1e5

            # Enthalpy
            h_liq = CP.PropsSI('H', 'T', T_kelvin, 'Q', 0, fluid) / 1000  # J/kg → kJ/kg
            h_vap = CP.PropsSI('H', 'T', T_kelvin, 'Q', 1, fluid) / 1000
            hfg = h_vap - h_liq

            # Entropy
            s_liq = CP.PropsSI('S', 'T', T_kelvin, 'Q', 0, fluid) / 1000  # J/kg·K → kJ/kg·K
            s_vap = CP.PropsSI('S', 'T', T_kelvin, 'Q', 1, fluid) / 1000

            # Density
            rho_liq = CP.PropsSI('D', 'T', T_kelvin, 'Q', 0, fluid)
            rho_vap = CP.PropsSI('D', 'T', T_kelvin, 'Q', 1, fluid)

            # Viscosity (vapor)
            mu_vap = CP.PropsSI('V', 'T', T_kelvin, 'Q', 1, fluid) * 1e6  # Pa·s → μPa·s

            # Specific heat
            cp_liq = CP.PropsSI('C', 'T', T_kelvin, 'Q', 0, fluid) / 1000  # J/kg·K → kJ/kg·K
            cp_vap = CP.PropsSI('C', 'T', T_kelvin, 'Q', 1, fluid) / 1000

            return FluidProperties(
                temperature=T_celsius,
                pressure=p_bar,
                h_liquid=h_liq,
                h_vapor=h_vap,
                hfg=hfg,
                s_liquid=s_liq,
                s_vapor=s_vap,
                rho_liquid=rho_liq,
                rho_vapor=rho_vap,
                mu_vapor=mu_vap,
                cp_liquid=cp_liq,
                cp_vapor=cp_vap
            )

        except Exception as e:
            print(f"Error getting properties for {fluid} at {T_celsius}°C: {e}")
            return None

    def get_metadata(self, fluid: str) -> Optional[FluidMetadata]:
        """Get metadata for a fluid"""
        return self.metadata_cache.get(fluid)

    def get_all_fluids(self) -> List[str]:
        """Get list of all available fluids"""
        return self.all_fluids.copy()

    def filter_fluids(self,
                     bp_range: Optional[Tuple[float, float]] = None,
                     gwp_max: Optional[int] = None,
                     safety_classes: Optional[List[str]] = None,
                     pressure_range: Optional[Tuple[float, float]] = None,
                     pressure_temp: float = 50.0) -> List[str]:
        """
        Filter fluids based on criteria

        IMPORTANT: If a fluid lacks metadata for a filter criterion, it is INCLUDED
        (shown to user). This lets the USER decide, not the program!

        Args:
            bp_range: Boiling point range (min, max) in °C
            gwp_max: Maximum GWP allowed
            safety_classes: List of acceptable ASHRAE classes
            pressure_range: Pressure range (min, max) in bar at pressure_temp
            pressure_temp: Temperature for pressure filtering (default 50°C)

        Returns:
            List of fluid names that match criteria
        """
        filtered = []

        for fluid in self.all_fluids:
            meta = self.get_metadata(fluid)

            # If no metadata at all, INCLUDE the fluid (let user see it)
            # User can filter it out manually if they want
            if not meta:
                filtered.append(fluid)
                continue

            skip = False

            # Boiling point filter - only apply if data exists
            if bp_range and meta.T_boiling_1atm is not None and meta.T_boiling_1atm != 0:
                if meta.T_boiling_1atm < bp_range[0] or meta.T_boiling_1atm > bp_range[1]:
                    skip = True

            # GWP filter - only apply if GWP data exists and is meaningful
            if not skip and gwp_max is not None and meta.gwp > 0:
                if meta.gwp > gwp_max:
                    skip = True

            # Safety class filter - only apply if safety class is known
            if not skip and safety_classes and meta.ashrae_class not in ['Unknown', '', None]:
                if meta.ashrae_class not in safety_classes:
                    skip = True

            # Pressure filter - only apply if we can get properties
            if not skip and pressure_range:
                try:
                    props = self.get_saturation_properties(fluid, pressure_temp)
                    if props and props.pressure > 0:
                        if props.pressure < pressure_range[0] or props.pressure > pressure_range[1]:
                            skip = True
                    # If can't get properties, INCLUDE the fluid anyway
                except:
                    # If error getting properties, INCLUDE the fluid
                    pass

            if not skip:
                filtered.append(fluid)

        return filtered

    def export_to_json(self, filename: str):
        """Export all metadata to JSON file"""
        data = {}
        for fluid in self.all_fluids:
            meta = self.get_metadata(fluid)
            if meta:
                data[fluid] = {
                    'name': meta.name,
                    'coolprop_name': meta.coolprop_name,
                    'formula': meta.formula,
                    'molar_mass': meta.molar_mass,
                    'T_critical': meta.T_critical,
                    'p_critical': meta.p_critical,
                    'T_boiling_1atm': meta.T_boiling_1atm,
                    'gwp': meta.gwp,
                    'odp': meta.odp,
                    'ashrae_class': meta.ashrae_class,
                    'flammable': meta.flammable,
                    'toxic': meta.toxic,
                    'orc_suitability': meta.orc_suitability,
                    'cost_index': meta.cost_index,
                    'availability': meta.availability,
                    'notes': meta.notes
                }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported metadata for {len(data)} fluids to {filename}")


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("FLUID DATABASE - Testing")
    print("="*70)

    # Initialize database
    db = FluidDatabase()

    print(f"\nTotal ORC-suitable fluids: {len(db.get_all_fluids())}")
    print(f"\nSample fluids: {db.get_all_fluids()[:10]}")

    # Test property retrieval
    print("\n" + "="*70)
    print("Testing R1233zd(E) properties at 50°C:")
    print("="*70)
    props = db.get_saturation_properties('R1233zd(E)', 50)
    if props:
        print(f"Pressure: {props.pressure:.2f} bar")
        print(f"Latent heat: {props.hfg:.1f} kJ/kg")
        print(f"Vapor viscosity: {props.mu_vapor:.1f} μPa·s")
        print(f"Vapor density: {props.rho_vapor:.2f} kg/m³")

    # Test filtering
    print("\n" + "="*70)
    print("Fluids with boiling point 10-30°C:")
    print("="*70)
    filtered = db.filter_fluids(bp_range=(10, 30))
    for f in filtered[:10]:
        meta = db.get_metadata(f)
        print(f"  {f}: Tb = {meta.T_boiling_1atm:.1f}°C, Tc = {meta.T_critical:.1f}°C")

    # Export metadata
    print("\n" + "="*70)
    db.export_to_json('data/fluid_metadata_generated.json')
    print("="*70)
