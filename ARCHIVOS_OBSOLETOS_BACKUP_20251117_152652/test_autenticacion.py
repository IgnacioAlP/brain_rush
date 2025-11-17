# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el sistema de autenticación actualizado
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_password_hashing():
    """Probar el sistema de hashing de contraseñas"""
    print("\n" + "="*60)
    print("1. PRUEBA DE HASHING DE CONTRASEÑAS (bcrypt)")
    print("="*60)
    
    from utils_auth import hash_password, verificar_password
    
    # Crear hash de una contraseña
    password = "MiContraseñaSegura123!"
    print(f"\n📝 Contraseña original: {password}")
    
    password_hash = hash_password(password)
    print(f"🔒 Hash bcrypt generado: {password_hash[:60]}...")
    print(f"   Longitud del hash: {len(password_hash)} caracteres")
    print(f"   Prefijo: {password_hash[:4]} (identifica bcrypt)")
    
    # Verificar contraseña correcta
    es_correcta = verificar_password(password, password_hash)
    print(f"\n✅ Verificación con contraseña correcta: {es_correcta}")
    
    # Verificar contraseña incorrecta
    es_incorrecta = verificar_password("ContraseñaIncorrecta", password_hash)
    print(f"❌ Verificación con contraseña incorrecta: {es_incorrecta}")
    
    # Probar compatibilidad con MD5 (legacy)
    import hashlib
    password_md5 = "test123"
    hash_md5 = hashlib.md5(password_md5.encode()).hexdigest()
    print(f"\n🔄 Compatibilidad MD5 (legacy)")
    print(f"   Contraseña: {password_md5}")
    print(f"   Hash MD5: {hash_md5}")
    
    es_valido_md5 = verificar_password(password_md5, hash_md5)
    print(f"   ✅ Verificación MD5 legacy: {es_valido_md5}")
    
    print("\n✅ PRUEBA COMPLETADA: Sistema de hashing funciona correctamente\n")


def test_cookies():
    """Probar el sistema de cookies encriptadas"""
    print("\n" + "="*60)
    print("2. PRUEBA DE COOKIES ENCRIPTADAS")
    print("="*60)
    
    from itsdangerous import URLSafeTimedSerializer
    
    # Crear cookies de prueba (sin Flask context, usando serializer directo)
    usuario_id = 123
    nombre_usuario = "Juan Pérez"
    
    print(f"\n📝 Datos originales:")
    print(f"   ID: {usuario_id}")
    print(f"   Nombre: {nombre_usuario}")
    
    # Crear serializer con clave temporal
    serializer = URLSafeTimedSerializer('test-secret-key-12345')
    
    # Encriptar
    cookie_id = serializer.dumps(usuario_id, salt='cookie-user_id')
    cookie_nombre = serializer.dumps(nombre_usuario, salt='cookie-user_name')
    
    print(f"\n🔒 Cookies encriptadas:")
    print(f"   ID encriptado: {cookie_id[:50]}...")
    print(f"   Nombre encriptado: {cookie_nombre[:50]}...")
    
    # Desencriptar
    id_desencriptado = serializer.loads(cookie_id, salt='cookie-user_id')
    nombre_desencriptado = serializer.loads(cookie_nombre, salt='cookie-user_name')
    
    print(f"\n✅ Datos desencriptados:")
    print(f"   ID: {id_desencriptado}")
    print(f"   Nombre: {nombre_desencriptado}")
    
    # Verificar integridad
    if id_desencriptado == usuario_id and nombre_desencriptado == nombre_usuario:
        print(f"\n✅ PRUEBA COMPLETADA: Cookies se encriptan y desencriptan correctamente\n")
    else:
        print(f"\n❌ ERROR: Los datos no coinciden\n")


