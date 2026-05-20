import streamlit as st
import ollama
import sqlite3
from datetime import datetime

conn = sqlite3.connect('memomind.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    created_at TEXT
)
''')

conn.commit()

st.title("MemoMind AI")
st.subheader("IA de lembretes e anotações")

user_input = st.text_input("Digite sua mensagem")

if st.button("Enviar"):

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': user_input
            }
        ]
    )

    answer = response['message']['content']

    cursor.execute(
        "INSERT INTO reminders (message, created_at) VALUES (?, ?)",
        (user_input, str(datetime.now()))
    )

    conn.commit()

    st.success(answer)

st.subheader("Histórico")

cursor.execute("SELECT * FROM reminders ORDER BY id DESC")
rows = cursor.fetchall()

for row in rows:
    st.write(f"{row[1]} - {row[2]}")
