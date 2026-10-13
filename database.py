import sqlite3

def connect_db():
    conn = sqlite3.connect("campus_bridge.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            category TEXT NOT NULL,
            details TEXT NOT NULL,
            status TEXT DEFAULT 'Pending HOD Review',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def save_concern(name, department, category, details):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO concerns (name, department, category, details)
        VALUES (?, ?, ?, ?)
    ''', (name, department, category, details))
    concern_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return concern_id

# NAYA FUNCTION: Data fetch karne ke liye
def get_all_concerns():
    conn = connect_db()
    cursor = conn.cursor()
    # Pura data layega, sabse nayi complaint sabse upar (DESC)
    cursor.execute("SELECT * FROM concerns ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
def update_status(concern_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE concerns SET status = ? WHERE id = ?", (new_status, concern_id))
    conn.commit()
    conn.close()
    # NAYA FUNCTION: Single complaint track karne ke liye
def get_concern_by_id(concern_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concerns WHERE id = ?", (concern_id,))
    row = cursor.fetchone()
    conn.close()
    return row