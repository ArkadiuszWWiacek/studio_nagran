import app.views.sesje as sesje_view_module
from app.models import Artysci, Inzynierowie, Sesje, SprzetySesje, Utwory
from tests.test_types import (ArtystaFixtures, MonkeyPatchFixtures,
                              SesjaFixtures, SimpleMonkeyPatchFixtures)


class TestArtysciEndpoints:
    def test_index_contains_expected_content(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Studio nagrań" in html

    def test_list_empty(self, client):
        response = client.get("/artysci/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Studio nagrań" in html
        assert "Artyści" in html

    def test_create_success(self, create_artist):
        artist = create_artist(nazwa="TestBand", imie="Jan", nazwisko="Kowalski")
        assert artist is not None
        assert artist.Imie == "Jan"
        assert artist.Nazwisko == "Kowalski"

    def test_list_defaults_sort_and_order(self, client):
        resp = client.get("/artysci/")
        assert resp.status_code == 200

    def test_dodaj_artyste_get_renders_form(self, client):
        resp = client.get("/artysci/dodaj")
        assert resp.status_code == 200

    def test_list_sorting(self, create_artist, client):
        create_artist(nazwa="Zenek", imie="Z")
        create_artist(nazwa="Adam", imie="A")

        response = client.get("/artysci/?sort=Nazwa&order=asc")
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert html.index("Adam") < html.index("Zenek")

    def test_edytuj_get_renders_form(self, create_artist, client):
        artist = create_artist(nazwa="BandX", imie="Jan", nazwisko="Kowalski")
        resp = client.get(f"/artysci/edytuj/{artist.IdArtysty}")

        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "BandX" in html

    def test_edytuj_post_updates_and_redirects(self, create_artist, client, db_session):
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

    def test_utwory_artysty_renders_modal(self, create_artist, client):
        artist = create_artist(nazwa="BandU")
        resp = client.get(f"/artysci/utwory/{artist.IdArtysty}")
        assert resp.status_code == 200

    def test_utwory_artysty_renders_modal_contains_songs(self, fixtures: ArtystaFixtures):
        artist = fixtures.create_artist(nazwa="BandU")
        engineer = fixtures.create_engineer(imie="EngU", nazwisko="EU")
        sesja = fixtures.create_session(artist, engineer)

        title = "BandU - HitSingle"
        fixtures.create_song(artist, sesja, tytul=title)
        assert fixtures.db_session.query(Utwory).filter_by(Tytul=title).count() == 1

        resp = fixtures.client.get(f"/artysci/utwory/{artist.IdArtysty}")
        assert resp.status_code == 200

        html = resp.get_data(as_text=True)
        assert title in html


class TestInzynierowieEndpoints:
    def test_create_success(self, create_engineer):
        eng = create_engineer(imie="TestAdam", nazwisko="TestNowak")
        assert eng is not None
        assert eng.Nazwisko == "TestNowak"

    def test_list_renders(self, client):
        response = client.get("/inzynierowie/")
        assert response.status_code == 200

    def test_list_defaults_sort_and_order(self, client):
        resp = client.get("/inzynierowie/")
        assert resp.status_code == 200

    def test_list_sorting(self, create_engineer, client):
        create_engineer(imie="Zenon", nazwisko="Z")
        create_engineer(imie="Adam", nazwisko="A")

        resp = client.get("/inzynierowie/?sort=Imie&order=asc")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert html.index("Adam") < html.index("Zenon")

    def test_dodaj_inzyniera_get_renders_form(self, client):
        resp = client.get("/inzynierowie/dodaj")
        assert resp.status_code == 200

    def test_dodaj_inzyniera_post_redirects(self, client):
        resp = client.post("/inzynierowie/dodaj", data={"imie": "R", "nazwisko": "D"})
        assert resp.status_code in (301, 302)
        assert "/inzynierowie/" in resp.headers.get("Location", "")

    def test_edytuj_get_renders_form(self, create_engineer, client):
        eng = create_engineer(imie="Jan", nazwisko="Kowalski")
        resp = client.get(f"/inzynierowie/edytuj/{eng.IdInzyniera}")

        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Jan" in html

    def test_edytuj_post_updates_and_redirects(self, create_engineer, client, db_session):
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


class TestSprzetEndpoints:
    def test_create_success(self, create_equipment):
        equip = create_equipment(producent="TestMic", model="TM1", kategoria="Mikrofony")
        assert equip is not None
        assert equip.Model == "TM1"
        assert equip.Kategoria == "Mikrofony"

    def test_dodaj_sprzet_get_renders_form(self, client):
        resp = client.get("/sprzet/dodaj")
        assert resp.status_code == 200


class TestUtworyEndpoints:
    def test_list_renders(self, client):
        resp = client.get("/utwory/")
        assert resp.status_code == 200

    def test_list_defaults_sort_and_order(self, client):
        resp = client.get("/utwory/")
        assert resp.status_code == 200

    def test_dodaj_utwor_get_renders_form(self, client):
        resp = client.get("/utwory/dodaj")
        assert resp.status_code == 200

    def test_dodaj_utwor_post_creates_song(self, utwory_base_setup, create_song):
        artist, _, sesja = utwory_base_setup
        title = "ChainSong"

        song = create_song(artist, sesja, tytul=title)

        assert song.IdArtysty == artist.IdArtysty
        assert song.IdSesji == sesja.IdSesji


class TestSesjeEndpoints:
    def test_create_multi_sprzet(self, session_with_equipment, db_session):
        _, _, sesja, _ = session_with_equipment

        assert sesja is not None
        assert db_session.query(SprzetySesje).filter_by(IdSesji=sesja.IdSesji).count() == 2

    def test_list_renders(self, client):
        resp = client.get("/sesje/")
        assert resp.status_code == 200

    def test_dodaj_sesje_get_renders_form(self, client):
        resp = client.get("/sesje/dodaj")
        assert resp.status_code == 200

    def test_dodaj_sesje_post_creates_session(
        self, create_artist, create_engineer, client, db_session
    ):
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

    def test_dodaj_sesje_post_with_termin_stop(
        self, create_artist, create_engineer, client, db_session
    ):
        artist = create_artist(nazwa="StopArtist")
        engineer = create_engineer(imie="StopEng", nazwisko="SE")

        resp = client.post(
            "/sesje/dodaj",
            data={
                "artysta": str(artist.IdArtysty),
                "inzynier": str(engineer.IdInzyniera),
                "termin_start": "2025-06-01",
                "termin_stop": "2025-06-10",
                "sprzet": [],
            },
            follow_redirects=True,
        )

        assert resp.status_code == 200

        sesja = db_session.query(Sesje).filter_by(IdArtysty=artist.IdArtysty).first()
        assert sesja is not None
        assert str(sesja.TerminStart)[:10] == "2025-06-01"
        assert str(sesja.TerminStop)[:10] == "2025-06-10"

    def test_edytuj_sesje_get_renders_form(
        self,
        create_artist,
        create_engineer,
        create_session,
        client
    ):
        artist = create_artist(nazwa="EditSArtist")
        engineer = create_engineer(imie="Edit", nazwisko="Eng")
        sesja = create_session(artist, engineer)

        resp = client.get(f"/sesje/edytuj/{sesja.IdSesji}")
        assert resp.status_code == 200

    def test_edytuj_sesje_post_updates_and_equipment_links(self, session_fixtures: SesjaFixtures):
        artist = session_fixtures.create_artist(nazwa="EditSEquipArtist")
        engineer = session_fixtures.create_engineer(imie="Equip", nazwisko="Editor")
        eq1 = session_fixtures.create_equipment(producent="E1", model="M1", kategoria="Mikrofony")
        eq2 = session_fixtures.create_equipment(producent="E2", model="M2", kategoria="Procesory")

        sesja = session_fixtures.create_session(artist, engineer, sprzet_ids=[str(eq1.IdSprzetu)])
        assert session_fixtures.db_session.query(
            SprzetySesje
        ).filter_by(IdSesji=sesja.IdSesji).count() == 1

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
        assert session_fixtures.db_session.query(
            SprzetySesje
        ).filter_by(IdSesji=sesja.IdSesji).count() == 2

    def test_sesja_details_view_renders(
        self,
        create_artist,
        create_engineer,
        create_session,
        client
    ):
        artist = create_artist(nazwa="DetA")
        engineer = create_engineer(imie="Det", nazwisko="Eng")
        sesja = create_session(artist, engineer)

        resp = client.get(f"/sesje/{sesja.IdSesji}")
        assert resp.status_code == 200

    def test_edytuj_sesje_returns_404_when_not_found(self, client):
        resp = client.get("/sesje/edytuj/999999")
        assert resp.status_code == 404

    def test_edytuj_sesje_post_returns_404_when_update_returns_none(self, client):
        resp = client.post(
            "/sesje/edytuj/999999",
            data={"artysta": "1", "inzynier": "1", "termin_start": "2025-01-01", "sprzet": []},
            follow_redirects=False,
        )
        assert resp.status_code == 404

    def test_edytuj_sesje_post_hits_updated_none_branch(
        self,
        monkeypatch_fixtures: MonkeyPatchFixtures
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
