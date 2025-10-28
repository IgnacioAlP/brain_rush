from bd import obtener_conexion

def crear_sala(nombre, cuestionario_id, docente_id, **kwargs):
    import random
    pin_sala = str(random.randint(100000, 999999))
    max_participantes = kwargs.get('max_participantes', 30)
    modo_juego = kwargs.get('modo_juego', 'individual')
    
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                'INSERT INTO salas_juego (pin_sala, id_cuestionario, modo_juego, estado, max_participantes) VALUES (%s, %s, %s, %s, %s)', 
                (pin_sala, cuestionario_id, modo_juego, 'esperando', max_participantes)
            )
            conexion.commit()
            return cursor.lastrowid
    finally:
        conexion.close()

def obtener_sala_por_id(id_sala):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id_sala, pin_sala FROM salas_juego WHERE id_sala = %s', (id_sala,))
            return cursor.fetchone()
    finally:
        conexion.close()

def obtener_participantes_sala(sala_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    ps.id_participante, 
                    ps.id_usuario, 
                    ps.nombre_participante, 
                    ps.fecha_union, 
                    ps.estado,
                    ps.id_grupo,
                    gs.nombre_grupo
                FROM participantes_sala ps
                LEFT JOIN grupos_sala gs ON ps.id_grupo = gs.id_grupo
                WHERE ps.id_sala = %s AND ps.estado != 'desconectado'
                ORDER BY ps.fecha_union ASC
            ''', (sala_id,))
            
            participantes = []
            for row in cursor.fetchall():
                participantes.append({
                    'id_participante': row[0],
                    'id_usuario': row[1],
                    'nombre_participante': row[2],
                    'fecha_union': row[3],
                    'estado': row[4],
                    'id_grupo': row[5],
                    'nombre_grupo': row[6]
                })
            return participantes
    finally:
        conexion.close()

def obtener_sala_por_codigo(pin_sala):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT id_sala, pin_sala, id_cuestionario, modo_juego, estado, max_participantes, fecha_creacion 
                FROM salas_juego 
                WHERE pin_sala = %s
            ''', (pin_sala,))
            
            resultado = cursor.fetchone()
            if resultado:
                return {
                    'id': resultado[0],
                    'pin_sala': resultado[1],
                    'id_cuestionario': resultado[2],
                    'modo_juego': resultado[3],
                    'estado': resultado[4],
                    'max_participantes': resultado[5],
                    'fecha_creacion': resultado[6]
                }
            return None
    finally:
        conexion.close()

def agregar_participante_sala(sala_id, nombre_participante, id_usuario=None):
    """Agrega un participante a una sala de juego"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar que no exista ya el participante (por nombre o usuario)
            if id_usuario:
                cursor.execute('''
                    SELECT id_participante FROM participantes_sala 
                    WHERE id_sala = %s AND id_usuario = %s AND estado != 'desconectado'
                ''', (sala_id, id_usuario))
            else:
                cursor.execute('''
                    SELECT id_participante FROM participantes_sala 
                    WHERE id_sala = %s AND nombre_participante = %s AND estado != 'desconectado'
                ''', (sala_id, nombre_participante))
            
            if cursor.fetchone():
                raise ValueError("El participante ya está en la sala")
            
            # Insertar nuevo participante
            cursor.execute('''
                INSERT INTO participantes_sala (id_sala, id_usuario, nombre_participante, estado) 
                VALUES (%s, %s, %s, 'esperando')
            ''', (sala_id, id_usuario, nombre_participante))
            
            conexion.commit()
            return cursor.lastrowid
    finally:
        conexion.close()

def eliminar_participante_sala(participante_id):
    """Elimina un participante de una sala (marca como desconectado)"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE participantes_sala 
                SET estado = 'desconectado' 
                WHERE id_participante = %s
            ''', (participante_id,))
            conexion.commit()
            return cursor.rowcount > 0
    finally:
        conexion.close()

def actualizar_estado_sala(sala_id, nuevo_estado):
    """Actualiza el estado de una sala"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE salas_juego 
                SET estado = %s 
                WHERE id_sala = %s
            ''', (nuevo_estado, sala_id))
            conexion.commit()
            return cursor.rowcount > 0
    finally:
        conexion.close()

# ==================== FUNCIONES DE GRUPOS ====================

def crear_grupos_sala(sala_id, num_grupos, nombres=None):
    """
    Crea grupos para una sala específica
    
    Args:
        sala_id: ID de la sala
        num_grupos: Número de grupos a crear
        nombres: Lista opcional de nombres personalizados para los grupos
        
    Returns:
        Lista de IDs de los grupos creados
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Primero eliminar grupos existentes de esta sala
            cursor.execute('DELETE FROM grupos_sala WHERE id_sala = %s', (sala_id,))
            
            # Crear los nuevos grupos
            ids_grupos = []
            for i in range(num_grupos):
                nombre_grupo = nombres[i] if nombres and i < len(nombres) else f'Grupo {i + 1}'
                
                cursor.execute('''
                    INSERT INTO grupos_sala (id_sala, nombre_grupo, numero_grupo, capacidad_maxima) 
                    VALUES (%s, %s, %s, %s)
                ''', (sala_id, nombre_grupo, i + 1, 0))  # capacidad 0 = sin límite
                
                ids_grupos.append(cursor.lastrowid)
            
            conexion.commit()
            return ids_grupos
    finally:
        conexion.close()

def obtener_grupos_sala(sala_id):
    """
    Obtiene todos los grupos de una sala con el conteo de participantes
    
    Returns:
        Lista de diccionarios con información de cada grupo
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    g.id_grupo,
                    g.nombre_grupo,
                    g.numero_grupo,
                    g.capacidad_maxima,
                    COUNT(p.id_participante) as num_participantes
                FROM grupos_sala g
                LEFT JOIN participantes_sala p ON g.id_grupo = p.id_grupo AND p.estado != 'desconectado'
                WHERE g.id_sala = %s
                GROUP BY g.id_grupo, g.nombre_grupo, g.numero_grupo, g.capacidad_maxima
                ORDER BY g.numero_grupo
            ''', (sala_id,))
            
            grupos = []
            for row in cursor.fetchall():
                grupos.append({
                    'id_grupo': row[0],
                    'nombre_grupo': row[1],
                    'numero_grupo': row[2],
                    'capacidad_maxima': row[3],
                    'num_participantes': row[4]
                })
            return grupos
    finally:
        conexion.close()

def asignar_participante_grupo(participante_id, grupo_id):
    """
    Asigna un participante a un grupo específico
    
    Args:
        participante_id: ID del participante
        grupo_id: ID del grupo (puede ser None para quitar del grupo)
        
    Returns:
        True si se actualizó correctamente
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE participantes_sala 
                SET id_grupo = %s 
                WHERE id_participante = %s
            ''', (grupo_id, participante_id))
            conexion.commit()
            return cursor.rowcount > 0
    finally:
        conexion.close()

def habilitar_grupos_sala(sala_id, habilitar=True, num_grupos=3):
    """
    Habilita o deshabilita los grupos para una sala
    
    Args:
        sala_id: ID de la sala
        habilitar: True para habilitar, False para deshabilitar
        num_grupos: Número de grupos a crear (solo si habilitar=True)
        
    Returns:
        True si se actualizó correctamente
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE salas_juego 
                SET grupos_habilitados = %s, num_grupos = %s 
                WHERE id_sala = %s
            ''', (1 if habilitar else 0, num_grupos if habilitar else 0, sala_id))
            conexion.commit()
            return cursor.rowcount > 0
    finally:
        conexion.close()
