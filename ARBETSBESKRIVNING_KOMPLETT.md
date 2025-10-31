# ARBETSBESKRIVNING: INTERAKTIVT ARBETSMEDIUMANALYSVERKTYG FÖR TESLA-TURBIN ORC

**Version:** 2.0 KOMPLETT  
**Datum:** 2025-10-31  
**Status:** Klar för implementation  

---

## INNEHÅLLSFÖRTECKNING

1. [Projektmål och omfattning](#1-projektmål-och-omfattning)
2. [Alla tillgängliga arbetsmedier](#2-alla-tillgängliga-arbetsmedier)
3. [Sorteringsfunktionalitet](#3-sorteringsfunktionalitet)
4. [Interaktiv GUI (detaljerad)](#4-interaktiv-gui-detaljerad)
5. [Automatisk datahämtning](#5-automatisk-datahämtning)
6. [Beräkningsmotor](#6-beräkningsmotor)
7. [Dynamisk diagramgenerering](#7-dynamisk-diagramgenerering)
8. [Exportfunktioner](#8-exportfunktioner)
9. [Teknisk arkitektur](#9-teknisk-arkitektur)
10. [Dataflöde och algoritmer](#10-dataflöde-och-algoritmer)
11. [Implementation fas-för-fas](#11-implementation-fas-för-fas)
12. [Testplan och kvalitetssäkring](#12-testplan-och-kvalitetssäkring)
13. [Risker och mitigering](#13-risker-och-mitigering)
14. [Framtida utveckling](#14-framtida-utveckling)

---

## 1. PROJEKTMÅL OCH OMFATTNING

### 1.1 Övergripande mål

Utveckla ett **Python-baserat interaktivt verktyg** för automatisk jämförelse av arbetsmedier för Tesla-turbin ORC-system med fokus på:

- ✅ **Alla 130+ arbetsmedier från CoolProp** tillgängliga för val
- ✅ **Avancerad sortering och filtrering** (kokpunkt, tryck, GWP, säkerhet, etc.)
- ✅ **Automatisk datahämtning** från termodynamiska databaser (CoolProp)
- ✅ **Interaktiv GUI** med realtidsuppdatering
- ✅ **Dynamiska diagram** anpassade efter användarval
- ✅ **Professionella exportfunktioner** (PDF-rapport, PNG-diagram, CSV-data)

### 1.2 Användningsområden

- **Examensarbeten:** Snabb jämförelse av medier för lågtemperatur-ORC
- **Forskning:** Systematisk screening av 100+ medier
- **Industriella projekt:** Beslutsunderlag för mediumval
- **Utbildning:** Pedagogiskt verktyg för termodynamik

### 1.3 Målgrupp

- Ingenjörsstudenter (VVS, maskin, energi)
- Forskare inom ORC-system
- Projektingenjörer inom spillvärmeutnyttjande
- Konstruktörer av Tesla-turbiner

---

## 2. ALLA TILLGÄNGLIGA ARBETSMEDIER

### 2.1 Fullständig mediumlista från CoolProp

Verktyget ska stödja **ALLA** följande medier (130+ stycken):

#### 2.1.1 HFC-medier (Hydrofluorokarboner)
```python
HFC_MEDIA = [
    'R11', 'R12', 'R13', 'R14',
    'R22', 'R23',
    'R32',
    'R113', 'R114', 'R115', 'R116',
    'R123', 'R124', 'R125',
    'R134a',
    'R141b', 'R142b', 'R143a', 'R152a',
    'R161',
    'R218',
    'R227ea', 'R236ea', 'R236fa', 'R245ca', 'R245fa',
    'R365mfc',
    'R404A', 'R407C', 'R410A', 'R507A',
]
```

#### 2.1.2 HFO-medier (Hydrofluoroolefiner) - Miljövänliga
```python
HFO_MEDIA = [
    'R1233zd(E)',    # ★ PRIMÄR FÖR ORC
    'R1234yf',
    'R1234ze(E)',
    'R1234ze(Z)',    # ★ BACKUP FÖR ORC
    'R1336mzz(Z)',
]
```

#### 2.1.3 Naturliga medier (HC, NH3, CO2, H2O)
```python
NATURLIGA_MEDIA = [
    # Kolväten (HC)
    'Methane', 'Ethane', 'Propane', 'n-Butane', 'IsoButane',
    'n-Pentane', 'Isopentane', 'Neopentane',
    'n-Hexane', 'n-Heptane', 'n-Octane', 'n-Nonane', 'n-Decane',
    'Cyclopentane', 'Cyclohexane',
    'R600',      # Butane
    'R600a',     # Isobutane - Potentiell för ORC
    'R601',      # Pentane
    'R601a',     # Isopentane
    
    # Oorganiska
    'Ammonia',   # NH3 - Klassiskt för ORC
    'CarbonDioxide',  # CO2
    'Water',     # H2O - Ångturbin
    'Air',
]
```

#### 2.1.4 Industriella/Speciella medier
```python
INDUSTRIELLA_MEDIA = [
    'Acetone', 'Benzene', 'Toluene',
    'MD2M', 'MD3M', 'MD4M', 'MDM',  # Siloxaner för ORC
    'D4', 'D5', 'D6',               # Siloxaner för ORC
    'MM',                           # Hexamethyldisiloxan
    'Ethanol', 'Methanol',
    'RC318',
]
```

#### 2.1.5 CoolProp-specifika namn
```python
COOLPROP_ALIASES = {
    'R1233zd(E)': 'R1233zd(E)',
    'R1234ze(Z)': 'R1234ze(Z)',
    'R1234ze(E)': 'R1234ze(E)',
    'IsoButane': 'R600a',
    'Isopentane': 'R601a',
}
```

### 2.2 Metadata för alla medier

Varje medium lagras med följande metadata:

```python
MEDIUM_METADATA = {
    'R1233zd(E)': {
        'fullname': '1-Chloro-3,3,3-trifluoroprop-1-ene',
        'formula': 'CHCl=CHCF3',
        'molar_mass': 130.5,  # g/mol
        'coolprop_name': 'R1233zd(E)',
        'ashrae_class': 'A1',
        'gwp': 7,
        'odp': 0,
        'boiling_point': 19.0,  # °C @ 1 atm
        'critical_temp': 165.6,  # °C
        'critical_pressure': 35.73,  # bar
        'category': 'HFO',
        'safety_notes': 'Ej brandfarlig, ej giftig, säkrast för heminstallation',
        'orc_suitability': 'EXCELLENT',  # EXCELLENT/GOOD/MODERATE/POOR
        'cost_relative': 1.03,  # Relativt R245fa
        'availability': 'GOOD',  # EXCELLENT/GOOD/MODERATE/LIMITED
    },
    
    'R245fa': {
        'fullname': '1,1,1,3,3-Pentafluoropropane',
        'formula': 'CF3CH2CHF2',
        'molar_mass': 134.05,
        'coolprop_name': 'R245fa',
        'ashrae_class': 'B1',
        'gwp': 1030,
        'odp': 0,
        'boiling_point': 15.3,
        'critical_temp': 154.01,
        'critical_pressure': 36.51,
        'category': 'HFC',
        'safety_notes': 'Lite toxisk (B1), fasas ut pga högt GWP',
        'orc_suitability': 'GOOD',
        'cost_relative': 1.00,
        'availability': 'EXCELLENT',
    },
    
    # ... Metadata för ALLA 130+ medier
}
```

### 2.3 Kategorisering av medier

Medier grupperas för enklare navigering:

```python
CATEGORIES = {
    'ORC_OPTIMAL': [
        'R1233zd(E)', 'R245fa', 'R1234ze(Z)', 
        'R600a', 'R601a', 'Ammonia',
        'Isopentane', 'n-Pentane',
        'Cyclopentane'
    ],
    
    'ORC_GOOD': [
        'R1234yf', 'R1234ze(E)', 'R1336mzz(Z)',
        'n-Butane', 'Propane'
    ],
    
    'ORC_MODERATE': [
        'R134a', 'R152a', 'R143a',
        'Ethanol', 'Methanol'
    ],
    
    'ORC_POOR': [
        'R22', 'R404A', 'R410A',
        'CarbonDioxide', 'Water'
    ],
    
    'MILJOVANLIGA_GWP<10': [
        'R1233zd(E)', 'R1234ze(Z)', 'R1234yf', 'R1234ze(E)',
        'Ammonia', 'Water', 'CO2', 'R600a', 'R600', 'R601', 'R601a'
    ],
    
    'SAKERHET_A1': [
        'R1233zd(E)', 'R134a', 'R227ea', 'R236fa', 'R245fa'
    ],
    
    'BRANDFARLIGA': [
        'R600a', 'R600', 'R601', 'R601a', 'R32', 'R1234yf',
        'Propane', 'n-Butane', 'IsoButane', 'Ammonia', 'Methane'
    ],
}
```

---

## 3. SORTERINGSFUNKTIONALITET

### 3.1 Sorteringskriterier

Användaren ska kunna sortera medier enligt följande parametrar:

#### 3.1.1 Termodynamiska egenskaper
```python
SORTERING_TERMODYNAMISK = {
    'kokpunkt_asc': 'Kokpunkt (låg → hög)',
    'kokpunkt_desc': 'Kokpunkt (hög → låg)',
    'tryck_50C_asc': 'Tryck @ 50°C (låg → hög)',
    'tryck_50C_desc': 'Tryck @ 50°C (hög → låg)',
    'tryck_20C_asc': 'Tryck @ 20°C (låg → hög)',
    'hfg_desc': 'Förångningsvärme (hög → låg)',
    'viskositet_asc': 'Viskositet (låg → hög)',
    'critical_temp_desc': 'Kritisk temperatur (hög → låg)',
}
```

#### 3.1.2 Miljö och säkerhet
```python
SORTERING_MILJO_SAKERHET = {
    'gwp_asc': 'GWP (låg → hög) - Miljövänligast först',
    'safety_desc': 'Säkerhet (A1 → B2L) - Säkrast först',
    'orc_suitability_desc': 'ORC-lämplighet (bäst → sämst)',
}
```

#### 3.1.3 Ekonomi och tillgänglighet
```python
SORTERING_EKONOMI = {
    'cost_asc': 'Kostnad (billig → dyr)',
    'availability_desc': 'Tillgänglighet (bäst → sämst)',
}
```

#### 3.1.4 ORC-specifika kriterier
```python
SORTERING_ORC_SPECIFIK = {
    'optimal_for_20_30C': 'Optimal för 20-30°C kokpunkt',
    'pressure_ratio_optimal': 'Bästa tryckförhållande (2.0-2.5)',
    'disk_gap_match': 'Passar TesTur diskavstånd (0.19-0.23 mm)',
    'total_score': 'Totalpoäng (viktad sammanställning)',
}
```

### 3.2 Sorteringsalgoritm

```python
def sortera_medier(medielist, sortering_typ, custom_temp=None):
    """
    Sorterar medier enligt valt kriterium
    
    Args:
        medielist: Lista med mediumnamn
        sortering_typ: Nyckel från SORTERING_*
        custom_temp: Anpassad temperatur för trycksortering (default 50°C)
    
    Returns:
        Sorterad lista med (medium, score, metadata)
    """
    
    resultlist = []
    
    for medium in medielist:
        try:
            # Hämta data från CoolProp
            data = hamta_termodynamisk_data(medium, custom_temp or 50)
            metadata = MEDIUM_METADATA.get(medium, {})
            
            # Beräkna sorteringsscore
            if sortering_typ == 'kokpunkt_asc':
                score = data['boiling_point']
            
            elif sortering_typ == 'optimal_for_20_30C':
                # Ju närmare 25°C kokpunkt, desto högre score
                bp = data['boiling_point']
                score = -abs(bp - 25.0)  # Negativ avvikelse
            
            elif sortering_typ == 'pressure_ratio_optimal':
                # Tryckförhållande närmast 2.0-2.5
                p_evap = data['pressure_50C']
                p_cond = data['pressure_20C']
                ratio = p_evap / p_cond
                if 2.0 <= ratio <= 2.5:
                    score = 1.0  # Perfekt
                else:
                    score = -abs(ratio - 2.25)  # Avvikelse från optimum
            
            elif sortering_typ == 'total_score':
                # Viktad totalpoäng
                score = berakna_total_score(medium, data, metadata)
            
            elif sortering_typ == 'gwp_asc':
                score = metadata.get('gwp', 9999)
            
            elif sortering_typ == 'safety_desc':
                # A1=4, A2L=3, B1=2, B2L=1
                safety_map = {'A1': 4, 'A2L': 3, 'B1': 2, 'B2L': 1}
                score = -safety_map.get(metadata.get('ashrae_class', 'B2L'), 0)
            
            resultlist.append({
                'medium': medium,
                'score': score,
                'data': data,
                'metadata': metadata
            })
        
        except Exception as e:
            print(f"Varning: Kunde inte hämta data för {medium}: {e}")
            continue
    
    # Sortera efter score (högst först)
    resultlist.sort(key=lambda x: x['score'], reverse=True)
    
    return resultlist
```

### 3.3 Totalpoäng-beräkning

```python
def berakna_total_score(medium, data, metadata):
    """
    Beräknar viktad totalpoäng för ORC-lämplighet
    
    Viktning:
    - Kokpunkt nära 20-30°C: 30%
    - Lågt tryck: 20%
    - Säkerhet (A1 bäst): 20%
    - Låg GWP: 15%
    - Hög förångningsvärme: 10%
    - Låg kostnad: 5%
    """
    
    score = 0
    
    # 1. Kokpunkt (30%) - Optimal: 20-30°C
    bp = data['boiling_point']
    if 20 <= bp <= 30:
        score += 30
    elif 15 <= bp < 20 or 30 < bp <= 35:
        score += 20
    elif 10 <= bp < 15 or 35 < bp <= 40:
        score += 10
    else:
        score += 0
    
    # 2. Tryck vid 50°C (20%) - Lägre = bättre
    p50 = data['pressure_50C']
    if p50 < 3.0:
        score += 20
    elif p50 < 5.0:
        score += 15
    elif p50 < 8.0:
        score += 10
    else:
        score += 5
    
    # 3. Säkerhet (20%)
    safety = metadata.get('ashrae_class', 'B2L')
    safety_points = {'A1': 20, 'A2L': 15, 'B1': 10, 'A2': 8, 'B2L': 5}
    score += safety_points.get(safety, 0)
    
    # 4. GWP (15%)
    gwp = metadata.get('gwp', 9999)
    if gwp < 10:
        score += 15
    elif gwp < 100:
        score += 12
    elif gwp < 1000:
        score += 8
    else:
        score += 3
    
    # 5. Förångningsvärme (10%)
    hfg = data.get('hfg_50C', 0)
    if hfg > 200:
        score += 10
    elif hfg > 150:
        score += 8
    else:
        score += 5
    
    # 6. Kostnad (5%)
    cost = metadata.get('cost_relative', 1.0)
    if cost < 1.05:
        score += 5
    elif cost < 1.15:
        score += 3
    else:
        score += 1
    
    return score
```

### 3.4 Filterfunktioner

Utöver sortering ska användaren kunna filtrera:

```python
FILTER_ALTERNATIV = {
    'kokpunkt_min': (None, '°C', 'Minimum kokpunkt'),
    'kokpunkt_max': (None, '°C', 'Maximum kokpunkt'),
    'tryck_50C_max': (None, 'bar', 'Max tryck @ 50°C'),
    'gwp_max': (None, '-', 'Max GWP'),
    'endast_A1': (False, 'bool', 'Endast A1-klassade'),
    'endast_miljovanliga': (False, 'bool', 'Endast GWP < 10'),
    'exkludera_brandfarliga': (False, 'bool', 'Exkludera A2L/A2/A3'),
    'endast_orc_optimal': (False, 'bool', 'Endast ORC EXCELLENT/GOOD'),
}

def filtrera_medier(medielist, filters):
    """Applicerar filter på mediumlista"""
    filtered = []
    
    for medium in medielist:
        metadata = MEDIUM_METADATA.get(medium, {})
        
        # Kokpunkt filter
        bp = metadata.get('boiling_point', 0)
        if filters.get('kokpunkt_min') and bp < filters['kokpunkt_min']:
            continue
        if filters.get('kokpunkt_max') and bp > filters['kokpunkt_max']:
            continue
        
        # Tryck filter
        if filters.get('tryck_50C_max'):
            # Behöver hämta från CoolProp
            pass
        
        # GWP filter
        if filters.get('gwp_max'):
            gwp = metadata.get('gwp', 9999)
            if gwp > filters['gwp_max']:
                continue
        
        # Säkerhet filter
        if filters.get('endast_A1'):
            if metadata.get('ashrae_class') != 'A1':
                continue
        
        # Miljö filter
        if filters.get('endast_miljovanliga'):
            if metadata.get('gwp', 9999) >= 10:
                continue
        
        # Brandfarlighet filter
        if filters.get('exkludera_brandfarliga'):
            safety = metadata.get('ashrae_class', '')
            if 'A2' in safety or 'A3' in safety:
                continue
        
        # ORC-lämplighet filter
        if filters.get('endast_orc_optimal'):
            suitability = metadata.get('orc_suitability', 'POOR')
            if suitability not in ['EXCELLENT', 'GOOD']:
                continue
        
        filtered.append(medium)
    
    return filtered
```

---

## 4. INTERAKTIV GUI (DETALJERAD)

### 4.1 Huvudlayout (Streamlit-baserad)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  🔬 TESLA-TURBIN ORC - ARBETSMEDIUMANALYS                                ║
║  Automatisk jämförelse av 130+ medier med CoolProp                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  📋 STEG 1: VÄLJ MEDIER                                                   ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ Sortera efter: [Kokpunkt nära 20-30°C ▼]  [Applicera sortering]  │  ║
║  │                                                                     │  ║
║  │ Filter:  [Kokpunkt 10-40°C] [GWP < 100] [☑ Endast A1]            │  ║
║  │          [☐ Exkludera brandfarliga] [☑ ORC-optimal/good]          │  ║
║  │                                                                     │  ║
║  │ Snabbval:  [ORC-Optimal (9)] [Miljövänliga GWP<10] [Alla (130+)] │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌─────────────────────────── MEDIUMLISTA ────────────────────────────┐  ║
║  │  #  │ Medium        │ Kokp. │ P@50°C │ GWP  │ Säk. │ Score │ Välj │  ║
║  │─────┼───────────────┼───────┼────────┼──────┼──────┼───────┼──────│  ║
║  │  1  │ R1233zd(E)    │ 19.0  │ 2.48   │   7  │  A1  │  88   │  ☑   │  ║
║  │  2  │ R245fa        │ 15.3  │ 3.44   │ 1030 │  B1  │  74   │  ☑   │  ║
║  │  3  │ R1234ze(Z)    │  9.8  │ 5.62   │   1  │ A2L  │  72   │  ☑   │  ║
║  │  4  │ R600a         │ -11.7 │ 5.40   │   3  │  A3  │  64   │  ☐   │  ║
║  │  5  │ Isopentane    │ 27.8  │ 1.98   │   3  │  A3  │  68   │  ☐   │  ║
║  │ ... │ (125+ medier) │       │        │      │      │       │      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  [Välj alla synliga] [Avmarkera alla] [Invertera val]                    ║
║                                                                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ⚙️ STEG 2: DRIFTBETINGELSER                                              ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Kondenseringstemperatur:  [20]°C  ◄───────────►  (10-30°C)       │  ║
║  │  Förångningstemperatur:    [50]°C  ◄───────────►  (30-80°C)       │  ║
║  │                                                                     │  ║
║  │  Tryckförhållande valda medier: 1.98 - 2.80  [Optimal: 2.0-2.5]  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  🔧 TURBINPARAMETRAR                                                      ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  Diskdiameter:           [254] mm                                  │  ║
║  │  Antal diskar:           [75]                                      │  ║
║  │  Diskavstånd (önskat):   [0.234] mm  (TesTur referens)           │  ║
║  │  Önskad effekt:          [2000] W                                  │  ║
║  │                                                                     │  ║
║  │  💡 Beräknat diskavstånd för valda medier: 0.18-0.20 mm          │  ║
║  │     ⚠️ Avvikelse från TesTur: -18% till -15%                      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  📊 STEG 3: VÄLJ DIAGRAM                                                  ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  [☑] P-T kurvor (saturerade)      [☑] Tryckförhållande           │  ║
║  │  [☑] GWP-jämförelse               [☑] Viskositet vs temp          │  ║
║  │  [☑] Förångningsvärme             [☐] Carnot-effektivitet         │  ║
║  │  [☑] Säkerhetsmatrix              [☑] Kostnadsanalys              │  ║
║  │  [☑] Spindeldiagram (total)       [☐] T-s diagram                 │  ║
║  │  [☑] Detaljerad tabell            [☐] h-s diagram (Mollier)       │  ║
║  │                                                                     │  ║
║  │  Visa endast valt diagram: [P-T kurvor ▼]                         │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  [🔄 GENERERA ANALYS]  [📄 EXPORTERA PDF]  [💾 SPARA ALLA DIAGRAM]      ║
║                                                                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  📈 RESULTATPANEL - LIVE PREVIEW                                          ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │                                                                     │  ║
║  │              [INTERAKTIVT DIAGRAM VISAS HÄR]                       │  ║
║  │                                                                     │  ║
║  │  • Hover för detaljerad data                                       │  ║
║  │  • Klick för att dölja/visa kurva                                  │  ║
║  │  • Zoom med mushjul                                                │  ║
║  │                                                                     │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  📊 SAMMANFATTNING FÖR VALDA MEDIER                                       ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  🥇 BÄST (totalpoäng): R1233zd(E) - 88/100                         │  ║
║  │     ✓ Kokpunkt 19.0°C (optimal zon)                                │  ║
║  │     ✓ Lägst tryck (2.48 bar @ 50°C)                                │  ║
║  │     ✓ Säkrast (A1)                                                 │  ║
║  │     ✓ Miljövänligast (GWP 7)                                       │  ║
║  │                                                                     │  ║
║  │  🥈 TVÅA: R245fa - 74/100                                          │  ║
║  │     ✓ Bäst tillgänglighet                                          │  ║
║  │     ✓ Mest dokumenterad (>20 år ORC)                               │  ║
║  │     ⚠️ Högt GWP (1030), fasas ut                                   │  ║
║  │                                                                     │  ║
║  │  🥉 TREA: R1234ze(Z) - 72/100                                      │  ║
║  │     ✓ Extremt låg GWP (<1)                                         │  ║
║  │     ⚠️ A2L kräver säkerhetsanalys                                  │  ║
║  │     ⚠️ Högre tryck (5.62 bar)                                      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 4.2 Streamlit implementation

```python
import streamlit as st
import CoolProp.CoolProp as CP
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfiguration
st.set_page_config(
    page_title="Tesla-Turbin ORC Analys",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titel
st.title("🔬 TESLA-TURBIN ORC - ARBETSMEDIUMANALYS")
st.caption("Automatisk jämförelse av 130+ medier med CoolProp")

# Sidebar för inställningar
with st.sidebar:
    st.header("⚙️ Inställningar")
    
    # Temperaturinställningar
    st.subheader("Driftbetingelser")
    T_cond = st.slider("Kondensering (°C)", 10, 30, 20)
    T_evap = st.slider("Förångning (°C)", 30, 80, 50)
    
    # Turbinparametrar
    st.subheader("Turbinparametrar")
    disk_diameter = st.number_input("Diskdiameter (mm)", 100, 500, 254)
    num_disks = st.number_input("Antal diskar", 10, 150, 75)
    target_power = st.number_input("Önskad effekt (W)", 500, 5000, 2000)

# Huvudinnehåll
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Välj medier", 
    "📊 Diagram", 
    "📈 Detaljanalys",
    "📄 Exportera"
])

with tab1:
    st.header("STEG 1: Välj arbetsmedier")
    
    # Sortering
    col1, col2 = st.columns([3, 1])
    with col1:
        sort_option = st.selectbox(
            "Sortera efter:",
            [
                "Kokpunkt nära 20-30°C (bäst först)",
                "Kokpunkt (låg → hög)",
                "Tryck @ 50°C (låg → hög)",
                "GWP (låg → hög) - Miljövänligast",
                "Säkerhet (A1 bäst)",
                "Totalpoäng (ORC-lämplighet)",
                "Kostnad (billig → dyr)",
                "Alfabetisk"
            ]
        )
    with col2:
        if st.button("🔄 Applicera sortering", use_container_width=True):
            st.rerun()
    
    # Filter
    st.subheader("Filter")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_bp_min = st.number_input("Min kokpunkt (°C)", -50, 50, 10)
        filter_bp_max = st.number_input("Max kokpunkt (°C)", -50, 50, 40)
    
    with col2:
        filter_gwp_max = st.number_input("Max GWP", 0, 10000, 1000)
        filter_only_a1 = st.checkbox("Endast A1-klassade")
    
    with col3:
        filter_eco_friendly = st.checkbox("Endast miljövänliga (GWP<10)")
        filter_no_flammable = st.checkbox("Exkludera brandfarliga")
    
    with col4:
        filter_orc_optimal = st.checkbox("Endast ORC-optimala", value=True)
    
    # Snabbval
    st.subheader("Snabbval")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("ORC-Optimal (9 medier)", use_container_width=True):
            st.session_state.selected_media = CATEGORIES['ORC_OPTIMAL']
    with col2:
        if st.button("Miljövänliga GWP<10", use_container_width=True):
            st.session_state.selected_media = CATEGORIES['MILJOVANLIGA_GWP<10']
    with col3:
        if st.button("Säkrast (A1)", use_container_width=True):
            st.session_state.selected_media = CATEGORIES['SAKERHET_A1']
    with col4:
        if st.button("Visa alla (130+)", use_container_width=True):
            st.session_state.show_all = True
    
    # Mediumtabell
    st.subheader("Tillgängliga medier")
    
    # Filtrera och sortera medier
    filtered_media = filtrera_och_sortera_medier(
        sort_option, 
        filter_bp_min, filter_bp_max, 
        filter_gwp_max, filter_only_a1,
        filter_eco_friendly, filter_no_flammable,
        filter_orc_optimal
    )
    
    # Skapa DataFrame för display
    df_media = skapa_medium_dataframe(filtered_media, T_evap)
    
    # Interaktiv tabell
    selected_rows = st.data_editor(
        df_media,
        column_config={
            "Välj": st.column_config.CheckboxColumn(
                "Välj",
                default=False,
            ),
            "Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=100,
            ),
        },
        disabled=["Medium", "Kokpunkt", "Tryck@50°C", "GWP", "Säkerhet", "Score"],
        hide_index=True,
        use_container_width=True
    )
    
    # Hämta valda medier
    selected_media = df_media[selected_rows["Välj"]]["Medium"].tolist()
    st.info(f"✅ {len(selected_media)} medier valda")

with tab2:
    st.header("📊 Diagram och visualiseringar")
    
    if len(selected_media) == 0:
        st.warning("⚠️ Välj minst ett medium i Tab 1")
    else:
        # Diagramval
        col1, col2, col3 = st.columns(3)
        with col1:
            show_pt = st.checkbox("P-T kurvor", value=True)
            show_pressure_ratio = st.checkbox("Tryckförhållande", value=True)
            show_gwp = st.checkbox("GWP-jämförelse", value=True)
        
        with col2:
            show_viscosity = st.checkbox("Viskositet vs temp", value=True)
            show_hfg = st.checkbox("Förångningsvärme", value=True)
            show_safety = st.checkbox("Säkerhetsmatrix", value=True)
        
        with col3:
            show_spider = st.checkbox("Spindeldiagram", value=True)
            show_table = st.checkbox("Detaljerad tabell", value=True)
        
        # Generera valda diagram
        if show_pt:
            st.subheader("P-T Kurvor (Saturerade)")
            fig_pt = generera_pt_diagram(selected_media, T_cond, T_evap)
            st.plotly_chart(fig_pt, use_container_width=True)
        
        if show_pressure_ratio:
            st.subheader("Tryckförhållande")
            fig_pr = generera_pressure_ratio_diagram(selected_media, T_cond, T_evap)
            st.plotly_chart(fig_pr, use_container_width=True)
        
        # ... fler diagram

with tab3:
    st.header("📈 Detaljanalys")
    # Detaljerad analys av valda medier

with tab4:
    st.header("📄 Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generera PDF-rapport", use_container_width=True):
            pdf_file = generera_pdf_rapport(selected_media, T_cond, T_evap)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇️ Ladda ner PDF",
                    f,
                    file_name="Arbetsmediumanalys.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    with col2:
        if st.button("💾 Spara alla diagram (PNG)", use_container_width=True):
            zip_file = spara_alla_diagram(selected_media)
            with open(zip_file, "rb") as f:
                st.download_button(
                    "⬇️ Ladda ner ZIP",
                    f,
                    file_name="Diagram.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    
    with col3:
        if st.button("📊 Exportera data (CSV)", use_container_width=True):
            csv_file = exportera_csv(selected_media, T_cond, T_evap)
            st.download_button(
                "⬇️ Ladda ner CSV",
                csv_file,
                file_name="Mediumdata.csv",
                mime="text/csv",
                use_container_width=True
            )
```

---

## 5. AUTOMATISK DATAHÄMTNING

### 5.1 CoolProp-interface

```python
import CoolProp.CoolProp as CP
import numpy as np
from typing import Dict, List, Tuple
import warnings

class CoolPropDataHandler:
    """Hanterar automatisk datahämtning från CoolProp"""
    
    def __init__(self):
        self.cache = {}  # Cache för prestanda
        self.failed_media = []  # Medier som CoolProp inte stödjer
    
    def hamta_fullstandig_data(self, medium: str, temp_range: np.ndarray) -> Dict:
        """
        Hämtar komplett termodynamisk data för ett medium
        
        Args:
            medium: CoolProp-namn (t.ex. 'R1233zd(E)')
            temp_range: Temperaturvektor i °C
        
        Returns:
            Dictionary med alla termodynamiska egenskaper
        """
        
        cache_key = f"{medium}_{temp_range[0]}_{temp_range[-1]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            data = {
                'medium': medium,
                'temp_C': temp_range,
                'pressure_bar': [],
                'density_liquid_kg_m3': [],
                'density_vapor_kg_m3': [],
                'enthalpy_fg_kJ_kg': [],
                'entropy_fg_kJ_kgK': [],
                'viscosity_vapor_uPas': [],
                'viscosity_liquid_uPas': [],
                'thermal_cond_vapor_W_mK': [],
                'cp_vapor_kJ_kgK': [],
                'surface_tension_N_m': [],
            }
            
            # Hämta kritiska egenskaper
            T_crit_K = CP.PropsSI('Tcrit', medium)
            P_crit_Pa = CP.PropsSI('Pcrit', medium)
            
            data['T_critical_C'] = T_crit_K - 273.15
            data['P_critical_bar'] = P_crit_Pa / 1e5
            data['T_triple_C'] = CP.PropsSI('Ttriple', medium) - 273.15
            
            # Beräkna kokpunkt vid 1 atm
            try:
                T_boil_K = CP.PropsSI('T', 'P', 101325, 'Q', 0, medium)
                data['boiling_point_C'] = T_boil_K - 273.15
            except:
                data['boiling_point_C'] = None
            
            # Loopa över temperaturer
            for T_C in temp_range:
                T_K = T_C + 273.15
                
                # Skippa om över kritisk temperatur
                if T_K >= T_crit_K:
                    continue
                
                try:
                    # Saturerade egenskaper
                    P = CP.PropsSI('P', 'T', T_K, 'Q', 1, medium)
                    rho_l = CP.PropsSI('D', 'T', T_K, 'Q', 0, medium)
                    rho_v = CP.PropsSI('D', 'T', T_K, 'Q', 1, medium)
                    h_l = CP.PropsSI('H', 'T', T_K, 'Q', 0, medium)
                    h_v = CP.PropsSI('H', 'T', T_K, 'Q', 1, medium)
                    s_l = CP.PropsSI('S', 'T', T_K, 'Q', 0, medium)
                    s_v = CP.PropsSI('S', 'T', T_K, 'Q', 1, medium)
                    mu_v = CP.PropsSI('V', 'T', T_K, 'Q', 1, medium)
                    mu_l = CP.PropsSI('V', 'T', T_K, 'Q', 0, medium)
                    k_v = CP.PropsSI('L', 'T', T_K, 'Q', 1, medium)
                    cp_v = CP.PropsSI('C', 'T', T_K, 'Q', 1, medium)
                    sigma = CP.PropsSI('I', 'T', T_K, 'Q', 0, medium)
                    
                    # Konvertera enheter
                    data['pressure_bar'].append(P / 1e5)
                    data['density_liquid_kg_m3'].append(rho_l)
                    data['density_vapor_kg_m3'].append(rho_v)
                    data['enthalpy_fg_kJ_kg'].append((h_v - h_l) / 1000)
                    data['entropy_fg_kJ_kgK'].append((s_v - s_l) / 1000)
                    data['viscosity_vapor_uPas'].append(mu_v * 1e6)
                    data['viscosity_liquid_uPas'].append(mu_l * 1e6)
                    data['thermal_cond_vapor_W_mK'].append(k_v)
                    data['cp_vapor_kJ_kgK'].append(cp_v / 1000)
                    data['surface_tension_N_m'].append(sigma)
                
                except Exception as e:
                    warnings.warn(f"Kunde inte hämta data för {medium} @ {T_C}°C: {e}")
                    continue
            
            # Cacha resultat
            self.cache[cache_key] = data
            
            return data
        
        except Exception as e:
            print(f"❌ Fel för {medium}: {e}")
            self.failed_media.append(medium)
            return None
    
    def hamta_enskild_egenskap(self, medium: str, property_name: str, 
                                T_C: float, P_bar: float = None) -> float:
        """
        Hämtar en enskild egenskap vid specifikt tillstånd
        
        Args:
            medium: CoolProp-namn
            property_name: 'P', 'D', 'H', 'S', 'V', 'L', 'C', etc.
            T_C: Temperatur i °C
            P_bar: Tryck i bar (optional)
        
        Returns:
            Egenskap i SI-enheter
        """
        
        T_K = T_C + 273.15
        
        if P_bar:
            P_Pa = P_bar * 1e5
            value = CP.PropsSI(property_name, 'T', T_K, 'P', P_Pa, medium)
        else:
            # Saturerade egenskaper (Q=1 för ånga)
            value = CP.PropsSI(property_name, 'T', T_K, 'Q', 1, medium)
        
        return value
    
    def berakna_diskavstand(self, medium: str, T_C: float) -> float:
        """
        Beräknar optimalt diskavstånd från viskositet
        Baserat på Huber et al. 2003 och TesTur-data
        
        Formula: s_opt = 0.012 * sqrt(μ)  [mm]
        där μ är viskositet i μPa·s
        """
        
        mu_vapor = self.hamta_enskild_egenskap(medium, 'V', T_C)
        mu_uPas = mu_vapor * 1e6
        
        s_opt_mm = 0.012 * np.sqrt(mu_uPas)
        
        return s_opt_mm
    
    def lista_alla_tillgangliga_medier(self) -> List[str]:
        """Returnerar lista över alla medier CoolProp stödjer"""
        
        fluids = CP.get_global_param_string("fluids_list").split(',')
        return sorted(fluids)
    
    def validera_medium(self, medium: str) -> Tuple[bool, str]:
        """
        Validerar om medium finns i CoolProp
        
        Returns:
            (giltig, meddelande)
        """
        
        try:
            T_crit = CP.PropsSI('Tcrit', medium)
            return (True, f"✓ {medium} tillgängligt")
        except:
            return (False, f"❌ {medium} ej tillgängligt i CoolProp")
```

### 5.2 Felhantering och validering

```python
class DataValidator:
    """Validerar och rensar termodynamisk data"""
    
    @staticmethod
    def validera_temperaturomrade(T_C: float, medium: str) -> bool:
        """Kontrollerar om temperatur är inom giltigt område"""
        
        T_triple = CP.PropsSI('Ttriple', medium) - 273.15
        T_crit = CP.PropsSI('Tcrit', medium) - 273.15
        
        if T_C < T_triple:
            raise ValueError(f"{medium}: T={T_C}°C under trippelpunkt ({T_triple:.1f}°C)")
        
        if T_C >= T_crit:
            raise ValueError(f"{medium}: T={T_C}°C över kritisk temp ({T_crit:.1f}°C)")
        
        return True
    
    @staticmethod
    def validera_tryck(P_bar: float, medium: str, T_C: float) -> bool:
        """Kontrollerar om tryck är realistiskt"""
        
        P_sat_bar = CP.PropsSI('P', 'T', T_C + 273.15, 'Q', 0, medium) / 1e5
        
        if P_bar < P_sat_bar * 0.9:
            warnings.warn(f"{medium}: Tryck {P_bar:.2f} bar under mättningstryck")
        
        if P_bar > 50:
            warnings.warn(f"{medium}: Högt tryck {P_bar:.2f} bar - säkerhetsrisk")
        
        return True
    
    @staticmethod
    def rensa_outliers(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """Tar bort outliers med z-score metod"""
        
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        return data[z_scores < threshold]
```

---

## 6. BERÄKNINGSMOTOR

### 6.1 Termodynamiska beräkningar

```python
class ORCCalculator:
    """Beräknar ORC-systemparametrar"""
    
    def __init__(self, medium: str, T_evap_C: float, T_cond_C: float):
        self.medium = medium
        self.T_evap_C = T_evap_C
        self.T_cond_C = T_cond_C
        self.data_handler = CoolPropDataHandler()
    
    def carnot_effektivitet(self) -> float:
        """Beräknar teoretisk Carnot-effektivitet"""
        
        T_evap_K = self.T_evap_C + 273.15
        T_cond_K = self.T_cond_C + 273.15
        
        eta_carnot = 1 - (T_cond_K / T_evap_K)
        
        return eta_carnot
    
    def isentropisk_verkningsgrad(self, typ: str = 'konservativ') -> float:
        """
        Uppskattar isentropisk verkningsgrad för Tesla-turbin
        
        Baserat på:
        - TesTur experimentella data: 30-40%
        - MDPI CFD-simuleringar: 45-55%
        - Teoretiskt max (Carnot): 60-70%
        """
        
        if typ == 'konservativ':
            return 0.35  # Konservativ (TesTur lägsta)
        elif typ == 'realistisk':
            return 0.45  # Realistisk (TesTur medel)
        elif typ == 'optimistisk':
            return 0.55  # Optimistisk (MDPI simuleringar)
        else:
            return 0.40  # Default
    
    def tryckforhallande(self) -> float:
        """Beräknar tryckförhållande P_evap / P_cond"""
        
        P_evap = self.data_handler.hamta_enskild_egenskap(
            self.medium, 'P', self.T_evap_C
        ) / 1e5
        
        P_cond = self.data_handler.hamta_enskild_egenskap(
            self.medium, 'P', self.T_cond_C
        ) / 1e5
        
        return P_evap / P_cond
    
    def massflode_for_effekt(self, P_target_W: float, 
                              eta_pump: float = 0.7,
                              eta_generator: float = 0.9) -> float:
        """
        Beräknar massflöde för önskad effekt
        
        Args:
            P_target_W: Måleffekt i W
            eta_pump: Pumpverkningsgrad
            eta_generator: Generatorverkningsgrad
        
        Returns:
            Massflöde i kg/s
        """
        
        # Hämta entalpier
        h_1 = CP.PropsSI('H', 'T', self.T_cond_C + 273.15, 'Q', 0, self.medium) / 1000  # kJ/kg
        h_2 = h_1  # Isentropisk pump (försumbar höjning)
        h_3 = CP.PropsSI('H', 'T', self.T_evap_C + 273.15, 'Q', 1, self.medium) / 1000
        
        # Isentropisk expansion
        s_3 = CP.PropsSI('S', 'T', self.T_evap_C + 273.15, 'Q', 1, self.medium)
        h_4s = CP.PropsSI('H', 'P', CP.PropsSI('P', 'T', self.T_cond_C + 273.15, 'Q', 0, self.medium), 
                          'S', s_3, self.medium) / 1000
        
        # Verklig expansion
        eta_is = self.isentropisk_verkningsgrad('realistisk')
        h_4 = h_3 - eta_is * (h_3 - h_4s)
        
        # Turbin arbete
        W_turb = h_3 - h_4  # kJ/kg
        
        # Pump arbete
        v_1 = 1 / CP.PropsSI('D', 'T', self.T_cond_C + 273.15, 'Q', 0, self.medium)  # m³/kg
        P_evap_Pa = CP.PropsSI('P', 'T', self.T_evap_C + 273.15, 'Q', 0, self.medium)
        P_cond_Pa = CP.PropsSI('P', 'T', self.T_cond_C + 273.15, 'Q', 0, self.medium)
        W_pump = v_1 * (P_evap_Pa - P_cond_Pa) / 1000 / eta_pump  # kJ/kg
        
        # Netto arbete
        W_net = W_turb - W_pump
        
        # Massflöde
        m_dot = (P_target_W / 1000) / (W_net * eta_generator)  # kg/s
        
        return m_dot
    
    def varmevaxlare_area(self, Q_dot_W: float, U_W_m2K: float, 
                          LMTD_K: float) -> float:
        """
        Beräknar värmeväxlarearea
        
        Args:
            Q_dot_W: Värmeöverföring i W
            U_W_m2K: Värmeöverföringskoefficient W/(m²·K)
            LMTD_K: Log Mean Temperature Difference i K
        
        Returns:
            Area i m²
        """
        
        A_m2 = Q_dot_W / (U_W_m2K * LMTD_K)
        
        return A_m2
    
    def ekonomisk_analys(self, drifttimmar_per_ar: int = 4000) -> Dict:
        """
        Enkel ekonomisk analys
        
        Returns:
            Dictionary med kostnader och payback
        """
        
        # Komponentkostnader (uppskattningar)
        cost_turbin = 3000  # €
        cost_evaporator = 2000
        cost_condenser = 1500
        cost_pump = 500
        cost_medium_per_kg = 20 * MEDIUM_METADATA[self.medium].get('cost_relative', 1.0)
        
        # Massflöde och fyllnadsmängd
        m_dot = self.massflode_for_effekt(2000)  # kg/s
        m_total_kg = m_dot * 60 * 5  # 5 minuter bufferttid
        
        cost_medium = m_total_kg * cost_medium_per_kg
        
        total_capex = cost_turbin + cost_evaporator + cost_condenser + cost_pump + cost_medium
        
        # Årlig elproduktion
        P_avg_W = 2000  # Genomsnitt
        E_year_kWh = (P_avg_W / 1000) * drifttimmar_per_ar
        
        # Intäkter (0.15 €/kWh spotpris)
        revenue_year = E_year_kWh * 0.15
        
        # Payback
        payback_years = total_capex / revenue_year
        
        return {
            'capex_total': total_capex,
            'medium_cost': cost_medium,
            'medium_kg': m_total_kg,
            'energy_year_kWh': E_year_kWh,
            'revenue_year': revenue_year,
            'payback_years': payback_years
        }
```

---

## 7. DYNAMISK DIAGRAMGENERERING

### 7.1 Interaktiva Plotly-diagram

```python
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class DiagramGenerator:
    """Genererar interaktiva Plotly-diagram"""
    
    def __init__(self, media_list: List[str], T_cond: float, T_evap: float):
        self.media_list = media_list
        self.T_cond = T_cond
        self.T_evap = T_evap
        self.data_handler = CoolPropDataHandler()
        self.colors = px.colors.qualitative.Plotly
    
    def pt_kurvor(self) -> go.Figure:
        """Genererar P-T diagram med saturerade kurvor"""
        
        fig = go.Figure()
        
        temp_range = np.linspace(10, 80, 100)
        
        for i, medium in enumerate(self.media_list):
            data = self.data_handler.hamta_fullstandig_data(medium, temp_range)
            
            if data is None:
                continue
            
            color = self.colors[i % len(self.colors)]
            
            # Plottar P-T kurva
            fig.add_trace(go.Scatter(
                x=data['temp_C'],
                y=data['pressure_bar'],
                mode='lines+markers',
                name=medium,
                line=dict(color=color, width=3),
                marker=dict(size=4, symbol='circle'),
                hovertemplate=(
                    f"<b>{medium}</b><br>" +
                    "T: %{x:.1f}°C<br>" +
                    "P: %{y:.2f} bar<br>" +
                    "<extra></extra>"
                )
            ))
            
            # Markera arbetstemperaturer
            if self.T_evap in temp_range:
                idx = np.abs(temp_range - self.T_evap).argmin()
                fig.add_trace(go.Scatter(
                    x=[self.T_evap],
                    y=[data['pressure_bar'][idx]],
                    mode='markers',
                    marker=dict(size=12, color=color, symbol='star'),
                    showlegend=False,
                    hovertemplate=f"Förångning: {self.T_evap}°C<extra></extra>"
                ))
        
        # Markera arbetsområden
        fig.add_vrect(
            x0=30, x1=80,
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Förångning", annotation_position="top left"
        )
        
        fig.add_vrect(
            x0=10, x1=30,
            fillcolor="blue", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Kondensering", annotation_position="top left"
        )
        
        fig.update_layout(
            title="Saturerade Tryck-Temperatur Kurvor",
            xaxis_title="Temperatur (°C)",
            yaxis_title="Mättningstryck (bar)",
            hovermode='closest',
            template='plotly_white',
            legend=dict(x=0.02, y=0.98),
            height=600
        )
        
        fig.update_xaxis(range=[10, 80], gridcolor='lightgray')
        fig.update_yaxis(gridcolor='lightgray')
        
        return fig
    
    def tryckforhallande_diagram(self) -> go.Figure:
        """Genererar diagram över tryckförhållande"""
        
        data_list = []
        
        for medium in self.media_list:
            calc = ORCCalculator(medium, self.T_evap, self.T_cond)
            ratio = calc.tryckforhallande()
            
            data_list.append({
                'Medium': medium,
                'Tryckförhållande': ratio,
                'Bedömning': 'OPTIMAL' if 2.0 <= ratio <= 2.5 else 
                             'GODTAGBAR' if 1.5 <= ratio < 2.0 or 2.5 < ratio <= 3.0 else 
                             'DÅLIG'
            })
        
        df = pd.DataFrame(data_list)
        df = df.sort_values('Tryckförhållande', ascending=False)
        
        fig = px.bar(
            df,
            x='Medium',
            y='Tryckförhållande',
            color='Bedömning',
            color_discrete_map={'OPTIMAL': 'green', 'GODTAGBAR': 'orange', 'DÅLIG': 'red'},
            title=f"Tryckförhållande vid T_cond={self.T_cond}°C, T_evap={self.T_evap}°C"
        )
        
        # Markera optimal zon
        fig.add_hline(y=2.0, line_dash="dash", line_color="green", 
                      annotation_text="Optimal min (2.0)")
        fig.add_hline(y=2.5, line_dash="dash", line_color="green",
                      annotation_text="Optimal max (2.5)")
        
        fig.update_layout(
            yaxis_title="P_evap / P_cond",
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def spindeldiagram(self) -> go.Figure:
        """Genererar spindeldiagram (radar chart)"""
        
        fig = go.Figure()
        
        categories = ['Kokpunkt\n(20-30°C)', 'Lågt tryck', 'Säkerhet', 
                      'Miljö (GWP)', 'Förångningsvärme', 'Kostnad']
        
        for i, medium in enumerate(self.media_list):
            metadata = MEDIUM_METADATA.get(medium, {})
            data = self.data_handler.hamta_fullstandig_data(medium, np.array([50]))
            
            # Normalisera scores (0-10)
            scores = [
                max(0, 10 - abs(metadata.get('boiling_point', 25) - 25) * 0.5),  # Kokpunkt
                max(0, 10 - (data['pressure_bar'][0] - 2.0) * 2),  # Tryck
                {'A1': 10, 'A2L': 7, 'B1': 5, 'B2L': 3}.get(metadata.get('ashrae_class', 'B2L'), 3),
                10 if metadata.get('gwp', 9999) < 10 else 5,  # GWP
                (data['enthalpy_fg_kJ_kg'][0] - 150) / 10,  # hfg
                10 - (metadata.get('cost_relative', 1.0) - 1.0) * 50  # Kostnad
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],  # Stäng polygon
                theta=categories + [categories[0]],
                fill='toself',
                name=medium,
                line_color=self.colors[i % len(self.colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            title="Sammansatt Bedömning (Spindeldiagram)",
            height=600
        )
        
        return fig
    
    def jamforelsetabell(self) -> pd.DataFrame:
        """Skapar detaljerad jämförelsetabell"""
        
        rows = []
        
        for medium in self.media_list:
            metadata = MEDIUM_METADATA.get(medium, {})
            data = self.data_handler.hamta_fullstandig_data(medium, np.array([20, 50]))
            calc = ORCCalculator(medium, self.T_evap, self.T_cond)
            
            if data is None:
                continue
            
            row = {
                'Medium': medium,
                'Kokpunkt (°C)': metadata.get('boiling_point', '-'),
                'P @ 50°C (bar)': f"{data['pressure_bar'][1]:.2f}",
                'P @ 20°C (bar)': f"{data['pressure_bar'][0]:.2f}",
                'Tryckförh.': f"{calc.tryckforhallande():.2f}",
                'hfg @ 50°C (kJ/kg)': f"{data['enthalpy_fg_kJ_kg'][1]:.0f}",
                'μ @ 50°C (μPa·s)': f"{data['viscosity_vapor_uPas'][1]:.1f}",
                'Diskavstånd (mm)': f"{self.data_handler.berakna_diskavstand(medium, 50):.2f}",
                'ASHRAE': metadata.get('ashrae_class', '-'),
                'GWP': metadata.get('gwp', '-'),
                'Kostnad': f"{metadata.get('cost_relative', 1.0):.2f}x",
                'ORC-lämplighet': metadata.get('orc_suitability', '-')
            }
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df
```

---

## 8. EXPORTFUNKTIONER

### 8.1 PDF-rapportgenerering

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime

class PDFExporter:
    """Genererar professionella PDF-rapporter"""
    
    def __init__(self, media_list: List[str], T_cond: float, T_evap: float):
        self.media_list = media_list
        self.T_cond = T_cond
        self.T_evap = T_evap
        self.diagram_gen = DiagramGenerator(media_list, T_cond, T_evap)
    
    def generera_rapport(self, filename: str = "Arbetsmediumanalys.pdf") -> str:
        """
        Genererar komplett PDF-rapport
        
        Returns:
            Sökväg till genererad PDF
        """
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Anpassad rubrikstil
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Titel
        story.append(Paragraph("ARBETSMEDIUMANALYS", title_style))
        story.append(Paragraph("Tesla-Turbin ORC-System", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Metadata
        metadata_text = f"""
        <b>Datum:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>
        <b>Antal jämförda medier:</b> {len(self.media_list)}<br/>
        <b>Kondenseringstemperatur:</b> {self.T_cond}°C<br/>
        <b>Förångningstemperatur:</b> {self.T_evap}°C<br/>
        """
        story.append(Paragraph(metadata_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Sammanfattning
        story.append(Paragraph("1. SAMMANFATTNING", styles['Heading1']))
        best_medium = self._hitta_basta_medium()
        summary_text = f"""
        Baserat på automatisk analys av termodynamiska egenskaper från CoolProp-databasen
        rekommenderas <b>{best_medium}</b> som det mest lämpliga arbetsmediet för detta ORC-system.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Jämförelsetabell
        story.append(Paragraph("2. JÄMFÖRELSETABELL", styles['Heading1']))
        df = self.diagram_gen.jamforelsetabell()
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(PageBreak())
        
        # Diagram
        story.append(Paragraph("3. TERMODYNAMISKA DIAGRAM", styles['Heading1']))
        
        # Spara diagram som bilder
        fig_pt = self.diagram_gen.pt_kurvor()
        fig_pt.write_image("temp_pt.png", width=800, height=600)
        story.append(Image("temp_pt.png", width=180*mm, height=135*mm))
        story.append(Spacer(1, 10))
        
        fig_ratio = self.diagram_gen.tryckforhallande_diagram()
        fig_ratio.write_image("temp_ratio.png", width=800, height=600)
        story.append(Image("temp_ratio.png", width=180*mm, height=135*mm))
        story.append(PageBreak())
        
        fig_spider = self.diagram_gen.spindeldiagram()
        fig_spider.write_image("temp_spider.png", width=800, height=600)
        story.append(Image("temp_spider.png", width=180*mm, height=135*mm))
        
        # Detaljerad analys för varje medium
        story.append(PageBreak())
        story.append(Paragraph("4. DETALJANALYS PER MEDIUM", styles['Heading1']))
        
        for medium in self.media_list:
            story.extend(self._skapa_medium_sektion(medium))
        
        # Referenser
        story.append(PageBreak())
        story.append(Paragraph("5. REFERENSER OCH KÄLLOR", styles['Heading1']))
        refs = """
        [1] CoolProp - Open-source thermophysical property database<br/>
        [2] NIST REFPROP Database<br/>
        [3] ASHRAE Standard 34-2019 - Designation and Safety Classification of Refrigerants<br/>
        [4] EU F-gas Regulation 517/2014<br/>
        """
        story.append(Paragraph(refs, styles['Normal']))
        
        # Generera PDF
        doc.build(story)
        
        # Städa temporära filer
        import os
        os.remove("temp_pt.png")
        os.remove("temp_ratio.png")
        os.remove("temp_spider.png")
        
        return filename
    
    def _hitta_basta_medium(self) -> str:
        """Hittar bästa medium baserat på totalpoäng"""
        
        best = None
        best_score = -999
        
        for medium in self.media_list:
            metadata = MEDIUM_METADATA.get(medium, {})
            data = self.diagram_gen.data_handler.hamta_fullstandig_data(medium, np.array([50]))
            
            if data is None:
                continue
            
            score = berakna_total_score(medium, data, metadata)
            
            if score > best_score:
                best_score = score
                best = medium
        
        return best
    
    def _skapa_medium_sektion(self, medium: str) -> List:
        """Skapar detaljerad sektion för ett medium"""
        
        story = []
        styles = getSampleStyleSheet()
        
        metadata = MEDIUM_METADATA.get(medium, {})
        
        story.append(Paragraph(f"4.{self.media_list.index(medium) + 1} {medium}", styles['Heading2']))
        
        # Grundläggande info
        info_text = f"""
        <b>Fullständigt namn:</b> {metadata.get('fullname', 'N/A')}<br/>
        <b>Kemisk formel:</b> {metadata.get('formula', 'N/A')}<br/>
        <b>Molekylvikt:</b> {metadata.get('molar_mass', 'N/A')} g/mol<br/>
        <b>ASHRAE-klass:</b> {metadata.get('ashrae_class', 'N/A')}<br/>
        <b>GWP:</b> {metadata.get('gwp', 'N/A')}<br/>
        <b>Kokpunkt @ 1 atm:</b> {metadata.get('boiling_point', 'N/A')}°C<br/>
        <b>Kritisk temperatur:</b> {metadata.get('critical_temp', 'N/A')}°C<br/>
        <b>ORC-lämplighet:</b> {metadata.get('orc_suitability', 'N/A')}<br/>
        """
        
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Beräknade parametrar
        calc = ORCCalculator(medium, self.T_evap, self.T_cond)
        
        calc_text = f"""
        <b>Tryckförhållande:</b> {calc.tryckforhallande():.2f}<br/>
        <b>Carnot-effektivitet:</b> {calc.carnot_effektivitet() * 100:.1f}%<br/>
        <b>Beräknat diskavstånd @ 50°C:</b> {self.diagram_gen.data_handler.berakna_diskavstand(medium, 50):.2f} mm<br/>
        """
        
        story.append(Paragraph(calc_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        return story
```

### 8.2 CSV och JSON export

```python
class DataExporter:
    """Exporterar rådata i olika format"""
    
    @staticmethod
    def exportera_csv(media_list: List[str], T_range: np.ndarray, 
                      filename: str = "mediumdata.csv") -> str:
        """Exporterar termodynamisk data till CSV"""
        
        data_handler = CoolPropDataHandler()
        all_data = []
        
        for medium in media_list:
            data = data_handler.hamta_fullstandig_data(medium, T_range)
            
            if data is None:
                continue
            
            for i, T in enumerate(data['temp_C']):
                row = {
                    'Medium': medium,
                    'Temp_C': T,
                    'Pressure_bar': data['pressure_bar'][i],
                    'Density_liquid_kg_m3': data['density_liquid_kg_m3'][i],
                    'Density_vapor_kg_m3': data['density_vapor_kg_m3'][i],
                    'Enthalpy_fg_kJ_kg': data['enthalpy_fg_kJ_kg'][i],
                    'Viscosity_vapor_uPas': data['viscosity_vapor_uPas'][i],
                }
                all_data.append(row)
        
        df = pd.DataFrame(all_data)
        df.to_csv(filename, index=False)
        
        return filename
    
    @staticmethod
    def exportera_json(media_list: List[str], config: Dict, 
                       filename: str = "analys_konfiguration.json") -> str:
        """Exporterar komplett konfiguration för reproducerbarhet"""
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'media': media_list,
            'configuration': config,
            'metadata': {m: MEDIUM_METADATA.get(m, {}) for m in media_list}
        }
        
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename
```

---

## 9. TEKNISK ARKITEKTUR

### 9.1 Modulstruktur (utökad)

```
tesla_orc_analyzer/
│
├── main.py                       # Streamlit GUI
├── requirements.txt              # Dependencies
├── README.md                     # Användardokumentation
├── setup.py                      # Installation
│
├── core/
│   ├── __init__.py
│   ├── data_handler.py          # CoolProp-interface
│   ├── calculations.py          # ORC-beräkningar
│   ├── validator.py             # Datavalidering
│   └── cache_manager.py         # Prestanda-caching
│
├── gui/
│   ├── __init__.py
│   ├── streamlit_app.py         # Huvudapp
│   ├── components.py            # GUI-komponenter
│   └── styling.py               # CSS och tema
│
├── analysis/
│   ├── __init__.py
│   ├── sorting.py               # Sorteringsalgoritmer
│   ├── filtering.py             # Filterfunktioner
│   ├── scoring.py               # Bedömningssystem
│   └── comparison.py            # Jämförelselogik
│
├── visualization/
│   ├── __init__.py
│   ├── plotly_diagrams.py       # Plotly-diagram
│   ├── matplotlib_static.py     # Statiska diagram
│   └── color_schemes.py         # Färgpaletter
│
├── export/
│   ├── __init__.py
│   ├── pdf_generator.py         # PDF-rapporter
│   ├── csv_exporter.py          # CSV-export
│   └── json_exporter.py         # JSON-export
│
├── data/
│   ├── medium_metadata.yaml     # Metadata för alla medier
│   ├── ashrae_classes.yaml      # ASHRAE-klassificering
│   ├── gwp_data.yaml            # GWP-värden
│   └── orc_suitability.yaml     # ORC-lämplighet
│
├── tests/
│   ├── __init__.py
│   ├── test_data_handler.py
│   ├── test_calculations.py
│   ├── test_sorting.py
│   └── test_export.py
│
└── docs/
    ├── user_manual.md
    ├── api_documentation.md
    ├── examples/
    │   ├── example_basic.py
    │   └── example_advanced.py
    └── screenshots/
```

### 9.2 Dependencies (requirements.txt)

```
# Core dependencies
CoolProp>=6.4.1
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# GUI
streamlit>=1.20.0

# Visualization
plotly>=5.10.0
matplotlib>=3.5.0
seaborn>=0.12.0

# Export
reportlab>=3.6.0
PyPDF2>=3.0.0
pillow>=9.0.0

# Data handling
PyYAML>=6.0
openpyxl>=3.0.9

# Testing
pytest>=7.0.0
pytest-cov>=3.0.0

# Optional
python-dotenv>=0.19.0
```

---

## 10. DATAFLÖDE OCH ALGORITMER

### 10.1 Huvudflöde (sekvensdiagram)

```
Användare → GUI → Sortering → CoolProp → Beräkning → Diagram → Export
   │         │        │           │           │          │         │
   │         │        │           │           │          │         │
   ↓         ↓        ↓           ↓           ↓          ↓         ↓
Väljer    Visar   Filtrerar   Hämtar     Beräknar   Genererar   Skapar
medier   lista    efter       termo-      ORC-       inter-      PDF
         sorterad  GWP<100    dynamik     params     aktiva      med
         efter              (P,T,h,μ)              diagram      data
         kokpunkt
```

### 10.2 Cache-strategi

```python
class CacheManager:
    """Hanterar caching för prestanda"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cached_data(self, medium: str, temp_range: Tuple) -> Dict:
        """Hämtar cachad data om tillgänglig"""
        
        cache_key = f"{medium}_{temp_range[0]}_{temp_range[-1]}.pkl"
        cache_path = os.path.join(self.cache_dir, cache_key)
        
        if os.path.exists(cache_path):
            # Kontrollera ålder (< 30 dagar)
            age = time.time() - os.path.getmtime(cache_path)
            if age < 30 * 24 * 3600:
                import pickle
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
        
        return None
    
    def save_to_cache(self, medium: str, temp_range: Tuple, data: Dict):
        """Sparar data till cache"""
        
        cache_key = f"{medium}_{temp_range[0]}_{temp_range[-1]}.pkl"
        cache_path = os.path.join(self.cache_dir, cache_key)
        
        import pickle
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
```

---

## 11. IMPLEMENTATION FAS-FÖR-FAS

### Fas 1: CORE FUNKTIONALITET (Vecka 1-2, 60 timmar)

**Mål:** Grundläggande datahämtning och sortering

**Uppgifter:**
- [ ] Setup projektstruktur
- [ ] Implementera CoolPropDataHandler (20h)
  - Automatisk datahämtning
  - Felhantering
  - Caching
- [ ] Implementera sorteringsalgoritmer (15h)
  - Alla 15+ sorteringskriterier
  - Filterfunktioner
  - Totalpoäng-beräkning
- [ ] Skapa YAML-databaser (10h)
  - medium_metadata.yaml (130+ medier)
  - ashrae_classes.yaml
  - gwp_data.yaml
- [ ] Basic Streamlit GUI (15h)
  - Mediumval med checkboxar
  - Sorteringsdropdown
  - Enkel tabell

**Leverabler:**
- Fungerande datahämtning från CoolProp
- Sortering och filtrering av medier
- Basic GUI för mediumval

**Acceptanskriterier:**
- Kan hämta data för minst 100 medier
- Sortering fungerar för alla kriterier
- GUI laddar på <2 sekunder

---

### Fas 2: BERÄKNINGSMOTOR (Vecka 3, 40 timmar)

**Mål:** Kompletta ORC-beräkningar

**Uppgifter:**
- [ ] Implementera ORCCalculator (25h)
  - Carnot-effektivitet
  - Tryckförhållande
  - Massflödesberäkningar
  - Diskavstånd från viskositet
  - Ekonomisk analys
- [ ] Validering och tester (10h)
  - Verifiera mot TesTur-data
  - Jämför med manuella beräkningar
- [ ] GUI-integration (5h)
  - Visa beräknade parametrar
  - Real-time uppdatering

**Leverabler:**
- Fullständig beräkningsmotor
- Validerade resultat
- Integration med GUI

**Acceptanskriterier:**
- Beräkningar matchar manuella beräkningar (±2%)
- Uppdatering <500ms vid parameterändr ing
- Alla 130+ medier fungerar

---

### Fas 3: VISUALISERING (Vecka 4-5, 50 timmar)

**Mål:** Interaktiva och statiska diagram

**Uppgifter:**
- [ ] Plotly-diagram (30h)
  - P-T kurvor
  - Tryckförhållande
  - GWP-jämförelse
  - Viskositet vs temp
  - Spindeldiagram
  - Jämförelsetabell
- [ ] Matplotlib-diagram för PDF (10h)
  - Statiska versioner
  - Högupplöst export
- [ ] Interaktivitet (10h)
  - Hover-tooltips
  - Zoom/pan
  - Klick för visa/dölj kurvor

**Leverabler:**
- 8+ diagram-typer
- Interaktiva Plotly-versioner
- Statiska matplotlib för PDF

**Acceptanskriterier:**
- Alla diagram genereras på <2 sek
- Interaktivitet fungerar smidigt
- Professionell grafisk kvalitet

---

### Fas 4: EXPORT OCH DOKUMENTATION (Vecka 6, 40 timmar)

**Mål:** PDF, CSV, JSON export + dokumentation

**Uppgifter:**
- [ ] PDF-generering (20h)
  - ReportLab implementation
  - Mallar och styling
  - Automatisk layout
- [ ] CSV/JSON export (5h)
- [ ] Användarmanual (10h)
  - Skärmdumpar
  - Exempel
  - FAQ
- [ ] Koddokumentation (5h)
  - Docstrings
  - API-dokumentation

**Leverabler:**
- Professionella PDF-rapporter
- CSV/JSON export
- Komplett dokumentation

**Acceptanskriterier:**
- PDF genereras på <5 sek
- Rapporter är professionella
- Dokumentation är komplett

---

### Fas 5: TESTNING OCH POLERING (Vecka 7, 30 timmar)

**Mål:** Bugfixar, prestanda, användartester

**Uppgifter:**
- [ ] Enhetstester (10h)
  - 80% code coverage
- [ ] Integrationstester (5h)
- [ ] Användartester (10h)
  - 5 testanvändare
  - Feedback-iteration
- [ ] Prestanda-optimering (5h)
  - Caching
  - Asynkron laddning

**Leverabler:**
- Testad och stabil kod
- Användarfeedback implementerad
- Optimerad prestanda

---

## 12. TESTPLAN OCH KVALITETSSÄKRING

### 12.1 Enhetstester

```python
# tests/test_data_handler.py

def test_hamta_data_r1233():
    """Testar datahämtning för R1233zd(E)"""
    handler = CoolPropDataHandler()
    data = handler.hamta_fullstandig_data('R1233zd(E)', np.array([50]))
    
    assert data is not None
    assert 2.45 < data['pressure_bar'][0] < 2.51  # ±1% av 2.48 bar
    assert data['boiling_point_C'] is not None

def test_sortering_kokpunkt():
    """Testar sortering efter kokpunkt"""
    media = ['R1233zd(E)', 'R245fa', 'R1234ze(Z)']
    sorted_media = sortera_medier(media, 'kokpunkt_asc')
    
    assert sorted_media[0]['medium'] == 'R1234ze(Z)'  # Lägst (9.8°C)
    assert sorted_media[-1]['medium'] == 'R1233zd(E)'  # Högst (19.0°C)

def test_totalpoang_berakning():
    """Testar totalpoäng-beräkning"""
    score = berakna_total_score('R1233zd(E)', mock_data, mock_metadata)
    
    assert 80 <= score <= 95  # R1233zd(E) ska ha högt score
```

### 12.2 Integrationstester

```python
def test_komplett_workflow():
    """Testar hela flödet från val till export"""
    
    # 1. Välj medier
    media = ['R1233zd(E)', 'R245fa']
    
    # 2. Sortera
    sorted_media = sortera_medier(media, 'total_score')
    
    # 3. Hämta data
    handler = CoolPropDataHandler()
    data1 = handler.hamta_fullstandig_data(media[0], np.linspace(10, 80, 50))
    data2 = handler.hamta_fullstandig_data(media[1], np.linspace(10, 80, 50))
    
    # 4. Generera diagram
    diag_gen = DiagramGenerator(media, 20, 50)
    fig = diag_gen.pt_kurvor()
    
    # 5. Exportera PDF
    pdf_exp = PDFExporter(media, 20, 50)
    pdf_path = pdf_exp.generera_rapport('test_rapport.pdf')
    
    # Verifiering
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 100000  # > 100 KB
```

### 12.3 Prestanda-tester

```python
import time

def test_datahämtning_prestanda():
    """Datahämtning ska ta <100ms per medium"""
    
    handler = CoolPropDataHandler()
    
    start = time.time()
    data = handler.hamta_fullstandig_data('R245fa', np.linspace(10, 80, 50))
    elapsed = time.time() - start
    
    assert elapsed < 0.1  # < 100 ms

def test_diagram_generering_prestanda():
    """Diagram ska genereras på <2 sek"""
    
    media = ['R1233zd(E)', 'R245fa', 'R1234ze(Z)']
    diag_gen = DiagramGenerator(media, 20, 50)
    
    start = time.time()
    fig = diag_gen.pt_kurvor()
    elapsed = time.time() - start
    
    assert elapsed < 2.0  # < 2 sek
```

---

## 13. RISKER OCH MITIGERING

| # | Risk | Sannolikhet | Impact | Mitigation |
|---|------|-------------|--------|------------|
| 1 | CoolProp saknar data för vissa medier | Hög | Medel | Fallback till manuell databas, tydliga varningar |
| 2 | Långsam GUI-respons vid 100+ medier | Medel | Hög | Asynkron laddning, caching, paginering |
| 3 | CoolProp-installation komplex | Hög | Hög | Standalone .exe med PyInstaller, Docker-image |
| 4 | Felaktig GWP-data (ändras över tid) | Medel | Låg | Versionshantering av databas, uppdateringsrutin |
| 5 | PDF-generering misslyckas | Låg | Medel | Felhantering, fallback till PNG-export |
| 6 | Stora temperaturområden → minnesbrist | Låg | Medel | Begränsa max antal temperatupunkter till 200 |
| 7 | Användare förstår inte resultat | Medel | Medel | Tydliga förklaringar, tooltips, FAQ |
| 8 | Prestanda dålig på låg-spec datorer | Medel | Medel | Cloud-version (Streamlit Cloud), optimering |

---

## 14. FRAMTIDA UTVECKLING

### Fas 6+: Avancerade funktioner (Efter release)

#### 14.1 Optimeringsalgoritm
```python
from scipy.optimize import minimize

def hitta_optimalt_medium(
    restrictions: Dict,
    weights: Dict = {'kokpunkt': 0.3, 'tryck': 0.2, 'safety': 0.2, 'gwp': 0.15, 'hfg': 0.1, 'cost': 0.05}
) -> str:
    """
    Använder scipy.optimize för att hitta bästa medium
    
    Args:
        restrictions: {'max_gwp': 100, 'min_boiling': 15, ...}
        weights: Viktning av kriterier
    
    Returns:
        Optimalt medium-namn
    """
    pass
```

#### 14.2 Machine Learning-förutsägelse
- Träna modell på befintlig ORC-data
- Förutsäga verklig prestanda från termodynamik
- Rekommendera medium baserat på specifik applikation

#### 14.3 3D-visualisering
- T-s diagram (Temperatur-entropi)
- h-s diagram (Mollier)
- p-h diagram (Tryck-entalpi)
- Interaktiv 3D-yta

#### 14.4 Cloud-version
- Webb-app utan installation
- Spara projekt i molnet
- Dela analyser med kollegor
- API för integration med andra verktyg

#### 14.5 CAD-integration
- Export till SolidWorks
- Export till Fusion 360
- Direktgenerering av turbin-geometri

#### 14.6 Realtidsdata
- Integration med IoT-sensorer
- Live-monitoring av ORC-system
- Jämför verklig vs teoretisk prestanda

---

## 15. SAMMANFATTNING

### 15.1 Leverabler

**Version 1.0 (7 veckor, 220 timmar):**
✅ Automatisk datahämtning för 130+ medier (CoolProp)  
✅ Avancerad sortering (15+ kriterier) och filtrering  
✅ Interaktiv Streamlit GUI  
✅ 8+ diagram-typer (Plotly interaktiva)  
✅ Komplett beräkningsmotor (ORC-parametrar)  
✅ PDF-rapportgenerering  
✅ CSV/JSON export  
✅ Omfattande dokumentation  

### 15.2 Teknisk stack

**Core:**
- Python 3.9+
- CoolProp 6.4.1+ (termodynamik)
- NumPy, Pandas, SciPy (beräkningar)

**GUI:**
- Streamlit (interaktiv webb-app)

**Visualisering:**
- Plotly (interaktiva diagram)
- Matplotlib (statiska PDF-diagram)

**Export:**
- ReportLab (PDF)
- PyYAML (konfiguration)

### 15.3 Systemkrav

**Minimum:**
- Python 3.9+
- 4 GB RAM
- Windows/Mac/Linux

**Rekommenderat:**
- Python 3.11+
- 8 GB RAM
- SSD-disk (för caching)

### 15.4 Installation (efter färdigställande)

```bash
# Klona repo
git clone https://github.com/user/tesla-orc-analyzer.git
cd tesla-orc-analyzer

# Installera dependencies
pip install -r requirements.txt

# Kör applikation
streamlit run main.py
```

**Eller standalone:**
```bash
# Ladda ner .exe (Windows)
wget https://releases/.../TeslaORCAnalyzer.exe

# Kör direkt
TeslaORCAnalyzer.exe
```

### 15.5 Nästa steg

1. ✅ **Godkänn arbetsbeskrivning**
2. **Starta Fas 1** (Core funktionalitet)
   - Setup projektstruktur
   - CoolProp-integration
   - Sorteringsalgoritmer
3. **Veckovis uppföljning**
   - Demo varje fredag
   - Feedback och justering
4. **Release 1.0** (vecka 7)

---

**Dokument skaparat:** 2025-10-31  
**Version:** 2.0 KOMPLETT  
**Total uppskattad tid:** 220 timmar (≈7 veckor heltid)  
**Status:** ✅ Redo för implementation
