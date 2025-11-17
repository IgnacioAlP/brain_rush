#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from bd import obtener_conexion

def ejecutar_migracion():
    """
    Agrega el campo id_cuestionario a la tabla recompensas
    """
    conexion = obtener_conexion()
    
    try:
        with conexion.cursor() as cursor:
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'brain_rush' 
                AND TABLE_NAME = 'recompensas' 
                AND COLUMN_NAME = 'id_cuestionario'
            """)
            
            existe = cursor.fetchone()[0]
            
            if existe > 0:
                print("✅ La columna 'id_cuestionario' ya existe en la tabla 'recompensas'")
                return
            
            print("📝 Agregando columna 'id_cuestionario' a la tabla 'recompensas'...")
            
            # Agregar columna
            cursor.execute("""
                ALTER TABLE `recompensas` 
                ADD COLUMN `id_cuestionario` INT NULL AFTER `tipo`
            """)
            
            print("✅ Columna agregada exitosamente")
            
            # Agregar foreign key
            print("📝 Agregando foreign key...")
            cursor.execute("""
                ALTER TABLE `recompensas`
                ADD CONSTRAINT `FK_recompensas_cuestionario` 
                FOREIGN KEY (`id_cuestionario`) 
                REFERENCES `cuestionarios` (`id_cuestionario`) 
                ON DELETE CASCADE
            """)
            
            print("✅ Foreign key agregada exitosamente")
            
            # Crear índice
            print("📝 Creando índice...")
            cursor.execute("""
                CREATE INDEX `idx_recompensas_cuestionario` 
                ON `recompensas` (`id_cuestionario`)
            """)
            
            print("✅ Índice creado exitosamente")
            
            conexion.commit()
            
            # Verificar la estructura actualizada
            cursor.execute("DESCRIBE recompensas")
            print("\n📊 Estructura actualizada de la tabla 'recompensas':")
            print("-" * 80)
            for row in cursor.fetchall():
                print(f"{row[0]:<25} {row[1]:<20} {row[2]:<5} {row[3]:<5} {row[4] or ''}")
            print("-" * 80)
            
            print("\n✅ ¡Migración completada exitosamente!")
            
    except Exception as e:
        conexion.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conexion.close()

if __name__ == '__main__':
    print("=" * 80)
    print("MIGRACIÓN: Agregar id_cuestionario a tabla recompensas")
    print("=" * 80)
    ejecutar_migracion()
