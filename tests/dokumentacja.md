# Dokumentacja Testów

## Wstęp

Projekt zawiera kompleksowy zestaw testów napisany w `pytest`, obejmujący 6 plików testowych z ponad 60 przypadkami testowymi. Testy wykorzystują bazę danych SQLite w trybie in-memory, zapewniając izolację i szybkie wykonanie.

### Struktura katalogu `./tests`

```
tests/
├── __init__.py                    # Pusty plik modułu
├── conftest.py                    # Fixture i konfiguracja pytest
├── dokumentacja.md                # Dokumentacja testów
├── statystyki_uzycia.md          # Statystyki użycia fixtures
├── test_blueprints.py            # Testy integracyjne HTTP (~40 testów)
├── test_database.py              # Testy inicjalizacji bazy (2 testy)
├── test_seed.py                  # Testy seedowania danych (1 test)
├── test_services.py              # Testy logiki biznesowej (18 testów)
├── test_types.py                 # Dataklasy dla fixture
└── test_unit.py                  # Testy jednostkowe z mockami (~15 testów)
```

***

## 2. Konfiguracja testów `conftest.py`

### 2.1. Fixture `_db_in_memory` (autouse)

**Cel:** Zapewnienie świeżej bazy SQLite in-memory dla każdego testu.

```python
@pytest.fixture(autouse=True)
def _db_in_memory():
    """Zawsze uruchamiaj testy na świeżej bazie SQLite in-memory."""
```

**Działanie:**
- Tworzy engine SQLite w pamięci z `check_same_thread=False`
- Rejestruje adapter dla typów `datetime` do ISO format
- Podmienia globalną sesję `database.session` na testową
- Po zakończeniu testu usuwa wszystkie tabele i przywraca oryginalną sesję

**Zalety:**
- Pełna izolacja między testami
- Brak zapisów na dysku
- Szybkie wykonanie (wszystko w RAM)

### 2.2. Fixture `client`

Zwraca `FlaskClient` z wyłączonym CSRF i trybem testowym.

```python
@pytest.fixture(scope="function", name="client")
def fixture_client() -> FlaskClient:
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False
    test_app.config["SECRET_KEY"] = "test-secret"
```

### 2.3. Factory fixtures

Projekt używa wzorca **factory fixtures** do tworzenia danych testowych:

| Fixture | Parametry | Zwraca | Zastosowanie |
|---------|-----------|--------|--------------|
| `create_artist` | `nazwa`, `imie`, `nazwisko` | `Artysci` | Tworzenie artystów przez POST |
| `create_engineer` | `imie`, `nazwisko` | `Inzynierowie` | Tworzenie inżynierów |
| `create_equipment` | `producent`, `model`, `kategoria` | `Sprzet` | Tworzenie sprzętu |
| `create_session` | `artist`, `engineer`, `termin_start`, `sprzet_ids` | `Sesje` | Tworzenie sesji z relacjami |
| `create_song` | `artist`, `sesja`, `tytul` | `Utwory` | Tworzenie utworów |

**Przykład użycia:**
```python
def test_example(create_artist, create_engineer):
    artist = create_artist(nazwa="TestBand", imie="Jan")
    engineer = create_engineer(imie="Adam", nazwisko="Nowak")
    # ... dalszy test
```

### 2.4. Złożone fixture

#### `utwory_base_setup`
Tworzy kompletny zestaw: artysta + inżynier + sesja dla testów utworów.

#### `session_with_equipment`
Tworzy sesję z dwoma elementami sprzętu - gotowa do testów relacji many-to-many.

### 2.5. Dataclass fixtures

Projekt używa dataclass do grupowania powiązanych fixture:

- **`ArtystaFixtures`** - dla testów artystów
- **`SesjaFixtures`** - dla testów sesji
- **`MonkeyPatchFixtures`** - dla testów z monkeypatch
- **`SimpleMonkeyPatchFixtures`** - dla prostszych testów monkeypatch

**Zaleta:** Lepsza czytelność i type hints w testach.

### 2.6. Mock fixtures dla seedowania

```python
@pytest.fixture
def mock_db_seed(monkeypatch):
    class MockConnection:
        executescript_called = commit_called = close_called = False
...
```

Używany w `test_seed.py` do weryfikacji wywołań bez faktycznego seedowania bazy.

***

## 3. Plik `test_blueprints.py` - Testy integracyjne HTTP

### 3.1. Struktura testów

Testy są podzielone na klasy według blueprintów:

