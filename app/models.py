from flask import Flask
from . import db    # Importa `db` desde __init__.py
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
    
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    activo = db.Column(db.Boolean, default=True)
    clave_publica = db.Column(db.String(256))

    roles = db.relationship('Rol', secondary='usuarios_roles')

class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50))
    jerarquia = db.Column(db.Integer)

    permisos = db.relationship('Permiso', secondary='roles_permisos')
    usuarios = db.relationship('Usuario', secondary='usuarios_roles')

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id_permiso = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(50))
    descripcion = db.Column(db.Text)

class RolesPermisos(db.Model):
    __tablename__ = 'roles_permisos'
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)
    id_permiso = db.Column(db.Integer, db.ForeignKey('permisos.id_permiso'), primary_key=True)

class UsuariosRoles(db.Model):
    __tablename__ = 'usuarios_roles'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)

class Documento(db.Model):
    __tablename__ = 'documentos'
    id_documento = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(100))
    ruta_archivo = db.Column(db.Text)
    clave_simetrica = db.Column(db.String(256))
    propietario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    tipo = db.Column(db.String(50))
    fecha_subida = db.Column(db.DateTime)

    usuario = db.relationship('Usuario', backref='documentos')

class Historial(db.Model):
    __tablename__ = 'historial'
    id_historial = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    id_documento = db.Column(db.Integer, db.ForeignKey('documentos.id_documento'))
    accion = db.Column(db.String(50))
    fecha_accion = db.Column(db.DateTime)
    descripcion = db.Column(db.Text)

    usuario = db.relationship('Usuario', backref='acciones')
    documento = db.relationship('Documento', backref='acciones')
