import app.db.database as db
from datetime import datetime

class UsuariosLogic:
    
    @staticmethod
    def obtener_usuarios():
        """Obtiene todos los usuarios sin mostrar contraseñas"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario, nombre_completo, rol, activo, fecha_creacion, ultimo_acceso
                FROM usuarios 
                ORDER BY nombre_completo
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def crear_usuario(usuario, password, rol, nombre_completo):
        """Crea un nuevo usuario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                password_encriptada = db.encriptar_password(password)
                cursor.execute("""
                    INSERT INTO usuarios (usuario, password, nombre_completo, rol, fecha_creacion)
                    VALUES (?, ?, ?, ?, ?)
                """, (usuario, password_encriptada, nombre_completo, rol, fecha_actual))
                conn.commit()
                return True, "Usuario creado exitosamente"
            except db.sqlite3.IntegrityError:
                return False, "El nombre de usuario ya existe"
    
    @staticmethod
    def actualizar_usuario(id, datos):
        """Actualiza datos de un usuario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            try:
                update_fields = []
                params = []
                
                if 'nombre_completo' in datos:
                    update_fields.append("nombre_completo = ?")
                    params.append(datos['nombre_completo'])
                
                if 'rol' in datos:
                    update_fields.append("rol = ?")
                    params.append(datos['rol'])
                
                if 'activo' in datos:
                    update_fields.append("activo = ?")
                    params.append(datos['activo'])
                
                if 'password' in datos and datos['password']:
                    update_fields.append("password = ?")
                    params.append(db.encriptar_password(datos['password']))
                
                if update_fields:
                    query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE id = ?"
                    params.append(id)
                    cursor.execute(query, params)
                    conn.commit()
                    return True, "Usuario actualizado"
                else:
                    return False, "No hay datos para actualizar"
                    
            except db.sqlite3.IntegrityError:
                return False, "Error de integridad de datos"
    
    @staticmethod
    def cambiar_password(id, password_actual, password_nueva):
        """Cambia la contraseña de un usuario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            
            # Verificar contraseña actual
            cursor.execute("SELECT password FROM usuarios WHERE id = ?", (id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return False, "Usuario no encontrado"
            
            if not db.verificar_password(password_actual, resultado['password']):
                return False, "La contraseña actual es incorrecta"
            
            # Actualizar contraseña
            password_encriptada = db.encriptar_password(password_nueva)
            cursor.execute("UPDATE usuarios SET password = ? WHERE id = ?", 
                          (password_encriptada, id))
            conn.commit()
            
            return True, "Contraseña cambiada exitosamente"
    
    @staticmethod
    def validar_credenciales(usuario, password):
        """Valida las credenciales del usuario"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, usuario, password, nombre_completo, rol, activo FROM usuarios WHERE usuario = ?", (usuario,))
            res = cursor.fetchone()
            if res and db.verificar_password(password, res['password']):
                if res['activo'] == 1:
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?", (fecha, res['id']))
                    conn.commit()
                    return True, dict(res)
                return False, "Usuario inactivo"
            return False, "Credenciales incorrectas"