- `TestArtysciEndpoints` (12 testów)
- `TestInzynierowieEndpoints` (7 testów)
- `TestSprzetEndpoints` (2 testy)
- `TestUtworyEndpoints` (4 testy)
- `TestSesjeEndpoints` (15 testów)

### 3.2. Kluczowe wzorce testowe

#### Testowanie widoków GET
```python
def test_list_empty(self, client):
    response = client.get("/artysci/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Studio nagrań" in html
    assert "Artyści" in html
```

#### Testowanie sortowania
```python
def test_list_sorting(self, create_artist, client):
    create_artist(nazwa="Zenek", imie="Z")
    create_artist(nazwa="Adam", imie="A")
    
    response = client.get("/artysci/?sort=Nazwa&order=asc")
    html = response.get_data(as_text=True)
    
    assert response.status_code == 200
    assert html.index("Adam") < html.index("Zenek")
```

**Uwaga:** Test sprawdza kolejność tekstu w HTML, nie tylko obecność danych.

#### Testowanie POST z utworzeniem rekordu
```python
def test_dodaj_sesje_post_creates_session(self, create_artist, create_engineer, client, db_session):
    artist = create_artist(nazwa="PostArtist")
    engineer = create_engineer(imie="PostEng", nazwisko="PE")
    
    resp = client.post(
        "/sesje/dodaj",
        data={
            "artysta": str(artist.IdArtysty),
            "inzynier": str(engineer.IdInzyniera),
            "termin_start": "2025-05-01 18:00",
            "sprzet": [],
        },
        follow_redirects=True,
    )
    
    sesja = db_session.query(Sesje).filter_by(
        IdArtysty=artist.IdArtysty
    ).first()

    assert resp.status_code == 200
    assert sesja is not None
```

### 3.3. Testowanie walidacji dat

Projekt zawiera rozbudowane testy walidacji formatu daty:

```python
def test_dodaj_sesje_invalid_date_format(self, create_artist, create_engineer, client):
    # ... setup
    resp = client.post("/sesje/dodaj", data={
        "termin_start": "01-01-2025",
    })
    assert resp.status_code == 200
    assert "Nieprawidłowy format".encode() in resp.data
```

**Testowane przypadki:**
- Format `DD-MM-YYYY` zamiast `YYYY-MM-DD`
- Pusta data
- Format z `/` zamiast `-`
- Format `DD/MM/YYYY`
- Kompletnie błędny string

### 3.4. Testowanie z monkeypatch

```python
def test_edytuj_sesje_post_hits_updated_none_branch(
    self, monkeypatch_fixtures: MonkeyPatchFixtures
):
    artist = monkeypatch_fixtures.create_artist(nazwa="PatchArtist")
    engineer = monkeypatch_fixtures.create_engineer(imie="Patch", nazwisko="Eng")
    sesja = monkeypatch_fixtures.create_session(artist, engineer)
    
    def mock_update(_idsesji, _session_data):
        return None
    
    monkeypatch_fixtures.monkeypatch.setattr(
        sesje_view_module,
        "update_session_with_equipment", 
        mock_update
    )
    
    resp = monkeypatch_fixtures.client.post(f"/sesje/edytuj/{sesja.IdSesji}", ...)

    assert resp.status_code == 404
```

**Cel:** Testowanie ścieżek błędów, które są trudne do wywołania naturalnie.

### 3.5. Testowanie relacji many-to-many

```python
def test_create_multi_sprzet(self, session_with_equipment, db_session):
    _, _, sesja, _ = session_with_equipment
    
    assert sesja is not None
    assert db_session.query(SprzetySesje).filter_by(IdSesji=sesja.IdSesji).count() == 2
```

Weryfikuje poprawne utworzenie wpisów w tabeli pośredniej `SprzetySesje`.

***

## 4. Plik `test_services.py` - Testy logiki biznesowej

### 4.1. Testowanie operacji CRUD

#### `test_create_record_persists_artist`
```python
def test_create_record_persists_artist(self, db_session):
    create_record(Artysci, Nazwa="BandA", Imie="Jan", Nazwisko="Kowalski")

    saved = db_session.query(Artysci).filter_by(Nazwa="BandA").first()

    assert saved is not None
    assert saved.Nazwa == "BandA"
```

**Wzorzec:** Create → Flush → Query → Assert

#### `test_update_record`
```python
def test_update_record(self, db_session):
    create_record(Artysci, Nazwa="Before", Imie="Old")

    artist = db_session.query(Artysci).filter_by(Nazwa="Before").one()
    update_record(artist, Nazwa="After", Imie="New")
    refreshed = db_session.query(Artysci).filter_by(IdArtysty=artist.IdArtysty).one()

    assert refreshed.Nazwa == "After"
```

