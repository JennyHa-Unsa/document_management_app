from flask import current_app as app
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from app.services.rbac import verificar_permiso, verificar_jerarquia
from app.services.file_operations import list_files, read_file, write_file, delete_file
from app.services.encryption import encrypt_file, decrypt_file, generate_symmetric_key
from app.models.doumento import Documento, db
from app.models.usuario import Usuario


import os

bp = Blueprint("document", __name__, url_prefix="/documents")

# Configura la ruta base para documentos
BASE_FOLDER = "encrypted_documents"

# Crea la carpeta base si no existe
if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

@bp.route("/")
@login_required
@verificar_permiso("leer")
def list_documents(): 
    """ 
    Muestra una lista de documentos accesibles para el usuario actual. 
    """ 
    if "user_id" not in session: 
        return redirect(url_for("auth.login")) # Asegúrate de redirigir al login si no está autenticado 
    
    user_documents = Documento.query.filter_by(propietario=current_user.id_usuario).all() 
    return render_template("documents/list.html", documents=user_documents)

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "xlsx", "jpg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/upload", methods=["GET", "POST"])
@login_required
@verificar_permiso("crear")
def upload_document():
    """
    Permite al usuario subir y cifrar un documento.
    """
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            if len(file.read()) > MAX_FILE_SIZE:
                flash("El archivo es demasiado grande.", "danger")
                return redirect(url_for("document.upload_document"))
            file.seek(0)  # Vuelve al inicio del archivo tras leerlo

            file_path = os.path.join(BASE_FOLDER, file.filename)
            content = file.read()

            try:
                symmetric_key = generate_symmetric_key()
                encrypted_content = encrypt_file(content, symmetric_key)

                # Guarda el archivo cifrado
                with open(file_path, "wb") as encrypted_file:
                    encrypted_file.write(encrypted_content)

                new_document = Documento(
                    nombre_documento=file.filename,
                    ruta_archivo=file_path,
                    clave_simetrica=symmetric_key.hex(),
                    propietario=current_user.id_usuario,
                    tipo=file.content_type
                )
                db.session.add(new_document)
                db.session.commit()

                flash("Documento subido y cifrado correctamente.", "success")
                return redirect(url_for("document.list_documents"))
            except Exception as e:
                flash("Error al procesar el archivo. Inténtalo de nuevo.", "danger")
                return redirect(url_for("document.upload_document"))
        else:
            flash("Tipo de archivo no permitido.", "danger")

    return render_template("documents/upload.html")



@bp.route("/download/<int:document_id>", methods=["GET"])
@login_required
@verificar_permiso("leer")
def download_document(document_id):
    """
    Descifra y permite al usuario descargar un documento.
    """
    document = Documento.query.get_or_404(document_id)

    # Validar que el usuario tiene acceso al documento
    if document.propietario != current_user.id_usuario and not verificar_permiso("administrar")():
        flash("No tienes permiso para acceder a este documento.", "danger")
        return redirect(url_for("document.list_documents"))

    with open(document.ruta_archivo, "rb") as encrypted_file:
        encrypted_content = encrypted_file.read()

    symmetric_key = bytes.fromhex(document.clave_simetrica)
    decrypted_content = decrypt_file(encrypted_content, symmetric_key)

    response = app.response_class(
        decrypted_content,
        mimetype=document.tipo,
        direct_passthrough=True,
    )
    response.headers.set("Content-Disposition", "attachment", filename=document.nombre_documento)
    return response


@bp.route("/delete/<int:document_id>", methods=["DELETE"])
@login_required
@verificar_permiso("eliminar")
def delete_document(document_id):
    """
    Permite al usuario eliminar un documento.
    """
    document = Documento.query.get_or_404(document_id)

    # Validar que el usuario tiene acceso al documento
    if document.propietario != current_user.id_usuario and not verificar_permiso("administrar")():
        flash("No tienes permiso para eliminar este documento.", "danger")
        return redirect(url_for("document.list_documents"))

    # Elimina el archivo del sistema y de la base de datos
    os.remove(document.ruta_archivo)
    db.session.delete(document)
    db.session.commit()

    flash("Documento eliminado correctamente.", "success")
    return redirect(url_for("document.list_documents"))
