import sqlite3
from datetime import datetime


DB_FILE = "assistant.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            message_id TEXT PRIMARY KEY,
            thread_id TEXT,
            sender TEXT,
            subject TEXT,
            classification TEXT,
            draft_id TEXT,
            processed_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def is_processed(message_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM processed_emails
        WHERE message_id = ?
    """, (message_id,))

    result = cursor.fetchone()

    conn.close()

    return result is not None


def mark_processed(
    message_id,
    thread_id,
    sender,
    subject,
    classification,
    draft_id=None
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO processed_emails
        (
            message_id,
            thread_id,
            sender,
            subject,
            classification,
            draft_id,
            processed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        message_id,
        thread_id,
        sender,
        subject,
        classification,
        draft_id,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def get_processsed_emails():
    conn = get_connection()
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM processed_emails
    """)
    
    result = cursor.fetchall()
    
    conn.close()
    
    return result

if __name__ == "__main__":

    initialize_database()

    print("Database initialized successfully.")