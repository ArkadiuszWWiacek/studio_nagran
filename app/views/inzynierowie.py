from flask import Blueprint, request, redirect, url_for, render_template
from sqlalchemy import select
from app import database
from app.models import Inzynierowie

inzynierowie_bp = Blueprint('inzynierowie', __name__)

@inzynierowie_bp.route("/")
def inzynierowie_view():
    sesja = database.Session()
    try:
        sort_by = request.args.get("sort", "IdInzyniera")
        order = request.args.get("order", "asc")

        sort_columns = {
            "IdInzyniera": Inzynierowie.IdInzyniera,
            "Imie": Inzynierowie.Imie,
            "Nazwisko": Inzynierowie.Nazwisko,
        }

        if sort_by not in sort_columns:
            sort_by = "IdInzyniera"

        column = sort_columns[sort_by]
        if order == "desc":
            column = column.desc()
        else:
            column = column.asc()

        wynik_zapytania = select(Inzynierowie).order_by(column)
        rezultat = sesja.execute(wynik_zapytania)
        inzynierowie = rezultat.scalars().all()

        return render_template(
            "inzynierowie.html", inzynierowie=inzynierowie, sort_by=sort_by, order=order
        )
    finally:
        sesja.close()


@inzynierowie_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_inzyniera_view():
    if request.method == "POST":
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")
        sesja = database.Session()
        try:
            nowy_inzynier = Inzynierowie(Imie=imie, Nazwisko=nazwisko)
            sesja.add(nowy_inzynier)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("inzynierowie.inzynierowie_view"))

    return render_template("dodaj_inzyniera.html")


@inzynierowie_bp.route("/edytuj/<int:id_inzyniera>", methods=["GET", "POST"])
def edytuj_inzyniera_view(id_inzyniera):
    sesja = database.Session()
    try:
        inzynier = (
            sesja.query(Inzynierowie)
            .filter(Inzynierowie.IdInzyniera == id_inzyniera)
            .first()
        )
        if request.method == "POST":
            inzynier.Imie = request.form.get("imie")
            inzynier.Nazwisko = request.form.get("nazwisko")
            sesja.commit()
            return redirect(url_for("inzynierowie.inzynierowie_view"))

        return render_template("edytuj_inzyniera.html", inzynier=inzynier)
    finally:
        sesja.close()
