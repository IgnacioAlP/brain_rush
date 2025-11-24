from bd import obtener_conexion
import pymysql.cursors

def obtener_ranking_global():
    """
    Obtiene el ranking global de todos los estudiantes
    basado en sus puntajes acumulados de todas las participaciones
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        # Query para obtener el ranking global
        # Suma todos los puntajes de todas las participaciones de cada estudiante
        query = """
            SELECT 
                u.id_usuario,
                u.nombre,
                u.apellidos,
                CONCAT(u.nombre, ' ', u.apellidos) as nombre_completo,
                COUNT(DISTINCT ps.id_participante) as total_participaciones,
                COALESCE(SUM(rs.puntaje_total), 0) as puntaje_acumulado,
                COALESCE(SUM(rs.respuestas_correctas), 0) as total_correctas,
                COALESCE(SUM(rp.es_correcta), 0) as total_respuestas_correctas_alt,
                COALESCE(COUNT(rp.id_respuesta_participante), 0) as total_respuestas,
                COALESCE(AVG(rs.puntaje_total), 0) as promedio_puntaje,
                MAX(rs.puntaje_total) as mejor_puntaje,
                MAX(ps.fecha_union) as ultima_participacion
            FROM usuarios u
            LEFT JOIN participantes_sala ps ON u.id_usuario = ps.id_usuario
            LEFT JOIN ranking_sala rs ON ps.id_participante = rs.id_participante
            LEFT JOIN respuestas_participantes rp ON ps.id_participante = rp.id_participante
            WHERE u.tipo_usuario = 'estudiante'
            GROUP BY u.id_usuario, u.nombre, u.apellidos
            HAVING total_participaciones > 0
            ORDER BY puntaje_acumulado DESC, total_correctas DESC, promedio_puntaje DESC
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Agregar la posición/puesto a cada estudiante
        ranking = []
        for idx, estudiante in enumerate(resultados, start=1):
            estudiante['posicion'] = idx
            
            # Calcular precisión global
            if estudiante['total_respuestas'] > 0:
                estudiante['precision_global'] = round(
                    (estudiante['total_correctas'] / estudiante['total_respuestas']) * 100, 
                    1
                )
            else:
                estudiante['precision_global'] = 0.0
            
            # Formatear números para mejor visualización
            estudiante['puntaje_acumulado'] = int(estudiante['puntaje_acumulado'])
            estudiante['promedio_puntaje'] = round(estudiante['promedio_puntaje'], 1)
            estudiante['mejor_puntaje'] = int(estudiante['mejor_puntaje']) if estudiante['mejor_puntaje'] else 0
            
            ranking.append(estudiante)
        
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Ranking global obtenido con {len(ranking)} estudiantes")
        return ranking
        
    except Exception as e:
        print(f"Error al obtener ranking global: {e}")
        import traceback
        traceback.print_exc()
        return []

def obtener_ranking_global_por_docente(id_docente):
    """
    Obtiene el ranking global de estudiantes 
    pero solo en los cuestionarios creados por un docente específico
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        # Query para obtener el ranking filtrado por cuestionarios del docente
        query = """
            SELECT 
                u.id_usuario,
                u.nombre,
                u.apellidos,
                CONCAT(u.nombre, ' ', u.apellidos) as nombre_completo,
                COUNT(DISTINCT ps.id_participante) as total_participaciones,
                COALESCE(SUM(rs.puntaje_total), 0) as puntaje_acumulado,
                COALESCE(SUM(rs.respuestas_correctas), 0) as total_correctas,
                COALESCE(COUNT(rp.id_respuesta_participante), 0) as total_respuestas,
                COALESCE(AVG(rs.puntaje_total), 0) as promedio_puntaje,
                MAX(rs.puntaje_total) as mejor_puntaje,
                MAX(ps.fecha_union) as ultima_participacion,
                GROUP_CONCAT(DISTINCT c.titulo SEPARATOR ', ') as cuestionarios_jugados
            FROM usuarios u
            LEFT JOIN participantes_sala ps ON u.id_usuario = ps.id_usuario
            LEFT JOIN ranking_sala rs ON ps.id_participante = rs.id_participante
            LEFT JOIN respuestas_participantes rp ON ps.id_participante = rp.id_participante
            LEFT JOIN salas_juego s ON ps.id_sala = s.id_sala
            LEFT JOIN cuestionarios c ON s.id_cuestionario = c.id_cuestionario
            WHERE u.tipo_usuario = 'estudiante'
            AND c.id_docente = %s
            GROUP BY u.id_usuario, u.nombre, u.apellidos
            HAVING total_participaciones > 0
            ORDER BY puntaje_acumulado DESC, total_correctas DESC, promedio_puntaje DESC
        """
        
        cursor.execute(query, (id_docente,))
        resultados = cursor.fetchall()
        
        # Agregar la posición/puesto a cada estudiante
        ranking = []
        for idx, estudiante in enumerate(resultados, start=1):
            estudiante['posicion'] = idx
            
            # Calcular precisión global
            if estudiante['total_respuestas'] > 0:
                estudiante['precision_global'] = round(
                    (estudiante['total_correctas'] / estudiante['total_respuestas']) * 100, 
                    1
                )
            else:
                estudiante['precision_global'] = 0.0
            
            # Formatear números para mejor visualización
            estudiante['puntaje_acumulado'] = int(estudiante['puntaje_acumulado'])
            estudiante['promedio_puntaje'] = round(estudiante['promedio_puntaje'], 1)
            estudiante['mejor_puntaje'] = int(estudiante['mejor_puntaje']) if estudiante['mejor_puntaje'] else 0
            
            ranking.append(estudiante)
        
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Ranking del docente {id_docente} obtenido con {len(ranking)} estudiantes")
        return ranking
        
    except Exception as e:
        print(f"Error al obtener ranking por docente: {e}")
        import traceback
        traceback.print_exc()
        return []

