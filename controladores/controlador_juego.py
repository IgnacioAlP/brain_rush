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
                SET estado = 'en_juego', 
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
            cursor.execute('''
                INSERT INTO ranking_sala (id_participante, id_sala, puntaje_total, respuestas_correctas, tiempo_total_respuestas)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    puntaje_total = puntaje_total + VALUES(puntaje_total),
                    respuestas_correctas = respuestas_correctas + VALUES(respuestas_correctas),
                    tiempo_total_respuestas = tiempo_total_respuestas + VALUES(tiempo_total_respuestas)
            ''', (participante_id, sala_id, puntaje, 1 if es_correcta else 0, tiempo_respuesta))
            
            conexion.commit()
            
            return {
                'es_correcta': bool(es_correcta),
                'puntaje_obtenido': puntaje,
                'tiempo_respuesta': tiempo_respuesta
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
                # Finalizar juego
                cursor.execute('''
                    UPDATE salas_juego 
                    SET estado = 'finalizado', pregunta_actual = %s
                    WHERE id_sala = %s
                ''', (total_preguntas, sala_id))
                
                cursor.execute('''
                    UPDATE estado_juego_sala
                    SET estado_pregunta = 'finalizada'
                    WHERE id_sala = %s
                ''', (sala_id,))
                
                # Calcular posiciones finales
                calcular_ranking_final(sala_id, cursor)
                
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
            cursor.execute('''
                SELECT 
                    r.posicion,
                    p.nombre_participante,
                    r.puntaje_total,
                    r.respuestas_correctas,
                    r.tiempo_total_respuestas,
                    g.nombre_grupo,
                    p.id_participante
                FROM ranking_sala r
                JOIN participantes_sala p ON r.id_participante = p.id_participante
                LEFT JOIN grupos_sala g ON p.id_grupo = g.id_grupo
                WHERE r.id_sala = %s
                ORDER BY r.puntaje_total DESC, r.tiempo_total_respuestas ASC
            ''', (sala_id,))
            
            ranking = []
            for row in cursor.fetchall():
                ranking.append({
                    'posicion': row[0],  # Usar la posición de la BD
                    'nombre_participante': row[1],
                    'puntaje_total': row[2],
                    'respuestas_correctas': row[3],
                    'tiempo_total_respuestas': float(row[4]),
                    'nombre_grupo': row[5],
                    'id_participante': row[6]
                })
            
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

def finalizar_juego_sala(sala_id):
    """
    Finaliza el juego en una sala
    - Cambia el estado a 'finalizada'
    - Calcula el ranking final
    - Actualiza el estado de los participantes
    
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
