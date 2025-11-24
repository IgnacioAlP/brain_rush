# -*- coding: utf-8 -*-
"""
Controlador para el sistema de juego en tiempo real
Maneja el inicio del juego, respuestas de participantes y cálculo de puntuación
"""

from bd import obtener_conexion
from datetime import datetime
import time

# ==================== CONSTANTES DE PUNTUACIÓN ====================
PUNTAJE_MAXIMO = 1000
PUNTAJE_MINIMO = 10
DECREMENTO_POR_MEDIO_SEGUNDO = 100  # -100 puntos cada 0.5 segundos

def calcular_puntaje(tiempo_respuesta_segundos):
    """
    Calcula el puntaje basado en el tiempo de respuesta
    
    Fórmula: 1000 puntos - (100 puntos por cada 0.5 segundos)
    Mínimo: 10 puntos
    
    Args:
        tiempo_respuesta_segundos: Tiempo en segundos desde que se mostró la pregunta
        
    Returns:
        Puntaje calculado (entre 10 y 1000)
    """
    # Calcular intervalos de 0.5 segundos
    intervalos = int(tiempo_respuesta_segundos / 0.5)
    
    # Calcular puntaje
    puntaje = PUNTAJE_MAXIMO - (intervalos * DECREMENTO_POR_MEDIO_SEGUNDO)
    
    # Asegurar que esté en el rango válido
    return max(PUNTAJE_MINIMO, min(PUNTAJE_MAXIMO, puntaje))

# ==================== GESTIÓN DEL ESTADO DEL JUEGO ====================

