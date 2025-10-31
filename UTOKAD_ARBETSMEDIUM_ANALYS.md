# UTÖKAD ARBETSMEDIUMANALYS - TESLA-TURBIN ORC

## TILLAGDA KANDIDATER

---

## 3.6 R1234yf - Modern Bilklimatanläggning-refrigerant

### Grundegenskaper

| **Egenskap** | **Värde** |
|---|---|
| Kemisk formel | CF₃CF=CH₂ (2,3,3,3-Tetrafluoropropen) |
| Molekylvikt | 114,04 g/mol |
| Kokpunkt (1 atm) | **-29,5°C** |
| Kritisk temperatur | 94,7°C |
| Kritiskt tryck | 33,82 bar |
| ASHRAE-klassning | **A2L** (icke-toxisk, lätt brandfarlig) |
| GWP (100 år) | **4** (mycket låg) |
| ODP | 0 |

*Källa: ASHRAE 34-2019, NIST REFPROP*

### Termodynamiska egenskaper

**Tabell 3.6.1: R1234yf Mättningstryck**

| **Temp (°C)** | **Tryck (bar)** |
|---|---|
| 10 | 4,24 |
| 20 | 5,66 |
| 30 | 7,42 |
| 40 | 9,57 |
| 50 | 12,15 |
| 60 | 15,22 |
| 70 | 18,83 |
| 80 | 23,03 |

**Egenskaper vid 50°C:**
- Tryck: **12,15 bar** (mycket högt!)
- Förångningsvärme: ~130 kJ/kg
- Viskositet ånga: ~11,5 μPa·s
- Beräknat diskavstånd: ~0,18 mm

### Bedömning

**FÖRDELAR:**
- ✅ GWP 4 - extremt låg klimatpåverkan
- ✅ Modern, välstuderad (bilindustrin)
- ✅ God tillgänglighet
- ✅ Viskositet lämplig för Tesla-turbin

**NACKDELAR:**
- ❌ **Kokpunkt -29,5°C** → FÖR LÅG för denna applikation
- ❌ **Tryck 12,15 bar vid 50°C** → MYCKET HÖGT, kräver robusta komponenter
- ❌ **Tryck 4,24 bar vid 10°C kondensering** → SVÅRT att kondensera effektivt
- ❌ **A2L-klassning** → Kräver brandsäkerhetsanalys och läckdetektorer
- ❌ Lägre förångningsvärme → Högre massflöde behövs

**SLUTSATS:** ❌ **EJ REKOMMENDERAD** för lågtemperatur-ORC (30-80°C). Kokpunkten är för låg, vilket ger alltför höga tryck vid drifttemperaturerna. R1234yf är designad för bilklimatanläggningar med helt andra temperaturer.

---

## 3.7 R1234ze(E) - Modern ORC-kandidat

### Grundegenskaper

| **Egenskap** | **Värde** |
|---|---|
| Kemisk formel | CF₃CH=CHF (trans-1,3,3,3-Tetrafluoropropen) |
| Molekylvikt | 114,04 g/mol |
| Kokpunkt (1 atm) | **-18,95°C** |
| Kritisk temperatur | 109,4°C |
| Kritiskt tryck | 36,35 bar |
| ASHRAE-klassning | **A2L** (icke-toxisk, lätt brandfarlig) |
| GWP (100 år) | **6** (mycket låg) |
| ODP | 0 |

*Källa: ASHRAE 34-2019, Honeywell tekniska data*

**VIKTIGT:** Detta är **E-isomeren** av R1234ze, INTE Z-isomeren som redan analyserats. E-isomeren har lägre kokpunkt än Z-isomeren.

### Termodynamiska egenskaper

**Tabell 3.7.1: R1234ze(E) Mättningstryck**

| **Temp (°C)** | **Tryck (bar)** |
|---|---|
| 10 | 3,17 |
| 20 | 4,16 |
| 30 | 5,39 |
| 40 | 6,90 |
| 50 | 8,72 |
| 60 | 10,90 |
| 70 | 13,49 |
| 80 | 16,54 |

**Egenskaper vid 50°C:**
- Tryck: **8,72 bar**
- Förångningsvärme: ~147 kJ/kg
- Viskositet ånga: ~11,9 μPa·s
- Beräknat diskavstånd: ~0,19 mm

### Bedömning

**FÖRDELAR:**
- ✅ GWP 6 - extremt låg klimatpåverkan
- ✅ Icke-toxisk (A-klassning)
- ✅ Tillgänglig från flera leverantörer
- ✅ Viskositet lämplig för Tesla-turbin

**NACKDELAR:**
- ❌ **Kokpunkt -18,95°C** → FÖR LÅG (men bättre än R1234yf)
- ⚠️ **Tryck 8,72 bar vid 50°C** → HÖGT (men acceptabelt)
- ⚠️ **Tryck 3,17 bar vid 10°C** → Gör kondensering svårare än R1233zd(E)
- ❌ **A2L-klassning** → Kräver brandsäkerhetsanalys, läckdetektorer, ventilation
- ⚠️ Mindre ORC-erfarenhet än R245fa

