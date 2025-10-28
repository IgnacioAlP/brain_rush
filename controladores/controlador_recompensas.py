from bd import obtener_conexion

# Insertar nueva recompensa asociada a un cuestionario
def insertar_recompensa(nombre, descripcion, puntos_requeridos, tipo, id_cuestionario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO recompensas (nombre, descripcion, puntos_requeridos, tipo, id_cuestionario)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre, descripcion, puntos_requeridos, tipo, id_cuestionario)
        )
    conexion.commit()
    conexion.close()


# Obtener todas las recompensas de un cuestionario específico
def obtener_recompensas_por_cuestionario(id_cuestionario):
    conexion = obtener_conexion()
    recompensas = []
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id_recompensa, nombre, descripcion, puntos_requeridos, tipo
            FROM recompensas
            WHERE id_cuestionario = %s
            ORDER BY puntos_requeridos ASC
            """,
            (id_cuestionario,)
        )
        # ✅ Convertir filas a diccionarios manualmente
        columnas = [col[0] for col in cursor.description]
        recompensas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error al obtener recompensas del cuestionario {id_cuestionario}: {e}")
    finally:
        conexion.close()
    return recompensas


# Eliminar recompensa por su ID
def eliminar_recompensa(id_recompensa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM recompensas WHERE id_recompensa = %s", (id_recompensa,))
    conexion.commit()
    conexion.close()

def obtener_ganadores_recompensas(id_cuestionario=None):
    conexion = obtener_conexion()
    with conexion.cursor(dictionary=True) as cursor:
        if id_cuestionario:
            cursor.execute("""
                SELECT r.nombre AS recompensa, r.tipo, u.nombre AS estudiante, u.apellidos, ro.fecha_otorgacion
                FROM recompensas_otorgadas ro
                JOIN recompensas r ON ro.id_recompensa = r.id_recompensa
                JOIN usuarios u ON ro.id_estudiante = u.id_usuario
                WHERE r.id_cuestionario = %s
                ORDER BY ro.fecha_otorgacion DESC
            """, (id_cuestionario,))
        else:
            cursor.execute("""
                SELECT r.nombre AS recompensa, r.tipo, u.nombre AS estudiante, u.apellidos, ro.fecha_otorgacion
                FROM recompensas_otorgadas ro
                JOIN recompensas r ON ro.id_recompensa = r.id_recompensa
                JOIN usuarios u ON ro.id_estudiante = u.id_usuario
                ORDER BY ro.fecha_otorgacion DESC
            """)
        return cursor.fetchall()


def asignar_recompensas_top3(sala_id):
    """
    Asigna automáticamente recompensas a los 3 primeros puestos de una sala
    
    Args:
        sala_id: ID de la sala finalizada
        
    Returns:
        Diccionario con información de las recompensas asignadas
    """
    conexion = obtener_conexion()
    recompensas_asignadas = []
    
    try:
        with conexion.cursor() as cursor:
            # Obtener el cuestionario de la sala
            cursor.execute('''
                SELECT id_cuestionario FROM salas_juego WHERE id_sala = %s
            ''', (sala_id,))
            
            result = cursor.fetchone()
            if not result:
                print(f"❌ Sala {sala_id} no encontrada")
                return {'success': False, 'error': 'Sala no encontrada'}
            
            id_cuestionario = result[0]
            
            # Obtener recompensas configuradas para este cuestionario ordenadas por tipo
            # Asumimos: trofeo (1er), medalla (2do), insignia (3ro)
            cursor.execute('''
                SELECT id_recompensa, nombre, tipo, puntos_requeridos
                FROM recompensas
                WHERE id_cuestionario = %s
                ORDER BY 
                    CASE 
                        WHEN tipo = 'trofeo' THEN 1
                        WHEN tipo = 'medalla' THEN 2
                        WHEN tipo = 'insignia' THEN 3
                        ELSE 4
                    END,
                    puntos_requeridos DESC
                LIMIT 3
            ''', (id_cuestionario,))
            
            recompensas_disponibles = cursor.fetchall()
            
            if not recompensas_disponibles:
                print(f"⚠️ No hay recompensas configuradas para el cuestionario {id_cuestionario}")
                return {'success': False, 'error': 'No hay recompensas configuradas'}
            
            # Obtener TOP 3 del ranking
            cursor.execute('''
                SELECT 
                    r.posicion,
                    p.id_participante,
                    p.id_usuario,
                    p.nombre_participante,
                    r.puntaje_total
                FROM ranking_sala r
                JOIN participantes_sala p ON r.id_participante = p.id_participante
                WHERE r.id_sala = %s AND p.id_usuario IS NOT NULL
                ORDER BY r.posicion ASC
                LIMIT 3
            ''', (sala_id,))
            
            top3_participantes = cursor.fetchall()
            
            if not top3_participantes:
                print(f"⚠️ No hay participantes registrados para asignar recompensas")
                return {'success': False, 'error': 'No hay participantes con usuarios registrados'}
            
            # Asignar recompensas a cada posición
            for i, participante_data in enumerate(top3_participantes):
                posicion, id_participante, id_usuario, nombre_participante, puntaje_total = participante_data
                
                # Si hay recompensa disponible para esta posición
                if i < len(recompensas_disponibles):
                    id_recompensa, nombre_recompensa, tipo_recompensa, puntos_requeridos = recompensas_disponibles[i]
                    
                    # Verificar si ya se asignó esta recompensa a este usuario
                    cursor.execute('''
                        SELECT COUNT(*) 
                        FROM recompensas_otorgadas 
                        WHERE id_recompensa = %s AND id_estudiante = %s
                    ''', (id_recompensa, id_usuario))
                    
                    ya_tiene = cursor.fetchone()[0]
                    
                    if ya_tiene == 0:
                        # Insertar recompensa otorgada
                        cursor.execute('''
                            INSERT INTO recompensas_otorgadas (id_estudiante, id_recompensa)
                            VALUES (%s, %s)
                        ''', (id_usuario, id_recompensa))
                        
                        recompensas_asignadas.append({
                            'posicion': posicion,
                            'nombre_participante': nombre_participante,
                            'recompensa': nombre_recompensa,
                            'tipo': tipo_recompensa,
                            'puntaje': puntaje_total
                        })
                        
                        print(f"🏆 Recompensa '{nombre_recompensa}' ({tipo_recompensa}) asignada a {nombre_participante} (Posición {posicion})")
                    else:
                        print(f"⚠️ {nombre_participante} ya tiene la recompensa '{nombre_recompensa}'")
            
            conexion.commit()
            
            return {
                'success': True,
                'total_asignadas': len(recompensas_asignadas),
                'recompensas': recompensas_asignadas
            }
            
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al asignar recompensas automáticas: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}
    finally:
        conexion.close()
