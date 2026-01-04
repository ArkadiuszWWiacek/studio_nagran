from flask import Blueprint, request, redirect, url_for, render_template
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app import database
from app.models import Sesje, Artysci, Inzynierowie, Sprzet, SprzetySesje

sesje_bp = Blueprint('sesje', __name__)


@sesje_bp.route("/")
def sesje_view():
    sesja = database.Session()
    try:
        sort_by = request.args.get("sort", "IdSesji")
        order = request.args.get("order", "asc")

        if sort_by in ["NazwaArtysty", "ImieArtysty", "NazwiskoArtysty"]:
            if sort_by == "NazwaArtysty":
                column = Artysci.Nazwa
            elif sort_by == "ImieArtysty":
                column = Artysci.Imie
            else:
                column = Artysci.Nazwisko

            if order == "desc":
                column = column.desc()
            else:
                column = column.asc()

            sesje_list = (
                sesja.query(Sesje)
                .join(Artysci)
                .options(joinedload(Sesje.artysci))
                .options(joinedload(Sesje.inzynierowie))
                .order_by(column)
                .all()
            )
        elif sort_by in ["ImieInzyniera", "NazwiskoInzyniera"]:
            if sort_by == "ImieInzyniera":
                column = Inzynierowie.Imie
            else:
                column = Inzynierowie.Nazwisko

            if order == "desc":
                column = column.desc()
            else:
                column = column.asc()

            sesje_list = (
                sesja.query(Sesje)
                .join(Inzynierowie)
                .options(joinedload(Sesje.artysci))
                .options(joinedload(Sesje.inzynierowie))
                .order_by(column)
                .all()
            )
        else:
            sort_columns = {"IdSesji": Sesje.IdSesji}

            if sort_by not in sort_columns:
                sort_by = "IdSesji"

            column = sort_columns[sort_by]
            if order == "desc":
                column = column.desc()
            else:
                column = column.asc()

            sesje_list = (
                sesja.query(Sesje)
                .options(joinedload(Sesje.artysci))
                .options(joinedload(Sesje.inzynierowie))
                .order_by(column)
                .all()
            )

        return render_template(
            "sesje.html", sesje=sesje_list, sort_by=sort_by, order=order
        )
    finally:
        sesja.close()


@sesje_bp.route("/<int:IdSesji>")
def sesja_details_view(IdSesji):
    sesja = database.Session()
    try:
        sesja_details = (
            select(Sesje)
            .options(joinedload(Sesje.artysci))
            .options(joinedload(Sesje.inzynierowie))
            .options(joinedload(Sesje.utwory))
            .options(joinedload(Sesje.sprzety_sesje).joinedload(SprzetySesje.sprzet))
            .where(Sesje.IdSesji == IdSesji)
        )
        wynik_zapytania = sesja.execute(sesja_details)
        rezultat = wynik_zapytania.scalars().first()
        return render_template("modal_detale.html", sesja_details=rezultat)
    finally:
        sesja.close()


@sesje_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_sesje_view():
    sesja = database.Session()
    if request.method == "POST":
        id_artysty = request.form.get("artysta")
        id_inzyniera = request.form.get("inzynier")
        termin_start = request.form.get("termin_start")
        termin_stop = request.form.get("termin_stop")
        if termin_stop == "" or not termin_stop:
            termin_stop = None
        wybrane_sprzety_ids = request.form.getlist("sprzet")
        try:
            nowa_sesja = Sesje(
                IdArtysty=id_artysty,
                IdInzyniera=id_inzyniera,
                TerminStart=termin_start,
                TerminStop=termin_stop,
            )
            sesja.add(nowa_sesja)
            sesja.flush()
            for id_sprzetu in wybrane_sprzety_ids:
                powiazanie = SprzetySesje(
                    IdSprzetu=int(id_sprzetu), IdSesji=nowa_sesja.IdSesji
                )
                sesja.add(powiazanie)
            sesja.commit()
        except Exception as e:
            sesja.rollback()
            print(f"Błąd podczas dodawania sesji: {e}")
        finally:
            sesja.close()
        return redirect(url_for("sesje.sesje_view"))
    else:
        try:
            artysci = sesja.query(Artysci).order_by(Artysci.Nazwa).all()
            inzynierowie = (
                sesja.query(Inzynierowie).order_by(Inzynierowie.Nazwisko).all()
            )
            sprzety = sesja.query(Sprzet).order_by(Sprzet.Kategoria, Sprzet.Model).all()
            return render_template(
                "dodaj_sesje.html",
                artysci=artysci,
                inzynierowie=inzynierowie,
                sprzety=sprzety,
            )
        finally:
            sesja.close()
