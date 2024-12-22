# Este archivo implementará el cifrado simétrico y asimétrico utilizando PyCryptodome.
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

def generate_symmetric_key():
    """
    Genera una clave simétrica para cifrar archivos.
    """
    return get_random_bytes(32)

def encrypt_file(content, key):
    """
    Cifra el contenido de un archivo con AES.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(content)
    return cipher.nonce + tag + ciphertext

def decrypt_file(encrypted_content, key):
    """
    Descifra el contenido de un archivo cifrado con AES.
    """
    nonce = encrypted_content[:16]
    tag = encrypted_content[16:32]
    ciphertext = encrypted_content[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def encrypt_key_with_public_key(key, public_key_pem):
    """
    Cifra una clave simétrica usando una clave pública (RSA).
    """
    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(key)

def decrypt_key_with_private_key(encrypted_key, private_key_pem):
    """
    Descifra una clave simétrica usando una clave privada (RSA).
    """
    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_key)
