from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config.from_object(Config)

    # Configuración de sesión
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Registra rutas de Blueprints
    with app.app_context():
        # Importa los modelos aquí para que se registren con SQLAlchemy 
        from . import models 
        db.create_all() # Crear todas las tablas definidas en models.py

        from app.routes import auth, document
        app.register_blueprint(auth.bp)
        app.register_blueprint(document.bp)

    return app
