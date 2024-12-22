from .. import db

class UsuariosRoles(db.Model):
    __tablename__ = 'usuarios_roles'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)
