import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from backend.config import settings

logger = logging.getLogger("trading_bot.database")

# Crear el sync engine para migraciones e inicialización sin dependencia de greenlet
sync_engine = create_engine(
    "sqlite:///trading_bot.db",
    echo=False
)

# Crear el async engine de SQLAlchemy para SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Configura pragmas de alto rendimiento y cero corrupción para SQLite.
    WAL (Write-Ahead Logging) permite lecturas y escrituras concurrentes sin bloqueos.
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA foreign_keys=ON;")

        # Auto-migración segura de columnas añadidas en trades si la tabla ya existía
        try:
            cursor.execute("ALTER TABLE trades ADD COLUMN realized_cash_pnl NUMERIC(18, 2) DEFAULT 0.00;")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE trades ADD COLUMN peak_price NUMERIC(18, 4);")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE trades ADD COLUMN channel_id INTEGER;")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE trades ADD COLUMN channel_name VARCHAR(120) DEFAULT 'Chartoro FX';")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE trades ADD COLUMN execution_mode VARCHAR(30) DEFAULT 'AUDIT';")
        except Exception:
            pass

        cursor.close()
        logger.info("SQLite Pragmas (WAL, NORMAL, busy_timeout=5000) configurados correctamente.")
    except Exception as e:
        logger.error(f"Error al configurar pragmas de SQLite: {e}")


# Fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_db():
    """Generador de sesión asíncrona para inyección de dependencias."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
