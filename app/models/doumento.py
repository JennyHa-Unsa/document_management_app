from .. import db

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
