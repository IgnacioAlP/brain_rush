"""
Script para obtener tokens de OneDrive manualmente
Ejecutar: python obtener_tokens_onedrive.py
"""

import msal
import os
from datetime import datetime, timedelta

# Cargar variables del .env
from dotenv import load_dotenv
load_dotenv()

# Configuración de Azure
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID', 'common')
REDIRECT_URI = os.getenv('ONEDRIVE_REDIRECT_URI', 'http://localhost:5000/callback/onedrive')

SCOPES = [
    'https://graph.microsoft.com/Files.ReadWrite.All',
    'https://graph.microsoft.com/User.Read'
]

def obtener_tokens_interactivo():
    """Obtener tokens usando flujo interactivo (Device Code Flow)"""
    print("\n🔐 Obteniendo tokens de OneDrive...")
    print(f"Cliente ID: {CLIENT_ID}")
    print(f"Tenant: {TENANT_ID}")
    print(f"Scopes: {', '.join(SCOPES)}\n")
    
    # Crear aplicación MSAL
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=authority
    )
    
    # Usar Device Code Flow (no requiere servidor web)
    flow = app.initiate_device_flow(scopes=SCOPES)
    
    if "user_code" not in flow:
        raise ValueError(f"Error iniciando Device Flow: {flow.get('error_description')}")
    
    print("📱 INSTRUCCIONES:")
    print(f"1. Abre tu navegador en: {flow['verification_uri']}")
    print(f"2. Ingresa este código: {flow['user_code']}")
    print(f"3. Autoriza con la cuenta de OneDrive donde quieres guardar los archivos\n")
    print("⏳ Esperando autorización...")
    
    # Esperar que el usuario autorice
    result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        access_token = result['access_token']
        refresh_token = result.get('refresh_token')
        expires_in = result.get('expires_in', 3600)
        token_expires = datetime.now() + timedelta(seconds=expires_in)
        
        print("\n✅ ¡Tokens obtenidos exitosamente!\n")
        print("📋 TOKENS (copia estos valores al .env):")
        print("-" * 80)
        print(f"ONEDRIVE_ACCESS_TOKEN={access_token}")
        print(f"ONEDRIVE_REFRESH_TOKEN={refresh_token}")
        print(f"ONEDRIVE_TOKEN_EXPIRES={token_expires.isoformat()}")
        print("-" * 80)
        
        # Actualizar .env automáticamente
        actualizar = input("\n¿Actualizar .env automáticamente? (s/n): ").lower()
        if actualizar == 's':
            actualizar_env_file(access_token, refresh_token, token_expires)
            print("\n✅ Archivo .env actualizado correctamente")
            print("🔄 Reinicia el servidor Flask para aplicar los cambios")
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_at': token_expires
        }
    else:
        error = result.get('error')
        error_desc = result.get('error_description', 'Error desconocido')
        print(f"\n❌ Error obteniendo tokens: {error}")
        print(f"Descripción: {error_desc}")
        return None


def actualizar_env_file(access_token, refresh_token, token_expires):
    """Actualizar archivo .env con los nuevos tokens"""
    env_path = '.env'
    
    # Leer archivo actual
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Actualizar líneas
    new_lines = []
    tokens_actualizados = {
        'access': False,
        'refresh': False,
        'expires': False
    }
    
    for line in lines:
        if line.startswith('ONEDRIVE_ACCESS_TOKEN='):
            new_lines.append(f'ONEDRIVE_ACCESS_TOKEN={access_token}\n')
            tokens_actualizados['access'] = True
        elif line.startswith('ONEDRIVE_REFRESH_TOKEN='):
            new_lines.append(f'ONEDRIVE_REFRESH_TOKEN={refresh_token}\n')
            tokens_actualizados['refresh'] = True
        elif line.startswith('ONEDRIVE_TOKEN_EXPIRES='):
            new_lines.append(f'ONEDRIVE_TOKEN_EXPIRES={token_expires.isoformat()}\n')
            tokens_actualizados['expires'] = True
        else:
            new_lines.append(line)
    
    # Si algún token no existía, agregarlo
    if not tokens_actualizados['access']:
        new_lines.append(f'ONEDRIVE_ACCESS_TOKEN={access_token}\n')
    if not tokens_actualizados['refresh']:
        new_lines.append(f'ONEDRIVE_REFRESH_TOKEN={refresh_token}\n')
    if not tokens_actualizados['expires']:
        new_lines.append(f'ONEDRIVE_TOKEN_EXPIRES={token_expires.isoformat()}\n')
    
    # Escribir archivo
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🎓 Brain RUSH - Obtener Tokens de OneDrive")
    print("="*80)
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("\n❌ Error: AZURE_CLIENT_ID y AZURE_CLIENT_SECRET no están configurados en .env")
        print("   Configura estas variables primero")
        exit(1)
    
    try:
        obtener_tokens_interactivo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
