import sqlite3

def conectar():
    return sqlite3.connect("pos.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()
