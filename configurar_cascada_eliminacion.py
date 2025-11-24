# -*- coding: utf-8 -*-
"""
Script para agregar ON DELETE CASCADE a todas las foreign keys
Este script ejecuta el archivo SQL agregar_cascada_eliminacion.sql
"""

from bd import obtener_conexion
import os

def ejecutar_sql_cascade():
    """Ejecuta el script SQL para agregar ON DELETE CASCADE"""
    
    # Leer el archivo SQL
    sql_file = 'agregar_cascada_eliminacion.sql'
    
    if not os.path.exists(sql_file):
        print(f"❌ Error: No se encontró el archivo {sql_file}")
        return False
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Dividir por los delimitadores de SQL
    statements = []
    current_statement = []
    in_delimiter_block = False
    
    for line in sql_content.split('\n'):
        line = line.strip()
        
        # Ignorar comentarios y líneas vacías
        if not line or line.startswith('--'):
            continue
        
        # Detectar bloques DELIMITER
        if line.upper().startswith('DELIMITER'):
            in_delimiter_block = not in_delimiter_block
            continue
        
        current_statement.append(line)
        
        # Si encontramos punto y coma y no estamos en un bloque DELIMITER
        if ';' in line and not in_delimiter_block:
            statement = ' '.join(current_statement)
            if statement.strip():
                statements.append(statement)
            current_statement = []
    
    print(f"📝 Se encontraron {len(statements)} statements SQL\n")
    
    # Ejecutar cada statement
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        exitos = 0
        errores = 0
        
        for i, statement in enumerate(statements, 1):
            try:
                # Limpiar el statement
                statement = statement.strip()
                if not statement or statement == ';':
                    continue
                
                # Ejecutar
                cursor.execute(statement)
                exitos += 1
                
                # Mostrar progreso cada 5 statements
                if i % 5 == 0:
                    print(f"✅ Ejecutados {i}/{len(statements)} statements...")
                
            except Exception as e:
                error_msg = str(e)
                # Ignorar errores de "constraint doesn't exist" (es normal)
                if "doesn't exist" not in error_msg.lower() and "unknown" not in error_msg.lower():
                    print(f"⚠️ Error en statement {i}: {error_msg[:100]}")
                    errores += 1
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"\n{'='*50}")
        print(f"✅ Proceso completado")
        print(f"   Statements exitosos: {exitos}")
        print(f"   Errores (no críticos): {errores}")
        print(f"{'='*50}\n")
        
        # Verificar las foreign keys
        verificar_foreign_keys()
        
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def verificar_foreign_keys():
    """Verifica las foreign keys y sus reglas ON DELETE"""
    print("\n🔍 Verificando foreign keys con ON DELETE CASCADE...\n")
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                CONSTRAINT_NAME,
                REFERENCED_TABLE_NAME,
                DELETE_RULE
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = 'brain_rush'
            ORDER BY TABLE_NAME, CONSTRAINT_NAME
        """)
        
        fks = cursor.fetchall()
        
        cascade_count = 0
        set_null_count = 0
        restrict_count = 0
        
        print(f"{'Tabla':<30} {'FK':<40} {'Referencia':<20} {'ON DELETE':<15}")
        print("=" * 110)
        
        for fk in fks:
            table, constraint, ref_table, delete_rule = fk
            
            # Contar por tipo
            if delete_rule == 'CASCADE':
                cascade_count += 1
                emoji = "✅"
            elif delete_rule == 'SET NULL':
                set_null_count += 1
                emoji = "🔵"
            else:
                restrict_count += 1
                emoji = "⚠️"
            
            print(f"{emoji} {table:<28} {constraint:<38} {ref_table:<18} {delete_rule:<15}")
        
        cursor.close()
        conexion.close()
        
        print("\n" + "=" * 110)
        print(f"\n📊 Resumen:")
        print(f"   ✅ CASCADE: {cascade_count}")
        print(f"   🔵 SET NULL: {set_null_count}")
        print(f"   ⚠️ RESTRICT/NO ACTION: {restrict_count}")
        print(f"   📝 Total: {len(fks)}\n")
        
    except Exception as e:
        print(f"❌ Error verificando foreign keys: {e}")
        if 'conexion' in locals():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 CONFIGURACIÓN DE ON DELETE CASCADE")
    print("=" * 50)
    print()
    
    respuesta = input("⚠️ Este script modificará las foreign keys de la base de datos.\n¿Deseas continuar? (s/n): ")
    
    if respuesta.lower() == 's':
        print("\n🚀 Iniciando configuración...\n")
        ejecutar_sql_cascade()
    else:
        print("\n❌ Operación cancelada")
