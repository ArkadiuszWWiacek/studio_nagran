# Dokumentacja Testów - System Zarządzania Studio Nagrań

## Wstęp

Projekt zawiera kompleksowy zestaw testów dla aplikacji Flask służącej do zarządzania studiem nagrań. Testy obejmują:
- Testy jednostkowe modeli danych
- Testy integracyjne serwisów
- Testy funkcjonalności endpointów blueprintów
- Testy inicjalizacji bazy danych
- Testy seed'owania bazy danych

Wszystkie testy działają na bazie SQLite in-memory dla szybkości i izolacji.

---

## 1. Architektura Testów

### 1.1 Pliki Testów

| Plik | Przeznaczenie | Liczba Testów |
|------|---------------|---------------|
| `conftest.py` | Konfiguracja pytest, fixtures, setupy | - |
| `test_types.py` | Definicje typów dataclass dla fixtures | - |
| `test_database.py` | Testy inicjalizacji bazy danych | 2 |
| `test_seed.py` | Testy seed'owania bazy danych | 2 |
| `test_services.py` | Testy integracyjne serwisów | 17 |
| `test_blueprints.py` | Testy endpointów HTTP | 38+ |

### 1.2 Struktura Bazy Danych Testowej

```
SQLite In-Memory
├── Artysci (artyści)
├── Inzynierowie (inżynierowie)
├── Sesje (sesje nagrań)
├── Utwory (utwory/piosenki)
├── Sprzet (sprzęt)
└── SprzetySesje (relacja wiele-do-wielu sesji i sprzętu)
```

---

## 2. Konfiguracja Testów (conftest.py)

### 2.1 Fixture Globalna: `_db_in_memory`

```python
@pytest.fixture(autouse=True)
def _db_in_memory():
    """Zawsze uruchamiaj testy na świeżej bazie SQLite in-memory."""
```

**Charakterystyka:**
- **Automatyczne uruchomienie** (`autouse=True`) dla każdego testu
- Tworzy engine SQLite in-memory: `sqlite:///:memory:`
- Rejestruje adaptator dla typu `datetime`
- Resetuje bazę po każdym teście
- Izoluje testy od siebie nawzajem

**Proces:**
1. Tworzy nowy engine SQLite
2. Konfiguruje session factory z `scoped_session`
3. Tworzy wszystkie tabele (`base.metadata.create_all`)
4. Zastępuje globalną sesję bazy testową
5. Po teście: usuwa tabele, czyści sesję, przywraca oryginalne obiekty

### 2.2 Fixture: `client`

```python
@pytest.fixture(scope="function", name="client")
def fixture_client() -> FlaskClient:
    """Fixture klienta testowego."""
```

**Przeznaczenie:** Testowanie endpointów HTTP
**Konfiguracja:**
- `TESTING = True` - tryb testowy Flask'a
- `WTF_CSRF_ENABLED = False` - wyłączenie CSRF dla testów
- Context manager zapewnia app context podczas testów

### 2.3 Fixture: `db_session`

```python
@pytest.fixture(scope="function", name="db_session")
def fixture_db_session():
    """Jedna ścieżka transakcyjna jak w services.py."""
```

**Przeznaczenie:** Bezpośrednie testowanie operacji bazodanowych

### 2.4 Factory Fixtures - Tworzenie Danych

#### `create_artist`
```python
def _create(nazwa="DefaultArtist", imie=None, nazwisko=None):
    # Tworzy artystę przez HTTP POST
    # Zwraca obiekt Artysci z bazy
```

**Parametry:**
- `nazwa` (wymagane) - nazwa zespołu
- `imie` (opcjonalne) - imię reprezentanta
- `nazwisko` (opcjonalne) - nazwisko reprezentanta

#### `create_engineer`
```python
def _create(imie="DefaultEng", nazwisko="DefaultSurname"):
    # Tworzy inżyniera przez HTTP POST
    # Zwraca obiekt Inzynierowie z bazy
```

#### `create_equipment`
```python
def _create(producent="DefaultProducer", model="M1", kategoria="Mikrofony"):
    # Tworzy sprzęt przez HTTP POST
    # Zwraca obiekt Sprzet z bazy
```

**Kategorie sprzętu:**
- `"Mikrofony"`
- `"Procesory"`
- Inne (zależy od ograniczeń bazy)

#### `create_session`
```python
def _create(artist, engineer, termin_start="2025-01-01", sprzet_ids=None):
    # Tworzy sesję nagrań
    # Zwraca obiekt Sesje z relacją do sprzętu
```

