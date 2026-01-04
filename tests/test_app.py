import pytest
import sys
from contextlib import contextmanager
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

sys.path.insert(0, ".")
from app import create_app
from app.models import (
    Artysci,
    Inzynierowie,
    Sprzet,
    Utwory,
    Sesje,
    SprzetySesje,
    Base,
)
from app import database


@pytest.fixture(scope="function")
def client() -> FlaskClient:
    """Fixtura klienta testowego z izolowaną bazą danych"""
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["WTF_CSRF_ENABLED"] = False
    
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionFactory = sessionmaker(bind=test_engine)
    TestSession = scoped_session(TestSessionFactory)
    
    Base.metadata.bind = test_engine
    Base.metadata.create_all(test_engine)
    
    original_session = database.Session
    original_engine = database.engine
    database.Session = TestSession
    database.engine = test_engine
    

    with test_app.test_client() as test_client:
        with test_app.app_context():
            try:
                yield test_client
            finally:
                TestSession.remove()
                Base.metadata.drop_all(test_engine)
                test_engine.dispose()
                database.Session = original_session
                database.engine = original_engine


@contextmanager
def get_session():
    session = database.Session()
    try:
        yield session
        session.commit()  # ✓ DODANE - commit zmian
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



class TestArtysci:
    """Testy widoków artystów"""

    def test_artysci_view_get(self, client: FlaskClient):
        """Test jednostkowy GET /artysci zwraca szablon"""
        # Arrange
        expected_title = "Artyści".encode('utf-8')
        
        # Act
        response = client.get("/artysci/")
        
        # Assert
        assert response.status_code == 200
        assert expected_title in response.data

    def test_dodaj_artyste_post_success(self, client: FlaskClient):
        """Test integracyjny POST /artysci/dodaj dodaje artystę"""
        # Arrange
        data = {"nazwa": "TestBand", "imie": "Jan", "nazwisko": "Kowalski"}
        
        # Act
        response = client.post("/artysci/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        
        with get_session() as session:
            artist = session.query(Artysci).filter(Artysci.Nazwa == "TestBand").first()
            assert artist is not None
            assert artist.Imie == "Jan"
            assert artist.Nazwisko == "Kowalski"


class TestInzynierowie:
    """Testy widoków inżynierów"""

    def test_inzynierowie_view_get(self, client: FlaskClient):
        """Test jednostkowy GET /inzynierowie zwraca szablon"""
        # Arrange
        expected_title = "Inżynierowie".encode('utf-8')
        
        # Act
        response = client.get("/inzynierowie/")
        
        # Assert
        assert response.status_code == 200
        assert expected_title in response.data

    def test_dodaj_inzyniera_post_success(self, client: FlaskClient):
        """Test integracyjny POST /inzynierowie/dodaj dodaje inżyniera"""
        # Arrange
        data = {"imie": "Jan", "nazwisko": "Kowalski"}
        
        # Act
        response = client.post("/inzynierowie/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        
        with get_session() as session:
            engineer = session.query(Inzynierowie).filter(
                Inzynierowie.Imie == "Jan",
                Inzynierowie.Nazwisko == "Kowalski"
            ).first()
            assert engineer is not None


class TestSprzet:
    """Testy widoków sprzętu"""

    def test_sprzet_view_get(self, client: FlaskClient):
        """Test jednostkowy GET /sprzet zwraca szablon"""
        # Arrange
        expected_title = "Sprzęt".encode('utf-8')
        
        # Act
        response = client.get("/sprzet/")
        
        # Assert
        assert response.status_code == 200
        assert expected_title in response.data

    def test_dodaj_sprzet_post_success(self, client: FlaskClient):
        """Test integracyjny POST /sprzet/dodaj dodaje sprzęt"""
        # Arrange
        data = {"producent": "TestProducer", "model": "TestModel", "kategoria": "TestCategory"}
        
        # Act
        response = client.post("/sprzet/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        
        with get_session() as session:
            equipment = session.query(Sprzet).filter(
                Sprzet.Producent == "TestProducer",
                Sprzet.Model == "TestModel"
            ).first()
            assert equipment is not None
            assert equipment.Kategoria == "TestCategory"


class TestUtwory:
    """Testy widoków utworów"""

    def test_utwory_view_get(self, client: FlaskClient):
        """Test jednostkowy GET /utwory zwraca szablon"""
        # Arrange
        expected_title = "Utwory".encode('utf-8')
        
        # Act
        response = client.get("/utwory/")
        
        # Assert
        assert response.status_code == 200
        assert expected_title in response.data

    def test_dodaj_utwor_get_shows_data(self, client: FlaskClient):
        """Test integracyjny GET /utwory/dodaj wyświetla dane z bazy"""
        # Arrange
        client.post("/artysci/dodaj", data={"nazwa": "TestArtist"})
        
        # Act
        response = client.get("/utwory/dodaj")
        
        # Assert
        assert response.status_code == 200
        assert b"TestArtist" in response.data

    def test_dodaj_utwor_post_success(self, client: FlaskClient):
        """Test integracyjny POST /utwory/dodaj z poprawnymi danymi"""
        # Arrange
        # Przygotowanie artysty i inżyniera
        client.post("/artysci/dodaj", data={"nazwa": "TestArtist2", "imie": "Jan", "nazwisko": "Kowalski"})
        client.post("/inzynierowie/dodaj", data={"imie": "Adam", "nazwisko": "Nowak"})
        
        # Pobranie ID z bazy
        with get_session() as session:
            artist = session.query(Artysci).filter(Artysci.Nazwa == "TestArtist2").first()
            engineer = session.query(Inzynierowie).filter(Inzynierowie.Imie == "Adam").first()
            artist_id = artist.IdArtysty
            engineer_id = engineer.IdInzyniera
        
        # Przygotowanie sesji
        client.post("/sesje/dodaj", data={
            "artysta": str(artist_id),
            "inzynier": str(engineer_id),
            "termin_start": "2025-01-01"
        })
        
        # Pobranie ID sesji
        with get_session() as session:
            sesja = session.query(Sesje).first()
            sesja_id = sesja.IdSesji
        
        data = {"artysta": str(artist_id), "idSesji": str(sesja_id), "tytul": "Test Song"}
        
        # Act
        response = client.post("/utwory/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        
        with get_session() as session:
            utwor = session.query(Utwory).filter(Utwory.Tytul == "Test Song").first()
            assert utwor is not None
            assert utwor.IdArtysty == artist_id
            assert utwor.IdSesji == sesja_id


class TestSesje:
    """Testy widoków sesji"""

    def test_sesje_view_sorting(self, client: FlaskClient):
        """Test jednostkowy sortowania sesji"""
        # Arrange
        expected_title = "Sesje".encode('utf-8')
        sort_params = "?sort=IdSesji&order=desc"
        
        # Act
        response = client.get(f"/sesje/{sort_params}")
        
        # Assert
        assert response.status_code == 200
        assert expected_title in response.data

    def test_dodaj_sesje_post_multiple_sprzet(self, client: FlaskClient):
        """Test integracyjny dodawania sesji z wieloma sprzętami"""
        # Arrange
        # Przygotowanie danych testowych
        client.post("/artysci/dodaj", data={"nazwa": "TestArtist3"})
        client.post("/inzynierowie/dodaj", data={"imie": "Jan", "nazwisko": "Test"})
        client.post("/sprzet/dodaj", data={"producent": "P1", "model": "M1", "kategoria": "K1"})
        client.post("/sprzet/dodaj", data={"producent": "P2", "model": "M2", "kategoria": "K2"})
        
        # Pobranie ID z bazy
        with get_session() as session:
            artist = session.query(Artysci).filter(Artysci.Nazwa == "TestArtist3").first()
            engineer = session.query(Inzynierowie).filter(
                Inzynierowie.Imie == "Jan",
                Inzynierowie.Nazwisko == "Test"
            ).first()
            sprzet_list = session.query(Sprzet).all()
            
            data = {
                "artysta": str(artist.IdArtysty),
                "inzynier": str(engineer.IdInzyniera),
                "termin_start": "2025-01-01",
                "sprzet": [str(sprzet_list[0].IdSprzetu), str(sprzet_list[1].IdSprzetu)],
            }
        
        # Act
        response = client.post("/sesje/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code == 200


class TestErrorHandling:
    """Testy obsługi błędów"""

    def test_duplicate_artist_handling(self, client: FlaskClient):
        """Test obsługi duplikatu artysty"""
        # Arrange
        data = {"nazwa": "UniqueArtist", "imie": "Jan", "nazwisko": "Kowalski"}
        client.post("/artysci/dodaj", data=data, follow_redirects=True)
        
        # Act
        response = client.post("/artysci/dodaj", data=data, follow_redirects=True)
        
        # Assert
        assert response.status_code in [200, 400, 409]

    def test_invalid_data_handling(self, client: FlaskClient):
        """Test walidacji nieprawidłowych danych"""
        # Arrange
        empty_data = {}
        
        # Act
        response = client.post("/artysci/dodaj", data=empty_data, follow_redirects=True)
        
        # Assert
        assert response.status_code in [200, 400]
