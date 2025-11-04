# -*- coding: utf-8 -*-
"""
Script para probar la creación de una sala automática con PIN de 8 caracteres
"""

from bd import obtener_conexion
import random
import string

def probar_crear_sala_automatica():
    print("🧪 PRUEBA DE CREACIÓN DE SALA AUTOMÁTICA")
    print("=" * 60)
    
    # Generar PIN de prueba
    codigo_aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    pin_sala = f'AUTO{codigo_aleatorio}'
    
    print(f"\n📌 PIN Generado:")
    print(f"   PIN: {pin_sala}")
    print(f"   Longitud: {len(pin_sala)} caracteres")
    print(f"   Formato: AUTO + 4 caracteres alfanuméricos")
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        # Obtener un cuestionario para probar
        cursor.execute("SELECT id_cuestionario FROM cuestionarios LIMIT 1")
        cuestionario = cursor.fetchone()
        
        if not cuestionario:
            print("\n⚠️ No hay cuestionarios disponibles para probar")
            return
        
        id_cuestionario = cuestionario[0]
        
        print(f"\n🎯 Creando sala de prueba...")
        print(f"   Cuestionario ID: {id_cuestionario}")
        
        # Crear sala
        cursor.execute('''
            INSERT INTO salas_juego 
            (id_cuestionario, pin_sala, estado, modo_juego, total_preguntas, fecha_creacion, grupos_habilitados, num_grupos)
            VALUES (%s, %s, 'en_curso', 'individual', 10, NOW(), 0, 0)
        ''', (id_cuestionario, pin_sala))
        
        conexion.commit()
        id_sala = cursor.lastrowid
        
        print(f"   ✅ Sala creada con ID: {id_sala}")
        
        # Verificar que se guardó correctamente
        cursor.execute('''
            SELECT id_sala, pin_sala, modo_juego, LENGTH(pin_sala) as longitud
            FROM salas_juego
            WHERE id_sala = %s
        ''', (id_sala,))
        
        sala = cursor.fetchone()
        
        print(f"\n📋 VERIFICACIÓN:")
        print(f"   ID Sala: {sala[0]}")
        print(f"   PIN almacenado: {sala[1]}")
        print(f"   Modo: {sala[2]}")
        print(f"   Longitud: {sala[3]} caracteres")
        
        if sala[1] == pin_sala and sala[3] == 8:
            print(f"\n   ✅ PIN SE GUARDÓ CORRECTAMENTE (8 caracteres completos)")
        else:
            print(f"\n   ❌ PIN SE TRUNCÓ")
            print(f"      Esperado: {pin_sala} (8 chars)")
            print(f"      Obtenido: {sala[1]} ({sala[3]} chars)")
        
        # Probar la función es_sala_automatica
        es_auto = sala[1].startswith('AUTO') and len(sala[1]) == 8
        print(f"\n🔍 DETECCIÓN DE MODO:")
        print(f"   es_sala_automatica(): {es_auto}")
        print(f"   {'✅ CORRECTO' if es_auto else '❌ INCORRECTO'}")
        
        cursor.close()
        conexion.close()
        
        print("\n" + "=" * 60)
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if conexion:
            conexion.rollback()
            conexion.close()

if __name__ == "__main__":
    probar_crear_sala_automatica()
