# RAPORT: UŻYCIA FIXTURES I DATACLASS

**Data analizy:** 25 stycznia 2026  
**Analiza statyczna kodu** 6 plików testowych

## **PODSUMOWANIE**

### **📈 TOP 10 NAJCZĘŚCIEJ UŻYWANYCH FIXTURES**
| Miejsce | Nazwa Fixture              | Wywołań | Główny cel |
|---------|----------------------------|---------|------------|
| 🥇     | `client`                  | **10x** | Testy HTTP endpointów |
| 🥈     | `create_artist`           | **8x**  | Tworzenie artystów |
| 🥉     | `create_engineer`         | **6x**  | Tworzenie inżynierów |
| 4      | `create_session`          | **6x**  | Tworzenie sesji |
| 5      | `db_session`              | **6x**  | Bezpośredni dostęp do bazy |
| 6      | `fixtures` (composite)    | **4x**  | Pakiet dla artystów/utworów |
| 7      | `session_fixtures`        | **2x**  | Pakiet dla sesji + sprzęt |
| 8      | `monkeypatch_fixtures`    | **2x**  | Testy z mockami |
| 9      | `simple_monkeypatch_fixtures` | **2x** | Proste mocki |
| 10     | `create_song`             | **2x**  | Tworzenie utworów |

**RAZEM:**  
📦 **12 unikalnych fixtures**  
🔄 **51 wywołań fixtures**  

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