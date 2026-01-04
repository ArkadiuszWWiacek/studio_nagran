from flask import Blueprint, request, redirect, url_for, render_template
from app import database
from app.models import Sprzet

sprzet_bp = Blueprint('sprzet', __name__)


@sprzet_bp.route("/")
def sprzet_view():
    sesja = database.Session()
    try:
        sort_by = request.args.get("sort", "IdSprzetu")
        order = request.args.get("order", "asc")

        sort_columns = {
            "IdSprzetu": Sprzet.IdSprzetu,
            "Producent": Sprzet.Producent,
            "Model": Sprzet.Model,
            "Kategoria": Sprzet.Kategoria,
        }

        if sort_by not in sort_columns:
            sort_by = "IdSprzetu"

        column = sort_columns[sort_by]
        if order == "desc":
            column = column.desc()
        else:
            column = column.asc()

        sprzety = sesja.query(Sprzet).order_by(column).all()

        return render_template(
            "sprzet.html", sprzety=sprzety, sort_by=sort_by, order=order
        )
    finally:
        sesja.close()


@sprzet_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_sprzet_view():
    if request.method == "POST":
        producent = request.form.get("producent")
        model = request.form.get("model")
        kategoria = request.form.get("kategoria")
        sesja = database.Session()
        try:
            nowy_sprzet = Sprzet(Producent=producent, Model=model, Kategoria=kategoria)
            sesja.add(nowy_sprzet)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("sprzet.sprzet_view"))
    else:
        return render_template("dodaj_sprzet.html")
