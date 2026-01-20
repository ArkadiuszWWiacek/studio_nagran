from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Artysci, Utwory
from app.services import (create_record, get_all_sorted,
                          get_sesje_for_utwor_form, get_utwory_sorted)

utwory_bp = Blueprint("utwory", __name__)


@utwory_bp.route("/")
def utwory_view():
    sortby = request.args.get("sort", "IdUtworu")
    order = request.args.get("order", "asc")

    utwory = get_utwory_sorted(sortby=sortby, order=order)

    return render_template("utwory.html", utwory=utwory, sort_by=sortby, order=order)


@utwory_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_utwor_view():
    if request.method == "POST":
        create_record(
            Utwory,
            IdArtysty=int(request.form.get("artysta")),
            IdSesji=int(request.form.get("idSesji")),
            Tytul=request.form.get("tytul"),
        )
        return redirect(url_for("utwory.utwory_view"))

    artysci = get_all_sorted(Artysci, "Nazwa", "asc")
    sesje = get_sesje_for_utwor_form()
    return render_template("dodaj_utwor.html", artysci=artysci, sesje=sesje)
