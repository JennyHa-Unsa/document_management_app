# Este archivo validará las operaciones basándose en los roles y permisos del usuario.
from app.models import Usuario, Documento

def has_permission(user, action):
    """
    Verifica si un usuario tiene permisos para realizar una acción.
    """
    user_roles = user.roles
    for role in user_roles:
        for permission in role.permisos:
            if permission.accion == action:
                return True
    return False

def can_access_document(user, document):
    """
    Verifica si un usuario puede acceder a un documento específico.
    """
    if document.propietario == user.id_usuario or has_permission(user, "administrar"):
        return True
    return False
