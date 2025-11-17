"""
Script de prueba para verificar configuración de OneDrive OAuth2
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN ONEDRIVE")
print("=" * 60)

# Verificar variables de entorno
variables = {
    'AZURE_CLIENT_ID': os.getenv('AZURE_CLIENT_ID'),
    'AZURE_CLIENT_SECRET': os.getenv('AZURE_CLIENT_SECRET'),
    'AZURE_TENANT_ID': os.getenv('AZURE_TENANT_ID'),
    'ONEDRIVE_REDIRECT_URI': os.getenv('ONEDRIVE_REDIRECT_URI'),
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD')
}

print("\n📋 Variables de Entorno:")
print("-" * 60)
for nombre, valor in variables.items():
    if valor:
        if 'SECRET' in nombre or 'PASSWORD' in nombre:
            print(f"✅ {nombre}: {'*' * 20} (configurada)")
        else:
            print(f"✅ {nombre}: {valor}")
    else:
        print(f"❌ {nombre}: NO CONFIGURADA")

# Verificar librerías
print("\n📦 Librerías Instaladas:")
print("-" * 60)

try:
    import msal
    print(f"✅ msal: {msal.__version__}")
except ImportError:
    print("❌ msal: NO INSTALADA - Ejecuta: pip install msal")

try:
    import requests
    print(f"✅ requests: {requests.__version__}")
except ImportError:
    print("❌ requests: NO INSTALADA - Ejecuta: pip install requests")

try:
    import openpyxl
    print(f"✅ openpyxl: Instalada")
except ImportError:
    print("❌ openpyxl: NO INSTALADA - Ejecuta: pip install openpyxl")

try:
    from flask_mail import Mail
    print(f"✅ Flask-Mail: Instalada")
except ImportError:
    print("❌ Flask-Mail: NO INSTALADA - Ejecuta: pip install Flask-Mail")

# Verificar base de datos
print("\n🗄️  Base de Datos:")
print("-" * 60)

try:
    from bd import obtener_conexion
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Verificar tabla usuarios
    cursor.execute("SHOW TABLES LIKE 'usuarios'")
    if cursor.fetchone():
        print("✅ Tabla 'usuarios' existe")
        
        # Verificar columnas de OneDrive
        cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'onedrive_%'")
        columnas = cursor.fetchall()
        
        if len(columnas) == 3:
            print("✅ Columnas de OneDrive agregadas:")
            for col in columnas:
                print(f"   - {col[0]}: {col[1]}")
        else:
            print(f"⚠️  Solo {len(columnas)}/3 columnas de OneDrive encontradas")
            print("   Ejecuta: python agregar_tokens_simple.py")
    else:
        print("❌ Tabla 'usuarios' NO EXISTE")
    
    cursor.close()
    conexion.close()
    
except Exception as e:
    print(f"❌ Error conectando a la base de datos: {e}")

# Verificar URLs de redirección
print("\n🔗 URLs de Redirección:")
print("-" * 60)

redirect_uri = os.getenv('ONEDRIVE_REDIRECT_URI')
if redirect_uri:
    if 'localhost' in redirect_uri:
        print(f"🏠 MODO LOCAL: {redirect_uri}")
        print("   Para PythonAnywhere, cambia a:")
        print("   https://proyectoweb20252.pythonanywhere.com/callback/onedrive")
    elif 'pythonanywhere' in redirect_uri:
        print(f"🌐 MODO PRODUCCIÓN: {redirect_uri}")
        print("   Para local, cambia a:")
        print("   http://localhost:5000/callback/onedrive")
    else:
        print(f"⚠️  URL personalizada: {redirect_uri}")

# Verificar Azure Portal
print("\n☁️  Azure Portal:")
print("-" * 60)
print("⚠️  ACCIÓN REQUERIDA:")
print("   1. Ve a: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade")
print("   2. Selecciona: 'BrainRush OneDrive Integration'")
print("   3. Ve a: Authentication → Platform configurations → Web")
print("   4. Agrega AMBAS URLs:")
print("      - http://localhost:5000/callback/onedrive")
print("      - https://proyectoweb20252.pythonanywhere.com/callback/onedrive")
print("   5. Guarda los cambios")

# Resumen
print("\n" + "=" * 60)
print("📊 RESUMEN")
print("=" * 60)

errores = []
advertencias = []

if not all(variables.values()):
    errores.append("Faltan variables de entorno en .env")

try:
    import msal, requests
except:
    errores.append("Faltan librerías (msal o requests)")

if errores:
    print("\n❌ ERRORES ENCONTRADOS:")
    for error in errores:
        print(f"   - {error}")
    print("\n⚠️  Corrige los errores antes de continuar")
else:
    print("\n✅ CONFIGURACIÓN CORRECTA")
    print("\n📝 Próximos pasos:")
    print("   1. Agregar URLs de redirección en Azure Portal")
    print("   2. Ejecutar: python main.py")
    print("   3. Abrir: http://localhost:5000")
    print("   4. Probar exportación a OneDrive")

print("\n" + "=" * 60)
