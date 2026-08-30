import os
import sys
import sqlite3

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

db_paths = [
    "trading_bot.db",
    "data/trading_bot.db",
    "/app/data/trading_bot.db",
    "/app/trading_bot.db"
]

def reset_database(db_path: str):
    if not os.path.exists(db_path):
        return False

    print(f"🧹 Limpiando base de datos: {db_path}...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Eliminar trades antiguos
        cursor.execute("DELETE FROM trades;")
        print("  - Tabla 'trades' vaciada.")
        
        # Eliminar mensajes de telegram antiguos
        cursor.execute("DELETE FROM raw_telegram_messages;")
        print("  - Tabla 'raw_telegram_messages' vaciada.")
        
        # Eliminar logs de auditoría antiguos
        cursor.execute("DELETE FROM system_audit_logs;")
        print("  - Tabla 'system_audit_logs' vaciada.")
        
        # Reiniciar secuencias autoincrementales
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('trades', 'raw_telegram_messages', 'system_audit_logs');")
        except Exception:
            pass

        conn.commit()
        cursor.execute("VACUUM;")
        cursor.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.close()
        print(f"✅ Base de datos {db_path} reiniciada a cero con éxito.")
        return True
    except Exception as e:
        print(f"❌ Error al limpiar {db_path}: {e}")
        return False

def main():
    print("==================================================")
    print("🚀 REINICIO DE HISTORIAL DE TRADES (AUTOORO)")
    print("==================================================")
    cleaned_any = False
    for p in db_paths:
        if reset_database(p):
            cleaned_any = True

    if not cleaned_any:
        print("No se encontraron bases de datos en las rutas habituales. Creando/limpiando data/trading_bot.db...")
        os.makedirs("data", exist_ok=True)
        reset_database("data/trading_bot.db")

    print("==================================================")
    print("✨ HISTORIAL VACIADO AL 100%. LISTO PARA LA NUEVA SESIÓN.")
    print("==================================================")

if __name__ == "__main__":
    main()
