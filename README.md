# Studio Nagrań

Aplikacja webowa do zarządzania studiem nagrań, umożliwiająca rejestrację sesji nagraniowych, artystów, inżynierów dźwięku, sprzętu oraz utworów muzycznych.

## Autor

**Arkadiusz Wiącek - 35027**

## Opis projektu

Studio Nagrań to system zarządzania bazą danych studia nagraniowego zbudowany przy użyciu Flask i SQLAlchemy. Aplikacja umożliwia kompleksowe zarządzanie wszystkimi aspektami działalności studia, w tym:

- Rejestracja i zarządzanie artystami (soliści i zespoły)
- Zarządzanie inżynierami dźwięku
- Katalog sprzętu studyjnego (mikrofony, przedwzmacniacze, efekty, itp.)
- Planowanie i rejestracja sesji nagraniowych
- Katalog nagranych utworów

## Wymagania systemowe

- Python 3.12.12 lub nowszy
- SQLite (wbudowane w Python)

## Technologie

- **Backend**: Flask
- **ORM**: SQLAlchemy (Core 2.0)
- **Baza danych**: SQLite
- **Frontend**: HTML (Jinja2 templates)

## Instalacja

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/ArkadiuszWWiacek/studio_nagran
cd studio_nagran
```

### 2. Utwórz wirtualne środowisko

```bash
python -m venv .venv
```

### 3. Aktywuj wirtualne środowisko

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

## Struktura projektu

```
studio_nagran/
├── .gitignore
├── config.py
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
├── seed_data.sql
├── studio_nagran.db
├── app
│   ├── __init__.py
│   ├── blueprints.py
│   ├── database.py
│   ├── models.py
│   ├── services.py
│   ├── static/
│   │   ├── style.css
│   │   └── images/
│   │      └── colour_wave.jpg
│   ├── templates/
│   │   ├── artysci.html
│   │   ├── base.html
│   │   ├── dodaj_artyste.html
│   │   ├── dodaj_inzyniera.html
│   │   ├── dodaj_sesje.html
│   │   ├── dodaj_sprzet.html
│   │   ├── dodaj_utwor.html
│   │   ├── edytuj_artyste.html
│   │   ├── edytuj_inzyniera.html
│   │   ├── edytuj_sesje.html
│   │   ├── index.html
│   │   ├── inzynierowie.html
│   │   ├── modal_detale.html
│   │   ├── modal_utwory.html
│   │   ├── sesje_detale.html
│   │   ├── sesje.html
│   │   ├── sprzet.html
│   │   └── utwory.html
│   └── views/
│       ├── __init__.py
│       ├── artysci.py
│       ├── inzynierowie.py
│       ├── sesje.py
│       ├── sprzet.py
│       └── utwory.py
└── tests
   ├── __init__.py
   ├── conftest.py
   ├── dokumentacja.md
   ├── statystyki_uzycia.md
   ├── test_blueprints.py
   ├── test_database.py
   ├── test_services.py
   └── test_types.py
```

## Uruchomienie aplikacji
Sprawdź sekcję ["Konfiguracja"](#konfiguracja)
```bash
python run.py
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

## Model bazy danych

### Tabele

#### Artysci
- `IdArtysty` (PK) - Identyfikator artysty
- `Nazwa` - Nazwa artysty/zespołu
- `Imie` - Imię (dla artystów solowych)
- `Nazwisko` - Nazwisko (dla artystów solowych)

#### Inzynierowie
- `IdInzyniera` (PK) - Identyfikator inżyniera
- `Imie` - Imię inżyniera
- `Nazwisko` - Nazwisko inżyniera

#### Sprzet
- `IdSprzetu` (PK) - Identyfikator sprzętu
- `Producent` - Producent sprzętu
- `Model` - Model sprzętu
- `Kategoria` - Kategoria sprzętu (mikrofon, przedwzmacniacz, itp.)

#### Sesje
- `IdSesji` (PK) - Identyfikator sesji
- `IdArtysty` (FK) - Powiązanie z artystą
- `IdInzyniera` (FK) - Powiązanie z inżynierem
- `TerminStart` - Data i czas rozpoczęcia sesji
- `TerminStop` - Data i czas zakończenia sesji (opcjonalne)

#### Utwory
- `IdUtworu` (PK) - Identyfikator utworu
- `IdArtysty` (FK) - Powiązanie z artystą
- `IdSesji` (FK) - Powiązanie z sesją
- `Tytul` - Tytuł utworu

#### SprzetySesje (tabela powiązań)
- `IdSprzetu` (PK, FK) - Identyfikator sprzętu
- `IdSesji` (PK, FK) - Identyfikator sesji

### Relacje

- Artysta może mieć wiele sesji i utworów (1:N)
- Inżynier może prowadzić wiele sesji (1:N)
- Sesja może wykorzystywać wiele jednostek sprzętu (N:M)
- Sesja może zawierać wiele utworów (1:N)

## Funkcjonalności

### Zarządzanie artystami
- **Przeglądanie** (`/artysci`) - lista wszystkich artystów z możliwością sortowania
- **Dodawanie** (`/artysci/dodaj`) - formularz dodawania nowego artysty
- **Edycja** (`/artysci/edytuj/<id>`) - formularz edycji danych artysty
- **Utwory artysty** (`/artysci/<id>`) - lista utworów danego artysty

