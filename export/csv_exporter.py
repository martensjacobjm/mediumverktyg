#!/usr/bin/env python3
"""
CSV Exporter - Export fluid data to CSV format
For Excel and further analysis
"""

import csv
from typing import List
from core.scoring import FluidScore


class CSVExporter:
    """Export fluid scores to CSV format"""

    def __init__(self):
        pass

    def export_scores(self, scores: List[FluidScore], filename: str):
        """
        Export list of FluidScore objects to CSV

        Args:
            scores: List of FluidScore objects
            filename: Output CSV filename
        """

        # Define CSV columns
        fieldnames = [
            'Rank',
            'Fluid',
            'Total Score',
            'Thermo Score',
            'Env Score',
            'Safety Score',
            'Econ Score',
            'GWP',
            'ODP',
            'ASHRAE Class',
            'Flammable',
            'Toxic',
            'Pressure @ 50°C [bar]',
            'hfg @ 50°C [kJ/kg]',
            'Viscosity @ 50°C [μPa·s]',
            'Pressure Ratio',
            'ORC Suitability'
        ]

        # Write CSV
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write data rows
            for score in scores:
                row = {
                    'Rank': score.rank or '',
                    'Fluid': score.fluid,
                    'Total Score': f"{score.total_score:.1f}",
                    'Thermo Score': f"{score.thermo_score:.1f}",
                    'Env Score': f"{score.env_score:.1f}",
                    'Safety Score': f"{score.safety_score:.1f}",
                    'Econ Score': f"{score.econ_score:.1f}",
                    'GWP': score.gwp if score.gwp is not None else '',
                    'ODP': score.odp if score.odp is not None else '',
                    'ASHRAE Class': score.ashrae_class or '',
                    'Flammable': '',  # Would need to get from metadata
                    'Toxic': '',      # Would need to get from metadata
                    'Pressure @ 50°C [bar]': f"{score.pressure_50C:.2f}" if score.pressure_50C else '',
                    'hfg @ 50°C [kJ/kg]': f"{score.hfg_50C:.1f}" if score.hfg_50C else '',
                    'Viscosity @ 50°C [μPa·s]': f"{score.viscosity_50C:.1f}" if score.viscosity_50C else '',
                    'Pressure Ratio': f"{score.pressure_ratio:.2f}" if score.pressure_ratio else '',
                    'ORC Suitability': score.orc_suitability or ''
                }

                writer.writerow(row)

        print(f"✓ Exported {len(scores)} fluids to {filename}")
        return filename

    def export_detailed_comparison(self, fluids: List[str], db, calc, filename: str):
        """
        Export detailed comparison of selected fluids

        Args:
            fluids: List of fluid names
            db: FluidDatabase instance
            calc: ThermodynamicCalculator instance
            filename: Output CSV filename
        """

        # Temperature range for properties
        temps = list(range(10, 81, 5))

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow(['Temperature [°C]'] + [f'{fluid} - P [bar]' for fluid in fluids] +
                          [f'{fluid} - hfg [kJ/kg]' for fluid in fluids] +
                          [f'{fluid} - μ [μPa·s]' for fluid in fluids] +
                          [f'{fluid} - ρ_vap [kg/m³]' for fluid in fluids])

            # Data rows
            for T in temps:
                row = [T]

                # Pressure for all fluids
                for fluid in fluids:
                    props = db.get_saturation_properties(fluid, T)
                    row.append(f"{props.pressure:.2f}" if props else '')

                # hfg for all fluids
                for fluid in fluids:
                    props = db.get_saturation_properties(fluid, T)
                    row.append(f"{props.hfg:.1f}" if props else '')

                # Viscosity for all fluids
                for fluid in fluids:
                    props = db.get_saturation_properties(fluid, T)
                    row.append(f"{props.mu_vapor:.1f}" if props else '')

                # Density for all fluids
                for fluid in fluids:
                    props = db.get_saturation_properties(fluid, T)
                    row.append(f"{props.rho_vapor:.2f}" if props else '')

                writer.writerow(row)

        print(f"✓ Exported detailed comparison to {filename}")
        return filename


# Test
if __name__ == "__main__":
    from core.scoring import FluidScorer

    print("="*70)
    print("CSV EXPORTER - Testing")
    print("="*70)

    # Create test data
    scorer = FluidScorer(T_hot=50, T_cold=20)
    scores = scorer.rank_fluids()

    # Export top 20
    exporter = CSVExporter()
    exporter.export_scores(scores[:20], 'test_export_top20.csv')

    print("\n✓ Test completed. Check test_export_top20.csv")
