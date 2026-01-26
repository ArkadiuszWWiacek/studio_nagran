# ZAKTUALIZOWANY README.md DLA PROJEKTU STUDIO_NAGRAN

# Studio Nagrań 🎵

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://img.shields.io/badge/tests-75%20passing-brightgreen.svg)

Aplikacja webowa do zarządzania studiem nagrań, umożliwiająca rejestrację sesji nagraniowych, artystów, inżynierów dźwięku, sprzętu oraz utworów muzycznych.

## 📋 Spis treści

- [Autor](#autor)
- [Opis projektu](#opis-projektu)
- [Funkcjonalności](#funkcjonalności)
- [Wymagania systemowe](#wymagania-systemowe)
- [Technologie](#technologie)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Uruchomienie](#uruchomienie-aplikacji)
- [Komendy CLI](#komendy-cli)
- [Model bazy danych](#model-bazy-danych)
- [Struktura projektu](#struktura-projektu)
- [Testy](#testy-i-narzędzia)
- [Użycie AI](#użycie-ai-w-projekcie)
- [Planowane funkcjonalności](#planowane-funkcjonalności)
- [Licencja](#licencja)

## 👤 Autor

**Arkadiusz Wiącek - 35027**  
📧 arkadiusz.wiacek@uth.pl

## 📖 Opis projektu

Studio Nagrań to system zarządzania bazą danych studia nagraniowego zbudowany przy użyciu Flask i SQLAlchemy. Aplikacja umożliwia kompleksowe zarządzanie wszystkimi aspektami działalności studia, w tym:

- 👨‍🎤 Rejestracja i zarządzanie artystami (soliści i zespoły)
- 🎛️ Zarządzanie inżynierami dźwięku
- 🎤 Katalog sprzętu studyjnego (mikrofony, przedwzmacniacze, efekty, itp.)
- 📅 Planowanie i rejestracja sesji nagraniowych
- 🎵 Katalog nagranych utworów

## ✨ Funkcjonalności

### 🎤 Zarządzanie artystami
- ✅ Przeglądanie (`/artysci`) - lista wszystkich artystów z możliwością sortowania
- ✅ Dodawanie (`/artysci/dodaj`) - formularz dodawania nowego artysty
- ✅ Edycja (`/artysci/edytuj/<id>`) - formularz edycji danych artysty
- ✅ Utwory artysty (`/artysci/<id>`) - lista utworów danego artysty (modal)

### 🎛️ Zarządzanie inżynierami
- ✅ Przeglądanie (`/inzynierowie`) - lista wszystkich inżynierów z możliwością sortowania
- ✅ Dodawanie (`/inzynierowie/dodaj`) - formularz dodawania nowego inżyniera
- ✅ Edycja (`/inzynierowie/edytuj/<id>`) - formularz edycji danych inżyniera

### 🎚️ Zarządzanie sprzętem
- ✅ Przeglądanie (`/sprzet`) - lista całego sprzętu z możliwością sortowania
- ✅ Dodawanie (`/sprzet/dodaj`) - formularz dodawania nowego sprzętu

### 🎵 Zarządzanie utworami
- ✅ Przeglądanie (`/utwory`) - lista wszystkich utworów z danymi artysty i sesji
- ✅ Dodawanie (`/utwory/dodaj`) - formularz dodawania nowego utworu

### 📅 Zarządzanie sesjami
- ✅ Przeglądanie (`/sesje`) - lista wszystkich sesji z możliwością sortowania
- ✅ Dodawanie (`/sesje/dodaj`) - formularz dodawania nowej sesji z wyborem sprzętu
- ✅ Edycja (`/sesje/edytuj/<id>`) - formularz edycji sesji z możliwością zmiany sprzętu
- ✅ Szczegóły sesji (`/sesje/<id>`) - pełne informacje o sesji, wykorzystanym sprzęcie i utworach

### 🔍 Sortowanie danych

Wszystkie widoki list obsługują sortowanie poprzez parametry URL:
- `sort` - kolumna do sortowania
- `order` - kierunek sortowania (`asc` lub `desc`)

**Przykład:** `/artysci?sort=Nazwisko&order=desc`

## 💻 Wymagania systemowe

- Python 3.12+ lub nowszy
- SQLite (wbudowane w Python)
- Przeglądarka internetowa (Chrome, Firefox, Safari, Edge)

## 🛠️ Technologie

| Kategoria | Technologia | Wersja |
|-----------|-------------|---------|
| **Backend** | Flask | 3.1.2 |
| **ORM** | SQLAlchemy | 2.0.45 |
| **Baza danych** | SQLite | - |
| **Frontend** | HTML/Jinja2 | - |
| **CSS** | Custom CSS | - |
| **Testy** | pytest | 9.0.2 |
| **Coverage** | pytest-cov | 7.0.0 |
| **Linting** | pylint | 4.0.4 |
| **CLI** | click | 8.3.1 |

## 📦 Instalacja

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

## ⚙️ Konfiguracja

### Baza danych

Domyślnie aplikacja korzysta z bazy SQLite `studio_nagran.db`, która jest tworzona automatycznie przy pierwszym uruchomieniu.

Konfiguracja połączenia znajduje się w `app/database.py`:

```python
engine = create_engine("sqlite:///studio_nagran.db", echo=True, future=True)
```

### Inicjalizacja bazy danych

Przed pierwszym użyciem zainicjalizuj strukturę bazy:

```bash
flask init-db
```

Komenda utworzy wszystkie wymagane tabele zgodnie z modelami SQLAlchemy.

### Załadowanie danych przykładowych

Aby załadować przykładowe dane (artystów, inżynierów, sprzęt, sesje):

```bash
flask seed
```

Dane przykładowe są wczytywane z pliku `seed_data.sql`.

### Tryb debugowania

Aplikacja domyślnie uruchamia się w trybie debug. W środowisku produkcyjnym zmień w `run.py`:

```python
app.run(host="0.0.0.0", port=5000, debug=False)
```

## 🚀 Uruchomienie aplikacji

Po zakończeniu [konfiguracji](#konfiguracja) uruchom aplikację:

```bash
python run.py
```

Aplikacja będzie dostępna pod adresem: **`http://localhost:5000`**

## 🔧 Komendy CLI

Aplikacja udostępnia własne komendy Flask CLI:

| Komenda | Opis |
|---------|------|
| `flask init-db` | Inicjalizuje strukturę bazy danych (tworzy tabele) |
| `flask seed` | Wczytuje dane przykładowe z `seed_data.sql` |

**Przykład użycia:**

```bash
# Inicjalizacja bazy
flask init-db

# Załadowanie przykładowych danych
flask seed
```

## 🗄️ Model bazy danych

### Tabele

#### Artysci
- `IdArtysty` (PK, INTEGER) - Identyfikator artysty
- `Nazwa` (TEXT) - Nazwa artysty/zespołu
- `Imie` (TEXT) - Imię (dla artystów solowych)
- `Nazwisko` (TEXT) - Nazwisko (dla artystów solowych)

#### Inzynierowie
- `IdInzyniera` (PK, INTEGER) - Identyfikator inżyniera
- `Imie` (TEXT) - Imię inżyniera
- `Nazwisko` (TEXT) - Nazwisko inżyniera

#### Sprzet
- `IdSprzetu` (PK, INTEGER) - Identyfikator sprzętu
- `Producent` (TEXT) - Producent sprzętu
- `Model` (TEXT) - Model sprzętu
- `Kategoria` (TEXT) - Kategoria sprzętu (mikrofon, przedwzmacniacz, itp.)

#### Sesje
- `IdSesji` (PK, INTEGER) - Identyfikator sesji
- `IdArtysty` (FK → Artysci) - Powiązanie z artystą
- `IdInzyniera` (FK → Inzynierowie) - Powiązanie z inżynierem
- `TerminStart` (DATETIME) - Data i czas rozpoczęcia sesji
- `TerminStop` (DATETIME, NULL) - Data i czas zakończenia sesji (opcjonalne)

#### Utwory
- `IdUtworu` (PK, INTEGER) - Identyfikator utworu
- `IdArtysty` (FK → Artysci) - Powiązanie z artystą
- `IdSesji` (FK → Sesje) - Powiązanie z sesją
- `Tytul` (TEXT) - Tytuł utworu

#### SprzetySesje (tabela powiązań many-to-many)
- `IdSprzetu` (PK, FK → Sprzet) - Identyfikator sprzętu
- `IdSesji` (PK, FK → Sesje) - Identyfikator sesji

### Relacje

```
Artysci (1) ──────┬──── (N) Sesje
                  └──── (N) Utwory

Inzynierowie (1) ─────── (N) Sesje

Sprzet (N) ──── SprzetySesje ──── (N) Sesje

Sesje (1) ─────────────────────── (N) Utwory
```

**Relacje szczegółowo:**
- Artysta może mieć wiele sesji i utworów (1:N)
- Inżynier może prowadzić wiele sesji (1:N)
- Sesja może wykorzystywać wiele jednostek sprzętu (N:M przez SprzetySesje)
- Sesja może zawierać wiele utworów (1:N)

## 📁 Struktura projektu

```
studio_nagran/
├── .gitignore                     # Pliki ignorowane przez Git
├── config.py                      # Konfiguracja aplikacji
├── pytest.ini                     # Konfiguracja pytest
├── README.md                      # Dokumentacja projektu
├── requirements.txt               # Zależności Python
├── run.py                         # Punkt wejścia aplikacji
├── run_tests.bat                  # Skrypt testów (Windows)
├── run_tests.sh                   # Skrypt testów (Linux/macOS)
├── seed_data.sql                  # Dane przykładowe SQL
├── studio_nagran.db               # Baza danych SQLite (generowana)
├── app/                           # Główny katalog aplikacji
│   ├── __init__.py               # Factory aplikacji Flask
│   ├── blueprints.py             # Rejestracja blueprintów
│   ├── database.py               # Konfiguracja bazy danych
│   ├── models.py                 # Modele SQLAlchemy
│   ├── services.py               # Logika biznesowa
│   ├── static/                   # Pliki statyczne
│   │   ├── style.css            # Style CSS
│   │   └── images/              # Obrazy
│   │       └── colour_wave.jpg  # Tło aplikacji
│   ├── templates/                # Szablony Jinja2
│   │   ├── base.html            # Szablon bazowy
│   │   ├── index.html           # Strona główna
│   │   ├── artysci.html         # Lista artystów
│   │   ├── dodaj_artyste.html   # Formularz dodawania artysty
│   │   ├── edytuj_artyste.html  # Formularz edycji artysty
│   │   ├── modal_utwory.html    # Modal z utworami artysty
│   │   ├── inzynierowie.html    # Lista inżynierów
│   │   ├── dodaj_inzyniera.html # Formularz dodawania inżyniera
│   │   ├── edytuj_inzyniera.html# Formularz edycji inżyniera
│   │   ├── sprzet.html          # Lista sprzętu
│   │   ├── dodaj_sprzet.html    # Formularz dodawania sprzętu
│   │   ├── utwory.html          # Lista utworów
│   │   ├── dodaj_utwor.html     # Formularz dodawania utworu
│   │   ├── sesje.html           # Lista sesji
│   │   ├── dodaj_sesje.html     # Formularz dodawania sesji
│   │   ├── edytuj_sesje.html    # Formularz edycji sesji
│   │   ├── sesja_detale.html    # Szczegóły sesji
│   │   └── modal_detale.html    # Modal ze szczegółami
│   └── views/                    # Kontrolery (blueprinty)
│       ├── __init__.py
│       ├── artysci.py           # Endpointy artystów
│       ├── inzynierowie.py      # Endpointy inżynierów
│       ├── sesje.py             # Endpointy sesji
│       ├── sprzet.py            # Endpointy sprzętu
│       └── utwory.py            # Endpointy utworów
└── tests/                        # Testy automatyczne
    ├── __init__.py
    ├── conftest.py              # Konfiguracja pytest + fixtures
    ├── dokumentacja.md          # Dokumentacja testów
    ├── statystyki_uzycia.md     # Raport użycia fixtures
    ├── test_blueprints.py       # Testy HTTP/Flask (40 testów)
    ├── test_database.py         # Testy inicjalizacji DB (2 testy)
    ├── test_seed.py             # Testy seedowania (2 testy)
    ├── test_services.py         # Testy logiki biznesowej (18 testów)
    ├── test_types.py            # Typy pomocnicze (dataclass)
    └── test_unit.py             # Testy jednostkowe z mockami (15 testów)
```

## 🧪 Testy i narzędzia

### Architektura testów

Projekt wykorzystuje **profesjonalne podejście warstwowe** z SQLite in-memory:

#### 📊 Statystyki testów

- **75+ testów** w 5 plikach testowych
- **~3.5s** czas wykonania pełnego zestawu
- **100% pokrycie** kluczowych ścieżek (CRUD + edge cases)
- **Izolacja** poprzez świeżą bazę in-memory dla każdego testu

#### 🔧 Fixtures

**12 reużywalnych fixtures** w `conftest.py`:

| Typ | Fixtures | Zastosowanie |
|-----|----------|--------------|
| **Setup** | `_db_in_memory` (autouse) | Izolacja testów - świeża baza dla każdego testu |
| **Flask** | `client` | FlaskClient do testów HTTP (33 użycia) |
| **Database** | `db_session` | Sesja SQLAlchemy (13 użyć) |
| **Factory** | `create_artist`, `create_engineer`, `create_equipment`, `create_session`, `create_song` | Tworzenie danych testowych (31 użyć łącznie) |
| **Composite** | `utwory_base_setup`, `session_with_equipment` | Złożone scenariusze testowe |
| **Dataclass** | `fixtures`, `session_fixtures`, `monkeypatch_fixtures`, `simple_monkeypatch_fixtures` | Grupowanie powiązanych dependencies |
| **Mock** | `mock_session`, `mock_db_seed` | Testy jednostkowe z izolacją |

**Wzorce:** AAA (Arrange-Act-Assert), Factory Pattern, Composite Fixtures

#### 📂 Typy testów

| Plik | Liczba testów | Typ | Opis |
|------|---------------|-----|------|
| `test_blueprints.py` | 40 | **End-to-end** | Pełne testy HTTP (GET/POST, redirecty, 404, walidacja) |
| `test_services.py` | 18 | **Integracyjne** | Serwisy + prawdziwa baza (sortowanie, relacje, rollback) |
| `test_unit.py` | 15 | **Jednostkowe** | Mock SQLAlchemy dla izolowanych testów serwisów |
| `test_database.py` | 2 | **Setup** | Inicjalizacja bazy + CLI commands |
| `test_seed.py` | 2 | **Setup** | Seedowanie danych przykładowych |

**Dokumentacja testów:** [`/tests/dokumentacja.md`](./tests/dokumentacja.md)  
**Raport fixtures:** [`/tests/statystyki_uzycia.md`](./tests/statystyki_uzycia.md)

### Uruchomienie testów

#### Wszystkie testy z pokryciem
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

#### Szybkie uruchomienie (bez pokrycia)
```bash
pytest tests/ -v
```

#### Tylko konkretny plik
```bash
pytest tests/test_services.py -v
```

#### Testy dopasowane do wzorca
```bash
pytest tests/ -k "test_dodaj" -v
```

### Skrypty automatyzujące

#### Linux / macOS
```bash
chmod +x run_tests.sh
./run_tests.sh
```

#### Windows
```bash
run_tests.bat
```

**Skrypty uruchamiają:**
1. pytest z raportem pokrycia
2. pylint z parametrami projektu

### Analiza statyczna

Pylint z pominiętymi komunikatami `missing-function-docstring` i `too-few-public-methods`:

```bash
pylint ./ --ignore=.venv --disable=C0114,C0115,C0116,R0903
```

## 🤖 Użycie AI w projekcie

**Perplexity AI** (różne modele) zastosowano do:
- ✅ Generowanie/aktualizacja/refaktoryzacja testów
- ✅ Debugowanie i rozwiązywanie problemów
- ✅ Wyjaśnianie struktur (ORM relacje, fixtures pytest)
- ✅ Dokumentacja techniczna (README, raporty)
- ✅ Optymalizacja kodu i best practices

## 🚧 Planowane funkcjonalności

### ✅ Zrealizowane
- [x] Edycja sesji nagraniowych
- [x] Pełne testy automatyczne (75+ testów)
- [x] Dokumentacja techniczna
- [x] CLI commands (seed, init-db)

### 📋 W planach
- [ ] Funkcjonalność usuwania rekordów (artystów, inżynierów, sprzętu, sesji, utworów)
- [ ] Edycja utworów
- [ ] Edycja sprzętu
- [ ] Zaawansowane wyszukiwanie i filtrowanie
- [ ] Eksport danych do CSV/PDF
- [ ] Dashboard ze statystykami
- [ ] Autentykacja użytkowników
- [ ] API REST

## 📄 Licencja

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

## 📞 Wsparcie

W przypadku pytań lub problemów, skontaktuj się z autorem projektu:  
📧 **arkadiusz.wiacek@uth.pl**

---

**Wersja**: 1.2.0  
**Data ostatniej aktualizacji**: 26.01.2026  
**Status**: 🟢 Aktywny rozwój
```