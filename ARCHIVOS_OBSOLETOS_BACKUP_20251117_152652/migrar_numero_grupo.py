# -*- coding: utf-8 -*-
"""Script para agregar columna numero_grupo a la tabla grupos_sala"""

import pymysql
from bd import obtener_conexion

def ejecutar_migracion():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        print("🔧 Agregando columna numero_grupo a grupos_sala...")
        try:
            cursor.execute("""
                ALTER TABLE grupos_sala
                ADD COLUMN numero_grupo INT NOT NULL DEFAULT 1 AFTER nombre_grupo
            """)
            print("✅ Columna numero_grupo agregada")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("⚠️  La columna numero_grupo ya existe")
            else:
                raise
        
        print("🔧 Renombrando columna capacidad a capacidad_maxima...")
        try:
            cursor.execute("""
                ALTER TABLE grupos_sala
                CHANGE COLUMN capacidad capacidad_maxima INT DEFAULT NULL
            """)
            print("✅ Columna renombrada a capacidad_maxima")
        except pymysql.err.OperationalError as e:
            if "Unknown column 'capacidad'" in str(e):
                print("⚠️  La columna capacidad no existe o ya fue renombrada")
            else:
                raise
        
        print("📊 Creando índice compuesto...")
        try:
            cursor.execute("""
                CREATE INDEX idx_grupos_sala_numero ON grupos_sala (id_sala, numero_grupo)
            """)
            print("✅ Índice creado")
        except pymysql.err.OperationalError as e:
            if "Duplicate key name" in str(e):
                print("⚠️  El índice ya existe")
            else:
                raise
        
        conexion.commit()
        
        print("\n✅ ¡Migración completada exitosamente!")
        
        # Verificar
        cursor.execute("DESCRIBE grupos_sala")
        print("\n📋 Estructura actual de grupos_sala:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_migracion()
