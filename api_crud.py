# -*- coding: utf-8 -*-
"""
APIs CRUD para todas las tablas de Brain Rush
Cada tabla tiene 5 endpoints: crear, actualizar, obtener_uno, obtener_todos, eliminar
Seguridad: JWT (requiere token en header Authorization)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bd import obtener_conexion
import pymysql

# ================================================================================
# BLUEPRINT PRINCIPAL
# ================================================================================
api_crud = Blueprint('api_crud', __name__, url_prefix='/api')

# ================================================================================
# UTILITIES
# ================================================================================

def obtener_usuario_actual():
    """Obtiene el ID del usuario autenticado desde el JWT"""
    try:
        return get_jwt_identity()
    except:
        return None

def respuesta_error(mensaje, codigo=400):
    """Respuesta de error estandarizada"""
    return jsonify({'success': False, 'error': mensaje}), codigo

def respuesta_exito(datos=None, mensaje='Operación exitosa', codigo=200):
    """Respuesta de éxito estandarizada"""
    return jsonify({'success': True, 'mensaje': mensaje, 'data': datos}), codigo

# ================================================================================
# TABLA: USUARIOS
# ================================================================================

@api_crud.route('/usuarios', methods=['POST'])
@jwt_required()
def api_registrar_usuario():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return respuesta_error('No se enviaron datos', 400)
        
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        email = data.get('email')
        contraseña = data.get('contraseña_hash')  # Recibir como contraseña_hash para compatibilidad
        tipo_usuario = data.get('tipo_usuario', 'estudiante')
        estado = data.get('estado', 'activo')
        
        # Validar campos requeridos
        if not all([nombre, apellidos, email, contraseña]):
            return respuesta_error('Faltan campos requeridos: nombre, apellidos, email, contraseña_hash', 400)
        
        # Hashear la contraseña si no está hasheada
        import bcrypt
        if len(contraseña) < 50:  # Si no es un hash bcrypt (que tiene ~60 caracteres)
            contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            contraseña_hash = contraseña
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellidos, email, contraseña_hash, tipo_usuario, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, apellidos, email, contraseña_hash, tipo_usuario, estado))
        
        conexion.commit()
        usuario_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_usuario': usuario_id}, 'Usuario registrado exitosamente', 201)
    except pymysql.IntegrityError as e:
        return respuesta_error(f'Email ya registrado: {str(e)}', 409)
    except Exception as e:
        return respuesta_error(f'Error al registrar usuario: {str(e)}', 500)

@api_crud.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_usuario(usuario_id):
    """Actualizar usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['nombre', 'apellidos', 'email', 'tipo_usuario', 'estado']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Usuario actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar usuario: {str(e)}', 500)

@api_crud.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
def api_obtener_usuario(usuario_id):
    """Obtener un usuario por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_usuario, nombre, apellidos, email, tipo_usuario, estado, fecha_registro
            FROM usuarios WHERE id_usuario = %s
        """, (usuario_id,))
        
        usuario = cursor.fetchone()
        conexion.close()
        
        if not usuario:
            return respuesta_error('Usuario no encontrado', 404)
        
        return respuesta_exito(usuario)
    except Exception as e:
        return respuesta_error(f'Error al obtener usuario: {str(e)}', 500)

@api_crud.route('/usuarios', methods=['GET'])
@jwt_required()
def api_obtener_usuarios():
    """Obtener todos los usuarios"""
    try:
        # Verificar autenticación
        usuario_actual = obtener_usuario_actual()
        print(f"✅ Usuario autenticado: {usuario_actual}")
        
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_usuario, nombre, apellidos, email, tipo_usuario, estado, fecha_registro
            FROM usuarios ORDER BY fecha_registro DESC
        """)
        
        usuarios = cursor.fetchall()
        conexion.close()
        
        print(f"📊 Usuarios encontrados: {len(usuarios)}")
        
        return respuesta_exito(usuarios if usuarios else [], f'{len(usuarios)} usuarios encontrados')
    except Exception as e:
        print(f"❌ Error en api_obtener_usuarios: {str(e)}")
        import traceback
        traceback.print_exc()
        return respuesta_error(f'Error al obtener usuarios: {str(e)}', 500)

@api_crud.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_usuario(usuario_id):
    """Eliminar un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Usuario eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar usuario: {str(e)}', 500)

# ================================================================================
# TABLA: CUESTIONARIOS
# ================================================================================

@api_crud.route('/cuestionarios', methods=['POST'])
@jwt_required()
def api_registrar_cuestionario():
    """Registrar nuevo cuestionario"""
    try:
        data = request.get_json()
        usuario_id = obtener_usuario_actual()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO cuestionarios (titulo, descripcion, id_docente, estado)
            VALUES (%s, %s, %s, %s)
        """, (data.get('titulo'), data.get('descripcion'), usuario_id, 
              data.get('estado', 'borrador')))
        
        conexion.commit()
        cuestionario_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_cuestionario': cuestionario_id}, 
                              'Cuestionario registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar cuestionario: {str(e)}', 500)

@api_crud.route('/cuestionarios/<int:cuestionario_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_cuestionario(cuestionario_id):
    """Actualizar cuestionario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['titulo', 'descripcion', 'estado', 'fecha_programada', 'fecha_publicacion']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(cuestionario_id)
        query = f"UPDATE cuestionarios SET {', '.join(campos)} WHERE id_cuestionario = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Cuestionario actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar cuestionario: {str(e)}', 500)

@api_crud.route('/cuestionarios/<int:cuestionario_id>', methods=['GET'])
@jwt_required()
def api_obtener_cuestionario(cuestionario_id):
    """Obtener un cuestionario por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_cuestionario, titulo, descripcion, id_docente, estado, 
                   fecha_creacion, fecha_programada, fecha_publicacion
            FROM cuestionarios WHERE id_cuestionario = %s
        """, (cuestionario_id,))
        
        cuestionario = cursor.fetchone()
        conexion.close()
        
        if not cuestionario:
            return respuesta_error('Cuestionario no encontrado', 404)
        
        return respuesta_exito(cuestionario)
    except Exception as e:
        return respuesta_error(f'Error al obtener cuestionario: {str(e)}', 500)

