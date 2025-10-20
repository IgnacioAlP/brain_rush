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
        
        # Verificar que la contraseña sea única
        if not verificar_contrasena_unica(password):
            return False, "Esta contraseña ya está siendo utilizada por otro usuario. Por favor, elige una diferente."
        
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

def verificar_contrasena_unica(password, excluir_usuario_id=None):
    """Verificar que una contraseña no esté siendo usada por otro usuario"""
    try:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            if excluir_usuario_id:
                cursor.execute(
                    "SELECT id_usuario FROM usuarios WHERE contraseña_hash = %s AND id_usuario != %s", 
                    (password_hash, excluir_usuario_id)
                )
            else:
                cursor.execute(
                    "SELECT id_usuario FROM usuarios WHERE contraseña_hash = %s", 
                    (password_hash,)
                )
            resultado = cursor.fetchone()
        conexion.close()
        return resultado is None  # True si es única, False si ya existe
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return True  # En caso de error, permitir la contraseña

def eliminar_usuario_completo(usuario_id):
    """
    Elimina un usuario y todos sus datos relacionados en cascada
    
    Para ESTUDIANTES elimina:
    - Respuestas en respuestas_estudiantes
    - Participaciones
    - Ranking
    - Recompensas otorgadas
    - Usuario_roles
    - Usuario
    
    Para DOCENTES elimina:
    - Todas las preguntas de sus cuestionarios (opciones_respuesta, cuestionario_preguntas)
    - Todos sus cuestionarios
    - Usuario_roles
    - Usuario
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtener tipo de usuario
        cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            cursor.close()
            conexion.close()
            return False, "Usuario no encontrado"
        
        tipo_usuario = resultado[0]
        print(f"DEBUG: Eliminando usuario ID {usuario_id}, tipo: {tipo_usuario}")
        
        if tipo_usuario == 'estudiante':
            # Eliminar respuestas del estudiante
            cursor.execute("""
                DELETE FROM respuestas_estudiantes 
                WHERE id_estudiante = %s
            """, (usuario_id,))
            print(f"DEBUG: Eliminadas respuestas del estudiante")
            
            # Eliminar participaciones
            cursor.execute("""
                DELETE FROM participaciones 
                WHERE id_estudiante = %s
            """, (usuario_id,))
            print(f"DEBUG: Eliminadas participaciones")
            
            # Eliminar del ranking
            cursor.execute("""
                DELETE FROM ranking 
                WHERE id_estudiante = %s
            """, (usuario_id,))
            print(f"DEBUG: Eliminado del ranking")
            
            # Eliminar recompensas otorgadas
            cursor.execute("""
                DELETE FROM recompensas_otorgadas 
                WHERE id_estudiante = %s
            """, (usuario_id,))
            print(f"DEBUG: Eliminadas recompensas otorgadas")
            
        elif tipo_usuario == 'docente':
            # Obtener IDs de todos los cuestionarios del docente
            cursor.execute("""
                SELECT id_cuestionario 
                FROM cuestionarios 
                WHERE id_docente = %s
            """, (usuario_id,))
            cuestionarios = cursor.fetchall()
            
            for cuestionario in cuestionarios:
                cuestionario_id = cuestionario[0]
                print(f"DEBUG: Eliminando cuestionario ID {cuestionario_id}")
                
                # Obtener IDs de preguntas de este cuestionario
                cursor.execute("""
                    SELECT id_pregunta 
                    FROM cuestionario_preguntas 
                    WHERE id_cuestionario = %s
                """, (cuestionario_id,))
                preguntas = cursor.fetchall()
                
                for pregunta in preguntas:
                    pregunta_id = pregunta[0]
                    
                    # Eliminar respuestas de estudiantes a esta pregunta
                    cursor.execute("""
                        DELETE FROM respuestas_estudiantes 
                        WHERE id_cuestionario_pregunta IN (
                            SELECT id_cuestionario_pregunta 
                            FROM cuestionario_preguntas 
                            WHERE id_pregunta = %s
                        )
                    """, (pregunta_id,))
                    
                    # Eliminar opciones de respuesta
                    cursor.execute("""
                        DELETE FROM opciones_respuesta 
                        WHERE id_pregunta = %s
                    """, (pregunta_id,))
                
                # Eliminar relaciones cuestionario_preguntas
                cursor.execute("""
                    DELETE FROM cuestionario_preguntas 
                    WHERE id_cuestionario = %s
                """, (cuestionario_id,))
                
                # Eliminar las preguntas del cuestionario
                cursor.execute("""
                    DELETE FROM preguntas 
                    WHERE id_pregunta IN (
                        SELECT DISTINCT cp.id_pregunta 
                        FROM (SELECT id_pregunta FROM cuestionario_preguntas WHERE id_cuestionario = %s) cp
                    )
                """, (cuestionario_id,))
                
                # Eliminar participaciones del cuestionario
                cursor.execute("""
                    DELETE FROM participaciones 
                    WHERE id_cuestionario = %s
                """, (cuestionario_id,))
                
                # Eliminar ranking del cuestionario
                cursor.execute("""
                    DELETE FROM ranking 
                    WHERE id_cuestionario = %s
                """, (cuestionario_id,))
            
            # Eliminar todos los cuestionarios del docente
            cursor.execute("""
                DELETE FROM cuestionarios 
                WHERE id_docente = %s
            """, (usuario_id,))
            print(f"DEBUG: Eliminados {len(cuestionarios)} cuestionarios del docente")
        
        # Eliminar roles de usuario (común para todos)
        cursor.execute("""
            DELETE FROM usuario_roles 
            WHERE id_usuario = %s
        """, (usuario_id,))
        print(f"DEBUG: Eliminados roles de usuario")
        
        # Finalmente, eliminar el usuario
        cursor.execute("""
            DELETE FROM usuarios 
            WHERE id_usuario = %s
        """, (usuario_id,))
        print(f"DEBUG: Usuario eliminado")
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"✅ Usuario ID {usuario_id} ({tipo_usuario}) eliminado completamente")
        return True, "Usuario eliminado exitosamente"
        
    except Exception as e:
        print(f"❌ Error eliminando usuario {usuario_id}: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False, f"Error al eliminar usuario: {str(e)}"
