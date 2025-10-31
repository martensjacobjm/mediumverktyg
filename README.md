# ORC Working Fluid Analysis Tool

**Version:** 1.0.0  
**Status:** Production Ready ✅  
**License:** MIT

Dynamiskt Python-baserat GUI-verktyg för jämförelse och analys av 79+ arbetsmedier för Tesla-turbin ORC-system.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Översikt

Detta verktyg ger ingenjörer, forskare och studenter möjlighet att:
- **Jämföra 79+ arbetsmedier** från CoolProp-databasen
- **Filtrera dynamiskt** efter kokpunkt, GWP, tryck, säkerhetsklass
- **Visualisera** termodynamiska egenskaper i realtid
- **Exportera** professionella rapporter (PDF, PNG, CSV)
- **Designa Tesla-turbiner** med TesTur-validerade beräkningar

---

## ✨ Features

### 🔬 Core Funktionalitet
- ✅ **79 ORC-lämpliga fluider** med fullständiga termodynamiska egenskaper
- ✅ **Intelligent rankingsystem** (Termo 40%, Miljö 30%, Säkerhet 20%, Ekonomi 10%)
- ✅ **TesTur-validerade** beräkningar för diskavstånd och turbindesign
- ✅ **Automatisk datahämtning** från CoolProp

### 🖥️ Interactive GUI
- ✅ **Realtidsfiltrering** och **sorterbara kolumner**
- ✅ **Färgkodning** och **stjärnbetyg** ⭐⭐⭐⭐⭐
- ✅ **5 diagramtyper** med matplotlib
- ✅ **Export till PDF, PNG, CSV**

---

## 🚀 Snabbstart

```bash
# Installation
pip install -r requirements.txt

# Kör applikationen
python3 main.py
```

---

## 🏆 Top 5 Rankade Fluider

| Rank | Fluid | Score | GWP | Safety |
|------|-------|-------|-----|--------|
| 1 | R1233zd(E) | 96.4 | 7 | A1 ⭐⭐⭐⭐⭐ |
| 2 | R1234ze(E) | 88.4 | 6 | A2L ⭐⭐⭐⭐⭐ |
| 3 | IsoButane | 88.0 | 3 | A3 ⭐⭐⭐⭐⭐ |

**Rekommendation:** R1233zd(E) - Säkrast för heminstallation

---

Se `INSTALLATION.md` för detaljerad guide.

**Version:** 1.0.0 | **Datum:** 2025-10-31
