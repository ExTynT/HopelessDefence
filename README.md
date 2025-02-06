# HopelessDefence - Game Design Document

V tomto repozitári sa náchadza implementácia hry v **Pygame**.

Hra reprezentuje semestrálnu prácu z predmetu **Objektové Technológie** (**OT**).

**Autor:** Ivan Klopček

**Vybraná téma:** _One level, but constantly changing_ - jeden level, ale neustále sa mení.

## 1. Úvod

**HopelessDefence** je _tower defense_ hra vytvorená ako semestrálny projekt pre predmet Objektové Technológie. Hra spĺňa zadanú tému "_One level, but constantly changing_", kde hráč musí brániť svoju **základňu** proti neustále sa meniacim vlnám **nepriateľov**. 

Hlavným cieľom hry je **prežiť** čo najdlhšie pomocou **strategického** umiestňovania **veží** a efektívneho manažovania **zdrojov**. Hráč musí čeliť rôznym typom nepriateľov, ktorí sa postupne stávajú **silnejšími** a **nebezpečnejšími**. Každá hra je _jedinečná_ vďaka **dynamickému systému vĺn** nepriateľov a možnostiam **vylepšovania veží**.

### 1.1 Inšpirácia

_**Bloons TD**_

**Bloons TD** je _tower defense_ hra zameraná na **strategickú obranu** územia pomocou rôznych typov **veží**, ktoré chránia cestu pred prichádzajúcimi vlnami nepriateľov. Koncept hry je založený na **postupnom budovaní** obranného systému, kde hráč musí čeliť čoraz väčšiemu množstvu nepriateľov s rozličnými vlastnosťami a schopnosťami. Hra ponúka **komplexný systém vylepšovania** veží, kde každá veža má svoj _unikátny strom vylepšení_ a _špeciálne schopnosti_.

<p align="center">
<img src="readme_images/20612905241641377784gol1.jpg" alt="Bloons TD">
<br>
<em>Obrázok 1 - Ukážka hry Bloons TD</em>
</p>

### 1.2 Herný zážitok

Cieľom hry je, aby hráč **ubránil** svoju základňu pred neustále prichádzajúcimi vlnami nepriateľov. Hráč musí **strategicky** umiestňovať obranné veže po mape a **efektívne** ich vylepšovať, aby dokázal čeliť čoraz silnejším nepriateľom. Každá veža má svoje _jedinečné vlastnosti_ a _schopnosti_, ktoré môžu byť kľúčové pre prežitie.

Hra sa odohráva na jednej **dynamicky sa meniacej mape**, kde sa nepretržite zvyšuje **náročnosť** a počet nepriateľov. Hráč musí správne **hospodáriť** so získanými zdrojmi, ktoré dostáva za eliminovanie nepriateľov, a využívať ich na **stavbu** nových veží alebo **vylepšovanie** existujúcich. Prežitie každej ďalšej vlny vyžaduje _premyslenú stratégiu_ a _rýchle rozhodovanie_.

### 1.3 Vývojový softvér

- **Pygame-CE**: zvolený programovací jazyk.
- **Visual Studio Code**: vybrané IDE.
- **Joystix** (1001fonts.com): herný font.
- **ElevenLabs**: nástroj na generovanie zvukových efektov.
- **PixelLab.ai**: tvorba pixel art grafiky.
- **Suno.ai**: generovanie hernej hudby.

## 2. Koncept

### 2.1 Prehľad hry

**HopelessDefence** je _tower defense_ hra postavená na princípe **dynamicky sa meniacej mapy**. Hráč v role obrancu základne musí čeliť neustálym vlnám nepriateľov prostredníctvom **strategického** umiestňovania a vylepšovania obranných veží. S každou vlnou sa mapa mení, čím vytvára **unikátne výzvy** a núti hráča **adaptovať** svoju stratégiu. Hlavným cieľom je **prežiť** čo najdlhšie a dosiahnuť čo najvyššie skóre pomocou efektívneho využívania dostupných zdrojov a taktického rozmiestnenia obrany.

### 2.2 Interpretácia témy

