from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

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