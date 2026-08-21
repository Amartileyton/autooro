import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

import httpx
import jwt
from fastapi import APIRouter, HTTPException, Header, Depends, status
from pydantic import BaseModel

from backend.config import settings

logger = logging.getLogger("trading_bot.auth")

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class GoogleLoginRequest(BaseModel):
    credential: str  # Google ID Token JWT


class UserProfile(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    sub: Optional[str] = None


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token JWT de sesión firmado internamente."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodifica y valida un token JWT emitido por el sistema."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("email", "").strip().lower()
        allowed = [e.strip().lower() for e in settings.ALLOWED_EMAILS]
        if email not in allowed:
            logger.warning(f"[AUTH] Token válido pero correo {email} revocado o no en ALLOWED_EMAILS")
            return None
        return payload
    except jwt.PyJWTError as e:
        logger.debug(f"[AUTH] Error al decodificar JWT: {e}")
        return None


async def verify_google_id_token(id_token: str) -> Dict[str, Any]:
    """
    Verifica criptográficamente el token con Google OAuth 2.0.
    Soporta verificación nativa con google-auth y fallback directo con Google tokeninfo API.
    """
    # 1. Intentar verificación con biblioteca oficial google-auth
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        id_info = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID or None
        )
        return id_info
    except Exception as e:
        logger.debug(f"[AUTH] google-auth verificación local: {e}. Probando tokeninfo API...")

    # 2. Fallback de alta confiabilidad con endpoint oficial tokeninfo de Google
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        )
        if resp.status_code != 200:
            logger.error(f"[AUTH] Google tokeninfo rechazó el token: {resp.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de Google inválido o expirado."
            )
        id_info = resp.json()

        # Validar audiencia (audience) si está configurado el CLIENT_ID
        aud = id_info.get("aud")
        if settings.GOOGLE_CLIENT_ID and aud != settings.GOOGLE_CLIENT_ID:
            logger.error(f"[AUTH] Audiencia no coincide: esperado={settings.GOOGLE_CLIENT_ID}, recibido={aud}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token de Google no pertenece a esta aplicación."
            )

        return id_info


async def get_current_user(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """
    Dependencia de seguridad para proteger rutas REST.
    Acepta tanto Authorization: Bearer <JWT> como X-API-KEY (para scripts internos / tests).
    """
    # 1. Si viene con X-API-KEY válida
    if settings.API_KEY and x_api_key == settings.API_KEY:
        return {"email": "system-api-key@goldex.local", "name": "System Admin (API Key)", "is_admin": True}

    # 2. Si viene con Authorization: Bearer <token>
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ", 1)[1].strip()
        payload = verify_session_token(token)
        if payload:
            return payload

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado. Inicia sesión con una cuenta de Google autorizada."
    )


@router.post("/google-login")
async def google_login(req: GoogleLoginRequest):
    """
    Recibe el token de Google, valida su firma, verifica si el correo
    está en la lista blanca y emite un JWT de sesión para el Obsidian Terminal.
    """
    id_info = await verify_google_id_token(req.credential)

    email = id_info.get("email", "").strip().lower()
    email_verified = id_info.get("email_verified", True)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token de Google no contiene un correo electrónico."
        )

    # Validar lista blanca estricta
    allowed_list = [e.strip().lower() for e in settings.ALLOWED_EMAILS]
    if email not in allowed_list:
        logger.warning(f"[SECURITY ALERT] Intento de acceso DENEGADO para correo no autorizado: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acceso denegado: El correo '{email}' no está autorizado en este terminal."
        )

    name = id_info.get("name", email.split("@")[0])
    picture = id_info.get("picture", "")

    # Crear token de sesión firmado
    session_data = {
        "sub": id_info.get("sub", email),
        "email": email,
        "name": name,
        "picture": picture,
    }
    jwt_token = create_access_token(session_data)

    logger.info(f"✅ [AUTH] Sesión iniciada con éxito para el operador autorizado: {email} ({name})")

    return {
        "status": "success",
        "access_token": jwt_token,
        "token_type": "bearer",
        "expires_in_hours": settings.JWT_EXPIRATION_HOURS,
        "user": {
            "email": email,
            "name": name,
            "picture": picture
        }
    }


@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    """Verifica el estado de la sesión actual y devuelve los datos del operador."""
    return {"status": "authenticated", "user": user}
