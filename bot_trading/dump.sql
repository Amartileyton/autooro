BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    message_id INTEGER, 
    channel_id INTEGER, 
    channel_name VARCHAR(120), 
    raw_text TEXT NOT NULL, 
    parsed_success BOOLEAN NOT NULL, 
    parser_used VARCHAR(30) NOT NULL, 
    error_reason VARCHAR(255), 
    received_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id VARCHAR(50) UNIQUE,
    slot_id INTEGER,
    symbol VARCHAR(20) DEFAULT 'XAUUSD',
    side VARCHAR(10) NOT NULL,
    status VARCHAR(30) NOT NULL,
    entry_price NUMERIC(18, 4) NOT NULL,
    current_sl NUMERIC(18, 4),
    initial_sl NUMERIC(18, 4),
    tp1 NUMERIC(18, 4),
    tp2 NUMERIC(18, 4),
    tp3 NUMERIC(18, 4),
    lot_size NUMERIC(18, 4) NOT NULL,
    pnl NUMERIC(18, 2) DEFAULT 0.00,
    realized_cash_pnl NUMERIC(18, 2) DEFAULT 0.00,
    peak_price NUMERIC(18, 4),
    close_price NUMERIC(18, 4),
    close_reason VARCHAR(100),
    open_time DATETIME NOT NULL,
    close_time DATETIME,
    raw_signal_id INTEGER,
    channel_id INTEGER,
    channel_name VARCHAR(120) DEFAULT 'Chartoro FX',
    execution_mode VARCHAR(30) DEFAULT 'AUDIT'
);
CREATE TABLE IF NOT EXISTS system_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type VARCHAR(50) NOT NULL,
    actor VARCHAR(50) NOT NULL,
    slot_id INTEGER,
    ticket_id VARCHAR(50),
    details_json TEXT,
    created_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS news_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_id VARCHAR(100) NOT NULL,
    news_title VARCHAR(255) NOT NULL,
    news_url TEXT,
    news_asset VARCHAR(50) DEFAULT 'MACRO',
    action_type VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL
);
COMMIT;
