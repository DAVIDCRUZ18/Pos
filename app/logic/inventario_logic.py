import app.db.database as db
from datetime import datetime

class InventarioLogic:
    
    @staticmethod
    def obtener_productos():
        """Obtiene todos los productos del inventario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_producto(codigo, nombre, categoria, precio, costo, stock, min_stock, proveedor):
        """Crea un nuevo producto en el inventario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO productos (nombre, precio, stock, codigo_barras, categoria, costo, min_stock, proveedor, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, precio, stock, codigo, categoria, costo, min_stock, proveedor, fecha_actual))
            conn.commit()
    
    @staticmethod
    def actualizar_producto(id, datos):
        """Actualiza un producto existente"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos
                SET nombre=?, codigo_barras=?, precio=?, costo=?, stock=?, min_stock=?, categoria=?, proveedor=?
                WHERE id=?
            """, (
                datos.get('nombre'),
                datos.get('codigo'),
                datos.get('precio'),
                datos.get('costo', 0),
                datos.get('stock'),
                datos.get('min_stock', 5),
                datos.get('categoria'),
                datos.get('proveedor', 'N/A'),
                id
            ))
            conn.commit()
    
    @staticmethod
    def eliminar_producto(id):
        """Elimina un producto del inventario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id=?", (id,))
            conn.commit()
    
    @staticmethod
    def buscar_productos(termino):
        """Busca productos por nombre o código"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM productos
                WHERE nombre LIKE ? OR codigo_barras LIKE ?
                ORDER BY nombre
            """, (f"%{termino}%", f"%{termino}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def productos_bajo_stock(minimo=None):
        """Obtiene productos con stock bajo"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            if minimo is not None:
                cursor.execute("SELECT * FROM productos WHERE stock <= ?", (minimo,))
            else:
                cursor.execute("SELECT * FROM productos WHERE stock <= min_stock")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def ajustar_stock(producto_id, cantidad, tipo='entrada'):
        """Ajusta el stock de un producto"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            if tipo == 'entrada':
                cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, producto_id))
            elif tipo == 'salida':
                cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
                row = cursor.fetchone()
                if row and row['stock'] >= cantidad:
                    cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
                else:
                    raise ValueError("Stock insuficiente")
            conn.commit()
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtiene un producto específico por su ID"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def obtener_producto_por_codigo(codigo):
        """Obtiene un producto por su código de barras"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo_barras = ?", (codigo,))
            row = cursor.fetchone()
            return dict(row) if row else None
