import sqlite3

DATABASE = "pocketsmart.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_expense(category, description, amount):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses(category, description, amount) VALUES (?, ?, ?)",
        (category, description, amount)
    )
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return expenses

def get_total_expenses():
    conn = get_connection()
    result = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()
    conn.close()
    return result[0]

def get_category_totals():
    conn = get_connection()
    result = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category"
    ).fetchall()
    conn.close()
    return result