"_One level, but constantly changing_" reprezentuje základný princíp hry, ktorý sa prejavuje v **štyroch kľúčových aspektoch**:

- **Dynamická mapa**: Každá vlna prináša nový layout s unikátnymi trasami a strategickými pozíciami pre veže
- **Progresívna náročnosť**: HP nepriateľov sa zvyšuje o 25% každou vlnou, vrcholiac súbojom s bossom
- **Adaptívna ekonómia**: Znižujúci sa príjem mincí núti k strategickému hospodáreniu so zdrojmi
- **Evolučný systém veží**: Kombinácia dočasných vylepšení počas hry a permanentného progressu medzi hrami

### 2.3 Základné mechaniky

**1. Systém mapy**
- Mapa obsahuje **pevne stanovené cesty** pre pohyb nepriateľov
- **Špeciálne pozície** (_gold spots_) poskytujú bonusy pre veže
- Každá mapa má **definovaný štartovací** a **cieľový bod** pre nepriateľov

**2. Systém nepriateľov**
- **4 typy nepriateľov** s unikátnymi vlastnosťami:
  - `Základný orb`: Vyvážené vlastnosti
  - `Rýchly orb`: Zvýšená rýchlosť pohybu
  - `Odolný orb`: Zvýšené HP
  - `Boss`: Najsilnejší nepriateľ s vysokým HP
- Nepriatelia sa generujú na **pevne stanovenom mieste** (štartovací bod)
- Pohyb po **preddefinovaných trasách** smerom k základni

**3. Systém veží**
- **4 typy veží** s rôznymi schopnosťami:
  - `Laser Tower`: Rýchla streľba
  - `Cannon Tower`: Plošné poškodenie
  - `Basic Tower`: Vyvážený útok
  - `Boost Tower`: Podporné vylepšenia
- Každá veža má **2 unikátne vylepšenia**
- Veže môžu byť **predané** alebo **vylepšené** počas hry
- Všetky veže sa **automaticky predajú** po skončení každého levelu

**Vylepšenia veží:**
- `Basic Tower`:
  - **Rapid Fire**: Rýchlejšia streľba (DMG +25%, CD -25%)
  - **Double Shot**: Dva projektily s nižším poškodením
- `Laser Tower`:
  - **Piercing Beam**: Prestrelenie nepriateľov (100% DMG prvý, 50% DMG druhý)
  - **Overcharge**: Dočasné zdvojnásobenie poškodenia (5s aktívne, 3s cooldown)
- `Cannon Tower`:
  - **Heavy Shells**: Vysoké poškodenie jednému cieľu (DMG +350%)
  - **Cluster Bombs**: Tri výbuchy (54 DMG stred, 30 DMG boky)
- `Boost Tower`:
  - **DMG Boost**: Zvýšenie poškodenia okolitých veží (+50%)
  - **SPD Boost**: Zvýšenie rýchlosti streľby okolitých veží (+25%)

**4. Systém vĺn**
- Každá vlna obsahuje **15 nepriateľov**
- **Postupná náročnosť**:
  - Vlna 1: Len základné orby
  - Vlna 2: Základné a rýchle orby
  - Vlna 3: Všetky typy okrem bossa
  - Vlna 4: Všetky typy + boss na konci
- **HP multiplikátor** sa zvyšuje o 25% každou vlnou
- Po každej vlne sa **náhodne vyberie** nová mapa
- Každá vlna končí až po **eliminácii všetkých nepriateľov**

**5. Ekonomický systém**
- Získavanie **mincí** za eliminovanie nepriateľov
- **Nákup** a **vylepšovanie** veží
- **Permanentné vylepšenia** v obchode

### 2.4 Návrh tried

**Tower**
```
- Správa všetkých typov veží a ich vlastností
- Systém vylepšení a útokov
- Manažment projektilových útokov
- Interakcia s ekonomickým systémom
```

**Enemy**
```
- Implementácia rôznych typov nepriateľov
- Systém pohybu po mape
- Správa zdravia a odmien
- Interakcia s vežami a projektilmi
```

**Wave**
```
- Generovanie vĺn nepriateľov
- Správa náročnosti a HP multiplikátora
- Manažment boss vĺn
- Aktualizácia hernej mapy
```

