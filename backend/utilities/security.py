from __future__ import annotations

import hashlib, os

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class Password:
    # Security Parameters
    salt_len: int = 32
    hash_function: str = "SHA256"
    hmac_iterations: int = 500000

    @classmethod
    def hashPassword(cls: Password, password: str) -> str:
        salt: bytes = os.urandom(cls.salt_len).hex().encode("UTF-8")
        return salt.decode("utf-8", errors="ignore") + hashlib.pbkdf2_hmac(cls.hash_function, password.encode("utf-8"), salt, cls.hmac_iterations).decode("utf-8", errors="ignore")

    @classmethod
    def isSame(cls: Password, hashed_password: str, plain_password: str) -> bool:
        if (hashed_password is None) or (plain_password is None):
            return False
        elif len(hashed_password) < cls.salt_len*2: 
            return False

        salt: bytes = hashed_password[:cls.salt_len*2].encode("utf-8")
        return hashed_password == (salt.decode("utf-8", errors="ignore") + hashlib.pbkdf2_hmac(cls.hash_function, plain_password.encode("utf-8"), salt, cls.hmac_iterations).decode("utf-8", errors="ignore"))


# TODO:
class Certificate:
    @staticmethod
    def isValid(path: str) -> bool:
        return False

    @staticmethod
    def generate(path: str) -> bool:
        return False