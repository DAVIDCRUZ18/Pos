# app/logic/ventas_logic.py
import app.db.database as db
from datetime import datetime

class VentasLogic:
    """Clase para manejar la lógica de ventas"""
    
    @staticmethod
    def obtener_todas_ventas():
        """Obtiene todas las ventas de la base de datos"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, v.fecha, v.total, v.cliente_id, 
                       COALESCE(c.nombre, 'Consumidor Final') as cliente_nombre, v.estado
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.fecha DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_venta_por_id(venta_id):
        """Obtiene una venta específica por ID"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, COALESCE(c.nombre, 'Consumidor Final') as cliente_nombre, c.documento
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?
            """, (venta_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def obtener_detalle_venta(venta_id):
        """Obtiene el detalle de productos de una venta"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dv.*, p.nombre as producto_nombre, p.codigo_barras
                FROM detalle_venta dv
                JOIN productos p ON dv.producto_id = p.id
                WHERE dv.venta_id = ?
            """, (venta_id,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def crear_venta(cliente_id, productos, usuario_id, metodo_pago="efectivo"):
        """Crea una nueva venta con transacción"""
        if not productos:
            return {'exito': False, 'mensaje': 'No hay productos en la venta'}
        
        total = sum(p['subtotal'] for p in productos)
        
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()
                
                # Insertar venta
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO ventas (fecha, total, cliente_id, usuario_id, metodo_pago, estado)
                    VALUES (?, ?, ?, ?, ?, 'completada')
                """, (fecha, total, cliente_id, usuario_id, metodo_pago))
                
                venta_id = cursor.lastrowid
                
                # Insertar detalles y actualizar stock
                for p in productos:
                    cursor.execute("""
                        INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (venta_id, p['producto_id'], p['cantidad'], p['precio'], p['subtotal']))
                    
                    # Descontar stock
                    cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (p['cantidad'], p['producto_id']))
                
                conn.commit()
                return {'exito': True, 'mensaje': 'Venta exitosa', 'venta_id': venta_id}
        except Exception as e:
            return {'exito': False, 'mensaje': f'Error en base de datos: {str(e)}'}

    @staticmethod
    def anular_venta(venta_id, usuario_id, motivo=""):
        """Anula venta y devuelve stock"""
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()
                
                # Obtener detalles para devolver stock
                cursor.execute("SELECT producto_id, cantidad FROM detalle_venta WHERE venta_id = ?", (venta_id,))
                detalles = cursor.fetchall()
                
                for d in detalles:
                    cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (d['cantidad'], d['producto_id']))
                
                # Actualizar estado
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    UPDATE ventas 
                    SET estado = 'anulada', motivo_anulacion = ?, usuario_anula = ?, fecha_anulacion = ?
                    WHERE id = ?
                """, (motivo, usuario_id, fecha, venta_id))
                
                conn.commit()
                return {'exito': True, 'mensaje': 'Venta anulada'}
        except Exception as e:
            return {'exito': False, 'mensaje': str(e)}
