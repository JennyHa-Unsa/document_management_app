from .. import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id_permiso = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(50))
    descripcion = db.Column(db.Text)

