from flask import Flask
from app import create_app
# from app.models import db

app = create_app()

# Crea las tablas si no existen aún
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    print("Base de datos SQLite:", app.config['SQLALCHEMY_DATABASE_URI'])

