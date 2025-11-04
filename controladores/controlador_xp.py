# -*- coding: utf-8 -*-
"""
Controlador para el sistema de XP, Niveles e Insignias
Gestiona la experiencia de los estudiantes y el desbloqueo de logros
"""

from bd import obtener_conexion
from datetime import datetime
import math

# ==================== CONSTANTES DEL SISTEMA ====================
XP_POR_RESPUESTA_CORRECTA = 10  # XP base por respuesta correcta (CAMBIADO A 10)
XP_POR_VICTORIA = 50  # XP extra por ganar una partida
XP_BONUS_VELOCIDAD = 5  # XP extra por responder rápido (< 3 segundos)
XP_BONUS_RACHA = 3  # XP extra por cada respuesta en racha

# Fórmula de XP necesario por nivel: XP_needed = 100 * level^1.5
def calcular_xp_para_nivel(nivel):
    """
    Calcula cuánto XP se necesita para alcanzar un nivel específico
    Fórmula exponencial: 100 * nivel^1.5
    """
    return int(100 * math.pow(nivel, 1.5))

def calcular_nivel_por_xp(xp_total):
    """
    Calcula el nivel correspondiente a un total de XP acumulado
    """
    nivel = 1
    xp_acumulado = 0
    
    while True:
        xp_necesario = calcular_xp_para_nivel(nivel)
        if xp_acumulado + xp_necesario > xp_total:
            break
        xp_acumulado += xp_necesario
        nivel += 1
    
    return nivel, xp_total - xp_acumulado

# ==================== GESTIÓN DE XP ====================

