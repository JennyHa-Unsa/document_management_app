from .. import db

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
