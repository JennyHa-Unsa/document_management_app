from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Configuración de sesión
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Inicializa extensiones
    db.init_app(app)
    csrf.init_app(app)

    # Registra rutas
    with app.app_context():
        from app.routes import auth, document
        app.register_blueprint(auth.bp)
        app.register_blueprint(document.bp)

    return app
