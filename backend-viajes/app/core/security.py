
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba una contraseña contra su hash."""
    return password_hash.verify(plain_password, hashed_password)
