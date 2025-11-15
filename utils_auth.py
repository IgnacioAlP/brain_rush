# -*- coding: utf-8 -*-
"""
Utilidades de autenticación y manejo de cookies seguras
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app, request, make_response
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


# ==================== ENCRIPTACIÓN DE CONTRASEÑAS ====================

def hash_password(password):
    """
    Hashea una contraseña usando bcrypt (mucho más seguro que MD5 o SHA256)
    
    Args:
        password (str): Contraseña en texto plano
    
    Returns:
        str: Hash de la contraseña
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verificar_password(password, password_hash):
    """
    Verifica si una contraseña coincide con su hash
    
    Args:
        password (str): Contraseña en texto plano
        password_hash (str): Hash almacenado en la base de datos
    
    Returns:
        bool: True si coincide, False en caso contrario
    """
    try:
        # Primero intentar con bcrypt (nuevo sistema)
        if password_hash.startswith('$2b$') or password_hash.startswith('$2a$'):
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        
        # Compatibilidad con MD5 antiguo (para migración gradual)
        import hashlib
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        if password_hash == md5_hash:
            return True
        
        # También verificar contraseñas en texto plano (legacy)
        if password_hash == password:
            return True
        
        return False
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False


# ==================== GESTIÓN DE COOKIES ENCRIPTADAS ====================

def obtener_serializer():
    """Obtiene el serializador para cookies seguras"""
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def crear_cookie_segura(nombre, valor, max_age=None):
    """
    Crea una cookie encriptada
    
    Args:
        nombre (str): Nombre de la cookie
        valor: Valor a encriptar (puede ser str, int, dict, etc.)
        max_age (int): Tiempo de vida en segundos (None = sesión)
    
    Returns:
        str: Token encriptado
    """
    serializer = obtener_serializer()
    return serializer.dumps(valor, salt=f'cookie-{nombre}')


