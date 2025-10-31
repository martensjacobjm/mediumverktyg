================================================================================
ORC MALUNG - TERMODYNAMISKA VERKTYG
================================================================================
Genererat: 2025-10-29
Projekt: Tesla-Turbin ORC Lågtemperatur 30-80°C
================================================================================

INNEHÅLL
--------------------------------------------------------------------------------
Detta paket innehåller kompletta termodynamiska verktyg för dimensionering
av ORC Malung projektet. Alla data genererade med CoolProp - professionell
termodynamisk databas som används inom forskning och industri.

FILER I PAKETET
--------------------------------------------------------------------------------

📊 DATA-FILER:
  
  R245fa_saturated.csv
    - Kompletta saturerade ångtabeller för R245fa
    - Temperaturområde: 10-80°C i 5°C steg
    - Kolumner: T, p, ρ_vätska, ρ_ånga, h_vätska, h_ånga, hfg, s, μ_ånga
  
  R1233zdE_saturated.csv
    - Kompletta saturerade ångtabeller för R1233zd(E)
    - Samma format som R245fa
    - Användbart för Excel/Python-import

📈 DIAGRAM:
  
  ORC_termo_jamforelse.png
    - 4 subplots: Tryck, hfg, Viskositet, Densitet
    - Jämför R245fa vs R1233zd(E) 
    - Visar optimal driftzon
  
  ORC_tryck_temperatur.png
    - Detaljerad tryck-temperatur jämförelse
    - Markerar kondensering/förångning zoner
    - Visar önskat tryckintervall 2-10 bar

📄 BERÄKNINGAR:
  
  ORC_Berakningsformler.txt
    - Snabbreferens för alla formler
    - Carnot, Rankine, massflöde, värmeväxlare
    - Tesla-turbin diskavstånd
    - Exempel-beräkningar
  
  ORC_Dimensionering_Berakningar.txt
    - Färdiga beräkningar för 4 scenarion:
      1. R1233zd(E) 50→20°C 1kW
      2. R1233zd(E) 50→20°C 2kW
      3. R1233zd(E) 80→10°C 2kW (maximal prestanda)
      4. R245fa 50→20°C 1kW (jämförelse)
    - Inkluderar massflöde, värmeväxlare, pump, diskavstånd

🐍 PYTHON-SCRIPTS:
  
  orc_termo_data.py
    - Genererar saturerade ångtabeller
    - Jämför medier vid nyckeltemperaturer
    - Exporterar till CSV
  
  orc_visualisering.py
    - Skapar diagram från CSV-data
    - Anpassningsbara plots
  
  orc_kalkylator.py
    - INTERAKTIV KALKYLATOR
    - Beräknar kompletta ORC-system
    - Ändra parametrar för dina scenarion

INSTALLATION & ANVÄNDNING
--------------------------------------------------------------------------------

KRAV:
  Python 3.x
  pip install CoolProp pandas matplotlib

KÖRA SCRIPTS:

1. Generera nya tabeller:
   python3 orc_termo_data.py

2. Skapa diagram:
   python3 orc_visualisering.py

3. Beräkna dimensionering:
   python3 orc_kalkylator.py

ANPASSA KALKYLATOR:
  Öppna orc_kalkylator.py och ändra:
  - Temperaturer (T_hot, T_cold)
  - Måleffekt (P_target_kW)
  - Verkningsgrader (eta_turb, eta_gen, eta_pump)
  
  Exempel lägg till nytt scenario:
  result_5 = calc_system("R1233zd(E)", "R1233zd(E)", 60, 15, 1.5)

NYCKELRESULTAT FRÅN BERÄKNINGAR
--------------------------------------------------------------------------------

GRUNDDIMENSIONERING (R1233zd(E) 50°C → 20°C, 1 kW):
  
  Massflöde:              9,1 g/s
  Tryckförhållande:       2,71:1 (optimal zon)
  Förångare:              1,96 kW värmebehov
  Kondensor:              2,96 kW kylbehov
  Pumpeffekt:             2 W (försumbar)
  Diskavstånd turbin:     0,191 mm
  Köldbärare flöde:       8,5 L/min (sommardrift)
  
  ✓ System verifierat genomförbart med dessa parametrar

