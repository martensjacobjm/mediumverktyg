# Installation och Användning - ORC Fluid Analysis Tool

## Systemkrav

- **Python:** 3.8 eller senare
- **Operativsystem:** Windows, macOS, eller Linux med X11
- **RAM:** Minst 2 GB
- **Disk:** ~500 MB (för dependencies och cache)

## Installation

### 1. Klona eller ladda ner projektet

```bash
git clone <repository-url>
cd mediumverktyg
```

### 2. Installera dependencies

```bash
pip install -r requirements.txt
```

**Dependencies som installeras:**
- CoolProp (termodynamisk databas)
- matplotlib (diagram)
- numpy, pandas (datahantering)
- reportlab (PDF-export)
- tkinter (GUI - oftast föriinstallerat med Python)

### 3. Verifiera installation

```bash
# Testa core-moduler
python3 -m core.fluid_database
python3 -m core.thermodynamics
python3 -m core.tesla_turbine
python3 -m core.scoring
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
   - Välj diagramtyp från dropdown
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

- **Fil → Exportera PDF rapport** (kommer snart)
- **Fil → Exportera CSV data** (kommer snart)

## Felsökning

### "ModuleNotFoundError: No module named 'CoolProp'"

```bash
pip install CoolProp
```

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
- Fler diagramtyper
- PDF-export implementation
- Fler medier i metadata
- Prestanda-optimeringar
- Översättningar

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

**Version:** 0.5.0
**Datum:** 2025-10-31
