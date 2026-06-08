import sqlite3


conn = sqlite3.connect("memomind.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        created_at TEXT,
        remind_at TEXT,
        notified INTEGER DEFAULT 0
    )
    """
)

cursor.execute("PRAGMA table_info(reminders)")
columns = [column[1] for column in cursor.fetchall()]

if "remind_at" not in columns:
    cursor.execute("ALTER TABLE reminders ADD COLUMN remind_at TEXT")

if "notified" not in columns:
    cursor.execute("ALTER TABLE reminders ADD COLUMN notified INTEGER DEFAULT 0")

conn.commit()
conn.close()
