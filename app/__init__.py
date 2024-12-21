from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializa extensiones
    db.init_app(app)

    # Registra rutas (se agregarán más adelante)
    with app.app_context():
        from app.routes import auth, document
        app.register_blueprint(auth.bp)
        app.register_blueprint(document.bp)

    return app
