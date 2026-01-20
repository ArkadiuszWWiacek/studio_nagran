from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Inzynierowie
from app.services import (create_record, get_all_sorted, get_by_id,
                          update_record)

inzynierowie_bp = Blueprint("inzynierowie", __name__)


@inzynierowie_bp.route("/")
def inzynierowie_view():
    sortby = request.args.get("sort", "IdInzyniera")
    order = request.args.get("order", "asc")

    inzynierowie = get_all_sorted(Inzynierowie, sortby, order)
    context = {"inzynierowie": inzynierowie, "sortby": sortby, "order": order}
    return render_template("inzynierowie.html", **context)


@inzynierowie_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_inzyniera_view():
    if request.method == "POST":
        create_record(
            Inzynierowie,
            Imie=request.form.get("imie"),
            Nazwisko=request.form.get("nazwisko"),
        )
        return redirect(url_for("inzynierowie.inzynierowie_view"))

    return render_template("dodaj_inzyniera.html")


@inzynierowie_bp.route("/edytuj/<int:id_inzyniera>", methods=["GET", "POST"])
def edytuj_inzyniera_view(id_inzyniera: int):
    inzynier = get_by_id(Inzynierowie, id_inzyniera)

    if request.method == "POST":
        update_record(
            inzynier,
            Imie=request.form.get("imie"),
            Nazwisko=request.form.get("nazwisko"),
        )
        return redirect(url_for("inzynierowie.inzynierowie_view"))

    return render_template("edytuj_inzyniera.html", inzynier=inzynier)
