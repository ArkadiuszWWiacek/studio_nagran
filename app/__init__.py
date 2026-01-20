import sqlite3
from flask import Flask, render_template
import click

from app import database
from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    database.init_app(app)

    @app.cli.command("seed")
    def seed_db():
        """Zaseeduj bazę danych."""

        conn = sqlite3.connect('studio_nagran.db')
        with open('seed_data.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)

        conn.commit()
        conn.close()
        click.echo('Baza zaseedowana!')

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