def iniciar_juego_sala(sala_id):
    """
    Inicia el juego en una sala
    
    Args:
        sala_id: ID de la sala
        
    Returns:
        True si se inició correctamente, False en caso contrario
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener el cuestionario de la sala
            cursor.execute('''
                SELECT id_cuestionario FROM salas_juego WHERE id_sala = %s
            ''', (sala_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            id_cuestionario = result[0]
            
            # Contar preguntas del cuestionario
            cursor.execute('''
                SELECT COUNT(*) FROM cuestionario_preguntas WHERE id_cuestionario = %s
            ''', (id_cuestionario,))
            
            total_preguntas = cursor.fetchone()[0]
            
            # Actualizar estado de la sala
            cursor.execute('''
                UPDATE salas_juego 
                SET estado = 'en_curso', 
                    pregunta_actual = 1,
                    total_preguntas = %s,
                    tiempo_inicio_juego = NOW()
                WHERE id_sala = %s
            ''', (total_preguntas, sala_id))
            
            # Crear estado inicial del juego
            cursor.execute('''
                INSERT INTO estado_juego_sala (id_sala, pregunta_actual, estado_pregunta)
                VALUES (%s, 1, 'mostrando')
                ON DUPLICATE KEY UPDATE 
                    pregunta_actual = 1,
                    tiempo_inicio_pregunta = NOW(),
                    estado_pregunta = 'mostrando'
            ''', (sala_id,))
            
            # Actualizar estado de participantes
            cursor.execute('''
                UPDATE participantes_sala 
                SET estado = 'jugando' 
                WHERE id_sala = %s AND estado = 'esperando'
            ''', (sala_id,))
            
            # Inicializar ranking para todos los participantes
            cursor.execute('''
                INSERT INTO ranking_sala (id_participante, id_sala, puntaje_total, respuestas_correctas, tiempo_total_respuestas)
                SELECT id_participante, id_sala, 0, 0, 0
                FROM participantes_sala
                WHERE id_sala = %s AND estado = 'jugando'
                ON DUPLICATE KEY UPDATE puntaje_total = 0, respuestas_correctas = 0, tiempo_total_respuestas = 0
            ''', (sala_id,))
            
            conexion.commit()
            
            # Verificar que el estado se actualizó correctamente
            cursor.execute('SELECT estado FROM salas_juego WHERE id_sala = %s', (sala_id,))
            estado_verificado = cursor.fetchone()
            print(f"✅ [CONTROLADOR_JUEGO] Estado verificado después de commit: '{estado_verificado[0] if estado_verificado else 'NULL'}'")
            
            return True
    finally:
        conexion.close()

def obtener_pregunta_actual_sala(sala_id):
    """
    Obtiene la pregunta actual que se está mostrando en la sala
    
    Returns:
        Diccionario con datos de la pregunta, opciones y tiempo de inicio
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Primero verificar el estado de la sala
            cursor.execute('SELECT estado FROM salas_juego WHERE id_sala = %s', (sala_id,))
            sala_estado = cursor.fetchone()
            
            if not sala_estado or sala_estado[0] == 'finalizada':
                return None  # Juego finalizado, no hay pregunta activa
            
            # Obtener estado del juego
            cursor.execute('''
                SELECT 
                    e.pregunta_actual,
                    e.tiempo_inicio_pregunta,
                    e.estado_pregunta,
                    s.id_cuestionario,
                    s.total_preguntas
                FROM estado_juego_sala e
                JOIN salas_juego s ON e.id_sala = s.id_sala
                WHERE e.id_sala = %s
            ''', (sala_id,))
            
            estado = cursor.fetchone()
            if not estado:
                return None
            
            num_pregunta, tiempo_inicio, estado_pregunta, id_cuestionario, total_preguntas = estado
            
            # Validar que num_pregunta sea >= 1
            if num_pregunta < 1:
                return None
            
            # Obtener la pregunta específica
            cursor.execute('''
                SELECT 
                    p.id_pregunta,
                    p.enunciado,
                    p.tipo,
                    cp.orden
                FROM cuestionario_preguntas cp
                JOIN preguntas p ON cp.id_pregunta = p.id_pregunta
                WHERE cp.id_cuestionario = %s
                ORDER BY cp.orden
                LIMIT %s, 1
            ''', (id_cuestionario, num_pregunta - 1))
            
            pregunta_data = cursor.fetchone()
            if not pregunta_data:
                return None
            
            id_pregunta, enunciado, tipo, orden = pregunta_data
            
            # Obtener opciones de respuesta
            cursor.execute('''
                SELECT id_opcion, texto_opcion
                FROM opciones_respuesta
                WHERE id_pregunta = %s
                ORDER BY id_opcion
            ''', (id_pregunta,))
            
            opciones = []
            for opcion in cursor.fetchall():
                opciones.append({
                    'id_opcion': opcion[0],
                    'texto': opcion[1]
                })
            
            return {
                'id_pregunta': id_pregunta,
                'enunciado': enunciado,
                'tipo': tipo,
                'numero_pregunta': num_pregunta,
                'total_preguntas': total_preguntas,
                'opciones': opciones,
                'tiempo_inicio': tiempo_inicio,
                'estado': estado_pregunta
            }
    finally:
        conexion.close()

