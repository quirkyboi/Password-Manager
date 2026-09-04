import sqlite3

conn = sqlite3.connect("vault.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    master_password TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    password_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    category TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

conn.commit()