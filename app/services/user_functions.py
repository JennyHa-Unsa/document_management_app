from ..models.usuario import Usuario
from .. import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

def get_user_by_email(email):
    """
    Busca un usuario en la base de datos por su correo electrónico.
    :param email: Correo electrónico del usuario.
    :return: Objeto Usuario o None si no se encuentra.
    """
    return Usuario.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """
    Busca un usuario en la base de datos por su ID.
    :param user_id: ID del usuario.
    :return: Objeto Usuario o None si no se encuentra.
    """
    return Usuario.query.get(user_id)

def save_user_to_db(name, phone, email, password):
    """
    Guarda un nuevo usuario en la base de datos.
    :param name: Nombre del usuario.
    :param phone: Teléfono del usuario.
    :param email: Correo electrónico del usuario.
    :param password: Contraseña sin cifrar.
    :return: Mensaje de éxito o excepción.
    """
    hashed_password = generate_password_hash(password)
    new_user = Usuario(
        nombre=name,
        telefono=phone,
        email=email,
        password_hash=hashed_password
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        raise ValueError("El correo electrónico ya está registrado.")
