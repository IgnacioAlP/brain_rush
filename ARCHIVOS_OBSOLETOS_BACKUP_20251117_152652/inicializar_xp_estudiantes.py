"""
Script para inicializar XP de estudiantes existentes
"""
from bd import obtener_conexion

def inicializar_xp_estudiantes():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        print("\n🔧 INICIALIZANDO XP PARA ESTUDIANTES EXISTENTES")
        print("=" * 60)
        
        # Obtener todos los estudiantes
        cursor.execute("""
            SELECT id_usuario, CONCAT(nombre, ' ', apellidos) as nombre_completo, email 
            FROM usuarios 
            WHERE tipo_usuario = 'estudiante'
        """)
        estudiantes = cursor.fetchall()
        
        print(f"\n📊 Estudiantes encontrados: {len(estudiantes)}")
        
        if len(estudiantes) == 0:
            print("⚠️  No hay estudiantes en la base de datos")
            return
        
        inicializados = 0
        ya_existian = 0
        
        for estudiante in estudiantes:
            id_usuario, nombre, correo = estudiante
            
            # Verificar si ya tiene registro de XP
            cursor.execute("""
                SELECT id_usuario FROM experiencia_usuarios 
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            if cursor.fetchone():
                ya_existian += 1
                print(f"  ✓ {nombre} ({correo}) - Ya tiene XP")
            else:
                # Crear registro de XP
                cursor.execute("""
                    INSERT INTO experiencia_usuarios 
                    (id_usuario, xp_actual, nivel_actual, xp_total_acumulado)
                    VALUES (%s, 0, 1, 0)
                """, (id_usuario,))
                
                # Crear registro de estadísticas
                cursor.execute("""
                    INSERT INTO estadisticas_juego 
                    (id_usuario, total_partidas, total_respuestas_correctas, 
                     total_respuestas_incorrectas, racha_actual, mejor_racha,
                     precision_general, tiempo_promedio_respuesta)
                    VALUES (%s, 0, 0, 0, 0, 0, 0.0, 0.0)
                """, (id_usuario,))
                
                inicializados += 1
                print(f"  🆕 {nombre} ({correo}) - XP inicializado")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETADO")
        print(f"   • Inicializados: {inicializados}")
        print(f"   • Ya existían: {ya_existian}")
        print(f"   • Total: {len(estudiantes)}\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    inicializar_xp_estudiantes()