**Parametry:**
- `artist` - obiekt Artysci
- `engineer` - obiekt Inzynierowie
- `termin_start` - data rozpoczęcia (string lub datetime)
- `sprzet_ids` - lista ID sprzętu

#### `create_song`
```python
def _create(artist, sesja, tytul="DefaultSong"):
    # Tworzy utwór przez HTTP POST
    # Zwraca obiekt Utwory z bazy
```

### 2.5 Composite Fixtures - Bundlowanie Factories

#### `fixtures` (ArtystaFixtures)
```python
@pytest.fixture
def fixtures(create_artist, create_engineer, create_session, create_song, client, db_session):
    return ArtystaFixtures(...)
```

**Zawiera:** factories dla artystów, inżynierów, sesji, piosenek + klient + sesję bazową

**Użycie:**
```python
def test_example(self, fixtures: ArtystaFixtures):
    artist = fixtures.create_artist(nazwa="Band")
    song = fixtures.create_song(artist, session, tytul="Song")
```

#### `session_fixtures` (SesjaFixtures)
Jak wyżej, ale dla testów sesji z dodanym `create_equipment`

#### `monkeypatch_fixtures` (MonkeyPatchFixtures)
Dla testów wymagających mockowania z pytest.monkeypatch

#### `simple_monkeypatch_fixtures` (SimpleMonkeyPatchFixtures)
Minimalna wersja: `client` + `monkeypatch`

### 2.6 Fixture: `mock_db_seed`

```python
@pytest.fixture
def mock_db_seed(monkeypatch):
    """Mockuje operacje bazy danych dla testów seed'owania."""
```

**Mockuje:**
- `sqlite3.connect()` - zwraca MockConnection
- `builtins.open()` - zwraca MockFile

**MockConnection:**
- `executescript_called` - flaga czy wykonano SQL
- `commit_called` - flaga czy zacommitowano
- `close_called` - flaga czy zamknięto

**MockFile:**
- `read_called` - flaga czy odczytano
- `read()` - zwraca `"-- seed SQL content"`

---

## 3. Testy Typów (test_types.py)

### 3.1 Klasy Dataclass

#### ArtystaFixtures
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

**Przeznaczenie:** Grupowanie fixtures dla testów artystów

#### SesjaFixtures
```python
@dataclass
class SesjaFixtures:
    create_artist: callable
    create_engineer: callable
    create_equipment: callable
    create_session: callable
    client: object
    db_session: object
```

**Przeznaczenie:** Fixtures dla testów sesji z obsługą sprzętu

#### MonkeyPatchFixtures
```python
@dataclass
class MonkeyPatchFixtures:
    create_artist: callable
    create_engineer: callable
    create_session: callable
    client: object
    monkeypatch: object
```

**Przeznaczenie:** Fixtures dla testów z mockingiem

#### SimpleMonkeyPatchFixtures
```python
@dataclass
class SimpleMonkeyPatchFixtures:
    client: object
    monkeypatch: object
```

**Przeznaczenie:** Minimalne fixtures dla prostych testów z monkeypatch

---

## 4. Testy Bazy Danych (test_database.py)

### 4.1 `test_init_db_creates_tables()`

```python
def test_init_db_creates_tables():
    database.init_db()
```

**Testuje:**
- Funkcja `database.init_db()` poprawnie tworzy tabele

**Asercje:**
- Brak wyjątku - funkcja się wykonuje

### 4.2 `test_init_db_cli_command_calls_init_db_and_echoes_message()`

```python
def test_init_db_cli_command_calls_init_db_and_echoes_message(client, monkeypatch):
    # Mock'uje init_db
    # Wywoła CLI command 'init-db'
    # Sprawdza czy init_db została wywołana i czy wiadomość się wydrukuje
```

**Testuje:**
- CLI command `init-db` poprawnie wywoła `database.init_db()`
- Wydrukuje komunikat `"Initialized the database."`

**Technika:**
- Monkeypatch do podmienienia `database.init_db()`
- Licznik `called["n"]` do weryfikacji wywołania

---

## 5. Testy Seed'owania (test_seed.py)

### 5.1 `test_seed_database()`

```python
def test_seed_database(mock_db_seed):
    mock_conn, mock_file = mock_db_seed
    seed_database()
    
    assert mock_conn.executescript_called
    assert mock_file.read_called
    assert mock_conn.commit_called
    assert mock_conn.close_called
```

**Testuje:**
- Funkcja `seed_database()` wykonuje seed bazy

**Kroki:**
1. Otwiera plik SQL
2. Wykonuje SQL skrypt (`executescript`)
3. Commituje zmiany
4. Zamyka połączenie

### 5.2 `test_seed_cli_calls_database()`