**SLUTSATS:** ⚠️ **MÖJLIG KANDIDAT** om extremt låg GWP är absolut krav OCH man accepterar A2L-säkerhetskrav. Dock SÄMRE än R1233zd(E) på grund av högre tryck och brandsäkerhetskrav.

**JÄMFÖRELSE E vs Z isomer:**

| **Parameter** | **R1234ze(E)** | **R1234ze(Z)** |
|---|---|---|
| Kokpunkt | -18,95°C | **9,8°C** ← BÄTTRE |
| Tryck 50°C | 8,72 bar | **5,62 bar** ← BÄTTRE |
| Tryck 10°C | 3,17 bar | **1,90 bar** ← BÄTTRE |
| ASHRAE | A2L | A2L (samma) |
| GWP | 6 | <1 ← BÄTTRE |

**→ R1234ze(Z) är ÖVERLÄGSEN R1234ze(E) för lågtemperatur-ORC!**

---

## 3.8 R141b - FÖRBJUDEN (men historiskt intressant)

### Grundegenskaper

| **Egenskap** | **Värde** |
|---|---|
| Kemisk formel | CH₃CCl₂F (1,1-Diklor-1-fluoretan) |
| Molekylvikt | 116,95 g/mol |
| Kokpunkt (1 atm) | **32,0°C** |
| Kritisk temperatur | 204,4°C |
| Kritiskt tryck | 42,12 bar |
| ASHRAE-klassning | **D1 (BANNED)** |
| GWP (100 år) | 725 |
| **ODP** | **0,12** ← OZONNEDBRYTANDE! |

*Källa: ASHRAE 34-2019, Montreal Protocol*

### Termodynamiska egenskaper

**Tabell 3.8.1: R141b Mättningstryck**

| **Temp (°C)** | **Tryck (bar)** |
|---|---|
| 10 | 0,29 |
| 20 | 0,49 |
| 30 | 0,77 |
| 40 | 1,17 |
| 50 | 1,71 |
| 60 | 2,42 |
| 70 | 3,33 |
| 80 | 4,48 |

**Egenskaper vid 50°C:**
- Tryck: **1,71 bar** (extremt lågt!)
- Förångningsvärme: ~226 kJ/kg (mycket hög)
- Viskositet ånga: ~10,8 μPa·s
- Beräknat diskavstånd: ~0,17 mm

### Historisk användning

R141b var EXTREMT populärt för lågtemperatur-ORC innan förbudet:
- Optimal kokpunkt (32,0°C) perfekt för 30-80°C drift
- Mycket lågt tryck → enkla, billiga komponenter
- Hög förångningsvärme → lägre massflöde
- Icke-brandfarlig (D1, men toxisk vid brand)

### Varför FÖRBJUDEN?

**Montreal Protocol (1987) och Köpenhamn Amendment (1992):**
- ODP 0,12 → Bryter ned ozonskiktet
- Produktionsstopp: **1 januari 2020** (industriländer)
- **Permanent förbud** i EU och USA
- Ingen tillgänglighet för nya installationer

### Ersättare för R141b

R141b hade PERFEKTA termodynamiska egenskaper för lågtemperatur-ORC. Ersättare söks aktivt:

| **Ersättare** | **Kokpunkt** | **GWP** | **ODP** | **Status** |
|---|---|---|---|---|
| **R1233zd(E)** | 19,0°C | <7 | 0 | ✅ GODKÄND |
| **R1336mzz(Z)** | 33,4°C | <10 | 0 | ✅ Ny ersättare |
| R245fa | 15,3°C | 1030 | 0 | ⚠️ Fasas ut |

**→ R1233zd(E) utvecklades SPECIFIKT som ersättare för R141b!**

### Bedömning

**FÖRDELAR (endast teoretiska):**
- ✅ Perfekt kokpunkt (32,0°C) → optimal för 30-80°C drift
- ✅ Extremt lågt tryck (1,71 bar vid 50°C)
- ✅ Hög förångningsvärme → lågt massflöde
- ✅ Icke-brandfarlig
- ✅ God viskositet för Tesla-turbin

**NACKDELAR:**
- ❌ **PERMANENT FÖRBJUDEN** (ODP 0,12)
- ❌ **Ingen tillgänglighet**
- ❌ **Illegalt att använda i nya system**
- ❌ D1-klassning (toxisk vid brand)
- ❌ GWP 725 (högt, men irrelevant då det är förbjudet)

**SLUTSATS:** ❌ **KAN EJ ANVÄNDAS** - Permanent förbjuden enligt Montreal Protocol. Inkluderad endast för historisk kontext. **Använd R1233zd(E) istället** (designad som direkt ersättare).

---

## UPPDATERAD JÄMFÖRELSETABELL - ALLA KANDIDATER

### Tabell 4.1: Fullständig Kandidatjämförelse