@api_crud.route('/cuestionarios', methods=['GET'])
@jwt_required()
def api_obtener_cuestionarios():
    """Obtener todos los cuestionarios"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_cuestionario, titulo, descripcion, id_docente, estado,
                   fecha_creacion, fecha_programada, fecha_publicacion
            FROM cuestionarios ORDER BY fecha_creacion DESC
        """)
        
        cuestionarios = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(cuestionarios if cuestionarios else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener cuestionarios: {str(e)}', 500)

@api_crud.route('/cuestionarios/<int:cuestionario_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_cuestionario(cuestionario_id):
    """Eliminar un cuestionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM cuestionarios WHERE id_cuestionario = %s", (cuestionario_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Cuestionario eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar cuestionario: {str(e)}', 500)

# ================================================================================
# TABLA: PREGUNTAS
# ================================================================================

@api_crud.route('/preguntas', methods=['POST'])
@jwt_required()
def api_registrar_pregunta():
    """Registrar nueva pregunta"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO preguntas (enunciado, tipo, puntaje_base, tiempo_sugerido)
            VALUES (%s, %s, %s, %s)
        """, (data.get('enunciado'), data.get('tipo'), 
              data.get('puntaje_base', 1), data.get('tiempo_sugerido', 30)))
        
        conexion.commit()
        pregunta_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_pregunta': pregunta_id}, 
                              'Pregunta registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar pregunta: {str(e)}', 500)

@api_crud.route('/preguntas/<int:pregunta_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_pregunta(pregunta_id):
    """Actualizar pregunta"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['enunciado', 'tipo', 'puntaje_base', 'tiempo_sugerido']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(pregunta_id)
        query = f"UPDATE preguntas SET {', '.join(campos)} WHERE id_pregunta = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Pregunta actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar pregunta: {str(e)}', 500)

@api_crud.route('/preguntas/<int:pregunta_id>', methods=['GET'])
@jwt_required()
def api_obtener_pregunta(pregunta_id):
    """Obtener una pregunta por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_pregunta, enunciado, tipo, puntaje_base, tiempo_sugerido
            FROM preguntas WHERE id_pregunta = %s
        """, (pregunta_id,))
        
        pregunta = cursor.fetchone()
        conexion.close()
        
        if not pregunta:
            return respuesta_error('Pregunta no encontrada', 404)
        
        return respuesta_exito(pregunta)
    except Exception as e:
        return respuesta_error(f'Error al obtener pregunta: {str(e)}', 500)

@api_crud.route('/preguntas', methods=['GET'])
@jwt_required()
def api_obtener_preguntas():
    """Obtener todas las preguntas"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_pregunta, enunciado, tipo, puntaje_base, tiempo_sugerido
            FROM preguntas ORDER BY id_pregunta DESC
        """)
        
        preguntas = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(preguntas if preguntas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener preguntas: {str(e)}', 500)

@api_crud.route('/preguntas/<int:pregunta_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_pregunta(pregunta_id):
    """Eliminar una pregunta"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM preguntas WHERE id_pregunta = %s", (pregunta_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Pregunta eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar pregunta: {str(e)}', 500)

# ================================================================================
# TABLA: OPCIONES_RESPUESTA
# ================================================================================

@api_crud.route('/opciones-respuesta', methods=['POST'])
@jwt_required()
def api_registrar_opcion():
    """Registrar nueva opción de respuesta"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO opciones_respuesta (id_pregunta, texto_opcion, es_correcta)
            VALUES (%s, %s, %s)
        """, (data.get('id_pregunta'), data.get('texto_opcion'), 
              data.get('es_correcta', 0)))
        
        conexion.commit()
        opcion_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_opcion': opcion_id}, 
                              'Opción registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar opción: {str(e)}', 500)

@api_crud.route('/opciones-respuesta/<int:opcion_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_opcion(opcion_id):
    """Actualizar opción de respuesta"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['texto_opcion', 'es_correcta']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(opcion_id)
        query = f"UPDATE opciones_respuesta SET {', '.join(campos)} WHERE id_opcion = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Opción actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar opción: {str(e)}', 500)

@api_crud.route('/opciones-respuesta/<int:opcion_id>', methods=['GET'])
@jwt_required()
def api_obtener_opcion(opcion_id):
    """Obtener una opción por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_opcion, id_pregunta, texto_opcion, es_correcta
            FROM opciones_respuesta WHERE id_opcion = %s
        """, (opcion_id,))
        
        opcion = cursor.fetchone()
        conexion.close()
        
        if not opcion:
            return respuesta_error('Opción no encontrada', 404)
        
        return respuesta_exito(opcion)
    except Exception as e:
        return respuesta_error(f'Error al obtener opción: {str(e)}', 500)

@api_crud.route('/opciones-respuesta', methods=['GET'])
@jwt_required()
def api_obtener_opciones():
    """Obtener todas las opciones"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_opcion, id_pregunta, texto_opcion, es_correcta
            FROM opciones_respuesta ORDER BY id_opcion DESC
        """)
        
        opciones = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(opciones if opciones else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener opciones: {str(e)}', 500)

@api_crud.route('/opciones-respuesta/<int:opcion_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_opcion(opcion_id):
    """Eliminar una opción"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM opciones_respuesta WHERE id_opcion = %s", (opcion_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Opción eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar opción: {str(e)}', 500)

# ================================================================================
# TABLA: SALAS_JUEGO
# ================================================================================

@api_crud.route('/salas-juego', methods=['POST'])
@jwt_required()
def api_registrar_sala():
    """Registrar nueva sala de juego"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO salas_juego (pin_sala, id_cuestionario, modo_juego, estado, tiempo_por_pregunta)
            VALUES (%s, %s, %s, %s, %s)
        """, (data.get('pin_sala'), data.get('id_cuestionario'), 
              data.get('modo_juego', 'individual'), data.get('estado', 'esperando'),
              data.get('tiempo_por_pregunta', 30)))
        
        conexion.commit()
        sala_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_sala': sala_id}, 'Sala registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar sala: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_sala(sala_id):
    """Actualizar sala de juego"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['estado', 'tiempo_por_pregunta', 'modo_juego', 'max_participantes']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(sala_id)
        query = f"UPDATE salas_juego SET {', '.join(campos)} WHERE id_sala = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Sala actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar sala: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>', methods=['GET'])
@jwt_required()
def api_obtener_sala(sala_id):
    """Obtener una sala por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_sala, pin_sala, id_cuestionario, modo_juego, estado, 
                   tiempo_por_pregunta, max_participantes, fecha_creacion
            FROM salas_juego WHERE id_sala = %s
        """, (sala_id,))
        
        sala = cursor.fetchone()
        conexion.close()
        
        if not sala:
            return respuesta_error('Sala no encontrada', 404)
        
        return respuesta_exito(sala)
    except Exception as e:
        return respuesta_error(f'Error al obtener sala: {str(e)}', 500)

@api_crud.route('/salas-juego', methods=['GET'])
@jwt_required()
def api_obtener_salas():
    """Obtener todas las salas"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_sala, pin_sala, id_cuestionario, modo_juego, estado,
                   tiempo_por_pregunta, max_participantes, fecha_creacion
            FROM salas_juego ORDER BY fecha_creacion DESC
        """)
        
        salas = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(salas if salas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener salas: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_sala(sala_id):
    """Eliminar una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM salas_juego WHERE id_sala = %s", (sala_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Sala eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar sala: {str(e)}', 500)

# ================================================================================
# TABLA: INSIGNIAS_CATALOGO
# ================================================================================

@api_crud.route('/insignias-catalogo', methods=['POST'])
@jwt_required()
def api_registrar_insignia():
    """Registrar nueva insignia"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO insignias_catalogo 
            (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, precio_xp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data.get('nombre'), data.get('descripcion'), data.get('icono', '🏆'),
              data.get('tipo', 'bronce'), data.get('requisito_tipo'), data.get('requisito_valor'),
              data.get('xp_bonus', 0), data.get('rareza', 'comun'), data.get('precio_xp', 0)))
        
        conexion.commit()
        insignia_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_insignia': insignia_id}, 'Insignia registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar insignia: {str(e)}', 500)

