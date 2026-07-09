import sqlite3
from datetime import datetime

DB_NAME = "space.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS apod (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT UNIQUE,
            title       TEXT,
            explanation TEXT,
            url         TEXT,
            media_type  TEXT,
            fetched_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS favourites (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            apod_id   INTEGER,
            saved_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (apod_id) REFERENCES apod(id)
        );

        CREATE TABLE IF NOT EXISTS search_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword     TEXT,
            searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully!")

def save_apod(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO apod (date, title, explanation, url, media_type)
            VALUES (?, ?, ?, ?, ?)
        """, (data['date'], data['title'], data['explanation'], data['url'], data['media_type']))
        conn.commit()
    except Exception as e:
        print(f"Error saving APOD: {e}")
    finally:
        conn.close()

def get_apod_by_date(date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apod WHERE date = ?", (date,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_apods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apod ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_favourite(apod_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if already in favourites
        cursor.execute("SELECT id FROM favourites WHERE apod_id = ?", (apod_id,))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return "already"
        cursor.execute("INSERT INTO favourites (apod_id) VALUES (?)", (apod_id,))
        conn.commit()
        conn.close()
        return "added"
    except Exception as e:
        print(f"Error adding favourite: {e}")
        conn.close()
        return "error"

def remove_favourite(apod_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favourites WHERE apod_id = ?", (apod_id,))
    conn.commit()
    conn.close()

def get_favourites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT apod.*, favourites.id as fav_id, favourites.saved_at
        FROM favourites
        JOIN apod ON favourites.apod_id = apod.id
        ORDER BY favourites.saved_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def is_favourite(apod_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM favourites WHERE apod_id = ?", (apod_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def save_search(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO search_log (keyword) VALUES (?)", (keyword,))
    conn.commit()
    conn.close()

def search_apods(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM apod
        WHERE title LIKE ? OR explanation LIKE ?
        ORDER BY date DESC
    """, (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM apod")
    total_apods = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM favourites")
    total_favs = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT keyword, COUNT(*) as count
        FROM search_log
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT 1
    """)
    top_search = cursor.fetchone()
    conn.close()
    return {
        "total_apods": total_apods,
        "total_favs": total_favs,
        "top_search": dict(top_search) if top_search else None
    }
