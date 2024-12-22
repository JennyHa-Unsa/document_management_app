import os
import pytest
from app import create_app
from app.models import db, Usuario, Documento

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

@pytest.fixture
def setup_documents(client):
    with client.app_context():
        user = Usuario.query.filter_by(email="test@example.com").first()
        document = Documento(
            nombre_documento="test.txt",
            ruta_archivo="encrypted_documents/test.txt",
            clave_simetrica="abc123",
            propietario=user.id_usuario
        )
        db.session.add(document)
        db.session.commit()

def test_list_documents(client, setup_documents):
    with client.session_transaction() as session:
        session["user_id"] = 1  # Simula un usuario autenticado

    response = client.get("/documents/")
    assert response.status_code == 200
    assert b"test.txt" in response.data

def test_upload_document(client):
    with client.session_transaction() as session:
        session["user_id"] = 1  # Simula un usuario autenticado

    file_data = {"file": (b"dummy content", "test_upload.txt")}
    response = client.post("/documents/upload", data=file_data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200
    assert b"Documento subido y cifrado correctamente" in response.data
    assert os.path.exists("encrypted_documents/test_upload.txt")

def test_download_document(client, setup_documents):
    with client.session_transaction() as session:
        session["user_id"] = 1  # Simula un usuario autenticado

    response = client.get("/documents/download/1")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'attachment; filename="test.txt"'

def test_delete_document(client, setup_documents):
    with client.session_transaction() as session:
        session["user_id"] = 1  # Simula un usuario autenticado

    response = client.post("/documents/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Documento eliminado correctamente" in response.data
    assert not os.path.exists("encrypted_documents/test.txt")
