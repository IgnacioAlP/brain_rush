"""
Script para resetear XP de todos los estudiantes
"""
from bd import obtener_conexion

def resetear_xp_estudiantes():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        print("\n🔄 RESETEANDO XP DE ESTUDIANTES")
        print("=" * 60)
        
        # Obtener todos los estudiantes
        cursor.execute("""
            SELECT id_usuario, CONCAT(nombre, ' ', apellidos) as nombre_completo
            FROM usuarios 
            WHERE tipo_usuario = 'estudiante'
        """)
        estudiantes = cursor.fetchall()
        
        print(f"\n📊 Estudiantes encontrados: {len(estudiantes)}")
        
        for id_usuario, nombre in estudiantes:
            # Resetear experiencia
            cursor.execute("""
                UPDATE experiencia_usuarios
                SET xp_actual = 0, nivel_actual = 1, xp_total_acumulado = 0
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            # Resetear estadísticas
            cursor.execute("""
                UPDATE estadisticas_juego
                SET total_partidas_jugadas = 0,
                    total_partidas_ganadas = 0,
                    total_respuestas_correctas = 0,
                    total_respuestas_incorrectas = 0,
                    racha_actual = 0,
                    racha_maxima = 0,
                    precision_promedio = 0.0,
                    tiempo_promedio_respuesta = 0.0
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            # Eliminar insignias desbloqueadas (excepto las compradas)
            cursor.execute("""
                DELETE FROM insignias_usuarios
                WHERE id_usuario = %s
                AND id_insignia NOT IN (
                    SELECT id_insignia FROM compras_insignias WHERE id_usuario = %s
                )
            """, (id_usuario, id_usuario))
            
            # Limpiar historial de XP
            cursor.execute("""
                DELETE FROM historial_xp WHERE id_usuario = %s
            """, (id_usuario,))
            
            print(f"  ✓ {nombre} - XP reseteado")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print(f"✅ XP RESETEADO PARA {len(estudiantes)} ESTUDIANTES")
        print("   • XP: 0")
        print("   • Nivel: 1")
        print("   • Estadísticas: Borradas")
        print("   • Insignias automáticas: Borradas")
        print("   • Insignias compradas: Conservadas\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    confirmar = input("⚠️  ¿Estás seguro de resetear el XP de todos los estudiantes? (si/no): ")
    if confirmar.lower() in ['si', 's', 'yes', 'y']:
        resetear_xp_estudiantes()
    else:
        print("❌ Operación cancelada")
