import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

DB_NAME = "spendly.db"

def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

def seed_db():
    """Inserts sample data for development if the database is empty."""
    with get_db() as conn:
        # Check if users table already contains data
        user_exists = conn.execute("SELECT 1 FROM users LIMIT 1").fetchone()
        if user_exists:
            return

        # Insert demo user
        hashed_password = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", hashed_password)
        )
        user_id = cursor.lastrowid

        # Sample expenses covering all categories
        # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
        current_month = datetime.now().strftime("%Y-%m")
        sample_expenses = [
            (user_id, 15.50, "Food", f"{current_month}-01", "Lunch at Cafe"),
            (user_id, 42.00, "Transport", f"{current_month}-02", "Weekly fuel"),
            (user_id, 120.00, "Bills", f"{current_month}-05", "Electricity bill"),
            (user_id, 30.00, "Health", f"{current_month}-08", "Pharmacy"),
            (user_id, 60.00, "Entertainment", f"{current_month}-12", "Movie ticket"),
            (user_id, 85.20, "Shopping", f"{current_month}-15", "New t-shirt"),
            (user_id, 10.00, "Other", f"{current_month}-18", "Parking fee"),
            (user_id, 25.00, "Food", f"{current_month}-20", "Dinner"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
        conn.commit()
