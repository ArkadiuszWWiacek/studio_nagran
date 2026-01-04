from flask import Blueprint, request, redirect, url_for, render_template
from sqlalchemy.orm import joinedload
from app import database
from app.models import Utwory, Artysci, Sesje

utwory_bp = Blueprint('utwory', __name__)


@utwory_bp.route("/")
def utwory_view():
    sesja = database.Session()
    try:
        sort_by = request.args.get("sort", "IdUtworu")
        order = request.args.get("order", "asc")

        if sort_by in ["Imie", "Nazwisko"]:
            if sort_by == "Imie":
                column = Artysci.Imie
            else:
                column = Artysci.Nazwisko

            if order == "desc":
                column = column.desc()
            else:
                column = column.asc()

            utwory = (
                sesja.query(Utwory)
                .join(Artysci)
                .options(joinedload(Utwory.artysci))
                .options(joinedload(Utwory.sesje))
                .order_by(column)
                .all()
            )
        else:
            sort_columns = {"IdUtworu": Utwory.IdUtworu, "Tytul": Utwory.Tytul}

            if sort_by not in sort_columns:
                sort_by = "IdUtworu"

            column = sort_columns[sort_by]
            if order == "desc":
                column = column.desc()
            else:
                column = column.asc()

            utwory = (
                sesja.query(Utwory)
                .options(joinedload(Utwory.artysci))
                .options(joinedload(Utwory.sesje))
                .order_by(column)
                .all()
            )

        return render_template(
            "utwory.html", utwory=utwory, sort_by=sort_by, order=order
        )
    finally:
        sesja.close()


@utwory_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_utwor_view():
    sesja = database.Session()
    if request.method == "POST":
        artysta = request.form.get("artysta")
        idSesji = request.form.get("idSesji")
        tytul = request.form.get("tytul")
        try:
            nowy_utwor = Utwory(
                IdArtysty=int(artysta), IdSesji=int(idSesji), Tytul=tytul
            )
            print(nowy_utwor)
            sesja.add(nowy_utwor)
            sesja.commit()
        except Exception as e:
            sesja.rollback()
            print(f"Błąd podczas dodawania utworu: {e}")
        finally:
            sesja.close()
        return redirect(url_for("utwory.utwory_view"))
    else:
        try:
            artysci = sesja.query(Artysci).order_by(Artysci.Nazwa).all()
            sesje = sesja.query(Sesje).order_by(Sesje.IdSesji).all()
            return render_template("dodaj_utwor.html", artysci=artysci, sesje=sesje)
        finally:
            sesja.close()
