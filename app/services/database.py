import sqlite3
from datetime import datetime

DB_PATH = "coach_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table for user stats (Streaks)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id TEXT PRIMARY KEY, streak INTEGER DEFAULT 0, last_active TEXT)''')
    # Table for weekly reports
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY, user_id TEXT, date TEXT, plan TEXT)''')
    conn.commit()
    conn.close()

# THIS WAS MISSING - The function your main.py is looking for
def get_user_stats(user_id: str):
    """Retrieves the current streak for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT streak FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def update_user_streak(user_id: str):
    """Increments the streak or starts it at 1."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO users (user_id, streak, last_active) 
        VALUES (?, 1, ?) 
        ON CONFLICT(user_id) DO UPDATE SET 
        streak = streak + 1,
        last_active = ?
    """, (user_id, now, now))
    conn.commit()
    conn.close()

def log_plan_to_history(user_id: str, plan: str):
    """Saves the AI plan to the history table for weekly reporting."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, date, plan) VALUES (?, ?, ?)",
                   (user_id, datetime.now().strftime("%Y-%m-%d"), plan))
    conn.commit()
    conn.close()