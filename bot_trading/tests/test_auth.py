import pytest
from datetime import timedelta
from backend.config import settings
from backend.api.auth import create_access_token, verify_session_token


def test_allowed_emails_configuration():
    """Verifica que los correos autorizados estén cargados correctamente en settings."""
    allowed = [e.lower() for e in settings.ALLOWED_EMAILS]
    assert "adriamartileyton@gmail.com" in allowed
    assert "adriamartileyton2@gmail.com" in allowed
    assert "intruder@gmail.com" not in allowed


def test_jwt_token_issuance_and_verification_success():
    """Verifica emisión y decodificación de JWT para un correo autorizado."""
    user_data = {
        "sub": "google-sub-12345",
        "email": "adriamartileyton@gmail.com",
        "name": "Adrià Martí",
        "picture": "https://lh3.googleusercontent.com/a/dummy"
    }

    token = create_access_token(user_data)
    assert isinstance(token, str)
    assert len(token) > 20

    payload = verify_session_token(token)
    assert payload is not None
    assert payload["email"] == "adriamartileyton@gmail.com"
    assert payload["name"] == "Adrià Martí"


def test_jwt_token_verification_rejected_for_unauthorized_email():
    """Verifica que un token con correo no autorizado sea rechazado por la lista blanca."""
    unauthorized_data = {
        "sub": "google-sub-99999",
        "email": "intruder@example.com",
        "name": "Hacker",
    }

    token = create_access_token(unauthorized_data)
    payload = verify_session_token(token)
    assert payload is None


def test_expired_jwt_token():
    """Verifica que un token expirado sea rechazado."""
    user_data = {
        "sub": "google-sub-12345",
        "email": "adriamartileyton2@gmail.com",
        "name": "Adrià 2",
    }

    # Emitir token expirado hace 1 hora
    expired_token = create_access_token(user_data, expires_delta=timedelta(hours=-1))
    payload = verify_session_token(expired_token)
    assert payload is None
