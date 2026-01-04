import pytest
import sys
from unittest.mock import patch, MagicMock, call
from flask.testing import FlaskClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Importuj aplikację - ZMIEŃ NA NAZWĘ SWEGO PLIKU
sys.path.insert(0, ".")
from studio_nagran_refactored import (
    app,
    Artysci,
    Inzynierowie,
    Sprzet,
    Utwory,
    Sesje,
    SprzetySesje,
    Base,
    SESSION,
)  # Zmień 'app' na nazwę pliku


@pytest.fixture
def client() -> FlaskClient:
    """Fixture dla Flask test client z bazą w pamięci"""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Utwórz bazę w pamięci i zainicjuj tabele
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    # Patch SESSION globalny
    with patch("app.SESSION", Session):
        with app.test_client() as client:
            yield client


class TestArtysciViews:
    """Testy widoków artystów"""

    def test_artysci_view_get(self, client: FlaskClient):
        """Test GET /artysci zwraca szablon z pustą listą"""
        response = client.get("/artysci")
        assert response.status_code == 200
        assert b"artysci.html" in response.data

    def test_dodaj_artyste_post_success(self, client: FlaskClient):
        """Test POST /artysci/dodaj dodaje artystę"""
        data = {"nazwa": "TestBand", "imie": "Jan", "nazwisko": "Kowalski"}
        response = client.post("/artysci/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"TestBand" in response.data

    def test_dodaj_artyste_empty_data(self, client: FlaskClient):
        """Test POST z pustymi danymi"""
        data = {"nazwa": "", "imie": "", "nazwisko": ""}
        response = client.post("/artysci/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"artysci.html" in response.data  # Przekierowanie mimo pustych danych


class TestUtworyViews:
    """Testy widoków utworów"""

    def test_utwory_view_get(self, client: FlaskClient):
        """Test GET /utwory zwraca szablon"""
        response = client.get("/utwory")
        assert response.status_code == 200
        assert b"utwory.html" in response.data

    def test_dodaj_utwor_get_lists(self, client: FlaskClient):
        """Test GET /utwory/dodaj zwraca listy artystów i sesji"""
        # Najpierw dodaj dane testowe
        with patch("app.SESSION") as mock_session:
            mock_ses = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_ses
            mock_ses.query.return_value.order_by.return_value.all.return_value = [
                Artysci(IdArtysty=1, Nazwa="TestArtist"),
                Sesje(IdSesji=1),
            ]
            response = client.get("/utwory/dodaj")
            assert response.status_code == 200
            assert b"dodaj_utwor.html" in response.data

    @patch("app.sesja.commit")
    @patch("app.sesja.add")
    def test_dodaj_utwor_post_success(self, mock_add, mock_commit, client: FlaskClient):
        """Test POST /utwory/dodaj z poprawnymi danymi"""
        data = {"artysta": "1", "idSesji": "1", "tytul": "Test Song"}
        response = client.post("/utwory/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"utwory.html" in response.data
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    @patch("app.sesja.commit", side_effect=Exception("DB Error"))
    def test_dodaj_utwor_integrity_error(self, mock_commit, client: FlaskClient):
        """Test obsługi błędu IntegrityError"""
        data = {"artysta": "999", "idSesji": "999", "tytul": "Invalid"}
        response = client.post("/utwory/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200  # Nadal przekierowuje mimo błędu


class TestSesjeViews:
    """Testy widoków sesji"""

    def test_sesje_view_sorting(self, client: FlaskClient):
        """Test sortowania sesji"""
        response = client.get("/sesje?sort=IdSesji&order=desc")
        assert response.status_code == 200
        assert b"sesje.html" in response.data

    def test_dodaj_sesje_post_multiple_sprzet(self, client: FlaskClient):
        """Test dodawania sesji z wieloma sprzętami"""
        data = {
            "artysta": "1",
            "inzynier": "1",
            "termin_start": "2025-01-01",
            "sprzet": ["1", "2"],  # Wiele sprzętów
        }
        response = client.post("/sesje/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"sesje.html" in response.data


class TestErrorHandling:
    """Testy obsługi błędów"""

    @patch("app.sesja.commit", side_effect=Exception("Test Error"))
    def test_global_error_handling(self, mock_commit, client: FlaskClient):
        """Test ogólnej obsługi błędów"""
        data = {"nazwa": "Test", "imie": "Jan", "nazwisko": "Kowalski"}
        response = client.post("/artysci/dodaj", data=data, follow_redirects=True)
        assert response.status_code == 200  # Przekierowanie mimo błędu
