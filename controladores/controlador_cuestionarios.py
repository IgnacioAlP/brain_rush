from bd import obtener_conexion
from datetime import datetime

def obtener_cuestionarios_por_docente(docente_id):
    """Obtiene los cuestionarios de un docente específico"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
        SELECT 
            id_cuestionario,
            titulo,
            descripcion,
            fecha_creacion,
            fecha_programada,
            fecha_publicacion,
            estado
        FROM cuestionarios 
        WHERE id_docente = %s 
        ORDER BY fecha_creacion DESC
        """
        
        cursor.execute(query, (docente_id,))
        cuestionarios = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return cuestionarios
        
    except Exception as e:
        print(f"Error obteniendo cuestionarios del docente {docente_id}: {e}")
        return []

def crear_cuestionario(titulo, descripcion, id_docente, categoria=None, tiempo_limite=30, max_intentos=1):
    """Crea un nuevo cuestionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Solo usar los campos que existen en la tabla actual
        query = """
        INSERT INTO cuestionarios 
        (titulo, descripcion, id_docente, fecha_creacion, estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        fecha_actual = datetime.now()
        valores = (titulo, descripcion, id_docente, fecha_actual, 'borrador')
        
        cursor.execute(query, valores)
        cuestionario_id = cursor.lastrowid
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Cuestionario creado exitosamente con ID: {cuestionario_id}")
        return cuestionario_id
        
    except Exception as e:
        print(f"Error creando cuestionario: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        raise e

def obtener_cuestionario_por_id(cuestionario_id):
    """Obtiene un cuestionario por su ID devolviendo diccionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
        SELECT 
            c.id_cuestionario,
            c.titulo,
            c.descripcion,
            c.id_docente,
            c.fecha_creacion,
            c.fecha_programada,
            c.fecha_publicacion,
            c.estado,
            u.nombre as nombre_docente,
            u.apellidos as apellidos_docente
        FROM cuestionarios c
        LEFT JOIN usuarios u ON c.id_docente = u.id_usuario
        WHERE c.id_cuestionario = %s
        """
        
        cursor.execute(query, (cuestionario_id,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            # Convertir tupla a diccionario
            cuestionario = {
                'id_cuestionario': resultado[0],
                'titulo': resultado[1],
                'descripcion': resultado[2],
                'id_docente': resultado[3],
                'fecha_creacion': resultado[4],
                'fecha_programada': resultado[5],
                'fecha_publicacion': resultado[6],
                'estado': resultado[7],
                'nombre_docente': resultado[8],
                'apellidos_docente': resultado[9]
            }
            return cuestionario
        
        return None
        
    except Exception as e:
        print(f"Error obteniendo cuestionario {cuestionario_id}: {e}")
        return None

def obtener_cuestionario_por_id_simple(cuestionario_id):
    """Obtiene un cuestionario por su ID devolviendo tupla para compatibilidad"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
        SELECT 
            id_cuestionario,
            titulo,
            descripcion,
            id_docente,
            fecha_creacion,
            fecha_programada,
            fecha_publicacion,
            estado
        FROM cuestionarios
        WHERE id_cuestionario = %s
        """
        
        cursor.execute(query, (cuestionario_id,))
        cuestionario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return cuestionario
        
    except Exception as e:
        print(f"Error obteniendo cuestionario {cuestionario_id}: {e}")
        return None

def obtener_cuestionarios():
    """Obtiene todos los cuestionarios"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
        SELECT 
            c.*,
            u.nombre as nombre_docente,
            u.apellidos as apellidos_docente,
            (SELECT COUNT(*) FROM preguntas p WHERE p.id_cuestionario = c.id_cuestionario) as total_preguntas
        FROM cuestionarios c
        LEFT JOIN usuarios u ON c.id_docente = u.id_usuario
        ORDER BY c.fecha_creacion DESC
        """
        
        cursor.execute(query)
        cuestionarios = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return cuestionarios
        
    except Exception as e:
        print(f"Error obteniendo cuestionarios: {e}")
        return []

def actualizar_cuestionario(cuestionario_id, titulo, descripcion, id_docente=None, categoria=None, tiempo_limite=None, max_intentos=None):
    """Actualiza un cuestionario existente"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Solo actualizar campos que existen en la tabla
        query = "UPDATE cuestionarios SET titulo = %s, descripcion = %s WHERE id_cuestionario = %s"
        valores = [titulo, descripcion, cuestionario_id]
        
        if id_docente is not None:
            query = "UPDATE cuestionarios SET titulo = %s, descripcion = %s, id_docente = %s WHERE id_cuestionario = %s"
            valores = [titulo, descripcion, id_docente, cuestionario_id]
        
        cursor.execute(query, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return True
        
    except Exception as e:
        print(f"Error actualizando cuestionario {cuestionario_id}: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def eliminar_cuestionario(cuestionario_id):
    """Elimina un cuestionario y sus preguntas asociadas"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Primero eliminar las respuestas asociadas
        cursor.execute("DELETE FROM respuestas WHERE id_pregunta IN (SELECT id_pregunta FROM preguntas WHERE id_cuestionario = %s)", (cuestionario_id,))
        
        # Luego eliminar las preguntas
        cursor.execute("DELETE FROM preguntas WHERE id_cuestionario = %s", (cuestionario_id,))
        
        # Finalmente eliminar el cuestionario
        cursor.execute("DELETE FROM cuestionarios WHERE id_cuestionario = %s", (cuestionario_id,))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True
        
    except Exception as e:
        print(f"Error eliminando cuestionario {cuestionario_id}: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def cambiar_estado_cuestionario(cuestionario_id, nuevo_estado):
    """Cambia el estado de un cuestionario (borrador, publicado, archivado)"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = "UPDATE cuestionarios SET estado = %s WHERE id_cuestionario = %s"
        cursor.execute(query, (nuevo_estado, cuestionario_id))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True
        
    except Exception as e:
        print(f"Error cambiando estado del cuestionario {cuestionario_id}: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def obtener_estadisticas_sistema():
    """Obtiene estadísticas generales del sistema"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # Total de cuestionarios
        cursor.execute("SELECT COUNT(*) as total FROM cuestionarios")
        total_cuestionarios = cursor.fetchone()['total']
        
        # Cuestionarios por estado
        cursor.execute("SELECT estado, COUNT(*) as cantidad FROM cuestionarios GROUP BY estado")
        por_estado = cursor.fetchall()
        
        # Total de preguntas
        cursor.execute("SELECT COUNT(*) as total FROM preguntas")
        total_preguntas = cursor.fetchone()['total']
        
        # Docentes activos (que tienen cuestionarios)
        cursor.execute("SELECT COUNT(DISTINCT id_docente) as total FROM cuestionarios")
        docentes_activos = cursor.fetchone()['total']
        
        cursor.close()
        conexion.close()
        
        estadisticas = {
            'total_cuestionarios': total_cuestionarios,
            'total_preguntas': total_preguntas,
            'docentes_activos': docentes_activos,
            'por_estado': {item['estado']: item['cantidad'] for item in por_estado}
        }
        
        return estadisticas
        
    except Exception as e:
        print(f"Error obteniendo estadísticas del sistema: {e}")
        return {
            'total_cuestionarios': 0,
            'total_preguntas': 0,
            'docentes_activos': 0,
            'por_estado': {}
        }

def publicar_cuestionario(cuestionario_id, id_docente):
    """Cambia el estado de un cuestionario de 'borrador' a 'publicado'"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar que el cuestionario pertenece al docente y está en estado borrador
        cursor.execute("""
            SELECT estado FROM cuestionarios 
            WHERE id_cuestionario = %s AND id_docente = %s
        """, (cuestionario_id, id_docente))
        
        resultado = cursor.fetchone()
        if not resultado:
            cursor.close()
            conexion.close()
            return False, "Cuestionario no encontrado o no pertenece al docente"
        
        estado_actual = resultado[0]
        if estado_actual != 'borrador':
            cursor.close()
            conexion.close()
            return False, f"El cuestionario no puede publicarse desde el estado '{estado_actual}'"
        
        # Actualizar estado a publicado y establecer fecha de publicación
        cursor.execute("""
            UPDATE cuestionarios 
            SET estado = 'publicado', fecha_publicacion = NOW()
            WHERE id_cuestionario = %s AND id_docente = %s
        """, (cuestionario_id, id_docente))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True, "Cuestionario publicado exitosamente"
        
    except Exception as e:
        print(f"Error publicando cuestionario {cuestionario_id}: {e}")
        return False, f"Error al publicar: {str(e)}"

def despublicar_cuestionario(cuestionario_id, id_docente):
    """Cambia el estado de un cuestionario de 'publicado' a 'borrador'"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar que el cuestionario pertenece al docente y está publicado
        cursor.execute("""
            SELECT estado FROM cuestionarios 
            WHERE id_cuestionario = %s AND id_docente = %s
        """, (cuestionario_id, id_docente))
        
        resultado = cursor.fetchone()
        if not resultado:
            cursor.close()
            conexion.close()
            return False, "Cuestionario no encontrado o no pertenece al docente"
        
        estado_actual = resultado[0]
        if estado_actual != 'publicado':
            cursor.close()
            conexion.close()
            return False, f"El cuestionario no puede despublicarse desde el estado '{estado_actual}'"
        
        # Actualizar estado a borrador y limpiar fecha de publicación
        cursor.execute("""
            UPDATE cuestionarios 
            SET estado = 'borrador', fecha_publicacion = NULL
            WHERE id_cuestionario = %s AND id_docente = %s
        """, (cuestionario_id, id_docente))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True, "Cuestionario despublicado exitosamente"
        
    except Exception as e:
        print(f"Error despublicando cuestionario {cuestionario_id}: {e}")
        return False, f"Error al despublicar: {str(e)}"
