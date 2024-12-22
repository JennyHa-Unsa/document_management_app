from .. import db

class RolesPermisos(db.Model):
    __tablename__ = 'roles_permisos'
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True)
    id_permiso = db.Column(db.Integer, db.ForeignKey('permisos.id_permiso'), primary_key=True)
