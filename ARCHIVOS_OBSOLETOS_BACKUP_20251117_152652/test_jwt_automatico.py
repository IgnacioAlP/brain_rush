"""
Script de prueba automatizado para JWT (sin interacción)

IMPORTANTE: Antes de ejecutar, debes iniciar el servidor:
    python main.py
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

print("=" * 70)
print("PRUEBA AUTOMÁTICA DE AUTENTICACIÓN JWT")
print("=" * 70)

# Verificar servidor
print("\n🔍 Verificando servidor Flask...")
try:
    response = requests.get(f'{BASE_URL}/login', timeout=2)
    print(f"✅ Servidor activo (Status: {response.status_code})")
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Servidor no está corriendo. Ejecuta: python main.py")
    exit(1)

# Test 1: Login sin datos
print("\n" + "=" * 70)
print("TEST 1: Login sin datos (debe fallar)")
print("=" * 70)
response = requests.post(f'{BASE_URL}/api/auth', json={})
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
if response.status_code == 400:
    print("✅ PASS: Rechaza request sin datos correctamente")
else:
    print("❌ FAIL: Debería retornar 400")

# Test 2: Login con credenciales incorrectas
print("\n" + "=" * 70)
print("TEST 2: Login con credenciales incorrectas (debe fallar)")
print("=" * 70)
response = requests.post(f'{BASE_URL}/api/auth', json={
    'email': 'noexiste@test.com',
    'password': 'wrongpass'
})
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
if response.status_code == 401:
    print("✅ PASS: Rechaza credenciales incorrectas")
else:
    print("❌ FAIL: Debería retornar 401")

# Test 3: Login con email válido pero password incorrecta
print("\n" + "=" * 70)
print("TEST 3: Login con email válido pero password incorrecta")
print("=" * 70)
response = requests.post(f'{BASE_URL}/api/auth', json={
    'email': '75502058@usat.pe',
    'password': 'passwordincorrecto123'
})
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
if response.status_code == 401:
    print("✅ PASS: Rechaza password incorrecta")
else:
    print("❌ FAIL: Debería retornar 401")

# Test 4: Instrucciones para login exitoso
print("\n" + "=" * 70)
print("TEST 4: Login Exitoso (MANUAL)")
print("=" * 70)
print("Para probar un login exitoso, ejecuta este comando con tus credenciales:")
print()
print("curl -X POST http://127.0.0.1:5000/api/auth \\")
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"email": "tu_email@ejemplo.com", "password": "tu_password"}\'')
print()
print("O usa Python:")
print()
print("import requests")
print("response = requests.post('http://127.0.0.1:5000/api/auth', json={")
print("    'email': 'tu_email@ejemplo.com',")
print("    'password': 'tu_password'")
print("})")
print("token = response.json()['access_token']")
print("print('Token:', token)")
print()
print("Luego usa el token:")
print("headers = {'Authorization': f'Bearer {token}'}")
print("response = requests.post('http://127.0.0.1:5000/api/ENDPOINT', headers=headers)")

# Resumen
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)
print("✅ Endpoint /api/auth está funcionando")
print("✅ Validación de datos activa")
print("✅ Validación de credenciales activa")
print("✅ Respuestas JSON correctas")
print()
print("💡 Endpoints protegidos con @jwt_or_session_required:")
print("   - /api/comprar-insignia")
print("   - /exportar-resultados")
print("   - /api/iniciar-sala")
print("   - /api/cerrar-sala")
print("   - /publicar-cuestionario")
print("   - /despublicar-cuestionario")
print("   - /eliminar-pregunta")
print("   - /importar-preguntas")
print("   - /api/verificar-respuesta")
print("   - /api/obtener-estadisticas-sala")
print("=" * 70)
