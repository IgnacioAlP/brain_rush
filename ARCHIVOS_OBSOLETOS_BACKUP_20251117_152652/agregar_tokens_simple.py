import pymysql
from bd import obtener_conexion

try:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Verificar si las columnas ya existen
    cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'onedrive_access_token'")
    if cursor.fetchone() is None:
        print("Agregando columnas de OneDrive...")
        cursor.execute("""
            ALTER TABLE usuarios 
            ADD COLUMN onedrive_access_token TEXT NULL,
            ADD COLUMN onedrive_refresh_token TEXT NULL,
            ADD COLUMN onedrive_token_expires DATETIME NULL
        """)
        conexion.commit()
        print("✅ Columnas agregadas exitosamente")
    else:
        print("✅ Las columnas ya existen")
    
    # Mostrar estructura de la tabla
    cursor.execute("DESCRIBE usuarios")
    print("\n📋 Estructura de la tabla usuarios:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]}")
    
    cursor.close()
    conexion.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
