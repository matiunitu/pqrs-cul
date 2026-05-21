from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt

# ─── Configuración JWT ─────────────────────────────────────────────────────────
SECRET_KEY = "supersecretkey_pqrs_2024_$#@!"   # Cambiar en producción
ALGORITHM  = "HS256"
# Token expira en 60 minutos (temporal / sesión corta)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ─── Hash de contraseñas ───────────────────────────────────────────────────────

def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        # Check if the hash is a valid bcrypt hash
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except (ValueError, TypeError):
        # ValueError is raised if the hash is not a valid bcrypt hash
        return False


def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode('utf-8'), salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