**Map**
```
- Definícia herných máp
- Správa špeciálnych pozícií
- Systém ciest pre nepriateľov
- Aktualizácia mapy medzi vlnami
```

**Economy**
```
- Správa hernej meny
- Systém odmien
- Manažment nákupov a vylepšení
- Konverzia zdrojov na kredity
```

**Shop**
```
- Systém permanentných vylepšení
- Správa kreditov
- Manažment multiplierov pre veže
- Ukladanie postupu vylepšení
```

## 3. Grafika

### 3.1 Interpretácia témy

Grafický štýl hry je navrhnutý tak, aby podporoval hlavnú tému "_One level, but constantly changing_". Minimalistický dizajn s jasnými farebnými odlíšeniami umožňuje hráčovi rýchlo sa orientovať v dynamicky sa meniacom prostredí. Nepriateľské orby svojimi farbami indikujú ich typ a nebezpečnosť, zatiaľ čo veže svojím dizajnom jasne komunikujú ich funkciu a dosah. Tento prístup zabezpečuje, že aj napriek neustálym zmenám v hernom prostredí zostáva hra prehľadná a čitateľná.

### 3.2 Dizajn

Hra je navrhnutá s dôrazom na **čistý a prehľadný vizuálny štýl**, ktorý podporuje hrateľnosť a strategické rozhodovanie. Grafické spracovanie využíva **minimalistický prístup** s jasne rozlíšiteľnými hernými prvkami:

**1. Nepriateľské jednotky**
- Dizajn nepriateľov využíva **orbové tvary** v charakteristických farbách:
  - `Základný orb`: Červený - symbolizuje základnú hrozbu
  - `Rýchly orb`: Modrý - evokuje dynamiku a rýchlosť
  - `Odolný orb`: Tmavofialový - vyjadruje odolnosť a silu
  - `Boss`: Čierny - najnebezpečnejší nepriateľ s impozantným vzhľadom

<p align="center">
<img src="sprites/enemies/orb_1.png" alt="Základný orb" width="60">
<img src="sprites/enemies/orb_2_speed.png" alt="Rýchly orb" width="60">
<img src="sprites/enemies/orb_3_tough.png" alt="Odolný orb" width="60">
<img src="sprites/enemies/orb_4_boss.png" alt="Boss" width="90">
<br>
<em>Obrázok 2 - Typy nepriateľov (zľava: Základný, Rýchly, Odolný, Boss)</em>
</p>

**2. Obranné veže**
- Každý typ veže má **unikátny vizuálny štýl**:
  - `Laser Tower`: Futuristický dizajn s energetickými efektmi
  - `Cannon Tower`: Robustná konštrukcia s výrazným delom
  - `Basic Tower`: Klasický vzhľad s vyváženými proporciami
  - `Boost Tower`: Podporný dizajn 

<p align="center">
<img src="sprites/towers/tower_1_laser.png" alt="Laser Tower" width="60">
<img src="sprites/towers/tower_2_cannon.png" alt="Cannon Tower" width="60">
<img src="sprites/towers/tower_3_basic.png" alt="Basic Tower" width="60">
<img src="sprites/towers/tower_4_boosting.png" alt="Boost Tower" width="60">
<br>
<em>Obrázok 3 - Typy veží (zľava: Laser, Cannon, Basic, Boost)</em>
</p>

**3. Efekty a projektily**
- **Vizuálna spätná väzba** pre rôzne herné mechaniky:
  - Laserové lúče s červeným efektom
  - Delové gule s explóziami
  - Štandardné projektily s tracer efektmi
  - Boost efekty zobrazujúce oblasť pôsobenia

**4. Herné prostredie**
- **Prehľadný mapový dizajn**:
  - Jasne viditeľné cesty pre nepriateľov
  - Zvýraznené špeciálne pozície (_gold spots_)
  - Kontrastné pozadie pre lepšiu čitateľnosť
  - Intuitívne rozpoznateľné štartovacie a cieľové body

<p align="center">
<img src="readme_images/Qwr1.png" alt="Herné prostredie" width="400">
<br>
<em>Obrázok 4 - Ukážka herného prostredia</em>
</p>

