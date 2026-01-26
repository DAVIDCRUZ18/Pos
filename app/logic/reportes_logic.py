import app.db.database as db
from datetime import datetime

class ReportesLogic:
    
    @staticmethod
    def reporte_ventas_periodo(fecha_inicio, fecha_fin):
        """Reporte de ventas en período específico"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, c.nombre as cliente_nombre, 
                       u.nombre_completo as usuario_nombre, v.metodo_pago
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN usuarios u ON v.usuario_id = u.id
                WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 'completada'
                ORDER BY v.fecha DESC
            """, (fecha_inicio, fecha_fin))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def reporte_productos_mas_vendidos(limite=10):
        """Productos más vendidos"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nombre, SUM(dv.cantidad) as total_vendido, 
                       SUM(dv.subtotal) as total_recaudado
                FROM productos p
                JOIN detalle_venta dv ON p.id = dv.producto_id
                JOIN ventas v ON dv.venta_id = v.id
                WHERE v.estado = 'completada'
                AND strftime('%Y-%m', v.fecha) = strftime('%Y-%m', 'now')
                GROUP BY p.id, p.nombre
                ORDER BY total_vendido DESC
                LIMIT ?
            """, (limite,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def reporte_inventario_valorizado():
        """Reporte de inventario valorizado"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*, c.nombre as categoria_nombre,
                       (p.stock * p.costo) as valor_costo,
                       (p.stock * p.precio) as valor_venta
                FROM productos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.nombre
            """)
            productos = [dict(row) for row in cursor.fetchall()]
            
            total_costo = sum(p['valor_costo'] for p in productos)
            total_venta = sum(p['valor_venta'] for p in productos)
            
            return {
                'productos': productos,
                'totales': {
                    'valor_costo_total': total_costo,
                    'valor_venta_total': total_venta,
                    'utilidad_potencial': total_venta - total_costo
                }
            }
    
    @staticmethod
    def reporte_clientes_frecuentes():
        """Clientes más frecuentes"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.nombre, COUNT(v.id) as total_compras, 
                       COALESCE(SUM(v.total), 0) as total_gastado
                FROM clientes c
                LEFT JOIN ventas v ON c.id = v.cliente_id
                WHERE v.estado = 'completada'
                GROUP BY c.id, c.nombre
                HAVING total_compras > 0
                ORDER BY total_compras DESC
                LIMIT 10
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def reporte_general_negocio():
        """Reporte general del negocio"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            
            # Ventas mes actual
            cursor.execute("""
                SELECT COUNT(*) as total_ventas, COALESCE(SUM(total), 0) as monto_ventas
                FROM ventas 
                WHERE estado = 'completada' 
                AND strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            """)
            ventas_mes = dict(cursor.fetchone())
            
            # Compras mes actual
            cursor.execute("""
                SELECT COUNT(*) as total_compras, COALESCE(SUM(total), 0) as monto_compras
                FROM compras 
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            """)
            compras_mes = dict(cursor.fetchone())
            
            # Gastos mes actual
            cursor.execute("""
                SELECT COUNT(*) as total_gastos, COALESCE(SUM(monto), 0) as monto_gastos
                FROM gastos 
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            """)
            gastos_mes = dict(cursor.fetchone())
            
            # Total productos
            cursor.execute("SELECT COUNT(*) as total_productos FROM productos")
            total_productos = cursor.fetchone()[0]
            
            # Productos bajo stock
            cursor.execute("""
                SELECT COUNT(*) as bajo_stock
                FROM productos 
                WHERE stock <= min_stock
            """)
            bajo_stock = cursor.fetchone()[0]
            
            return {
                'resumen_mes': {
                    'ventas': ventas_mes,
                    'compras': compras_mes,
                    'gastos': gastos_mes,
                    'utilidad_operativa': ventas_mes['monto_ventas'] - gastos_mes['monto_gastos']
                },
                'inventario': {
                    'total_productos': total_productos,
                    'productos_bajo_stock': bajo_stock,
                    'stock_critico': bajo_stock > 0
                }
            }