```python
def test_seed_cli_calls_database(mock_db_seed):
    app = create_app()
    runner = CliRunner()
    result = runner.invoke(app.cli, ['seed'])
    
    assert result.exit_code == 0
    assert 'Baza zaseedowana!' in result.stdout
```

**Testuje:**
- CLI command `seed` poprawnie seed'uje bazę
- Wydrukuje komunikat `"Baza zaseedowana!"`

---

## 6. Testy Serwisów (test_services.py)

### 6.1 Testy `get_all_sorted()`

#### `test_get_all_sorted_empty()`
```python
def test_get_all_sorted_empty(self):
    result = get_all_sorted(Artysci, "Nazwa", "asc")
    assert result == []
```
Testuje zwracanie pustej listy dla pustej tabeli

#### `test_get_all_sorted_orders()`
```python
result = get_all_sorted(Artysci, "Nazwa", "asc")
assert [a.Nazwa for a in result] == ["A", "B"]
```
Testuje sortowanie rosnące (ascending)

#### `test_get_all_sorted_orders_desc()`
```python
result = get_all_sorted(Artysci, "Nazwa", "desc")
assert [a.Nazwa for a in result] == ["B", "A"]
```
Testuje sortowanie malejące (descending)

### 6.2 Testy `create_record()`

#### `test_create_record_persists_artist()`
```python
create_record(Artysci, Nazwa="BandA", Imie="Jan", Nazwisko="Kowalski")
saved = db_session.query(Artysci).filter_by(Nazwa="BandA").first()
assert saved is not None
assert saved.Imie == "Jan"
```
Testuje:
- Tworzenie artysty przez serwis
- Persistence w bazie
- Poprawne wartości atrybutów

#### `test_create_inzynier_persists()`
Analogicznie dla inżynierów

#### `test_create_sprzet_persists()`
Analogicznie dla sprzętu z kategorią "Mikrofony"

### 6.3 Testy `get_by_id()`

```python
def test_get_by_id(self, db_session):
    create_record(Artysci, Nazwa="FindMe")
    artist_id = db_session.query(Artysci).filter_by(Nazwa="FindMe").one().IdArtysty
    found = get_by_id(Artysci, artist_id)
    assert found is not None
    assert found.Nazwa == "FindMe"
```

Testuje:
- Wyszukiwanie po ID
- Zwrócenie poprawnego obiektu

### 6.4 Testy `update_record()`

```python
def test_update_record(self, db_session):
    create_record(Artysci, Nazwa="Before", Imie="Old")
    artist = db_session.query(Artysci).filter_by(Nazwa="Before").one()
    update_record(artist, Nazwa="After", Imie="New")
    refreshed = db_session.query(Artysci).filter_by(IdArtysty=artist.IdArtysty).one()
    assert refreshed.Nazwa == "After"
    assert refreshed.Imie == "New"
```

Testuje:
- Aktualizację istniejącego rekordu
- Persistence zmian

### 6.5 Testy `get_utwory_by_artist()`

```python
def test_get_utwory_by_artist_returns_only_matching(self):
    a1 = create_record(Artysci, Nazwa="A1")
    a2 = create_record(Artysci, Nazwa="A2")
    eng = create_record(Inzynierowie, Imie="E", Nazwisko="X")
    sesja = create_record(Sesje, IdArtysty=a1.IdArtysty, IdInzyniera=eng.IdInzyniera, ...)
    create_record(Utwory, IdArtysty=a1.IdArtysty, IdSesji=sesja.IdSesji, Tytul="SongA1")
    create_record(Utwory, IdArtysty=a2.IdArtysty, IdSesji=sesja.IdSesji, Tytul="SongA2")
    result = get_utwory_by_artist(a1.IdArtysty)
    assert [u.Tytul for u in result] == ["SongA1"]
```

Testuje:
- Filtrowanie utworów po ID artysty
- Ignoruje utwory innych artystów

### 6.6 Testy `get_utwory_sorted()`

#### `test_get_utwory_sorted_by_artist_first_name()`
```python
result = get_utwory_sorted(sortby="Imie", order="asc")
assert [u.artysci.Imie for u in result][:2] == ["Adam", "Zen"]
```

Testuje:
- Sortowanie utworów po imienia artysty
- Relacja do tabeli artystów (u.artysci.Imie)

#### `test_get_utwory_sorted_defaults_when_unknown_sort()`
```python
result = get_utwory_sorted(sortby="NIE_MA", order="asc")
assert len(result) == 2
```

Testuje:
- Fallback do domyślnego sortowania dla nieznanego pola
- Zwrócenie wszystkich rekordów

