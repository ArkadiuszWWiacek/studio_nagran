from datetime import datetime

import pytest

from app.models import (Artysci, Inzynierowie, Sesje, Sprzet, SprzetySesje,
                        Utwory)
from app.services import (SessionData, create_record,
                          create_session_with_equipment, get_all_sorted,
                          get_by_id, get_session_details, get_sessions_sorted,
                          get_utwory_by_artist, get_utwory_sorted,
                          update_record)


class TestServices:
    """Testy integracyjne services na SQLite (:memory:)."""

    def test_get_all_sorted_empty(self):
        result = get_all_sorted(Artysci, "Nazwa", "asc")
        assert result == []

    def test_create_record_persists_artist(self, db_session):
        create_record(Artysci, Nazwa="BandA", Imie="Jan", Nazwisko="Kowalski")
        saved = db_session.query(Artysci).filter_by(Nazwa="BandA").first()
        assert saved is not None
        assert saved.Imie == "Jan"

    def test_get_all_sorted_orders(self):
        create_record(Artysci, Nazwa="B")
        create_record(Artysci, Nazwa="A")
        result = get_all_sorted(Artysci, "Nazwa", "asc")
        assert [a.Nazwa for a in result] == ["A", "B"]

    def test_get_all_sorted_orders_desc(self):
        create_record(Artysci, Nazwa="B")
        create_record(Artysci, Nazwa="A")
        result = get_all_sorted(Artysci, "Nazwa", "desc")
        assert [a.Nazwa for a in result] == ["B", "A"]

    def test_get_by_id(self, db_session):
        create_record(Artysci, Nazwa="FindMe")
        artist_id = db_session.query(Artysci).filter_by(Nazwa="FindMe").one().IdArtysty

        found = get_by_id(Artysci, artist_id)
        assert found is not None
        assert found.Nazwa == "FindMe"

    def test_update_record(self, db_session):
        create_record(Artysci, Nazwa="Before", Imie="Old")
        artist = db_session.query(Artysci).filter_by(Nazwa="Before").one()

        update_record(artist, Nazwa="After", Imie="New")

        refreshed = db_session.query(Artysci).filter_by(IdArtysty=artist.IdArtysty).one()
        assert refreshed.Nazwa == "After"
        assert refreshed.Imie == "New"

    def test_create_inzynier_persists(self, db_session):
        create_record(Inzynierowie, Imie="Adam", Nazwisko="Nowak")
        saved = db_session.query(Inzynierowie).filter_by(Imie="Adam", Nazwisko="Nowak").first()
        assert saved is not None

    def test_create_sprzet_persists(self, db_session):
        # Jeśli masz CHECK/ENUM na Kategoria, użyj dozwolonej wartości.
        create_record(Sprzet, Producent="P", Model="M", Kategoria="Mikrofony")

        saved = db_session.query(Sprzet).filter_by(Producent="P", Model="M").first()
        assert saved is not None
        assert saved.Kategoria == "Mikrofony"

    def test_get_db_session_rolls_back_on_error(self, db_session):
        before = db_session.query(Artysci).count()

        with pytest.raises(TypeError):
            create_record(Artysci, NIEISTNIEJACE_POLE="X")

        after = db_session.query(Artysci).count()
        assert after == before

    def test_get_utwory_by_artist_returns_only_matching(self,):
        a1 = create_record(Artysci, Nazwa="A1")
        a2 = create_record(Artysci, Nazwa="A2")

        eng = create_record(Inzynierowie, Imie="E", Nazwisko="X")
        sesja = create_record(
            Sesje,
            IdArtysty=a1.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None,
        )

        create_record(Utwory, IdArtysty=a1.IdArtysty, IdSesji=sesja.IdSesji, Tytul="SongA1")
        create_record(Utwory, IdArtysty=a2.IdArtysty, IdSesji=sesja.IdSesji, Tytul="SongA2")

        result = get_utwory_by_artist(a1.IdArtysty)
        assert [u.Tytul for u in result] == ["SongA1"]

    def test_get_utwory_sorted_by_artist_first_name(self):
        a1 = create_record(Artysci, Nazwa="Band1", Imie="Zen", Nazwisko="Z")
        a2 = create_record(Artysci, Nazwa="Band2", Imie="Adam", Nazwisko="A")

        eng = create_record(Inzynierowie, Imie="E", Nazwisko="X")
        sesja = create_record(
            Sesje,
            IdArtysty=a1.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None,
        )

        create_record(Utwory, IdArtysty=a1.IdArtysty, IdSesji=sesja.IdSesji, Tytul="T1")
        create_record(Utwory, IdArtysty=a2.IdArtysty, IdSesji=sesja.IdSesji, Tytul="T2")

        result = get_utwory_sorted(sortby="Imie", order="asc")
        assert [u.artysci.Imie for u in result][:2] == ["Adam", "Zen"]

    def test_get_utwory_sorted_defaults_when_unknown_sort(self):
        a = create_record(Artysci, Nazwa="Band", Imie="B", Nazwisko="B")
        eng = create_record(Inzynierowie, Imie="E", Nazwisko="X")
        sesja = create_record(
            Sesje,
            IdArtysty=a.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None,
        )

        create_record(Utwory, IdArtysty=a.IdArtysty, IdSesji=sesja.IdSesji, Tytul="S1")
        create_record(Utwory, IdArtysty=a.IdArtysty, IdSesji=sesja.IdSesji, Tytul="S2")

        result = get_utwory_sorted(sortby="NIE_MA", order="asc")
        assert len(result) == 2

    def test_get_sessions_sorted_by_artist_name(self):
        a1 = create_record(Artysci, Nazwa="Zenek")
        a2 = create_record(Artysci, Nazwa="Adam")
        eng = create_record(Inzynierowie, Imie="E", Nazwisko="X")

        create_record(
            Sesje,
            IdArtysty=a1.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None
        )
        create_record(
            Sesje,
            IdArtysty=a2.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-02",
            TerminStop=None
        )

        result = get_sessions_sorted(sortby="NazwaArtysty", order="asc")
        assert [s.artysci.Nazwa for s in result][:2] == ["Adam", "Zenek"]

    def test_get_sessions_sorted_by_engineer_last_name(self):
        artist = create_record(Artysci, Nazwa="Band")

        e1 = create_record(Inzynierowie, Imie="A", Nazwisko="Nowak")
        e2 = create_record(Inzynierowie, Imie="B", Nazwisko="Adamski")

        create_record(
            Sesje,
            IdArtysty=artist.IdArtysty,
            IdInzyniera=e1.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None
        )
        create_record(
            Sesje,
            IdArtysty=artist.IdArtysty,
            IdInzyniera=e2.IdInzyniera,
            TerminStart="2025-01-02",
            TerminStop=None
        )

        result = get_sessions_sorted(sortby="NazwiskoInzyniera", order="asc")
        assert [s.inzynierowie.Nazwisko for s in result][:2] == ["Adamski", "Nowak"]

    def test_get_session_details_loads_related(self, db_session):
        artist = create_record(Artysci, Nazwa="BandX")
        eng = create_record(Inzynierowie, Imie="Eng", Nazwisko="One")
        sesja = create_record(
            Sesje,
            IdArtysty=artist.IdArtysty,
            IdInzyniera=eng.IdInzyniera,
            TerminStart="2025-01-01",
            TerminStop=None,
        )

        create_record(Utwory, IdArtysty=artist.IdArtysty, IdSesji=sesja.IdSesji, Tytul="Hit")
        sprzet = create_record(Sprzet, Producent="P", Model="M", Kategoria="Mikrofony")

        db_session.add(SprzetySesje(IdSprzetu=sprzet.IdSprzetu, IdSesji=sesja.IdSesji))
        db_session.flush()

        details = get_session_details(sesja.IdSesji)
        assert details is not None
        assert details.artysci.Nazwa == "BandX"
        assert details.inzynierowie.Nazwisko == "One"
        assert any(u.Tytul == "Hit" for u in details.utwory)
        assert any(link.sprzet.Model == "M" for link in details.sprzety_sesje)

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
