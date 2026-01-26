import app.db.database as db
from datetime import datetime

class GastosLogic:
    
    @staticmethod
    def obtener_gastos():
        """Obtiene todos los gastos"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT g.*, u.nombre_completo as usuario_nombre
                FROM gastos g
                LEFT JOIN usuarios u ON g.usuario_id = u.id
                ORDER BY g.fecha DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_gasto(descripcion, monto, categoria="", usuario_id=None):
        """Crea un nuevo gasto"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO gastos (fecha, descripcion, monto, categoria, usuario_id)
                VALUES (?, ?, ?, ?, ?)
            """, (fecha_actual, descripcion, monto, categoria, usuario_id))
            conn.commit()
    
    @staticmethod
    def actualizar_gasto(id, datos):
        """Actualiza un gasto"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE gastos 
                SET descripcion=?, monto=?, categoria=?
                WHERE id=?
            """, (datos.get('descripcion'), datos.get('monto'), datos.get('categoria'), id))
            conn.commit()
    
    @staticmethod
    def eliminar_gasto(id):
        """Elimina un gasto"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))
            conn.commit()
    
    @staticmethod
    def obtener_gastos_por_periodo(fecha_inicio, fecha_fin):
        """Obtiene gastos en un rango de fechas"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT g.*, u.nombre_completo as usuario_nombre
                FROM gastos g
                LEFT JOIN usuarios u ON g.usuario_id = u.id
                WHERE DATE(g.fecha) BETWEEN ? AND ?
                ORDER BY g.fecha DESC
            """, (fecha_inicio, fecha_fin))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_estadisticas_gastos():
        """Obtiene estadísticas generales de gastos"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            
            # Total del mes
            cursor.execute("""
                SELECT SUM(monto) as total_mes, COUNT(*) as cantidad_mes
                FROM gastos 
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            """)
            mes_stats = cursor.fetchone()
            
            # Totales por categoría
            cursor.execute("""
                SELECT categoria, SUM(monto) as total
                FROM gastos
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
                GROUP BY categoria
                ORDER BY total DESC
            """)
            por_categoria = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total_mes': mes_stats['total_mes'] or 0,
                'cantidad_mes': mes_stats['cantidad_mes'] or 0,
                'por_categoria': por_categoria
            }