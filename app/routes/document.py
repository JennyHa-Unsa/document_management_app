from flask import Blueprint

bp = Blueprint("document", __name__)

@bp.route("/documents")
def documents():
    return "Document route is working!"
