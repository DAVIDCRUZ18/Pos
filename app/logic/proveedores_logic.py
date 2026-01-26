import app.db.database as db
from datetime import datetime

class ProveedoresLogic:
    
    @staticmethod
    def obtener_proveedores():
        """Obtiene todos los proveedores"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores ORDER BY nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_proveedor(nombre, nit_rut="", telefono="", contacto=""):
        """Crea un nuevo proveedor"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                cursor.execute("""
                    INSERT INTO proveedores (nombre, nit_rut, telefono, contacto, fecha_registro)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, nit_rut, telefono, contacto, fecha_actual))
                conn.commit()
                return True, "Proveedor creado exitosamente"
            except db.sqlite3.IntegrityError:
                return False, "El NIT/RUT ya está registrado"
            except Exception as e:
                return False, f"Error: {str(e)}"
    
    @staticmethod
    def actualizar_proveedor(id, datos):
        """Actualiza datos de un proveedor"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE proveedores 
                    SET nombre=?, nit_rut=?, telefono=?, contacto=?
                    WHERE id=?
                """, (
                    datos.get('nombre'), datos.get('nit_rut'), datos.get('telefono'),
                    datos.get('contacto'), id
                ))
                conn.commit()
                return True, "Proveedor actualizado"
            except db.sqlite3.IntegrityError:
                return False, "El NIT/RUT ya existe"
    
    @staticmethod
    def eliminar_proveedor(id):
        """Elimina un proveedor si no tiene productos asociados"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            # Verificar si tiene productos
            cursor.execute("SELECT COUNT(*) FROM productos WHERE proveedor_id = ?", (id,))
            if cursor.fetchone()[0] > 0:
                return False, "No se puede eliminar: el proveedor tiene productos asociados"
            
            cursor.execute("DELETE FROM proveedores WHERE id = ?", (id,))
    @staticmethod
    def buscar_proveedores(termino):
        """Busca proveedores por nombre o NIT/RUT"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM proveedores
                WHERE nombre LIKE ? OR nit_rut LIKE ?
                ORDER BY nombre
            """, (f"%{termino}%", f"%{termino}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_historial_compras(proveedor_id):
        """Obtiene el historial de compras de un proveedor"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.fecha, c.total
                FROM compras c
                WHERE c.proveedor_id = ?
                ORDER BY c.fecha DESC
            """, (proveedor_id,))
            return [dict(row) for row in cursor.fetchall()]