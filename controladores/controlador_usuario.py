# -*- coding: utf-8 -*-
from bd import obtener_conexion
import hashlib
import pymysql
from flask import current_app, url_for, render_template
from flask_mail import Message
from extensions import mail
from itsdangerous import URLSafeTimedSerializer

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
    """
    Autenticar un usuario con email y contraseña.
    (Versi�n ANTIGUA: Mantenida por sus mensajes de estado detallados)
    """
    try:
        email = email.strip().lower()

        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            # Buscar el usuario por email
            cursor.execute("""
                SELECT id_usuario, nombre, apellidos, email, `contraseña_hash`, tipo_usuario, estado
                FROM usuarios
                WHERE email = %s
            """, (email,))
            usuario = cursor.fetchone()
        conexion.close()

        if not usuario:
            print(f"Usuario no encontrado: {email}")
            return False, "Email o contraseña incorrectos"

        # LÓGICA AÑADIDA PARA VERIFICAR ESTADO (del c�digo ANTIGUO)
        if usuario['estado'] == 'inactivo':
            print(f"Intento de login para cuenta inactiva: {email}")
            return False, "Tu cuenta no ha sido activada. Por favor, revisa tu correo electr�nico."

        if usuario['estado'] != 'activo':
            print(f"Intento de login para cuenta no activa: {email} (estado: {usuario['estado']})")
            return False, "Tu cuenta está suspendida o inactiva."

        # Verificar la contraseña
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
                return False, "Email o contraseña incorrectos"

    except Exception as e:
        print(f"Error en autenticación: {e}")
        return False, "Error interno del sistema."
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
                SELECT id_usuario, nombre, apellidos, email, `contraseña_hash`, tipo_usuario, estado
                FROM usuarios 
                WHERE email = %s AND estado = 'activo'
            """, (email,))
            usuario = cursor.fetchone()
        conexion.close()
        
        if not usuario:
            print(f"Usuario no encontrado: {email}")
            return False, None
        
        # Verificar la contraseña
        # Primero intentamos con hash MD5 (m�todo simple)
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
        
        # Verificar que la contraseña sea �nica
        if not verificar_contrasena_unica(password):
            return False, "Esta contraseña ya está siendo utilizada por otro usuario. Por favor, elige una diferente."
        
        # Hash de la contraseña
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        # Determinar el estado inicial seg�n si el correo está habilitado
        from flask import current_app
        mail_enabled = current_app.config.get('MAIL_ENABLED', False)
        estado_inicial = 'inactivo' if mail_enabled else 'activo'
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Verificar si el email ya existe
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                conexion.close()
                return False, "El email ya está registrado"
            
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellidos, email, `contraseña_hash`, tipo_usuario, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellidos, email, password_hash, tipo_usuario, estado_inicial))
            
            conexion.commit()
            usuario_id = cursor.lastrowid
        conexion.close()
        
        print(f"Usuario creado exitosamente: {email}")
        return True, usuario_id
        
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False, str(e)


def enviar_correo_confirmacion(email):
    """Genera y envía el correo de confirmaci�n."""
    try:
        # Crear el serializador
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        
        # Generar el token
        token = serializer.dumps(email, salt='email-confirm-salt')
        
        # Crear el enlace de confirmaci�n
        confirm_url = url_for('confirmar_email', token=token, _external=True)
        
        print(f"DEBUG: URL de confirmaci�n generada: {confirm_url}")
        
        # Crear el cuerpo del mensaje usando una plantilla
        try:
            html = render_template('Email_confirmacion.html', confirm_url=confirm_url, email=email)
        except Exception as template_error:
            print(f"DEBUG: Error al renderizar template, usando HTML b�sico: {template_error}")
            # HTML b�sico como fallback
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h1 style="color: #4ECDC4; text-align: center;">�Bienvenido a Brain RUSH! ??</h1>
                        <p style="color: #333; font-size: 16px;">Hola,</p>
                        <p style="color: #333; font-size: 16px;">Gracias por registrarte en Brain RUSH. Para activar tu cuenta, por favor haz clic en el siguiente bot�n:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{confirm_url}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; display: inline-block;">
                                Confirmar mi cuenta
                            </a>
                        </div>
                        <p style="color: #666; font-size: 14px;">Si el bot�n no funciona, copia y pega este enlace en tu navegador:</p>
                        <p style="color: #4ECDC4; font-size: 14px; word-break: break-all;">{confirm_url}</p>
                        <p style="color: #999; font-size: 12px; margin-top: 30px; text-align: center;">Este enlace expirar� en 1 hora.</p>
                        <p style="color: #999; font-size: 12px; text-align: center;">Si no te registraste en Brain RUSH, ignora este correo.</p>
                    </div>
                </body>
            </html>
            """
        
        # Crear y enviar el mensaje
        msg = Message(
            subject='Confirma tu cuenta - Brain RUSH ??',
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_USERNAME')),
            recipients=[email],
            html=html
        )
        
        mail.send(msg)
        print(f"? Correo de confirmaci�n enviado exitosamente a: {email}")
        return True, "Correo enviado exitosamente"
        
    except Exception as e:
        print(f"? Error al enviar correo de confirmaci�n: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

# --- Funci�n del C�DIGO ANTIGUO (necesaria para 'crear_usuario') ---
def activar_cuenta_usuario(email):
    """Cambia el estado de un usuario de 'inactivo' a 'activo'."""
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Primero, verificar que el usuario existe y está inactivo
            cursor.execute("SELECT estado FROM usuarios WHERE email = %s", (email,))
            resultado = cursor.fetchone()

            if not resultado:
                return False, "El usuario no existe."

            if resultado[0] == 'activo':
                return True, "Tu cuenta ya ha sido activada previamente. Ya puedes iniciar sesi�n."

            # Actualizar el estado a 'activo'
            cursor.execute("UPDATE usuarios SET estado = 'activo' WHERE email = %s", (email,))
            conexion.commit()

        conexion.close()
        return True, "�Tu cuenta ha sido activada! Ahora puedes iniciar sesi�n."

    except Exception as e:
        print(f"Error al activar la cuenta de {email}: {e}")
        return False, "Ocurri� un error al activar tu cuenta."


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

# --- Funci�n del C�DIGO NUEVO ---
def verificar_contrasena_unica(password, excluir_usuario_id=None):
    """Verificar que una contraseña no está siendo usada por otro usuario"""
    try:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            if excluir_usuario_id:
                cursor.execute(
                    "SELECT id_usuario FROM usuarios WHERE `contraseña_hash` = %s AND id_usuario != %s", 
                    (password_hash, excluir_usuario_id)
                )
            else:
                cursor.execute(
                    "SELECT id_usuario FROM usuarios WHERE `contraseña_hash` = %s", 
                    (password_hash,)
                )
            resultado = cursor.fetchone()
        conexion.close()
        return resultado is None  # True si es �nica, False si ya existe
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return True  # En caso de error, permitir la contraseña (comportamiento seguro)

# --- Funci�n del C�DIGO ANTIGUO ---
def actualizar_usuario(usuario_id, nombre, apellidos, email, password=None):
    """Actualizar datos personales del usuario (propio perfil)"""
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            if password:
                # (NOTA: Se podr�a a�adir la verificación de contraseña �nica aqu� tambi�n si se desea)
                # if not verificar_contrasena_unica(password, excluir_usuario_id=usuario_id):
                #     return False, "Esa contraseña ya está en uso."
                
                password_hash = hashlib.md5(password.encode()).hexdigest()
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, apellidos = %s, email = %s, `contraseña_hash` = %s
                    WHERE id_usuario = %s
                """, (nombre, apellidos, email, password_hash, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nombre = %s, apellidos = %s, email = %s
                    WHERE id_usuario = %s
                """, (nombre, apellidos, email, usuario_id))
            conexion.commit()
        conexion.close()
        return True, "Perfil actualizado correctamente"
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False, str(e)

