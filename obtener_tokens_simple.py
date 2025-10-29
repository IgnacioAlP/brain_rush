"""
Script simplificado para obtener URL de autorización de OneDrive
Ejecutar: python obtener_tokens_simple.py
"""

import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Configuración de Azure
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID', 'common')
REDIRECT_URI = os.getenv('ONEDRIVE_REDIRECT_URI', 'http://localhost:5000/callback/onedrive')

print("\n" + "="*80)
print("🎓 Brain RUSH - Obtener Tokens de OneDrive")
print("="*80)

if not CLIENT_ID or not CLIENT_SECRET:
    print("\n❌ Error: AZURE_CLIENT_ID y AZURE_CLIENT_SECRET no están configurados en .env")
    exit(1)

print(f"""
✅ Configuración detectada:
   Cliente ID: {CLIENT_ID}
   Tenant: {TENANT_ID}
   Redirect URI: {REDIRECT_URI}

📋 OPCIÓN 1 - Usar el servidor Flask (RECOMENDADO):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Asegúrate de que Flask esté corriendo:
   python main.py

2. Abre tu navegador en:
   http://localhost:5000/auth/onedrive-sistema

3. Inicia sesión como DOCENTE en Brain RUSH

4. Autoriza con tu cuenta de Microsoft/OneDrive

5. Los tokens se guardarán automáticamente en .env

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 OPCIÓN 2 - Autorización manual:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Copia esta URL y ábrela en tu navegador:
""")

# Construir URL de autorización manualmente
scopes = "Files.ReadWrite User.Read offline_access"
auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope={scopes}&state=SISTEMA_CONFIG"

print(f"\n{auth_url}\n")

print("""
2. Autoriza con tu cuenta de Microsoft/OneDrive

3. Serás redirigido a:
   http://localhost:5000/callback/onedrive?code=CODIGO_AQUI...

4. Copia el CÓDIGO de la URL (el valor después de 'code=')

5. Ejecuta este comando en Python:
""")

print("""
   import msal
   from datetime import datetime, timedelta

   app = msal.ConfidentialClientApplication(
       client_id='""" + CLIENT_ID + """',
       client_credential='""" + CLIENT_SECRET + """',
       authority='https://login.microsoftonline.com/""" + TENANT_ID + """'
   )

   result = app.acquire_token_by_authorization_code(
       code='PEGA_AQUI_EL_CODIGO',
       scopes=['Files.ReadWrite', 'User.Read'],
       redirect_uri='""" + REDIRECT_URI + """'
   )

   if 'access_token' in result:
       print("\\n✅ TOKENS OBTENIDOS:")
       print(f"\\nONEDRIVE_ACCESS_TOKEN={result['access_token']}")
       print(f"ONEDRIVE_REFRESH_TOKEN={result.get('refresh_token', '')}")
       expires = datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
       print(f"ONEDRIVE_TOKEN_EXPIRES={expires.isoformat()}")
       print("\\n📋 Copia estos valores al archivo .env")
   else:
       print(f"\\n❌ Error: {result}")
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  RECOMENDACIÓN: Usa la OPCIÓN 1 (más fácil)

   Solo necesitas:
   1. Ejecutar: python main.py
   2. Visitar: http://localhost:5000/auth/onedrive-sistema
   3. Listo! Los tokens se guardan automáticamente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