### 6.7 Testy `get_sessions_sorted()`

#### `test_get_sessions_sorted_by_artist_name()`
```python
result = get_sessions_sorted(sortby="NazwaArtysty", order="asc")
assert [s.artysci.Nazwa for s in result][:2] == ["Adam", "Zenek"]
```

Testuje:
- Sortowanie sesji po nazwie artysty
- Relacja do tabeli artystów

#### `test_get_sessions_sorted_by_engineer_last_name()`
```python
result = get_sessions_sorted(sortby="NazwiskoInzyniera", order="asc")
assert [s.inzynierowie.Nazwisko for s in result][:2] == ["Adamski", "Nowak"]
```

Testuje:
- Sortowanie sesji po nazwisku inżyniera
- Relacja do tabeli inżynierów

### 6.8 Testy `get_session_details()`

```python
def test_get_session_details_loads_related(self, db_session):
    artist = create_record(Artysci, Nazwa="BandX")
    eng = create_record(Inzynierowie, Imie="Eng", Nazwisko="One")
    sesja = create_record(Sesje, IdArtysty=artist.IdArtysty, ...)
    create_record(Utwory, IdArtysty=artist.IdArtysty, IdSesji=sesja.IdSesji, Tytul="Hit")
    sprzet = create_record(Sprzet, Producent="P", Model="M", Kategoria="Mikrofony")
    db_session.add(SprzetySesje(IdSprzetu=sprzet.IdSprzetu, IdSesji=sesja.IdSesji))
    db_session.flush()
    
    details = get_session_details(sesja.IdSesji)
    assert details.artysci.Nazwa == "BandX"
    assert details.inzynierowie.Nazwisko == "One"
    assert any(u.Tytul == "Hit" for u in details.utwory)
    assert any(link.sprzet.Model == "M" for link in details.sprzety_sesje)
```

Testuje:
- Ładowanie sesji z wszystkimi relacjami
- Dostęp do artysty, inżyniera, utworów
- Dostęp do sprzętu przez tabelę pośrednią

### 6.9 Testy `create_session_with_equipment()`

```python
def test_create_session_with_equipment_creates_links(self, db_session):
    artist = create_record(Artysci, Nazwa="Band")
    eng = create_record(Inzynierowie, Imie="Eng", Nazwisko="X")
    s1 = create_record(Sprzet, Producent="P1", Model="M1", Kategoria="Mikrofony")
    s2 = create_record(Sprzet, Producent="P2", Model="M2", Kategoria="Procesory")
    
    session_data = SessionData(
        idartysty=artist.IdArtysty,
        idinzyniera=eng.IdInzyniera,
        terminstart=datetime(2026, 1, 20, 10, 0),
        terminstop=datetime(2026, 1, 20, 12, 0),
        sprzet_ids=[s1.IdSprzetu, s2.IdSprzetu]
    )
    
    nowa = create_session_with_equipment(session_data)
    assert nowa.IdSesji is not None
    assert db_session.query(SprzetySesje).filter_by(IdSesji=nowa.IdSesji).count() == 2
```

Testuje:
- Tworzenie sesji z `SessionData` dataclass
- Automatyczne tworzenie linków SprzetySesje
- Liczba linków odpowiada liczbie sprzętu

### 6.10 Testy Obsługi Błędów

#### `test_get_db_session_rolls_back_on_error()`
```python
def test_get_db_session_rolls_back_on_error(self, db_session):
    before = db_session.query(Artysci).count()
    with pytest.raises(TypeError):
        create_record(Artysci, NIEISTNIEJACE_POLE="X")
    after = db_session.query(Artysci).count()
    assert after == before
```

Testuje:
- Rollback transakcji przy błędzie
- Dane nie są commitment'owane

---

## 7. Testy Blueprintów (test_blueprints.py)

### 7.1 Testy Endpointów Artystów (TestArtysciEndpoints)

#### `test_index_contains_expected_content()`
```python
resp = client.get("/")
assert resp.status_code == 200
assert "Studio nagrań" in html
```
Testuje: Strona główna zwraca kod 200 i zawiera tekst

#### `test_list_empty()`
```python
response = client.get("/artysci/")
assert response.status_code == 200
assert "Studio nagrań" in html
assert "Artyści" in html
```
Testuje: Lista artystów się renderuje, gdy lista jest pusta

#### `test_create_success()`
```python
artist = create_artist(nazwa="TestBand", imie="Jan", nazwisko="Kowalski")
assert artist is not None
assert artist.Imie == "Jan"
assert artist.Nazwisko == "Kowalski"
```
Testuje: Tworzenie artysty przez factory

