import pytest
from flask import session
from app import create_app
from app.models.usuario import db, Usuario

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Agregar usuario de prueba
            user = Usuario(
                nombre="Test User",
                telefono="+1234567890",
                email="test@example.com",
                password_hash="hashed_password",
                otp_secret="base32secret3232"
            )
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post("/auth/register", data={
        "name": "New User",
        "phone": "+1987654321",
        "email": "new_user@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200  # Verifica que la redirección fue exitosa
    assert "Usuario registrado con éxito.".encode('utf-8') in response.data

def test_login_with_valid_credentials(client):
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "hashed_password"  # Simula la contraseña correcta
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Se ha enviado un código OTP a tu número de teléfono.".encode('utf-8') in response.data
    assert "temp_user_id" in session

def test_login_with_invalid_credentials(client):
    response = client.post("/auth/login", data={
        "email": "wrong@example.com",
        "password": "wrong_password"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Credenciales inválidas. Por favor, intente nuevamente.".encode('utf-8') in response.data

def test_verify_otp_with_correct_code(client):
    with client.session_transaction() as session:
        session["temp_user_id"] = 1  # Usuario de prueba con ID 1

    response = client.post("/auth/verify", data={"otp_code": "123456"})  # Simula OTP correcto
    assert response.status_code == 302  # Redirección tras autenticación
    assert "Autenticación exitosa.".encode('utf-8') in response.data

def test_logout(client):
    with client.session_transaction() as session:
        session["user_id"] = 1  # Usuario autenticado

    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert "Has cerrado sesión.".encode('utf-8') in response.data
    
    # Verifica que el usuario ha sido desconectado limpiando la sesión 
    with client.session_transaction() as session: 
        assert "user_id" not in session