| **Medium** | **Kokpunkt (°C)** | **Tryck 10°C (bar)** | **Tryck 50°C (bar)** | **hfg 50°C (kJ/kg)** | **μ 50°C (μPa·s)** | **Diskavstånd (mm)** | **ASHRAE** | **GWP** | **Status** |
|---|---|---|---|---|---|---|---|---|---|
| **R1233zd(E)** | 19,0 | 0,65 | 2,48 | 173 | 11,8 | 0,18-0,20 | A1 | <7 | ✅ REKOMMENDERAD |
| **R245fa** | 15,3 | 0,83 | 3,44 | 176 | 12,5 | 0,19-0,23 | B1 | 1030 | ✅ BACKUP |
| **R1234ze(Z)** | 9,8 | 1,90 | 5,62 | 160 | 12,2 | 0,20 | A2L | <1 | ⚠️ MÖJLIG |
| **R1234ze(E)** | -18,95 | 3,17 | 8,72 | 147 | 11,9 | 0,19 | A2L | 6 | ❌ FÖR HÖG TRYCK |
| **R1234yf** | -29,5 | 4,24 | 12,15 | 130 | 11,5 | 0,18 | A2L | 4 | ❌ FÖR HÖG TRYCK |
| **R141b** | 32,0 | 0,29 | 1,71 | 226 | 10,8 | 0,17 | D1 | 725 | ❌ FÖRBJUDEN (ODP) |

*Källa: ASHRAE 34-2019, CoolProp, NIST REFPROP, Montreal Protocol*

### Tabell 4.2: Sammanfattande Bedömning

| **Medium** | **Termodynamik** | **Säkerhet** | **Miljö** | **Tillgänglighet** | **Totalbedömning** |
|---|---|---|---|---|---|
| R1233zd(E) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **⭐⭐⭐⭐⭐ BÄST** |
| R245fa | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | **⭐⭐⭐⭐ BACKUP** |
| R1234ze(Z) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **⭐⭐⭐ MÖJLIG** |
| R1234ze(E) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ Ej rekommenderad |
| R1234yf | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ Ej rekommenderad |
| R141b | ⭐⭐⭐⭐⭐ | ⭐⭐ | ❌ | ❌ | ❌ FÖRBJUDEN |

---

## UPPDATERAD SLUTSATS

### Rangordning efter analys av ALLA kandidater:

**🥇 1. R1233zd(E)** - PRIMÄR REKOMMENDATION
- Optimal kokpunkt (19,0°C) närmast ideal zon 20-30°C
- Lägst tryck av alla tillåtna kandidater
- Säkrast (A1)
- Bäst miljö (GWP <7)
- Direktersättare för förbjudna R141b

**🥈 2. R245fa** - SEKUNDÄR REKOMMENDATION  
- Etablerad med >20 års ORC-erfarenhet
- God tillgänglighet
- Acceptabel säkerhet (B1)
- Något högre tryck och GWP än R1233zd(E)

**🥉 3. R1234ze(Z)** - BACKUP VID EXTREMA MILJÖKRAV
- Lägst GWP (<1) av alla
- Men kräver A2L brandsäkerhetsanalys
- Högre tryck än R1233zd(E)
- Begränsad tillgänglighet

**❌ 4-6. EJ REKOMMENDERADE:**
- **R1234ze(E)** - För högt tryck (8,72 bar vid 50°C)
- **R1234yf** - Mycket för högt tryck (12,15 bar vid 50°C)  
- **R141b** - FÖRBJUDEN (ODP 0,12)

### Varför INTE de nya kandidaterna?

**R1234yf och R1234ze(E):**
- Kokpunkt för låg → tryck för högt vid drifttemperatur
- Designade för ANDRA applikationer (bilklimatanläggning, kylar)
- Kräver A2L brandsäkerhetsanalys
- Ingen fördel över R1233zd(E) som har perfekt kombination

**R141b:**
- Perfekta termodynamiska egenskaper
- Men permanent förbjuden sedan 2020
- R1233zd(E) utvecklades specifikt som ersättare

### FINAL REKOMMENDATION (OFÖRÄNDRAD)

**För ORC Malung-projektet rekommenderas fortfarande R1233zd(E) som primärt arbetsmedium.**

Efter analys av ALLA tänkbara kandidater står R1233zd(E) kvar som det bästa valet tack vare:
1. Optimal kokpunkt för lågtemperatur-ORC
2. Lägst tryck av alla TILLÅTNA alternativ  
3. Säkrast möjliga klassning (A1)
4. Extremt låg klimatpåverkan (GWP <7)
5. Utvecklad SPECIFIKT för att ersätta förbjudna R141b

**R245fa kvarstår som backup** vid otillgänglighet eller budgetbegränsningar.

---

**Dokument uppdaterat: 2025-10-31**  
**Version: 2.0 - UTÖKAD MED YTTERLIGARE KANDIDATER**  
**Status: FÄRDIG FÖR GRANSKNING**  
**Projekt: ORC Malung Tesla-Turbin**
