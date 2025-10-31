# Dynamic ORC Working Fluid Analysis Tool

**Status:** Core modules implemented ✅
**Next:** GUI implementation
**Version:** 0.5.0

## Project Overview

Python-based interactive tool for comparing and analyzing 79+ working fluids for Tesla turbine ORC systems.

### Features Implemented

✅ **Core Modules:**
- `core/fluid_database.py` - CoolProp integration for 79 fluids with metadata
- `core/thermodynamics.py` - Complete ORC cycle calculations
- `core/tesla_turbine.py` - TesTur-validated turbine design
- `core/scoring.py` - Weighted ranking algorithm

✅ **Data:**
- Automatic thermodynamic property retrieval from CoolProp
- Manual metadata for 30+ key fluids (GWP, safety, cost)
- TesTur reference data for validation

### Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Test core modules
python3 -m core.fluid_database
python3 -m core.thermodynamics
python3 -m core.tesla_turbine
python3 -m core.scoring
```

### Top Ranked Fluids (50°C → 20°C)

| Rank | Fluid | Total Score | GWP | Safety | Notes |
|------|-------|-------------|-----|--------|-------|
| 1 | R1233zd(E) | 96.4 | 7 | A1 | ⭐⭐⭐⭐⭐ Best overall |
| 2 | R1234ze(E) | 88.4 | 6 | A2L | ⭐⭐⭐⭐⭐ Slightly flammable |
| 3 | IsoButane | 88.0 | 3 | A3 | ⭐⭐⭐⭐⭐ Flammable, cheap |
| 4 | n-Butane | 88.0 | 4 | A3 | ⭐⭐⭐⭐⭐ Flammable, cheap |
| 5 | Isopentane | 87.0 | 5 | A3 | ⭐⭐⭐⭐⭐ Flammable, excellent ORC |

### Validated Results

**R1233zd(E) @ 50°C → 20°C, 1 kW:**
- Pressure: 2.93 bar (✓ matches legacy code)
- Viscosity: 12.1 μPa·s (✓ matches legacy code)
- Disc spacing: 0.191 mm (✓ TesTur-scaled)
- System efficiency: 51.02% (✓ matches legacy code)

### Next Steps

1. **GUI Implementation** (in progress)
   - Main window with filter panel
   - Results list with sorting
   - Dynamic matplotlib plots

2. **Export Functions** (pending)
   - PDF report generation
   - PNG diagram export
   - CSV data export

3. **Testing** (pending)
   - Unit tests for all modules
   - Integration tests
   - User acceptance testing

### Architecture

```
mediumverktyg/
├── core/                  # Core calculation modules ✅
│   ├── fluid_database.py  # CoolProp integration
│   ├── thermodynamics.py  # ORC calculations
│   ├── tesla_turbine.py   # Turbine design
│   └── scoring.py         # Ranking algorithm
├── gui/                   # GUI (next step)
├── export/                # Export functions (next step)
├── data/                  # Metadata ✅
└── tests/                 # Unit tests (next step)
```

### Scoring Algorithm

Weighted scoring (0-100 scale):
- **Thermodynamic (40%):** Latent heat, pressure ratio, pressure level
- **Environmental (30%):** GWP, ODP
- **Safety (20%):** ASHRAE class, flammability
- **Economic (10%):** Cost, availability

### Development Timeline

- ✅ Week 1: Project structure, core modules, data
- 🔄 Week 2: GUI, visualization (current)
- ⏳ Week 3: Export, testing, documentation

### References

- CoolProp 7.1.0 thermodynamic database
- TesTur experimental data (Video K7qZvq1CMFg)
- ASHRAE safety classification standards
- Legacy orc_kalkylator_enhanced.py validation

---

**Author:** Automated development
**Date:** 2025-10-31
**License:** MIT
