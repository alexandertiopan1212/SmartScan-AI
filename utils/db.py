import sqlite3
from datetime import datetime

DB_PATH = "data/matching_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            invoice_file TEXT,
            po_file TEXT,
            match_status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_log(invoice_file, po_file, status, notes=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs (timestamp, invoice_file, po_file, match_status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), invoice_file, po_file, status, notes))
    conn.commit()
    conn.close()

def get_logs(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = c.fetchall()
    conn.close()
    return logs