def leer_cookie_segura(nombre, max_age=None):
    """
    Lee y desencripta una cookie
    
    Args:
        nombre (str): Nombre de la cookie
        max_age (int): Tiempo máximo de validez en segundos
    
    Returns:
        El valor desencriptado o None si es inválida/expirada
    """
    try:
        cookie_value = request.cookies.get(nombre)
        if not cookie_value:
            return None
        
        serializer = obtener_serializer()
        return serializer.loads(cookie_value, salt=f'cookie-{nombre}', max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None
    except Exception as e:
        print(f"Error al leer cookie {nombre}: {e}")
        return None


def establecer_cookies_usuario(response, usuario_id, nombre_usuario):
    """
    Establece las cookies encriptadas de usuario en la respuesta
    
    Args:
        response: Objeto Response de Flask
        usuario_id (int): ID del usuario
        nombre_usuario (str): Nombre del usuario
    
    Returns:
        Response: El objeto response modificado
    """
    # Crear cookies encriptadas
    cookie_id = crear_cookie_segura('user_id', usuario_id)
    cookie_nombre = crear_cookie_segura('user_name', nombre_usuario)
    
    # Establecer cookies con configuración segura
    # httponly=True: No accesible desde JavaScript (previene XSS)
    # secure=True: Solo HTTPS en producción
    # samesite='Lax': Protección CSRF
    
    is_production = current_app.config.get('ENV') == 'production'
    
    response.set_cookie(
        'user_id',
        cookie_id,
        max_age=timedelta(days=7),  # 7 días
        httponly=True,
        secure=is_production,  # HTTPS en producción
        samesite='Lax'
    )
    
    response.set_cookie(
        'user_name',
        cookie_nombre,
        max_age=timedelta(days=7),
        httponly=True,
        secure=is_production,
        samesite='Lax'
    )
    
    return response


def limpiar_cookies_usuario(response):
    """
    Elimina las cookies de usuario
    
    Args:
        response: Objeto Response de Flask
    
    Returns:
        Response: El objeto response modificado
    """
    response.set_cookie('user_id', '', expires=0)
    response.set_cookie('user_name', '', expires=0)
    return response


def obtener_usuario_cookies():
    """
    Obtiene los datos del usuario desde las cookies encriptadas
    
    Returns:
        dict: {'usuario_id': int, 'nombre_usuario': str} o None si no hay cookies válidas
    """
    usuario_id = leer_cookie_segura('user_id', max_age=7*24*60*60)  # 7 días
    nombre_usuario = leer_cookie_segura('user_name', max_age=7*24*60*60)
    
    if usuario_id is not None and nombre_usuario is not None:
        return {
            'usuario_id': usuario_id,
            'nombre_usuario': nombre_usuario
        }
    return None


# ==================== JWT (SIN flask-jwt-extended) ====================

def crear_token_jwt(usuario_id, expiracion_horas=24):
    """
    Crea un token JWT personalizado
    
    Args:
        usuario_id (int): ID del usuario
        expiracion_horas (int): Horas hasta que expire el token
    
    Returns:
        str: Token JWT
    """
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=expiracion_horas),
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def verificar_token_jwt(token):
    """
    Verifica y decodifica un token JWT
    
    Args:
        token (str): Token JWT
    
    Returns:
        dict: Payload decodificado o None si es inválido
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        print("Token JWT expirado")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token JWT inválido: {e}")
        return None


def extraer_token_jwt_request():
    """
    Extrae el token JWT del header Authorization
    
    Returns:
        str: Token JWT o None
    """
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]  # Remover 'Bearer '
    return None


# ==================== DECORADORES DE PROTECCIÓN ====================

def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado
    Verifica sesión de Flask O cookies encriptadas O token JWT
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for
        
        # 1. Verificar sesión de Flask (método tradicional)
        if 'usuario_id' in session and session.get('logged_in'):
            return f(*args, **kwargs)
        
        # 2. Verificar cookies encriptadas
        usuario_cookies = obtener_usuario_cookies()
        if usuario_cookies:
            # Establecer sesión desde cookies para compatibilidad
            session['usuario_id'] = usuario_cookies['usuario_id']
            session['usuario_nombre'] = usuario_cookies['nombre_usuario']
            session['logged_in'] = True
            return f(*args, **kwargs)
        
        # 3. Verificar JWT (para APIs)
        token = extraer_token_jwt_request()
        if token:
            payload = verificar_token_jwt(token)
            if payload:
                # Establecer sesión desde JWT para compatibilidad
                session['usuario_id'] = payload['usuario_id']
                session['logged_in'] = True
                return f(*args, **kwargs)
        
        # No autenticado - redirigir o retornar error
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({'error': 'Autenticación requerida'}), 401
        else:
            return redirect(url_for('login'))
    
    return decorated_function


def jwt_or_session_required(f):
    """
    Decorador que acepta autenticación por JWT O por sesión
    Alias de login_required para compatibilidad
    """
    return login_required(f)


def docente_required(f):
    """
    Decorador que requiere que el usuario sea docente
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for
        
        # Primero verificar autenticación con login_required
        auth_check = login_required(lambda: None)()
        if auth_check:  # Si hay redirección o error
            return auth_check
        
        # Verificar tipo de usuario
        if session.get('usuario_tipo') != 'docente':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para docentes'}), 403
            else:
                return redirect(url_for('dashboard_estudiante'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def estudiante_required(f):
    """
    Decorador que requiere que el usuario sea estudiante
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for
        
        # Primero verificar autenticación
        auth_check = login_required(lambda: None)()
        if auth_check:
            return auth_check
        
        # Verificar tipo de usuario
        if session.get('usuario_tipo') != 'estudiante':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para estudiantes'}), 403
            else:
                return redirect(url_for('dashboard_admin'))
        
        return f(*args, **kwargs)
    
    return decorated_function
