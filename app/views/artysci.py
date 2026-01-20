from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Artysci
from app.services import (create_record, get_all_sorted, get_by_id,
                          get_utwory_by_artist, update_record)

artysci_bp = Blueprint("artysci", __name__)


@artysci_bp.route("/")
def artysci_view():
    sortby = request.args.get("sort", "IdArtysty")
    order = request.args.get("order", "asc")

    artysci = get_all_sorted(Artysci, sortby, order)

    return render_template("artysci.html", artysci=artysci, sort_by=sortby, order=order)


@artysci_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_artyste_view():
    if request.method == "POST":
        create_record(
            Artysci,
            Nazwa=request.form.get("nazwa"),
            Imie=request.form.get("imie"),
            Nazwisko=request.form.get("nazwisko"),
        )
        return redirect(url_for("artysci.artysci_view"))

    return render_template("dodaj_artyste.html")


@artysci_bp.route("/edytuj/<int:id_artysty>", methods=["GET", "POST"])
def edytuj_artyste_view(id_artysty: int):
    artysta = get_by_id(Artysci, id_artysty)

    if request.method == "POST":
        update_record(
            artysta,
            Nazwa=request.form.get("nazwa"),
            Imie=request.form.get("imie"),
            Nazwisko=request.form.get("nazwisko"),
        )
        return redirect(url_for("artysci.artysci_view"))

    return render_template("edytuj_artyste.html", artysta=artysta)


@artysci_bp.route("/utwory/<int:id_artysty>")
def utwory_artysty_view(id_artysty: int):
    utwory = get_utwory_by_artist(id_artysty)
    return render_template("modal_utwory.html", utwory_artysty=utwory)