def otorgar_xp(id_usuario, cantidad_xp, razon, id_sala=None, id_pregunta=None):
    """
    Otorga XP a un usuario y actualiza su nivel si es necesario
    
    Returns:
        dict con información de la transacción (xp_ganado, nivel_anterior, nivel_nuevo, subio_nivel, insignias_nuevas)
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener experiencia actual
            cursor.execute('''
                SELECT xp_actual, nivel_actual, xp_total_acumulado 
                FROM experiencia_usuarios 
                WHERE id_usuario = %s
            ''', (id_usuario,))
            
            exp_data = cursor.fetchone()
            if not exp_data:
                # Crear registro si no existe (solo para estudiantes)
                cursor.execute('SELECT tipo_usuario FROM usuarios WHERE id_usuario = %s', (id_usuario,))
                user_type = cursor.fetchone()
                if user_type and user_type[0] == 'estudiante':
                    cursor.execute('''
                        INSERT INTO experiencia_usuarios (id_usuario, xp_actual, nivel_actual, xp_total_acumulado)
                        VALUES (%s, 0, 1, 0)
                    ''', (id_usuario,))
                    exp_data = (0, 1, 0)
                else:
                    return None  # No otorgar XP a docentes
            
            xp_actual, nivel_actual, xp_total = exp_data
            nuevo_xp_actual = xp_actual + cantidad_xp
            nuevo_xp_total = xp_total + cantidad_xp
            nivel_anterior = nivel_actual
            
            # Calcular si subió de nivel
            xp_necesario = calcular_xp_para_nivel(nivel_actual + 1)
            niveles_ganados = 0
            
            while nuevo_xp_actual >= xp_necesario:
                nuevo_xp_actual -= xp_necesario
                nivel_actual += 1
                niveles_ganados += 1
                xp_necesario = calcular_xp_para_nivel(nivel_actual + 1)
            
            # Actualizar experiencia
            cursor.execute('''
                UPDATE experiencia_usuarios 
                SET xp_actual = %s, nivel_actual = %s, xp_total_acumulado = %s
                WHERE id_usuario = %s
            ''', (nuevo_xp_actual, nivel_actual, nuevo_xp_total, id_usuario))
            
            # Registrar en historial
            cursor.execute('''
                INSERT INTO historial_xp (id_usuario, cantidad_xp, razon, id_sala, id_pregunta)
                VALUES (%s, %s, %s, %s, %s)
            ''', (id_usuario, cantidad_xp, razon, id_sala, id_pregunta))
            
            # Bonus por subir de nivel
            if niveles_ganados > 0:
                bonus_xp = niveles_ganados * 50
                cursor.execute('''
                    INSERT INTO historial_xp (id_usuario, cantidad_xp, razon)
                    VALUES (%s, %s, 'bonus_nivel')
                ''', (id_usuario, bonus_xp))
            
            conexion.commit()
            
            # Verificar insignias desbloqueadas
            insignias_nuevas = verificar_y_desbloquear_insignias(id_usuario)
            
            return {
                'xp_ganado': cantidad_xp,
                'xp_actual': nuevo_xp_actual,
                'xp_total': nuevo_xp_total,
                'nivel_anterior': nivel_anterior,
                'nivel_nuevo': nivel_actual,
                'subio_nivel': niveles_ganados > 0,
                'niveles_ganados': niveles_ganados,
                'xp_para_siguiente_nivel': xp_necesario,
                'porcentaje_nivel': round((nuevo_xp_actual / xp_necesario) * 100, 1),
                'insignias_nuevas': insignias_nuevas
            }
    finally:
        conexion.close()

def calcular_xp_por_respuesta(tiempo_respuesta, es_correcta, racha_actual=0):
    """
    Calcula el XP a otorgar por una respuesta según múltiples factores
    """
    if not es_correcta:
        return 0
    
    xp_total = XP_POR_RESPUESTA_CORRECTA
    
    # Bonus por velocidad (< 3 segundos)
    if tiempo_respuesta < 3.0:
        xp_total += XP_BONUS_VELOCIDAD
    
    # Bonus por racha (convertir racha_actual a int para evitar errores con Decimal)
    if racha_actual > 0:
        xp_total += min(int(racha_actual) * XP_BONUS_RACHA, 50)  # Máximo 50 XP de bonus por racha
    
    return xp_total

# ==================== GESTIÓN DE ESTADÍSTICAS ====================

def actualizar_estadisticas_respuesta(id_usuario, es_correcta, tiempo_respuesta):
    """
    Actualiza las estadísticas del usuario después de responder una pregunta
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener estadísticas actuales
            cursor.execute('SELECT * FROM estadisticas_juego WHERE id_usuario = %s', (id_usuario,))
            stats = cursor.fetchone()
            
            if not stats:
                # Crear estadísticas si no existen
                cursor.execute('INSERT INTO estadisticas_juego (id_usuario) VALUES (%s)', (id_usuario,))
                stats = (None, id_usuario, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, None, None)
            
            # Convertir valores de la BD a int para evitar problemas con Decimal
            total_correctas = int(stats[3]) if stats[3] else 0
            total_incorrectas = int(stats[4]) if stats[4] else 0
            racha_actual = int(stats[5]) if stats[5] else 0
            racha_maxima = int(stats[6]) if stats[6] else 0
            
            # Actualizar racha
            if es_correcta:
                total_correctas += 1
                racha_actual += 1
                racha_maxima = max(racha_maxima, racha_actual)
            else:
                total_incorrectas += 1
                racha_actual = 0
            
            # Calcular nueva precisión
            total_respuestas = total_correctas + total_incorrectas
            nueva_precision = (total_correctas / total_respuestas * 100) if total_respuestas > 0 else 0
            
            # Actualizar tiempo promedio (convertir Decimal a float para evitar errores)
            tiempo_promedio_actual = float(stats[8]) if stats[8] else 0.0
            if tiempo_promedio_actual == 0:
                nuevo_tiempo_promedio = float(tiempo_respuesta)
            else:
                nuevo_tiempo_promedio = (tiempo_promedio_actual * (total_respuestas - 1) + float(tiempo_respuesta)) / total_respuestas
            
            cursor.execute('''
                UPDATE estadisticas_juego 
                SET total_respuestas_correctas = %s,
                    total_respuestas_incorrectas = %s,
                    racha_actual = %s,
                    racha_maxima = %s,
                    precision_promedio = %s,
                    tiempo_promedio_respuesta = %s,
                    fecha_ultima_partida = NOW()
                WHERE id_usuario = %s
            ''', (total_correctas, total_incorrectas, racha_actual, racha_maxima, 
                  nueva_precision, nuevo_tiempo_promedio, id_usuario))
            
            conexion.commit()
            return racha_actual
    finally:
        conexion.close()

