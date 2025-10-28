# Script para instalar dependencias de OneDrive
# Ejecutar: python instalar_onedrive.py

import subprocess
import sys

def instalar_dependencias():
    """Instala las dependencias necesarias para OneDrive"""
    print("🔧 Instalando dependencias para OneDrive...")
    print("-" * 50)
    
    dependencias = [
        'msal>=1.24.0',
        'requests>=2.31.0'
    ]
    
    for dep in dependencias:
        print(f"\n📦 Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {dep}: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("✅ Todas las dependencias instaladas correctamente")
    print("=" * 50)
    print("\n📋 Próximos pasos:")
    print("1. Ejecuta el script SQL: python ejecutar_sql.py agregar_onedrive_tokens.sql")
    print("2. Configura las variables de entorno en el archivo .env")
    print("3. Lee CONFIGURAR_ONEDRIVE.md para obtener las credenciales de Azure")
    print("4. Reinicia el servidor Flask")
    
    return True

if __name__ == '__main__':
    exito = instalar_dependencias()
    sys.exit(0 if exito else 1)