**5. Dizajn menu**
- **Všetky menu prvky** vytvorené pomocou nástroja **PixelLab.ai**:

<p align="center">
<img src="readme_images/V6HG.png" alt="Hlavné menu" width="400">
<br>
<em>Obrázok 5 - Hlavné menu</em>
</p>

<p align="center">
<img src="readme_images/WbYI.png" alt="Herné menu" width="400">
<img src="readme_images/nULK.png" alt="Shop menu" width="400">
<br>
<em>Obrázok 6 - Herné menu (vľavo) a Shop menu (vpravo)</em>
</p>

<p align="center">
<img src="readme_images/RlIO.png" alt="Shop menu detail" width="400">
<img src="readme_images/dz6G.png" alt="Game over menu" width="400">
<br>
<em>Obrázok 7 - Detail shop menu (vľavo) a Game over obrazovka (vpravo)</em>
</p>

## 4. Zvuk

### 4.1 Hudba

Hudobná stránka hry bola vytvorená pomocou nástroja **Suno.ai**, ktorý generuje unikátnu hernú hudbu. Každá časť hry má svoju charakteristickú melódiu:

- `Menu hudba`: Pieseň, vytvárajúca príjemnú atmosféru v menu
- `Herná hudba`: Séria melodických piesní, vytvárajúca napätie počas hrania
- `Shop hudba`: Relaxačná melódia pre príjemné nakupovanie
- `Victory/Game Over`: Krátke melodické motívy pre víťazstvo a prehru

### 4.2 Zvukové efekty

Zvukové efekty boli vytvorené pomocou nástroja **ElevenLabs** a sú navrhnuté tak, aby poskytovali jasnú zvukovú spätnú väzbu:

**Veže a útoky:**
- `Basic Tower`: Zvuk tlmeného výstrelu
- `Laser Tower`: Vysokofrekvenčný zvuk laseru
- `Cannon Tower`: Výrazný,dunivý zvuk výstrelu dela

## 5. Herný zážitok

### 5.1 Používateľské rozhranie

Používateľské rozhranie je navrhnuté s dôrazom na **prehľadnosť** a **intuitívnosť**, zachovávajúc jednotný grafický štýl celej hry:

**Hlavná obrazovka**
- Tlačidlo `PLAY` pre spustenie novej hry
- Tlačidlo `SHOP` pre vstup do obchodu
- Tlačidlo `EXIT` pre ukončenie hry

**Herná obrazovka**
- Zobrazenie aktuálneho levelu
- Indikátor životov základne
- Počítadlo dostupných mincí
- Informácie o aktuálnej vlne
- Informácie o počte zostávajúcich nepriateľov
- Tlačidlo `MENU` pre vstup do menu

**Kontextové menu**
- Menu pre výber typu veže pri stavaní
- Menu pre vylepšovanie existujúcich veží
- Informácie o cenách a vlastnostiach veží

### 5.2 Ovládanie

**Základné ovládanie**
- `Ľavé tlačidlo myši`: 
  - Výber pozície pre stavbu veže
  - Potvrdenie výberu v menu
  - Nákup a vylepšovanie veží
- `Pravé tlačidlo myši`:
  - Zrušenie výberu
  - Zatvorenie aktuálneho menu
  - Predaj veže (s potvrdením)

**Interakcia s vežami**
- `Kliknutie na vežu`: Zobrazenie menu vylepšení
- `Kliknutie na prázdne pole`: Zobrazenie menu pre stavbu veže
- `Predaj veže`: Pravé tlačidlo myši + potvrdenie v dialógu

**Ovládanie obchodu**
- Výber vylepšení pomocou myši
- Nákup vylepšení tlačidlami `+/-`
- Prepínanie kategórií tlačidlom `SWITCH`
- Návrat do hry tlačidlom `BACK`

**Obrazovka víťazstva nad bossom**
- Tlačidlo `CONTINUE` pre pokračovanie v hre
- Tlačidlo `SHOP` pre vstup do obchodu
- Tlačidlo `MENU` pre návrat do hlavného menu







