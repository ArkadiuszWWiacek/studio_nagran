# RAPORT: Statystyki użycia fixtures w testach automatycznych

**Data wygenerowania:** 26 stycznia 2026

***

## 1. Executive Summary

- **Liczba zdefiniowanych fixtures:** 17
- **Liczba jawnie wywoływanych fixtures:** 16
- **Fixtures wywoływane niejawnie:** 1 (`autouse=True`)
- **Całkowita liczba wywołań fixtures:** 93
- **Średnia liczba wywołań na fixture:** 5.81
- **Najczęściej używany fixture:** `client` (33 wywołań)
- **Najrzadziej używany fixture:** `create_equipment` (1 wywołanie)

***

## 2. Ranking fixtures według liczby wywołań

| Pozycja | Fixture | Wywołania | Typ | Scope |
|---------|---------|-----------|-----|-------|
| 1 | `client` | 33 | flask_client | function |
| 2 | `create_engineer` | 14 | factory | function |
| 3 | `create_artist` | 13 | factory | function |
| 4 | `db_session` | 13 | database | function |
| 5 | `mock_session` | 6 | mock | function ||
| 6 | `create_session` | 2 | factory | function |
| 7 | `session_fixtures` | 2 | dataclass | function |
| 8 | `mock_db_seed` | 2 | mock | function |
| 9-16 | *pozostałe* | 1 | różne | function |

### Fixture wywoływany niejawnie

- `_db_in_memory` (typ: setup, **autouse=True** - uruchamia się automatycznie przed każdym testem)

***

## 3. Analiza według typu fixtures

| Typ fixture | Liczba fixtures | Całkowite wywołania | Średnia wywołań |
|-------------|-----------------|---------------------|-----------------|
| flask_client | 1 | 33 | 33.00 |
| database | 1 | 13 | 13.00 |
| factory | 5 | 31 | 6.20 |
| mock | 2 | 8 | 4.00 |
| dataclass | 4 | 5 | 1.25 |
| composite | 2 | 2 | 1.00 |
| pytest_builtin | 1 | 1 | 1.00 |

### Kluczowe wnioski z analizy typów:

**Factory fixtures** (31 wywołań):
- `create_engineer` - 14 wywołań
- `create_artist` - 13 wywołań  
- `create_session` - 2 wywołania
- `create_equipment` - 1 wywołanie
- `create_song` - 1 wywołanie

**Mock fixtures** (8 wywołań):
- `mock_session` - 6 wywołań (w `test_unit.py`)
- `mock_db_seed` - 2 wywołania (w `test_seed.py`)

***

## 4. Analiza użycia według plików testowych

| Plik testowy | Używane fixtures | Całkowite wywołania |
|--------------|------------------|---------------------|
| `test_blueprints.py` | 12 | 78 |
| `test_services.py` | 1 | 8 |
| `test_unit.py` | 1 | 6 |
| `test_seed.py` | 1 | 2 |
| `test_database.py` | 2 | 2 |

### Szczegółowa analiza pliku `test_blueprints.py`

Ten plik dominuje w użyciu fixtures (78 z 93 wywołań = 84%):

**Najczęściej używane fixtures:**
- `client` - 32 wywołania
- `create_engineer` - 14 wywołań
- `create_artist` - 13 wywołań
- `db_session` - 5 wywołań
- `session_fixtures` - 2 wywołania

***

## 5. Szczegółowy profil wybranych fixtures

### `client` (33 wywołania) ⭐ TOP #1

**Właściwości:**
- Typ: flask_client
- Scope: function  
- Autouse: Nie
- Wykorzystanie: 35% wszystkich wywołań

**Używany w testach:**
- `test_blueprints.py` (32 testy) - testy HTTP endpoints
- `test_database.py` (1 test) - test komendy CLI

**Analiza:** Najbardziej krytyczny fixture dla testów integracyjnych. Każdy test HTTP wymaga tego fixture.

***

### `create_artist` i `create_engineer` (13-14 wywołań) ⭐ TOP #2-3

**Właściwości:**
- Typ: factory
- Pattern: Factory fixture do tworzenia danych testowych

**Typowe użycie:**
```python
def test_example(create_artist, create_engineer):
    artist = create_artist(nazwa="TestBand", imie="Jan")
    engineer = create_engineer(imie="Adam", nazwisko="Nowak")
```

**Analiza:** Kluczowe fixtures dla testów wymagających danych artystów i inżynierów. Używane głównie w testach sesji i utworów.

***

### `db_session` (13 wywołań) ⭐ TOP #4

**Właściwości:**
- Typ: database
- Używany w: `test_blueprints.py` (5x), `test_services.py` (8x)

**Zastosowanie:**
- Weryfikacja zapisów w bazie po operacjach POST
- Testy logiki biznesowej wymagające dostępu do sesji SQLAlchemy

**Przykład:**
```python
def test_edytuj_post_updates(create_artist, client, db_session):
    artist = create_artist(nazwa="Before")
    # ... operacja edycji
    refreshed = db_session.query(Artysci).filter_by(IdArtysty=artist.IdArtysty).one()
    assert refreshed.Nazwa == "After"
```

