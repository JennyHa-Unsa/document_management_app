# Funciones auxiliares para tareas como la carga de claves públicas y privadas.
def load_public_key(user):
    """
    Carga la clave pública de un usuario desde la base de datos.
    """
    return user.clave_publica

def load_private_key(file_path):
    """
    Carga una clave privada desde un archivo local.
    """
    with open(file_path, 'rb') as file:
        return file.read()
