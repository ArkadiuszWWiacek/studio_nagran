from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Sprzet
from app.services import create_record, get_all_sorted

sprzet_bp = Blueprint("sprzet", __name__)


@sprzet_bp.route("/")
def sprzet_view():
    sortby = request.args.get("sort", "IdSprzetu")
    order = request.args.get("order", "asc")

    sprzety = get_all_sorted(Sprzet, sortby, order)
    return render_template("sprzet.html", sprzety=sprzety, sort_by=sortby, order=order)


@sprzet_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_sprzet_view():
    if request.method == "POST":
        create_record(
            Sprzet,
            Producent=request.form.get("producent"),
            Model=request.form.get("model"),
            Kategoria=request.form.get("kategoria"),
        )
        return redirect(url_for("sprzet.sprzet_view"))

    return render_template("dodaj_sprzet.html")
