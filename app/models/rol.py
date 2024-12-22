from .. import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50))
    jerarquia = db.Column(db.Integer)

    permisos = db.relationship('Permiso', secondary='roles_permisos')
    usuarios = db.relationship('Usuario', secondary='usuarios_roles')
