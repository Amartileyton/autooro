from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, Boolean, Text, Enum as SQLEnum
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.shared.enums import OrderSide, TradeStatus, ExecutionMode


class Base(DeclarativeBase):
    pass


class RawTelegramMessage(Base):
    """Auditoría estricta del 100% de los mensajes entrantes de Telegram."""
    __tablename__ = "raw_telegram_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    channel_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default="Chartoro FX")
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_success: Mapped[bool] = mapped_column(Boolean, default=False)
    parser_used: Mapped[str] = mapped_column(String(30), default="REGEX")  # REGEX / AI / NONE
    error_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )


class Trade(Base):
    """Ciclo de vida completo de cada operación vinculada a los slots de capital."""
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    slot_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # 1 a 4
    symbol: Mapped[str] = mapped_column(String(20), default="XAUUSD")
    side: Mapped[OrderSide] = mapped_column(SQLEnum(OrderSide), nullable=False)
    status: Mapped[TradeStatus] = mapped_column(SQLEnum(TradeStatus), default=TradeStatus.PENDING, index=True)

    # Precios de alta precisión financiera
    entry_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    current_sl: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    initial_sl: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tp1: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tp2: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    tp3: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)

    lot_size: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    pnl: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    realized_cash_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    peak_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    close_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    close_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    open_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    close_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_signal_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    channel_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default="Chartoro FX", index=True)
    execution_mode: Mapped[ExecutionMode] = mapped_column(SQLEnum(ExecutionMode), default=ExecutionMode.AUDIT, index=True)  # AUDIT / PRODUCTION


class SystemAuditLog(Base):
    """Registro inmutable de eventos críticos, cambios de estado y órdenes."""
    __tablename__ = "system_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    event_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(20), default="INFO")  # INFO / WARNING / CRITICAL
    details_json: Mapped[str] = mapped_column(Text, nullable=False)


class NewsInteraction(Base):
    """Registro persistente de clics, likes, dislikes y consultas IA del usuario sobre noticias."""
    __tablename__ = "news_interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_id: Mapped[str] = mapped_column(String(128), index=True)
    news_title: Mapped[str] = mapped_column(String(300), nullable=False)
    news_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    news_asset: Mapped[Optional[str]] = mapped_column(String(60), nullable=True, default="MACRO")
    action_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # 'click', 'like', 'dislike', 'summarize'
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