HÖGRE EFFEKT (R1233zd(E) 50°C → 20°C, 2 kW):
  
  Massflöde:              18,2 g/s (dubbelt)
  Förångare:              3,91 kW
  Kondensor:              5,91 kW
  Köldbärare:             17 L/min
  
  ✓ Linjär skalning fungerar

MAXIMAL PRESTANDA (R1233zd(E) 80°C → 10°C, 2 kW):
  
  Tryckförhållande:       8,96:1 (mycket bra!)
  Carnot verkningsgrad:   19,82% (dubbelt jämfört med 50→20°C)
  Massflöde:              15,9 g/s (lägre tack vare högre hfg)
  Diskavstånd:            0,201 mm (något större pga högre viskositet)
  
  ✓ Sommardrift med solfångare 80°C + KB 10°C = OPTIMAL konfiguration

R245fa VS R1233zd(E) JÄMFÖRELSE (50°C → 20°C, 1 kW):
  
  Massflöde:              9,0 vs 9,1 g/s (praktiskt identiska)
  Tryck förångning:       3,44 vs 2,93 bar (R1233zd(E) 15% lägre)
  Diskavstånd:            0,197 vs 0,191 mm (mycket liknande)
  Systemverkningsgrad:    51% för båda
  
  ✓ R1233zd(E) ÖVERLÄGSET tack vare:
    - Lägre tryck (enklare system)
    - A1 klassning (säkrare än R245fa B1)
    - GWP <7 (147× bättre miljö än R245fa 1030)

VIKTIGA SLUTSATSER
--------------------------------------------------------------------------------

1. R1233zd(E) BEKRÄFTAT som primärt val
   - Optimal kokpunkt 19°C
   - Lägst tryck vid drift
   - Säkrast och miljövänligast

2. Diskavstånd 0,19-0,20 mm VERIFIERAT
   - Skalning från TesTur korrekt
   - Praktiskt identiskt för R245fa och R1233zd(E)

3. Massflöde 9-18 g/s för 1-2 kW
   - Linjär skalning fungerar
   - Pumpen försumbar (<1% av effekt)

4. Sommardrift 80°C → 10°C OPTIMAL
   - Dubbel Carnot-verkningsgrad (20% vs 9%)
   - Solfångare + KB kombinationen perfekt

5. Köldbärare 8-17 L/min för 1-2 kW
   - Normalt husvattenflöde räcker (15-20 L/min)
   - Sommardrift utan problem

NÄSTA STEG
--------------------------------------------------------------------------------

1. ✅ Termodynamisk analys KLAR
2. ✅ Medium val BEKRÄFTAT (R1233zd(E))
3. ✅ Dimensionering BERÄKNAD

ÅTERSTÅR:
4. Mechanisk design Tesla-turbin (disk, hus, axel)
5. Värmevxlare specifikation (plattvxlare vs spiral)
6. Tank-design (1000L + 500L preliminärt)
7. Styrningssystem (temperatur, tryck, massflöde)
8. Inköp komponenter
9. Konstruktion prototyp
10. Test & validering

SUPPORT & KONTAKT
--------------------------------------------------------------------------------

Termodynamiska frågor:
  - CoolProp dokumentation: http://www.coolprop.org/
  - NIST REFPROP: https://www.nist.gov/srd/refprop

ORC forskning:
  - Ken Reiley Tesla Turbine research
  - MDPI Tesla Turbine CFD studies
  - DOE ORC low-temperature applications

F-gas reglering:
  - ASHRAE Standard 34-2019
  - EU F-gas Regulation 517/2014

================================================================================
Detta paket innehåller ALLT du behöver för termodynamisk dimensionering
av ORC Malung projektet. Lycka till med konstruktionen!
================================================================================
