import app.db.database as db
from datetime import datetime

class ClientesLogic:
    
    @staticmethod
    def obtener_clientes():
        """Obtiene todos los clientes"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes ORDER BY nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_cliente(nombre, documento="", telefono="", email="", direccion=""):
        """Crea un nuevo cliente"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                cursor.execute("""
                    INSERT INTO clientes (nombre, documento, telefono, email, direccion, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombre, documento, telefono, email, direccion, fecha_actual))
                conn.commit()
                return True, "Cliente creado exitosamente"
            except db.sqlite3.IntegrityError:
                return False, "El documento ya está registrado"
            except Exception as e:
                return False, f"Error: {str(e)}"
    
    @staticmethod
    def actualizar_cliente(id, datos):
        """Actualiza datos de un cliente"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE clientes 
                    SET nombre=?, documento=?, telefono=?, email=?, direccion=?
                    WHERE id=?
                """, (
                    datos.get('nombre'), datos.get('documento'), datos.get('telefono'),
                    datos.get('email'), datos.get('direccion'), id
                ))
                conn.commit()
                return True, "Cliente actualizado"
            except db.sqlite3.IntegrityError:
                return False, "El documento ya existe"
    
    @staticmethod
    def eliminar_cliente(id):
        """Elimina un cliente si no tiene ventas asociadas"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            # Verificar si tiene ventas
            cursor.execute("SELECT COUNT(*) FROM ventas WHERE cliente_id = ?", (id,))
            if cursor.fetchone()[0] > 0:
                return False, "No se puede eliminar: el cliente tiene ventas registradas"
            
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
            conn.commit()
            return True, "Cliente eliminado"
    
    @staticmethod
    def buscar_cliente(termino):
        """Busca clientes por nombre o documento"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM clientes
                WHERE nombre LIKE ? OR documento LIKE ?
                ORDER BY nombre
            """, (f"%{termino}%", f"%{termino}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_historial_compras(cliente_id):
        """Obtiene el historial de compras de un cliente"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, v.estado, v.metodo_pago
                FROM ventas v
                WHERE v.cliente_id = ?
                ORDER BY v.fecha DESC
            """, (cliente_id,))
            return [dict(row) for row in cursor.fetchall()]