#### `test_dodaj_artyste_get_renders_form()`
```python
resp = client.get("/artysci/dodaj")
assert resp.status_code == 200
```
Testuje: Formularz dodawania artysty się renderuje

#### `test_list_sorting()`
```python
create_artist(nazwa="Zenek", imie="Z")
create_artist(nazwa="Adam", imie="A")
response = client.get("/artysci/?sort=Nazwa&order=asc")
assert html.index("Adam") < html.index("Zenek")
```
Testuje:
- Parametry sortowania `sort` i `order`
- Właściwa kolejność w HTML (Adam przed Zenekiem)

#### `test_edytuj_get_renders_form()`
```python
artist = create_artist(nazwa="BandX", imie="Jan", nazwisko="Kowalski")
resp = client.get(f"/artysci/edytuj/{artist.IdArtysty}")
assert resp.status_code == 200
assert "BandX" in html
```
Testuje: Formularz edycji zawiera istniejące dane

#### `test_edytuj_post_updates_and_redirects()`
```python
artist = create_artist(nazwa="Before", imie="Old", nazwisko="X")
resp = client.post(
    f"/artysci/edytuj/{artist.IdArtysty}",
    data={"nazwa": "After", "imie": "New", "nazwisko": "Y"},
    follow_redirects=True,
)
assert resp.status_code == 200
refreshed = db_session.query(Artysci).filter_by(IdArtysty=artist.IdArtysty).one()
assert refreshed.Nazwa == "After"
assert refreshed.Imie == "New"
assert refreshed.Nazwisko == "Y"
```

Testuje:
- Edycja danych artysty
- Redirect po udanej edycji
- Persistence zmian w bazie

#### `test_utwory_artysty_renders_modal()`
```python
artist = create_artist(nazwa="BandU")
resp = client.get(f"/artysci/utwory/{artist.IdArtysty}")
assert resp.status_code == 200
```
Testuje: Modal z utworami artysty się renderuje

#### `test_utwory_artysty_renders_modal_contains_songs()`
```python
artist = fixtures.create_artist(nazwa="BandU")
engineer = fixtures.create_engineer(imie="EngU", nazwisko="EU")
sesja = fixtures.create_session(artist, engineer)
title = "BandU - HitSingle"
fixtures.create_song(artist, sesja, tytul=title)

resp = fixtures.client.get(f"/artysci/utwory/{artist.IdArtysty}")
assert title in html
```

Testuje:
- Utwory artysty są wyświetlane w modalu
- Tytuł utworu jest widoczny

### 7.2 Testy Endpointów Inżynierów (TestInzynierowieEndpoints)

#### `test_create_success()`
```python
eng = create_engineer(imie="TestAdam", nazwisko="TestNowak")
assert eng is not None
assert eng.Nazwisko == "TestNowak"
```

#### `test_list_rendering()`
```python
response = client.get("/inzynierowie/")
assert response.status_code == 200
```

#### `test_list_sorting()`
```python
create_engineer(imie="Zenon", nazwisko="Z")
create_engineer(imie="Adam", nazwisko="A")
resp = client.get("/inzynierowie/?sort=Imie&order=asc")
assert html.index("Adam") < html.index("Zenon")
```

#### `test_dodaj_inzyniera_get_renders_form()`
```python
resp = client.get("/inzynierowie/dodaj")
assert resp.status_code == 200
```

#### `test_dodaj_inzyniera_post_redirects()`
```python
resp = client.post("/inzynierowie/dodaj", data={"imie": "R", "nazwisko": "D"})
assert resp.status_code in (301, 302)
assert "/inzynierowie/" in resp.headers.get("Location", "")
```

Testuje: POST redirect do listy inżynierów

#### `test_edytuj_post_updates_and_redirects()`
```python
eng = create_engineer(imie="Old", nazwisko="Name")
resp = client.post(
    f"/inzynierowie/edytuj/{eng.IdInzyniera}",
    data={"imie": "New", "nazwisko": "Surname"},
    follow_redirects=True,
)
assert resp.status_code == 200
refreshed = db_session.query(Inzynierowie).filter_by(IdInzyniera=eng.IdInzyniera).one()
assert refreshed.Imie == "New"
assert refreshed.Nazwisko == "Surname"
```

### 7.3 Testy Endpointów Sprzętu (TestSprzetEndpoints)

#### `test_create_success()`
```python
equip = create_equipment(producent="TestMic", model="TM1", kategoria="Mikrofony")
assert equip is not None
assert equip.Model == "TM1"
assert equip.Kategoria == "Mikrofony"
```