***

### `_db_in_memory` (autouse=True) 🔧

**Właściwości:**
- Typ: setup
- Autouse: TAK - uruchamia się automatycznie przed każdym testem
- Niewidoczny w parametrach testów (dlatego 0 "użyć")

**Funkcja:**
```python
@pytest.fixture(autouse=True)
def _db_in_memory():
    # Tworzy świeżą bazę SQLite in-memory
    # Podmienia globalną sesję
    # Po teście: cleanup
```

**Analiza:** Kluczowy fixture zapewniający izolację testów. Chociaż nie jest "używany" jawnie, działa dla każdego testu.

***

## 6. Rekomendacje i wnioski

### 6.1. Najczęściej używane fixtures (TOP 5)

1. `client` - 33 wywołań
2. `create_engineer` - 14 wywołań
3. `create_artist` - 13 wywołań
4. `db_session` - 13 wywołań
5. `mock_session` - 6 wywołań

✅ **Ocena:** Te fixtures są kluczowe dla testów i są intensywnie wykorzystywane. Dobra praktyka!

### 6.2. Fixtures z pojedynczym użyciem

- `create_equipment` - tylko w `test_create_success` (test_blueprints.py)
- `fixtures` - tylko w `test_utwory_artysty_renders_modal_contains_songs`
- `session_with_equipment` - tylko w `test_create_multi_sprzet`
- `utwory_base_setup` - tylko w `test_dodaj_utwor_post_creates_song`
- `create_song` - tylko w `test_dodaj_utwor_post_creates_song`
- `monkeypatch_fixtures` - tylko w `test_edytuj_sesje_post_hits_updated_none_branch`
- `simple_monkeypatch_fixtures` - tylko w `test_edytuj_sesje_post_hits_service_sesja_is_none_branch`
- `monkeypatch` - tylko w `test_init_db_cli_command_calls_init_db_and_echoes_message`

⚠️ **Uwaga:** 8 fixtures (50%) ma pojedyncze użycie. Rozważ:
- Czy można zastąpić je bezpośrednim setupem w teście?
- Czy w przyszłości będą używane szerzej?
- Czy warto utrzymywać złożone composite fixtures dla jednego testu?

### 6.3. Wykorzystanie factory fixtures

| Factory Fixture | Wywołania | Ocena |
|-----------------|-----------|-------|
| `create_engineer` | 14 | ⭐ Doskonałe |
| `create_artist` | 13 | ⭐ Doskonałe |
| `create_session` | 2 | ✅ Dobre |
| `create_equipment` | 1 | ⚠️ Rozważ inline setup |
| `create_song` | 1 | ⚠️ Rozważ inline setup |

✅ **Wnioski:** Factory fixtures `create_artist` i `create_engineer` są powszechnie używane - dobra praktyka!

### 6.4. Analiza dataclass fixtures

Projekt używa 4 dataclass fixtures do grupowania dependencies:

- `fixtures` (ArtystaFixtures) - 1 użycie
- `session_fixtures` (SesjaFixtures) - 2 użycia
- `monkeypatch_fixtures` - 1 użycie
- `simple_monkeypatch_fixtures` - 1 użycie

📊 **Analiza:** Dataclass fixtures mają niskie wykorzystanie (1-2 razy). **Rekomendacja:** Rozważ zastąpienie ich bezpośrednim użyciem podstawowych fixtures, chyba że planujesz rozszerzenie testów.

***

## 7. Podsumowanie

Projekt `studio_nagran` wykorzystuje fixtures w sposób **zorganizowany i przemyślany**:

✅ **Mocne strony:**
- Prawie wszystkie fixtures są wykorzystywane (1 nieużywany z ważnego powodu - autouse)
- Factory pattern dla `create_artist` i `create_engineer` jest intensywnie używany
- Fixture `_db_in_memory` z `autouse=True` zapewnia izolację testów
- Średnio 5.81 wywołań na fixture wskazuje na dobre ponowne użycie
- Testy HTTP dobrze wykorzystują `client` fixture (33 wywołania)

⚠️ **Obszary do rozważenia:**
- 50% fixtures ma pojedyncze użycie - czy wszystkie są potrzebne?
- Dataclass fixtures mają niską adopcję
- Composite fixtures (`session_with_equipment`, `utwory_base_setup`) użyte tylko raz

📊 **Statystyki finalne:**
- **16 fixtures** aktywnie używanych
- **93 wywołania** w sumie
- **5 plików testowych** korzysta z fixtures  
- **84% wywołań** w `test_blueprints.py` (testy integracyjne HTTP)
- **Factory fixtures** stanowią 33% wszystkich wywołań

⚡ **Efektywność:**
- TOP 4 fixtures (client, create_engineer, create_artist, db_session) = 78% wywołań
- Dobra koncentracja na kluczowych fixtures
- Minimalna liczba nieużywanych fixtures (tylko 1)

***

**Ogólna ocena:** ⭐⭐⭐⭐ (4/5) - Bardzo dobry poziom organizacji fixtures dla projektu edukacyjnego.

*Raport wygenerowany automatycznie - Projekt studio_nagran - 2026-01-26*