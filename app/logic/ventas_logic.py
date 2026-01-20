# app/logic/ventas_logic.py
"""
Lógica de negocio para el módulo de Ventas
Aquí va toda la lógica sin código de interfaz
"""
import app.db.database as db
from datetime import datetime
from decimal import Decimal

class VentasLogic:
    """Clase para manejar la lógica de ventas"""
    
    @staticmethod
    def obtener_todas_ventas():
        """Obtiene todas las ventas de la base de datos"""
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, v.cliente_id, 
                       c.nombre as cliente_nombre, v.estado
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.fecha DESC
            """)
            ventas = cursor.fetchall()
            conn.close()
            return ventas
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            return []
    
    @staticmethod
    def obtener_venta_por_id(venta_id):
        """Obtiene una venta específica por ID"""
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, c.nombre as cliente_nombre, c.documento
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?
            """, (venta_id,))
            venta = cursor.fetchone()
            conn.close()
            return venta
        except Exception as e:
            print(f"Error al obtener venta: {e}")
            return None
    
    @staticmethod
    def obtener_detalle_venta(venta_id):
        """Obtiene el detalle de productos de una venta"""
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            
            # CAMBIO: detalle_ventas → detalle_venta
            cursor.execute("""
                SELECT dv.id, dv.venta_id, dv.cantidad, dv.precio_unitario,
                    dv.subtotal, p.nombre as producto_nombre, p.codigo_barras
                FROM detalle_venta dv
                JOIN productos p ON dv.producto_id = p.id
                WHERE dv.venta_id = ?
            """, (venta_id,))
            
            detalle = cursor.fetchall()
            conn.close()
            
            print(f"✅ Detalle venta {venta_id}: {len(detalle)} productos encontrados")  # DEBUG
            
            return detalle
            
        except Exception as e:
            print(f"❌ Error al obtener detalle: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def obtener_venta_por_id(venta_id):
        """Obtiene una venta específica por ID"""
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, v.cliente_id, v.metodo_pago,
                    COALESCE(c.nombre, 'Consumidor Final') as cliente_nombre,
                    c.documento
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?
            """, (venta_id,))
            
            venta = cursor.fetchone()
            conn.close()
            
            print(f"✅ Venta {venta_id} encontrada: {venta}")  # DEBUG
            
            return venta
            
        except Exception as e:
            print(f"❌ Error al obtener venta: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def crear_venta(cliente_id, productos, usuario_id, metodo_pago="efectivo"):
        """
        Crea una nueva venta
        
        Args:
            cliente_id: ID del cliente (puede ser None)
            productos: Lista de diccionarios [{producto_id, cantidad, precio, subtotal}, ...]
            usuario_id: ID del usuario que realiza la venta
            metodo_pago: Método de pago (efectivo, tarjeta, etc)
        
        Returns:
            dict: {'exito': bool, 'mensaje': str, 'venta_id': int}
        """
        try:
            # Validar que hay productos
            if not productos or len(productos) == 0:
                return {'exito': False, 'mensaje': 'No hay productos en la venta'}
            
            # Calcular total
            total = sum(p['subtotal'] for p in productos)
            
            # Iniciar transacción
            conn = db.conectar()
            cursor = conn.cursor()
            
            # Insertar venta
            cursor.execute("""
                INSERT INTO ventas (fecha, total, cliente_id, usuario_id, metodo_pago, estado)
                VALUES (?, ?, ?, ?, ?, 'completada')
            """, (datetime.now(), total, cliente_id, usuario_id, metodo_pago))
            
            venta_id = cursor.lastrowid
            
            # Insertar detalle de venta y actualizar inventario
            for producto in productos:
                # Insertar detalle
                cursor.execute("""
                    INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (venta_id, producto['producto_id'], producto['cantidad'], 
                      producto['precio'], producto['subtotal']))
                
                # Actualizar stock
                cursor.execute("""
                    UPDATE productos 
                    SET stock = stock - ?
                    WHERE id = ?
                """, (producto['cantidad'], producto['producto_id']))
            
            conn.commit()
            conn.close()
            
            return {
                'exito': True, 
                'mensaje': 'Venta registrada exitosamente',
                'venta_id': venta_id
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return {'exito': False, 'mensaje': f'Error al crear venta: {str(e)}'}
    
    @staticmethod
    def anular_venta(venta_id, usuario_id, motivo=""):
        """
        Anula una venta y devuelve stock
        
        Args:
            venta_id: ID de la venta a anular
            usuario_id: ID del usuario que anula
            motivo: Motivo de anulación
        
        Returns:
            dict: {'exito': bool, 'mensaje': str}
        """
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            
            # Verificar que la venta existe y no está anulada
            cursor.execute("SELECT estado FROM ventas WHERE id = ?", (venta_id,))
            venta = cursor.fetchone()
            
            if not venta:
                return {'exito': False, 'mensaje': 'Venta no encontrada'}
            
            if venta[0] == 'anulada':
                return {'exito': False, 'mensaje': 'La venta ya está anulada'}
            
            # Obtener detalle para devolver stock
            cursor.execute("""
                SELECT producto_id, cantidad 
                FROM detalle_venta 
                WHERE venta_id = ?
            """, (venta_id,))
            detalles = cursor.fetchall()
            
            # Devolver stock
            for detalle in detalles:
                cursor.execute("""
                    UPDATE productos 
                    SET stock = stock + ?
                    WHERE id = ?
                """, (detalle[1], detalle[0]))
            
            # Actualizar estado de venta
            cursor.execute("""
                UPDATE ventas 
                SET estado = 'anulada', 
                    motivo_anulacion = ?,
                    usuario_anula = ?,
                    fecha_anulacion = ?
                WHERE id = ?
            """, (motivo, usuario_id, datetime.now(), venta_id))
            
            conn.commit()
            conn.close()
            
            return {'exito': True, 'mensaje': 'Venta anulada exitosamente'}
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            return {'exito': False, 'mensaje': f'Error al anular venta: {str(e)}'}
    
    @staticmethod
    def obtener_ventas_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene ventas en un rango de fechas"""
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, c.nombre as cliente, v.estado
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE DATE(v.fecha) BETWEEN ? AND ?
                ORDER BY v.fecha DESC
            """, (fecha_inicio, fecha_fin))
            ventas = cursor.fetchall()
            conn.close()
            return ventas
        except Exception as e:
            print(f"Error al obtener ventas por fecha: {e}")
            return []
    
    @staticmethod
    def obtener_estadisticas_ventas(fecha_inicio=None, fecha_fin=None):
        """
        Obtiene estadísticas de ventas
        
        Returns:
            dict: Diccionario con estadísticas
        """
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            
            # Base query
            where_clause = "WHERE estado = 'completada'"
            params = []
            
            if fecha_inicio and fecha_fin:
                where_clause += " AND DATE(fecha) BETWEEN ? AND ?"
                params = [fecha_inicio, fecha_fin]
            
            # Total ventas
            cursor.execute(f"""
                SELECT COUNT(*), COALESCE(SUM(total), 0)
                FROM ventas {where_clause}
            """, params)
            total_ventas, monto_total = cursor.fetchone()
            
            # Promedio por venta
            promedio = monto_total / total_ventas if total_ventas > 0 else 0
            
            # Producto más vendido
            cursor.execute(f"""
                SELECT p.nombre, SUM(dv.cantidad) as total_cantidad
                FROM detalle_venta dv
                JOIN productos p ON dv.producto_id = p.id
                JOIN ventas v ON dv.venta_id = v.id
                {where_clause}
                GROUP BY p.id, p.nombre
                ORDER BY total_cantidad DESC
                LIMIT 1
            """, params)
            producto_top = cursor.fetchone()
            
            conn.close()
            
            return {
                'total_ventas': total_ventas,
                'monto_total': monto_total,
                'promedio_venta': promedio,
                'producto_mas_vendido': producto_top[0] if producto_top else "N/A",
                'cantidad_vendida': producto_top[1] if producto_top else 0
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_ventas': 0,
                'monto_total': 0,
                'promedio_venta': 0,
                'producto_mas_vendido': "N/A",
                'cantidad_vendida': 0
            }
    
    @staticmethod
    def validar_stock_disponible(producto_id, cantidad_solicitada):
        """
        Valida si hay stock disponible para un producto
        
        Returns:
            dict: {'disponible': bool, 'stock_actual': int, 'mensaje': str}
        """
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                return {
                    'disponible': False,
                    'stock_actual': 0,
                    'mensaje': 'Producto no encontrado'
                }
            
            stock_actual = resultado[0]
            
            if stock_actual >= cantidad_solicitada:
                return {
                    'disponible': True,
                    'stock_actual': stock_actual,
                    'mensaje': 'Stock disponible'
                }
            else:
                return {
                    'disponible': False,
                    'stock_actual': stock_actual,
                    'mensaje': f'Stock insuficiente. Disponible: {stock_actual}'
                }
                
        except Exception as e:
            return {
                'disponible': False,
                'stock_actual': 0,
                'mensaje': f'Error al validar stock: {str(e)}'
            }