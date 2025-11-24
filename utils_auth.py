# -*- coding: utf-8 -*-
"""
Utilidades de autenticación y manejo de cookies seguras
REFACTORIZADO: Sin dependencia de Flask-JWT-Extended (Usa PyJWT nativo)
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app, request, make_response, session, jsonify, redirect, url_for
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# ==================== ENCRIPTACIÓN DE CONTRASEÑAS ====================

def hash_password(password):
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_password(password, password_hash):
    """Verifica si una contraseña coincide con su hash"""
    try:
        # 1. Intentar con bcrypt
        if password_hash.startswith('$2b$') or password_hash.startswith('$2a$'):
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), password_hash)

        # 2. Compatibilidad con MD5 antiguo
        import hashlib
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        if password_hash == md5_hash:
            return True

        # 3. Texto plano (legacy)
        if password_hash == password:
            return True

        return False
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False

# ==================== GESTIÓN DE COOKIES ENCRIPTADAS ====================

def obtener_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def crear_cookie_segura(nombre, valor, max_age=None):
    serializer = obtener_serializer()
    return serializer.dumps(valor, salt=f'cookie-{nombre}')

def leer_cookie_segura(nombre, max_age=None):
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
    cookie_id = crear_cookie_segura('user_id', usuario_id)
    cookie_nombre = crear_cookie_segura('user_name', nombre_usuario)

    is_production = current_app.config.get('ENV') == 'production'

    response.set_cookie('user_id', cookie_id, max_age=timedelta(days=7), httponly=True, secure=is_production, samesite='Lax')
    response.set_cookie('user_name', cookie_nombre, max_age=timedelta(days=7), httponly=True, secure=is_production, samesite='Lax')
    return response

def limpiar_cookies_usuario(response):
    response.set_cookie('user_id', '', expires=0)
    response.set_cookie('user_name', '', expires=0)
    return response

def obtener_usuario_cookies():
    usuario_id = leer_cookie_segura('user_id', max_age=7*24*60*60)
    nombre_usuario = leer_cookie_segura('user_name', max_age=7*24*60*60)
    if usuario_id is not None and nombre_usuario is not None:
        return {'usuario_id': usuario_id, 'nombre_usuario': nombre_usuario}
    return None

# ==================== JWT MANUAL (Reemplazo de flask-jwt-extended) ====================

def crear_token_jwt(usuario_id, expiracion_horas=24):
    """
    Crea un access token usando PyJWT directamente
    """
    try:
        payload = {
            'sub': usuario_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expiracion_horas)
        }
        # Usamos la SECRET_KEY de la app global
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        print(f"Error creando token: {e}")
        return None

def crear_refresh_token(usuario_id):
    """Versión simplificada de refresh token (dura 30 días)"""
    return crear_token_jwt(usuario_id, expiracion_horas=720)

def extraer_token_jwt_request():
    """Extrae el token JWT del header Authorization con formato 'JWT <token>'"""
    auth_header = request.headers.get('Authorization', '')

    # CAMBIO AQUI: Buscamos 'JWT ' en lugar de 'Bearer '
    if auth_header.startswith('JWT '):
        return auth_header[4:] # 'JWT ' tiene 4 caracteres (J-W-T-espacio)

    # Opcional: Soporte legacy para Bearer por si acaso
    if auth_header.startswith('Bearer '):
        return auth_header[7:]

    return None

def verificar_token_jwt(token):
    """Decodifica y verifica el token"""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expirado")
        return None
    except jwt.InvalidTokenError:
        print("Token inválido")
        return None
    except Exception as e:
        print(f"Error verificando token: {e}")
        return None

# ==================== DECORADORES DE PROTECCIÓN ====================

def login_required(f):
    """Decorador que acepta sesión, cookies o JWT Manual"""
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # 1. Sesión tradicional
        if 'usuario_id' in session and session.get('logged_in'):
            return f(*args, **kwargs)

        # 2. Cookies encriptadas (Autologin)
        usuario_cookies = obtener_usuario_cookies()
        if usuario_cookies:
            session['usuario_id'] = usuario_cookies['usuario_id']
            session['usuario_nombre'] = usuario_cookies['nombre_usuario']
            session['logged_in'] = True
            return f(*args, **kwargs)

        # 3. JWT en Authorization header (MANUAL)
        token = extraer_token_jwt_request()
        if token:
            payload = verificar_token_jwt(token)
            if payload and 'sub' in payload:
                # Token válido, loguear en sesión temporalmente para este request
                session['usuario_id'] = payload['sub']
                session['logged_in'] = True
                return f(*args, **kwargs)

        # No autenticado
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({'error': 'Autenticación requerida (Token inválido o faltante)'}), 401
        else:
            return redirect(url_for('login'))

    return decorated_function

def jwt_or_session_required(f):
    """Alias para compatibilidad"""
    return login_required(f)

def docente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Primero verificamos login
        auth_response = login_required(lambda: "OK")()
        if auth_response != "OK":
            return auth_response # Retorna el error o redirect del login_required

        # Verificar rol (asumiendo que está en sesión tras el login)
        if session.get('usuario_tipo') != 'docente':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para docentes'}), 403
            else:
                return redirect(url_for('dashboard_estudiante')) # O página de error

        return f(*args, **kwargs)
    return decorated_function

def estudiante_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_response = login_required(lambda: "OK")()
        if auth_response != "OK":
            return auth_response

        if session.get('usuario_tipo') != 'estudiante':
            if request.is_json:
                return jsonify({'error': 'Acceso solo para estudiantes'}), 403
            else:
                return redirect(url_for('dashboard_admin'))

        return f(*args, **kwargs)
    return decorated_function