### 4.2. Testowanie sortowania

```python
def test_get_all_sorted_orders(self):
    create_record(Artysci, Nazwa="B")
    create_record(Artysci, Nazwa="A")

    result = get_all_sorted(Artysci, "Nazwa", "asc")

    assert [a.Nazwa for a in result] == ["A", "B"]
```

**Wzorzec:** Create unordered → Sort → Assert order

### 4.3. Testowanie filtrowania

```python
def test_get_utwory_by_artist_returns_only_matching(self):
    a1 = create_record(Artysci, Nazwa="A1")
    a2 = create_record(Artysci, Nazwa="A2")
    # ... setup sesji
    create_record(Utwory, IdArtysty=a1.IdArtysty, Tytul="SongA1")
    create_record(Utwory, IdArtysty=a2.IdArtysty, Tytul="SongA2")
    
    result = get_utwory_by_artist(a1.IdArtysty)
    assert [u.Tytul for u in result] == ["SongA1"]
```

Weryfikuje, że filtrowanie nie zwraca danych innych artystów.

### 4.4. Testowanie złożonych relacji

```python
def test_get_session_details_loads_related(self, db_session):
    artist = create_record(Artysci, Nazwa="BandX")
    eng = create_record(Inzynierowie, Imie="Eng", Nazwisko="One")
    sesja = create_record(Sesje, IdArtysty=artist.IdArtysty, ...)
    create_record(Utwory, IdArtysty=artist.IdArtysty, IdSesji=sesja.IdSesji, Tytul="Hit")
    sprzet = create_record(Sprzet, Producent="P", Model="M", Kategoria="Mikrofony")
    db_session.add(SprzetySesje(IdSprzetu=sprzet.IdSprzetu, IdSesji=sesja.IdSesji))
    
    details = get_session_details(sesja.IdSesji)
    assert details.artysci.Nazwa == "BandX"
    assert any(u.Tytul == "Hit" for u in details.utwory)
    assert any(link.sprzet.Model == "M" for link in details.sprzety_sesje)
```

**Sprawdza:**
- Eager loading relacji
- Poprawność join'ów
- Dostęp do zagnieżdżonych danych

### 4.5. Testowanie rollback przy błędach

```python
def test_get_db_session_rolls_back_on_error(self, db_session):
    before = db_session.query(Artysci).count()
    
    with pytest.raises(TypeError):
        create_record(Artysci, NIEISTNIEJACE_POLE="X")
    
    after = db_session.query(Artysci).count()
    assert after == before
```

Weryfikuje, że context manager `get_db_session` poprawnie wycofuje zmiany.

***

## 5. Plik `test_unit.py` - Testy jednostkowe z mockami

### 5.1. Testowanie z mock session

```python
@pytest.fixture
def mock_session(self):
    session = Mock(spec=Session)
    session.execute.return_value.scalars.return_value.all.return_value = []
    session.query.return_value.filter.return_value.first.return_value = None
    return session
```

**Cel:** Testowanie logiki bez faktycznego dostępu do bazy.

### 5.2. Testowanie `safe_date_parse`

Funkcja ma **10 przypadków testowych** pokrywających:

#### Poprawne formaty
```python
def test_valid_datetime_space(self):
    result = safe_date_parse('2026-01-25 14:30')

    assert result == dt(2026, 1, 25, 14, 30)

def test_valid_datetime_iso_format(self):
    result = safe_date_parse('2026-01-25T14:30')

    assert result == dt(2026, 1, 25, 14, 30)
```

#### Błędy walidacji
```python
def test_empty_string(self):
    with pytest.raises(ValueError, match='Pusta data'):
        safe_date_parse('')

def test_bad_date_part_dashes(self):
    with pytest.raises(ValueError, match='Zly format daty'):
        safe_date_parse('2026/01/25 14:30')
```

**Testowane przypadki:**
- Pusta data / None / whitespace
- Zła długość części daty
- Zły separator (/ zamiast -)
- Zły format czasu (. zamiast :)
- Złą kolejność (DD-MM-YYYY)

### 5.3. Testowanie metadanych modeli

```python
def test_artysci_columns(self):
    insp = inspect(Artysci)
    columns = [col.name for col in insp.c]
    assert 'IdArtysty' in columns
    assert 'Nazwa' in columns
```

Weryfikuje poprawność definicji SQLAlchemy.

***

## 6. Plik `test_database.py` - Testy inicjalizacji

### 6.1. Test tworzenia tabel

```python
def test_init_db_creates_tables():
    database.init_db()
```

