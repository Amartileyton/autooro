from decimal import Decimal
from typing import List, Optional, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Entorno y Servidor API
    ENVIRONMENT: str = Field(default="development", description="development / production")
    HOST: str = Field(default="0.0.0.0", description="Host del backend FastAPI")
    PORT: int = Field(default=8000, description="Puerto del backend FastAPI")
    API_KEY: str = Field(default="sec_xauusd_trading_key_2026", description="API Key para proteger endpoints REST")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:4321", "http://127.0.0.1:4321", "*"],
        description="Orígenes permitidos para CORS"
    )

    # Base de Datos SQLite WAL
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./trading_bot.db",
        description="URL asíncrona de SQLite"
    )

    # Telegram MTProto Ingesta (Telethon)
    TG_API_ID: int = Field(default=0, description="API ID obtenido en my.telegram.org")
    TG_API_HASH: str = Field(default="", description="API Hash obtenido en my.telegram.org")
    TG_PHONE: str = Field(default="", description="Número de teléfono de la cuenta Telegram")
    TG_SESSION_NAME: str = Field(default="bot_session", description="Nombre del archivo .session de Telethon")
    TARGET_CHANNEL_ID: int = Field(default=0, description="ID numérico del canal de Telegram a escuchar")
    INGESTION_ENABLED: bool = Field(default=True, description="Flag maestro para habilitar/pausar ingesta")

    # Telegram Bot Administrativo (Aiogram)
    TELEGRAM_BOT_TOKEN: str = Field(default="", description="Token del bot privado creado con @BotFather")
    ADMIN_TELEGRAM_USER_ID: int = Field(default=0, description="ID numérico del usuario administrador")

    # Motor de Riesgo y Slots
    MAX_CONCURRENT_SLOTS: int = Field(default=4, description="Número máximo de slots concurrentes")
    SLOT_MARGIN_PERCENT: Decimal = Field(default=Decimal("0.25"), description="Porcentaje de margen libre por slot (25%)")
    LEVERAGE: Decimal = Field(default=Decimal("100.0"), description="Apalancamiento de la cuenta (ej. 100:1)")
    CONTRACT_SIZE: Decimal = Field(default=Decimal("100.0"), description="Tamaño de contrato XAUUSD (100 oz troy)")
    MIN_LOT_SIZE: Decimal = Field(default=Decimal("0.01"), description="Lote mínimo permitido por el broker")
    LOT_STEP: Decimal = Field(default=Decimal("0.01"), description="Incremento de lote permitido")
    SLIPPAGE_TOLERANCE_USD: Decimal = Field(default=Decimal("0.00"), description="Tolerancia máxima de deslizamiento en USD")
    DEFAULT_DYNAMIC_SL_DELTA_USD: Decimal = Field(
        default=Decimal("8.50"),
        description="Delta en USD para SL dinámico si la señal no especifica SL"
    )
    AUTO_EXECUTION_ENABLED: bool = Field(default=True, description="Flag maestro para habilitar/pausar auto-ejecución")

    # Capa de Broker
    BROKER_TYPE: str = Field(default="paper", description="'paper' para simulación local, 'ctrader' para live")
    INITIAL_PAPER_BALANCE: Decimal = Field(default=Decimal("10000.00"), description="Balance inicial para Paper Broker")
    PAPER_SPREAD_MIN_CENTS: Decimal = Field(default=Decimal("0.10"), description="Spread mínimo simulado en USD")
    PAPER_SPREAD_MAX_CENTS: Decimal = Field(default=Decimal("0.25"), description="Spread máximo simulado en USD")
    INITIAL_XAUUSD_PRICE: Decimal = Field(default=Decimal("2345.50"), description="Precio inicial de simulación de XAUUSD")

    # cTrader Open API Credentials (para modo live)
    CTRADER_CLIENT_ID: str = Field(default="", description="cTrader Open API Client ID")
    CTRADER_CLIENT_SECRET: str = Field(default="", description="cTrader Open API Client Secret")
    CTRADER_ACCOUNT_ID: int = Field(default=0, description="cTrader Account ID")
    CTRADER_ACCESS_TOKEN: str = Field(default="", description="cTrader Access Token")
    CTRADER_HOST: str = Field(default="live.ctraderapi.com", description="Host cTrader Open API")
    CTRADER_PORT: int = Field(default=5035, description="Puerto cTrader Open API")

    # IA Fallback (Opcional para rescate de señales no estructuradas)
    AI_FALLBACK_ENABLED: bool = Field(default=False, description="Activar IA como parser de rescate secundario")
    AI_API_KEY: str = Field(default="", description="API Key de OpenAI o Gemini")
    AI_PROVIDER: str = Field(default="gemini", description="'gemini' o 'openai'")
    AI_MODEL: str = Field(default="gemini-2.0-flash", description="Modelo de ultra-baja latencia")

    @field_validator("TG_API_ID", "TARGET_CHANNEL_ID", "ADMIN_TELEGRAM_USER_ID", "CTRADER_ACCOUNT_ID", "PORT", "MAX_CONCURRENT_SLOTS", "CTRADER_PORT", mode="before")
    @classmethod
    def parse_optional_int(cls, v: Any) -> int:
        if v is None or v == "":
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0

    @field_validator("SLOT_MARGIN_PERCENT", "LEVERAGE", "CONTRACT_SIZE", "MIN_LOT_SIZE", "LOT_STEP", "SLIPPAGE_TOLERANCE_USD", "DEFAULT_DYNAMIC_SL_DELTA_USD", "INITIAL_PAPER_BALANCE", "PAPER_SPREAD_MIN_CENTS", "PAPER_SPREAD_MAX_CENTS", "INITIAL_XAUUSD_PRICE", mode="before")
    @classmethod
    def parse_optional_decimal(cls, v: Any) -> Decimal:
        if v is None or v == "":
            return Decimal("0.0")
        return Decimal(str(v))


settings = Settings()
