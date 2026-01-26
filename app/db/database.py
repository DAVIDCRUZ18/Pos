import sqlite3
import bcrypt
from datetime import datetime
from contextlib import contextmanager

DATABASE_NAME = "pos.db"

@contextmanager
def get_db():
    """Context manager para asegurar que la conexión siempre se cierre"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def crear_tablas():
    """Crea todas las tablas con integridad referencial"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                nombre_completo TEXT,
                rol TEXT CHECK(rol IN ('admin', 'vendedor')) DEFAULT 'vendedor',
                activo INTEGER DEFAULT 1,
                fecha_creacion TEXT,
                ultimo_acceso TEXT,
                codigo_creacion TEXT UNIQUE
            )
        """)
        
        # Tabla de categorías
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT
            )
        """)
        
        # Tabla de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                documento TEXT UNIQUE,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_registro TEXT
            )
        """)

        # Tabla de proveedores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nit_rut TEXT UNIQUE,
                telefono TEXT,
                contacto TEXT,
                fecha_registro TEXT
            )
        """)
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio >= 0),
                stock INTEGER DEFAULT 0 CHECK(stock >= 0),
                codigo_barras TEXT UNIQUE,
                categoria_id INTEGER,
                costo REAL DEFAULT 0,
                min_stock INTEGER DEFAULT 5,
                proveedor_id INTEGER,
                fecha_creacion TEXT,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
            )
        """)
        
        # Tabla de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                cliente_id INTEGER,
                usuario_id INTEGER NOT NULL,
                metodo_pago TEXT DEFAULT 'efectivo',
                estado TEXT DEFAULT 'completada',
                motivo_anulacion TEXT,
                usuario_anula INTEGER,
                fecha_anulacion TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # Tabla de detalle de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        # Tabla de compras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                proveedor_id INTEGER,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # Tabla de detalle de compras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_compra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                costo_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        # Tabla de gastos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                categoria TEXT,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        
        conn.commit()
    print("[OK] Estructura de base de datos completa y optimizada")

def encriptar_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verificar_password(password_plana, password_encriptada):
    if isinstance(password_encriptada, str):
        import hashlib
        old_hash = hashlib.sha256(password_plana.encode()).hexdigest()
        return old_hash == password_encriptada
    return bcrypt.checkpw(password_plana.encode('utf-8'), password_encriptada)

def crear_usuario_admin():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
        if cursor.fetchone() is None:
            pwd = encriptar_password("admin123")
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO usuarios (usuario, password, nombre_completo, rol, fecha_creacion)
                VALUES (?, ?, ?, ?, ?)
            """, ("admin", pwd, "Administrador", "admin", fecha))
            conn.commit()
            print("[OK] Admin creado")

def validar_login(usuario, password):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, password, nombre_completo, rol, activo FROM usuarios WHERE usuario = ?", (usuario,))
        res = cursor.fetchone()
        if res and verificar_password(password, res['password']):
            if res['activo'] == 1:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?", (fecha, res['id']))
                conn.commit()
                return True, dict(res)
            return False, "Usuario inactivo"
        return False, "Credenciales incorrectas"

def inicializar_bd():
    crear_tablas()
    crear_usuario_admin()

if __name__ == "__main__":
    inicializar_bd()
