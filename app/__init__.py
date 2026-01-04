from flask import Flask, render_template
from app.database import init_db

def create_app():
    app = Flask(__name__)
    
    from app.views.artysci import artysci_bp
    from app.views.inzynierowie import inzynierowie_bp
    from app.views.sprzet import sprzet_bp
    from app.views.utwory import utwory_bp
    from app.views.sesje import sesje_bp
    
    app.register_blueprint(artysci_bp, url_prefix='/artysci')
    app.register_blueprint(inzynierowie_bp, url_prefix='/inzynierowie')
    app.register_blueprint(sprzet_bp, url_prefix='/sprzet')
    app.register_blueprint(utwory_bp, url_prefix='/utwory')
    app.register_blueprint(sesje_bp, url_prefix='/sesje')
    
    @app.route("/")
    def index():
        init_db()
        return render_template("index.html")
    
    return app
