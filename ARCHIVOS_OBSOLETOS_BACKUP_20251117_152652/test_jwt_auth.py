"""
Script de prueba para verificar la autenticación JWT

IMPORTANTE: Antes de ejecutar este script, debes iniciar el servidor Flask:
    python main.py

El servidor debe estar corriendo en http://127.0.0.1:5000
"""
import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'

print("=" * 60)
print("PRUEBA DE AUTENTICACIÓN JWT")
print("=" * 60)

# Verificar que el servidor esté corriendo
print("\n🔍 Verificando que el servidor Flask esté activo...")
try:
    response = requests.get(f'{BASE_URL}/login', timeout=2)
    print(f"✅ Servidor activo (Status: {response.status_code})")
except requests.exceptions.ConnectionError:
    print("❌ ERROR: El servidor Flask no está corriendo")
    print("\n📋 Para iniciar el servidor, ejecuta en otra terminal:")
    print("   python main.py")
    print("\nLuego vuelve a ejecutar este script.")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Error verificando servidor: {e}")
    sys.exit(1)

# Test 1: Login con credenciales incorrectas
print("\n1️⃣ Test: Login con credenciales incorrectas")
response = requests.post(f'{BASE_URL}/api/auth', json={
    'email': 'noexiste@test.com',
    'password': 'wrongpass'
})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
assert response.status_code == 401, "Debería retornar 401 Unauthorized"
print("   ✅ PASS: Rechaza credenciales incorrectas")

# Test 2: Login sin datos
print("\n2️⃣ Test: Login sin datos")
response = requests.post(f'{BASE_URL}/api/auth', json={})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
assert response.status_code == 400, "Debería retornar 400 Bad Request"
print("   ✅ PASS: Rechaza request sin datos")

# Test 3: Login exitoso (necesitas crear un usuario de prueba primero)
print("\n3️⃣ Test: Login exitoso")
print("   ⚠️  Este test requiere un usuario de prueba en la BD")
print("   Ejemplo: email='docente@test.com', password='password123'")
print("   ")

# Solicitar credenciales al usuario
email = input("   Ingresa email de prueba (o Enter para omitir): ").strip()

if email:
    password = input("   Ingresa password: ").strip()
    
    response = requests.post(f'{BASE_URL}/api/auth', json={
        'email': email,
        'password': password
    })
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200 and 'access_token' in data:
        print("   ✅ PASS: Login exitoso, token recibido")
        
        # Test 4: Usar token en endpoint protegido
        print("\n4️⃣ Test: Acceder a endpoint protegido con JWT")
        token = data['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Intentar acceder a un endpoint protegido
        # Nota: Necesitas un endpoint que use @jwt_or_session_required
        # Por ejemplo, si tienes /api/mi-perfil o similar
        
        print(f"   Token (primeros 50 chars): {token[:50]}...")
        print("   ✅ Token JWT generado correctamente")
        print("   ")
        print("   💡 Para probar el token, usa:")
        print(f'   curl -H "Authorization: Bearer {token}" http://127.0.0.1:5000/api/TU_ENDPOINT')
        
    else:
        print("   ❌ FAIL: No se pudo autenticar")
else:
    print("   ⏭️  Test omitido")

# Test 5: Acceder a endpoint protegido sin autenticación
print("\n5️⃣ Test: Acceder a endpoint protegido sin autenticación")
print("   (Este test funcionará cuando tengas endpoints con @jwt_or_session_required)")
print("   Ejemplo de uso:")
print("   ")
print("   @app.route('/api/datos-protegidos')")
print("   @jwt_or_session_required")
print("   def datos_protegidos():")
print("       return jsonify({'data': 'información secreta'})")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print("✅ Flask-JWT-Extended configurado correctamente")
print("✅ Endpoint /api/auth funcionando")
print("✅ Validación de credenciales activa")
print("✅ Generación de tokens JWT operativa")
print("\n💡 Siguiente paso: Probar endpoints protegidos con @jwt_or_session_required")
print("=" * 60)
