# Installation och Användning - ORC Fluid Analysis Tool

## Systemkrav

- **Python:** 3.8 - 3.13 (VIKTIGT: Python 3.14+ fungerar INTE ännu!)
- **Operativsystem:** Windows, macOS, eller Linux med X11
- **RAM:** Minst 2 GB
- **Disk:** ~500 MB (för dependencies och cache)

### ⚠️ KRITISKT - Python-version

**CoolProp** (kärnkomponent) har inte paket för Python 3.14+.

**Kontrollera din version:**
```bash
python --version
```

**Har du Python 3.14?**
1. Installera Python 3.12: https://www.python.org/downloads/release/python-3120/
2. Välj den i VSCode: `Ctrl+Shift+P` → "Python: Select Interpreter" → Python 3.12

## Installation

### 1. Klona eller ladda ner projektet

```bash
git clone <repository-url>
cd mediumverktyg
```

### 2. Kontrollera Python-version (VIKTIGT!)

```bash
# Kör detta FÖRST för att verifiera din Python-version
python check_python_version.py
```

Om du har Python 3.14, **STOPP** - se instruktioner ovan för att installera Python 3.12.

### 3. Installera dependencies

**Rekommenderad metod** (kontrollerar Python-version automatiskt):
```bash
pip install -e .
```

**Alternativ metod** (om du är säker på din Python-version):
```bash
pip install -r requirements.txt
```

**Dependencies som installeras:**
- CoolProp (termodynamisk databas) - **KRÄVER Python 3.8-3.13**
- matplotlib (diagram)
- numpy, pandas (datahantering)
- reportlab (PDF-export)
- tkinter (GUI - föriinstallerat med Python)

### 4. Verifiera installation

```bash
# Testa core-moduler
python -m core.fluid_database
python -m core.thermodynamics
python -m core.tesla_turbine
python -m core.scoring
```

Om alla tester kör utan fel är installationen klar!

## Köra programmet

```bash
python3 main.py
```

eller på Windows:

```bash
python main.py
```

## Första användning

När programmet startar:

1. **Filter-panel (vänster)**
   - Justera kokpunkt, GWP, tryck
   - Välj säkerhetsklasser
   - Filter appliceras automatiskt

2. **Resultat (övre höger)**
   - Visar alla rankade medier
   - Klicka på kolumnrubrik för sortering
   - Ctrl+klick för att välja flera

3. **Diagram (nedre höger)**
   - Visar jämförelse för valda medier
   - Välj diagramtyp från dropdown:
     * Tryck-Temperatur
     * Förångningsvärme
     * Viskositet
     * Densitet (ånga)
     * Jämförelse 4-panel
     * **T-s diagram** (Temperatur-Entropi)
     * **P-h diagram** (Tryck-Entalpi)
     * **Mollier diagram** (Entalpi-Entropi)
   - Zooma med mushjul

## Snabbguide

### Hitta bästa mediet för hemmainstallation

1. Sätt GWP max till **100** (gröna knappen "< 100")
2. Kryssa endast i **A1** och **A2L** (säkrast)
3. Kokpunkt: **10-30°C**
4. Tryck @ 50°C: **2-8 bar**

**→ R1233zd(E) rankas #1!** ⭐⭐⭐⭐⭐

### Jämföra flera medier

1. Välj 2-5 medier från resultatlistan (Ctrl+klick)
2. Välj "Jämförelse 4-panel" från dropdown
3. Se direkt jämförelse av:
   - Tryck vs temperatur
   - Förångningsvärme
   - Viskositet
   - Densitet

### Exportera resultat

- **Fil → Exportera PDF rapport** - Komplett rapport med diagram och data
- **Fil → Exportera CSV data** - För Excel/LibreOffice analys
- Alla diagram kan även sparas som PNG via matplotlib toolbar

## Felsökning

### "Building wheel for CoolProp failed" eller "Cannot open include file: 'boost/..."

**Orsak:** Du har Python 3.14 som CoolProp inte stödjer än.

**Lösning:**
1. Installera Python 3.12: https://www.python.org/downloads/release/python-3120/
2. I VSCode: `Ctrl+Shift+P` → "Python: Select Interpreter" → Python 3.12
3. Kör installation igen: `pip install -e .`

