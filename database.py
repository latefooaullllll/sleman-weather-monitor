
import sqlite3
from pathlib import Path

# Lokasi database
DB_PATH = Path(__file__).resolve().parent / "sleman_weather.db"


# Membuat koneksi database
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Membuat database dan tabel
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel data cuaca
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_update TEXT NOT NULL UNIQUE,
            suhu REAL,
            kelembapan REAL,
            kecepatan_angin REAL,
            kode_cuaca INTEGER,
            kondisi TEXT
        )
    """)

    # Tabel pengguna Telegram
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_chats (
            chat_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()

    print("Database berhasil disiapkan!")


# Menyimpan data cuaca
def save_weather(weather, condition):
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO weather_data (
            waktu_update,
            suhu,
            kelembapan,
            kecepatan_angin,
            kode_cuaca,
            kondisi
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        weather["time"],
        weather["temperature_2m"],
        weather["relative_humidity_2m"],
        weather["wind_speed_10m"],
        weather["weather_code"],
        condition
    ))

    berhasil_disimpan = cursor.rowcount > 0

    conn.commit()
    conn.close()

    if berhasil_disimpan:
        print("Data cuaca berhasil disimpan!")
    else:
        print("Data dengan waktu tersebut sudah tersedia.")

    return berhasil_disimpan


# Mengambil data cuaca terbaru
def get_latest_weather():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM weather_data
        ORDER BY waktu_update DESC
        LIMIT 1
    """)

    data = cursor.fetchone()
    conn.close()

    return dict(data) if data else None


# Mengambil seluruh riwayat cuaca
def get_weather_history(limit=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM weather_data
        ORDER BY waktu_update DESC
    """

    if limit is not None:
        cursor.execute(query + " LIMIT ?", (limit,))
    else:
        cursor.execute(query)

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return data


# Menyimpan ID pengguna Telegram
def save_chat_id(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO telegram_chats (chat_id)
        VALUES (?)
    """, (chat_id,))

    conn.commit()
    conn.close()

    print(f"Chat ID {chat_id} berhasil didaftarkan!")


# Mengambil seluruh ID pengguna Telegram
def get_chat_ids():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT chat_id FROM telegram_chats
    """)

    data = cursor.fetchall()
    conn.close()

    return [row["chat_id"] for row in data]


# Menjalankan inisialisasi jika file dijalankan langsung
if __name__ == "__main__":
    init_db()

    print("\nDatabase siap digunakan.")
    print("Lokasi database:", DB_PATH)
