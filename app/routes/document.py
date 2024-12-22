from flask import Blueprint
from app.auth.rbac import verificar_permiso, verificar_jerarquia


bp = Blueprint("document", __name__)

@bp.route("/documents")
def documents():
    return "Document route is working!"
