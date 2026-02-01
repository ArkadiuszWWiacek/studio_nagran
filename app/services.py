from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app import database
from app.models import Artysci, Inzynierowie, Sesje, SprzetySesje, Utwory


@dataclass
class SessionData:
    idartysty: int
    idinzyniera: int
    terminstart: dt
    terminstop: dt
    sprzet_ids: list[int]

@contextmanager
def get_db_session():
    session = database.session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_all_sorted(model_class, sort_by=None, order='asc'):
    with get_db_session() as session:
        stmt = select(model_class)
        if sort_by:
            col = getattr(model_class, sort_by)
            if order == 'desc':
                stmt = stmt.order_by(col.desc())
            else:
                stmt = stmt.order_by(col)
        return session.execute(stmt).scalars().all()

def create_record(model_class, **kwargs):
    with get_db_session() as session:
        instance = model_class(**kwargs)
        session.add(instance)
        session.flush()
        return instance

def get_by_id(model_class, id_value):
    pk_name = list(model_class.__table__.primary_key.columns)[0].name
    with get_db_session() as session:
        return session.query(model_class).filter(getattr(model_class, pk_name) == id_value).first()

def update_record(instance, **kwargs):
    for attr, value in kwargs.items():
        setattr(instance, attr, value)
    with get_db_session() as session:
        session.merge(instance)

def get_utwory_by_artist(id_artysty: int):
    with get_db_session() as session:
        stmt = select(Utwory).where(Utwory.IdArtysty == id_artysty)
        return session.execute(stmt).scalars().all()

def get_utwory_sorted(sortby: str = "IdUtworu", order: str = "asc"):
    with get_db_session() as session:
        stmt = (
            select(Utwory)
            .options(joinedload(Utwory.artysci))
            .options(joinedload(Utwory.sesje))
        )

        mapping = {
            "IdUtworu": Utwory.IdUtworu,
            "Tytul": Utwory.Tytul,
            "Imie": Artysci.Imie,
            "Nazwisko": Artysci.Nazwisko,
        }

        col = mapping.get(sortby, Utwory.IdUtworu)
        if sortby in ("Imie", "Nazwisko"):
            stmt = stmt.join(Artysci)

        stmt = stmt.order_by(col.desc() if order == "desc" else col.asc())
        return session.execute(stmt).scalars().all()


def get_sessions_sorted(sortby: str = "IdSesji", order: str = "asc"):
    with get_db_session() as session:
        stmt = (
            select(Sesje)
            .options(joinedload(Sesje.artysci))
            .options(joinedload(Sesje.inzynierowie))
        )

        mapping = {
            "IdSesji": Sesje.IdSesji,
            "NazwaArtysty": Artysci.Nazwa,
            "ImieArtysty": Artysci.Imie,
            "NazwiskoArtysty": Artysci.Nazwisko,
            "ImieInzyniera": Inzynierowie.Imie,
            "NazwiskoInzyniera": Inzynierowie.Nazwisko,
        }

        col = mapping.get(sortby, Sesje.IdSesji)
        if sortby in ("NazwaArtysty", "ImieArtysty", "NazwiskoArtysty"):
            stmt = stmt.join(Artysci)
        if sortby in ("ImieInzyniera", "NazwiskoInzyniera"):
            stmt = stmt.join(Inzynierowie)

        stmt = stmt.order_by(col.desc() if order == "desc" else col.asc())
        return session.execute(stmt).scalars().all()


def get_session_details(idsesji: int):
    with get_db_session() as session:
        stmt = (
            select(Sesje)
            .options(joinedload(Sesje.artysci))
            .options(joinedload(Sesje.inzynierowie))
            .options(joinedload(Sesje.utwory))
            .options(joinedload(Sesje.sprzety_sesje).joinedload(SprzetySesje.sprzet))
            .where(Sesje.IdSesji == idsesji)
        )
        return session.execute(stmt).scalars().first()

def create_session_with_equipment(session_data: SessionData):
    with get_db_session() as session:
        nowa = Sesje(
            IdArtysty=session_data.idartysty,
            IdInzyniera=session_data.idinzyniera,
            TerminStart=session_data.terminstart,
            TerminStop=session_data.terminstop,
        )
        session.add(nowa)
        session.flush()

        for idsprzetu in session_data.sprzet_ids:
            session.add(SprzetySesje(IdSprzetu=idsprzetu, IdSesji=nowa.IdSesji))

        session.flush()
        return nowa

def update_session_with_equipment(idsesji: int, session_data: SessionData):
    with get_db_session() as session:
        sesja = session.query(Sesje).filter_by(IdSesji=idsesji).first()
        if sesja is None:
            return None

        sesja.IdArtysty = session_data.idartysty
        sesja.IdInzyniera = session_data.idinzyniera
        sesja.TerminStart = session_data.terminstart
        sesja.TerminStop = session_data.terminstop

        session.query(SprzetySesje).filter_by(IdSesji=idsesji).delete()
        for idsprzetu in session_data.sprzet_ids:
            session.add(SprzetySesje(IdSprzetu=idsprzetu, IdSesji=idsesji))

        session.flush()
        return sesja

def get_sesje_for_utwor_form():
    with get_db_session() as session:
        stmt = (
            select(
                Sesje.IdSesji.label("IdSesji"),
                Sesje.IdArtysty.label("IdArtysty"),
                Artysci.Nazwa.label("NazwaArtysty"),
            )
            .join(Artysci, Artysci.IdArtysty == Sesje.IdArtysty)
            .order_by(Sesje.IdSesji.asc())
        )

        rows = session.execute(stmt).all()

        return [
            {
                "IdSesji": r.IdSesji,
                "IdArtysty": r.IdArtysty,
                "NazwaArtysty": r.NazwaArtysty,
            }
            for r in rows
        ]

def get_selected_sprzet_ids(id_sesji):
    with get_db_session() as session: 
        selected_sprzet_ids = [
                row.IdSprzetu
                for row in session.query(SprzetySesje).filter_by(IdSesji=id_sesji).all()
            ]
        return selected_sprzet_ids

def safe_date_parse(date_str):
    date_str = (date_str or '').strip()
    if not date_str:
        raise ValueError("Pusta data")

    date_str = date_str.replace('T', ' ')

    date_part = date_str.split()[0].split('T')[0]
    if len(date_part) != 10 or date_part.count('-') != 2:
        raise ValueError("Zly format daty")

    try:
        return dt.strptime(date_str, '%Y-%m-%d %H:%M')
    except ValueError as exc:
        raise ValueError("Zly format daty") from exc
