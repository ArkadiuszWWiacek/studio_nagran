from flask import Flask, request, redirect, url_for, render_template
from pprint import pprint
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    joinedload,
    contains_eager,
)

engine = create_engine("sqlite:///studio_nagran_01.db", echo=True, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Artysci(Base):
    __tablename__ = "artysci"
    IdArtysty = Column(Integer, primary_key=True)
    Nazwa = Column(String)
    Imie = Column(String)
    Nazwisko = Column(String)
    sesje = relationship(
        "Sesje", back_populates="artysci", cascade="all, delete-orphan"
    )
    utwory = relationship(
        "Utwory", back_populates="artysci", cascade="all, delete-orphan"
    )


class Inzynierowie(Base):
    __tablename__ = "inzynierowie"
    IdInzyniera = Column(Integer, primary_key=True)
    Imie = Column(String)
    Nazwisko = Column(String)
    sesje = relationship(
        "Sesje", back_populates="inzynierowie", cascade="all, delete-orphan"
    )


class Sprzet(Base):
    __tablename__ = "sprzet"
    IdSprzetu = Column(Integer, primary_key=True)
    Producent = Column(String)
    Model = Column(String)
    Kategoria = Column(String)
    sprzety_sesje = relationship(
        "SprzetySesje", back_populates="sprzet", cascade="all, delete-orphan"
    )


class Utwory(Base):
    __tablename__ = "utwory"
    IdUtworu = Column(Integer, primary_key=True)
    IdArtysty = Column(Integer, ForeignKey("artysci.IdArtysty", ondelete="CASCADE"))
    IdSesji = Column(Integer, ForeignKey("sesje.IdSesji", ondelete="CASCADE"))
    Tytul = Column(String)
    artysci = relationship("Artysci", back_populates="utwory")
    sesje = relationship("Sesje", back_populates="utwory")


class Sesje(Base):
    __tablename__ = "sesje"
    IdSesji = Column(Integer, primary_key=True)
    IdArtysty = Column(Integer, ForeignKey("artysci.IdArtysty", ondelete="CASCADE"))
    IdInzyniera = Column(
        Integer, ForeignKey("inzynierowie.IdInzyniera", ondelete="CASCADE")
    )
    TerminStart = Column(String)
    TerminStop = Column(String)
    artysci = relationship("Artysci", back_populates="sesje")
    inzynierowie = relationship("Inzynierowie", back_populates="sesje")
    utwory = relationship("Utwory", back_populates="sesje")
    sprzety_sesje = relationship("SprzetySesje", back_populates="sesje")


class SprzetySesje(Base):
    __tablename__ = "sprzety_sesje"
    IdSprzetu = Column(
        Integer, ForeignKey("sprzet.IdSprzetu", ondelete="CASCADE"), primary_key=True
    )
    IdSesji = Column(
        Integer, ForeignKey("sesje.IdSesji", ondelete="CASCADE"), primary_key=True
    )
    sprzet = relationship("Sprzet", back_populates="sprzety_sesje")
    sesje = relationship("Sesje", back_populates="sprzety_sesje")


def init_db():
    Base.metadata.create_all(bind=engine)
    sesja = Session()
    try:
        if sesja.query(Artysci).first() is not None:
            return
    finally:
        sesja.close()


app = Flask(__name__)


@app.route("/")
def index():
    init_db()
    return render_template("index.html")


@app.route("/artysci")
def artysci_view():
    sesja = Session()
    try:
        # Pobierz parametr sortowania z URL
        sort_by = request.args.get("sort", "IdArtysty")
        order = request.args.get("order", "asc")

        # Mapowanie nazw kolumn
        sort_columns = {
            "IdArtysty": Artysci.IdArtysty,
            "Nazwa": Artysci.Nazwa,
            "Imie": Artysci.Imie,
            "Nazwisko": Artysci.Nazwisko,
        }

        # Sprawdź czy kolumna istnieje
        if sort_by not in sort_columns:
            sort_by = "IdArtysty"

        # Zastosuj sortowanie
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


@app.route("/artysci/dodaj", methods=["GET", "POST"])
def dodaj_artyste_view():
    if request.method == "POST":
        nazwa = request.form.get("nazwa")
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")
        sesja = Session()
        try:
            nowy_artysta = Artysci(Nazwa=nazwa, Imie=imie, Nazwisko=nazwisko)
            sesja.add(nowy_artysta)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("artysci_view"))
    else:
        return render_template("dodaj_artyste.html")


