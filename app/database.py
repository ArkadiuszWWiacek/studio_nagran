import click
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///studio_nagran_01.db", echo=True, future=True)
session = sessionmaker(bind=engine, expire_on_commit=False)
base = declarative_base()

def init_db():
    base.metadata.create_all(bind=engine)

def init_app(app: Flask):
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("Initialized the database.")