### Zarządzanie inżynierami
- **Przeglądanie** (`/inzynierowie`) - lista wszystkich inżynierów z możliwością sortowania
- **Dodawanie** (`/inzynierowie/dodaj`) - formularz dodawania nowego inżyniera
- **Edycja** (`/inzynierowie/edytuj/<id>`) - formularz edycji danych inżyniera

### Zarządzanie sprzętem
- **Przeglądanie** (`/sprzet`) - lista całego sprzętu z możliwością sortowania
- **Dodawanie** (`/sprzet/dodaj`) - formularz dodawania nowego sprzętu

### Zarządzanie utworami
- **Przeglądanie** (`/utwory`) - lista wszystkich utworów z danymi artysty i sesji
- **Dodawanie** (`/utwory/dodaj`) - formularz dodawania nowego utworu

### Zarządzanie sesjami
- **Przeglądanie** (`/sesje`) - lista wszystkich sesji z możliwością sortowania
- **Dodawanie** (`/sesje/dodaj`) - formularz dodawania nowej sesji z wyborem sprzętu
- **Szczegóły sesji** (`/sesje/<id>`) - pełne informacje o sesji, wykorzystanym sprzęcie i utworach

## Sortowanie danych

Wszystkie widoki list obsługują sortowanie poprzez parametry URL:
- `sort` - kolumna do sortowania
- `order` - kierunek sortowania (`asc` lub `desc`)

Przykład: `/artysci?sort=Nazwisko&order=desc`

## Konfiguracja

### Baza danych

Domyślnie aplikacja korzysta z bazy SQLite `studio_nagran.db`, która jest tworzona automatycznie przy pierwszym uruchomieniu. Połączenie z bazą można zmienić modyfikując linię:

```python
engine = create_engine("sqlite:///studio_nagran.db", echo=True, future=True)
```

### Inicjalizacja danych przykładowych
```bash
flask seed
```

### Tryb debugowania

Aplikacja uruchamia się w trybie debug. W środowisku produkcyjnym zmień:

```python
app.run(host="0.0.0.0", port=5000, debug=False)
```

## Testy i narzędzia
### Testy
**Architektura testów** opiera się na **warstwowym podejściu** z SQLite in-memory.

**Fixtures** w architekturze testów są **sercem systemu**, zamieniają 885+ linii boilerplate'u na 12 reużywalnych fabryk (`create_artist`: 8x, `client`: 10x)

**Composite dataclass** (`ArtystaFixtures`, `SesjaFixtures`) grupują powiązane fabryki, umożliwiając złożone scenariusze jednym wywołaniem. 

**Fixture `_db_in_memory`** zapewnia **perfekcyjną izolację** - każdy test startuje z czystą bazą SQLite, gwarantując niezależność wyników. 

**Kluczowe elementy:**
- `conftest.py` - 12 fixtures (factories + composite dataclass)
- `test_services.py` (17 testów) - integracja serwisów z bazą 
- `test_blueprints.py` (36 testów) - pełne testy HTTP/Flask z `client`
- `test_*` - CLI, seed, inicjalizacja DB

**Wzorce:** AAA, factory pattern

100% code coverage z branch testing

**optymalna reużywalność** (`client`:10x, `create_artist`:8x). 

**Wyniki:**
- **szybkie** (3.5s/56 testów)
- **kompletne** (CRUD+edge cases)
- **zrównoważone** (49% factories, 20% HTTP)

**Jednostkowe/integracyjne** (services: sortowanie, CRUD, rollback błędów) i **integracyjne/end-to-end** (blueprints: GET/POST endpointy, redirecty, 404, monkeypatch symulacja błędów)
- Dokumentacja testów: [/tests/dokumantacja.md](./tests/dokumentacja.md#wstep)
- Raport: [/tests/statystyki_uzycia.md](./tests/statystyki_uzycia.md#podsumowanie)

#### Uruchomienie testów
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Narzędzia
Analiza statyczna z pominięciem komunikatów `missing-function-docstring` i `too-few-public-method`
```bash
pylint ./ --ignore=.venv --disable=C0114,C0115,C0116,R0903
```

### Skrypt do uruchamiania testów
Skrypt uruchamia testy z raportem pokrycia oraz analizę statyczną `pylint` z parametrami pominięcia błędów `missing-function-docstring` i `too-few-public-method`

Linux / MacOS
```bash
./run_tests.sh
```

Windows
```bash
./run_tests.bat
```

## Użycie AI
**Perplexity AI** (różne modele) zastosowano do:
- generowanie/aktualizacja testów
- debugowanie
- wyjaśnianie struktur (ORM relacje, fixtures pytest)

## Planowane funkcjonalności

- [ ] Funkcjonalność usuwania rekordów (artystów, inżynierów, sprzętu, sesji, utworów)
- [ ] Edycja sesji nagraniowych
- [ ] Edycja utworów
- [ ] Edycja sprzętu
- [ ] Zaawansowane wyszukiwanie i filtrowanie

## Licencja

Ten projekt jest udostępniony na licencji **MIT License**.

### MIT License

```
Copyright (c) 2026 Arkadiusz Wiącek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Wsparcie

W przypadku pytań lub problemów, skontaktuj się z autorem projektu: 
arkadiusz.wiacek@uth.pl

---

**Wersja**: 1.1.0  
**Data ostatniej aktualizacji**: 25.01.2026