def actualizar_estadisticas_partida(id_usuario, gano=False):
    """
    Actualiza las estadísticas después de completar una partida
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE estadisticas_juego 
                SET total_partidas_jugadas = total_partidas_jugadas + 1,
                    total_partidas_ganadas = total_partidas_ganadas + %s,
                    fecha_ultima_partida = NOW()
                WHERE id_usuario = %s
            ''', (1 if gano else 0, id_usuario))
            conexion.commit()
    finally:
        conexion.close()

# ==================== GESTIÓN DE INSIGNIAS ====================

def verificar_y_desbloquear_insignias(id_usuario):
    """
    Verifica si el usuario cumple los requisitos para nuevas insignias
    y las desbloquea automáticamente
    
    Returns:
        Lista de insignias recién desbloqueadas
    """
    conexion = obtener_conexion()
    insignias_nuevas = []
    
    try:
        with conexion.cursor() as cursor:
            # Obtener estadísticas del usuario
            cursor.execute('''
                SELECT e.nivel_actual, s.total_partidas_jugadas, s.racha_maxima, 
                       s.precision_promedio, s.tiempo_promedio_respuesta
                FROM experiencia_usuarios e
                LEFT JOIN estadisticas_juego s ON e.id_usuario = s.id_usuario
                WHERE e.id_usuario = %s
            ''', (id_usuario,))
            
            stats = cursor.fetchone()
            if not stats:
                return []
            
            nivel, partidas, racha, precision, tiempo = stats
            
            # Valores predeterminados si no hay estadísticas
            nivel = nivel or 1
            partidas = partidas or 0
            racha = racha or 0
            precision = precision or 0
            tiempo = tiempo or 0
            
            # Obtener insignias aún no desbloqueadas
            cursor.execute('''
                SELECT ic.id_insignia, ic.nombre, ic.descripcion, ic.icono, ic.tipo,
                       ic.requisito_tipo, ic.requisito_valor, ic.xp_bonus, ic.rareza, ic.color_hex
                FROM insignias_catalogo ic
                WHERE ic.activo = TRUE
                AND ic.id_insignia NOT IN (
                    SELECT id_insignia FROM insignias_usuarios WHERE id_usuario = %s
                )
            ''', (id_usuario,))
            
            insignias_disponibles = cursor.fetchall()
            
            for insignia in insignias_disponibles:
                id_insignia, nombre, descripcion, icono, tipo, req_tipo, req_valor, xp_bonus, rareza, color = insignia
                cumple_requisito = False
                
                # Verificar según tipo de requisito
                if req_tipo == 'nivel' and nivel >= req_valor:
                    cumple_requisito = True
                elif req_tipo == 'partidas' and partidas >= req_valor:
                    cumple_requisito = True
                elif req_tipo == 'racha' and racha >= req_valor:
                    cumple_requisito = True
                elif req_tipo == 'precision' and precision >= req_valor:
                    cumple_requisito = True
                elif req_tipo == 'velocidad' and tiempo > 0 and tiempo <= req_valor:
                    cumple_requisito = True
                
                # Desbloquear si cumple
                if cumple_requisito:
                    cursor.execute('''
                        INSERT INTO insignias_usuarios (id_usuario, id_insignia)
                        VALUES (%s, %s)
                    ''', (id_usuario, id_insignia))
                    
                    # Otorgar XP bonus
                    if xp_bonus > 0:
                        cursor.execute('''
                            INSERT INTO historial_xp (id_usuario, cantidad_xp, razon)
                            VALUES (%s, %s, %s)
                        ''', (id_usuario, xp_bonus, f'insignia_{nombre}'))
                        
                        cursor.execute('''
                            UPDATE experiencia_usuarios 
                            SET xp_actual = xp_actual + %s, xp_total_acumulado = xp_total_acumulado + %s
                            WHERE id_usuario = %s
                        ''', (xp_bonus, xp_bonus, id_usuario))
                    
                    insignias_nuevas.append({
                        'id': id_insignia,
                        'nombre': nombre,
                        'descripcion': descripcion,
                        'icono': icono,
                        'tipo': tipo,
                        'xp_bonus': xp_bonus,
                        'rareza': rareza,
                        'color': color
                    })
            
            conexion.commit()
            return insignias_nuevas
    finally:
        conexion.close()

def obtener_insignias_usuario(id_usuario):
    """
    Obtiene todas las insignias desbloqueadas por un usuario
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT ic.id_insignia, ic.nombre, ic.descripcion, ic.icono, ic.tipo,
                       ic.rareza, ic.color_hex, iu.fecha_desbloqueo, iu.mostrar_perfil
                FROM insignias_usuarios iu
                JOIN insignias_catalogo ic ON iu.id_insignia = ic.id_insignia
                WHERE iu.id_usuario = %s
                ORDER BY iu.fecha_desbloqueo DESC
            ''', (id_usuario,))
            
            insignias = []
            for row in cursor.fetchall():
                insignias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'icono': row[3],
                    'tipo': row[4],
                    'rareza': row[5],
                    'color': row[6],
                    'fecha_desbloqueo': row[7],
                    'mostrar_perfil': bool(row[8])
                })
            
            return insignias
    finally:
        conexion.close()

def obtener_progreso_insignias(id_usuario):
    """
    Obtiene el progreso del usuario hacia insignias no desbloqueadas
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener estadísticas
            cursor.execute('''
                SELECT e.nivel_actual, s.total_partidas_jugadas, s.racha_maxima, 
                       s.precision_promedio, s.tiempo_promedio_respuesta
                FROM experiencia_usuarios e
                LEFT JOIN estadisticas_juego s ON e.id_usuario = s.id_usuario
                WHERE e.id_usuario = %s
            ''', (id_usuario,))
            
            stats = cursor.fetchone()
            if not stats:
                return []
            
            nivel, partidas, racha, precision, tiempo = stats
            
            # Valores predeterminados si son None
            nivel = nivel or 1
            partidas = partidas or 0
            racha = racha or 0
            precision = precision or 0.0
            tiempo = tiempo or 0.0
            
            # Obtener insignias bloqueadas (excluir las comprables)
            cursor.execute('''
                SELECT ic.id_insignia, ic.nombre, ic.descripcion, ic.icono, ic.tipo,
                       ic.requisito_tipo, ic.requisito_valor, ic.rareza, ic.color_hex
                FROM insignias_catalogo ic
                WHERE ic.activo = TRUE
                AND (ic.precio_xp IS NULL OR ic.precio_xp = 0)
                AND ic.id_insignia NOT IN (
                    SELECT id_insignia FROM insignias_usuarios WHERE id_usuario = %s
                )
                ORDER BY ic.orden_visualizacion, ic.requisito_valor
            ''', (id_usuario,))
            
            insignias_bloqueadas = []
            for row in cursor.fetchall():
                req_tipo = row[5]
                req_valor = row[6]
                
                # Calcular progreso actual con valores seguros
                valor_actual = 0
                if req_tipo == 'nivel':
                    valor_actual = nivel
                elif req_tipo == 'partidas':
                    valor_actual = partidas
                elif req_tipo == 'racha':
                    valor_actual = racha
                elif req_tipo == 'precision':
                    valor_actual = precision
                elif req_tipo == 'velocidad':
                    valor_actual = tiempo if tiempo > 0 else 999
                
                # Asegurar que valor_actual no sea None antes de calcular porcentaje
                valor_actual = valor_actual or 0
                porcentaje = min(100, (valor_actual / req_valor * 100)) if req_valor > 0 else 0
                
                insignias_bloqueadas.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'icono': row[3],
                    'tipo': row[4],
                    'requisito_tipo': req_tipo,
                    'requisito_valor': req_valor,
                    'valor_actual': round(valor_actual, 2),
                    'porcentaje': round(porcentaje, 1),
                    'rareza': row[7],
                    'color': row[8]
                })
            
            return insignias_bloqueadas
    finally:
        conexion.close()

def obtener_todas_insignias_usuario(id_usuario):
    """
    Obtiene TODAS las insignias (desbloqueadas y bloqueadas) de un usuario
    con información de progreso
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener estadísticas del usuario
            cursor.execute('''
                SELECT e.nivel_actual, s.total_partidas_jugadas, s.racha_maxima, 
                       s.precision_promedio, s.tiempo_promedio_respuesta
                FROM experiencia_usuarios e
                LEFT JOIN estadisticas_juego s ON e.id_usuario = s.id_usuario
                WHERE e.id_usuario = %s
            ''', (id_usuario,))
            
            stats = cursor.fetchone()
            nivel = stats[0] if stats and stats[0] else 1
            partidas = stats[1] if stats and stats[1] else 0
            racha = stats[2] if stats and stats[2] else 0
            precision = stats[3] if stats and stats[3] else 0.0
            tiempo = stats[4] if stats and stats[4] else 0.0
            
            # Obtener TODAS las insignias del catálogo (comprables y no comprables)
            cursor.execute('''
                SELECT ic.id_insignia, ic.nombre, ic.descripcion, ic.icono, ic.tipo,
                       ic.requisito_tipo, ic.requisito_valor, ic.rareza, ic.color_hex,
                       ic.xp_bonus, ic.precio_xp,
                       iu.fecha_desbloqueo,
                       iu.id_insignia IS NOT NULL as desbloqueada
                FROM insignias_catalogo ic
                LEFT JOIN insignias_usuarios iu ON ic.id_insignia = iu.id_insignia 
                    AND iu.id_usuario = %s
                WHERE ic.activo = TRUE
                ORDER BY 
                    CASE WHEN iu.id_insignia IS NOT NULL THEN 0 ELSE 1 END,
                    iu.fecha_desbloqueo DESC,
                    ic.rareza DESC,
                    ic.orden_visualizacion,
                    ic.nombre
            ''', (id_usuario,))
            
            insignias = []
            for row in cursor.fetchall():
                desbloqueada = bool(row[12])
                
                # Calcular progreso para insignias bloqueadas
                progreso = 100 if desbloqueada else 0
                
                if not desbloqueada and row[5]:  # Si no está desbloqueada y tiene requisito
                    req_tipo = row[5]
                    req_valor = row[6] or 0
                    
                    valor_actual = 0
                    if req_tipo == 'nivel':
                        valor_actual = nivel
                    elif req_tipo == 'partidas':
                        valor_actual = partidas
                    elif req_tipo == 'racha':
                        valor_actual = racha
                    elif req_tipo == 'precision':
                        valor_actual = precision
                    elif req_tipo == 'velocidad':
                        valor_actual = tiempo if tiempo > 0 else 999
                    
                    if req_valor > 0:
                        progreso = min(100, round((valor_actual / req_valor) * 100, 1))
                
                insignias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'icono': row[3],
                    'tipo': row[4],
                    'rareza': row[7],
                    'color': row[8],
                    'xp_bonus': row[9] or 0,
                    'precio_xp': row[10],
                    'desbloqueada': desbloqueada,
                    'fecha_obtencion': row[11].isoformat() if row[11] else None,
                    'progreso': progreso
                })
            
            return insignias
    finally:
        conexion.close()

# ==================== PERFIL Y RANKING ====================

def obtener_perfil_xp(id_usuario):
    """
    Obtiene toda la información de XP, nivel e insignias de un usuario
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Datos del usuario
            cursor.execute('''
                SELECT CONCAT(nombre, ' ', apellidos) as nombre_completo, email
                FROM usuarios
                WHERE id_usuario = %s
            ''', (id_usuario,))
            
            usuario_data = cursor.fetchone()
            if not usuario_data:
                return None
            
            nombre_completo, email = usuario_data
            
            # Experiencia y nivel
            cursor.execute('''
                SELECT xp_actual, nivel_actual, xp_total_acumulado
                FROM experiencia_usuarios
                WHERE id_usuario = %s
            ''', (id_usuario,))
            
            exp_data = cursor.fetchone()
            if not exp_data:
                return None
            
            xp_actual, nivel, xp_total = exp_data
            xp_para_siguiente = calcular_xp_para_nivel(nivel + 1)
            porcentaje_nivel = round((xp_actual / xp_para_siguiente) * 100, 1)
            
            # Estadísticas
            cursor.execute('''
                SELECT total_partidas_jugadas, total_partidas_ganadas, 
                       total_respuestas_correctas, total_respuestas_incorrectas,
                       racha_actual, racha_maxima, precision_promedio, tiempo_promedio_respuesta
                FROM estadisticas_juego
                WHERE id_usuario = %s
            ''', (id_usuario,))
            
            stats_data = cursor.fetchone()
            
            # Insignias desbloqueadas (contar directamente de la BD)
            cursor.execute('''
                SELECT COUNT(*) FROM insignias_usuarios WHERE id_usuario = %s
            ''', (id_usuario,))
            insignias_desbloqueadas = cursor.fetchone()[0]
            
            # Total de insignias disponibles
            cursor.execute('SELECT COUNT(*) FROM insignias_catalogo WHERE activo = TRUE')
            total_insignias_disponibles = cursor.fetchone()[0]
            
            # Posición en ranking
            cursor.execute('''
                SELECT posicion_ranking FROM ranking_xp WHERE id_usuario = %s
            ''', (id_usuario,))
            ranking_data = cursor.fetchone()
            posicion_ranking = ranking_data[0] if ranking_data else None
            
            return {
                'id_usuario': id_usuario,
                'nombre_completo': nombre_completo,
                'email': email,
                'xp_actual': xp_actual,
                'nivel_actual': nivel,
                'xp_total_acumulado': xp_total,
                'xp_siguiente_nivel': xp_para_siguiente,
                'porcentaje_nivel': porcentaje_nivel,
                'insignias_desbloqueadas': insignias_desbloqueadas,
                'total_insignias': total_insignias_disponibles,
                'posicion_ranking': posicion_ranking,
                'estadisticas': {
                    'partidas_jugadas': stats_data[0] if stats_data else 0,
                    'partidas_ganadas': stats_data[1] if stats_data else 0,
                    'respuestas_correctas': stats_data[2] if stats_data else 0,
                    'respuestas_incorrectas': stats_data[3] if stats_data else 0,
                    'racha_actual': stats_data[4] if stats_data else 0,
                    'racha_maxima': stats_data[5] if stats_data else 0,
                    'precision': round(stats_data[6], 1) if stats_data else 0,
                    'tiempo_promedio': round(stats_data[7], 2) if stats_data else 0
                }
            }
    finally:
        conexion.close()

def obtener_ranking_global(limite=100):
    """
    Obtiene el ranking global de XP
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    id_usuario,
                    nombre_completo,
                    email,
                    nivel_actual,
                    xp_actual,
                    xp_total_acumulado,
                    total_insignias,
                    posicion_ranking
                FROM ranking_xp 
                LIMIT %s
            ''', (limite,))
            
            ranking = []
            for row in cursor.fetchall():
                ranking.append({
                    'id_usuario': row[0],
                    'nombre_completo': row[1],
                    'email': row[2],
                    'nivel_actual': row[3],
                    'xp_actual': row[4],
                    'xp_total_acumulado': row[5],
                    'total_insignias': row[6],
                    'posicion_ranking': row[7]
                })
            
            return ranking
    finally:
        conexion.close()