#### `test_dodaj_sprzet_get_renders_form()`
```python
resp = client.get("/sprzet/dodaj")
assert resp.status_code == 200
```

### 7.4 Testy Endpointów Utworów (TestUtworyEndpoints)

#### `test_list_renders()`
```python
resp = client.get("/utwory/")
assert resp.status_code == 200
```

#### `test_dodaj_utwor_get_renders_form()`
```python
resp = client.get("/utwory/dodaj")
assert resp.status_code == 200
```

#### `test_dodaj_utwor_post_creates_song()`
```python
artist, _, sesja = utwory_base_setup
title = "ChainSong"
song = create_song(artist, sesja, tytul=title)
assert song.IdArtysty == artist.IdArtysty
assert song.IdSesji == sesja.IdSesji
```

### 7.5 Testy Endpointów Sesji (TestSesjeEndpoints)

#### `test_create_multi_sprzet()`
```python
_, _, sesja, _ = session_with_equipment
assert sesja is not None
assert db_session.query(SprzetySesje).filter_by(IdSesji=sesja.IdSesji).count() == 2
```

Testuje: Sesja z wieloma elementami sprzętu

#### `test_list_renders()`
```python
resp = client.get("/sesje/")
assert resp.status_code == 200
```

#### `test_dodaj_sesje_get_renders_form()`
```python
resp = client.get("/sesje/dodaj")
assert resp.status_code == 200
```

#### `test_dodaj_sesje_post_creates_session()`
```python
artist = create_artist(nazwa="PostArtist")
engineer = create_engineer(imie="PostEng", nazwisko="PE")
resp = client.post(
    "/sesje/dodaj",
    data={
        "artysta": str(artist.IdArtysty),
        "inzynier": str(engineer.IdInzyniera),
        "termin_start": "2025-05-01",
        "sprzet": [],
    },
    follow_redirects=True,
)
assert resp.status_code == 200
sesja = db_session.query(Sesje).filter_by(
    IdArtysty=artist.IdArtysty,
    IdInzyniera=engineer.IdInzyniera
).first()
assert sesja is not None
assert str(sesja.TerminStart)[:10] == "2025-05-01"
assert sesja.TerminStop is None
```

Testuje:
- Tworzenie sesji bez terminu końcowego
- Konwersja daty string → datetime
- Persistence w bazie

#### `test_dodaj_sesje_post_with_termin_stop()`
```python
# Jak wyżej, ale z terminem końcowym
assert str(sesja.TerminStart)[:10] == "2025-06-01"
assert str(sesja.TerminStop)[:10] == "2025-06-10"
```

#### `test_edytuj_sesje_get_renders_form()`
```python
artist = create_artist(nazwa="EditSArtist")
engineer = create_engineer(imie="Edit", nazwisko="Eng")
sesja = create_session(artist, engineer)
resp = client.get(f"/sesje/edytuj/{sesja.IdSesji}")
assert resp.status_code == 200
```

#### `test_edytuj_sesje_post_updates_and_equipment_links()`
```python
artist = session_fixtures.create_artist(nazwa="EditSEquipArtist")
engineer = session_fixtures.create_engineer(imie="Equip", nazwisko="Editor")
eq1 = session_fixtures.create_equipment(producent="E1", model="M1", kategoria="Mikrofony")
eq2 = session_fixtures.create_equipment(producent="E2", model="M2", kategoria="Procesory")
sesja = session_fixtures.create_session(artist, engineer, sprzet_ids=[str(eq1.IdSprzetu)])

# Sesja ma 1 element sprzętu
assert session_fixtures.db_session.query(
    SprzetySesje
).filter_by(IdSesji=sesja.IdSesji).count() == 1

# Edytujemy i dodajemy drugi element
resp = session_fixtures.client.post(
    f"/sesje/edytuj/{sesja.IdSesji}",
    data={
        "artysta": str(artist.IdArtysty),
        "inzynier": str(engineer.IdInzyniera),
        "termin_start": "2025-02-02",
        "sprzet": [str(eq1.IdSprzetu), str(eq2.IdSprzetu)],
    },
    follow_redirects=True,
)

assert resp.status_code == 200
refreshed = session_fixtures.db_session.query(Sesje).filter_by(IdSesji=sesja.IdSesji).one()
assert str(refreshed.TerminStart)[:10] == "2025-02-02"

# Teraz ma 2 elementy sprzętu
assert session_fixtures.db_session.query(
    SprzetySesje
).filter_by(IdSesji=sesja.IdSesji).count() == 2
```

Testuje:
- Edycja danych sesji
- Aktualizacja linków do sprzętu
- Dodawanie/usuwanie sprzętu