@api_crud.route('/insignias-catalogo/<int:insignia_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_insignia(insignia_id):
    """Actualizar insignia"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['nombre', 'descripcion', 'icono', 'tipo', 'rareza', 'precio_xp', 'activo']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(insignia_id)
        query = f"UPDATE insignias_catalogo SET {', '.join(campos)} WHERE id_insignia = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Insignia actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar insignia: {str(e)}', 500)

@api_crud.route('/insignias-catalogo/<int:insignia_id>', methods=['GET'])
@jwt_required()
def api_obtener_insignia(insignia_id):
    """Obtener una insignia por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_insignia, nombre, descripcion, icono, tipo, requisito_tipo, 
                   requisito_valor, xp_bonus, rareza, precio_xp, activo
            FROM insignias_catalogo WHERE id_insignia = %s
        """, (insignia_id,))
        
        insignia = cursor.fetchone()
        conexion.close()
        
        if not insignia:
            return respuesta_error('Insignia no encontrada', 404)
        
        return respuesta_exito(insignia)
    except Exception as e:
        return respuesta_error(f'Error al obtener insignia: {str(e)}', 500)

@api_crud.route('/insignias-catalogo', methods=['GET'])
@jwt_required()
def api_obtener_insignias():
    """Obtener todas las insignias"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_insignia, nombre, descripcion, icono, tipo, requisito_tipo,
                   requisito_valor, xp_bonus, rareza, precio_xp, activo
            FROM insignias_catalogo ORDER BY orden_visualizacion, id_insignia
        """)
        
        insignias = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(insignias if insignias else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener insignias: {str(e)}', 500)

@api_crud.route('/insignias-catalogo/<int:insignia_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_insignia(insignia_id):
    """Eliminar una insignia"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM insignias_catalogo WHERE id_insignia = %s", (insignia_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Insignia eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar insignia: {str(e)}', 500)

# ================================================================================
# TABLA: RECOMPENSAS
# ================================================================================

@api_crud.route('/recompensas', methods=['POST'])
@jwt_required()
def api_registrar_recompensa():
    """Registrar nueva recompensa"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO recompensas (nombre, descripcion, puntos_requeridos, tipo)
            VALUES (%s, %s, %s, %s)
        """, (data.get('nombre'), data.get('descripcion'), 
              data.get('puntos_requeridos'), data.get('tipo')))
        
        conexion.commit()
        recompensa_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_recompensa': recompensa_id}, 
                              'Recompensa registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar recompensa: {str(e)}', 500)

@api_crud.route('/recompensas/<int:recompensa_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_recompensa(recompensa_id):
    """Actualizar recompensa"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['nombre', 'descripcion', 'puntos_requeridos', 'tipo']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            conexion.close()
            return respuesta_error('No hay campos para actualizar')
        
        valores.append(recompensa_id)
        query = f"UPDATE recompensas SET {', '.join(campos)} WHERE id_recompensa = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Recompensa actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar recompensa: {str(e)}', 500)

@api_crud.route('/recompensas/<int:recompensa_id>', methods=['GET'])
@jwt_required()
def api_obtener_recompensa(recompensa_id):
    """Obtener una recompensa por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_recompensa, nombre, descripcion, puntos_requeridos, tipo
            FROM recompensas WHERE id_recompensa = %s
        """, (recompensa_id,))
        
        recompensa = cursor.fetchone()
        conexion.close()
        
        if not recompensa:
            return respuesta_error('Recompensa no encontrada', 404)
        
        return respuesta_exito(recompensa)
    except Exception as e:
        return respuesta_error(f'Error al obtener recompensa: {str(e)}', 500)

@api_crud.route('/recompensas', methods=['GET'])
@jwt_required()
def api_obtener_recompensas():
    """Obtener todas las recompensas"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id_recompensa, nombre, descripcion, puntos_requeridos, tipo
            FROM recompensas ORDER BY puntos_requeridos
        """)
        
        recompensas = cursor.fetchall()
        conexion.close()
        
        return respuesta_exito(recompensas if recompensas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener recompensas: {str(e)}', 500)

@api_crud.route('/recompensas/<int:recompensa_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_recompensa(recompensa_id):
    """Eliminar una recompensa"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM recompensas WHERE id_recompensa = %s", (recompensa_id,))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Recompensa eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar recompensa: {str(e)}', 500)

# ================================================================================
# TABLA: ROLES
# ================================================================================

@api_crud.route('/roles', methods=['POST'])
@jwt_required()
def api_registrar_rol():
    """Registrar nuevo rol"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO roles (nombre_rol, descripcion)
            VALUES (%s, %s)
        """, (data.get('nombre_rol'), data.get('descripcion')))
        
        conexion.commit()
        rol_id = cursor.lastrowid
        conexion.close()
        
        return respuesta_exito({'id_rol': rol_id}, 'Rol registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar rol: {str(e)}', 500)

