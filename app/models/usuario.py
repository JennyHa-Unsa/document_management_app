from .. import db

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
