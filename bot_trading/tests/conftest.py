"""
Pytest configuration and database isolation fixtures.
Garantiza que la suite de pruebas NUNCA toque ni borre la base de datos real (trading_bot.db).
"""
import os
import sys

# Forzar base de datos de test antes de cualquier importacion de la aplicacion
import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_trading_bot.db"
os.environ["ENVIRONMENT"] = "test"

import pytest
from backend.config import settings

@pytest.fixture(scope="session", autouse=True)
def ensure_test_database():
    """Garantiza que settings apunta a la base de datos de test y limpia al finalizar."""
    assert "test_trading_bot.db" in settings.DATABASE_URL, f"PELIGRO: Los tests estan apuntando a {settings.DATABASE_URL}"
    yield
    # Limpiar archivo de base de datos de test al finalizar la sesion
    for f in ["test_trading_bot.db", "test_trading_bot.db-wal", "test_trading_bot.db-shm"]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass
