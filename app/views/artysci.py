from flask import Blueprint, request, redirect, url_for, render_template
from sqlalchemy import select
from app import database
from app.models import Artysci, Utwory

artysci_bp = Blueprint("artysci", __name__)


@artysci_bp.route("/")
def artysci_view():
    sesja = database.Session()
    try:
        sort_by = request.args.get("sort", "IdArtysty")
        order = request.args.get("order", "asc")

        sort_columns = {
            "IdArtysty": Artysci.IdArtysty,
            "Nazwa": Artysci.Nazwa,
            "Imie": Artysci.Imie,
            "Nazwisko": Artysci.Nazwisko,
        }

        if sort_by not in sort_columns:
            sort_by = "IdArtysty"

        column = sort_columns[sort_by]
        if order == "desc":
            column = column.desc()
        else:
            column = column.asc()

        wynik_zapytania = select(Artysci).order_by(column)
        rezultat = sesja.execute(wynik_zapytania)
        artysci = rezultat.scalars().all()

        return render_template(
            "artysci.html", artysci=artysci, sort_by=sort_by, order=order
        )
    finally:
        sesja.close()


@artysci_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_artyste_view():
    if request.method == "POST":
        nazwa = request.form.get("nazwa")
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")
        sesja = database.Session()
        try:
            nowy_artysta = Artysci(Nazwa=nazwa, Imie=imie, Nazwisko=nazwisko)
            sesja.add(nowy_artysta)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("artysci.artysci_view"))

    return render_template("dodaj_artyste.html")


@artysci_bp.route("/edytuj/<int:id_artysty>", methods=["GET", "POST"])
def edytuj_artyste_view(id_artysty):
    sesja = database.Session()
    try:
        artysta = sesja.query(Artysci).filter(Artysci.IdArtysty == id_artysty).first()
        if request.method == "POST":
            artysta.Nazwa = request.form.get("nazwa")
            artysta.Imie = request.form.get("imie")
            artysta.Nazwisko = request.form.get("nazwisko")
            sesja.commit()
            return redirect(url_for("artysci.artysci_view"))

        return render_template("edytuj_artyste.html", artysta=artysta)
    finally:
        sesja.close()


@artysci_bp.route("/<int:id_artysty>")
def utwory_artysty_view(id_artysty):
    sesja = database.Session()
    try:
        utwory_artysty = select(Utwory).where(Utwory.IdArtysty == id_artysty)
        result = sesja.execute(utwory_artysty).scalars().all()
        return render_template("modal_utwory.html", utwory_artysty=result)
    finally:
        sesja.close()