def registrar_respuesta_participante(participante_id, sala_id, id_pregunta, id_opcion_seleccionada, tiempo_respuesta):
    """
    Registra la respuesta de un participante y calcula el puntaje
    
    Args:
        participante_id: ID del participante
        sala_id: ID de la sala
        id_pregunta: ID de la pregunta respondida
        id_opcion_seleccionada: ID de la opción seleccionada
        tiempo_respuesta: Tiempo en segundos desde que se mostró la pregunta
        
    Returns:
        Diccionario con información del resultado (puntaje, es_correcta, etc.)
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si la respuesta es correcta
            cursor.execute('''
                SELECT es_correcta 
                FROM opciones_respuesta 
                WHERE id_opcion = %s
            ''', (id_opcion_seleccionada,))
            
            result = cursor.fetchone()
            es_correcta = result[0] if result else 0
            
            # Calcular puntaje solo si es correcta
            puntaje = calcular_puntaje(tiempo_respuesta) if es_correcta else 0
            
            # Registrar respuesta
            cursor.execute('''
                INSERT INTO respuestas_participantes 
                (id_participante, id_sala, id_pregunta, id_opcion_seleccionada, tiempo_respuesta, es_correcta, puntaje_obtenido)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    id_opcion_seleccionada = VALUES(id_opcion_seleccionada),
                    tiempo_respuesta = VALUES(tiempo_respuesta),
                    es_correcta = VALUES(es_correcta),
                    puntaje_obtenido = VALUES(puntaje_obtenido)
            ''', (participante_id, sala_id, id_pregunta, id_opcion_seleccionada, tiempo_respuesta, es_correcta, puntaje))
            
            # Actualizar o crear ranking del participante
            print(f"🔄 Actualizando ranking: participante={participante_id}, sala={sala_id}, puntaje={puntaje}, es_correcta={es_correcta}")
            cursor.execute('''
                INSERT INTO ranking_sala (id_participante, id_sala, puntaje_total, respuestas_correctas, tiempo_total_respuestas)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    puntaje_total = puntaje_total + VALUES(puntaje_total),
                    respuestas_correctas = respuestas_correctas + VALUES(respuestas_correctas),
                    tiempo_total_respuestas = tiempo_total_respuestas + VALUES(tiempo_total_respuestas)
            ''', (participante_id, sala_id, puntaje, 1 if es_correcta else 0, tiempo_respuesta))
            
            # Verificar el ranking actualizado
            cursor.execute('SELECT puntaje_total, respuestas_correctas FROM ranking_sala WHERE id_participante=%s AND id_sala=%s', 
                          (participante_id, sala_id))
            ranking_actual = cursor.fetchone()
            print(f"✅ Ranking actualizado: puntaje_total={ranking_actual[0]}, respuestas_correctas={ranking_actual[1]}")
            
            # ==================== SISTEMA DE XP E INSIGNIAS ====================
            # Obtener id_usuario del participante
            cursor.execute('SELECT id_usuario FROM participantes_sala WHERE id_participante = %s', (participante_id,))
            usuario_data = cursor.fetchone()
            
            resultado_xp = None
            if usuario_data:
                id_usuario = usuario_data[0]
                
                # Verificar que sea estudiante
                cursor.execute('SELECT tipo_usuario FROM usuarios WHERE id_usuario = %s', (id_usuario,))
                tipo_usuario = cursor.fetchone()
                
                if tipo_usuario and tipo_usuario[0] == 'estudiante':
                    # Importar controlador de XP
                    try:
                        from controladores import controlador_xp
                        
                        # Actualizar estadísticas
                        racha_actual = controlador_xp.actualizar_estadisticas_respuesta(
                            id_usuario, es_correcta, tiempo_respuesta
                        )
                        
                        # Otorgar XP si la respuesta es correcta
                        if es_correcta:
                            xp_ganado = controlador_xp.calcular_xp_por_respuesta(
                                tiempo_respuesta, es_correcta, racha_actual - 1
                            )
                            
                            resultado_xp = controlador_xp.otorgar_xp(
                                id_usuario, xp_ganado, 'respuesta_correcta', sala_id, id_pregunta
                            )
                            
                            print(f"🎯 XP otorgado: {xp_ganado} XP a usuario {id_usuario}")
                            if resultado_xp and resultado_xp['subio_nivel']:
                                print(f"⬆️ ¡Subió de nivel {resultado_xp['nivel_anterior']} → {resultado_xp['nivel_nuevo']}!")
                            if resultado_xp and resultado_xp['insignias_nuevas']:
                                print(f"🏆 Insignias desbloqueadas: {len(resultado_xp['insignias_nuevas'])}")
                    except Exception as e_xp:
                        print(f"⚠️ Error al procesar XP (no crítico): {e_xp}")
            
            conexion.commit()
            
            return {
                'es_correcta': bool(es_correcta),
                'puntaje_obtenido': puntaje,
                'tiempo_respuesta': tiempo_respuesta,
                'xp_info': resultado_xp  # Información de XP ganado
            }
    finally:
        conexion.close()

def avanzar_siguiente_pregunta(sala_id):
    """
    Avanza a la siguiente pregunta de la sala
    
    Returns:
        True si avanzó, False si ya no hay más preguntas
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener estado actual
            cursor.execute('''
                SELECT e.pregunta_actual, s.total_preguntas
                FROM estado_juego_sala e
                JOIN salas_juego s ON e.id_sala = s.id_sala
                WHERE e.id_sala = %s
            ''', (sala_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            pregunta_actual, total_preguntas = result
            
            # Verificar si hay más preguntas
            if pregunta_actual >= total_preguntas:
                # NO finalizar automáticamente cuando se avanza a la última pregunta
                # El docente debe finalizar manualmente
                # Solo retornar que no hay más preguntas
                conexion.commit()
                return False
            
            # Avanzar a siguiente pregunta
            siguiente_pregunta = pregunta_actual + 1
            
            cursor.execute('''
                UPDATE salas_juego 
                SET pregunta_actual = %s
                WHERE id_sala = %s
            ''', (siguiente_pregunta, sala_id))
            
            cursor.execute('''
                UPDATE estado_juego_sala
                SET pregunta_actual = %s,
                    tiempo_inicio_pregunta = NOW(),
                    estado_pregunta = 'mostrando'
                WHERE id_sala = %s
            ''', (siguiente_pregunta, sala_id))
            
            conexion.commit()
            return True
    finally:
        conexion.close()

def calcular_ranking_final(sala_id, cursor=None):
    """
    Calcula las posiciones finales del ranking
    Ordena por: puntaje DESC, luego tiempo_total ASC (más rápido gana)
    """
    cerrar_conexion = False
    conexion_local = None
    
    if cursor is None:
        conexion_local = obtener_conexion()
        cursor = conexion_local.cursor()
        cerrar_conexion = True
    
    try:
        # Obtener ranking ordenado
        cursor.execute('''
            SELECT id_ranking_sala
            FROM ranking_sala
            WHERE id_sala = %s
            ORDER BY puntaje_total DESC, tiempo_total_respuestas ASC
        ''', (sala_id,))
        
        rankings = cursor.fetchall()
        
        # Actualizar posiciones
        for posicion, (id_ranking,) in enumerate(rankings, start=1):
            cursor.execute('''
                UPDATE ranking_sala 
                SET posicion = %s 
                WHERE id_ranking_sala = %s
            ''', (posicion, id_ranking))
        
        if cerrar_conexion and conexion_local:
            conexion_local.commit()
    finally:
        if cerrar_conexion and conexion_local:
            cursor.close()
            conexion_local.close()

def obtener_ranking_sala(sala_id):
    """
    Obtiene el ranking actual de una sala
    
    Returns:
        Lista de participantes ordenados por puntaje y tiempo
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print(f"\n📊 Obteniendo ranking para sala {sala_id}...")
            
            cursor.execute('''
                SELECT 
                    r.posicion,
                    COALESCE(CONCAT(u.nombre, ' ', u.apellidos), p.nombre_participante) as nombre_completo,
                    r.puntaje_total,
                    r.respuestas_correctas,
                    r.tiempo_total_respuestas,
                    g.numero_grupo,
                    p.id_participante
                FROM ranking_sala r
                JOIN participantes_sala p ON r.id_participante = p.id_participante
                LEFT JOIN usuarios u ON p.id_usuario = u.id_usuario
                LEFT JOIN grupos_sala g ON p.id_grupo = g.id_grupo
                WHERE r.id_sala = %s
                ORDER BY r.puntaje_total DESC, r.tiempo_total_respuestas ASC
            ''', (sala_id,))
            
            ranking = []
            for row in cursor.fetchall():
                print(f"   👤 {row[1]}: {row[2]} puntos, {row[3]} correctas")
                ranking.append({
                    'posicion': row[0],
                    'nombre_completo': row[1],
                    'puntos_totales': row[2],  # Cambio de puntaje_total a puntos_totales para consistencia
                    'respuestas_correctas': row[3],
                    'tiempo_total_respuestas': float(row[4]),
                    'numero_grupo': row[5],
                    'id_participante': row[6]
                })
            
            print(f"✅ Total participantes en ranking: {len(ranking)}\n")
            return ranking
    finally:
        conexion.close()

def obtener_estadisticas_pregunta_actual(sala_id):
    """
    Obtiene estadísticas de cuántos participantes han respondido la pregunta actual
    
    Returns:
        Diccionario con total de participantes y cuántos han respondido
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Total de participantes activos
            cursor.execute('''
                SELECT COUNT(*) 
                FROM participantes_sala 
                WHERE id_sala = %s AND estado = 'jugando'
            ''', (sala_id,))
            
            total_participantes = cursor.fetchone()[0]
            
            # Pregunta actual
            cursor.execute('''
                SELECT pregunta_actual FROM salas_juego WHERE id_sala = %s
            ''', (sala_id,))
            
            pregunta_actual = cursor.fetchone()[0]
            
            # Cuántos han respondido
            cursor.execute('''
                SELECT COUNT(DISTINCT id_participante)
                FROM respuestas_participantes
                WHERE id_sala = %s AND id_pregunta = (
                    SELECT p.id_pregunta
                    FROM cuestionario_preguntas cp
                    JOIN preguntas p ON cp.id_pregunta = p.id_pregunta
                    JOIN salas_juego s ON cp.id_cuestionario = s.id_cuestionario
                    WHERE s.id_sala = %s
                    ORDER BY cp.orden
                    LIMIT %s, 1
                )
            ''', (sala_id, sala_id, pregunta_actual - 1))
            
            respondieron = cursor.fetchone()[0]
            
            return {
                'total': total_participantes,
                'respondieron': respondieron,
                'pendientes': total_participantes - respondieron
            }
    finally:
        conexion.close()

def obtener_detalle_respuestas_estudiantes(sala_id):
    """
    Obtiene el detalle de qué estudiantes han respondido la pregunta actual
    
    Returns:
        Diccionario con lista de estudiantes, tiempo de inicio de pregunta y estadísticas
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener pregunta actual, tiempo de inicio y tiempo configurado por pregunta
            cursor.execute('''
                SELECT ejs.pregunta_actual, ejs.tiempo_inicio_pregunta, s.id_cuestionario, s.tiempo_por_pregunta
                FROM estado_juego_sala ejs
                JOIN salas_juego s ON ejs.id_sala = s.id_sala
                WHERE ejs.id_sala = %s
            ''', (sala_id,))
            
            estado = cursor.fetchone()
            if not estado:
                return None
            
            num_pregunta_actual = estado[0]
            tiempo_inicio = estado[1]
            id_cuestionario = estado[2]
            tiempo_por_pregunta = estado[3]  # Tiempo límite configurado (en segundos)
            
            # Obtener id_pregunta actual
            cursor.execute('''
                SELECT p.id_pregunta
                FROM cuestionario_preguntas cp
                JOIN preguntas p ON cp.id_pregunta = p.id_pregunta
                WHERE cp.id_cuestionario = %s
                ORDER BY cp.orden
                LIMIT %s, 1
            ''', (id_cuestionario, num_pregunta_actual - 1))
            
            pregunta_result = cursor.fetchone()
            if not pregunta_result:
                return None
            
            id_pregunta_actual = pregunta_result[0]
            
            # Obtener todos los participantes con su estado de respuesta
            cursor.execute('''
                SELECT 
                    ps.id_participante,
                    CONCAT(u.nombre, ' ', u.apellidos) as nombre_completo,
                    COALESCE(gs.numero_grupo, ps.id_grupo, 0) as numero_grupo,
                    CASE 
                        WHEN rp.id_respuesta_participante IS NOT NULL THEN 1 
                        ELSE 0 
                    END as ha_respondido,
                    rp.tiempo_respuesta,
                    rp.es_correcta,
                    rp.puntaje_obtenido
                FROM participantes_sala ps
                JOIN usuarios u ON ps.id_usuario = u.id_usuario
                LEFT JOIN grupos_sala gs ON ps.id_grupo = gs.id_grupo
                LEFT JOIN respuestas_participantes rp ON 
                    rp.id_participante = ps.id_participante 
                    AND rp.id_sala = ps.id_sala
                    AND rp.id_pregunta = %s
                WHERE ps.id_sala = %s AND ps.estado = 'jugando'
                ORDER BY ha_respondido DESC, nombre_completo ASC
            ''', (id_pregunta_actual, sala_id))
            
            estudiantes = []
            total = 0
            respondieron = 0
            
            for row in cursor.fetchall():
                total += 1
                ha_respondido = bool(row[3])
                if ha_respondido:
                    respondieron += 1
                
                estudiantes.append({
                    'id_participante': row[0],
                    'nombre': row[1],
                    'grupo': row[2],
                    'ha_respondido': ha_respondido,
                    'tiempo_respuesta': float(row[4]) if row[4] else None,
                    'es_correcta': bool(row[5]) if row[5] is not None else None,
                    'puntaje': row[6] if row[6] else None
                })
            
            return {
                'estudiantes': estudiantes,
                'tiempo_inicio_pregunta': tiempo_inicio.isoformat() if tiempo_inicio else None,
                'tiempo_por_pregunta': tiempo_por_pregunta,  # Tiempo límite configurado
                'numero_pregunta_actual': num_pregunta_actual,  # Número de pregunta para detectar cambios
                'estadisticas': {
                    'total': total,
                    'respondieron': respondieron,
                    'pendientes': total - respondieron,
                    'porcentaje': round((respondieron / total * 100) if total > 0 else 0, 1)
                }
            }
    finally:
        conexion.close()

def finalizar_juego_sala(sala_id):
    """
    Finaliza el juego en una sala
    - Cambia el estado a 'finalizada'
    - Calcula el ranking final
    - Actualiza el estado de los participantes
    - Asigna recompensas automáticamente a los 3 primeros puestos
    
    Returns:
        True si se finalizó correctamente
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Calcular ranking final
            calcular_ranking_final(sala_id, cursor)
            
            # Actualizar estado de la sala
            cursor.execute('''
                UPDATE salas_juego 
                SET estado = 'finalizada'
                WHERE id_sala = %s
            ''', (sala_id,))
            
            # Actualizar estado de participantes
            cursor.execute('''
                UPDATE participantes_sala 
                SET estado = 'finalizado'
                WHERE id_sala = %s
            ''', (sala_id,))
            
            conexion.commit()
            print(f"✅ Juego finalizado para sala {sala_id}")
            
            # Asignar recompensas automáticamente a los 3 primeros puestos
            try:
                from controladores import controlador_recompensas
                resultado_recompensas = controlador_recompensas.asignar_recompensas_top3(sala_id)
                
                if resultado_recompensas['success']:
                    print(f"🏆 Recompensas asignadas: {resultado_recompensas['total_asignadas']}")
                    for recompensa in resultado_recompensas.get('recompensas', []):
                        print(f"   - {recompensa['nombre_participante']}: {recompensa['recompensa']} ({recompensa['tipo']})")
                else:
                    print(f"⚠️ No se pudieron asignar recompensas: {resultado_recompensas.get('error', 'Error desconocido')}")
            except Exception as e_recompensas:
                # No fallar el finalizamiento del juego si hay error en las recompensas
                print(f"⚠️ Error al asignar recompensas (no crítico): {e_recompensas}")
            
            return True
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al finalizar juego: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conexion.close()

def obtener_resultado_participante(sala_id, participante_id):
    """
    Obtiene el resultado de un participante específico en una sala
    
    Returns:
        Diccionario con posición, puntaje, respuestas correctas, etc.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    r.posicion,
                    r.puntaje_total,
                    r.respuestas_correctas,
                    r.tiempo_total_respuestas,
                    p.nombre_participante,
                    s.total_preguntas
                FROM ranking_sala r
                JOIN participantes_sala p ON r.id_participante = p.id_participante
                JOIN salas_juego s ON r.id_sala = s.id_sala
                WHERE r.id_sala = %s AND r.id_participante = %s
            ''', (sala_id, participante_id))
            
            result = cursor.fetchone()
            if not result:
                return None
            
            return {
                'posicion': result[0],
                'puntaje_total': result[1],
                'respuestas_correctas': result[2],
                'tiempo_total': float(result[3]),
                'nombre': result[4],
                'total_preguntas': result[5]
            }
    finally:
        conexion.close()