### "ModuleNotFoundError: No module named 'CoolProp'"

**Efter lyckad installation:**
```bash
pip install CoolProp
```

**Om det fortfarande inte fungerar - Python 3.14-problem:**
Se lösningen ovan.

### "ModuleNotFoundError: No module named 'tkinter'"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter ingår vanligtvis med Python från python.org

**Windows:**
Tkinter ingår med standard Python-installation

### GUI startar inte / Svart fönster

Verifiera att X11 är installerat (Linux):
```bash
echo $DISPLAY
# Ska visa något som ":0" eller ":1"
```

### Långsam prestanda

1. Minska antal medier i filter
2. Välj färre medier för plotting (max 5 rekommenderas)
3. Öka RAM-tilldelning om möjligt

## Exempel-workflows

### Workflow 1: Examensarbete - Hitta optimal fluid

```
1. Starta programmet
2. Sätt kokpunkt: 15-25°C (för 50°C värmekälla)
3. GWP max: 10 (miljövänligt)
4. Säkerhet: Endast A1 (heminstallation)
5. Resultat: R1233zd(E) bäst!
6. Välj R1233zd(E) + R245fa för jämförelse
7. Se diagram: Tryck-Temperatur
8. Exportera PDF för rapport
```

### Workflow 2: Forskningsprojekt - Screena alla medier

```
1. Starta med alla filter resetade (Visa → Återställ filter)
2. Sortera efter "Total" (klicka på kolumnrubriken)
3. Notera topp 10 medier
4. Välj topp 5
5. Välj "Jämförelse 4-panel"
6. Analysera termodynamiska egenskaper
7. Exportera CSV för vidare analys i Excel/Python
```

### Workflow 3: Industri - Billig och säker fluid

```
1. Kokpunkt: 10-30°C
2. Säkerhet: A1, A2L, A3 (acceptera brandfarliga om billigt)
3. Sortera efter "Ekon" (ekonomi)
4. Topp 3: IsoButane, n-Butane, Propane
5. OBS: Alla brandfarliga (A3)!
6. Välj R1233zd(E) för säkrare alternativ
```

## Avancerade funktioner

### Ändra beräkningstemperaturer

Redigera `gui/main_window.py`, rad 59:

```python
self.scorer = FluidScorer(T_hot=50, T_cold=20)  # Ändra här
```

### Anpassa scoring-vikter

Redigera `core/scoring.py`, rad 18-21:

```python
thermodynamic: float = 0.40  # 40% - Termodynamik
environmental: float = 0.30  # 30% - Miljö
safety: float = 0.20        # 20% - Säkerhet
economic: float = 0.10      # 10% - Ekonomi
```

### Lägga till ny fluid

Redigera `data/fluid_metadata_manual.json`:

```json
"NewFluid": {
  "formula": "CHxFy",
  "gwp": 50,
  "odp": 0.0,
  "ashrae_class": "A1",
  "flammable": false,
  "toxic": false,
  "orc_suitability": "GOOD",
  "cost_index": 1.0,
  "availability": "MODERATE",
  "notes": "Din beskrivning här"
}
```

## Support

### Rapportera buggar

1. Kontrollera att du har senaste versionen
2. Verifiera att dependencies är installerade korrekt
3. Kör i terminal för att se felmeddelanden
4. Skapa issue på GitHub med:
   - Python-version (`python --version`)
   - OS och version
   - Felmeddelande (hela traceback)
   - Steg för att reproducera

### Frågor

Se `README_PROJECT.md` för teknisk dokumentation.

### Bidra

Pull requests välkomna! Fokusområden:
- Fler medier i metadata
- Prestanda-optimeringar
- Översättningar
- Förbättrade termodynamiska beräkningar

## Licens

MIT License - Fri att använda i kommersiella och akademiska projekt.

---

**Utvecklad för:**
- Ingenjörsstudenter
- ORC-forskare
- Spillvärmeprojekt
- Tesla-turbinkonstruktörer

**Baserad på:**
- CoolProp 7.1.0 termodynamisk databas
- TesTur experimentdata (YouTube K7qZvq1CMFg)
- ASHRAE säkerhetsstandarder

**Version:** 1.0.0
**Datum:** 2025-10-31
