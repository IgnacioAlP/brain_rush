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
