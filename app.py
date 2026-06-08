import sqlite3
from datetime import datetime, timedelta

import ollama
import streamlit as st

try:
    from plyer import notification
except ImportError:
    notification = None

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


conn = sqlite3.connect("memomind.db", check_same_thread=False)
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


def send_notification(message):
    if notification is None:
        return

    notification.notify(
        title="MemoMind AI",
        message=message,
        app_name="MemoMind AI",
        timeout=10,
    )


def notify_due_reminders():
    now = datetime.now().isoformat(timespec="minutes")

    cursor.execute(
        """
        SELECT id, message, remind_at
        FROM reminders
        WHERE remind_at IS NOT NULL
          AND remind_at <= ?
          AND COALESCE(notified, 0) = 0
        ORDER BY remind_at ASC
        """,
        (now,),
    )

    due_reminders = cursor.fetchall()

    for reminder_id, message, remind_at in due_reminders:
        send_notification(message)
        cursor.execute(
            "UPDATE reminders SET notified = 1 WHERE id = ?",
            (reminder_id,),
        )
        st.warning(f"Lembrete: {message} ({remind_at})")

    if due_reminders:
        conn.commit()


if st_autorefresh is not None:
    st_autorefresh(interval=30000, key="reminder_checker")

notify_due_reminders()

st.title("MemoMind AI")
st.subheader("IA de lembretes e anotações")

user_input = st.text_input("Digite seu lembrete")
reminder_date = st.date_input("Data do lembrete")
default_reminder_time = (datetime.now() + timedelta(minutes=5)).time().replace(
    second=0,
    microsecond=0,
)
reminder_time = st.time_input("Hora do lembrete", value=default_reminder_time)

if st.button("Enviar"):
    if not user_input.strip():
        st.error("Digite uma mensagem para salvar o lembrete.")
    else:
        remind_at = datetime.combine(reminder_date, reminder_time)

        try:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )
            answer = response["message"]["content"]
        except Exception:
            answer = "Lembrete salvo. A resposta da IA não está disponível agora."

        cursor.execute(
            """
            INSERT INTO reminders (message, created_at, remind_at, notified)
            VALUES (?, ?, ?, 0)
            """,
            (
                user_input,
                datetime.now().isoformat(timespec="seconds"),
                remind_at.isoformat(timespec="minutes"),
            ),
        )

        conn.commit()

        st.success(answer)
        notify_due_reminders()

        if notification is None:
            st.info(
                "Para notificações no Windows, instale as dependências atualizadas do projeto."
            )

st.subheader("Histórico")

cursor.execute(
    """
    SELECT id, message, created_at, remind_at, COALESCE(notified, 0)
    FROM reminders
    ORDER BY id DESC
    """
)
rows = cursor.fetchall()

for row in rows:
    status = "notificado" if row[4] else "pendente"
    remind_at = row[3] or "sem horário"
    st.write(f"{row[1]} | lembrete: {remind_at} | {status}")
