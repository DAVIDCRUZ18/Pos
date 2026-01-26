import app.db.database as db
from datetime import datetime

class CategoriasLogic:
    
    @staticmethod
    def obtener_todas_categorias():
        """Obtiene todas las categorías"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categorias ORDER BY nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_categoria(nombre, descripcion=""):
        """Crea una nueva categoría"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO categorias (nombre, descripcion)
                    VALUES (?, ?)
                """, (nombre, descripcion))
                conn.commit()
                return True, "Categoría creada exitosamente"
            except db.sqlite3.IntegrityError:
                return False, "La categoría ya existe"
            except Exception as e:
                return False, f"Error: {str(e)}"
    
    @staticmethod
    def actualizar_categoria(id, nombre, descripcion=""):
        """Actualiza una categoría existente"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ?
                """, (nombre, descripcion, id))
                conn.commit()
                return True, "Categoría actualizada"
            except db.sqlite3.IntegrityError:
                return False, "El nombre ya existe"
    
    @staticmethod
    def eliminar_categoria(id):
        """Elimina una categoría"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            # Verificar si hay productos asociados
            cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (id,))
            if cursor.fetchone()[0] > 0:
                return False, "No se puede eliminar: hay productos asociados"
            
            cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
            conn.commit()
            return True, "Categoría eliminada"
    
    @staticmethod
    def obtener_categoria_por_id(id):
        """Obtiene una categoría por ID"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
            row = cursor.fetchone()
            return dict(row) if row else None