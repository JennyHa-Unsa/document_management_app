from functools import wraps
from flask import request, abort
from flask_login import current_user
from app.models import Rol, Permiso, UsuariosRoles, RolesPermisos

def verificar_permiso(accion):
    """
    Decorador para verificar si el usuario tiene un permiso específico.
    :param accion: Acción que se desea validar.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Verificar si el usuario está autenticado
            if not current_user.is_authenticated:
                abort(403, "Usuario no autenticado.")

            # Obtener roles del usuario
            roles_usuario = current_user.roles  # Asume que Usuario tiene relación con roles
            permisos_usuario = set()

            # Agregar permisos según los roles del usuario
            for rol in roles_usuario:
                for permiso in rol.permisos:
                    permisos_usuario.add(permiso.accion)

            # Validar si tiene el permiso requerido
            if accion not in permisos_usuario:
                abort(403, f"Permiso '{accion}' no autorizado.")
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def verificar_jerarquia(min_jerarquia):
    """
    Decorador para verificar si el usuario tiene un rol con jerarquía suficiente.
    :param min_jerarquia: Nivel jerárquico mínimo requerido.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Verificar si el usuario está autenticado
            if not current_user.is_authenticated:
                abort(403, "Usuario no autenticado.")

            # Verificar jerarquía
            jerarquias_usuario = [rol.jerarquia for rol in current_user.roles]
            if not any(j >= min_jerarquia for j in jerarquias_usuario):
                abort(403, "Jerarquía insuficiente.")
            
            return f(*args, **kwargs)
        return wrapped
    return decorator
