#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar las APIs CRUD con JWT
"""

import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:5000"
API_URL = f"{BASE_URL}/api"

def obtener_token():
    """Obtener token JWT"""
    print("\n🔐 Paso 1: Obteniendo token JWT...")
    
    # Autenticarse
    response = requests.post(
        f"{API_URL}/auth",
        json={
            "email": "75659265@usat.pe",
            "password": "91649821"
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Token obtenido: {token[:50]}...")
        return token
    else:
        print(f"❌ Error al obtener token")
        return None

def obtener_usuarios(token):
    """Obtener todos los usuarios"""
    print("\n👥 Paso 2: Obteniendo todos los usuarios...")
    
    headers = {
        "Authorization": f"JWT {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{API_URL}/usuarios", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Headers enviados: {headers}")
    
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('data', [])
        print(f"✅ Usuarios encontrados: {len(usuarios)}")
        for usuario in usuarios[:3]:  # Mostrar solo los primeros 3
            print(f"   - {usuario.get('nombre')} {usuario.get('apellidos')} ({usuario.get('email')})")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return False

def crear_usuario(token):
    """Crear un nuevo usuario"""
    print("\n➕ Paso 3: Creando nuevo usuario...")
    
    headers = {
        "Authorization": f"JWT {token}",
        "Content-Type": "application/json"
    }
    
    nuevo_usuario = {
        "nombre": "José",
        "apellidos": "Pérez",
        "email": "76ab239@usat.pe",
        "contraseña_hash": "de03bd53e93242b639cdb4a5f9396297901760cf9e6f6e93a09f0c397Dc5972665e87",
        "tipo_usuario": "estudiante",
        "estado": "activo"
    }
    
    print(f"Datos a enviar: {json.dumps(nuevo_usuario, indent=2)}")
    
    response = requests.post(
        f"{API_URL}/usuarios",
        json=nuevo_usuario,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Usuario creado: ID {data.get('data', {}).get('id_usuario')}")
        return True
    elif response.status_code == 409:
        print(f"⚠️ Usuario ya existe (email duplicado)")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return False

def main():
    print("="*80)
    print("🧪 PRUEBA DE APIs CRUD CON JWT")
    print("="*80)
    
    # Paso 1: Obtener token
    token = obtener_token()
    if not token:
        print("\n❌ No se pudo obtener token. Verifica tus credenciales.")
        return
    
    # Paso 2: Obtener usuarios
    if not obtener_usuarios(token):
        print("\n❌ Falló la obtención de usuarios")
        return
    
    # Paso 3: Crear usuario
    if not crear_usuario(token):
        print("\n❌ Falló la creación de usuario")
        return
    
    print("\n" + "="*80)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()