# ==================== TIENDA DE INSIGNIAS ====================

def obtener_insignias_tienda():
    """
    Obtiene todas las insignias disponibles para comprar
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT id_insignia, nombre, descripcion, tipo, rareza, 
                       icono, xp_bonus, precio_xp
                FROM insignias_catalogo
                WHERE precio_xp > 0
                ORDER BY precio_xp ASC
            ''')
            
            insignias = []
            for row in cursor.fetchall():
                insignias.append({
                    'id_insignia': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'tipo': row[3],
                    'rareza': row[4],
                    'icono': row[5],
                    'xp_bonus': row[6],
                    'precio_xp': row[7]
                })
            
            return insignias
    finally:
        conexion.close()

def comprar_insignia(id_usuario, id_insignia):
    """
    Permite a un usuario comprar una insignia con XP
    
    Returns:
        dict con resultado de la compra
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar que la insignia existe y es comprable
            cursor.execute('''
                SELECT nombre, precio_xp FROM insignias_catalogo
                WHERE id_insignia = %s AND precio_xp > 0
            ''', (id_insignia,))
            
            insignia_data = cursor.fetchone()
            if not insignia_data:
                return {'success': False, 'error': 'Insignia no disponible'}
            
            nombre_insignia, precio = insignia_data
            
            # Verificar que el usuario no la tiene ya
            cursor.execute('''
                SELECT id_insignia FROM insignias_usuarios
                WHERE id_usuario = %s AND id_insignia = %s
            ''', (id_usuario, id_insignia))
            
            if cursor.fetchone():
                return {'success': False, 'error': 'Ya tienes esta insignia'}
            
            # Verificar XP del usuario (usar xp_total_acumulado)
            cursor.execute('''
                SELECT xp_actual, nivel_actual, xp_total_acumulado 
                FROM experiencia_usuarios
                WHERE id_usuario = %s
            ''', (id_usuario,))
            
            xp_data = cursor.fetchone()
            if not xp_data:
                return {'success': False, 'error': 'Usuario no encontrado'}
            
            xp_actual, nivel_actual, xp_total_acumulado = xp_data
            
            if xp_total_acumulado < precio:
                return {
                    'success': False, 
                    'error': f'XP insuficiente. Necesitas {precio} XP, tienes {xp_total_acumulado} XP acumulados'
                }
            
            # Realizar la compra
            # 1. Descontar XP del total acumulado
            nuevo_xp_total = xp_total_acumulado - precio
            
            # 2. Recalcular nivel basándose en el nuevo XP total
            nuevo_nivel, nuevo_xp_actual = calcular_nivel_por_xp(nuevo_xp_total)
            
            # 3. Actualizar experiencia con los nuevos valores
            cursor.execute('''
                UPDATE experiencia_usuarios
                SET xp_actual = %s,
                    nivel_actual = %s,
                    xp_total_acumulado = %s
                WHERE id_usuario = %s
            ''', (nuevo_xp_actual, nuevo_nivel, nuevo_xp_total, id_usuario))
            
            # 4. Otorgar insignia
            cursor.execute('''
                INSERT INTO insignias_usuarios (id_usuario, id_insignia)
                VALUES (%s, %s)
            ''', (id_usuario, id_insignia))
            
            # 5. Registrar compra
            cursor.execute('''
                INSERT INTO compras_insignias (id_usuario, id_insignia, precio_pagado)
                VALUES (%s, %s, %s)
            ''', (id_usuario, id_insignia, precio))
            
            # 6. Registrar en historial
            cursor.execute('''
                INSERT INTO historial_xp (id_usuario, cantidad_xp, razon)
                VALUES (%s, %s, %s)
            ''', (id_usuario, -precio, f'Compra de insignia: {nombre_insignia}'))
            
            conexion.commit()
            
            return {
                'success': True,
                'mensaje': f'¡Insignia "{nombre_insignia}" comprada exitosamente!',
                'xp_gastado': precio,
                'xp_restante': nuevo_xp_total,
                'nivel_anterior': nivel_actual,
                'nivel_nuevo': nuevo_nivel,
                'bajo_nivel': nivel_actual > nuevo_nivel,
                'insignia': nombre_insignia
            }
            
    except Exception as e:
        conexion.rollback()
        return {'success': False, 'error': f'Error al comprar insignia: {str(e)}'}
    finally:
        conexion.close()

def obtener_historial_compras(id_usuario):
    """
    Obtiene el historial de compras de insignias de un usuario
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT c.fecha_compra, c.precio_pagado, i.nombre, i.icono
                FROM compras_insignias c
                JOIN insignias_catalogo i ON c.id_insignia = i.id_insignia
                WHERE c.id_usuario = %s
                ORDER BY c.fecha_compra DESC
            ''', (id_usuario,))
            
            compras = []
            for row in cursor.fetchall():
                compras.append({
                    'fecha': row[0].strftime('%d/%m/%Y %H:%M'),
                    'xp_gastado': row[1],
                    'nombre': row[2],
                    'icono': row[3]
                })
            
            return compras
    finally:
        conexion.close()
