#!/usr/bin/env python3
"""
Fluid Scoring and Ranking Algorithm
Weighted scoring based on thermodynamic, environmental, safety, and economic criteria
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from core.fluid_database import FluidDatabase, FluidMetadata
from core.thermodynamics import ThermodynamicCalculator, ORCSystemResults


@dataclass
class ScoringWeights:
    """Weights for different scoring categories (must sum to 1.0)"""
    thermodynamic: float = 0.40  # 40% - Performance matters most
    environmental: float = 0.30  # 30% - Sustainability important
    safety: float = 0.20  # 20% - Critical for home/small installations
    economic: float = 0.10  # 10% - Cost is a factor but not primary

    def __post_init__(self):
        total = self.thermodynamic + self.environmental + self.safety + self.economic
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")


@dataclass
class FluidScore:
    """Detailed score breakdown for a fluid"""
    fluid: str

    # Individual category scores (0-100)
    thermo_score: float
    env_score: float
    safety_score: float
    econ_score: float

    # Total weighted score (0-100)
    total_score: float

    # Thermodynamic details
    pressure_50C: Optional[float] = None
    hfg_50C: Optional[float] = None
    viscosity_50C: Optional[float] = None
    pressure_ratio: Optional[float] = None
    efficiency: Optional[float] = None

    # Metadata
    gwp: Optional[int] = None
    odp: Optional[float] = None
    ashrae_class: Optional[str] = None
    orc_suitability: Optional[str] = None
    T_boiling_1atm: Optional[float] = None  # Boiling point @ 1 atm [°C]

    # Ranking
    rank: Optional[int] = None


class FluidScorer:
    """Main class for scoring and ranking fluids"""

    def __init__(self,
                 weights: Optional[ScoringWeights] = None,
                 T_hot: float = 50.0,
                 T_cold: float = 20.0):
        """
        Initialize scorer

        Args:
            weights: Custom scoring weights (uses defaults if None)
            T_hot: Hot side temperature for evaluation [°C]
            T_cold: Cold side temperature for evaluation [°C]
        """
        self.weights = weights or ScoringWeights()
        self.T_hot = T_hot
        self.T_cold = T_cold

        self.db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')
        self.calc = ThermodynamicCalculator()

    def score_thermodynamic(self, fluid: str) -> tuple:
        """
        Score thermodynamic performance (0-100)

        Sub-scores:
        - Latent heat (hfg): Higher is better (40%)
        - Pressure ratio: Optimal 2.0-3.0 (30%)
        - Pressure level @ T_hot: Optimal 2-8 bar (30%)

        Returns:
            (score, details_dict)
        """
        props_hot = self.db.get_saturation_properties(fluid, self.T_hot)
        props_cold = self.db.get_saturation_properties(fluid, self.T_cold)

        if not props_hot or not props_cold:
            return 0.0, {}

        # Latent heat score (40 points max)
        # Optimal: > 150 kJ/kg
        hfg = props_hot.hfg
        hfg_score = min(40, (hfg / 150) * 40)

        # Pressure ratio score (30 points max)
        # Optimal: 2.0-3.0 for low-temp ORC
        pr = props_hot.pressure / props_cold.pressure
        if 2.0 <= pr <= 3.0:
            pr_score = 30
        else:
            # Penalize deviation
            deviation = min(abs(pr - 2.5), 2.5)
            pr_score = max(0, 30 * (1 - deviation / 2.5))

        # Pressure level score (30 points max)
        # Optimal: 2-8 bar @ T_hot (safe and practical)
        p_hot = props_hot.pressure
        if 2.0 <= p_hot <= 8.0:
            p_score = 30
        elif p_hot < 2.0:
            # Too low pressure (vacuum issues)
            p_score = max(0, 30 * (p_hot / 2.0))
        else:
            # Too high pressure (safety concerns)
            p_score = max(0, 30 * (1 - (p_hot - 8.0) / 20.0))

        total = hfg_score + pr_score + p_score

        details = {
            'hfg': hfg,
            'pressure_ratio': pr,
            'p_hot': p_hot,
            'p_cold': props_cold.pressure,
            'viscosity': props_hot.mu_vapor
        }

        return total, details

    def score_environmental(self, fluid: str) -> tuple:
        """
        Score environmental impact (0-100)

        Sub-scores:
        - GWP: Lower is better (70%)
        - ODP: Must be 0 (30%)

        Returns:
            (score, details_dict)
        """
        meta = self.db.get_metadata(fluid)
        if not meta:
            return 50.0, {}  # Default middle score if no data

        # GWP score (70 points max)
        # Excellent: GWP < 10
        # Good: GWP < 100
        # Moderate: GWP < 500
        # Poor: GWP > 1000
        gwp = meta.gwp
        if gwp < 10:
            gwp_score = 70
        elif gwp < 100:
            gwp_score = 70 * (1 - (gwp - 10) / 90)
        elif gwp < 500:
            gwp_score = 40 * (1 - (gwp - 100) / 400)
        elif gwp < 2000:
            gwp_score = 20 * (1 - (gwp - 500) / 1500)
        else:
            gwp_score = 0

        # ODP score (30 points max)
        # Must be 0 for modern fluids
        odp = meta.odp
        if odp == 0:
            odp_score = 30
        elif odp < 0.01:
            odp_score = 20
        elif odp < 0.05:
            odp_score = 10
        else:
            odp_score = 0  # BANNED

        total = gwp_score + odp_score

        details = {
            'gwp': gwp,
            'odp': odp
        }

        return total, details

    def score_safety(self, fluid: str) -> tuple:
        """
        Score safety (0-100)

        Sub-scores:
        - ASHRAE class: A1 best, B2L worst (70%)
        - Flammability: Penalize flammable (30%)

        Returns:
            (score, details_dict)
        """
        meta = self.db.get_metadata(fluid)
        if not meta:
            return 50.0, {}

        # ASHRAE class score (70 points max)
        ashrae_scores = {
            'A1': 70,    # Non-toxic, non-flammable
            'A2L': 60,   # Non-toxic, mildly flammable
            'A2': 50,    # Non-toxic, flammable
            'A3': 30,    # Non-toxic, highly flammable
            'B1': 50,    # Toxic, non-flammable
            'B2L': 40,   # Toxic, mildly flammable
            'B2': 30,    # Toxic, flammable
            'B3': 10,    # Toxic, highly flammable
            'Unknown': 30
        }
        ashrae_score = ashrae_scores.get(meta.ashrae_class, 30)

        # Flammability penalty (30 points max for non-flammable)
        if not meta.flammable:
            flam_score = 30
        else:
            flam_score = 10  # Significant penalty for flammability

        total = ashrae_score + flam_score

        details = {
            'ashrae_class': meta.ashrae_class,
            'flammable': meta.flammable,
            'toxic': meta.toxic
        }

        return total, details

    def score_economic(self, fluid: str) -> tuple:
        """
        Score economic factors (0-100)

        Sub-scores:
        - Cost: Lower is better (50%)
        - Availability: Higher is better (50%)

        Returns:
            (score, details_dict)
        """
        meta = self.db.get_metadata(fluid)
        if not meta:
            return 50.0, {}

        # Cost score (50 points max)
        # Lower cost_index is better (relative to R245fa = 1.0)
        cost_idx = meta.cost_index
        if cost_idx <= 0.5:
            cost_score = 50
        elif cost_idx <= 1.0:
            cost_score = 50 * (1 - (cost_idx - 0.5) / 0.5) + 25
        elif cost_idx <= 2.0:
            cost_score = 25 * (1 - (cost_idx - 1.0) / 1.0)
        else:
            cost_score = max(0, 10 * (1 - (cost_idx - 2.0) / 2.0))

        # Availability score (50 points max)
        avail_scores = {
            'EXCELLENT': 50,
            'GOOD': 40,
            'MODERATE': 25,
            'LIMITED': 10,
            'UNKNOWN': 20
        }
        avail_score = avail_scores.get(meta.availability, 20)

        total = cost_score + avail_score

        details = {
            'cost_index': cost_idx,
            'availability': meta.availability
        }

        return total, details

    def score_fluid(self, fluid: str) -> FluidScore:
        """
        Calculate total score for a fluid

        Returns:
            FluidScore object with complete breakdown
        """
        # Calculate individual category scores
        thermo_score, thermo_details = self.score_thermodynamic(fluid)
        env_score, env_details = self.score_environmental(fluid)
        safety_score, safety_details = self.score_safety(fluid)
        econ_score, econ_details = self.score_economic(fluid)

        # Calculate weighted total
        total_score = (
            thermo_score * self.weights.thermodynamic +
            env_score * self.weights.environmental +
            safety_score * self.weights.safety +
            econ_score * self.weights.economic
        )

        # Get metadata
        meta = self.db.get_metadata(fluid)

        return FluidScore(
            fluid=fluid,
            thermo_score=thermo_score,
            env_score=env_score,
            safety_score=safety_score,
            econ_score=econ_score,
            total_score=total_score,
            # Thermo details
            pressure_50C=thermo_details.get('p_hot'),
            hfg_50C=thermo_details.get('hfg'),
            viscosity_50C=thermo_details.get('viscosity'),
            pressure_ratio=thermo_details.get('pressure_ratio'),
            # Metadata
            gwp=env_details.get('gwp'),
            odp=env_details.get('odp'),
            ashrae_class=safety_details.get('ashrae_class'),
            orc_suitability=meta.orc_suitability if meta else None,
            T_boiling_1atm=meta.T_boiling_1atm if meta else None
        )

    def rank_fluids(self, fluids: Optional[List[str]] = None) -> List[FluidScore]:
        """
        Rank all fluids or a subset

        Args:
            fluids: List of fluid names (uses all if None)

        Returns:
            List of FluidScore objects sorted by total_score (highest first)
        """
        if fluids is None:
            fluids = self.db.get_all_fluids()

        scores = []
        for fluid in fluids:
            try:
                score = self.score_fluid(fluid)
                scores.append(score)
            except Exception as e:
                print(f"Warning: Could not score {fluid}: {e}")

        # Sort by total score (highest first)
        scores.sort(key=lambda x: x.total_score, reverse=True)

        # Assign ranks
        for i, score in enumerate(scores, 1):
            score.rank = i

        return scores

    def print_rankings(self, scores: List[FluidScore], top_n: int = 20):
        """Pretty print rankings"""

        print(f"\n{'='*100}")
        print(f"FLUID RANKINGS - Top {min(top_n, len(scores))}")
        print(f"Evaluation: {self.T_hot}°C → {self.T_cold}°C")
        print(f"Weights: Thermo {self.weights.thermodynamic:.0%}, Env {self.weights.environmental:.0%}, "
              f"Safety {self.weights.safety:.0%}, Econ {self.weights.economic:.0%}")
        print(f"{'='*100}")

        print(f"\n{'Rank':<6} {'Fluid':<15} {'Total':<8} {'Thermo':<8} {'Env':<8} {'Safety':<8} "
              f"{'Econ':<8} {'GWP':<8} {'Class':<8}")
        print(f"{'-'*100}")

        for score in scores[:top_n]:
            stars = '⭐' * min(5, int(score.total_score / 20) + 1)

            print(f"{score.rank:<6} {score.fluid:<15} {score.total_score:<8.1f} "
                  f"{score.thermo_score:<8.1f} {score.env_score:<8.1f} {score.safety_score:<8.1f} "
                  f"{score.econ_score:<8.1f} {score.gwp or 0:<8} {score.ashrae_class or 'N/A':<8} {stars}")

        print(f"{'='*100}\n")


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("FLUID SCORING SYSTEM - Testing")
    print("="*70)

    # Initialize scorer with default weights
    scorer = FluidScorer(T_hot=50, T_cold=20)

    # Rank all fluids
    print("\n### Ranking all ORC fluids ###")
    rankings = scorer.rank_fluids()

    # Print top 20
    scorer.print_rankings(rankings, top_n=20)

    # Detailed breakdown for top 3
    print("\n" + "="*70)
    print("DETAILED SCORE BREAKDOWN - Top 3")
    print("="*70)

    for i, score in enumerate(rankings[:3], 1):
        print(f"\n### {i}. {score.fluid} (Total: {score.total_score:.1f}/100) ###")
        print(f"\n  Thermodynamic: {score.thermo_score:.1f}/100 (weight {scorer.weights.thermodynamic:.0%})")
        print(f"    - Latent heat: {score.hfg_50C:.1f} kJ/kg")
        print(f"    - Pressure @ 50°C: {score.pressure_50C:.2f} bar")
        print(f"    - Pressure ratio: {score.pressure_ratio:.2f}:1")

        print(f"\n  Environmental: {score.env_score:.1f}/100 (weight {scorer.weights.environmental:.0%})")
        print(f"    - GWP: {score.gwp}")
        print(f"    - ODP: {score.odp}")

        print(f"\n  Safety: {score.safety_score:.1f}/100 (weight {scorer.weights.safety:.0%})")
        print(f"    - ASHRAE class: {score.ashrae_class}")

        print(f"\n  Economic: {score.econ_score:.1f}/100 (weight {scorer.weights.economic:.0%})")
        print(f"    - ORC suitability: {score.orc_suitability}")

    print("\n" + "="*70 + "\n")
