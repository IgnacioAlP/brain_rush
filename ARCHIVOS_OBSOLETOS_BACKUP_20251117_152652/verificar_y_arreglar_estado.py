# -*- coding: utf-8 -*-
"""
Script para verificar y arreglar la columna estado de salas_juego
"""
import pymysql
from bd import obtener_conexion

def verificar_y_arreglar():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        print("🔍 Verificando estructura de salas_juego...")
        
        # Ver estructura actual
        cursor.execute("DESCRIBE salas_juego")
        columnas = cursor.fetchall()
        
        print("\n📋 Columnas actuales:")
        for col in columnas:
            print(f"  {col[0]}: {col[1]}")
            if col[0] == 'estado':
                print(f"    ⚠️ Tipo actual de 'estado': {col[1]}")
        
        # Verificar si estado permite 'en_juego'
        print("\n🔍 Verificando valores actuales de estado...")
        cursor.execute("SELECT DISTINCT estado FROM salas_juego")
        estados = cursor.fetchall()
        print(f"  Valores encontrados: {[e[0] for e in estados]}")
        
        # Si es ENUM, necesitamos modificarlo
        print("\n🔧 Intentando modificar columna estado...")
        try:
            # Primero, cambiar a VARCHAR para permitir cualquier valor
            cursor.execute("""
                ALTER TABLE salas_juego 
                MODIFY COLUMN estado VARCHAR(20) DEFAULT 'esperando'
            """)
            print("  ✅ Columna estado modificada a VARCHAR(20)")
            conexion.commit()
        except Exception as e:
            print(f"  ⚠️ Error al modificar: {e}")
            conexion.rollback()
        
        # Probar actualizar una sala
        print("\n🧪 Probando actualización de estado...")
        cursor.execute("SELECT id_sala FROM salas_juego LIMIT 1")
        result = cursor.fetchone()
        if result:
            sala_test = result[0]
            cursor.execute("""
                UPDATE salas_juego 
                SET estado = 'en_juego' 
                WHERE id_sala = %s
            """, (sala_test,))
            conexion.commit()
            print(f"  ✅ Estado actualizado exitosamente en sala {sala_test}")
            
            # Verificar
            cursor.execute("SELECT estado FROM salas_juego WHERE id_sala = %s", (sala_test,))
            estado_nuevo = cursor.fetchone()[0]
            print(f"  Valor verificado: '{estado_nuevo}'")
            
            # Regresar a esperando
            cursor.execute("""
                UPDATE salas_juego 
                SET estado = 'esperando' 
                WHERE id_sala = %s
            """, (sala_test,))
            conexion.commit()
            print(f"  ✅ Estado regresado a 'esperando'")
        
        cursor.close()
        conexion.close()
        
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_y_arreglar()