@app.route("/artysci/edytuj/<int:IdArtysty>", methods=["GET", "POST"])
def edytuj_artyste_view(IdArtysty):
    sesja = Session()
    try:
        artysta = sesja.query(Artysci).filter(Artysci.IdArtysty == IdArtysty).first()
        if request.method == "POST":
            artysta.Nazwa = request.form.get("nazwa")
            artysta.Imie = request.form.get("imie")
            artysta.Nazwisko = request.form.get("nazwisko")
            sesja.commit()
            return redirect(url_for("artysci_view"))
        else:
            return render_template("edytuj_artyste.html", artysta=artysta)
    finally:
        sesja.close()


@app.route("/artysci/<int:IdArtysty>")
def utwory_artysty_view(IdArtysty):
    sesja = Session()
    try:
        utwory_artysty = select(Utwory).where(Utwory.IdArtysty == IdArtysty)
        result = sesja.execute(utwory_artysty).scalars().all()
        return render_template("modal_utwory.html", utwory_artysty=result)
    finally:
        sesja.close()


@app.route("/inzynierowie")
def inzynierowie_view():
    sesja = Session()
    try:
        # Pobierz parametr sortowania z URL
        sort_by = request.args.get("sort", "IdInzyniera")
        order = request.args.get("order", "asc")

        # Mapowanie nazw kolumn
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


@app.route("/inzynierowie/dodaj", methods=["GET", "POST"])
def dodaj_inzyniera_view():
    if request.method == "POST":
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")
        sesja = Session()
        try:
            nowy_inzynier = Inzynierowie(Imie=imie, Nazwisko=nazwisko)
            sesja.add(nowy_inzynier)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("inzynierowie_view"))
    else:
        return render_template("dodaj_inzyniera.html")


@app.route("/inzynierowie/edytuj/<int:IdInzyniera>", methods=["GET", "POST"])
def edytuj_inzyniera_view(IdInzyniera):
    sesja = Session()
    try:
        inzynier = (
            sesja.query(Inzynierowie)
            .filter(Inzynierowie.IdInzyniera == IdInzyniera)
            .first()
        )
        if request.method == "POST":
            inzynier.Imie = request.form.get("imie")
            inzynier.Nazwisko = request.form.get("nazwisko")
            sesja.commit()
            return redirect(url_for("inzynierowie_view"))
        else:
            return render_template("edytuj_inzyniera.html", inzynier=inzynier)
    finally:
        sesja.close()


@app.route("/sprzet")
def sprzet_view():
    sesja = Session()
    try:
        # Pobierz parametr sortowania z URL
        sort_by = request.args.get("sort", "IdSprzetu")
        order = request.args.get("order", "asc")

        # Mapowanie nazw kolumn
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


@app.route("/sprzet/dodaj", methods=["GET", "POST"])
def dodaj_sprzet_view():
    if request.method == "POST":
        producent = request.form.get("producent")
        model = request.form.get("model")
        kategoria = request.form.get("kategoria")
        sesja = Session()
        try:
            nowy_sprzet = Sprzet(Producent=producent, Model=model, Kategoria=kategoria)
            sesja.add(nowy_sprzet)
            sesja.commit()
        finally:
            sesja.close()
        return redirect(url_for("sprzet_view"))
    else:
        return render_template("dodaj_sprzet.html")


@app.route("/utwory")
def utwory_view():
    sesja = Session()
    try:
        # Pobierz parametr sortowania z URL
        sort_by = request.args.get("sort", "IdUtworu")
        order = request.args.get("order", "asc")

        # Dla sortowania po artyście musimy użyć joina
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
            # Standardowe sortowanie po kolumnach Utwory
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


@app.route("/utwory/dodaj", methods=["GET", "POST"])
def dodaj_utwor_view():
    sesja = Session()
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
            print(f"Błąd podczas dodawania sesji: {e}")
        finally:
            sesja.close()
        return redirect(url_for("utwory_view"))
    else:
        try:
            artysci = sesja.query(Artysci).order_by(Artysci.Nazwa).all()
            sesje = sesja.query(Sesje).order_by(Sesje.IdSesji).all()
            return render_template("dodaj_utwor.html", artysci=artysci, sesje=sesje)
        finally:
            sesja.close()


@app.route("/sesje")
def sesje_view():
    sesja = Session()
    try:
        # Pobierz parametr sortowania z URL
        sort_by = request.args.get("sort", "IdSesji")
        order = request.args.get("order", "asc")

        # Dla sortowania po powiązanych tabelach
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
            # Standardowe sortowanie po kolumnach Sesje
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


@app.route("/sesje/<int:IdSesji>")
def sesja_details_view(IdSesji):
    sesja = Session()
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


@app.route("/sesje/dodaj", methods=["GET", "POST"])
def dodaj_sesje_view():
    sesja = Session()
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
        return redirect(url_for("sesje_view"))
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
