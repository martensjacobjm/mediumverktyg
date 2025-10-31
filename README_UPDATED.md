# MEDIUMANALYS - ORC MALUNG

**Uppdaterad:** 2025-10-31  
**Status:** ✓ Komplett med Enhanced Analysis

---

## 🆕 NYA FILER (2025-10-31)

**VIKTIGT:** En ny undermapp `enhanced_analysis/` har skapats med förbättrade analyser!

**→ Gå till `enhanced_analysis/` för uppdaterad analys med TesTur-integration**

---

## MAPSTRUKTUR

```
mediumanalys/
├── README.txt                          (original översikt)
├── README_UPDATED.md                   (denna fil)
├── ORC_Berakningsformler.txt          (formelreferens)
├── ORC_Dimensionering_Berakningar.txt (scenarion 1-4)
├── 
├── Python-scripts (original):
│   ├── orc_kalkylator.py              (grundkalkylator)
│   ├── orc_termo_data.py              (generera tabeller)
│   ├── orc_visualisering.py           (diagram)
│   ├── generate_diagrams.py           (automatisk)
│   ├── generate_rapport.py            (Word-rapport)
│   └── generate_all.py                (kör allt)
│
├── Data-filer:
│   ├── R245fa_saturated.csv
│   └── R1233zdE_saturated.csv
│
├── outputs/                            (genererade filer)
│   ├── ORC_Arbetsmedium_Analys.docx
│   ├── ORC_tryck_temperatur.png
│   └── ORC_termo_jamforelse.png
│
└── enhanced_analysis/ ⭐ NYA FILER HÄR ⭐
    ├── SNABB_SAMMANFATTNING.md        (läs detta först!)
    ├── MASTER_INTEGRERAD_ANALYS.md    (komplett analys)
    ├── orc_kalkylator_enhanced.py     (förbättrad kalkylator)
    └── README.md                       (detaljer)
```

---

## VART SKA JAG BÖRJA?

### För Snabb Översikt (3 minuter)
```
Läs: enhanced_analysis/SNABB_SAMMANFATTNING.md
```

### För Komplett Förståelse (25 minuter)
```
Läs: enhanced_analysis/MASTER_INTEGRERAD_ANALYS.md
```

### För Beräkningar (1 minut)
```bash
cd enhanced_analysis
python orc_kalkylator_enhanced.py
```

---

## VAD ÄR NYTT I ENHANCED ANALYSIS?

### 1. TesTur-Integration ⭐
```
Original:  Isolerad termodynamisk analys
Enhanced:  ✓ TesTur Video K7qZvq1CMFg integrerad
           ✓ 1200W verifierad
           ✓ 10,000 RPM bekräftad
           ✓ Charlie Solis teknisk feedback
```

### 2. Diskavstånd Härlett ⭐
```
Original:  0,18-0,25 mm (utan härledning)
Enhanced:  ✓ 0,191 mm (exakt via viskositetsskalning)
           ✓ Beräkning transparent: √(12,1/18,2) = 0,816
           ✓ Från TesTur 0,234 mm × 0,816 = 0,191 mm
```

### 3. Systemdimensionering ⭐
```
Original:  Grundläggande beräkningar
Enhanced:  ✓ Energiflödesdiagram
           ✓ Driftlägen (Vinter/Sommar/Höst-Vår)
           ✓ Ekonomisk analys
           ✓ Konstruktionsfaser
```

### 4. Validering ⭐
```
Original:  CoolProp + teoretiska antaganden
Enhanced:  ✓ TesTur experimentdata
           ✓ MDPI CFD-forskning
           ✓ Charlie Solis praktisk erfarenhet
           ✓ Ken Reiley konstruktionsdata
```

---

## HUVUDRESULTAT

### R1233zd(E) BEKRÄFTAT SOM OPTIMAL
```
Kokpunkt:       19,0°C (bäst för 10-30°C kondensering)
Tryck 50°C:     2,93 bar (15% lägre än R245fa)
Säkerhet:       A1 (säkrast möjligt)
GWP:            <7 (147× bättre än R245fa)
Viskositet:     12,1 μPa·s
Diskavstånd:    0,191 mm (från TesTur-skalning)
Merkostnad:     +200-400 € (+3% av totalkostnad)
```

