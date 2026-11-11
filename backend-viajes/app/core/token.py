
import base64
import secrets
import time
from uuid import uuid4

import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from app.core.config import settings


# 1. Obtener el secreto original desde Base64
try:
    MASTER_SECRET = base64.b64decode(
        settings.APP_TOKEN_SECRET,
        validate=True,
    )
except Exception as exc:
    raise RuntimeError("APP_TOKEN_SECRET no es Base64 válido") from exc

if len(MASTER_SECRET) != 32:
    raise RuntimeError("APP_TOKEN_SECRET debe representar exactamente 32 bytes")


# 2. Derivar claves independientes mediante HKDF-SHA256
def derive_key(info: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=info,
    ).derive(MASTER_SECRET)


SIGNING_KEY = derive_key(b"jwt-firma")
ENCRYPTION_KEY = derive_key(b"jwt-cifrado")


# 3. Generar el payload
def create_access_token(
    usuario_id: int,
    idioma: str,
    expires_in: int = 900,
) -> str:
    now = int(time.time())

    payload = {
        "sub": str(usuario_id),
        "iat": now,
        "exp": now + expires_in,
        "jti": str(uuid4()),
        "idioma": idioma,
    }

    # 4. Firmar JWT con HS256
    signed_jwt = jwt.encode(
        payload,
        SIGNING_KEY,
        algorithm="HS256",
    )

    # 5. Cifrar JWT firmado con AES-256-GCM
    nonce = secrets.token_bytes(12)
    encrypted = AESGCM(ENCRYPTION_KEY).encrypt(
        nonce,
        signed_jwt.encode("utf-8"),
        None,
    )

    # Formato: nonce + ciphertext + tag, codificados en Base64 URL-safe
    return base64.urlsafe_b64encode(
        nonce + encrypted
    ).decode("ascii")


# 6. Descifrar y verificar el token recibido
def decode_access_token(token: str) -> dict:
    try:
        encrypted_data = base64.b64decode(
            token,
            altchars=b"-_",
            validate=True,
        )

        if len(encrypted_data) < 12 + 16:
            raise ValueError("Token cifrado demasiado corto")

        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        signed_jwt = AESGCM(ENCRYPTION_KEY).decrypt(
            nonce,
            ciphertext,
            None,
        )

        return jwt.decode(
            signed_jwt,
            SIGNING_KEY,
            algorithms=["HS256"],
        )

    except Exception as exc:
        raise ValueError("Token inválido") from exc
