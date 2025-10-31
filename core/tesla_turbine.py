#!/usr/bin/env python3
"""
Tesla Turbine Calculations
TesTur-validated disc spacing and turbine dimensioning
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class TesTurReference:
    """TesTur experimental data for validation"""
    medium: str = "Air @ 20°C"
    viscosity: float = 18.2  # μPa·s
    disc_spacing: float = 0.234  # mm
    disc_thickness: float = 0.254  # mm
    diameter: float = 254  # mm
    num_discs: int = 75
    num_nozzles: int = 12
    power_verified: float = 1200  # W
    rpm_operating: int = 10000
    pressure_in: float = 5.5  # bar
    pressure_out: float = 1.0  # bar
    pressure_ratio: float = 5.5
    source: str = "YouTube Video K7qZvq1CMFg, Charlie Solis comments"


# Global TesTur reference
TESTUR_REF = TesTurReference()


@dataclass
class TeslaTurbineDesign:
    """Tesla turbine design specifications"""
    fluid: str
    disc_spacing: float  # mm
    disc_spacing_tolerance: tuple  # (min, max) in mm
    disc_thickness: float  # mm
    diameter: float  # mm
    num_discs: int
    num_nozzles: int
    estimated_rpm: int
    viscosity_fluid: float  # μPa·s
    viscosity_scaling: float  # Ratio to TesTur
    notes: str = ""


def calculate_disc_spacing(mu_fluid: float,
                           mu_ref: float = TESTUR_REF.viscosity,
                           b_ref: float = TESTUR_REF.disc_spacing) -> tuple:
    """
    Calculate optimal disc spacing from viscosity

    Based on boundary layer theory for Tesla turbines:
    b₂ / b₁ = √(μ₂ / μ₁)

    Args:
        mu_fluid: Fluid vapor viscosity [μPa·s]
        mu_ref: Reference viscosity (TesTur air) [μPa·s]
        b_ref: Reference disc spacing (TesTur) [mm]

    Returns:
        (b_optimal, scaling_factor)
    """
    scaling_factor = math.sqrt(mu_fluid / mu_ref)
    b_optimal = b_ref * scaling_factor

    return b_optimal, scaling_factor


def design_tesla_turbine(fluid: str,
                        mu_vapor: float,
                        pressure_ratio: float,
                        target_power_kW: float = 1.0) -> TeslaTurbineDesign:
    """
    Design Tesla turbine based on fluid properties

    Args:
        fluid: Fluid name
        mu_vapor: Vapor viscosity [μPa·s]
        pressure_ratio: Evap pressure / cond pressure
        target_power_kW: Target power output [kW]

    Returns:
        TeslaTurbineDesign object
    """

    # Calculate disc spacing
    b_optimal, scaling = calculate_disc_spacing(mu_vapor)

    # Tolerance range (±5%)
    b_min = b_optimal * 0.95
    b_max = b_optimal * 1.05

    # Start with TesTur geometry as baseline
    disc_thickness = TESTUR_REF.disc_thickness
    diameter = TESTUR_REF.diameter
    num_discs = TESTUR_REF.num_discs
    num_nozzles = TESTUR_REF.num_nozzles

    # Estimate RPM scaling based on pressure ratio
    # Lower pressure ratio typically means lower RPM
    rpm_scaling = math.sqrt(pressure_ratio / TESTUR_REF.pressure_ratio)
    estimated_rpm = int(TESTUR_REF.rpm_operating * rpm_scaling)

    # Scale number of discs based on power target
    power_scaling = target_power_kW / (TESTUR_REF.power_verified / 1000)
    if power_scaling > 1.2:
        num_discs = int(num_discs * math.sqrt(power_scaling))

    # Generate notes
    notes = f"""Design based on TesTur scaling:
