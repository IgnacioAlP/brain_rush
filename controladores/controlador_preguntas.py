from bd import obtener_conexion

def obtener_preguntas_por_cuestionario(cuestionario_id):
    """Obtiene todas las preguntas de un cuestionario específico con sus opciones"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar primero si existe la tabla preguntas
        cursor.execute("SHOW TABLES LIKE 'preguntas'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            print(f"DEBUG: Tabla 'preguntas' no existe en la base de datos")
            cursor.close()
            conexion.close()
            return []
        
        query = """
        SELECT 
            p.id_pregunta,
            p.enunciado,
            p.tipo,
            p.puntaje_base,
            cp.orden
        FROM preguntas p
        INNER JOIN cuestionario_preguntas cp ON p.id_pregunta = cp.id_pregunta
        WHERE cp.id_cuestionario = %s
        ORDER BY cp.orden ASC
        """
        
        cursor.execute(query, (cuestionario_id,))
        resultados = cursor.fetchall()
        
        # Convertir tuplas a diccionarios y obtener opciones para cada pregunta
        preguntas = []
        for resultado in resultados:
            pregunta = {
                'id_pregunta': resultado[0],
                'enunciado': resultado[1],  # Usar 'enunciado' en lugar de 'texto'
                'tipo': resultado[2],       # Usar 'tipo' en lugar de 'tipo_pregunta'
                'puntaje_base': resultado[3],
                'orden': resultado[4],
                'opciones': []
            }
            
            # Si es pregunta de opción múltiple, obtener las opciones
            if resultado[2] == 'opcion_multiple':
                query_opciones = """
                SELECT id_opcion, texto_opcion, es_correcta
                FROM opciones_respuesta
                WHERE id_pregunta = %s
                ORDER BY id_opcion ASC
                """
                cursor.execute(query_opciones, (resultado[0],))
                opciones_resultado = cursor.fetchall()
                
                for opcion in opciones_resultado:
                    pregunta['opciones'].append({
                        'id_opcion': opcion[0],
                        'texto_opcion': opcion[1],
                        'es_correcta': bool(opcion[2])
                    })
            
            preguntas.append(pregunta)
        
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Obtenidas {len(preguntas)} preguntas para cuestionario {cuestionario_id}")
        for p in preguntas:
            print(f"DEBUG: Pregunta {p['id_pregunta']}: {len(p['opciones'])} opciones")
        
        return preguntas
        
    except Exception as e:
        print(f"DEBUG: Error obteniendo preguntas para cuestionario {cuestionario_id}: {e}")
        return []

def crear_pregunta(enunciado, tipo, cuestionario_id, puntaje_base=1):
    """Crea una nueva pregunta y la asocia a un cuestionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar que las tablas necesarias existen
        cursor.execute("SHOW TABLES LIKE 'preguntas'")
        if not cursor.fetchone():
            print("DEBUG: Tabla preguntas no existe, pero debería según bd.sql")
            cursor.close()
            conexion.close()
            return None
        
        # Insertar la pregunta usando la estructura correcta
        cursor.execute("""
            INSERT INTO preguntas (enunciado, tipo, puntaje_base)
            VALUES (%s, %s, %s)
        """, (enunciado, tipo, puntaje_base))
        
        pregunta_id = cursor.lastrowid
        
        # Obtener el siguiente orden para este cuestionario
        cursor.execute("""
            SELECT COALESCE(MAX(orden), 0) + 1 as siguiente_orden 
            FROM cuestionario_preguntas 
            WHERE id_cuestionario = %s
        """, (cuestionario_id,))
        
        orden = cursor.fetchone()[0]
        
        # Asociar la pregunta al cuestionario
        cursor.execute("""
            INSERT INTO cuestionario_preguntas (id_cuestionario, id_pregunta, orden)
            VALUES (%s, %s, %s)
        """, (cuestionario_id, pregunta_id, orden))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Pregunta creada con ID {pregunta_id} para cuestionario {cuestionario_id}")
        return pregunta_id
        
    except Exception as e:
        print(f"DEBUG: Error creando pregunta: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return None

def eliminar_pregunta(pregunta_id):
    """Elimina una pregunta y sus asociaciones"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Eliminar primero de cuestionario_preguntas
        cursor.execute("DELETE FROM cuestionario_preguntas WHERE id_pregunta = %s", (pregunta_id,))
        
        # Luego eliminar la pregunta
        cursor.execute("DELETE FROM preguntas WHERE id_pregunta = %s", (pregunta_id,))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return True
        
    except Exception as e:
        print(f"DEBUG: Error eliminando pregunta {pregunta_id}: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def crear_opcion_respuesta(pregunta_id, texto_opcion, es_correcta=False):
    """Crea una opción de respuesta para una pregunta"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO opciones_respuesta (id_pregunta, texto_opcion, es_correcta)
            VALUES (%s, %s, %s)
        """, (pregunta_id, texto_opcion, es_correcta))
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"DEBUG: Opción creada para pregunta {pregunta_id}: {texto_opcion} (correcta: {es_correcta})")
        return True
        
    except Exception as e:
        print(f"DEBUG: Error creando opción para pregunta {pregunta_id}: {e}")
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()
        return False

def obtener_opciones_por_pregunta(pregunta_id):
    """Obtiene todas las opciones de respuesta de una pregunta"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id_opcion, texto_opcion, es_correcta
            FROM opciones_respuesta
            WHERE id_pregunta = %s
        """, (pregunta_id,))
        
        resultados = cursor.fetchall()
        
        opciones = []
        for resultado in resultados:
            opciones.append({
                'id_opcion': resultado[0],
                'texto_opcion': resultado[1],
                'es_correcta': bool(resultado[2])
            })
        
        cursor.close()
        conexion.close()
        
        return opciones
        
    except Exception as e:
        print(f"DEBUG: Error obteniendo opciones para pregunta {pregunta_id}: {e}")
        return []
