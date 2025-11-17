# -*- coding: utf-8 -*-
"""
Script de prueba rápida para el sistema de autenticación
"""
import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_autenticacion_rapida():
    """Probar autenticación rápidamente"""
    print("\n" + "="*60)
    print("🔐 PRUEBA RÁPIDA DE AUTENTICACIÓN")
    print("="*60)
    
    from controladores import controlador_usuario
    
    # Probar con el usuario que tienes
    email = "75502058@usat.pe"
    
    print(f"\n📧 Email a probar: {email}")
    password = input("🔑 Ingresa la contraseña: ").strip()
    
    if not password:
        print("❌ No ingresaste contraseña")
        return
    
    print(f"\n🔍 Intentando autenticar...")
    
    try:
        success, resultado = controlador_usuario.autenticar_usuario(email, password)
        
        if success:
            print("\n" + "="*60)
            print("✅ AUTENTICACIÓN EXITOSA")
            print("="*60)
            print(f"\n👤 Datos del usuario:")
            print(f"   ID: {resultado['id_usuario']}")
            print(f"   Nombre: {resultado['nombre']}")
            print(f"   Apellidos: {resultado['apellidos']}")
            print(f"   Email: {resultado['email']}")
            print(f"   Tipo: {resultado['tipo_usuario']}")
            print(f"   Estado: {resultado['estado']}")
            print()
        else:
            print("\n" + "="*60)
            print("❌ AUTENTICACIÓN FALLIDA")
            print("="*60)
            print(f"\n⚠️ Mensaje: {resultado}")
            print()
            
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR EN AUTENTICACIÓN")
        print("="*60)
        print(f"\n🔴 Error: {e}")
        import traceback
        traceback.print_exc()

def test_verificar_hash_contraseña():
    """Verificar el hash de contraseña en la BD"""
    print("\n" + "="*60)
    print("🔍 VERIFICAR HASH DE CONTRASEÑA EN BD")
    print("="*60)
    
    from bd import obtener_conexion
    import pymysql
    
    email = "75502058@usat.pe"
    
    try:
        conexion = obtener_conexion()
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id_usuario, email, `contraseña_hash`, estado
                FROM usuarios 
                WHERE email = %s
            """, (email,))
            usuario = cursor.fetchone()
        conexion.close()
        
        if usuario:
            print(f"\n✅ Usuario encontrado en BD:")
            print(f"   ID: {usuario['id_usuario']}")
            print(f"   Email: {usuario['email']}")
            print(f"   Estado: {usuario['estado']}")
            print(f"\n🔑 Hash de contraseña:")
            
            password_hash = usuario['contraseña_hash']
            print(f"   Longitud: {len(password_hash)} caracteres")
            print(f"   Primeros 10 caracteres: {password_hash[:10]}...")
            
            # Detectar tipo de hash
            if password_hash.startswith('$2b$') or password_hash.startswith('$2a$'):
                print(f"   Tipo: ✅ bcrypt (SEGURO)")
            elif len(password_hash) == 32 and all(c in '0123456789abcdef' for c in password_hash.lower()):
                print(f"   Tipo: ⚠️ MD5 (INSEGURO - se migrará a bcrypt al iniciar sesión)")
            else:
                print(f"   Tipo: ❓ Desconocido")
            
            print()
        else:
            print(f"\n❌ Usuario no encontrado: {email}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

def menu_principal():
    """Menú principal"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "PRUEBAS DE AUTENTICACIÓN" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    while True:
        print("\n📋 Opciones:")
        print("   1. Probar login con email/contraseña")
        print("   2. Ver hash de contraseña en BD")
        print("   3. Salir")
        
        opcion = input("\n👉 Selecciona una opción (1-3): ").strip()
        
        if opcion == '1':
            test_autenticacion_rapida()
        elif opcion == '2':
            test_verificar_hash_contraseña()
        elif opcion == '3':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
