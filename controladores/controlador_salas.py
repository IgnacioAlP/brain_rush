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
                SELECT id_participante, id_usuario, nombre_participante, fecha_union, estado 
                FROM participantes_sala 
                WHERE id_sala = %s AND estado != 'desconectado'
                ORDER BY fecha_union ASC
            ''', (sala_id,))
            
            participantes = []
            for row in cursor.fetchall():
                participantes.append({
                    'id_participante': row[0],
                    'id_usuario': row[1],
                    'nombre_participante': row[2],
                    'fecha_union': row[3],
                    'estado': row[4]
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