### DIMENSIONERING 1-2 KW
```
Massflöde:      9-18 g/s
Förångare:      2-4 kW
Kondensor:      3-6 kW
Pump:           2-4 W (försumbar)
Diskavstånd:    0,19 mm
Disktjocklek:   0,25 mm
Antal diskar:   75
RPM:            8000-12000
```

### SYSTEM GENOMFÖRBART
```
Total kostnad:  ~70 000 kr
Elproduktion:   ~3360 kWh/år
Återbetalning:  ~11 år
```

---

## ORIGINAL DOKUMENTATION

De ursprungliga filerna finns kvar och fungerar fortfarande:

### Beräkningar
```bash
# Grundläggande kalkylator
python orc_kalkylator.py

# Generera termodynamiska tabeller
python orc_termo_data.py

# Skapa diagram
python orc_visualisering.py

# Allt i ett
python generate_all.py
```

### Formelreferens
```
Fil: ORC_Berakningsformler.txt
Innehåll: Carnot, Rankine, massflöde, värmeväxlare, diskavstånd
```

### Färdiga Beräkningar
```
Fil: ORC_Dimensionering_Berakningar.txt
Innehåll: 4 scenarion med kompletta beräkningar
```

---

## VARFÖR TVÅ VERSIONER?

**Original dokumentation:**
- Grundläggande termodynamik
- Snabbreferens formler
- Automatisk rapportgenerering
- Beprövade Python-scripts

**Enhanced analysis:**
- Integration med TesTur-data
- Validering mot experiment
- Systemdimensionering komplett
- Ekonomisk analys
- Konstruktionsfaser

**→ Använd båda! Original för snabbsökning, Enhanced för djupförståelse.**

---

## PRAKTISKA SPECIFIKATIONER

**Kopiera dessa till CAD-design:**

### Tesla-Turbin
```
Diskavstånd b:      0,191 mm (tol ±0,01 mm)
Disktjocklek th:    0,254 mm
Antal diskar N:     75
Diameter D:         254 mm (10 tum)
Munstycken:         12 st (30° fördelning)
Material:           316L rostfritt (diskar)
                    Aluminium (hus)
RPM design:         10,000 nominal, 12,000 max
Balansering:        G1 kvalitet (kritiskt!)
```

### Arbetsmedium
```
Primärt:            R1233zd(E)
Backup:             R245fa
Fyllning:           5-10 kg (beroende på system)
Förångning 50°C:    2,93 bar
Kondensering 20°C:  1,08 bar
Säkerhet:           A1 klassning
F-gas:              Certifierad installation krävs
```

### Värmeväxlare
```
Förångare:          Plattvärmeväxlare
  - Yta:            0,5 m²
  - Design tryck:   4 bar
  - Material:       316L rostfritt
  - Effekt:         2-4 kW

Kondensor:          Plattvärmeväxlare
  - Yta:            0,8 m²
  - Design tryck:   2 bar
  - Material:       316L rostfritt
  - Effekt:         3-6 kW
```

---

## KRITISKA FRAMGÅNGSFAKTORER

### 1. Diskavstånd Precision
```
⚠️ 0,19 mm ± 0,01 mm (absolut max tolerans)
- Kräver laserskärning ELLER precision CNC
- Kontrollera varje disk med mikrometer
- Använd shims för justering vid behov
```

### 2. Dynamisk Balansering
```
⚠️ OBLIGATORISK vid 10,000 RPM
- G1 balanseringsklass minimum
- Professionell balansering rekommenderas
- Test gradvis från 1000 till 10,000 RPM
```

### 3. F-gas Säkerhet
```
⚠️ R1233zd(E) kräver:
- Certifierad installatör
- Läckdetektor installerad
- Dokumenterad driftplan
- Regelbunden service
```

---

