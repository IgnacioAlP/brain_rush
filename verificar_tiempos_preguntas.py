# -*- coding: utf-8 -*-
"""
Script para verificar los tiempos límite de las preguntas importadas
Ayuda a identificar si hay tiempos incorrectos (multiplicados por 10)
"""

from bd import obtener_conexion

def verificar_tiempos_preguntas():
    """Verifica los tiempos límite configurados en los cuestionarios"""
    conexion = obtener_conexion()
    
    print("\n=== VERIFICACIÓN DE TIEMPOS LÍMITE ===\n")
    
    try:
        with conexion.cursor() as cursor:
            # Obtener cuestionarios con su tiempo límite por pregunta
            cursor.execute("""
                SELECT 
                    c.id_cuestionario,
                    c.titulo,
                    c.tiempo_limite_pregunta,
                    COUNT(cp.id_pregunta) as total_preguntas
                FROM cuestionarios c
                LEFT JOIN cuestionario_preguntas cp ON c.id_cuestionario = cp.id_cuestionario
                GROUP BY c.id_cuestionario, c.titulo, c.tiempo_limite_pregunta
                ORDER BY c.id_cuestionario
            """)
            
            cuestionarios = cursor.fetchall()
            
            print("📚 Cuestionarios y sus tiempos límite:\n")
            
            for cuest in cuestionarios:
                id_cuest, titulo, tiempo_limite, total_preguntas = cuest
                
                # Convertir tiempo a segundos si está en minutos
                tiempo_segundos = int(tiempo_limite) if tiempo_limite else 30
                tiempo_minutos = tiempo_segundos / 60
                
                estado = "✅" if tiempo_segundos <= 300 else "⚠️"
                
                print(f"{estado} Cuestionario #{id_cuest}: '{titulo}'")
                print(f"   Tiempo límite: {tiempo_segundos} segundos ({tiempo_minutos:.1f} minutos)")
                print(f"   Total preguntas: {total_preguntas}")
                
                if tiempo_segundos > 300:
                    print(f"   ⚠️ ALERTA: El tiempo parece estar en minutos en lugar de segundos")
                    print(f"   💡 Sugerencia: Debería ser {int(tiempo_segundos / 60)} segundos")
                
                print()
                
    finally:
        conexion.close()

def corregir_tiempos_multiplicados():
    """Corrige los tiempos que están multiplicados por 10 o en minutos"""
    conexion = obtener_conexion()
    
    print("\n=== CORRECCIÓN DE TIEMPOS ===\n")
    
    try:
        with conexion.cursor() as cursor:
            # Buscar cuestionarios con tiempos > 300 segundos (5 minutos)
            cursor.execute("""
                SELECT id_cuestionario, titulo, tiempo_limite_pregunta
                FROM cuestionarios
                WHERE tiempo_limite_pregunta > 300
            """)
            
            cuestionarios_corregir = cursor.fetchall()
            
            if not cuestionarios_corregir:
                print("✅ No hay tiempos que corregir\n")
                return
            
            print(f"Se encontraron {len(cuestionarios_corregir)} cuestionarios con tiempos anormales:\n")
            
            for cuest in cuestionarios_corregir:
                id_cuest, titulo, tiempo_actual = cuest
                tiempo_actual = int(tiempo_actual)
                
                # Asumir que está en minutos y convertir a segundos dividiendo por 60
                tiempo_corregido = tiempo_actual // 60
                
                print(f"📝 Cuestionario #{id_cuest}: '{titulo}'")
                print(f"   Tiempo actual: {tiempo_actual} segundos ({tiempo_actual/60:.1f} minutos)")
                print(f"   Tiempo corregido: {tiempo_corregido} segundos")
                
                respuesta = input(f"   ¿Corregir a {tiempo_corregido} segundos? (s/n): ")
                
                if respuesta.lower() == 's':
                    cursor.execute("""
                        UPDATE cuestionarios
                        SET tiempo_limite_pregunta = %s
                        WHERE id_cuestionario = %s
                    """, (tiempo_corregido, id_cuest))
                    print(f"   ✅ Corregido\n")
                else:
                    print(f"   ⏭️ Omitido\n")
            
            conexion.commit()
            print("✅ Corrección completada")
                
    finally:
        conexion.close()

if __name__ == "__main__":
    verificar_tiempos_preguntas()
    
    print("\n" + "="*50)
    respuesta = input("\n¿Deseas corregir los tiempos anormales? (s/n): ")
    if respuesta.lower() == 's':
        corregir_tiempos_multiplicados()
