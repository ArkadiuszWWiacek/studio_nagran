from flask import Blueprint, redirect, render_template, request, url_for, flash

from app.models import Artysci, Inzynierowie, Sesje, Sprzet, SprzetySesje
from app.services import (SessionData, create_session_with_equipment,
                          get_all_sorted, get_by_id, get_db_session,
                          get_session_details, get_sessions_sorted,
                          update_session_with_equipment, safe_date_parse)

sesje_bp = Blueprint("sesje", __name__)

@sesje_bp.route("/")
def sesje_view():
    sortby = request.args.get("sort", "IdSesji")
    order = request.args.get("order", "asc")
    sesje = get_sessions_sorted(sortby=sortby, order=order)
    return render_template("sesje.html", sesje=sesje, sort_by=sortby, order=order)

@sesje_bp.route("/<int:idsesji>")
def sesja_details_view(idsesji: int):
    sesja_details = get_session_details(idsesji)
    return render_template("modal_detale.html", sesja_details=sesja_details)

@sesje_bp.route("/dodaj", methods=["GET", "POST"])
def dodaj_sesje_view():
    form_data = {}

    if request.method == "POST":

        try:
            terminstart = safe_date_parse(request.form.get("termin_start"))
            terminstop_str = request.form.get("termin_stop", "")
            terminstop = safe_date_parse(terminstop_str) if terminstop_str.strip() else None

            idartysty = int(request.form.get("artysta"))
            idinzyniera = int(request.form.get("inzynier"))
            sprzet_ids = [int(x) for x in request.form.getlist("sprzet")]

            session_data = SessionData(idartysty=idartysty, idinzyniera=idinzyniera,
                                     terminstart=terminstart, terminstop=terminstop,
                                     sprzet_ids=sprzet_ids)
            create_session_with_equipment(session_data)
            return redirect(url_for("sesje.sesje_view"))

        except (ValueError, TypeError, IndexError) as e:
            flash(f'Nieprawidłowy format daty (użyj YYYY-MM-DD HH:MM), błąd: {str(e)}', 'error')
            form_data = {
                'artysta': request.form.get("artysta", ""),
                'inzynier': request.form.get("inzynier", ""),
                'termin_start': request.form.get("termin_start", ""),
                'termin_stop': request.form.get("termin_stop", ""),
                'sprzet': request.form.getlist("sprzet")
            }

    artysci = get_all_sorted(Artysci, "Nazwa", "asc")
    inzynierowie = get_all_sorted(Inzynierowie, "Nazwisko", "asc")
    sprzety = get_all_sorted(Sprzet, "Kategoria", "asc")
    return render_template("dodaj_sesje.html",
                           artysci=artysci,
                           inzynierowie=inzynierowie,
                           sprzety=sprzety,
                           form_data=form_data
                        )

@sesje_bp.route("/edytuj/<int:idsesji>", methods=["GET", "POST"])
def edytuj_sesje_view(idsesji: int):
    sesja = get_by_id(Sesje, idsesji)
    if sesja is None:
        return ("Not Found", 404)

    form_data = {}

    if request.method == "POST":
        try:
            terminstart_str = request.form.get('termin_start')
            terminstart = safe_date_parse(terminstart_str)

            terminstop_str = request.form.get('termin_stop')
            terminstop = safe_date_parse(terminstop_str) if terminstop_str else None

            session_data = SessionData(
                idartysty=int(request.form['artysta']),
                idinzyniera=int(request.form['inzynier']),
                terminstart=terminstart,
                terminstop=terminstop,
                sprzet_ids=[int(id) for id in request.form.getlist('sprzet')]
            )

            updated = update_session_with_equipment(idsesji, session_data)
            if updated is None:
                return ("Not Found", 404)

            return redirect(url_for("sesje.sesje_view"))

        except (ValueError, TypeError, IndexError) as e:
            flash(f'Nieprawidłowy format daty (użyj YYYY-MM-DD HH:MM), błąd: {str(e)}', 'error')
            form_data = {
                'artysta': request.form.get("artysta", ""),
                'inzynier': request.form.get("inzynier", ""),
                'termin_start': request.form.get("termin_start", ""),
                'termin_stop': request.form.get("termin_stop", ""),
                'sprzet': request.form.getlist("sprzet")
            }

    lists = {
        'artysci': get_all_sorted(Artysci, "Nazwa", "asc"),
        'inzynierowie': get_all_sorted(Inzynierowie, "Nazwisko", "asc"),
        'sprzety': get_all_sorted(Sprzet, "Kategoria", "asc")
    }

    with get_db_session() as session:
        selected_sprzet_ids = [
            row.IdSprzetu
            for row in session.query(SprzetySesje).filter_by(IdSesji=idsesji).all()
        ]

    context = {
        "sesja": sesja,
        "selected_sprzet_ids": selected_sprzet_ids,
        "form_data": form_data,
         **lists
    }
    return render_template("edytuj_sesje.html", **context)
