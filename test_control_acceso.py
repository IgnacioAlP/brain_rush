"""
Script para probar el control de acceso basado en roles
Verifica que estudiantes no puedan acceder a /docente y viceversa
"""

import requests
from requests.cookies import RequestsCookieJar

BASE_URL = "http://127.0.0.1:5000"

def probar_acceso_estudiante():
    """Prueba que un estudiante NO pueda acceder al panel docente"""
    print("\n" + "="*60)
    print("🧪 PROBANDO ACCESO DE ESTUDIANTE")
    print("="*60)
    
    session = requests.Session()
    
    # 1. Login como estudiante
    print("\n1️⃣ Iniciando sesión como estudiante (75502058@usat.pe)...")
    login_data = {
        'email': '75502058@usat.pe',
        'password': '75502058'  # Ajusta la contraseña si es diferente
    }
    
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Login exitoso como: {result.get('user', {}).get('nombre')}")
            print(f"   Tipo de usuario: {result.get('user', {}).get('tipo_usuario')}")
        else:
            print(f"   ❌ Error en login: {result.get('error')}")
            return
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
        return
    
    # 2. Intentar acceder al panel de estudiante (DEBE FUNCIONAR)
    print("\n2️⃣ Intentando acceder a /estudiante (debería permitir)...")
    response = session.get(f"{BASE_URL}/estudiante", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Acceso permitido a /estudiante (CORRECTO)")
    elif response.status_code in [301, 302, 303, 307, 308]:
        print(f"   ⚠️ Redirigido a: {response.headers.get('Location')}")
        print("   ❌ No debería redirigir si es estudiante (INCORRECTO)")
    else:
        print(f"   ❌ Error inesperado: {response.status_code}")
    
    # 3. Intentar acceder al panel docente (DEBE FALLAR)
    print("\n3️⃣ Intentando acceder a /docente (debería DENEGAR)...")
    response = session.get(f"{BASE_URL}/docente", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ❌ Acceso permitido a /docente (INCORRECTO - BUG!)")
    elif response.status_code in [301, 302, 303, 307, 308]:
        print(f"   ✅ Redirigido a: {response.headers.get('Location')} (CORRECTO)")
    elif response.status_code == 403:
        print("   ✅ Acceso denegado (403 Forbidden) (CORRECTO)")
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}")
    
    # 4. Intentar acceder al panel admin (DEBE FALLAR)
    print("\n4️⃣ Intentando acceder a /admin (debería DENEGAR)...")
    response = session.get(f"{BASE_URL}/admin", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ❌ Acceso permitido a /admin (INCORRECTO - BUG!)")
    elif response.status_code in [301, 302, 303, 307, 308]:
        print(f"   ✅ Redirigido a: {response.headers.get('Location')} (CORRECTO)")
    elif response.status_code == 403:
        print("   ✅ Acceso denegado (403 Forbidden) (CORRECTO)")
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}")


def probar_acceso_docente():
    """Prueba que un docente NO pueda acceder al panel estudiante"""
    print("\n" + "="*60)
    print("🧪 PROBANDO ACCESO DE DOCENTE")
    print("="*60)
    
    session = requests.Session()
    
    # 1. Login como docente
    print("\n1️⃣ Iniciando sesión como docente...")
    email_docente = input("   📧 Ingresa el email del docente: ").strip()
    password_docente = input("   🔒 Ingresa la contraseña: ").strip()
    
    login_data = {
        'email': email_docente,
        'password': password_docente
    }
    
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Login exitoso como: {result.get('user', {}).get('nombre')}")
            print(f"   Tipo de usuario: {result.get('user', {}).get('tipo_usuario')}")
            
            if result.get('user', {}).get('tipo_usuario') != 'docente':
                print(f"   ⚠️ ADVERTENCIA: El usuario no es docente!")
                return
        else:
            print(f"   ❌ Error en login: {result.get('error')}")
            return
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
        return
    
    # 2. Intentar acceder al panel docente (DEBE FUNCIONAR)
    print("\n2️⃣ Intentando acceder a /docente (debería permitir)...")
    response = session.get(f"{BASE_URL}/docente", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Acceso permitido a /docente (CORRECTO)")
    elif response.status_code in [301, 302, 303, 307, 308]:
        print(f"   ⚠️ Redirigido a: {response.headers.get('Location')}")
        print("   ❌ No debería redirigir si es docente (INCORRECTO)")
    else:
        print(f"   ❌ Error inesperado: {response.status_code}")
    
    # 3. Intentar acceder al panel estudiante (DEBE FALLAR)
    print("\n3️⃣ Intentando acceder a /estudiante (debería DENEGAR)...")
    response = session.get(f"{BASE_URL}/estudiante", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ❌ Acceso permitido a /estudiante (INCORRECTO - BUG!)")
    elif response.status_code in [301, 302, 303, 307, 308]:
        print(f"   ✅ Redirigido a: {response.headers.get('Location')} (CORRECTO)")
    elif response.status_code == 403:
        print("   ✅ Acceso denegado (403 Forbidden) (CORRECTO)")
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}")


if __name__ == "__main__":
    print("\n🔐 PRUEBA DE CONTROL DE ACCESO BASADO EN ROLES")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"✅ Servidor Flask detectado en {BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"❌ ERROR: No se puede conectar a {BASE_URL}")
        print("   Asegúrate de que el servidor Flask esté corriendo")
        exit(1)
    
    # Probar acceso de estudiante
    probar_acceso_estudiante()
    
    # Preguntar si quiere probar con docente
    print("\n" + "="*60)
    respuesta = input("\n¿Deseas probar también con un usuario docente? (s/n): ").strip().lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        probar_acceso_docente()
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
