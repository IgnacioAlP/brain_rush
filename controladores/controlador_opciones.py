from bd import obtener_conexion

def obtener_opciones_por_pregunta(pregunta_id):
    """Obtener todas las opciones de una pregunta"""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        # La tabla opciones_respuesta solo tiene: id_opcion, id_pregunta, texto_opcion, es_correcta
        query = """
            SELECT id_opcion, id_pregunta, texto_opcion, es_correcta
            FROM opciones_respuesta
            WHERE id_pregunta = %s
            ORDER BY id_opcion
        """
        cursor.execute(query, (pregunta_id,))
        resultados = cursor.fetchall()
        
        opciones = []
        for resultado in resultados:
            opciones.append({
                'id_opcion': resultado[0],
                'id_pregunta': resultado[1],
                'texto_opcion': resultado[2],
                'es_correcta': bool(resultado[3])
            })
        
        return opciones
    finally:
        conexion.close()

def crear_opcion(id_pregunta, texto_opcion, es_correcta, explicacion=''):
    """Crea una nueva opción de respuesta para una pregunta"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # La tabla opciones_respuesta solo tiene: id_opcion, id_pregunta, texto_opcion, es_correcta
        query = """
        INSERT INTO opciones_respuesta (id_pregunta, texto_opcion, es_correcta)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (id_pregunta, texto_opcion, es_correcta))
        conexion.commit()
        opcion_id = cursor.lastrowid
        return opcion_id
    except Exception as e:
        print(f"Error al crear opción: {e}")
        if 'conexion' in locals():
            conexion.rollback()
        return None
    finally:
        if 'conexion' in locals():
            conexion.close()

def eliminar_opciones_pregunta(pregunta_id):
    """Eliminar todas las opciones de una pregunta"""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM opciones_respuesta WHERE id_pregunta = %s"
        cursor.execute(query, (pregunta_id,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar opciones: {e}")
        return False
    finally:
        conexion.close()

def eliminar_opcion(id_opcion):
    """Eliminar una opción específica"""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM opciones_respuesta WHERE id_opcion = %s"
        cursor.execute(query, (id_opcion,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar opción: {e}")
        return False
    finally:
        conexion.close()

def actualizar_opcion(id_opcion, id_pregunta, texto_opcion, es_correcta, explicacion=''):
    """Actualizar una opción existente"""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        # La tabla opciones_respuesta solo tiene: id_opcion, id_pregunta, texto_opcion, es_correcta
        query = """
            UPDATE opciones_respuesta
            SET texto_opcion = %s, es_correcta = %s
            WHERE id_opcion = %s AND id_pregunta = %s
        """
        cursor.execute(query, (texto_opcion, es_correcta, id_opcion, id_pregunta))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar opción: {e}")
        return False
    finally:
        conexion.close()

def obtener_opcion_por_id(id_opcion):
    """Obtener una opción específica por su ID"""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        # La tabla opciones_respuesta solo tiene: id_opcion, id_pregunta, texto_opcion, es_correcta
        query = """
            SELECT id_opcion, id_pregunta, texto_opcion, es_correcta
            FROM opciones_respuesta
            WHERE id_opcion = %s
        """
        cursor.execute(query, (id_opcion,))
        resultado = cursor.fetchone()
        
        if resultado:
            return {
                'id_opcion': resultado[0],
                'id_pregunta': resultado[1],
                'texto_opcion': resultado[2],
                'es_correcta': bool(resultado[3])
            }
        return None
    finally:
        conexion.close()

