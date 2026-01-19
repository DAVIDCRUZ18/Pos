import sqlite3
import hashlib
from datetime import datetime

def conectar():
    """Establece conexión con la base de datos"""
    return sqlite3.connect("pos.db")

def crear_tablas():
    """Crea todas las tablas necesarias para el sistema"""
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_completo TEXT,
            rol TEXT DEFAULT 'vendedor',
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT,
            ultimo_acceso TEXT ,
            codigo_creacion TEXT UNIQUE
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

            fecha_anulacion TEXT,
            motivo_anulacion TEXT,
            usuario_anula INTEGER,

            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
    """)
    
    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            codigo_barras TEXT UNIQUE,
            categoria TEXT,
            fecha_creacion TEXT
        )
    """)
    
    # Tabla de detalle de ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,

            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
    """)
    
    conn.commit()
    conn.close()
    print("[OK] Tablas creadas exitosamente")

def encriptar_password(password):
    """Encripta la contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def crear_usuario_admin():
    """Crea el usuario administrador por defecto si no existe"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
        if cursor.fetchone() is None:
            password_encriptada = encriptar_password("admin123")
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT INTO usuarios (usuario, password, nombre_completo, rol, fecha_creacion)
                VALUES (?, ?, ?, ?, ?)
            """, ("admin", password_encriptada, "Administrador", "admin", fecha_actual))
            
            conn.commit()
            print("[OK] Usuario administrador creado")
            print("  Usuario: admin")
            print("  Contrasena: admin123")
        else:
            print("[OK] Usuario administrador ya existe")
    except Exception as e:
        print(f"[ERROR] Error al crear usuario admin: {e}")
    finally:
        conn.close()

def registrar_usuario(usuario, password, nombre_completo, rol="vendedor"):
    """Registra un nuevo usuario en el sistema"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        password_encriptada = encriptar_password(password)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO usuarios (usuario, password, nombre_completo, rol, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario, password_encriptada, nombre_completo, rol, fecha_actual))
        
        conn.commit()
        return True, "Usuario registrado exitosamente"
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe"
    except Exception as e:
        return False, f"Error al registrar usuario: {str(e)}"
    finally:
        conn.close()

def validar_login(usuario, password):
    """Valida las credenciales del usuario"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        password_encriptada = encriptar_password(password)
        
        cursor.execute("""
            SELECT id, usuario, nombre_completo, rol, activo
            FROM usuarios
            WHERE usuario = ? AND password = ?
        """, (usuario, password_encriptada))
        
        resultado = cursor.fetchone()
        
        if resultado:
            if resultado[4] == 1:  # Verificar si está activo
                # Actualizar último acceso
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?
                """, (fecha_actual, resultado[0]))
                conn.commit()
                
                return True, {
                    "id": resultado[0],
                    "usuario": resultado[1],
                    "nombre_completo": resultado[2],
                    "rol": resultado[3]
                }
            else:
                return False, "Usuario inactivo. Contacte al administrador"
        else:
            return False, "Usuario o contraseña incorrectos"
    except Exception as e:
        return False, f"Error en el login: {str(e)}"
    finally:
        conn.close()

def obtener_datos_usuario(usuario_id):
    """Obtiene los datos completos de un usuario"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, usuario, nombre_completo, rol, activo, fecha_creacion, ultimo_acceso , codigo_creacion
            FROM usuarios WHERE id = ?
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        if resultado:
            return {
                "id": resultado[0],
                "usuario": resultado[1],
                "nombre_completo": resultado[2],
                "rol": resultado[3],
                "activo": resultado[4],
                "fecha_creacion": resultado[5],
                "ultimo_acceso": resultado[6],
                "codigo_creacion" : resultado[8]
            }
        return None
    finally:
        conn.close()

def listar_usuarios():
    """Lista todos los usuarios del sistema"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, usuario, nombre_completo, rol, activo, fecha_creacion, ultimo_acceso , codigo_creacion
            FROM usuarios ORDER BY id
        """)
        
        usuarios = []
        for row in cursor.fetchall():
            usuarios.append({
                "id": row[0],
                "usuario": row[1],
                "nombre_completo": row[2],
                "rol": row[3],
                "activo": row[4],
                "fecha_creacion": row[5],
                "ultimo_acceso": row[6] ,
                "codigo_creacion": row[7]
            })
        return usuarios
    finally:
        conn.close()

def crear_datos_prueba():
    """Crea datos de prueba para el sistema"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # Verificar si ya hay productos
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            productos_prueba = [
                ("Coca Cola 600ml", 2500, 50, "7501234567890", "Bebidas"),
                ("Pan Integral", 3500, 30, "7501234567891", "Panadería"),
                ("Leche Entera 1L", 4200, 40, "7501234567892", "Lácteos"),
                ("Arroz 500g", 2800, 60, "7501234567893", "Granos"),
                ("Aceite Vegetal 1L", 8500, 25, "7501234567894", "Aceites")
            ]
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for producto in productos_prueba:
                cursor.execute("""
                    INSERT INTO productos (nombre, precio, stock, codigo_barras, categoria, fecha_creacion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (*producto, fecha_actual))
            
            conn.commit()
            print("[OK] Datos de prueba creados exitosamente")
        else:
            print("[OK] Ya existen productos en la base de datos")
    except Exception as e:
        print(f"[ERROR] Error al crear datos de prueba: {e}")
    finally:
        conn.close()

# Inicializar base de datos
def inicializar_bd():
    """Inicializa la base de datos con todas las configuraciones necesarias"""
    print("=== Inicializando Base de Datos ===")
    crear_tablas()
    crear_usuario_admin()
    crear_datos_prueba()
    print("=== Base de datos lista ===\n")

if __name__ == "__main__":
    # Ejecutar cuando se corra directamente este archivo
    inicializar_bd()