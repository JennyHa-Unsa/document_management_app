# Este archivo manejará las operaciones básicas del sistema de archivos, utilizando PyFilesystem2.
from fs.osfs import OSFS
import os

def list_files(folder_path):
    """
    Lista los archivos en una carpeta especificada.
    """
    with OSFS(folder_path) as fs:
        return [file.name for file in fs.scandir("/") if not file.is_dir]

def read_file(folder_path, file_name):
    """
    Lee el contenido de un archivo.
    """
    with OSFS(folder_path) as fs:
        with fs.open(file_name, 'rb') as file:
            return file.read()

def write_file(folder_path, file_name, content):
    """
    Escribe contenido en un archivo.
    """
    with OSFS(folder_path) as fs:
        with fs.open(file_name, 'wb') as file:
            file.write(content)

def delete_file(folder_path, file_name):
    """
    Elimina un archivo.
    """
    with OSFS(folder_path) as fs:
        fs.remove(file_name)
