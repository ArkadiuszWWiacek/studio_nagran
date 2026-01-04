from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///studio_nagran_01.db", echo=True, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    sesja = Session()
    try:
        # Sprawdzenie czy baza już istnieje
        from app.models import Artysci
        if sesja.query(Artysci).first() is not None:
            return
    finally:
        sesja.close()
