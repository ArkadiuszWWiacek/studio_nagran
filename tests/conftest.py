import sqlite3
from datetime import datetime

import pytest
from flask.testing import FlaskClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker

from app import create_app, database
from app.models import Artysci, Inzynierowie, Sprzet, Utwory, base
from app.services import (SessionData, create_session_with_equipment,
                          get_db_session)
from tests.test_types import (ArtystaFixtures, MonkeyPatchFixtures,
                              SesjaFixtures, SimpleMonkeyPatchFixtures)


@pytest.fixture(autouse=True)
def _db_in_memory():
    """Zawsze uruchamiaj testy na świeżej bazie SQLite in-memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(_dbapi_connection, _connection_record):
        sqlite3.register_adapter(datetime, lambda val: val.isoformat())

    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    test_session = scoped_session(session_factory)

    base.metadata.create_all(engine)

    old_session = database.session
    old_engine = database.engine

    database.session = test_session
    database.engine = engine

    try:
        yield
    finally:
        test_session.remove()
        base.metadata.drop_all(engine)
        engine.dispose()
        database.session = old_session
        database.engine = old_engine


@pytest.fixture(scope="function", name="client")
def fixture_client() -> FlaskClient:
    """Fixture klienta testowego."""
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client


@pytest.fixture(scope="function", name="db_session")
def fixture_db_session():
    """Jedna ścieżka transakcyjna jak w services.py."""
    with get_db_session() as session:
        yield session


@pytest.fixture(name="create_artist")
def fixture_create_artist(client, db_session):
    """Factory do tworzenia artystów."""
    def _create(nazwa="DefaultArtist", imie=None, nazwisko=None):
        data = {"nazwa": nazwa}
        if imie:
            data["imie"] = imie
        if nazwisko:
            data["nazwisko"] = nazwisko

        client.post("/artysci/dodaj", data=data, follow_redirects=True)
        return db_session.query(Artysci).filter_by(Nazwa=nazwa).one()

    return _create


@pytest.fixture(name="create_engineer")
def fixture_create_engineer(client, db_session):
    """Factory do tworzenia inżynierów."""
    def _create(imie="DefaultEng", nazwisko="DefaultSurname"):
        client.post(
            "/inzynierowie/dodaj",
            data={"imie": imie, "nazwisko": nazwisko},
            follow_redirects=True,
        )
        return db_session.query(Inzynierowie).filter_by(
            Imie=imie, Nazwisko=nazwisko
        ).one()

    return _create


@pytest.fixture(name="create_equipment")
def fixture_create_equipment(client, db_session):
    """Factory do tworzenia sprzętu."""
    def _create(producent="DefaultProducer", model="M1", kategoria="Mikrofony"):
        client.post(
            "/sprzet/dodaj",
            data={"producent": producent, "model": model, "kategoria": kategoria},
            follow_redirects=True,
        )
        return db_session.query(Sprzet).filter_by(Producent=producent, Model=model).one()

    return _create


@pytest.fixture(name="create_session")
def fixture_create_session():
    """Factory do tworzenia sesji - używa bezpośrednio SessionData."""
    def _create(artist, engineer, termin_start="2025-01-01", sprzet_ids=None):
        if sprzet_ids is None:
            sprzet_ids = []

        sprzet_ids_int = [int(id) for id in sprzet_ids] if sprzet_ids else []

        if isinstance(termin_start, str):
            termin_start_dt = datetime.strptime(termin_start, "%Y-%m-%d")
        else:
            termin_start_dt = termin_start

        session_data = SessionData(
            idartysty=artist.IdArtysty,
            idinzyniera=engineer.IdInzyniera,
            terminstart=termin_start_dt,
            terminstop=termin_start_dt,
            sprzet_ids=sprzet_ids_int
        )

        return create_session_with_equipment(session_data)

    return _create


@pytest.fixture(name="create_song")
def fixture_create_song(client, db_session):
    """Factory do tworzenia utworów."""
    def _create(artist, sesja, tytul="DefaultSong"):
        client.post(
            "/utwory/dodaj",
            data={
                "artysta": str(artist.IdArtysty),
                "idSesji": str(sesja.IdSesji),
                "tytul": tytul,
            },
            follow_redirects=True,
        )
        return db_session.query(Utwory).filter_by(Tytul=tytul).one()

    return _create


@pytest.fixture(name="utwory_base_setup")
def fixture_utwory_base_setup(create_artist, create_engineer, create_session):
    """Tworzy artystę, inżyniera i sesję dla testów utworów."""
    artist = create_artist(nazwa="UtworArtist")
    engineer = create_engineer(imie="UtworEng", nazwisko="UE")
    sesja = create_session(artist, engineer)

    return artist, engineer, sesja


@pytest.fixture(name="session_with_equipment")
def fixture_session_with_equipment(
    create_artist,
    create_engineer,
    create_equipment,
    create_session
):
    """Tworzy sesję z dwoma elementami sprzętu."""
    artist = create_artist(nazwa="EquipArtist")
    engineer = create_engineer(imie="EquipEng", nazwisko="EE")
    eq1 = create_equipment(producent="Mic1", model="M1", kategoria="Mikrofony")
    eq2 = create_equipment(producent="Mic2", model="M2", kategoria="Procesory")

    sprzet_ids = [str(eq1.IdSprzetu), str(eq2.IdSprzetu)]
    sesja = create_session(artist, engineer, sprzet_ids=sprzet_ids)

    return artist, engineer, sesja, [eq1, eq2]


@pytest.fixture
def fixtures(# pylint: disable=too-many-arguments,too-many-positional-arguments
    create_artist, create_engineer, create_session, create_song, client, db_session
):
    """Fixture zwracający dataclass z wszystkimi potrzebnymi fixtures"""
    return ArtystaFixtures(
        create_artist=create_artist,
        create_engineer=create_engineer,
        create_session=create_session,
        create_song=create_song,
        client=client,
        db_session=db_session
    )


@pytest.fixture
def session_fixtures(# pylint: disable=too-many-arguments,too-many-positional-arguments
    create_artist, create_engineer, create_equipment, create_session, client, db_session
):
    """Fixture dla testów sesji"""
    return SesjaFixtures(
        create_artist=create_artist,
        create_engineer=create_engineer,
        create_equipment=create_equipment,
        create_session=create_session,
        client=client,
        db_session=db_session
    )


@pytest.fixture
def monkeypatch_fixtures(# pylint: disable=too-many-arguments,too-many-positional-arguments
    create_artist, create_engineer, create_session, client, monkeypatch
):
    """Fixture dla testów z monkeypatch"""
    return MonkeyPatchFixtures(
        create_artist=create_artist,
        create_engineer=create_engineer,
        create_session=create_session,
        client=client,
        monkeypatch=monkeypatch
    )


@pytest.fixture
def simple_monkeypatch_fixtures(client, monkeypatch):
    """Fixture dla prostych testów z monkeypatch"""
    return SimpleMonkeyPatchFixtures(
        client=client,
        monkeypatch=monkeypatch
    )

@pytest.fixture
def mock_db_seed(monkeypatch):
    class MockConnection:
        executescript_called = commit_called = close_called = False

        def executescript(self, sql): # pylint: disable=W0613
            self.executescript_called = True

        def commit(self):
            self.commit_called = True

        def close(self):
            self.close_called = True

    class MockFile:
        read_called = False

        def read(self):
            self.read_called = True
            return "-- seed SQL content"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb): # pylint: disable=W0613
            pass

    mock_conn = MockConnection()
    mock_file = MockFile()

    def mock_open(filename, mode=None, encoding=None): # pylint: disable=W0613
        return mock_file

    monkeypatch.setattr('sqlite3.connect', lambda db: mock_conn)
    monkeypatch.setattr('builtins.open', mock_open)

    yield mock_conn, mock_file