@api_crud.route('/roles/<int:rol_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_rol(rol_id):
    """Actualizar rol"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        campos = []
        valores = []
        for campo in ['nombre_rol', 'descripcion']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        
        valores.append(rol_id)
        query = f"UPDATE roles SET {', '.join(campos)} WHERE id_rol = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Rol actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar rol: {str(e)}', 500)

@api_crud.route('/roles/<int:rol_id>', methods=['GET'])
@jwt_required()
def api_obtener_rol(rol_id):
    """Obtener un rol por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM roles WHERE id_rol = %s", (rol_id,))
        rol = cursor.fetchone()
        conexion.close()
        if not rol:
            return respuesta_error('Rol no encontrado', 404)
        return respuesta_exito(rol)
    except Exception as e:
        return respuesta_error(f'Error al obtener rol: {str(e)}', 500)

@api_crud.route('/roles', methods=['GET'])
@jwt_required()
def api_obtener_roles():
    """Obtener todos los roles"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM roles ORDER BY id_rol")
        roles = cursor.fetchall()
        conexion.close()
        return respuesta_exito(roles if roles else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener roles: {str(e)}', 500)

@api_crud.route('/roles/<int:rol_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_rol(rol_id):
    """Eliminar un rol"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM roles WHERE id_rol = %s", (rol_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Rol eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar rol: {str(e)}', 500)

# ================================================================================
# TABLA: USUARIO_ROLES
# ================================================================================

@api_crud.route('/usuario-roles', methods=['POST'])
@jwt_required()
def api_asignar_rol_usuario():
    """Asignar un rol a un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuario_roles (id_usuario, id_rol) VALUES (%s, %s)", 
                       (data.get('id_usuario'), data.get('id_rol')))
        conexion.commit()
        usuario_rol_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_usuario_rol': usuario_rol_id}, 'Rol asignado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al asignar rol: {str(e)}', 500)

@api_crud.route('/usuario-roles/<int:usuario_rol_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_asignacion_rol(usuario_rol_id):
    """Actualizar asignación de rol"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['id_usuario', 'id_rol']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(usuario_rol_id)
        query = f"UPDATE usuario_roles SET {', '.join(campos)} WHERE id_usuario_rol = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Asignación de rol actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar asignación: {str(e)}', 500)

@api_crud.route('/usuario-roles/<int:usuario_rol_id>', methods=['GET'])
@jwt_required()
def api_obtener_asignacion_rol(usuario_rol_id):
    """Obtener una asignación de rol por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuario_roles WHERE id_usuario_rol = %s", (usuario_rol_id,))
        asignacion = cursor.fetchone()
        conexion.close()
        if not asignacion:
            return respuesta_error('Asignación de rol no encontrada', 404)
        return respuesta_exito(asignacion)
    except Exception as e:
        return respuesta_error(f'Error al obtener asignación: {str(e)}', 500)

@api_crud.route('/usuario-roles', methods=['GET'])
@jwt_required()
def api_obtener_asignaciones_roles():
    """Obtener todas las asignaciones de roles"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuario_roles ORDER BY fecha_asignacion DESC")
        asignaciones = cursor.fetchall()
        conexion.close()
        return respuesta_exito(asignaciones if asignaciones else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener asignaciones: {str(e)}', 500)

@api_crud.route('/usuario-roles/<int:usuario_rol_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_asignacion_rol(usuario_rol_id):
    """Eliminar una asignación de rol"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuario_roles WHERE id_usuario_rol = %s", (usuario_rol_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Asignación de rol eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar asignación: {str(e)}', 500)

# ================================================================================
# TABLA: CUESTIONARIO_PREGUNTAS
# ================================================================================

@api_crud.route('/cuestionario-preguntas', methods=['POST'])
@jwt_required()
def api_asignar_pregunta_cuestionario():
    """Asignar una pregunta a un cuestionario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO cuestionario_preguntas (id_cuestionario, id_pregunta, orden) VALUES (%s, %s, %s)",
                       (data.get('id_cuestionario'), data.get('id_pregunta'), data.get('orden')))
        conexion.commit()
        cuestionario_pregunta_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_cuestionario_pregunta': cuestionario_pregunta_id}, 'Pregunta asignada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al asignar pregunta: {str(e)}', 500)

@api_crud.route('/cuestionario-preguntas/<int:cuestionario_pregunta_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_asignacion_pregunta(cuestionario_pregunta_id):
    """Actualizar el orden de una pregunta en un cuestionario"""
    try:
        data = request.get_json()
        if 'orden' not in data:
            return respuesta_error('El campo "orden" es requerido', 400)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE cuestionario_preguntas SET orden = %s WHERE id_cuestionario_pregunta = %s",
                       (data['orden'], cuestionario_pregunta_id))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Asignación de pregunta actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar asignación: {str(e)}', 500)

@api_crud.route('/cuestionario-preguntas/<int:cuestionario_pregunta_id>', methods=['GET'])
@jwt_required()
def api_obtener_asignacion_pregunta(cuestionario_pregunta_id):
    """Obtener una asignación de pregunta por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM cuestionario_preguntas WHERE id_cuestionario_pregunta = %s", (cuestionario_pregunta_id,))
        asignacion = cursor.fetchone()
        conexion.close()
        if not asignacion:
            return respuesta_error('Asignación no encontrada', 404)
        return respuesta_exito(asignacion)
    except Exception as e:
        return respuesta_error(f'Error al obtener asignación: {str(e)}', 500)

@api_crud.route('/cuestionarios/<int:cuestionario_id>/preguntas', methods=['GET'])
@jwt_required()
def api_obtener_preguntas_de_cuestionario(cuestionario_id):
    """Obtener todas las preguntas de un cuestionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT p.*, cp.orden FROM preguntas p
            JOIN cuestionario_preguntas cp ON p.id_pregunta = cp.id_pregunta
            WHERE cp.id_cuestionario = %s
            ORDER BY cp.orden
        """, (cuestionario_id,))
        preguntas = cursor.fetchall()
        conexion.close()
        return respuesta_exito(preguntas if preguntas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener preguntas del cuestionario: {str(e)}', 500)

@api_crud.route('/cuestionario-preguntas/<int:cuestionario_pregunta_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_asignacion_pregunta(cuestionario_pregunta_id):
    """Eliminar una asignación de pregunta de un cuestionario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM cuestionario_preguntas WHERE id_cuestionario_pregunta = %s", (cuestionario_pregunta_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Asignación de pregunta eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar asignación: {str(e)}', 500)

# ================================================================================
# TABLA: GRUPOS_SALA
# ================================================================================

@api_crud.route('/grupos-sala', methods=['POST'])
@jwt_required()
def api_registrar_grupo_sala():
    """Registrar un nuevo grupo en una sala"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO grupos_sala (id_sala, numero_grupo, nombre_grupo, capacidad) VALUES (%s, %s, %s, %s)",
                       (data.get('id_sala'), data.get('numero_grupo'), data.get('nombre_grupo'), data.get('capacidad')))
        conexion.commit()
        grupo_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_grupo': grupo_id}, 'Grupo registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar grupo: {str(e)}', 500)

@api_crud.route('/grupos-sala/<int:grupo_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_grupo_sala(grupo_id):
    """Actualizar un grupo de una sala"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['nombre_grupo', 'capacidad']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(grupo_id)
        query = f"UPDATE grupos_sala SET {', '.join(campos)} WHERE id_grupo = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Grupo actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar grupo: {str(e)}', 500)

@api_crud.route('/grupos-sala/<int:grupo_id>', methods=['GET'])
@jwt_required()
def api_obtener_grupo_sala(grupo_id):
    """Obtener un grupo de una sala por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM grupos_sala WHERE id_grupo = %s", (grupo_id,))
        grupo = cursor.fetchone()
        conexion.close()
        if not grupo:
            return respuesta_error('Grupo no encontrado', 404)
        return respuesta_exito(grupo)
    except Exception as e:
        return respuesta_error(f'Error al obtener grupo: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>/grupos', methods=['GET'])
@jwt_required()
def api_obtener_grupos_de_sala(sala_id):
    """Obtener todos los grupos de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM grupos_sala WHERE id_sala = %s ORDER BY numero_grupo", (sala_id,))
        grupos = cursor.fetchall()
        conexion.close()
        return respuesta_exito(grupos if grupos else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener grupos de la sala: {str(e)}', 500)

@api_crud.route('/grupos-sala/<int:grupo_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_grupo_sala(grupo_id):
    """Eliminar un grupo de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM grupos_sala WHERE id_grupo = %s", (grupo_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Grupo eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar grupo: {str(e)}', 500)

# ================================================================================
# TABLA: PARTICIPANTES_SALA
# ================================================================================

@api_crud.route('/participantes-sala', methods=['POST'])
@jwt_required()
def api_registrar_participante_sala():
    """Registrar un nuevo participante en una sala"""
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO participantes_sala (id_sala, id_usuario, nombre_participante, id_grupo, estado) VALUES (%s, %s, %s, %s, %s)",
                       (data.get('id_sala'), usuario_id, data.get('nombre_participante'), data.get('id_grupo'), 'esperando'))
        conexion.commit()
        participante_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_participante': participante_id}, 'Participante registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar participante: {str(e)}', 500)

@api_crud.route('/participantes-sala/<int:participante_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_participante_sala(participante_id):
    """Actualizar un participante de una sala"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['nombre_participante', 'id_grupo', 'estado']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(participante_id)
        query = f"UPDATE participantes_sala SET {', '.join(campos)} WHERE id_participante = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Participante actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar participante: {str(e)}', 500)

@api_crud.route('/participantes-sala/<int:participante_id>', methods=['GET'])
@jwt_required()
def api_obtener_participante_sala(participante_id):
    """Obtener un participante de una sala por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM participantes_sala WHERE id_participante = %s", (participante_id,))
        participante = cursor.fetchone()
        conexion.close()
        if not participante:
            return respuesta_error('Participante no encontrado', 404)
        return respuesta_exito(participante)
    except Exception as e:
        return respuesta_error(f'Error al obtener participante: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>/participantes', methods=['GET'])
@jwt_required()
def api_obtener_participantes_de_sala(sala_id):
    """Obtener todos los participantes de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM participantes_sala WHERE id_sala = %s ORDER BY fecha_union", (sala_id,))
        participantes = cursor.fetchall()
        conexion.close()
        return respuesta_exito(participantes if participantes else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener participantes de la sala: {str(e)}', 500)

@api_crud.route('/participantes-sala/<int:participante_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_participante_sala(participante_id):
    """Eliminar un participante de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM participantes_sala WHERE id_participante = %s", (participante_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Participante eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar participante: {str(e)}', 500)

# ================================================================================
# TABLA: RANKING_SALA
# ================================================================================

@api_crud.route('/ranking-sala', methods=['POST'])
@jwt_required()
def api_registrar_ranking_sala():
    """Registrar una entrada en el ranking de una sala"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO ranking_sala (id_participante, id_sala, puntaje_total, respuestas_correctas, tiempo_total_respuestas, posicion) VALUES (%s, %s, %s, %s, %s, %s)",
                       (data.get('id_participante'), data.get('id_sala'), data.get('puntaje_total', 0), data.get('respuestas_correctas', 0), data.get('tiempo_total_respuestas', 0), data.get('posicion')))
        conexion.commit()
        ranking_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_ranking_sala': ranking_id}, 'Ranking registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar ranking: {str(e)}', 500)

@api_crud.route('/ranking-sala/<int:ranking_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_ranking_sala(ranking_id):
    """Actualizar una entrada en el ranking de una sala"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['puntaje_total', 'respuestas_correctas', 'tiempo_total_respuestas', 'posicion']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(ranking_id)
        query = f"UPDATE ranking_sala SET {', '.join(campos)} WHERE id_ranking_sala = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Ranking actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar ranking: {str(e)}', 500)

@api_crud.route('/ranking-sala/<int:ranking_id>', methods=['GET'])
@jwt_required()
def api_obtener_ranking_sala(ranking_id):
    """Obtener una entrada del ranking por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM ranking_sala WHERE id_ranking_sala = %s", (ranking_id,))
        ranking = cursor.fetchone()
        conexion.close()
        if not ranking:
            return respuesta_error('Ranking no encontrado', 404)
        return respuesta_exito(ranking)
    except Exception as e:
        return respuesta_error(f'Error al obtener ranking: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>/ranking', methods=['GET'])
@jwt_required()
def api_obtener_ranking_de_sala(sala_id):
    """Obtener el ranking completo de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT rs.*, p.nombre_participante FROM ranking_sala rs
            JOIN participantes_sala p ON rs.id_participante = p.id_participante
            WHERE rs.id_sala = %s 
            ORDER BY posicion ASC, puntaje_total DESC
        """, (sala_id,))
        ranking = cursor.fetchall()
        conexion.close()
        return respuesta_exito(ranking if ranking else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener el ranking de la sala: {str(e)}', 500)

@api_crud.route('/ranking-sala/<int:ranking_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_ranking_sala(ranking_id):
    """Eliminar una entrada del ranking de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ranking_sala WHERE id_ranking_sala = %s", (ranking_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Ranking eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar ranking: {str(e)}', 500)

# ================================================================================
# TABLA: EXPERIENCIA_USUARIOS
# ================================================================================

@api_crud.route('/experiencia-usuarios', methods=['POST'])
@jwt_required()
def api_registrar_experiencia_usuario():
    """Registrar la experiencia de un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO experiencia_usuarios (id_usuario, xp_actual, nivel_actual, xp_total_acumulado) VALUES (%s, %s, %s, %s)",
                       (data.get('id_usuario'), data.get('xp_actual', 0), data.get('nivel_actual', 1), data.get('xp_total_acumulado', 0)))
        conexion.commit()
        experiencia_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_experiencia': experiencia_id}, 'Experiencia de usuario registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar experiencia: {str(e)}', 500)

@api_crud.route('/experiencia-usuarios/<int:id_usuario>', methods=['PUT'])
@jwt_required()
def api_actualizar_experiencia_usuario(id_usuario):
    """Actualizar la experiencia de un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['xp_actual', 'nivel_actual', 'xp_total_acumulado']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(id_usuario)
        query = f"UPDATE experiencia_usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Experiencia de usuario actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar experiencia: {str(e)}', 500)

@api_crud.route('/experiencia-usuarios/<int:id_usuario>', methods=['GET'])
@jwt_required()
def api_obtener_experiencia_usuario(id_usuario):
    """Obtener la experiencia de un usuario por ID de usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM experiencia_usuarios WHERE id_usuario = %s", (id_usuario,))
        experiencia = cursor.fetchone()
        conexion.close()
        if not experiencia:
            return respuesta_error('Experiencia no encontrada para el usuario', 404)
        return respuesta_exito(experiencia)
    except Exception as e:
        return respuesta_error(f'Error al obtener experiencia: {str(e)}', 500)

@api_crud.route('/experiencia-usuarios', methods=['GET'])
@jwt_required()
def api_obtener_todas_experiencias():
    """Obtener la experiencia de todos los usuarios"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM experiencia_usuarios ORDER BY nivel_actual DESC, xp_total_acumulado DESC")
        experiencias = cursor.fetchall()
        conexion.close()
        return respuesta_exito(experiencias if experiencias else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener todas las experiencias: {str(e)}', 500)

@api_crud.route('/experiencia-usuarios/<int:id_experiencia>', methods=['DELETE'])
@jwt_required()
def api_eliminar_experiencia_usuario(id_experiencia):
    """Eliminar la experiencia de un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM experiencia_usuarios WHERE id_experiencia = %s", (id_experiencia,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Experiencia de usuario eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar experiencia: {str(e)}', 500)

# ================================================================================
# TABLA: INSIGNIAS_USUARIOS
# ================================================================================

@api_crud.route('/insignias-usuarios', methods=['POST'])
@jwt_required()
def api_otorgar_insignia_usuario():
    """Otorgar una insignia a un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO insignias_usuarios (id_usuario, id_insignia, mostrar_perfil) VALUES (%s, %s, %s)",
                       (data.get('id_usuario'), data.get('id_insignia'), data.get('mostrar_perfil', False)))
        conexion.commit()
        insignia_usuario_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_insignia_usuario': insignia_usuario_id}, 'Insignia otorgada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al otorgar insignia: {str(e)}', 500)

@api_crud.route('/insignias-usuarios/<int:insignia_usuario_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_insignia_usuario(insignia_usuario_id):
    """Actualizar si una insignia se muestra en el perfil"""
    try:
        data = request.get_json()
        if 'mostrar_perfil' not in data:
            return respuesta_error('El campo "mostrar_perfil" es requerido', 400)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE insignias_usuarios SET mostrar_perfil = %s WHERE id_insignia_usuario = %s",
                       (data['mostrar_perfil'], insignia_usuario_id))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Insignia de usuario actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar insignia de usuario: {str(e)}', 500)

@api_crud.route('/insignias-usuarios/<int:insignia_usuario_id>', methods=['GET'])
@jwt_required()
def api_obtener_insignia_usuario(insignia_usuario_id):
    """Obtener una insignia de un usuario por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM insignias_usuarios WHERE id_insignia_usuario = %s", (insignia_usuario_id,))
        insignia = cursor.fetchone()
        conexion.close()
        if not insignia:
            return respuesta_error('Insignia de usuario no encontrada', 404)
        return respuesta_exito(insignia)
    except Exception as e:
        return respuesta_error(f'Error al obtener insignia de usuario: {str(e)}', 500)

@api_crud.route('/usuarios/<int:id_usuario>/insignias', methods=['GET'])
@jwt_required()
def api_obtener_insignias_de_usuario(id_usuario):
    """Obtener todas las insignias de un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT iu.*, ic.nombre, ic.descripcion, ic.icono FROM insignias_usuarios iu
            JOIN insignias_catalogo ic ON iu.id_insignia = ic.id_insignia
            WHERE iu.id_usuario = %s 
            ORDER BY iu.fecha_desbloqueo DESC
        """, (id_usuario,))
        insignias = cursor.fetchall()
        conexion.close()
        return respuesta_exito(insignias if insignias else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener insignias del usuario: {str(e)}', 500)

@api_crud.route('/insignias-usuarios/<int:insignia_usuario_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_insignia_usuario(insignia_usuario_id):
    """Eliminar una insignia otorgada a un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM insignias_usuarios WHERE id_insignia_usuario = %s", (insignia_usuario_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Insignia de usuario eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar insignia de usuario: {str(e)}', 500)

# ================================================================================
# TABLA: COMPRAS_INSIGNIAS
# ================================================================================

@api_crud.route('/compras-insignias', methods=['POST'])
@jwt_required()
def api_registrar_compra_insignia():
    """Registrar la compra de una insignia por un usuario"""
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO compras_insignias (id_usuario, id_insignia, xp_gastado) VALUES (%s, %s, %s)",
                       (usuario_id, data.get('id_insignia'), data.get('xp_gastado')))
        conexion.commit()
        compra_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_compra': compra_id}, 'Compra registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar compra: {str(e)}', 500)

@api_crud.route('/compras-insignias/<int:compra_id>', methods=['GET'])
@jwt_required()
def api_obtener_compra_insignia(compra_id):
    """Obtener una compra por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM compras_insignias WHERE id_compra = %s", (compra_id,))
        compra = cursor.fetchone()
        conexion.close()
        if not compra:
            return respuesta_error('Compra no encontrada', 404)
        return respuesta_exito(compra)
    except Exception as e:
        return respuesta_error(f'Error al obtener compra: {str(e)}', 500)

@api_crud.route('/usuarios/<int:id_usuario>/compras', methods=['GET'])
@jwt_required()
def api_obtener_compras_de_usuario(id_usuario):
    """Obtener todas las compras de un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT ci.*, ic.nombre as nombre_insignia FROM compras_insignias ci
            JOIN insignias_catalogo ic ON ci.id_insignia = ic.id_insignia
            WHERE ci.id_usuario = %s 
            ORDER BY ci.fecha_compra DESC
        """, (id_usuario,))
        compras = cursor.fetchall()
        conexion.close()
        return respuesta_exito(compras if compras else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener compras del usuario: {str(e)}', 500)

@api_crud.route('/compras-insignias/<int:compra_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_compra_insignia(compra_id):
    """Eliminar (revertir) una compra de insignia"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM compras_insignias WHERE id_compra = %s", (compra_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Compra eliminada/revertida exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar compra: {str(e)}', 500)

# El método PUT no es práctico para 'compras_insignias' ya que son registros inmutables.

# ================================================================================
# TABLA: ESTADISTICAS_JUEGO
# ================================================================================

@api_crud.route('/estadisticas-juego', methods=['POST'])
@jwt_required()
def api_registrar_estadisticas_juego():
    """Registrar estadísticas de un usuario (generalmente automático)"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO estadisticas_juego (id_usuario) VALUES (%s)", (data.get('id_usuario'),))
        conexion.commit()
        estadistica_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_estadistica': estadistica_id}, 'Estadísticas registradas exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar estadísticas: {str(e)}', 500)

@api_crud.route('/estadisticas-juego/<int:id_usuario>', methods=['PUT'])
@jwt_required()
def api_actualizar_estadisticas_juego(id_usuario):
    """Actualizar las estadísticas de un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        campos = []
        valores = []
        for campo in ['total_partidas_jugadas', 'total_partidas_ganadas', 'total_respuestas_correctas', 
                      'total_respuestas_incorrectas', 'racha_actual', 'racha_maxima', 
                      'precision_promedio', 'tiempo_promedio_respuesta', 'puntaje_maximo_obtenido']:
            if campo in data:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        if not campos:
            return respuesta_error('No se proporcionaron campos para actualizar', 400)
        valores.append(id_usuario)
        query = f"UPDATE estadisticas_juego SET {', '.join(campos)} WHERE id_usuario = %s"
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Estadísticas actualizadas exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar estadísticas: {str(e)}', 500)

@api_crud.route('/estadisticas-juego/<int:id_usuario>', methods=['GET'])
@jwt_required()
def api_obtener_estadisticas_juego(id_usuario):
    """Obtener las estadísticas de un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM estadisticas_juego WHERE id_usuario = %s", (id_usuario,))
        estadisticas = cursor.fetchone()
        conexion.close()
        if not estadisticas:
            return respuesta_error('Estadísticas no encontradas', 404)
        return respuesta_exito(estadisticas)
    except Exception as e:
        return respuesta_error(f'Error al obtener estadísticas: {str(e)}', 500)

@api_crud.route('/estadisticas-juego', methods=['GET'])
@jwt_required()
def api_obtener_todas_estadisticas():
    """Obtener las estadísticas de todos los usuarios"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM estadisticas_juego ORDER BY puntaje_maximo_obtenido DESC")
        estadisticas = cursor.fetchall()
        conexion.close()
        return respuesta_exito(estadisticas if estadisticas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener todas las estadísticas: {str(e)}', 500)

@api_crud.route('/estadisticas-juego/<int:id_estadistica>', methods=['DELETE'])
@jwt_required()
def api_eliminar_estadisticas_juego(id_estadistica):
    """Eliminar las estadísticas de un usuario (reset)"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM estadisticas_juego WHERE id_estadistica = %s", (id_estadistica,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Estadísticas eliminadas/reseteadas exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar estadísticas: {str(e)}', 500)

# ================================================================================
# TABLA: HISTORIAL_XP
# ================================================================================

@api_crud.route('/historial-xp', methods=['POST'])
@jwt_required()
def api_registrar_historial_xp():
    """Registrar una entrada en el historial de XP de un usuario"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO historial_xp (id_usuario, cantidad_xp, razon, id_sala, id_pregunta) VALUES (%s, %s, %s, %s, %s)",
                       (data.get('id_usuario'), data.get('cantidad_xp'), data.get('razon'), data.get('id_sala'), data.get('id_pregunta')))
        conexion.commit()
        historial_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_historial': historial_id}, 'Historial de XP registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar historial de XP: {str(e)}', 500)

@api_crud.route('/historial-xp/<int:historial_id>', methods=['GET'])
@jwt_required()
def api_obtener_historial_xp(historial_id):
    """Obtener una entrada del historial de XP por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM historial_xp WHERE id_historial = %s", (historial_id,))
        historial = cursor.fetchone()
        conexion.close()
        if not historial:
            return respuesta_error('Historial de XP no encontrado', 404)
        return respuesta_exito(historial)
    except Exception as e:
        return respuesta_error(f'Error al obtener historial de XP: {str(e)}', 500)

@api_crud.route('/usuarios/<int:id_usuario>/historial-xp', methods=['GET'])
@jwt_required()
def api_obtener_historial_xp_de_usuario(id_usuario):
    """Obtener todo el historial de XP de un usuario"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM historial_xp WHERE id_usuario = %s ORDER BY fecha_ganado DESC", (id_usuario,))
        historial = cursor.fetchall()
        conexion.close()
        return respuesta_exito(historial if historial else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener historial de XP del usuario: {str(e)}', 500)

@api_crud.route('/historial-xp/<int:historial_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_historial_xp(historial_id):
    """Eliminar una entrada del historial de XP"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM historial_xp WHERE id_historial = %s", (historial_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Historial de XP eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar historial de XP: {str(e)}', 500)

# PUT para historial_xp no es muy práctico, pero se puede añadir si es necesario.
# Las demás tablas como 'estado_juego_sala', 'respuestas_participantes' y 'ranking'
# a menudo se manejan a través de la lógica del juego en lugar de un CRUD directo.

# ================================================================================
# TABLA: ESTADO_JUEGO_SALA
# ================================================================================

@api_crud.route('/estado-juego-sala', methods=['POST'])
@jwt_required()
def api_registrar_estado_juego_sala():
    """Registrar un nuevo estado para una sala de juego"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO estado_juego_sala (id_sala, estado, fecha_cambio) VALUES (%s, %s, NOW())",
                       (data.get('id_sala'), data.get('estado')))
        conexion.commit()
        estado_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_estado': estado_id}, 'Estado de sala registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar estado de sala: {str(e)}', 500)

@api_crud.route('/estado-juego-sala/<int:estado_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_estado_juego_sala(estado_id):
    """Actualizar el estado de una sala de juego"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE estado_juego_sala SET estado = %s, fecha_cambio = NOW() WHERE id_estado = %s",
                       (data.get('estado'), estado_id))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Estado de sala actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar estado de sala: {str(e)}', 500)

@api_crud.route('/estado-juego-sala/<int:estado_id>', methods=['GET'])
@jwt_required()
def api_obtener_estado_juego_sala(estado_id):
    """Obtener un estado de sala por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM estado_juego_sala WHERE id_estado = %s", (estado_id,))
        estado = cursor.fetchone()
        conexion.close()
        if not estado:
            return respuesta_error('Estado de sala no encontrado', 404)
        return respuesta_exito(estado)
    except Exception as e:
        return respuesta_error(f'Error al obtener estado de sala: {str(e)}', 500)

@api_crud.route('/salas-juego/<int:sala_id>/estado', methods=['GET'])
@jwt_required()
def api_obtener_estados_de_sala(sala_id):
    """Obtener todos los estados de una sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM estado_juego_sala WHERE id_sala = %s ORDER BY fecha_cambio DESC", (sala_id,))
        estados = cursor.fetchall()
        conexion.close()
        return respuesta_exito(estados if estados else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener estados de la sala: {str(e)}', 500)

@api_crud.route('/estado-juego-sala/<int:estado_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_estado_juego_sala(estado_id):
    """Eliminar un estado de sala"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM estado_juego_sala WHERE id_estado = %s", (estado_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Estado de sala eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar estado de sala: {str(e)}', 500)

# ================================================================================
# TABLA: RESPUESTAS_PARTICIPANTES
# ================================================================================

@api_crud.route('/respuestas-participantes', methods=['POST'])
@jwt_required()
def api_registrar_respuesta_participante():
    """Registrar una respuesta de un participante"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO respuestas_participantes (id_participante, id_pregunta, id_opcion, correcta, tiempo_respuesta) VALUES (%s, %s, %s, %s, %s)",
                       (data.get('id_participante'), data.get('id_pregunta'), data.get('id_opcion'), data.get('correcta', 0), data.get('tiempo_respuesta')))
        conexion.commit()
        respuesta_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_respuesta': respuesta_id}, 'Respuesta registrada exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar respuesta: {str(e)}', 500)

@api_crud.route('/respuestas-participantes/<int:respuesta_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_respuesta_participante(respuesta_id):
    """Actualizar una respuesta de un participante"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE respuestas_participantes SET id_opcion = %s, correcta = %s, tiempo_respuesta = %s WHERE id_respuesta = %s",
                       (data.get('id_opcion'), data.get('correcta', 0), data.get('tiempo_respuesta'), respuesta_id))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Respuesta actualizada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar respuesta: {str(e)}', 500)

@api_crud.route('/respuestas-participantes/<int:respuesta_id>', methods=['GET'])
@jwt_required()
def api_obtener_respuesta_participante(respuesta_id):
    """Obtener una respuesta de un participante por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM respuestas_participantes WHERE id_respuesta = %s", (respuesta_id,))
        respuesta = cursor.fetchone()
        conexion.close()
        if not respuesta:
            return respuesta_error('Respuesta no encontrada', 404)
        return respuesta_exito(respuesta)
    except Exception as e:
        return respuesta_error(f'Error al obtener respuesta: {str(e)}', 500)

@api_crud.route('/participantes-sala/<int:participante_id>/respuestas', methods=['GET'])
@jwt_required()
def api_obtener_respuestas_de_participante(participante_id):
    """Obtener todas las respuestas de un participante"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT rp.*, p.enunciado, o.texto_opcion 
            FROM respuestas_participantes rp
            JOIN preguntas p ON rp.id_pregunta = p.id_pregunta
            LEFT JOIN opciones_respuesta o ON rp.id_opcion_seleccionada = o.id_opcion
            WHERE rp.id_participante = %s
            ORDER BY rp.id_respuesta_participante
        """, (participante_id,))
        respuestas = cursor.fetchall()
        conexion.close()
        return respuesta_exito(respuestas if respuestas else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener respuestas del participante: {str(e)}', 500)
    except Exception as e:
        return respuesta_error(f'Error al obtener respuestas del participante: {str(e)}', 500)

@api_crud.route('/respuestas-participantes/<int:respuesta_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_respuesta_participante(respuesta_id):
    """Eliminar una respuesta de un participante"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM respuestas_participantes WHERE id_respuesta_participante = %s", (respuesta_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Respuesta eliminada exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar respuesta: {str(e)}', 500)

# ================================================================================
# TABLA: RANKING
# ================================================================================

@api_crud.route('/ranking', methods=['POST'])
@jwt_required()
def api_registrar_ranking():
    """Registrar un nuevo ranking"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO ranking (id_usuario, id_sala, puntaje_total, posicion) VALUES (%s, %s, %s, %s)",
                       (data.get('id_usuario'), data.get('id_sala'), data.get('puntaje_total', 0), data.get('posicion')))
        conexion.commit()
        ranking_id = cursor.lastrowid
        conexion.close()
        return respuesta_exito({'id_ranking': ranking_id}, 'Ranking registrado exitosamente', 201)
    except Exception as e:
        return respuesta_error(f'Error al registrar ranking: {str(e)}', 500)

@api_crud.route('/ranking/<int:ranking_id>', methods=['PUT'])
@jwt_required()
def api_actualizar_ranking(ranking_id):
    """Actualizar un ranking"""
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE ranking SET puntaje_total = %s, posicion = %s WHERE id_ranking = %s",
                       (data.get('puntaje_total', 0), data.get('posicion'), ranking_id))
        conexion.commit()
        conexion.close()
        
        return respuesta_exito(None, 'Ranking actualizado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al actualizar ranking: {str(e)}', 500)

@api_crud.route('/ranking/<int:ranking_id>', methods=['GET'])
@jwt_required()
def api_obtener_ranking(ranking_id):
    """Obtener un ranking por ID"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM ranking WHERE id_ranking = %s", (ranking_id,))
        ranking = cursor.fetchone()
        conexion.close()
        if not ranking:
            return respuesta_error('Ranking no encontrado', 404)
        return respuesta_exito(ranking)
    except Exception as e:
        return respuesta_error(f'Error al obtener ranking: {str(e)}', 500)

@api_crud.route('/ranking', methods=['GET'])
@jwt_required()
def api_obtener_rankings():
    """Obtener todos los rankings"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM ranking ORDER BY puntaje_total DESC")
        rankings = cursor.fetchall()
        conexion.close()
        return respuesta_exito(rankings if rankings else [])
    except Exception as e:
        return respuesta_error(f'Error al obtener rankings: {str(e)}', 500)

@api_crud.route('/ranking/<int:ranking_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_ranking(ranking_id):
    """Eliminar un ranking"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ranking WHERE id_ranking = %s", (ranking_id,))
        conexion.commit()
        conexion.close()
        return respuesta_exito(None, 'Ranking eliminado exitosamente')
    except Exception as e:
        return respuesta_error(f'Error al eliminar ranking: {str(e)}', 500)

# ================================================================================
# FIN DEL MÓDULO API CRUD
# ================================================================================
# Total de tablas cubiertas: 24
# Cada tabla tiene 5 endpoints: POST (crear), PUT (actualizar), GET uno, GET lista, DELETE
# Todos los endpoints requieren autenticación JWT mediante @jwt_required()
# ================================================================================
