# ARBETSPLAN: DYNAMISKT ARBETSMEDIUMVERKTYG FÖR TESLA-TURBIN ORC

**Skapad:** 2025-10-31
**Projekt:** Interaktivt GUI-verktyg för ORC-mediumjämförelse
**Omfattning:** 130+ arbetsmedier från CoolProp med avancerad filtrering och visualisering

---

## INNEHÅLLSFÖRTECKNING

1. [Executive Summary](#1-executive-summary)
2. [Analys av befintlig kod](#2-analys-av-befintlig-kod)
3. [Systemarkitektur](#3-systemarkitektur)
4. [Implementationsplan](#4-implementationsplan)
5. [Tekniska specifikationer](#5-tekniska-specifikationer)
6. [Tidsplan och milstolpar](#6-tidsplan-och-milstolpar)
7. [Testplan](#7-testplan)
8. [Riskhantering](#8-riskhantering)

---

## 1. EXECUTIVE SUMMARY

### 1.1 Projektmål

Utveckla ett **professionellt Python-baserat GUI-verktyg** som:
- Stödjer **alla 130+ arbetsmedier** från CoolProp-databasen
- Ger **realtidsfiltrering och sortering** baserat på termodynamiska egenskaper, miljöpåverkan och säkerhet
- Genererar **dynamiska diagram** som uppdateras automatiskt vid användarval
- Exporterar **professionella rapporter** (PDF med alla beräkningar, PNG-diagram, CSV-rådata)
- Använder **korrekta tillståndsekvationer** (Peng-Robinson/Redlich-Kwong via CoolProp)
- Integrerar **TesTur-validering** för Tesla-turbinspecifika beräkningar

### 1.2 Nuvarande tillstånd

**Befintliga resurser (bra grund att bygga på):**
```
✓ orc_kalkylator.py              - Grundläggande termodynamiska beräkningar
✓ orc_kalkylator_enhanced.py     - TesTur-validering och diskavståndsberäkning
✓ orc_termo_data.py              - CoolProp-integration för datahämtning
✓ orc_visualisering.py           - Matplotlib-baserade plottar
✓ generate_rapport.py            - Rapportgenerering (grund)
✓ ARBETSBESKRIVNING_KOMPLETT.md  - Detaljerad kravspecifikation
```

**Begränsningar att åtgärda:**
```
✗ Endast 2 medier stöds (R245fa, R1233zd(E))
✗ Ingen interaktiv GUI - endast kommandorad
✗ Statiska scenarion - användaren kan inte ändra parametrar
✗ Ingen filtrering eller sortering
✗ Grundläggande visualisering utan realtidsuppdatering
✗ Ingen strukturerad databas för mediametadata
```

### 1.3 Målbild

```
┌─────────────────────────────────────────────────────────┐
│  🎯 DYNAMISKT ORC ARBETSMEDIUMVERKTYG                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Filtrera Medier]  [Sortera]  [Jämför]  [Exportera]   │
│                                                          │
│  ┌──────────────┬────────────────────────────────────┐ │
│  │ FILTER PANEL │  RESULTAT (130+ medier)           │ │
│  │              │                                     │ │
│  │ Kokpunkt:    │  1. R1233zd(E)  ⭐⭐⭐⭐⭐         │ │
│  │  [10-30°C]   │     Kokp: 19°C  GWP:7  A1         │ │
│  │              │                                     │ │
│  │ GWP:         │  2. R245fa      ⭐⭐⭐⭐           │ │
│  │  [< 100]     │     Kokp: 15°C  GWP:1030  B1      │ │
│  │              │                                     │ │
│  │ Säkerhet:    │  3. R1234ze(Z)  ⭐⭐⭐⭐⭐         │ │
│  │  [✓ A1/A2L]  │     Kokp: 9°C   GWP:1   A2L       │ │
│  │              │                                     │ │
│  │ Tryck @50°C: │  ... 127 more fluids ...          │ │
│  │  [2-8 bar]   │                                     │ │
│  └──────────────┴────────────────────────────────────┘ │
│                                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │  DIAGRAM: Tryck-Temperatur (Val: 3 medier)       │ │
│  │                                                    │ │
│  │  [Dynamisk matplotlib-plot uppdateras live]      │ │
│  │                                                    │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  [📄 Exportera PDF Rapport] [📊 PNG Diagram] [📊 CSV]  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. ANALYS AV BEFINTLIG KOD

### 2.1 Befintliga moduler och deras värde

#### 2.1.1 `orc_kalkylator_enhanced.py` ⭐⭐⭐⭐⭐
**Status:** Utmärkt grund - återanvänd 90%

**Styrkor:**
```python
✓ Välstrukturerad get_props() funktion för termodynamisk data
✓ calc_system_enhanced() - komplett ORC-beräkningsmotor
✓ calc_disc_spacing() - TesTur-validerad diskavståndsskalning
✓ TESTUR_REF dictionary - viktig referensdata
✓ Korrekt användning av CoolProp.PropsSI()
```

**Hur vi återanvänder:**
```
→ Extrahera till `core/thermodynamics.py`
→ Generalisera till stödja alla medier (inte bara R1233zd(E))
→ Lägg till caching för prestanda (LRU cache)
→ Implementera felhantering för medier utan fullständiga data
```

#### 2.1.2 `orc_termo_data.py` ⭐⭐⭐⭐
**Status:** Bra struktur - behöver utökas

**Styrkor:**
```python
✓ get_saturated_properties() - robust datahämtning
✓ Korrekt felhantering (try/except)
✓ Riktiga enhetskonverteringar
```

**Förbättringar:**
```
→ Utöka till alla 130+ medier
→ Lägg till metadata (GWP, säkerhet, kostnad)
→ Implementera bulk-datahämtning för snabbare laddning
→ Spara cache till JSON för snabbare restart
```

#### 2.1.3 `orc_visualisering.py` ⭐⭐⭐
**Status:** Grundläggande - behöver modernisering

**Styrkor:**
```python
✓ Grundläggande matplotlib-integration
✓ 4-panel layout är pedagogisk
```

**Begränsningar:**
```
✗ Statiska plottar - ingen interaktivitet
✗ Hårdkodad för 2 medier
✗ Ingen realtidsuppdatering
```

**Modernisering:**
```
→ Implementera dynamisk plottning med matplotlib FigureCanvasTkAgg
→ Stöd för N medier (användaren väljer)
→ Interaktiva tooltips (mplcursors)
→ Exportknapp direkt i GUI
```

#### 2.1.4 `generate_rapport.py` ⭐⭐
**Status:** Behöver omskrivning - grundkoncept OK

**Förbättringar:**
```
→ Använd ReportLab istället för FPDF för bättre UTF-8-stöd
→ Professionell mall med logotyp och sidfot
→ Inkludera alla beräkningar + metadata
→ Automatisk innehållsförteckning
→ Högkvalitativa vektorgrafik (matplotlib → PDF)
```

### 2.2 Metadata som saknas (måste skapas)

För att stödja 130+ medier behöver vi skapa en **komplett metadatadatabas**:

```python
# data/fluid_metadata.json
{
    "R1233zd(E)": {
        "fullname": "1-Chloro-3,3,3-trifluoroprop-1-ene",
        "formula": "CHCl=CHCF3",
        "coolprop_name": "R1233zd(E)",
        "molar_mass": 130.5,
        "ashrae_class": "A1",
        "gwp": 7,
        "odp": 0,
        "boiling_point_1atm": 19.0,
        "critical_temp": 165.6,
        "critical_pressure": 35.73,
        "category": "HFO",
        "orc_suitability": "EXCELLENT",
        "cost_index": 1.03,
        "availability": "GOOD",
        "safety_notes": "Non-flammable, non-toxic, safest for home installation",
        "environmental_rating": "A+",
        "commercial_status": "Available"
    },
    // ... 129 more fluids
}
```

**Strategi för att skapa denna data:**
1. Hämta termodynamiska egenskaper automatiskt från CoolProp
2. Komplettera med manuell metadata (GWP, säkerhet) från ASHRAE/EPA-databaser
3. Beräkna ORC-lämplighet med viktad poängalgoritm

---

## 3. SYSTEMARKITEKTUR

### 3.1 Modulmapp-struktur

```
mediumverktyg/
│
├── main.py                          # Startfil för GUI
├── requirements.txt                 # Python-beroenden
├── setup.py                         # Installation script
│
├── core/                            # Kärnfunktionalitet
│   ├── __init__.py
│   ├── thermodynamics.py           # CoolProp-beräkningar (från orc_kalkylator_enhanced.py)
│   ├── fluid_database.py           # Mediumdatabas och metadata
│   ├── calculations.py             # ORC-specifika beräkningar
│   ├── tesla_turbine.py            # Tesla-turbin dimensionering (diskavstånd etc)
│   └── scoring.py                  # Poängalgoritm för mediumranking
│
├── gui/                             # Grafiskt gränssnitt
│   ├── __init__.py
│   ├── main_window.py              # Huvudfönster (tkinter/PyQt5)
│   ├── filter_panel.py             # Filterkomponent
│   ├── results_panel.py            # Resultatlista med sortering
│   ├── plot_panel.py               # Dynamiska matplotlib-diagram
│   ├── comparison_panel.py         # Sidovid-jämförelse (upp till 5 medier)
│   └── dialogs.py                  # Exportdialog, inställningar etc
│
├── export/                          # Exportfunktioner
│   ├── __init__.py
│   ├── pdf_generator.py            # Professionella PDF-rapporter (ReportLab)
│   ├── plot_exporter.py            # PNG/SVG-export av diagram
│   └── csv_exporter.py             # CSV-data för Excel-import
│
├── data/                            # Statisk data och cache
│   ├── fluid_metadata.json         # Manuell metadata (GWP, säkerhet etc)
│   ├── coolprop_cache.json         # Cachad termodynamisk data
│   └── testur_reference.json       # TesTur-referensdata
│
├── tests/                           # Enhetstester
│   ├── test_thermodynamics.py
│   ├── test_database.py
│   ├── test_calculations.py
│   └── test_export.py
│
├── docs/                            # Dokumentation
│   ├── USER_GUIDE.md               # Användarhandledning
│   ├── API_REFERENCE.md            # API-dokumentation
│   └── THEORY.md                   # Termodynamisk teori
│
├── legacy/                          # Gamla filer (för referens)
│   ├── orc_kalkylator.py
│   ├── orc_kalkylator_enhanced.py
│   └── ...
│
└── assets/                          # Bilder, ikoner
    ├── logo.png
    └── icons/
```

### 3.2 Dataflöde

```
┌──────────────┐
│   USER GUI   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  FILTER & SORTING ENGINE                 │
│  - Kokpunkt: 10-30°C                     │
│  - GWP: < 100                            │
│  - Säkerhet: A1/A2L                      │
│  → Returnerar: 15 matchande medier       │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  FLUID DATABASE                          │
│  - Läser fluid_metadata.json             │
│  - Kolla CoolProp cache                  │
│  - Hämta ny data vid behov               │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  THERMODYNAMIC CALCULATIONS (CoolProp)   │
│  - PropsSI('P', 'T', 323.15, 'Q', 1, fl) │
│  - Beräkna hfg, μ, ρ, s, h               │
│  - Använd Peng-Robinson/Redlich-Kwong    │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  ORC SYSTEM CALCULATIONS                 │
│  - Massflöde m_dot                       │
│  - Värmeväxlare Q_evap, Q_cond           │
│  - Pumpeffekt P_pump                     │
│  - Tesla-turbin diskavstånd b            │
│  - Systemverkningsgrad η                 │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  SCORING ALGORITHM                       │
│  - Totalpoäng: viktad summa              │
│  - Termo: 40%, Miljö: 30%, Säkerhet: 20%│
│  - Ekonomi: 10%                          │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  DISPLAY & VISUALIZATION                 │
│  - Sorterad lista med stjärnbetyg        │
│  - Dynamiska matplotlib-plottar          │
│  - Realtidsuppdatering vid filterändring │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  EXPORT MODULE                           │
│  - PDF: Professionell rapport (ReportLab)│
│  - PNG: Högupplösta diagram (300 DPI)   │
│  - CSV: Rådata för Excel                │
└──────────────────────────────────────────┘
```

### 3.3 Teknologival

| Komponent | Teknologi | Motivering |
|-----------|-----------|------------|
| **GUI Framework** | **tkinter** (alt PyQt5) | Tkinter: Inbyggd i Python, snabb prototyping<br>PyQt5: Mer professionell, bättre för stora projekt |
| **Termodynamik** | **CoolProp** 6.6+ | Industristandard, 130+ fluider, exakta EoS |
| **Plotting** | **matplotlib** 3.5+ | Flexibel, PDF-vänlig, många plottyper |
| **PDF-generering** | **ReportLab** 4.0+ | Professionell kvalitet, bra dokumentation |
| **Datahantering** | **pandas** 2.0+ | Effektiv filtrering och sortering |
| **Datalagring** | **JSON** | Läsbar, versionshanterbar, enkel parsing |
| **Cache** | **functools.lru_cache** | Inbyggd, snabb, ingen extra dependency |

---

## 4. IMPLEMENTATIONSPLAN

### FAS 1: GRUND OCH DATABAS (Vecka 1)

#### Mål:
- Installera alla dependencies
- Skapa modulmappsstruktur
- Implementera grundläggande CoolProp-integration
- Skapa metadata-databas för alla 130+ medier

#### Tasks:

**1.1 Setup miljö**
```bash
# requirements.txt
CoolProp>=6.6.0
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=2.0.0
reportlab>=4.0.0
tk>=8.6
```

**1.2 Skapa `core/fluid_database.py`**
```python
import CoolProp.CoolProp as CP
import json
from functools import lru_cache

class FluidDatabase:
    def __init__(self):
        self.all_fluids = self._get_coolprop_fluids()
        self.metadata = self._load_metadata()

    def _get_coolprop_fluids(self):
        """Hämtar alla tillgängliga medier från CoolProp"""
        all_fluids = CP.FluidsList()
        # Filtrera bort olämpliga (t.ex. luft, helium för ORC)
        orc_candidates = [f for f in all_fluids if self._is_orc_candidate(f)]
        return orc_candidates

    def _is_orc_candidate(self, fluid):
        """Kontrollerar om ett medium är lämpligt för ORC"""
        try:
            T_crit = CP.PropsSI('Tcrit', fluid) - 273.15
            p_crit = CP.PropsSI('pcrit', fluid) / 1e5
            # ORC-kriterier: T_crit > 100°C, p_crit < 100 bar
            return T_crit > 100 and p_crit < 100
        except:
            return False

    @lru_cache(maxsize=1000)
    def get_properties(self, fluid, T_celsius):
        """Hämtar termodynamiska egenskaper med caching"""
        T = T_celsius + 273.15
        try:
            return {
                'p': CP.PropsSI('P', 'T', T, 'Q', 1, fluid) / 1e5,
                'h_vap': CP.PropsSI('H', 'T', T, 'Q', 1, fluid) / 1000,
                'h_liq': CP.PropsSI('H', 'T', T, 'Q', 0, fluid) / 1000,
                'rho_vap': CP.PropsSI('D', 'T', T, 'Q', 1, fluid),
                'rho_liq': CP.PropsSI('D', 'T', T, 'Q', 0, fluid),
                'mu_vap': CP.PropsSI('V', 'T', T, 'Q', 1, fluid) * 1e6,
                's_vap': CP.PropsSI('S', 'T', T, 'Q', 1, fluid) / 1000,
                's_liq': CP.PropsSI('S', 'T', T, 'Q', 0, fluid) / 1000,
            }
        except Exception as e:
            return None
```

**1.3 Generera `data/fluid_metadata.json`**
```python
# Script: scripts/generate_metadata.py
import CoolProp.CoolProp as CP
import json

# Manuell data från ASHRAE, EPA databaser
MANUAL_METADATA = {
    'R1233zd(E)': {'gwp': 7, 'odp': 0, 'ashrae_class': 'A1', ...},
    'R245fa': {'gwp': 1030, 'odp': 0, 'ashrae_class': 'B1', ...},
    # ... komplettera för alla medier
}

metadata = {}
for fluid in CP.FluidsList():
    try:
        metadata[fluid] = {
            'T_crit': CP.PropsSI('Tcrit', fluid) - 273.15,
            'p_crit': CP.PropsSI('pcrit', fluid) / 1e5,
            'M': CP.PropsSI('M', fluid),
            'T_boil': CP.PropsSI('T', 'P', 101325, 'Q', 0, fluid) - 273.15,
            **MANUAL_METADATA.get(fluid, {})
        }
    except:
        pass

with open('data/fluid_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

**Deliverables:**
```
✓ Fungerande FluidDatabase-klass
✓ fluid_metadata.json med 130+ medier
✓ Enhetstester för databas (test_database.py)
```

---

### FAS 2: BERÄKNINGSMOTOR (Vecka 2)

#### Mål:
- Portera befintliga beräkningar till modulär struktur
- Implementera ORC-systemberäkningar
- Integrera TesTur-validering

#### Tasks:

**2.1 Skapa `core/thermodynamics.py`**
```python
# Portera från orc_kalkylator_enhanced.py
from core.fluid_database import FluidDatabase

class ThermodynamicCalculator:
    def __init__(self):
        self.db = FluidDatabase()

    def calc_orc_cycle(self, fluid, T_hot, T_cold, P_target_kW,
                       eta_turb=0.55, eta_gen=0.93, eta_pump=0.65):
        """
        Beräknar komplett ORC-cykel
        Porterad från orc_kalkylator_enhanced.py men generaliserad
        """
        # ... implementera
```

**2.2 Skapa `core/tesla_turbine.py`**
```python
TESTUR_REF = {
    'medium': 'Air',
    'mu': 18.2,  # μPa·s
    'b': 0.234,  # mm
    'D': 254,  # mm
    'N_disks': 75,
    'P_verified': 1200,  # W
}

def calc_disc_spacing(mu_fluid):
    """Skalning från TesTur-data"""
    scaling = (mu_fluid / TESTUR_REF['mu'])**0.5
    return TESTUR_REF['b'] * scaling
```

**2.3 Skapa `core/scoring.py`**
```python
def calculate_total_score(fluid, T_hot=50, T_cold=20):
    """
    Beräknar totalpoäng för ORC-lämplighet

    Viktning:
    - Termodynamik: 40% (hfg, PR, η_carnot)
    - Miljö: 30% (GWP, ODP)
    - Säkerhet: 20% (ASHRAE class, brandfarlig)
    - Ekonomi: 10% (kostnad, tillgänglighet)
    """
    # ... implementera viktad poäng
```

**Deliverables:**
```
✓ Fungerande beräkningsmotor
✓ TesTur-integrerad diskavståndsberäkning
✓ Poängalgoritm för ranking
✓ Enhetstester för alla beräkningar
```

---

### FAS 3: GUI - GRUNDLÄGGANDE (Vecka 3)

#### Mål:
- Skapa huvudfönster med tkinter
- Implementera filterpanel
- Visa resultatlista

#### Tasks:

**3.1 Skapa `gui/main_window.py`**
```python
import tkinter as tk
from tkinter import ttk
from gui.filter_panel import FilterPanel
from gui.results_panel import ResultsPanel

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ORC Arbetsmediumverktyg")
        self.root.geometry("1400x900")

        # Layout: 3 kolumner
        self.filter_panel = FilterPanel(self.root, self.on_filter_change)
        self.results_panel = ResultsPanel(self.root, self.on_fluid_select)

        self.filter_panel.grid(row=0, column=0, sticky='ns')
        self.results_panel.grid(row=0, column=1, columnspan=2, sticky='nsew')

    def on_filter_change(self, filters):
        """Callback när filter ändras"""
        filtered_fluids = self.apply_filters(filters)
        self.results_panel.update(filtered_fluids)
```

**3.2 Skapa `gui/filter_panel.py`**
```python
class FilterPanel(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback

        # Kokpunkt slider
        ttk.Label(self, text="Kokpunkt [°C]").pack()
        self.bp_slider = tk.Scale(self, from_=-50, to=50, orient='horizontal')
        self.bp_slider.pack()

        # GWP slider
        ttk.Label(self, text="Max GWP").pack()
        self.gwp_slider = tk.Scale(self, from_=0, to=2000, orient='horizontal')
        self.gwp_slider.pack()

        # Säkerhetsklass checkboxes
        ttk.Label(self, text="Säkerhet").pack()
        self.safety_vars = {
            'A1': tk.BooleanVar(value=True),
            'A2L': tk.BooleanVar(value=True),
            'B1': tk.BooleanVar(value=False),
            'B2L': tk.BooleanVar(value=False),
        }
        for cls, var in self.safety_vars.items():
            ttk.Checkbutton(self, text=cls, variable=var,
                          command=self.on_change).pack()

        # Tryckområde
        ttk.Label(self, text="Tryck @ 50°C [bar]").pack()
        self.p_min = tk.Scale(self, from_=0, to=20, orient='horizontal')
        self.p_max = tk.Scale(self, from_=0, to=20, orient='horizontal')
        self.p_min.set(2)
        self.p_max.set(10)
        self.p_min.pack()
        self.p_max.pack()

    def on_change(self):
        filters = {
            'bp_range': (self.bp_slider.get(), self.bp_slider.get()+20),
            'gwp_max': self.gwp_slider.get(),
            'safety': [k for k,v in self.safety_vars.items() if v.get()],
            'pressure_range': (self.p_min.get(), self.p_max.get())
        }
        self.callback(filters)
```

**3.3 Skapa `gui/results_panel.py`**
```python
class ResultsPanel(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback

        # Trädvy (tree view) för resultat
        columns = ('Namn', 'Kokpunkt', 'GWP', 'Säkerhet', 'Poäng')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col,
                            command=lambda c=col: self.sort_by(c))

        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def update(self, fluids):
        """Uppdatera lista med nya resultat"""
        self.tree.delete(*self.tree.get_children())

        for fluid in fluids:
            self.tree.insert('', 'end', values=(
                fluid['name'],
                f"{fluid['bp']:.1f}",
                fluid['gwp'],
                fluid['safety'],
                f"⭐ {fluid['score']:.2f}"
            ))
```

**Deliverables:**
```
✓ Fungerande GUI med filter och resultat
✓ Realtidsuppdatering vid filterändring
✓ Sorterbara kolumner i resultatvis
```

---

### FAS 4: VISUALISERING (Vecka 4)

#### Mål:
- Integrera matplotlib i GUI
- Dynamiska plottar som uppdateras automatiskt
- Användarval av diagram-typ

#### Tasks:

**4.1 Skapa `gui/plot_panel.py`**
```python
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PlotPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Matplotlib figure embedded i tkinter
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Toolbar för zoom, pan, save
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)

        # Dropdown för diagram-typ
        self.plot_type = ttk.Combobox(self, values=[
            'Tryck-Temperatur',
            'Förångningsvärme',
            'Viskositet',
            'T-s Diagram',
            'P-h Diagram'
        ])
        self.plot_type.pack()
        self.plot_type.bind('<<ComboboxSelected>>', self.update_plot)

    def update_plot(self, selected_fluids):
        """Uppdatera plotten med valda medier"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        plot_type = self.plot_type.get()

        if plot_type == 'Tryck-Temperatur':
            self._plot_pressure_temp(ax, selected_fluids)
        elif plot_type == 'T-s Diagram':
            self._plot_ts_diagram(ax, selected_fluids)
        # ... etc

        self.canvas.draw()

    def _plot_pressure_temp(self, ax, fluids):
        """Tryck-Temperatur plot"""
        temps = np.linspace(0, 100, 101)

        for fluid in fluids:
            pressures = []
            for T in temps:
                props = db.get_properties(fluid, T)
                if props:
                    pressures.append(props['p'])

            ax.plot(temps, pressures, label=fluid, linewidth=2)

        ax.set_xlabel('Temperatur [°C]')
        ax.set_ylabel('Mättningstryck [bar]')
        ax.legend()
        ax.grid(True, alpha=0.3)
```

**Deliverables:**
```
✓ Embedded matplotlib i GUI
✓ 5+ diagramtyper implementerade
✓ Interaktiva tooltips (mplcursors)
✓ Export-knapp direkt i plot panel
```

---

### FAS 5: EXPORT & RAPPORTER (Vecka 5)

#### Mål:
- Professionell PDF-rapport med ReportLab
- PNG-export av högkvalitativa diagram
- CSV-export för Excel

#### Tasks:

**5.1 Skapa `export/pdf_generator.py`**
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Image

class PDFReportGenerator:
    def __init__(self, filename):
        self.doc = SimpleDocTemplate(filename, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []

    def add_title(self, title):
        self.story.append(Paragraph(title, self.styles['Title']))

    def add_fluid_table(self, fluids):
        """Skapar tabell med mediumjämförelse"""
        data = [['Medium', 'Kokpunkt', 'GWP', 'Säkerhet', 'Poäng']]

        for fluid in fluids:
            data.append([
                fluid['name'],
                f"{fluid['bp']:.1f}°C",
                str(fluid['gwp']),
                fluid['safety'],
                f"{fluid['score']:.2f}"
            ])

        table = Table(data)
        table.setStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])

        self.story.append(table)

    def add_plot(self, plot_filename):
        """Lägger till matplotlib-plot i PDF"""
        img = Image(plot_filename, width=400, height=300)
        self.story.append(img)

    def generate(self):
        self.doc.build(self.story)
```

**5.2 Skapa `export/csv_exporter.py`**
```python
import pandas as pd

def export_to_csv(fluids, filename):
    """Exportera resultat till CSV för Excel"""
    df = pd.DataFrame(fluids)
    df.to_csv(filename, index=False, encoding='utf-8-sig')  # Excel-vänlig encoding
```

**Deliverables:**
```
✓ Professionell PDF-rapport med logo och sidfot
✓ PNG-export i 300 DPI
✓ CSV-export med alla beräknade värden
✓ Exportdialog i GUI
```

---

### FAS 6: POLISH & TESTING (Vecka 6)

#### Mål:
- Enhetstester för alla moduler
- Felhantering och validering
- Användarhandledning
- Performance-optimering

#### Tasks:

**6.1 Enhetstester**
```python
# tests/test_thermodynamics.py
import unittest
from core.thermodynamics import ThermodynamicCalculator

class TestThermodynamics(unittest.TestCase):
    def setUp(self):
        self.calc = ThermodynamicCalculator()

    def test_orc_cycle_r1233zde(self):
        result = self.calc.calc_orc_cycle('R1233zd(E)', 50, 20, 1.0)
        self.assertAlmostEqual(result['eta_system'], 0.0485, places=3)
        self.assertAlmostEqual(result['b_disc'], 0.191, places=3)
```

**6.2 Performance-optimering**
```python
# Implementera:
- LRU cache för CoolProp-anrop
- Lazy loading av metadata
- Batch-beräkningar för filtrering
- Threading för långsamma operationer
```

**6.3 Dokumentation**
```markdown
# docs/USER_GUIDE.md

## Snabbstart
1. Starta programmet: `python main.py`
2. Välj temperaturområde i filter panel
3. Välj säkerhetsklass
4. Se resultat uppdateras automatiskt
5. Klicka på ett medium för detaljvy
6. Exportera rapport med knappen "Exportera PDF"

## Filterfunktioner
...
```

**Deliverables:**
```
✓ 90% kodtäckning med tester
✓ Användardokumentation (USER_GUIDE.md)
✓ API-dokumentation (docstrings + Sphinx)
✓ Performance: < 1 sekund för filteruppdatering
```

---

## 5. TEKNISKA SPECIFIKATIONER

### 5.1 Datastrukturer

#### FluidData
```python
@dataclass
class FluidData:
    name: str
    coolprop_name: str
    T_boil: float  # °C @ 1 atm
    T_crit: float  # °C
    p_crit: float  # bar
    M: float  # g/mol
    gwp: int
    odp: float
    ashrae_class: str
    orc_suitability: str  # EXCELLENT/GOOD/MODERATE/POOR
    cost_index: float
    availability: str

    # Beräknade egenskaper (caching)
    _properties_cache: Dict[float, Dict] = field(default_factory=dict)
```

#### FilterCriteria
```python
@dataclass
class FilterCriteria:
    bp_range: Tuple[float, float]  # Kokpunkt intervall
    gwp_max: int
    odp_max: float
    safety_classes: List[str]
    pressure_range: Tuple[float, float]  # @ 50°C
    orc_suitability: List[str]
    flammable_ok: bool
```

### 5.2 Algoritmer

#### Poängalgoritm
```python
def calculate_total_score(fluid: FluidData,
                         T_hot=50, T_cold=20) -> float:
    """
    Totalpoäng för ORC-lämplighet (0-100)

    Viktning:
    - Termodynamik (40%):
      - hfg (15%): Ju högre desto bättre
      - PR (15%): Optimal 2.0-2.5
      - η_carnot (10%): Högre bättre

    - Miljö (30%):
      - GWP (20%): Lägre bättre
      - ODP (10%): Måste vara 0

    - Säkerhet (20%):
      - ASHRAE class (15%): A1 > A2L > B1 > B2L
      - Brandfarlig (5%): -10 poäng om brandfarlig

    - Ekonomi (10%):
      - Kostnad (5%): Lägre bättre
      - Tillgänglighet (5%): Högre bättre
    """

    score = 0

    # Termodynamik (40 poäng)
    props = db.get_properties(fluid.name, T_hot)
    hfg = props['h_vap'] - props['h_liq']
    score += min(15, hfg / 10)  # Max 15 poäng vid hfg > 150 kJ/kg

    p_hot = props['p']
    p_cold = db.get_properties(fluid.name, T_cold)['p']
    PR = p_hot / p_cold
    if 2.0 <= PR <= 2.5:
        score += 15
    else:
        score += 15 * (1 - abs(PR - 2.25) / 2.25)

    eta_carnot = 1 - (T_cold + 273.15) / (T_hot + 273.15)
    score += eta_carnot * 100 * 0.1  # 10 poäng max

    # Miljö (30 poäng)
    score += max(0, 20 * (1 - fluid.gwp / 2000))  # 20 poäng vid GWP=0
    score += 10 if fluid.odp == 0 else 0  # 10 poäng vid ODP=0

    # Säkerhet (20 poäng)
    safety_scores = {'A1': 15, 'A2L': 12, 'B1': 8, 'B2L': 4}
    score += safety_scores.get(fluid.ashrae_class, 0)
    if 'flammable' in fluid.safety_notes.lower():
        score -= 10

    # Ekonomi (10 poäng)
    score += 5 * (1 / fluid.cost_index)  # Billigare = högre poäng
    avail_scores = {'EXCELLENT': 5, 'GOOD': 4, 'MODERATE': 2, 'LIMITED': 0}
    score += avail_scores.get(fluid.availability, 0)

    return min(100, max(0, score))
```

### 5.3 Performance-krav

| Operation | Max tid | Strategi |
|-----------|---------|----------|
| Initial laddning | < 5 sekunder | Cache metadata i JSON |
| Filter-uppdatering | < 1 sekund | Förberäknade egenskaper |
| Plot-uppdatering | < 2 sekunder | Använd färre datapunkter (N=50 istället för 200) |
| PDF-export | < 10 sekunder | Använd vektorgrafik |
| CSV-export | < 1 sekund | Använd pandas |

---

## 6. TIDSPLAN OCH MILSTOLPAR

### Översikt (6 veckor)

| Vecka | Fas | Milstolpe | Tid (h) |
|-------|-----|-----------|---------|
| 1 | Grund & Databas | ✓ Fungerande FluidDatabase<br>✓ fluid_metadata.json (130+ fluids) | 20 |
| 2 | Beräkningsmotor | ✓ Termodynamik-modul<br>✓ Tesla-turbin modul<br>✓ Poängalgoritm | 24 |
| 3 | GUI Grund | ✓ Huvudfönster<br>✓ Filter panel<br>✓ Resultat panel | 20 |
| 4 | Visualisering | ✓ Embedded matplotlib<br>✓ 5+ diagramtyper<br>✓ Interaktiva tooltips | 24 |
| 5 | Export | ✓ PDF-generator<br>✓ PNG-export<br>✓ CSV-export | 16 |
| 6 | Polish & Test | ✓ Enhetstester<br>✓ Dokumentation<br>✓ Performance-optimering | 20 |

**Total tid:** ~124 timmar (ca 3 veckor heltid eller 6 veckor deltid)

### Kritisk väg

```
Vecka 1: Databas  →  Vecka 2: Beräkningar  →  Vecka 3: GUI  →  Vecka 4: Plot
                                                                    ↓
                                                           Vecka 5: Export
                                                                    ↓
                                                           Vecka 6: Test
```

---

## 7. TESTPLAN

### 7.1 Enhetstester

```python
# tests/test_thermodynamics.py
def test_orc_cycle_r1233zde():
    """Validera mot känd referens"""
    calc = ThermodynamicCalculator()
    result = calc.calc_orc_cycle('R1233zd(E)', 50, 20, 1.0)
    assert abs(result['eta_system'] - 0.0485) < 0.001
    assert abs(result['b_disc'] - 0.191) < 0.005

def test_disc_spacing_scaling():
    """Validera TesTur-skalning"""
    b = calc_disc_spacing(12.1)  # R1233zd(E) viskositet
    assert 0.18 < b < 0.20  # Förväntat intervall
```

### 7.2 Integrationstester

```python
def test_filter_to_plot_pipeline():
    """Test att filtrering → sortering → plotting fungerar"""
    filters = FilterCriteria(
        bp_range=(10, 30),
        gwp_max=100,
        safety_classes=['A1', 'A2L']
    )
    fluids = filter_engine.apply(filters)
    assert len(fluids) > 0

    # Verifiera att plotten kan genereras
    plotter.plot_pressure_temp(fluids)
    assert plotter.figure is not None
```

### 7.3 Manuella tester

- [ ] GUI responsivitet: Filter-slider ska uppdatera resultat inom 1 sekund
- [ ] Export fungerar: PDF ska öppnas korrekt i Adobe Reader
- [ ] Alla 130+ medier visas: Inga medier saknas i listan
- [ ] Sortering korrekt: Klick på kolumnhuvud sorterar rätt
- [ ] Felhantering: Ogiltig input ger tydligt felmeddelande

---

## 8. RISKHANTERING

### 8.1 Identifierade risker

| Risk | Sannolikhet | Påverkan | Mitigering |
|------|-------------|----------|------------|
| **CoolProp-data saknas för vissa medier** | HÖG | MEDEL | Implementera robust felhantering, flagga medier utan fullständiga data |
| **Performance-problem vid 130+ medier** | MEDEL | HÖG | Implementera caching, lazy loading, batch-beräkningar |
| **GUI blir för komplex** | MEDEL | MEDEL | Iterativ design, börja enkelt och addera funktionalitet |
| **PDF-generering tar för lång tid** | LÅG | MEDEL | Använd vektorgrafik, komprimera bilder, visa progress bar |
| **Metadata-databas blir ohanterbar** | MEDEL | HÖG | Använd JSON-schema för validering, automatisera så mycket som möjligt |

### 8.2 Backup-plan

**Om CoolProp inte stödjer vissa medier:**
- Använd REFPROP-data (om tillgänglig)
- Markera medier som "Incomplete data" i GUI
- Tillåt manuell input av egenskaper

**Om performance blir problem:**
- Implementera multi-threading för beräkningar
- Använd C-extensions (Cython) för kritiska loopar
- Begränsa antal samtidigt visade medier till 50

---

## 9. NÄSTA STEG

### Omedelbar åtgärd (vecka 1)

```bash
# 1. Installera dependencies
pip install -r requirements.txt

# 2. Skapa mappstruktur
python scripts/setup_project_structure.py

# 3. Generera metadata-databas
python scripts/generate_metadata.py

# 4. Kör initial test
python tests/test_database.py

# 5. Starta GUI-prototyp
python main.py
```

### Prioritetsordning

1. **KRITISKT (vecka 1-2):** FluidDatabase + Beräkningsmotor
2. **HÖGT (vecka 3-4):** GUI + Visualisering
3. **MEDEL (vecka 5):** Export-funktioner
4. **LÅGT (vecka 6):** Polish, dokumentation

---

## 10. SAMMANFATTNING

### Vad vi bygger:
Ett **professionellt Python GUI-verktyg** för att jämföra 130+ ORC-arbetsmedier, med:
- Realtidsfiltrering och sortering
- Dynamiska termodynamiska diagram
- TesTur-validerade Tesla-turbinberäkningar
- Professionell PDF-rapportexport

### Hur vi återanvänder befintlig kod:
- `orc_kalkylator_enhanced.py` → `core/thermodynamics.py` (90% återanvändning)
- `orc_termo_data.py` → `core/fluid_database.py` (utökad till 130+ medier)
- `orc_visualisering.py` → `gui/plot_panel.py` (moderniserad med interaktivitet)
- TesTur-referensdata → `data/testur_reference.json`

### Vad som är nytt:
- Komplett metadata-databas för alla medier
- Interaktiv GUI med filter och sortering
- Dynamiska plottar (inte statiska PNG)
- Professionell PDF-rapportgenerering
- Poängalgoritm för automatisk ranking

### Framgångskriterier:
- ✓ Stödjer alla 130+ medier från CoolProp
- ✓ Filter-respons < 1 sekund
- ✓ Professionell PDF-rapport med diagram
- ✓ Användarvänligt för ingenjörsstudenter
- ✓ Validerat mot TesTur-data för Tesla-turbin

---

**Nästa dokument att läsa:** `docs/IMPLEMENTATION_GUIDE.md` (skapas efter godkännande av denna plan)

**Frågor/Feedback:** Kontakta projektledare för diskussion av prioriteringar och anpassningar.

