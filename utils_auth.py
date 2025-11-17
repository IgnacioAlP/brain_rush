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


# ==================== JWT (USANDO flask-jwt-extended) ====================

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    get_jwt_identity,
    decode_token,
)


def crear_token_jwt(usuario_id, expiracion_horas=24):
    """
    Crea un access token usando Flask-JWT-Extended
    """
    expires = timedelta(hours=expiracion_horas)
    return create_access_token(identity=usuario_id, expires_delta=expires)


def crear_refresh_token(usuario_id):
    """
    Crea un refresh token usando Flask-JWT-Extended
    """
    return create_refresh_token(identity=usuario_id)


def verificar_token_jwt(token):
    """
    Decodifica un token sin levantar excepción (usa decode_token)
    """
    try:
        payload = decode_token(token)
        return payload
    except Exception as e:
        print(f"Token JWT inválido o expirado: {e}")
        return None


def extraer_token_jwt_request():
    """Extrae el token JWT del header Authorization"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None


# ==================== DECORADORES DE PROTECCIÓN ====================


def login_required(f):
    """Decorador que acepta sesión o JWT (mantiene compatibilidad con API actual)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for

        # 1. Sesión tradicional
        if 'usuario_id' in session and session.get('logged_in'):
            return f(*args, **kwargs)

        # 2. Cookies encriptadas
        usuario_cookies = obtener_usuario_cookies()
        if usuario_cookies:
            session['usuario_id'] = usuario_cookies['usuario_id']
            session['usuario_nombre'] = usuario_cookies['nombre_usuario']
            session['logged_in'] = True
            return f(*args, **kwargs)

        # 3. JWT en Authorization header
        token = extraer_token_jwt_request()
        if token:
            try:
                # verify_jwt_in_request lee el header y valida el token
                verify_jwt_in_request()
                identidad = get_jwt_identity()
                if identidad:
                    session['usuario_id'] = identidad
                    session['logged_in'] = True
                    return f(*args, **kwargs)
            except Exception as e:
                print(f"Verificación JWT fallida: {e}")

        # No autenticado
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({'error': 'Autenticación requerida'}), 401
        else:
            return redirect(url_for('login'))

    return decorated_function


def jwt_or_session_required(f):
    """Alias para compatibilidad con el código existente"""
    return login_required(f)


def docente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for

        auth_check = login_required(lambda: None)()
        if auth_check:
            return auth_check

        if session.get('usuario_tipo') != 'docente':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para docentes'}), 403
            else:
                return redirect(url_for('dashboard_estudiante'))

        return f(*args, **kwargs)

    return decorated_function


def estudiante_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, jsonify, redirect, url_for

        auth_check = login_required(lambda: None)()
        if auth_check:
            return auth_check

        if session.get('usuario_tipo') != 'estudiante':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para estudiantes'}), 403
            else:
                return redirect(url_for('dashboard_admin'))

        return f(*args, **kwargs)

    return decorated_function
