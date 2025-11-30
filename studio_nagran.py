from flask import Flask, request, redirect, url_for, render_template
from pprint import pprint

# Flask  - główna klasa frameworka webowego, z niej tworzymy obiekt aplikacji
# request - obiekt opisujący żądanie z przeglądarki (metoda GET/POST, dane formularza itd.)
# redirect - funkcja do przekierowania użytkownika na inny adres (np. po zapisaniu danych)
# url_for  - funkcja do wygodnego budowania adresów URL na podstawie nazwy funkcji widoku

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    joinedload,
    contains_eager,
)

# create_engine   - tworzy "silnik" bazy, czyli obiekt do łączenia się z bazą danych
# Column, Integer, String, Float, ForeignKey - typy pól i klucze obce w modelach ORM
# declarative_base - tworzy klasę bazową, po której dziedziczą nasze modele (Klient, Produkt...)
# relationship    - opisuje relacje między tabelami (np. klient -> zamówienia)
# sessionmaker    - tworzy "fabrykę sesji", z której będziemy tworzyć konkretne sesje


# ---- KONFIGURACJA BAZY I ORM ----

# Silnik bazy SQLite.
# "sqlite:///sklep.db" - baza w pliku sklep.db w bieżącym katalogu.
# echo=True   - wypisuje w konsoli wszystkie zapytania SQL (bardzo przydatne w nauce).
# future=True - włącza nowszy styl SQLAlchemy (zgodny z wersją 2.x).
engine = create_engine("sqlite:///studio_nagran_01.db", echo=True, future=True)

# "Fabryka sesji" (do pracy z bazą).
#
# Uwaga:
# - sessionmaker(...) tworzy KLASĘ / SZABLON sesji.
# - Zmienna Session nie jest jeszcze połączeniem z bazą.
# - Dopiero wywołanie Session() tworzy KONKRETNY obiekt sesji:
#       sesja = Session()
#
# Sesja odpowiada za:
# - wykonywanie zapytań (SELECT, INSERT, UPDATE, DELETE),
# - śledzenie obiektów (Klient, Produkt itd.),
# - transakcje (commit, rollback).
Session = sessionmaker(bind=engine)

# Klasa bazowa dla modeli ORM.
# Wszystkie nasze modele (Klient, Produkt, Zamowienie, Koszyk) dziedziczą po Base.
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


# ---- APLIKACJA FLASK ----
app = Flask(__name__)


@app.route("/")
def index():
    init_db()  # upewniamy się, że baza i dane istnieją (tworzy tabele + dane przykładowe)
    return render_template("index.html")


@app.route("/artysci")
def artysci_view():
    sesja = Session()
    try:
        wynik_zapytania = select(Artysci)
        rezultat = sesja.execute(wynik_zapytania)
        artysci = rezultat.scalars().all()

        return render_template("artysci.html", artysci=artysci)
    finally:
        sesja.close()


@app.route("/artysci/dodaj", methods=["GET", "POST"])
def dodaj_artyste_view():
    """
    Widok obsługujący adres /artysci/dodaj.

    - przy metodzie GET: wyświetla prosty formularz HTML,
    - przy metodzie POST: czyta dane z formularza i zapisuje nowy produkt do bazy.
    """
    if request.method == "POST":
        # Odczyt danych z formularza (parametry "nazwa" i "cena")
        nazwa = request.form.get("nazwa")
        imie = request.form.get("imie")
        nazwisko = request.form.get("nazwisko")

        # Zapis do bazy
        sesja = Session()
        try:
            nowy_artysta = Artysci(Nazwa=nazwa, Imie=imie, Nazwisko=nazwisko)
            sesja.add(nowy_artysta)
            sesja.commit()
        finally:
            sesja.close()

        # Po dodaniu produktu przekierowujemy z powrotem na listę produktów
        return redirect(url_for("artysci_view"))
    else:
        # Jeśli metoda GET – wyświetlamy prosty formularz HTML
        return render_template("dodaj_artyste.html")

@app.route("/artysci/edytuj/<int:IdArtysty>", methods=["GET", "POST"])
def edytuj_artyste_view(IdArtysty):
    """
    Widok do edycji istniejącego artysty.
    """
    sesja = Session()
    try:
        artysta = sesja.query(Artysci).filter(Artysci.IdArtysty == IdArtysty).first()
        
        if request.method == "POST":
            # Aktualizacja danych z formularza
            artysta.Nazwa = request.form.get("nazwa")
            artysta.Imie = request.form.get("imie")
            artysta.Nazwisko = request.form.get("nazwisko")
            
            sesja.commit()
            return redirect(url_for("artysci_view"))
        else:
            # GET - wyświetl formularz z aktualnymi danymi
            return render_template("edytuj_artyste.html", artysta=artysta)
    finally:
        sesja.close()


@app.route("/inzynierowie")
def inzynierowie_view():

    sesja = Session()
    try:
        wynik_zapytania = select(Inzynierowie)
        rezultat = sesja.execute(wynik_zapytania)
        inzynierowie = rezultat.scalars().all()

        return render_template("inzynierowie.html", inzynierowie=inzynierowie)
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
    """
    Widok do edycji istniejącego inżyniera.
    """
    sesja = Session()
    try:
        inzynier = sesja.query(Inzynierowie).filter(Inzynierowie.IdInzyniera == IdInzyniera).first()
        
        if request.method == "POST":
            # Aktualizacja danych z formularza
            inzynier.Imie = request.form.get("imie")
            inzynier.Nazwisko = request.form.get("nazwisko")
            
            sesja.commit()
            return redirect(url_for("inzynierowie_view"))
        else:
            # GET - wyświetl formularz z aktualnymi danymi
            return render_template("edytuj_inzyniera.html", inzynier=inzynier)
    finally:
        sesja.close()


@app.route("/sprzet")
def sprzet_view():

    sesja = Session()
    try:
        sprzety = sesja.query(Sprzet).all()

        return render_template("sprzet.html", sprzety=sprzety)
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
        utwory = (
            sesja.query(Utwory)
            .options(joinedload(Utwory.artysci))
            .options(joinedload(Utwory.sesje))
            .all()
        )
        return render_template("utwory.html", utwory=utwory)
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
        sesje = (
            sesja.query(Sesje)
            .options(joinedload(Sesje.artysci))
            .options(joinedload(Sesje.inzynierowie))
            .all()
        )
        return render_template("sesje.html", sesje=sesje)
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


@app.route("/artysci/<int:IdArtysty>")
def utwory_artysty_view(IdArtysty):
    sesja = Session()

    try:
        utwory_artysty = select(Utwory).where(Utwory.IdArtysty == IdArtysty)

        result = sesja.execute(utwory_artysty).scalars().all()

        return render_template("modal_utwory.html", utwory_artysty=result)
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
    # Ten blok wykona się tylko wtedy, gdy uruchamiamy ten plik bezpośrednio:
    #   python mini_sklep.py
    #
    # debug=True:
    # - Flask wyświetla ładniejsze komunikaty o błędach,
    # - w trybie developerskim przeładowuje serwer po zmianie kodu.
    app.run(host="0.0.0.0", port=5000, debug=True)
