import sqlite3

conn = sqlite3.connect('memomind.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    created_at TEXT
)
''')

conn.commit()
conn.close()