#### `test_sesja_details_view_renders()`
```python
artist = create_artist(nazwa="DetA")
engineer = create_engineer(imie="Det", nazwisko="Eng")
sesja = create_session(artist, engineer)
resp = client.get(f"/sesje/{sesja.IdSesji}")
assert resp.status_code == 200
```

Testuje: Widok szczegółów sesji

#### `test_edytuj_sesje_returns_404_when_not_found()`
```python
resp = client.get("/sesje/edytuj/999999")
assert resp.status_code == 404
```

Testuje: 404 dla nieistniejącej sesji

#### `test_edytuj_sesje_post_returns_404_when_update_returns_none()`
```python
resp = client.post(
    "/sesje/edytuj/999999",
    data={"artysta": "1", "inzynier": "1", "termin_start": "2025-01-01", "sprzet": []},
    follow_redirects=False,
)
assert resp.status_code == 404
```

Testuje: 404 gdy update zwraca None

#### `test_edytuj_sesje_post_hits_updated_none_branch()`
```python
def test_edytuj_sesje_post_hits_updated_none_branch(self, monkeypatch_fixtures: MonkeyPatchFixtures):
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
    
    resp = monkeypatch_fixtures.client.post(
        f"/sesje/edytuj/{sesja.IdSesji}",
        data={
            "artysta": str(artist.IdArtysty),
            "inzynier": str(engineer.IdInzyniera),
            "termin_start": "2025-02-02",
            "sprzet": [],
        },
        follow_redirects=False,
    )
    
    assert resp.status_code == 404
```

Testuje:
- Mockowanie serwisu w blueprincie
- Obsługa None zwracanego przez serwis
- Code coverage dla gałęzi obsługi błędu

#### `test_edytuj_sesje_post_hits_service_sesja_is_none_branch()`
```python
def test_edytuj_sesje_post_hits_service_sesja_is_none_branch(
    self,
    simple_monkeypatch_fixtures: SimpleMonkeyPatchFixtures
):
    simple_monkeypatch_fixtures.monkeypatch.setattr(
        sesje_view_module,
        "get_by_id",
        lambda _model, _id_value: object()
    )
    
    resp = simple_monkeypatch_fixtures.client.post(
        "/sesje/edytuj/999999",
        data={
            "artysta": "1",
            "inzynier": "1",
            "termin_start": "2025-01-01",
            "sprzet": [],
        },
        follow_redirects=False,
    )
    
    assert resp.status_code == 404
```

Testuje:
- Mockowanie serwisu `get_by_id`
- Obsługa sytuacji gdy sesja nie zostaje znaleziona
- Code coverage dla gałęzi obsługi błędu

---

## 8. Wzorce Testowania

### 8.1 Wzorzec AAA (Arrange, Act, Assert)

```python
# ARRANGE - Przygotowanie
artist = create_artist(nazwa="TestBand")
engineer = create_engineer(imie="Test", nazwisko="Eng")

# ACT - Wykonanie
resp = client.post(f"/sesje/edytuj/{sesja.IdSesji}", data={...})

# ASSERT - Weryfikacja
assert resp.status_code == 200
refreshed = db_session.query(Sesje).filter_by(IdSesji=sesja.IdSesji).one()
assert refreshed.Nazwa == "UpdatedName"
```

### 8.2 Testowanie Relacji Bazy Danych

```python
# Many-to-Many relacja SprzetySesje
sprzety = db_session.query(SprzetySesje).filter_by(IdSesji=sesja.IdSesji).all()
assert len(sprzety) == 2

# Dostęp przez relacje
for sprzet_link in sprzety:
    assert sprzet_link.sprzet is not None
    assert sprzet_link.sprzet.Producent is not None
```

### 8.3 Testowanie HTTP

```python
# GET - pobieranie danych
resp = client.get("/artysci/")
assert resp.status_code == 200
html = resp.get_data(as_text=True)
assert "TestBand" in html

# POST - wysyłanie formularza
resp = client.post(
    "/artysci/dodaj",
    data={"nazwa": "Band", "imie": "John"},
    follow_redirects=True
)
assert resp.status_code == 200

# Redirect
resp = client.post("/artysci/dodaj", data={...}, follow_redirects=False)
assert resp.status_code in (301, 302)
assert "/artysci/" in resp.headers.get("Location", "")
```

### 8.4 Testowanie Monkeypatch

```python
def test_example(self, monkeypatch_fixtures: MonkeyPatchFixtures):
    def mock_function(arg1, arg2):
        return None
    
    monkeypatch_fixtures.monkeypatch.setattr(
        module_path,
        "function_name",
        mock_function
    )
    
    # Teraz funkcja zwróci None zamiast normalnego wyniku
```

