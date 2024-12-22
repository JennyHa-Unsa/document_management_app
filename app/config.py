import os

class Config:
    # Configuración para SQLite (puedes cambiar la ruta a donde prefieras almacenar el archivo .db)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "random string"  # Para sesiones y autenticación
    # SECRET_KEY = os.urandom(24)  # Para sesiones y autenticación

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
