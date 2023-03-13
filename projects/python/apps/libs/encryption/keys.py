import base64

from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def encrypt(message, pk):
    public_key = serialization.load_ssh_public_key(bytes(pk, 'ascii'))
    ciphertext = public_key.encrypt(
        bytes(message, 'ascii'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(ciphertext)


def generate_keys():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    return private_key, public_key