### 8.5 Testowanie Code Coverage

Testy z suffixem `_branch` lub `_hits_` są specjalnie napisane aby osiągnąć 100% code coverage:

```python
# Test obsługi None brancha
def test_edytuj_sesje_post_hits_updated_none_branch(self, ...):
    # Mock'uje serwis aby zwrócił None
    # Testuje kod obsługi tego None
```

---

## 9. Najlepsze Praktyki w Testach

### 9.1 Nazewnictwo Testów
- Przedrostek `test_` dla każdego testu
- Opis co jest testowane: `test_create_artist_persists_data`
- Specyficzne: `test_get_all_sorted_orders_asc` vs ogólne `test_sorting`

### 9.2 Organizacja Testów
```python
class TestArtysciEndpoints:
    """Testy endpointów artystów"""
    
    def test_list_empty(self):
        """Lista artystów gdy jest pusta"""
        
    def test_create_success(self):
        """Tworzenie artysty"""
```

### 9.3 Fixtures jako Fabryki
```python
# Łatwe do konfiguracji
artist = create_artist(nazwa="Custom", imie="Jan", nazwisko="Kowalski")

# Domyślne wartości
artist = create_artist()  # nazwa="DefaultArtist"
```

### 9.4 Logika Wspólna w Setup'ach
```python
# utwory_base_setup tworzy artystę, inżyniera i sesję
artist, engineer, sesja = utwory_base_setup
# Gotowe do użycia
```

### 9.5 Wyczyszczenie Danych
- `_db_in_memory` fixture automatycznie czyszcza bazę
- Każdy test startuje z pustą bazą
- Brak konfliktów między testami

---

## 10. Problemy Znane i Rozwiązania

### 10.1 Konwersja Daty
```python
# POPRAWNIE:
termin_start_dt = datetime.strptime("2025-01-01", "%Y-%m-%d")
session_data = SessionData(..., terminstart=termin_start_dt, ...)

# NIEPOPRAWNIE:
session_data = SessionData(..., terminstart="2025-01-01", ...)  # string!
```

### 10.2 Wartości Integer dla ID
```python
# POPRAWNIE:
sprzet_ids = [int(id) for id in sprzet_ids]

# NIEPOPRAWNIE:
sprzet_ids = sprzet_ids  # mogą być stringami!
```

### 10.3 Kategoria Sprzętu
```python
# Musi być jedną z dozwolonych wartości
create_equipment(kategoria="Mikrofony")  # OK
create_equipment(kategoria="Procesory")  # OK
create_equipment(kategoria="Nieznana")   # BŁĄD!
```

---

## 11. Uruchamianie Testów

### 11.1 Wszystkie testy
```bash
pytest
```

### 11.2 Konkretny plik
```bash
pytest test_blueprints.py
pytest test_services.py -v
```

### 11.3 Konkretna klasa
```bash
pytest test_blueprints.py::TestArtysciEndpoints
```

### 11.4 Konkretny test
```bash
pytest test_blueprints.py::TestArtysciEndpoints::test_list_sorting
```

### 11.5 Z verbosem
```bash
pytest -v
pytest -vv  # Bardziej verbose
```

### 11.6 Z pokryciem kodu
```bash
pytest --cov=app --cov-report=html
```

---

## 12. Statystyka Testów

| Moduł | Liczba Testów | Typ |
|-------|---------------|-----|
| test_database.py | 2 | Inicjalizacja bazy |
| test_seed.py | 2 | Seed'owanie |
| test_services.py | 17 | Integracyjne |
| test_blueprints.py | 38+ | Funkcjonalne |
| **RAZEM** | **59+** | |

---

## 13. Zasoby

- **pytest dokumentacja:** https://docs.pytest.org/
- **Flask testowanie:** https://flask.palletsprojects.com/testing/
- **SQLAlchemy ORM:** https://docs.sqlalchemy.org/orm/
- **fixtures best practices:** https://docs.pytest.org/en/latest/fixture.html

---

## Podsumowanie

Zestaw testów zapewnia:
✅ Szybkie testowanie na bazie in-memory
✅ Izolacja testów przez automatyczne czyszczenie
✅ Factories do łatwego tworzenia danych testowych
✅ Composite fixtures do bundlowania fabryki
✅ Monkeypatch dla mockowania zależności
✅ Testy wszystkich warstw: serwisy, blueprinty, baza
✅ High code coverage dzięki testom gałęzi błędu
✅ Czytelne nazewnictwo i organizacja

