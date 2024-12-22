from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager  # Manejador de sesiones de usuario
from .config import Config, TestingConfig

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == "testing": 
        app.config.from_object(TestingConfig) 
    else:
        app.config.from_object(Config)

    # Configuración de sesión
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Configuración de LoginManager
    login_manager.login_view = "auth.login"  # Redirección a login si no está autenticado
    login_manager.login_message = "Por favor, inicie sesión para acceder a esta página."
    login_manager.login_message_category = "info"

    # Callback para cargar usuario
    from .models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registra rutas de Blueprints
    with app.app_context():
        # Importa los modelos aquí para que se registren con SQLAlchemy 
        from . import models 
        db.create_all()  # Crear todas las tablas definidas en models.py

        from app.routes import auth, document
        app.register_blueprint(auth.bp)
        app.register_blueprint(document.bp)

    return app
