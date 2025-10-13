from bd import obtener_conexion
import hashlib
import pymysql

def obtener_usuario_por_id(usuario_id):
    """Obtener un usuario por su ID"""
    try:
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id_usuario, nombre, apellidos, email, tipo_usuario, estado, fecha_registro
                FROM usuarios 
                WHERE id_usuario = %s AND estado = 'activo'
            """, (usuario_id,))
            usuario = cursor.fetchone()
        conexion.close()
        return usuario
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None

def obtener_todos_usuarios():
    """Obtener todos los usuarios activos"""
    try:
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id_usuario, nombre, apellidos, email, tipo_usuario, estado, fecha_registro
                FROM usuarios 
                WHERE estado = 'activo'
                ORDER BY fecha_registro DESC
            """)
            usuarios = cursor.fetchall()
        conexion.close()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def autenticar_usuario(email, password):
    """Autenticar un usuario con email y contraseña"""
    try:
        if not email or not password:
            return False, None
            
        # Limpiar y normalizar el email
        email = email.strip().lower()
        
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            # Buscar el usuario por email
            cursor.execute("""
                SELECT id_usuario, nombre, apellidos, email, contraseña_hash, tipo_usuario, estado
                FROM usuarios 
                WHERE email = %s AND estado = 'activo'
            """, (email,))
            usuario = cursor.fetchone()
        conexion.close()
        
        if not usuario:
            print(f"Usuario no encontrado: {email}")
            return False, None
        
        # Verificar la contraseña
        # Primero intentamos con hash MD5 (método simple)
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        if usuario['contraseña_hash'] == password_hash:
            # Contraseña correcta, remover el hash antes de devolver
            del usuario['contraseña_hash']
            print(f"Login exitoso para usuario: {email}")
            return True, usuario
        else:
            # También intentar con la contraseña en texto plano por si no está hasheada
            if usuario['contraseña_hash'] == password:
                del usuario['contraseña_hash']
                print(f"Login exitoso para usuario (texto plano): {email}")
                return True, usuario
            else:
                print(f"Contraseña incorrecta para usuario: {email}")
                return False, None
                
    except Exception as e:
        print(f"Error en autenticación: {e}")
        return False, None

def crear_usuario(nombre, apellidos, email, password, tipo_usuario='estudiante'):
    """Crear un nuevo usuario"""
    try:
        print(f"DEBUG crear_usuario: nombre='{nombre}', apellidos='{apellidos}', email='{email}', password='{password}', tipo='{tipo_usuario}'")
        
        if not all([nombre, apellidos, email, password]):
            print(f"DEBUG: Campos faltantes - nombre: {bool(nombre)}, apellidos: {bool(apellidos)}, email: {bool(email)}, password: {bool(password)}")
            return False, "Todos los campos son requeridos"
        
        # Limpiar y normalizar datos
        email = email.strip().lower()
        nombre = nombre.strip()
        apellidos = apellidos.strip()
        
        # Hash de la contraseña
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Verificar si el email ya existe
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                conexion.close()
                return False, "El email ya está registrado"
            
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellidos, email, contraseña_hash, tipo_usuario, estado)
                VALUES (%s, %s, %s, %s, %s, 'activo')
            """, (nombre, apellidos, email, password_hash, tipo_usuario))
            
            conexion.commit()
            usuario_id = cursor.lastrowid
        conexion.close()
        
        print(f"Usuario creado exitosamente: {email}")
        return True, usuario_id
        
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False, str(e)

def verificar_email_disponible(email):
    """Verificar si un email está disponible para registro"""
    try:
        email = email.strip().lower()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            resultado = cursor.fetchone()
        conexion.close()
        return resultado is None
    except Exception as e:
        print(f"Error al verificar email: {e}")
        return False
