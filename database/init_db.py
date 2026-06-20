import sqlite3

conn = sqlite3.connect("lumina.db")

cursor = conn.cursor()

# =========================
# USERS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# =========================
# STUDY STATS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    xp INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    last_active_date TEXT
)
""")

# =========================
# QUIZ HISTORY
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    topic TEXT,
    score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database created successfully!")