# --- Funci�n del C�DIGO NUEVO ---
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
                
                # Eliminar las preguntas (esto puede ser redundante si las preguntas no se comparten,
                # pero es m�s seguro eliminar por si acaso)
                # Esta consulta es compleja y podr�a fallar si las preguntas se reutilizan. 
                # Es m�s seguro eliminar solo la relaci�n.
                
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
        
        # Eliminar roles de usuario (com�n para todos)
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
        
        print(f"? Usuario ID {usuario_id} ({tipo_usuario}) eliminado completamente")
        return True, "Usuario eliminado exitosamente"
        
    except Exception as e:
        print(f"? Error eliminando usuario {usuario_id}: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False, f"Error al eliminar usuario: {str(e)}"
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
        
        # Eliminar roles de usuario (com�n para todos)
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
        
        print(f"? Usuario ID {usuario_id} ({tipo_usuario}) eliminado completamente")
        return True, "Usuario eliminado exitosamente"
        
    except Exception as e:
        print(f"? Error eliminando usuario {usuario_id}: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False, f"Error al eliminar usuario: {str(e)}"

# Funciones de recuperaciÃ³n de contraseÃ±a para agregar a controlador_usuario.py

# ========== RECUPERACIÃ“N DE CONTRASEÃ‘A ==========

def solicitar_recuperacion_contrasena(email):
    """
    Genera un token de recuperaciÃ³n y envÃ­a el correo electrÃ³nico.
    Retorna: (success: bool, mensaje: str)
    """
    try:
        email = email.strip().lower()
        
        # Verificar que el usuario existe
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id_usuario, nombre, email, estado
                FROM usuarios
                WHERE email = %s
            """, (email,))
            usuario = cursor.fetchone()
        conexion.close()
        
        if not usuario:
            # Por seguridad, no revelar si el email existe o no
            return True, "Si el correo existe en nuestro sistema, recibirÃ¡s instrucciones para restablecer tu contraseÃ±a."
        
        if usuario['estado'] != 'activo':
            return False, "Esta cuenta no estÃ¡ activa. Por favor contacta al administrador."
        
        # Crear el serializador para generar el token
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        
        # Generar el token (vÃ¡lido por 1 hora)
        token = serializer.dumps(email, salt='password-reset-salt')
        
        # Crear el enlace de recuperaciÃ³n
        reset_url = url_for('restablecer_contrasena', token=token, _external=True)
        
        print(f"DEBUG: URL de recuperaciÃ³n generada: {reset_url}")
        
        # Crear el cuerpo del mensaje usando template
        try:
            html = render_template('Email_recuperacion.html', 
                                 reset_url=reset_url, 
                                 email=email,
                                 nombre=usuario['nombre'])
        except Exception as template_error:
            print(f"DEBUG: Error al renderizar template, usando HTML bÃ¡sico: {template_error}")
            # HTML bÃ¡sico como fallback
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h1 style="color: #FF6B6B; text-align: center;">ðŸ”’ RecuperaciÃ³n de ContraseÃ±a</h1>
                        <p style="color: #333; font-size: 16px;">Hola {usuario['nombre']},</p>
                        <p style="color: #333; font-size: 16px;">Recibimos una solicitud para restablecer la contraseÃ±a de tu cuenta en Brain RUSH.</p>
                        <p style="color: #333; font-size: 16px;">Haz clic en el siguiente botÃ³n para crear una nueva contraseÃ±a:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{reset_url}" style="background: linear-gradient(135deg, #FF6B6B 0%, #C44569 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; display: inline-block;">
                                Restablecer ContraseÃ±a
                            </a>
                        </div>
                        <p style="color: #666; font-size: 14px;">Si el botÃ³n no funciona, copia y pega este enlace en tu navegador:</p>
                        <p style="color: #FF6B6B; font-size: 14px; word-break: break-all;">{reset_url}</p>
                        <p style="color: #999; font-size: 12px; margin-top: 30px; text-align: center;">â° Este enlace expirarÃ¡ en 1 hora por seguridad.</p>
                        <p style="color: #999; font-size: 12px; text-align: center;">â— Si no solicitaste este cambio, ignora este correo. Tu contraseÃ±a permanecerÃ¡ sin cambios.</p>
                    </div>
                </body>
            </html>
            """
        
        # Crear y enviar el mensaje
        msg = Message(
            subject='ðŸ”’ RecuperaciÃ³n de ContraseÃ±a - Brain RUSH',
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_USERNAME')),
            recipients=[email],
            html=html
        )
        
        mail.send(msg)
        print(f"âœ… Correo de recuperaciÃ³n enviado exitosamente a: {email}")
        return True, "Si el correo existe en nuestro sistema, recibirÃ¡s instrucciones para restablecer tu contraseÃ±a."
        
    except Exception as e:
        print(f"âŒ Error al enviar correo de recuperaciÃ³n: {e}")
        import traceback
        traceback.print_exc()
        return False, "Hubo un error al procesar tu solicitud. Por favor intenta nuevamente."


def validar_token_recuperacion(token, max_age=3600):
    """
    Valida el token de recuperaciÃ³n de contraseÃ±a.
    max_age: tiempo en segundos (por defecto 1 hora = 3600 segundos)
    Retorna: (success: bool, email: str o error_msg: str)
    """
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
        print(f"âœ… Token vÃ¡lido para email: {email}")
        return True, email
    except Exception as e:
        print(f"âŒ Token invÃ¡lido o expirado: {e}")
        return False, "El enlace de recuperaciÃ³n es invÃ¡lido o ha expirado. Por favor solicita uno nuevo."


def restablecer_contrasena(email, nueva_contrasena):
    """
    Actualiza la contraseÃ±a de un usuario.
    Retorna: (success: bool, mensaje: str)
    """
    try:
        email = email.strip().lower()
        
        # Verificar que el usuario existe
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id_usuario, email, estado
                FROM usuarios
                WHERE email = %s
            """, (email,))
            usuario = cursor.fetchone()
            
            if not usuario:
                conexion.close()
                return False, "Usuario no encontrado."
            
            if usuario['estado'] != 'activo':
                conexion.close()
                return False, "Esta cuenta no estÃ¡ activa."
            
            # Hashear la nueva contraseña
            password_hash = hashlib.md5(nueva_contrasena.encode()).hexdigest()
            
            # Actualizar la contraseña (usar backticks para evitar problemas de encoding)
            cursor.execute("""
                UPDATE usuarios 
                SET `contraseña_hash` = %s
                WHERE email = %s
            """, (password_hash, email))
            
            conexion.commit()
        
        conexion.close()
        print(f"âœ… ContraseÃ±a actualizada exitosamente para: {email}")
        return True, "Tu contraseÃ±a ha sido actualizada exitosamente. Ya puedes iniciar sesiÃ³n."
        
    except Exception as e:
        print(f"âŒ Error al restablecer contraseÃ±a: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            conexion.close()
        return False, "Hubo un error al actualizar tu contraseÃ±a. Por favor intenta nuevamente."