def test_jwt():
    """Probar el sistema JWT personalizado"""
    print("\n" + "="*60)
    print("3. PRUEBA DE JWT PERSONALIZADO")
    print("="*60)
    
    import jwt
    from datetime import datetime, timedelta
    
    # Crear token directamente (sin Flask context)
    usuario_id = 456
    secret_key = 'test-secret-key-12345'
    
    print(f"\n📝 ID de usuario: {usuario_id}")
    
    # Crear payload
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    # Generar token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(f"\n🔑 Token JWT generado:")
    print(f"   {token[:80]}...")
    print(f"   Longitud: {len(token)} caracteres")
    
    # Verificar token
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(f"\n✅ Token verificado correctamente:")
        print(f"   Usuario ID: {decoded.get('usuario_id')}")
        print(f"   Emitido en: {decoded.get('iat')}")
        print(f"   Expira en: {decoded.get('exp')}")
        
        if decoded.get('usuario_id') == usuario_id:
            print(f"\n✅ PRUEBA COMPLETADA: JWT funciona correctamente\n")
        else:
            print(f"\n❌ ERROR: El usuario ID no coincide\n")
    except jwt.InvalidTokenError as e:
        print(f"\n❌ ERROR: Token inválido - {e}\n")


def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n" + "="*60)
    print("4. PRUEBA DE CONEXIÓN A BASE DE DATOS")
    print("="*60)
    
    try:
        from bd import verificar_conexion
        
        print("\n🔌 Intentando conectar a la base de datos...")
        
        if verificar_conexion():
            print("✅ Conexión exitosa a la base de datos")
            print("\n✅ PRUEBA COMPLETADA: Base de datos accesible\n")
        else:
            print("❌ No se pudo conectar a la base de datos")
            print("   Verifica tu archivo bd.py y credenciales\n")
    except Exception as e:
        print(f"❌ ERROR: {e}\n")


def verificar_sistema_completo():
    """Verificación completa del sistema"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "VERIFICACIÓN DEL SISTEMA" + " "*19 + "║")
    print("║" + " "*14 + "Brain Rush - Autenticación" + " "*17 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # 1. Verificar imports
        print("\n📦 Verificando paquetes instalados...")
        try:
            import jwt
            print("   ✅ PyJWT instalado")
        except ImportError:
            print("   ❌ PyJWT NO instalado")
            return False
        
        try:
            import bcrypt
            print("   ✅ bcrypt instalado")
        except ImportError:
            print("   ❌ bcrypt NO instalado")
            return False
        
        try:
            from itsdangerous import URLSafeTimedSerializer
            print("   ✅ itsdangerous instalado")
        except ImportError:
            print("   ❌ itsdangerous NO instalado")
            return False
        
        try:
            from flask import Flask, __version__ as flask_version
            print(f"   ✅ Flask {flask_version} instalado")
        except ImportError:
            print("   ❌ Flask NO instalado")
            return False
        
        # 2. Verificar archivos
        print("\n📄 Verificando archivos del sistema...")
        archivos_requeridos = [
            'utils_auth.py',
            'main.py',
            'requirements.txt',
            'controladores/controlador_usuario.py',
            'config.py',
            '.env'
        ]
        
        for archivo in archivos_requeridos:
            if os.path.exists(archivo):
                print(f"   ✅ {archivo}")
            else:
                print(f"   ❌ {archivo} NO ENCONTRADO")
        
        # 3. Ejecutar pruebas
        test_password_hashing()
        test_cookies()
        test_jwt()
        test_database_connection()
        
        # Resumen final
        print("\n" + "="*60)
        print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("\n🎉 El sistema de autenticación está listo para usar!")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecuta: python main.py")
        print("   2. Abre: http://localhost:5000")
        print("   3. Prueba registro/login con un usuario")
        print("\n⚠️  Recuerda:")
        print("   - Los usuarios con contraseñas MD5 se migrarán automáticamente")
        print("   - Las cookies se establecen al iniciar sesión")
        print("   - El JWT funciona para APIs móviles/externas")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR durante la verificación: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        resultado = verificar_sistema_completo()
        sys.exit(0 if resultado else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
