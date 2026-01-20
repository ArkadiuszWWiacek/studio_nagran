from app.views.artysci import artysci_bp
from app.views.inzynierowie import inzynierowie_bp
from app.views.sesje import sesje_bp
from app.views.sprzet import sprzet_bp
from app.views.utwory import utwory_bp


def register_blueprints(app):
    app.register_blueprint(artysci_bp, url_prefix="/artysci")
    app.register_blueprint(inzynierowie_bp, url_prefix="/inzynierowie")
    app.register_blueprint(sprzet_bp, url_prefix="/sprzet")
    app.register_blueprint(utwory_bp, url_prefix="/utwory")
    app.register_blueprint(sesje_bp, url_prefix="/sesje")
