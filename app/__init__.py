from flask import Flask, render_template

from app import database
from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    database.init_app(app)  # rejestruje komendę flask init-db

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
