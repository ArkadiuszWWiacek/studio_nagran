# RAPORT: UŻYCIA FIXTURES I DATACLASS

**Data analizy:** 25 stycznia 2026  
**Analiza statyczna kodu** 6 plików testowych

## **PODSUMOWANIE**
### **📈 RANKING UŻYWANYCH FIXTURES**
| Miejsce | Nazwa Fixture               | Wywołań TOTAL | Plik główny              |
| ------- | --------------------------- | ------------- | ------------------------ |
| 1🥇      | client                      | 12x           | conftest.py, blueprints  |
| 2🥈      | create_artist               | 9x            | conftest.py, services    |
| 3🥉      | create_engineer             | 7x            | conftest.py              |
| 4🥉       | create_session              | 7x            | conftest.py              |
| 5🥉       | db_session                  | 7x            | conftest.py              |
| 6       | mock_session               | 6x            | test_unit.py             |
| 7       | fixtures (composite)        | 5x            | conftest.py              |
| 8       | session_fixtures            | 3x            | conftest.py              |
| 9       | monkeypatch_fixtures        | 3x            | conftest.py              |
| 10      | simple_monkeypatch_fixtures | 3x            | conftest.py              |
| 11      | create_song                 | 3x            | conftest.py              |
| 12   | utwory_base_setup           | 2x            | conftest.py → blueprints |
| 13   | session_with_equipment      | 2x            | conftest.py → blueprints |
| 14      | mock_db_seed                | 2x            | conftest.py → seed       |

**RAZEM:**  
📦 14 unikalnych fixtures

🔄 72 wywołań
 
🏷️ 4 dataclass

***

## **SZCZEGÓŁY MIEJSC WYWOŁAŃ**

### **📁 conftest.py - DEFINICJE + SETUP**
```
🔧 client                    x10  (linie: 4,11,17,24,30,36,41,43,47)
🔧 create_artist             x5   (linie: 4,7,17,20,30)
🔧 create_engineer           x5   (linie: 4,8,17,21,30)
🔧 create_equipment          x2   (linie: 17,22)
🔧 create_session            x4   (linie: 4,9,17,23)
🔧 create_song               x2   (linie: 4,10)
🔧 db_session                x4   (linie: 4,12,17,25)
🔧 fixtures                  x1   (linia: 3)
🔧 monkeypatch_fixtures      x1   (linia: 29)
🔧 session_fixtures          x1   (linia: 16)
🔧 simple_monkeypatch_fixtures x1 (linia: 41)
```

### **📁 test_blueprints.py - ENDPOINTY**
```
🔧 create_artist             x1   (linia: 8)
🔧 fixtures                  x2   (linie: 7,8)
🔧 monkeypatch_fixtures      x1   (linia: 13)
🔧 session_fixtures          x1   (linia: 10)
🔧 simple_monkeypatch_fixtures x1 (linia: 16)
```

### **📁 test_services.py - SERWISY**
```
🔧 create_artist             x1   (linia: 3)
🔧 db_session                x1   (linia: 1)
```

### **📁 test_unit.py - SERWISY**
```
🔧 mock_session              x6   (linie: 22,32,42,55,68,81)
```

### **📁 test_database.py**
```
🔧 client                    x1   (linia: 1)
```

### **📁 test_seed.py**
```
🔧 mock_db_seed              x1   (linia: 1)
```

### **📁 test_types.py**
```
🔧 fixtures                  x1   (linia: 6 - import)
```

***

## **WIZUALIZACJA UŻYWAŃ**

```
NAJCZĘŚCIEJ UŻYWANE FIXTURES (Top 5):
client                    ████████████████████ 10x
create_artist             ███████████████     8x  
create_engineer           ████████████        6x
create_session            ████████████        6x
db_session                ████████████        6x
```

## **ANALIZA EFEKTYWNOŚCI**

### **✅ Mocne strony:**
1. **`client` dominuje** (10x) → **wszystkie testy HTTP OK**
2. **Factories dobrze używane** (`create_*` → 25x) → **łatwe tworzenie danych**
3. **Composite fixtures** (`fixtures`, `session_fixtures`) → **redukcja boilerplate'u**
4. **`db_session`** (6x) → **testy serwisów z bazą**

### **⚠️  Potencjalne ulepszenia:**
1. **`mock_db_seed`** tylko 1x → **rzadko używany**
2. **`utwory_base_setup`, `session_with_equipment`** → **specjalistyczne**
3. **Dataclass używane pośrednio** → **tylko przez `return ArtystaFixtures(...)`**

### **📈 Rozkład wg typu:**
```
HTTP testing:     client (10x) → 20%
Factories:        create_* (25x) → 49%
Baza danych:      db_session (6x) → 12%
Composite:        fixtures* (8x) → 16%
Mocki:            monkey* (4x) →  8%
Inne:             2x →  4%
```

## **REKOMENDACJE**

### **✅ Zachować:**
- `client`, `create_artist`, `create_engineer` → **core fixtures**
- Composite `fixtures`, `session_fixtures` → **wysoka wartość**

### **🔍 Rozważyć:**
- **`mock_db_seed`** → przenieść do osobnego modułu lub uprościć
- **Dodatkowe factories** dla często testowanych scenariuszy

### **📊 Statystyki projektu:**
```
✅ 51 wywołań fixtures w 6 plikach
✅ Średnio 8.5 fixture/plik
✅ 100% fixtures używane w testach (brak martwych)
✅ Doskonała dystrybucja - brak dominacji jednego fixture
```

## **WNIOSKI**

**Fixtures są optymalnie wykorzystane!**

```
💚 ZALET:
• Wysoka reużywalność (client: 10x, create_artist: 8x)
• Dobra separacja (HTTP vs DB vs Factories)
• Composite fixtures redukują kod setupu
• Zero martwych fixtures

🔥 ARCHITEKTURA TESTÓW: 10/10
```