- Viscosity ratio: {scaling:.3f} ({mu_vapor:.1f} / {TESTUR_REF.viscosity} μPa·s)
- Disc spacing scaled from {TESTUR_REF.disc_spacing} mm
- Pressure ratio: {pressure_ratio:.2f} vs TesTur {TESTUR_REF.pressure_ratio}
- Estimated RPM adjusted for pressure ratio
"""

    return TeslaTurbineDesign(
        fluid=fluid,
        disc_spacing=b_optimal,
        disc_spacing_tolerance=(b_min, b_max),
        disc_thickness=disc_thickness,
        diameter=diameter,
        num_discs=num_discs,
        num_nozzles=num_nozzles,
        estimated_rpm=estimated_rpm,
        viscosity_fluid=mu_vapor,
        viscosity_scaling=scaling,
        notes=notes
    )


def print_turbine_design(design: TeslaTurbineDesign, show_testur: bool = True):
    """Pretty print turbine design"""

    print(f"\n{'='*70}")
    print(f"TESLA TURBINE DESIGN: {design.fluid}")
    print(f"{'='*70}")

    print(f"\n--- DISC GEOMETRY ---")
    print(f"Disc spacing:        {design.disc_spacing:.3f} mm")
    print(f"  Tolerance range:   {design.disc_spacing_tolerance[0]:.3f} - "
          f"{design.disc_spacing_tolerance[1]:.3f} mm (±5%)")
    print(f"  Recommended start: {round(design.disc_spacing, 2):.2f} mm")
    print(f"Disc thickness:      {design.disc_thickness:.3f} mm")
    print(f"  Thickness/spacing: {design.disc_thickness/design.disc_spacing:.2f}")

    print(f"\n--- OVERALL DIMENSIONS ---")
    print(f"Rotor diameter:      {design.diameter} mm")
    print(f"Number of discs:     {design.num_discs}")
    print(f"Number of nozzles:   {design.num_nozzles}")
    print(f"Estimated RPM:       {design.estimated_rpm}")

    print(f"\n--- VISCOSITY SCALING ---")
    print(f"Fluid viscosity:     {design.viscosity_fluid:.1f} μPa·s")
    print(f"TesTur reference:    {TESTUR_REF.viscosity} μPa·s (air)")
    print(f"Scaling factor:      √({design.viscosity_fluid}/{TESTUR_REF.viscosity}) = {design.viscosity_scaling:.3f}")
    print(f"Impact on spacing:   {TESTUR_REF.disc_spacing} mm × {design.viscosity_scaling:.3f} = "
          f"{design.disc_spacing:.3f} mm")

    if show_testur:
        print(f"\n--- TESTUR REFERENCE DATA ---")
        print(f"Medium:              {TESTUR_REF.medium}")
        print(f"Disc spacing:        {TESTUR_REF.disc_spacing} mm")
        print(f"Disc thickness:      {TESTUR_REF.disc_thickness} mm")
        print(f"Diameter:            {TESTUR_REF.diameter} mm")
        print(f"Number of discs:     {TESTUR_REF.num_discs}")
        print(f"Verified power:      {TESTUR_REF.power_verified} W @ {TESTUR_REF.rpm_operating} RPM")
        print(f"Pressure ratio:      {TESTUR_REF.pressure_ratio}:1")
        print(f"Source:              {TESTUR_REF.source}")

    print(f"\n{'='*70}\n")


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("TESLA TURBINE DESIGN MODULE - Testing")
    print("="*70)

    # Test 1: R1233zd(E)
    print("\n### Test 1: R1233zd(E) @ 50°C ###")
    mu_r1233 = 12.1  # μPa·s
    pr_r1233 = 2.71
    design_r1233 = design_tesla_turbine('R1233zd(E)', mu_r1233, pr_r1233, 1.0)
    print_turbine_design(design_r1233)

    # Test 2: R245fa
    print("\n### Test 2: R245fa @ 50°C ###")
    mu_r245 = 12.9  # μPa·s
    pr_r245 = 2.80
    design_r245 = design_tesla_turbine('R245fa', mu_r245, pr_r245, 1.0)
    print_turbine_design(design_r245, show_testur=False)

    # Test 3: Isopentane (lower viscosity)
    print("\n### Test 3: Isopentane @ 50°C ###")
    mu_isopentane = 7.6  # μPa·s
    pr_isopentane = 2.06
    design_iso = design_tesla_turbine('Isopentane', mu_isopentane, pr_isopentane, 1.0)
    print_turbine_design(design_iso, show_testur=False)

    # Comparison table
    print("\n" + "="*90)
    print("TURBINE DESIGN COMPARISON")
    print("="*90)
    print(f"{'Fluid':<15} {'μ [μPa·s]':<12} {'b [mm]':<10} {'Scaling':<10} {'Est. RPM':<12}")
    print("="*90)

    designs = [design_r1233, design_r245, design_iso]
    for d in designs:
        print(f"{d.fluid:<15} {d.viscosity_fluid:<12.1f} {d.disc_spacing:<10.3f} "
              f"{d.viscosity_scaling:<10.3f} {d.estimated_rpm:<12}")

    print("="*90 + "\n")

    # Critical recommendations
    print("="*70)
    print("CRITICAL DESIGN RECOMMENDATIONS")
    print("="*70)
    print("\n1. DISC SPACING")
    print(f"   R1233zd(E):  {design_r1233.disc_spacing:.3f} mm (recommended starting point)")
    print(f"   Tolerance:   ±{(design_r1233.disc_spacing*0.05):.3f} mm for manufacturing")
    print(f"   TesTur ref:  {TESTUR_REF.disc_spacing} mm (air)")

    print("\n2. MANUFACTURING")
    print(f"   - Material: 316L stainless steel")
    print(f"   - Process: Laser cutting or water jet")
    print(f"   - Tolerance: ±0.01 mm critical for disc spacing")
    print(f"   - Surface finish: Ra < 0.8 μm")

    print("\n3. ASSEMBLY")
    print(f"   - Dynamic balancing required at {design_r1233.estimated_rpm} RPM")
    print(f"   - Shaft alignment critical (< 0.02 mm runout)")
    print(f"   - Use precision spacers for disc separation")

    print("\n4. TESTING SEQUENCE")
    print(f"   - Step 1: Air test @ 3-5 bar (like TesTur)")
    print(f"   - Step 2: Low-pressure ORC test @ 1-2 bar")
    print(f"   - Step 3: Full-power ORC test @ design pressure")

    print("\n" + "="*70)
    print(f"Based on: {TESTUR_REF.source}")
    print("="*70 + "\n")