## JÄMFÖRELSE ORIGINAL VS ENHANCED

| Aspekt | Original | Enhanced | Förbättring |
|--------|----------|----------|-------------|
| **Diskavstånd** | 0,18-0,25 mm | 0,191 mm | ✓ Exakt |
| **Härledning** | Begränsad | Fullständig | ✓ Transparent |
| **TesTur-data** | Nej | Ja | ✓ Validerad |
| **Systemdesign** | Komponenter | Komplett | ✓ Integrerad |
| **Ekonomi** | Kostnader | + återbetalning | ✓ Komplett |
| **Fasplan** | Nej | Ja (FAS 1-3) | ✓ Tidslinje |
| **Python** | Grundläggande | + TesTur-validering | ✓ Förbättrad |

---

## KÄLLOR OCH REFERENSER

### Primära Källor (Enhanced)
```
✓ TesTur Video K7qZvq1CMFg (lufttest 1200W)
✓ Charlie Solis kommentarer (ORC-erfarenhet)
✓ MDPI Energies 2019, 12, 44 (CFD-forskning)
✓ Viskositet_och_Diskavstand_KORRIGERAD.md
✓ Ken_Reiley_Konstruktionsmanual.md
```

### Termodynamik (Original)
```
✓ CoolProp 7.1.0 (termodynamisk databas)
✓ Bell et al. 2014 (CoolProp publication)
✓ NIST REFPROP (validering)
```

### Standards
```
✓ ASHRAE Standard 34-2019 (säkerhetsklassning)
✓ EU Regulation 517/2014 (F-gas)
✓ SS-EN 378:2016 (köldsystem)
```

---

## NÄSTA STEG

### 1. Läs Enhanced Analysis (idag)
```
□ SNABB_SAMMANFATTNING.md (3 min)
□ MASTER_INTEGRERAD_ANALYS.md (25 min)
□ Kör orc_kalkylator_enhanced.py (1 min)
```

### 2. Börja Detaljdesign (denna vecka)
```
□ CAD-modell Tesla-turbin
  - 75 diskar, 0,19mm gap, 0,25mm tjocklek
  - Turbinhus med 12 munstycken
  - Axel design för 10,000 RPM

□ FEM-analys
  - Stress vid 10,000 RPM
  - Modalanalys (undvik resonans)
  - Termisk expansion
```

### 3. Välj Leverantörer (nästa vecka)
```
□ Laserskärning diskar (tol ±0,01mm)
□ Plattvärmeväxlare (Alfa Laval)
□ Generator 2kW PMSG
□ F-gas certifierad installatör
```

---

## SUPPORT OCH KONTAKT

**Frågor om termodynamik:**
- CoolProp: http://www.coolprop.org/
- NIST REFPROP: https://www.nist.gov/srd/refprop

**Frågor om Tesla-turbiner:**
- Ken Reiley projektfiler
- MDPI journal Energies
- TesTur YouTube

**Frågor om F-gas:**
- ASHRAE Standard 34-2019
- EU F-gas Regulation
- Lokal certifierad installatör

---

## ÄNDRINGSLOGG

**2025-10-31 - Enhanced Analysis Release**
```
+ Ny undermapp enhanced_analysis/ skapad
+ MASTER_INTEGRERAD_ANALYS.md (komplett integration)
+ orc_kalkylator_enhanced.py (TesTur-validering)
+ SNABB_SAMMANFATTNING.md (3-minuters översikt)
+ README.md (detaljerad guide)
+ Denna README_UPDATED.md
```

**2025-10-29 - Original Release**
```
+ ORC termodynamiska verktyg komplett
+ Python-scripts för beräkning och visualisering
+ Word-rapportgenerering
+ CSV-data för R245fa och R1233zd(E)
```

---

**✓ MEDIUMANALYS KOMPLETT**  
**✓ ENHANCED ANALYSIS TILLGÄNGLIG**  
**✓ REDO FÖR DETALJDESIGN**

*För bästa resultat: Använd enhanced_analysis/ för projektstyrning*
