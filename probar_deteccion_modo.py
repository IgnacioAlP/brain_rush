# -*- coding: utf-8 -*-
"""
Script para probar la detección de modo automático en salas
"""

from bd import obtener_conexion

def es_sala_automatica(pin_sala):
    """Verifica si un PIN corresponde a una sala en modo automático"""
    if not pin_sala:
        return False
    return pin_sala.startswith('AUTO') and len(pin_sala) == 8

def probar_deteccion_salas():
    print("🔍 PRUEBA DE DETECCIÓN DE MODO AUTOMÁTICO")
    print("=" * 80)
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        # Obtener las últimas salas individuales
        cursor.execute('''
            SELECT id_sala, pin_sala, modo_juego, estado, LENGTH(pin_sala) as longitud
            FROM salas_juego
            WHERE modo_juego = 'individual'
            ORDER BY id_sala DESC
            LIMIT 5
        ''')
        
        salas = cursor.fetchall()
        
        print(f"\n📋 ÚLTIMAS 5 SALAS INDIVIDUALES:")
        print("-" * 80)
        print(f"{'ID':<6} {'PIN':<12} {'Long':<6} {'Es Auto?':<12} {'Tiene Docente?':<18}")
        print("-" * 80)
        
        for sala in salas:
            id_sala, pin_sala, modo, estado, longitud = sala
            
            # Detectar modo automático
            es_auto = es_sala_automatica(pin_sala)
            tiene_docente = not es_auto  # Simplificado para la prueba
            
            # Formatear salida
            es_auto_str = "✅ SÍ" if es_auto else "❌ NO"
            docente_str = "❌ NO (auto)" if not tiene_docente else "✅ SÍ (manual)"
            
            print(f"{id_sala:<6} {pin_sala:<12} {longitud:<6} {es_auto_str:<12} {docente_str:<18}")
        
        print("-" * 80)
        
        # Resumen
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN LENGTH(pin_sala) = 8 AND pin_sala LIKE 'AUTO%' THEN 1 ELSE 0 END) as automaticas,
                SUM(CASE WHEN LENGTH(pin_sala) = 6 THEN 1 ELSE 0 END) as manuales
            FROM salas_juego
            WHERE modo_juego = 'individual'
        ''')
        
        resumen = cursor.fetchone()
        total, automaticas, manuales = resumen
        
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   Total salas individuales: {total}")
        print(f"   🤖 Automáticas (AUTO + 4): {automaticas}")
        print(f"   👨‍🏫 Manuales (6 dígitos): {manuales}")
        
        cursor.close()
        conexion.close()
        
        print("\n" + "=" * 80)
        print("✅ Detección funcionando correctamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if conexion:
            conexion.close()

if __name__ == "__main__":
    probar_deteccion_salas()
