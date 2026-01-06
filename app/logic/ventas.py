from app.db.database import conectar
from datetime import datetime

def registrar_venta(total):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ventas (total, fecha) VALUES (?, ?)",
        (total, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
