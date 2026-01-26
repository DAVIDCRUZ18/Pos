import app.db.database as db
from datetime import datetime

class ComprasLogic:
    
    @staticmethod
    def obtener_todas_compras():
        """Obtiene todas las compras"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, p.nombre as proveedor_nombre, u.nombre_completo as usuario_nombre
                FROM compras c
                LEFT JOIN proveedores p ON c.proveedor_id = p.id
                LEFT JOIN usuarios u ON c.usuario_id = u.id
                ORDER BY c.fecha DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_compra(proveedor_id, productos, usuario_id):
        """
        Crea una nueva compra
        productos: [{producto_id, cantidad, costo_unitario, subtotal}, ...]
        """
        if not productos:
            return {'exito': False, 'mensaje': 'No hay productos en la compra'}
        
        total = sum(p['subtotal'] for p in productos)
        
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()
                
                # Insertar compra
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO compras (fecha, total, proveedor_id, usuario_id)
                    VALUES (?, ?, ?, ?)
                """, (fecha, total, proveedor_id, usuario_id))
                
                compra_id = cursor.lastrowid
                
                # Insertar detalles y actualizar stock
                for p in productos:
                    cursor.execute("""
                        INSERT INTO detalle_compra (compra_id, producto_id, cantidad, costo_unitario, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (compra_id, p['producto_id'], p['cantidad'], p['costo_unitario'], p['subtotal']))
                    
                    # Actualizar stock y costo
                    cursor.execute("""
                        UPDATE productos 
                        SET stock = stock + ?, costo = ?
                        WHERE id = ?
                    """, (p['cantidad'], p['costo_unitario'], p['producto_id']))
                
                conn.commit()
                return {'exito': True, 'mensaje': 'Compra registrada', 'compra_id': compra_id}
        except Exception as e:
            return {'exito': False, 'mensaje': f'Error: {str(e)}'}
    
    @staticmethod
    def obtener_compra_por_id(compra_id):
        """Obtiene una compra con sus detalles"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            
            # Obtener compra
            cursor.execute("""
                SELECT c.*, p.nombre as proveedor_nombre
                FROM compras c
                LEFT JOIN proveedores p ON c.proveedor_id = p.id
                WHERE c.id = ?
            """, (compra_id,))
            compra = cursor.fetchone()
            
            if not compra:
                return None
            
            # Obtener detalles
            cursor.execute("""
                SELECT dc.*, prod.nombre as producto_nombre
                FROM detalle_compra dc
                LEFT JOIN productos prod ON dc.producto_id = prod.id
                WHERE dc.compra_id = ?
            """, (compra_id,))
            detalles = cursor.fetchall()
            
            result = dict(compra)
            result['detalles'] = [dict(row) for row in detalles]
            return result