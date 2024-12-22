from flask import Flask
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    print("Base de datos SQLite:", app.config['SQLALCHEMY_DATABASE_URI'])