Prosty smoke test sprawdzający, czy `init_db()` wykonuje się bez błędów.

### 6.2. Test komendy CLI

```python
def test_init_db_cli_command_calls_init_db_and_echoes_message(client, monkeypatch):
    app = client.application
    database.init_app(app)
    
    called = {"n": 0}
    def fake_init_db():
        called["n"] += 1
    
    monkeypatch.setattr(database, "init_db", fake_init_db)
    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    
    assert result.exit_code == 0
    assert called["n"] == 1
    assert "Initialized the database." in result.output
```

**Sprawdza:**
- Wywołanie funkcji `init_db`
- Exit code = 0
- Komunikat w output

***

## 7. Plik `test_types.py` - Definicje pomocnicze

Zawiera 4 dataclass używane w fixture:

```python
@dataclass
class ArtystaFixtures:
    create_artist: callable
    create_engineer: callable
    create_session: callable
    create_song: callable
    client: object
    db_session: object
```

**Zalety:**
- Type hints w IDE
- Grupowanie powiązanych fixture
- Lepsza czytelność testów

***

## 8. Statystyki pokrycia testami

### Według typów testów

| Typ testu | Liczba testów | Pliki |
|-----------|---------------|-------|
| Integracyjne HTTP | ~40 | `test_blueprints.py` |
| Logika biznesowa | 18 | `test_services.py` |
| Jednostkowe z mockami | ~15 | `test_unit.py` |
| Inicjalizacja | 2 | `test_database.py` |
| **RAZEM** | **~75** | **4 pliki** |

### Pokrycie funkcjonalności

| Moduł aplikacji | Pokrycie testami | Uwagi |
|-----------------|------------------|-------|
| `services.py` | ✅ Pełne | Testy integracyjne + jednostkowe |
| `views/*.py` | ✅ Bardzo dobre | Wszystkie endpointy + edge cases |
| `models.py` | ✅ Dobre | Podstawowe testy metadanych |
| `database.py` | ⚠️ Częściowe | Tylko `init_db` |

***

## 9. Wzorce i dobre praktyki

### 9.1. Izolacja testów
- Każdy test działa na świeżej bazie in-memory
- Brak zależności między testami
- Fixture `autouse=True` zapewnia sprzątanie

### 9.2. Factory pattern
- Funkcje `create_*` zamiast bezpośredniego tworzenia
- Domyślne wartości dla wygody
- Możliwość override parametrów

### 9.3. Dataclass fixtures
- Grupowanie powiązanych dependencies
- Lepsze type hints
- Czytelniejsze signatury testów

### 9.4. Testowanie edge cases
- Walidacja dat: 6 różnych błędnych formatów
- Brakujące dane w formularzach
- Rollback przy błędach
- Nieistniejące ID (404)

### 9.5. Monkeypatch dla trudnych ścieżek
```python
monkeypatch.setattr(module, "function", mock_function)
```
Pozwala przetestować ścieżki błędów bez symulowania rzeczywistych awarii.

***

## 10. Możliwe ulepszenia

### 10.1. Brakujące obszary

1. **Testy wydajnościowe**
   - Brak testów z dużą ilością danych
   - Nie sprawdzono zachowania przy >1000 rekordów

2. **Testy bezpieczeństwa**
   - Brak testów SQL injection
   - Brak testów XSS w formularzach
   - Nie sprawdzono CSRF (wyłączone w testach)

3. **Testy end-to-end**
   - Brak Selenium/Playwright
   - Nie sprawdzono JavaScript
   - Brak testów interakcji z modałami

### 10.2. Metryki pokrycia

```bash
pytest --cov=app --cov-report=html
```

***

## 11. Uruchamianie testów

### Wszystkie testy
```bash
pytest tests/
```

### Konkretny plik
```bash
pytest tests/test_services.py
```

### Z verbose output
```bash
pytest tests/ -v
```

### Z pokryciem kodu
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Tylko testy dopasowane do wzorca
```bash
pytest tests/ -k "test_dodaj"
```

***

## 12. Podsumowanie

✅ **Mocne strony:**
- Pełna izolacja testów przez in-memory DB
- Factory fixtures zwiększające DRY
- Rozbudowane testy walidacji
- Testowanie edge cases i błędów
- Użycie monkeypatch do trudnych ścieżek
- Dataclass fixtures dla czytelności

⚠️ **Obszary do poprawy:**
- Dodać raporty pokrycia kodu
- Rozważyć testy E2E z Selenium
- Dodać testy bezpieczeństwa
- Parametryzować podobne testy
- Dodać docstringi w formacie Given-When-Then