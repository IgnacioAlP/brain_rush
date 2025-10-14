from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import InternalServerError
from config import config
from bd import verificar_conexion, obtener_conexion, inicializar_usuarios_prueba
import random

# Importar controladores
from controladores import controlador_salas
from controladores import controlador_usuario
from controladores import controlador_cuestionarios
from controladores import controlador_preguntas
from controladores import controlador_participaciones
from controladores import controlador_ranking
from controladores import controlador_recompensas
from controladores import controlador_respuestas
from controladores import controlador_opciones

# Funciones mínimas para hacer funcionar las salas
def verificar_y_crear_tabla_salas():
    """Verifica si existe la tabla salas_juego y la crea si no existe"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'salas_juego'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            print("DEBUG: Tabla salas_juego no existe, creándola...")
            create_table_query = """
            CREATE TABLE salas_juego (
                id_sala INT AUTO_INCREMENT PRIMARY KEY,
                pin_sala VARCHAR(6) UNIQUE NOT NULL,
                id_cuestionario INT,
                modo_juego ENUM('individual', 'grupo') DEFAULT 'individual',
                estado ENUM('esperando', 'en_curso', 'finalizada') DEFAULT 'esperando',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_cuestionario) REFERENCES cuestionarios(id_cuestionario)
            )
            """
            cursor.execute(create_table_query)
            conexion.commit()
            print("DEBUG: Tabla salas_juego creada exitosamente")
        else:
            print("DEBUG: Tabla salas_juego ya existe")
            
        conexion.close()
        return True
        
    except Exception as e:
        print(f"DEBUG: Error al verificar/crear tabla salas_juego: {str(e)}")
        if 'conexion' in locals():
            conexion.close()
        return False

def crear_sala_simple(cuestionario_id):
    try:
        print(f"DEBUG: crear_sala_simple - Iniciando con cuestionario_id: {cuestionario_id}")
        
        # Verificar que la tabla exista
        if not verificar_y_crear_tabla_salas():
            return None, None
            
        pin_sala = str(random.randint(100000, 999999))
        print(f"DEBUG: crear_sala_simple - PIN generado: {pin_sala}")
        
        conexion = obtener_conexion()
        print(f"DEBUG: crear_sala_simple - Conexión obtenida: {conexion}")
        
        cursor = conexion.cursor()
        query = "INSERT INTO salas_juego (pin_sala, id_cuestionario, modo_juego, estado) VALUES (%s, %s, %s, %s)"
        valores = (pin_sala, cuestionario_id, 'individual', 'esperando')
        print(f"DEBUG: crear_sala_simple - Query: {query}")
        print(f"DEBUG: crear_sala_simple - Valores: {valores}")
        
        cursor.execute(query, valores)
        conexion.commit()
        sala_id = cursor.lastrowid
        
        print(f"DEBUG: crear_sala_simple - Sala creada exitosamente con ID: {sala_id}")
        conexion.close()
        
        return sala_id, pin_sala
        
    except Exception as e:
        print(f"DEBUG: ERROR en crear_sala_simple: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.close()
        return None, None

def obtener_sala_por_id_simple(id_sala):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_sala, pin_sala, id_cuestionario, modo_juego, estado, max_participantes, fecha_creacion
            FROM salas_juego 
            WHERE id_sala = %s
        """, (id_sala,))
        sala = cursor.fetchone()
        if sala:
            return {
                'id': sala[0],
                'pin_sala': sala[1],
                'id_cuestionario': sala[2],
                'modo_juego': sala[3],
                'estado': sala[4],
                'max_participantes': sala[5],
                'fecha_creacion': sala[6]
            }
        return None
    finally:
        conexion.close()

def obtener_cuestionario_por_id_simple(id_cuestionario):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_cuestionario, titulo, descripcion FROM cuestionarios WHERE id_cuestionario = %s", (id_cuestionario,))
        return cursor.fetchone()
    finally:
        conexion.close()

def obtener_preguntas_por_cuestionario_simple(id_cuestionario):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM cuestionario_preguntas cp
            JOIN preguntas p ON cp.id_pregunta = p.id_pregunta 
            WHERE cp.id_cuestionario = %s
        """, (id_cuestionario,))
        count = cursor.fetchone()[0]
        return [{'id': i} for i in range(count)]  # Fake questions for count
    finally:
        conexion.close()

def obtener_cuestionarios_por_docente_simple(id_docente):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_cuestionario, titulo, descripcion, id_docente, estado, 
                   fecha_creacion, fecha_programada, fecha_publicacion
            FROM cuestionarios
            WHERE id_docente = %s
            ORDER BY fecha_creacion DESC
        """, (id_docente,))
        resultados = cursor.fetchall()
        
        cuestionarios = []
        for resultado in resultados:
            cuestionarios.append({
                'id_cuestionario': resultado[0],
                'titulo': resultado[1],
                'descripcion': resultado[2],
                'id_docente': resultado[3],
                'estado': resultado[4],
                'fecha_creacion': resultado[5],  # Mantenemos como datetime object
                'fecha_programada': resultado[6],  # Mantenemos como datetime object
                'fecha_publicacion': resultado[7],  # Mantenemos como datetime object
                'num_preguntas': 0  # Por ahora 0, se puede calcular después
            })
        
        return cuestionarios
    finally:
        conexion.close()
import os, json


app = Flask(__name__)

# Configurar la aplicación
env = os.getenv('FLASK_ENV', 'development')
app_config = config.get(env, config['default'])
app.config.from_object(app_config)
app.secret_key = app_config.SECRET_KEY

# Configurar CSRF
csrf = CSRFProtect(app)

#---RUTAS FIJAS---#

@app.route('/')
def index():
    """Página principal que redirije según el estado de sesión"""
    if 'logged_in' in session and session['logged_in']:
        # Usuario ya logueado, redirigir a su dashboard
        if session.get('usuario_tipo') == 'estudiante':
            return redirect(url_for('dashboard_estudiante'))
        else:
            return redirect(url_for('dashboard_admin'))
    else:
        # Usuario no logueado, mostrar página de inicio con nuevo diseño
        return render_template('BrainRush_Master.html')

@app.route('/demo')
def demo():
    """Ruta de demostración del nuevo diseño"""
    return render_template('BrainRush_Master.html')

@app.route('/maestra')
def maestra():
    """Página principal original (mantener por compatibilidad)"""
    return render_template('Maestra.html')

@app.route('/crear_sala')
def crear_sala():
	return render_template('CrearSala.html')

@app.route('/generar_preguntas', methods=['POST'])
def generar_preguntas():
    # Aquí procesas el formulario
    nombre_sala = request.form['nombre_sala']
    # lógica para crear la sala o redirigir
    return render_template('GenerarPreguntas.html', nombre_sala=nombre_sala)

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        # Aceptar JSON o form-data. Validaciones se hacen en el frontend.
        data = request.get_json(silent=True) or request.form.to_dict()
        try:
            nombre = (data.get('nombre') or '').strip()
            apellidos = (data.get('apellidos') or '').strip()
            email = (data.get('email') or '').strip().lower()
            password = data.get('password') or ''
            tipo_usuario = (data.get('tipo_usuario') or 'estudiante').strip().lower()

            print(f"DEBUG: Datos recibidos en registro:")
            print(f"  - nombre: '{nombre}' (len: {len(nombre)})")
            print(f"  - apellidos: '{apellidos}' (len: {len(apellidos)})")
            print(f"  - email: '{email}' (len: {len(email)})")
            print(f"  - password: '{'*' * len(password)}' (len: {len(password)})")
            print(f"  - tipo_usuario: '{tipo_usuario}' (len: {len(tipo_usuario)})")
            print(f"  - form data completo: {data}")

            print(f"DEBUG: Intentando crear usuario: {email}, tipo: {tipo_usuario}")
            
            success, result = controlador_usuario.crear_usuario(nombre, apellidos, email, password, tipo_usuario)
            
            if not success:
                error_msg = result or 'No se pudo registrar el usuario'
                print(f"DEBUG: Error en registro: {error_msg}")
                if request.is_json:
                    return jsonify({ 'success': False, 'error': error_msg }), 400
                flash(error_msg, 'error')
                return render_template('Registrarse.html')
            
            user_id = result
            print(f"DEBUG: Usuario creado exitosamente con ID: {user_id}")
            
            # Iniciar sesión automáticamente después del registro
            session['usuario_id'] = user_id
            session['usuario_email'] = email
            session['usuario_nombre'] = nombre
            session['usuario_apellidos'] = apellidos
            session['usuario_tipo'] = tipo_usuario
            session['logged_in'] = True
            
            # Redirigir según el tipo de usuario
            if tipo_usuario == 'estudiante':
                redirect_url = url_for('dashboard_estudiante')
            elif tipo_usuario == 'docente':
                redirect_url = url_for('dashboard_docente')
            else:
                redirect_url = url_for('dashboard_admin')
            
            if request.is_json:
                return jsonify({ 'success': True, 'user_id': user_id, 'redirect': redirect_url })
            
            flash('¡Registro completado exitosamente!', 'success')
            return redirect(redirect_url)
            
        except Exception as e:
            print(f"DEBUG: Excepción en registro: {str(e)}")
            error_msg = 'Error interno del sistema'
            if request.is_json:
                return jsonify({ 'success': False, 'error': error_msg, 'detail': str(e) }), 500
            flash(error_msg, 'error')
            return render_template('Registrarse.html')
    
    return render_template('Registrarse.html')

@app.route('/unirse_a_sala', methods=['GET', 'POST'])
def unirse_a_sala():
    if request.method == 'POST':
        # Procesar datos del formulario de unirse a sala aquí
        pass
    return render_template('UnirseASala.html')

# Ruta de error de sistema divertida
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        print(f"DEBUG: Intento de login para email: {email}")
        
        if not email or not password:
            error_msg = 'Email y contraseña son requeridos'
            if request.is_json:
                return jsonify({ 'success': False, 'error': error_msg }), 400
            flash(error_msg, 'error')
            return render_template('Login.html')

        ok, usuario = controlador_usuario.autenticar_usuario(email, password)
        if not ok:
            error_msg = 'Email o contraseña incorrectos'
            print(f"DEBUG: Login fallido para {email}")
            if request.is_json:
                return jsonify({ 'success': False, 'error': error_msg }), 400
            flash(error_msg, 'error')
            return render_template('Login.html')

        # Guardar información del usuario en la sesión
        session['usuario_id'] = usuario['id_usuario']
        session['usuario_email'] = usuario['email']
        session['usuario_nombre'] = usuario['nombre']
        session['usuario_apellidos'] = usuario['apellidos']
        session['usuario_tipo'] = usuario['tipo_usuario']
        session['logged_in'] = True

        print(f"DEBUG: Login exitoso para {email}, tipo: {usuario['tipo_usuario']}")

        # Redirigir según el tipo de usuario
        if usuario['tipo_usuario'] == 'estudiante':  # Estudiante
            if request.is_json:
                return jsonify({ 'success': True, 'redirect': url_for('dashboard_estudiante') })
            return redirect(url_for('dashboard_estudiante'))
        elif usuario['tipo_usuario'] == 'docente':  # Docente
            if request.is_json:
                return jsonify({ 'success': True, 'redirect': url_for('dashboard_docente') })
            return redirect(url_for('dashboard_docente'))
        else:  # Administrador u otros
            if request.is_json:
                return jsonify({ 'success': True, 'redirect': url_for('dashboard_admin') })
            return redirect(url_for('dashboard_admin'))
            
    except Exception as e:
        error_msg = f'Error del sistema: {str(e)}'
        print(f"DEBUG: Error en login: {error_msg}")
        if request.is_json:
            return jsonify({ 'success': False, 'error': 'Error del sistema. Intenta nuevamente.' }), 500
        flash('Error del sistema. Intenta nuevamente.', 'error')
        return render_template('Login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión del usuario"""
    session.clear()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

def login_required(f):
    """Decorador para requerir login"""
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    """Decorador para requerir permisos de administrador"""
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        if session.get('usuario_tipo') == 'estudiante':
            flash('No tienes permisos para acceder a esta sección', 'error')
            return redirect(url_for('dashboard_estudiante'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/estudiante')
@login_required
def dashboard_estudiante():
    """Dashboard para estudiantes"""
    if session.get('usuario_tipo') != 'estudiante':
        return redirect(url_for('dashboard_admin'))
    
    usuario = {
        'id_usuario': session['usuario_id'],
        'nombre': session['usuario_nombre'],
        'apellidos': session['usuario_apellidos'],
        'email': session['usuario_email'],
        'tipo_usuario': session['usuario_tipo']
    }
    
    # Obtener estadísticas del estudiante
    try:
        estadisticas = controlador_usuario.obtener_estadisticas_usuario(session['usuario_id'])
    except:
        estadisticas = {
            'total_participaciones': 0,
            'promedio_puntaje': 0,
            'mejor_posicion': 'N/A',
            'recompensas_obtenidas': 0
        }
    
    return render_template('DashboardEstudiante.html', usuario=usuario, estadisticas=estadisticas)

@app.route('/admin')
@login_required 
@admin_required
def dashboard_admin():
    """Dashboard para administradores, maestros, etc."""
    usuario = {
        'id_usuario': session['usuario_id'],
        'nombre': session['usuario_nombre'],
        'apellidos': session['usuario_apellidos'],
        'email': session['usuario_email'],
        'tipo_usuario': session['usuario_tipo']
    }
    
    # Si es docente, redirigir al dashboard de docente
    if session['usuario_tipo'] == 'docente':
        return redirect(url_for('dashboard_docente'))
    
    # Obtener estadísticas del sistema para administradores
    try:
        estadisticas = {
            'total_usuarios': len(controlador_usuario.obtener_todos_usuarios()),
            'total_cuestionarios': len(controlador_cuestionarios.obtener_cuestionarios()),
            'salas_activas': len(controlador_salas.obtener_salas_activas()),
            'total_participaciones': len(controlador_participaciones.obtener_participaciones()),
            'total_preguntas': len(controlador_preguntas.obtener_preguntas())
        }
    except:
        estadisticas = {
            'total_usuarios': 0,
            'total_cuestionarios': 0,
            'salas_activas': 0,
            'total_participaciones': 0,
            'total_preguntas': 0
        }
    
    return render_template('DashboardAdmin.html', usuario=usuario, estadisticas=estadisticas)

@app.route('/docente')
@login_required
def dashboard_docente():
    """Dashboard específico para docentes"""
    usuario = {
        'id_usuario': session['usuario_id'],
        'nombre': session['usuario_nombre'],
        'apellidos': session['usuario_apellidos'],
        'email': session['usuario_email'],
        'tipo_usuario': session['usuario_tipo']
    }
    
    # Obtener cuestionarios del docente
    try:
        id_docente = session['usuario_id']
        cuestionarios = obtener_cuestionarios_por_docente_simple(id_docente)
        
        # Estadísticas específicas del docente
        estadisticas = {
            'total_cuestionarios': len(cuestionarios),
            'cuestionarios_activos': len([c for c in cuestionarios if c.get('estado') == 'activo']),
            'total_estudiantes': 0,  # Implementar función para contar estudiantes únicos
            'total_respuestas': 0,    # Implementar función para contar respuestas
            'promedio_calificaciones': 0  # Implementar función para promedio
        }
        
        # Obtener resultados recientes de estudiantes
        resultados_recientes = []  # Implementar función para obtener resultados
        
    except Exception as e:
        print(f"Error obteniendo datos del docente: {e}")
        cuestionarios = []
        estadisticas = {
            'total_cuestionarios': 0,
            'cuestionarios_activos': 0,
            'total_estudiantes': 0,
            'total_respuestas': 0,
            'promedio_calificaciones': 0
        }
        resultados_recientes = []
    
    return render_template('DashboardDocente.html', 
                         usuario=usuario, 
                         estadisticas=estadisticas,
                         cuestionarios=cuestionarios,
                         resultados_recientes=resultados_recientes)

@app.route('/dashboard')
@login_required
def dashboard():
    """Ruta genérica de dashboard que redirije según el tipo de usuario"""
    if session.get('usuario_tipo') == 'estudiante':
        return redirect(url_for('dashboard_estudiante'))
    else:
        return redirect(url_for('dashboard_admin'))

# Rutas adicionales para estudiantes
@app.route('/historial/estudiante')
@login_required
def historial_estudiante():
    """Historial de participaciones del estudiante"""
    if session.get('usuario_tipo') != 'estudiante':
        return redirect(url_for('dashboard_admin'))
    
    try:
        participaciones = controlador_participaciones.obtener_participaciones_por_usuario(session['usuario_id'])
    except:
        participaciones = []
    
    return render_template('HistorialEstudiante.html', participaciones=participaciones)

@app.route('/ranking/global')
@login_required
def ranking_global():
    """Ranking global del sistema"""
    try:
        ranking = controlador_ranking.obtener_ranking_global()
    except:
        ranking = []
    
    return render_template('RankingGlobal.html', ranking=ranking)

@app.route('/mis-recompensas')
@login_required
def mis_recompensas():
    """Recompensas del estudiante"""
    if session.get('usuario_tipo') != 'estudiante':
        return redirect(url_for('dashboard_admin'))
    
    try:
        recompensas = controlador_recompensas.verificar_recompensas_disponibles(session['usuario_id'])
    except:
        recompensas = []
    
    return render_template('MisRecompensas.html', recompensas=recompensas)

# Rutas adicionales para administradores  
@app.route('/monitoreo/salas')
@login_required
@admin_required
def monitoreo_salas():
    """Monitoreo de salas activas"""
    try:
        salas = controlador_salas.obtener_salas_activas()
    except:
        salas = []
    
    return render_template('MonitoreoSalas.html', salas=salas)

@app.route('/reportes/sistema')
@login_required
@admin_required
def reportes_sistema():
    """Reportes y estadísticas del sistema"""
    try:
        estadisticas = controlador_cuestionarios.obtener_estadisticas_sistema()
    except:
        estadisticas = {}
    
    return render_template('ReportesSystem.html', estadisticas=estadisticas)

@app.route('/configuracion/sistema')
@login_required
@admin_required  
def configuracion_sistema():
    """Configuración del sistema"""
    return render_template('ConfiguracionSistema.html')

@app.route('/backup/datos')
@login_required
@admin_required
def backup_datos():
    """Backup de datos"""
    return render_template('BackupDatos.html')

@app.route('/logs/sistema')
@login_required
@admin_required
def logs_sistema():
    """Logs del sistema"""
    return render_template('LogsSistema.html')

@app.route('/otorgar-recompensas')
@login_required
@admin_required
def otorgar_recompensas():
    """Otorgar recompensas"""
    return render_template('OtorgarRecompensas.html')

@app.route('/errorsistema')
def error_sistema_page():
    # Renderiza un template divertido de error interno
    return render_template('ErrorSistema.html'), 500

# Rutas para salas
@app.route('/crear-sala', methods=['GET', 'POST'])
def crear_sala_route():
    if request.method == 'GET':
        return render_template('CrearSala.html')
    
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        nombre = data.get('nombre', '').strip()
        cuestionario_id = int(data.get('cuestionario_id'))
        tipo_sala = data.get('tipo_sala', 'individual')
        max_participantes = int(data.get('max_participantes', 30))
        tiempo_respuesta = int(data.get('tiempo_respuesta', 30))
        configuracion = data.get('configuracion', {})
        
        if not nombre:
            raise ValueError("El nombre de la sala es requerido")
        
        # Verificar que el cuestionario existe y pertenece al docente
        cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(cuestionario_id)
        if not cuestionario:
            raise ValueError("El cuestionario seleccionado no existe")
        
        # Crear la sala
        sala_id = controlador_salas.crear_sala(
            nombre=nombre,
            cuestionario_id=cuestionario_id,
            docente_id=session.get('user_id', 1),  # Por ahora usar 1 como default
            tipo_sala=tipo_sala,
            max_participantes=max_participantes,
            tiempo_respuesta=tiempo_respuesta
        )
        
        if request.is_json:
            return jsonify({'success': True, 'sala_id': sala_id, 'message': 'Sala creada exitosamente'})
        flash('¡Sala creada exitosamente!', 'success')
        return redirect(url_for('monitorear_sala', sala_id=sala_id))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al crear la sala: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/mis-salas')
def mis_salas():
    try:
        # Por ahora mostrar todas las salas, luego filtrar por docente
        salas = controlador_salas.obtener_salas()
        return render_template('MisSalas.html', salas=salas)
    except Exception as e:
        flash(f'Error al obtener las salas: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/sala/<string:codigo>/unirse', methods=['GET', 'POST'])
def unirse_sala_route(codigo):
    if request.method == 'GET':
        return render_template('UnirseASala.html')
    
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        nombre_participante = data.get('nombre_participante', '').strip()
        
        if not nombre_participante:
            raise ValueError("El nombre del participante es requerido")
        
        # Buscar la sala por código
        sala = controlador_salas.obtener_sala_por_codigo(codigo)
        if not sala:
            raise ValueError("Sala no encontrada")
        
        if sala['estado'] != 'esperando':
            raise ValueError("La sala no está disponible para unirse")
        
        # Verificar límite de participantes
        participantes_actuales = controlador_salas.obtener_participantes_sala(sala['id'])
        if len(participantes_actuales) >= sala['max_participantes']:
            raise ValueError("La sala ha alcanzado el límite de participantes")
        
        # Agregar el participante a la sala
        participante_id = controlador_salas.agregar_participante_sala(sala['id'], nombre_participante)
        
        session['participante_id'] = participante_id
        session['sala_id'] = sala['id']
        session['nombre_participante'] = nombre_participante
        
        if request.is_json:
            return jsonify({'success': True, 'participante_id': participante_id})
        return redirect(url_for('esperar_juego', sala_id=sala['id']))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al unirse a la sala: {str(e)}', 'error')
        return redirect(url_for('unirse_sala_route', codigo=codigo))

@app.route('/sala/<int:sala_id>/monitorear')
@app.route('/monitorear-sala/<int:sala_id>')
def monitorear_sala(sala_id):
    try:
        print(f"DEBUG: monitorear_sala - sala_id: {sala_id}")
        
        # Usar la función simple que ya existe
        sala = obtener_sala_por_id_simple(sala_id)
        print(f"DEBUG: Sala obtenida: {sala}")
        
        if not sala:
            print("DEBUG: Sala no encontrada")
            flash('Sala no encontrada', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        # Obtener participantes reales de la sala
        participantes = controlador_salas.obtener_participantes_sala(sala['id'])
        print(f"DEBUG: Participantes: {participantes}")
        
        # Verificar si existe el template MonitoreoJuego.html
        try:
            return render_template('MonitoreoJuego.html', sala=sala, participantes=participantes)
        except Exception as template_error:
            print(f"DEBUG: Error de template: {template_error}")
            # Template temporal hasta que se implemente MonitoreoJuego.html
            return render_template('MonitoreoJuego.html', 
                                 sala=sala,
                                 participantes=participantes)
            
    except Exception as e:
        print(f"DEBUG: Error en monitorear_sala: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error al cargar la sala: {str(e)}', 'error')
        return redirect(url_for('mis_cuestionarios'))

@app.route('/sala/<int:sala_id>/iniciar', methods=['POST'])
def iniciar_sala(sala_id):
    try:
        resultado = iniciar_juego_sala(sala_id)
        
        if not resultado:
            raise ValueError("No se pudo iniciar la sala")
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Sala iniciada exitosamente'})
        flash('¡Sala iniciada exitosamente!', 'success')
        return redirect(url_for('monitorear_sala', sala_id=sala_id))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al iniciar la sala: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/sala/<int:sala_id>/cerrar', methods=['POST'])
def cerrar_sala(sala_id):
    try:
        resultado = finalizar_sala(sala_id)
        
        if not resultado:
            raise ValueError("No se pudo cerrar la sala")
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Sala cerrada exitosamente'})
        flash('¡Sala cerrada exitosamente!', 'success')
        return redirect(url_for('mis_salas'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al cerrar la sala: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

# Rutas para respuestas y participaciones
@app.route('/responder-pregunta', methods=['POST'])
def responder_pregunta():
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        pregunta_id = int(data.get('pregunta_id'))
        participacion_id = int(data.get('participacion_id'))
        respuesta_seleccionada = data.get('respuesta_seleccionada', '').strip()
        tiempo_respuesta = float(data.get('tiempo_respuesta', 0))
        
        if not respuesta_seleccionada:
            raise ValueError("Debe seleccionar una respuesta")
        
        # Crear la respuesta
        respuesta_id = crear_respuesta_participante(
            participacion_id=participacion_id,
            pregunta_id=pregunta_id,
            respuesta_seleccionada=respuesta_seleccionada,
            tiempo_respuesta=tiempo_respuesta
        )
        
        # Verificar si la respuesta es correcta y calcular puntaje
        es_correcta, puntaje = verificar_respuesta_correcta(pregunta_id, respuesta_seleccionada, tiempo_respuesta)
        
        # Actualizar puntaje de la respuesta
        if es_correcta:
            actualizar_puntaje_respuesta(respuesta_id, puntaje)
        
        return jsonify({
            'success': True,
            'respuesta_id': respuesta_id,
            'es_correcta': es_correcta,
            'puntaje': puntaje,
            'message': 'Respuesta registrada exitosamente'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/resultados-participacion/<int:participacion_id>')
def ver_resultados_participacion(participacion_id):
    try:
        resultados = obtener_resultados_participacion(participacion_id)
        return render_template('ResultadosJuego.html', resultados=resultados)
    except Exception as e:
        flash(f'Error al obtener los resultados: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/ranking-sala/<int:sala_id>')
def ver_ranking_sala(sala_id):
    try:
        ranking = obtener_ranking_sala(sala_id)
        return jsonify({'success': True, 'ranking': ranking})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Rutas de administración y sistema
@app.route('/admin/usuarios')
def admin_usuarios():
    try:
        usuarios = obtener_todos_usuarios()
        return render_template('AdminUsuarios.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al cargar usuarios: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/admin/estadisticas')
def admin_estadisticas():
    try:
        estadisticas = obtener_estadisticas_sistema()
        return render_template('Estadisticas.html', estadisticas=estadisticas)
    except Exception as e:
        flash(f'Error al cargar estadísticas: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/perfil/<int:user_id>')
def perfil_usuario(user_id):
    try:
        usuario = obtener_usuario_por_id(user_id)
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('maestra'))
        
        # Obtener estadísticas del usuario
        estadisticas = obtener_estadisticas_usuario(user_id)
        
        return render_template('PerfilUsuario.html', usuario=usuario, estadisticas=estadisticas)
    except Exception as e:
        flash(f'Error al cargar el perfil: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion_sistema_old():
    if request.method == 'GET':
        try:
            configuracion = obtener_configuracion_sistema()
            return render_template('ConfiguracionSistema.html', configuracion=configuracion)
        except Exception as e:
            flash(f'Error al cargar configuración: {str(e)}', 'error')
            return redirect(url_for('error_sistema_page'))
    
    # POST - actualizar configuración
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        actualizar_configuracion_sistema(data)
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Configuración actualizada exitosamente'})
        flash('¡Configuración actualizada exitosamente!', 'success')
        return redirect(url_for('configuracion_sistema'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al actualizar configuración: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

# Rutas de juego tiempo real
@app.route('/juego/<int:sala_id>/estudiante')
def juego_estudiante(sala_id):
    try:
        # Verificar que el estudiante está en la sala
        participante_id = session.get('participante_id')
        if not participante_id:
            flash('Debes unirte a una sala primero', 'error')
            return redirect(url_for('unirse_sala_route', codigo=''))
        
        sala = obtener_sala_por_id(sala_id)
        if not sala:
            flash('Sala no encontrada', 'error')
            return redirect(url_for('maestra'))
        
        return render_template('JuegoEstudiante.html', sala=sala, participante_id=participante_id)
    except Exception as e:
        flash(f'Error al cargar el juego: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/juego/<int:sala_id>/siguiente-pregunta')
def siguiente_pregunta(sala_id):
    try:
        pregunta = obtener_siguiente_pregunta_sala(sala_id)
        if not pregunta:
            return jsonify({'success': False, 'finished': True, 'message': 'No hay más preguntas'})
        
        return jsonify({'success': True, 'pregunta': pregunta})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/esperar-juego/<int:sala_id>')
def esperar_juego(sala_id):
    try:
        sala = obtener_sala_por_id(sala_id)
        if not sala:
            flash('Sala no encontrada', 'error')
            return redirect(url_for('maestra'))
        
        return render_template('EsperarJuego.html', sala=sala)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

# Rutas para juegos
@app.route('/crear-cuestionario', methods=['GET', 'POST'])
def crear_cuestionario_route():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
        try:
            titulo = data.get('titulo', '').strip()
            descripcion = data.get('descripcion', '').strip()
            id_docente = session.get('usuario_id', 1)  # Usar usuario de sesión si está disponible
            
            if not titulo:
                raise ValueError("El título es requerido")
            
            # Debug: Verificar los datos antes de crear
            print(f"DEBUG: Creando cuestionario - titulo: {titulo}, id_docente: {id_docente}")
            
            cuestionario_id = controlador_cuestionarios.crear_cuestionario(titulo, descripcion, id_docente)
            
            print(f"DEBUG: Cuestionario creado con ID: {cuestionario_id}")
            
            if request.is_json:
                return jsonify({'success': True, 'cuestionario_id': cuestionario_id, 'message': 'Cuestionario creado exitosamente'})
            
            # FLUJO CORREGIDO: Después de crear el cuestionario, redirigir a agregar preguntas
            flash('¡Cuestionario creado exitosamente! Ahora puedes agregar preguntas.', 'success')
            return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
            
        except Exception as e:
            print(f"DEBUG: Error al crear cuestionario: {str(e)}")
            if request.is_json:
                return jsonify({'success': False, 'error': str(e)}), 400
            flash(f'Error al crear el cuestionario: {str(e)}', 'error')
            return redirect(url_for('error_sistema_page'))
    
    return render_template('CrearCuestionario.html')

# Nueva ruta: Agregar preguntas a un cuestionario recién creado
@app.route('/agregar-preguntas/<int:cuestionario_id>', methods=['GET', 'POST'])
def agregar_preguntas(cuestionario_id):
    print(f"DEBUG: *** agregar_preguntas - Método: {request.method}, cuestionario_id: {cuestionario_id}")
    
    # Si es POST, procesar el formulario de agregar pregunta
    if request.method == 'POST':
        print(f"DEBUG: *** Procesando POST - Form data: {dict(request.form)}")
        try:
            # Verificar que el usuario es docente
            if session.get('usuario_tipo') != 'docente':
                print(f"DEBUG: Usuario no es docente: {session.get('usuario_tipo')}")
                flash('Solo los docentes pueden agregar preguntas', 'error')
                return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
            
            # Obtener datos del formulario
            enunciado = request.form.get('question_text', '').strip()
            tipo = request.form.get('question_type', 'opcion_multiple')
            
            print(f"DEBUG: Enunciado: '{enunciado}', Tipo: '{tipo}'")
            
            if not enunciado:
                flash('El enunciado de la pregunta es requerido', 'error')
                return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
            
            # Verificar que el cuestionario pertenece al docente
            cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id_simple(cuestionario_id)
            if not cuestionario:
                flash('Cuestionario no encontrado', 'error')
                return redirect(url_for('mis_cuestionarios'))
            
            id_docente_actual = session.get('usuario_id', 1)
            if cuestionario[3] != id_docente_actual:
                flash('No tienes permisos para agregar preguntas a este cuestionario', 'error')
                return redirect(url_for('mis_cuestionarios'))
            
            # Crear la pregunta
            pregunta_id = controlador_preguntas.crear_pregunta(enunciado, tipo, cuestionario_id)
            print(f"DEBUG: Resultado crear_pregunta: {pregunta_id}")
            
            if pregunta_id:
                print(f"DEBUG: Pregunta {pregunta_id} creada exitosamente")
                
                # Si es opción múltiple, agregar las opciones
                if tipo == 'opcion_multiple':
                    opciones = []
                    opcion_correcta = request.form.get('correct_answer', '').strip()
                    print(f"DEBUG: Opción correcta seleccionada: '{opcion_correcta}'")
                    
                    for i in range(0, 4):  # option_0, option_1, option_2, option_3
                        opcion_texto = request.form.get(f'option_{i}', '').strip()
                        if opcion_texto:
                            # Verificar si esta opción es la correcta (índice como string)
                            es_correcta = (str(i) == opcion_correcta)
                            opciones.append({
                                'texto': opcion_texto,
                                'es_correcta': es_correcta
                            })
                            print(f"DEBUG: Opción {i}: '{opcion_texto}' (correcta: {es_correcta})")
                    
                    # Crear las opciones de respuesta
                    for opcion in opciones:
                        resultado = controlador_preguntas.crear_opcion_respuesta(pregunta_id, opcion['texto'], opcion['es_correcta'])
                        print(f"DEBUG: Opción creada: {resultado}")
                
                flash('Pregunta agregada exitosamente', 'success')
            else:
                flash('Error al crear la pregunta', 'error')
            
            return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
            
        except Exception as e:
            print(f"DEBUG: Error procesando pregunta: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            flash(f'Error al procesar la pregunta: {str(e)}', 'error')
            return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
    
    # Si es GET, mostrar el formulario
    try:
        # Verificar que el cuestionario existe y pertenece al usuario actual
        cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id_simple(cuestionario_id)
        print(f"DEBUG: agregar_preguntas GET - cuestionario obtenido: {cuestionario}")
        
        if not cuestionario:
            print(f"DEBUG: Cuestionario {cuestionario_id} no encontrado")
            flash('Cuestionario no encontrado', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        # Verificar que el cuestionario pertenece al usuario actual
        id_docente_actual = session.get('usuario_id', 1)
        if cuestionario[3] != id_docente_actual:  # cuestionario[3] es id_docente
            print(f"DEBUG: Usuario {id_docente_actual} no tiene permisos para cuestionario del docente {cuestionario[3]}")
            flash('No tienes permisos para editar este cuestionario', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        # Obtener las preguntas existentes del cuestionario
        preguntas = []
        try:
            preguntas = controlador_preguntas.obtener_preguntas_por_cuestionario(cuestionario_id)
        except Exception as e:
            print(f"DEBUG: Error obteniendo preguntas: {e}")
            preguntas = []  # En caso de error, asumimos que no hay preguntas aún
        
        # Convertir cuestionario (tupla) a diccionario para el template
        cuestionario_data = {
            'id_cuestionario': cuestionario[0],
            'titulo': cuestionario[1], 
            'descripcion': cuestionario[2],
            'id_docente': cuestionario[3],
            'fecha_creacion': cuestionario[4],
            'fecha_programada': cuestionario[5] if len(cuestionario) > 5 else None,
            'fecha_publicacion': cuestionario[6] if len(cuestionario) > 6 else None,
            'estado': cuestionario[7] if len(cuestionario) > 7 else 'borrador'
        }
        
        print(f"DEBUG: Mostrando GenerarPreguntas.html con cuestionario: {cuestionario_data}")
        print(f"DEBUG: Número de preguntas existentes: {len(preguntas)}")
        
        # Usar GenerarPreguntas.html que ya existe
        return render_template('GenerarPreguntas.html', 
                             cuestionario=cuestionario_data, 
                             preguntas=preguntas)
    
    except Exception as e:
        print(f"DEBUG: Error en agregar_preguntas GET: {str(e)}")
        flash(f'Error al cargar el cuestionario: {str(e)}', 'error')
        return redirect(url_for('mis_cuestionarios'))


# Nueva ruta: Crear sala específicamente para un cuestionario
@app.route('/crear-sala-cuestionario/<int:cuestionario_id>', methods=['GET', 'POST'])
def crear_sala_para_cuestionario(cuestionario_id):
    try:
        print(f"DEBUG: crear_sala_para_cuestionario - cuestionario_id: {cuestionario_id}, method: {request.method}")
        
        # Verificar que el cuestionario existe y tiene preguntas
        cuestionario = obtener_cuestionario_por_id_simple(cuestionario_id)
        print(f"DEBUG: Cuestionario obtenido: {cuestionario}")
        
        if not cuestionario:
            flash('Cuestionario no encontrado', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        # Verificar que el cuestionario tiene preguntas
        preguntas = obtener_preguntas_por_cuestionario_simple(cuestionario_id)
        print(f"DEBUG: Preguntas encontradas: {len(preguntas) if preguntas else 0}")
        
        if not preguntas or len(preguntas) == 0:
            flash('No se puede crear una sala para un cuestionario sin preguntas. Agrega preguntas primero.', 'error')
            return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
        
        if request.method == 'POST':
            print("DEBUG: Procesando POST para crear sala")
            data = request.get_json(silent=True) or request.form.to_dict()
            print(f"DEBUG: Datos recibidos: {data}")
            
            nombre_sala = data.get('nombre_sala', f"Sala - {cuestionario[1]}")  # cuestionario[1] es el titulo
            capacidad_maxima = int(data.get('capacidad_maxima', 50))
            id_docente = session.get('usuario_id', 1)
            
            print(f"DEBUG: Creando sala - nombre: {nombre_sala}, capacidad: {capacidad_maxima}, docente: {id_docente}")
            
            # Crear la sala
            try:
                sala_id, codigo_sala = crear_sala_simple(cuestionario_id)
                print(f"DEBUG: Sala creada con ID: {sala_id}, código: {codigo_sala}")
                
                if sala_id and codigo_sala:
                    # Para peticiones POST, siempre devolver JSON (ya que el frontend espera JSON)
                    print("DEBUG: Devolviendo respuesta JSON exitosa")
                    return jsonify({
                        'success': True, 
                        'sala_id': sala_id,
                        'codigo_sala': codigo_sala,
                        'capacidad': capacidad_maxima,
                        'message': 'Sala creada exitosamente'
                    })
                else:
                    error_msg = 'No se pudo crear la sala - función crear_sala_simple retornó valores nulos'
                    print(f"DEBUG: Error - {error_msg}")
                    print("DEBUG: Devolviendo respuesta JSON de error")
                    return jsonify({
                        'success': False,
                        'error': error_msg
                    }), 500
                    
            except Exception as sala_error:
                error_msg = f'Error al crear la sala: {str(sala_error)}'
                print(f"DEBUG: Exception en creación de sala: {error_msg}")
                print("DEBUG: Devolviendo respuesta JSON de excepción")
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 500
        
        # GET: Mostrar formulario para crear sala
        print("DEBUG: Mostrando formulario GET")
        cuestionario_data = {
            'id_cuestionario': cuestionario[0],
            'titulo': cuestionario[1],
            'descripcion': cuestionario[2],
            'num_preguntas': len(preguntas)
        }
        print(f"DEBUG: Datos del cuestionario para template: {cuestionario_data}")
        
        return render_template('CrearSalaEspecifica.html', cuestionario=cuestionario_data)
        
    except Exception as e:
        print(f"DEBUG: Error en crear_sala_para_cuestionario: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error al crear la sala: {str(e)}', 'error')
        return redirect(url_for('mis_cuestionarios'))

# Ruta para publicar un cuestionario
@app.route('/publicar-cuestionario/<int:cuestionario_id>', methods=['POST'])
@login_required
def publicar_cuestionario_route(cuestionario_id):
    try:
        if session.get('usuario_tipo') != 'docente':
            return jsonify({'success': False, 'error': 'Solo los docentes pueden publicar cuestionarios'}), 403
        
        id_docente = session.get('usuario_id')
        
        # Verificar que el cuestionario tiene preguntas antes de publicar
        try:
            preguntas = controlador_preguntas.obtener_preguntas_por_cuestionario(cuestionario_id)
            if not preguntas or len(preguntas) == 0:
                return jsonify({
                    'success': False, 
                    'error': 'No se puede publicar un cuestionario sin preguntas'
                }), 400
        except:
            return jsonify({
                'success': False, 
                'error': 'Error al verificar las preguntas del cuestionario'
            }), 500
        
        # Usar la nueva función publicar_cuestionario
        success, mensaje = controlador_cuestionarios.publicar_cuestionario(cuestionario_id, id_docente)
        
        if success:
            return jsonify({
                'success': True, 
                'message': mensaje
            })
        else:
            return jsonify({
                'success': False, 
                'error': mensaje
            }), 400
            
    except Exception as e:
        print(f"DEBUG: Error en publicar_cuestionario: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Ruta para despublicar un cuestionario
@app.route('/despublicar-cuestionario/<int:cuestionario_id>', methods=['POST'])
@login_required
def despublicar_cuestionario_route(cuestionario_id):
    try:
        if session.get('usuario_tipo') != 'docente':
            return jsonify({'success': False, 'error': 'Solo los docentes pueden despublicar cuestionarios'}), 403
        
        id_docente = session.get('usuario_id')
        
        # Usar la nueva función despublicar_cuestionario
        success, mensaje = controlador_cuestionarios.despublicar_cuestionario(cuestionario_id, id_docente)
        
        if success:
            return jsonify({
                'success': True, 
                'message': mensaje
            })
        else:
            return jsonify({
                'success': False, 
                'error': mensaje
            }), 400
            
    except Exception as e:
        print(f"DEBUG: Error en despublicar_cuestionario: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/mis-cuestionarios')
def mis_cuestionarios():
    try:
        id_docente = session.get('usuario_id', 1)  # Usar usuario de sesión si está disponible
        print(f"DEBUG: Obteniendo cuestionarios para docente ID: {id_docente}")
        
        cuestionarios = obtener_cuestionarios_por_docente_simple(id_docente)
        print(f"DEBUG: Cuestionarios encontrados: {len(cuestionarios) if cuestionarios else 0}")
        
        print(f"DEBUG: Cuestionarios: {cuestionarios}")
        return render_template('MisCuestionarios.html', cuestionarios=cuestionarios)
    except Exception as e:
        print(f"DEBUG: Error al obtener cuestionarios: {str(e)}")
        flash(f'Error al obtener cuestionarios: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/cuestionario/<int:cuestionario_id>')
def ver_cuestionario(cuestionario_id):
    try:
        cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(cuestionario_id)
        if not cuestionario:
            flash('Cuestionario no encontrado', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        preguntas = controlador_preguntas.obtener_preguntas_por_cuestionario(cuestionario_id)
        return render_template('VerCuestionario.html', cuestionario=cuestionario, preguntas=preguntas)
    except Exception as e:
        flash(f'Error al obtener cuestionario: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/editar-cuestionario/<int:cuestionario_id>')
def editar_cuestionario(cuestionario_id):
    try:
        print(f"DEBUG: Editando cuestionario ID: {cuestionario_id}")
        
        # Verificar que el usuario es docente
        if session.get('usuario_tipo') != 'docente':
            flash('Solo los docentes pueden editar cuestionarios', 'error')
            return redirect(url_for('dashboard_docente'))
        
        # Usar la función que devuelve diccionario
        cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(cuestionario_id)
        print(f"DEBUG: Cuestionario obtenido (diccionario): {cuestionario}")
        
        if not cuestionario:
            print(f"DEBUG: Cuestionario {cuestionario_id} no encontrado")
            flash('Cuestionario no encontrado', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        # Verificar que el cuestionario pertenece al docente actual
        id_docente_actual = session.get('usuario_id', 1)
        if cuestionario.get('id_docente') != id_docente_actual:
            print(f"DEBUG: Usuario {id_docente_actual} no tiene permisos para cuestionario del docente {cuestionario.get('id_docente')}")
            flash('No tienes permisos para editar este cuestionario', 'error')
            return redirect(url_for('mis_cuestionarios'))
        
        print(f"DEBUG: Obteniendo preguntas para cuestionario {cuestionario_id}")
        preguntas = []
        try:
            preguntas = controlador_preguntas.obtener_preguntas_por_cuestionario(cuestionario_id)
            print(f"DEBUG: Preguntas obtenidas: {len(preguntas) if preguntas else 0}")
        except Exception as e:
            print(f"DEBUG: Error obteniendo preguntas: {e}")
            preguntas = []
        
        return render_template('EditarCuestionario.html', 
                             cuestionario=cuestionario, 
                             preguntas=preguntas, 
                             cuestionario_id=cuestionario_id)
    except Exception as e:
        print(f"DEBUG: Error en editar_cuestionario: {str(e)}")
        print(f"DEBUG: Tipo de error: {type(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        flash(f'Error al obtener cuestionario: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/editar-cuestionario/<int:cuestionario_id>', methods=['POST'])
def actualizar_cuestionario_route(cuestionario_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        titulo = data.get('titulo', '').strip()
        descripcion = data.get('descripcion', '').strip()
        
        if not titulo:
            raise ValueError("El título es requerido")
        
        resultado = controlador_cuestionarios.actualizar_cuestionario(cuestionario_id, titulo, descripcion)
        
        if not resultado:
            raise ValueError("No se pudo actualizar el cuestionario")
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Cuestionario actualizado exitosamente'})
        flash('¡Cuestionario actualizado exitosamente!', 'success')
        return redirect(url_for('mis_cuestionarios'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al actualizar el cuestionario: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/eliminar-cuestionario/<int:cuestionario_id>', methods=['POST'])
def eliminar_cuestionario_route(cuestionario_id):
    try:
        resultado = controlador_cuestionarios.eliminar_cuestionario(cuestionario_id)
        
        if not resultado:
            raise ValueError("No se pudo eliminar el cuestionario")
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Cuestionario eliminado exitosamente'})
        flash('¡Cuestionario eliminado exitosamente!', 'success')
        return redirect(url_for('mis_cuestionarios'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al eliminar el cuestionario: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

# Rutas para preguntas
@app.route('/crear-pregunta/<int:cuestionario_id>', methods=['POST'])
def crear_pregunta_route(cuestionario_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        enunciado = data.get('enunciado', '').strip()
        tipo = data.get('tipo_pregunta', 'opcion_multiple')  # Corregido: usar 'tipo_pregunta'
        puntaje_base = int(data.get('puntaje_base', 1))
        tiempo_limite = int(data.get('tiempo_limite', 30))
        
        # Obtener opciones del formulario
        opciones_textos = request.form.getlist('opciones[]')
        respuesta_correcta_index = int(data.get('respuesta_correcta', 0))
        
        if not enunciado:
            raise ValueError("El enunciado es requerido")
        
        # Crear la pregunta
        pregunta_id = controlador_preguntas.crear_pregunta(enunciado, tipo, puntaje_base, tiempo_limite)
        
        # Crear las opciones si hay opciones de texto
        if opciones_textos and len(opciones_textos) > 0:
            for i, texto_opcion in enumerate(opciones_textos):
                if texto_opcion.strip():  # Solo crear si no está vacío
                    es_correcta = (i == respuesta_correcta_index)
                    controlador_opciones.crear_opcion_respuesta(pregunta_id, texto_opcion.strip(), es_correcta)
        
        # Obtener el siguiente orden para la pregunta en el cuestionario
        preguntas_existentes = controlador_preguntas.obtener_preguntas_por_cuestionario(cuestionario_id)
        orden = len(preguntas_existentes) + 1
        
        # Agregar la pregunta al cuestionario
        controlador_preguntas.agregar_pregunta_a_cuestionario(cuestionario_id, pregunta_id, orden)
        
        if request.is_json:
            return jsonify({'success': True, 'pregunta_id': pregunta_id, 'message': 'Pregunta creada exitosamente'})
        flash('¡Pregunta creada exitosamente!', 'success')
        return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))
    except Exception as e:
        print(f"DEBUG: Error en crear_pregunta_route: {str(e)}")
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al crear la pregunta: {str(e)}', 'error')
        return redirect(url_for('agregar_preguntas', cuestionario_id=cuestionario_id))

@app.route('/editar-pregunta/<int:pregunta_id>', methods=['POST'])
def editar_pregunta_route(pregunta_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        enunciado = data.get('enunciado', '').strip()
        tipo = data.get('tipo', 'opcion_multiple')
        puntaje_base = int(data.get('puntaje_base', 1))
        tiempo_limite = int(data.get('tiempo_limite', 30))
        opciones_data = data.get('opciones', [])
        
        if not enunciado:
            raise ValueError("El enunciado es requerido")
        
        # Actualizar la pregunta
        resultado = controlador_preguntas.actualizar_pregunta(pregunta_id, enunciado, tipo, puntaje_base, tiempo_limite)
        
        if not resultado:
            raise ValueError("No se pudo actualizar la pregunta")
        
        # Actualizar las opciones si es de opción múltiple
        if tipo == 'opcion_multiple' and opciones_data:
            actualizar_opciones_multiple(pregunta_id, opciones_data)
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Pregunta actualizada exitosamente'})
        flash('¡Pregunta actualizada exitosamente!', 'success')
        return redirect(request.referrer or url_for('mis_cuestionarios'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al actualizar la pregunta: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/eliminar-pregunta/<int:pregunta_id>', methods=['POST'])
def eliminar_pregunta_route(pregunta_id):
    try:
        resultado = controlador_preguntas.eliminar_pregunta(pregunta_id)
        
        if not resultado:
            raise ValueError("No se pudo eliminar la pregunta")
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Pregunta eliminada exitosamente'})
        flash('¡Pregunta eliminada exitosamente!', 'success')
        return redirect(request.referrer or url_for('mis_cuestionarios'))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error al eliminar la pregunta: {str(e)}', 'error')
        return redirect(url_for('error_sistema_page'))

@app.route('/pregunta/<int:pregunta_id>/opciones')
def obtener_opciones_pregunta(pregunta_id):
    try:
        opciones = controlador_opciones.obtener_opciones_por_pregunta(pregunta_id)
        return jsonify({'success': True, 'opciones': opciones})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
@app.route('/unirse-juego', methods=['GET', 'POST'])
def unirse_juego():
    if request.method == 'POST':
        # Procesar unión al juego
        data = request.get_json(silent=True) or request.form.to_dict()
        try:
            pin_sala = data.get('pin_sala', '').strip()
            nombre_jugador = data.get('nombre_jugador', '').strip()
            
            # Aquí iría la validación del PIN y registro del jugador
            if request.is_json:
                return jsonify({'success': True, 'redirect': f'/sala-espera/{pin_sala}'})
            return redirect(url_for('sala_espera', pin_sala=pin_sala))
        except Exception as e:
            if request.is_json:
                return jsonify({'success': False, 'error': str(e)}), 400
            flash('Error al unirse al juego', 'error')
            return redirect(url_for('error_sistema_page'))
    
    return render_template('UnirseJuego.html')

@app.route('/sala-espera/<pin_sala>')
def sala_espera(pin_sala):
    try:
        # Validar el PIN y obtener info de la sala
        sala = controlador_salas.obtener_sala_por_codigo(pin_sala)
        if not sala:
            flash('Sala no encontrada', 'error')
            return redirect(url_for('unirse_a_sala'))
        
        if sala['estado'] != 'esperando':
            flash('La sala no está disponible', 'error')
            return redirect(url_for('unirse_a_sala'))
        
        # Obtener participantes conectados
        participantes = controlador_salas.obtener_participantes_sala(sala['id'])
        
        # Obtener información del cuestionario
        cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(sala['id_cuestionario'])
        
        return render_template('SalaEspera.html', 
                             sala=sala, 
                             participantes=participantes,
                             cuestionario=cuestionario,
                             pin_sala=pin_sala)
    except Exception as e:
        print(f"Error en sala_espera: {e}")
        flash('Error al acceder a la sala', 'error')
        return redirect(url_for('unirse_a_sala'))

@app.route('/juego-estudiante/<pin_sala>')
def juego_estudiante_por_pin(pin_sala):
    # Aquí iría la lógica para obtener las preguntas del juego
    return render_template('JuegoEstudiante.html', pin_sala=pin_sala)

@app.route('/monitoreo-juego/<pin_sala>')
def monitoreo_juego(pin_sala):
    # Aquí iría la lógica para obtener el estado actual del juego
    return render_template('MonitoreoJuego.html', pin_sala=pin_sala)

@app.route('/resultados-juego/<pin_sala>')
def resultados_juego(pin_sala):
    # Aquí iría la lógica para obtener los resultados finales
    return render_template('ResultadosJuego.html', pin_sala=pin_sala)

# Rutas para APIs (respuestas JSON)
@app.route('/api/participantes/<pin_sala>')
def api_obtener_participantes(pin_sala):
    try:
        # Validar sala
        sala = controlador_salas.obtener_sala_por_codigo(pin_sala)
        if not sala:
            return jsonify({'success': False, 'error': 'Sala no encontrada'}), 404
        
        # Obtener participantes actuales
        participantes = controlador_salas.obtener_participantes_sala(sala['id'])
        
        # Formatear respuesta
        participantes_response = []
        for p in participantes:
            participantes_response.append({
                'id': p['id_participante'],
                'nombre': p['nombre_participante'],
                'estado': p['estado'],
                'fecha_union': p['fecha_union'].strftime('%Y-%m-%d %H:%M:%S') if p['fecha_union'] else None
            })
        
        return jsonify({
            'success': True, 
            'participantes': participantes_response,
            'total': len(participantes_response),
            'sala_estado': sala['estado']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/iniciar-juego/<pin_sala>', methods=['POST'])
def api_iniciar_juego(pin_sala):
    try:
        # Validar sala
        sala = controlador_salas.obtener_sala_por_codigo(pin_sala)
        if not sala:
            return jsonify({'success': False, 'error': 'Sala no encontrada'}), 404
        
        # Actualizar estado de la sala
        controlador_salas.actualizar_estado_sala(sala['id'], 'en_curso')
        
        return jsonify({'success': True, 'message': 'Juego iniciado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/enviar-respuesta/<pin_sala>', methods=['POST'])
def api_enviar_respuesta(pin_sala):
    try:
        data = request.get_json()
        jugador_id = data.get('jugador_id')
        pregunta_id = data.get('pregunta_id')
        respuesta = data.get('respuesta')
        
        # Lógica para procesar la respuesta
        return jsonify({'success': True, 'puntos': 100})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/estado-juego/<pin_sala>')
def api_estado_juego(pin_sala):
    try:
        # Lógica para obtener el estado actual del juego
        estado = {
            'pregunta_actual': 1,
            'total_preguntas': 10,
            'participantes': 8,
            'tiempo_restante': 30
        }
        return jsonify(estado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

###############################
# RUTAS CRUD PARA EL DASHBOARD
###############################

#-----INICIO-USUARIO-----#
@app.route('/usuario')
def usuario():
    usuarios = controlador_usuario.obtener_usuarios()
    return render_template('dashboard/usuario.html', usuarios=usuarios)

@app.route('/registrar_usuario')
def registrar_usuario():
    return render_template('dashboard/registrar_usuario.html')

@app.route('/insertar_usuario', methods=['POST'])
def insertar_usuario():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']
    password = request.form['password']
    tipo_usuario = request.form['tipo_usuario']
    controlador_usuario.crear_usuario(
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        password=password,
        tipo_usuario=tipo_usuario
    )
    return redirect(url_for('usuario'))

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    controlador_usuario.eliminar_usuario(id)
    return redirect(url_for('usuario'))

@app.route('/modificar_usuario', methods=['POST'])
def modificar_usuario():
    id = request.form['id']
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template('dashboard/modificar_usuario.html', usuario=usuario)

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    id = request.form['id']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']
    tipo_usuario = request.form['tipo_usuario']
    controlador_usuario.actualizar_usuario(id, nombre, apellidos, email, tipo_usuario)
    return redirect(url_for('usuario'))

@app.route('/suspender_usuario', methods=['POST'])
def suspender_usuario():
    id = request.form['id']
    controlador_usuario.cambiar_estado_usuario(id, 'suspendido')
    return redirect(url_for('usuario'))

@app.route('/activar_usuario', methods=['POST'])
def activar_usuario():
    id = request.form['id']
    controlador_usuario.cambiar_estado_usuario(id, 'activo')
    return redirect(url_for('usuario'))
#-----FIN-USUARIO-----#

#-----INICIO-CUESTIONARIO-----#
@app.route('/cuestionario')
def cuestionario():
    cuestionarios = controlador_cuestionarios.obtener_cuestionarios()
    return render_template('dashboard/cuestionario.html', cuestionarios=cuestionarios)

@app.route('/registrar_cuestionario')
def registrar_cuestionario():
    docentes = controlador_usuario.obtener_usuarios_por_tipo('docente')
    return render_template('dashboard/registrar_cuestionario.html', docentes=docentes)

@app.route('/insertar_cuestionario', methods=['POST'])
def insertar_cuestionario():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    id_docente = request.form['id_docente']
    categoria = request.form.get('categoria', '')
    tiempo_limite = request.form.get('tiempo_limite', 0)
    max_intentos = request.form.get('max_intentos', 1)
    
    controlador_cuestionarios.crear_cuestionario(
        titulo=titulo,
        descripcion=descripcion,
        id_docente=id_docente,
        categoria=categoria,
        tiempo_limite=tiempo_limite,
        max_intentos=max_intentos
    )
    return redirect(url_for('cuestionario'))

@app.route('/eliminar_cuestionario/<int:id>')
def eliminar_cuestionario(id):
    controlador_cuestionarios.eliminar_cuestionario(id)
    return redirect(url_for('cuestionario'))

@app.route('/modificar_cuestionario', methods=['POST'])
def modificar_cuestionario():
    id = request.form['id']
    cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(id)
    docentes = controlador_usuario.obtener_usuarios_por_tipo('docente')
    return render_template('dashboard/modificar_cuestionario.html', cuestionario=cuestionario, docentes=docentes)

@app.route('/actualizar_cuestionario', methods=['POST'])
def actualizar_cuestionario():
    id = request.form['id']
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    id_docente = request.form['id_docente']
    categoria = request.form.get('categoria', '')
    tiempo_limite = request.form.get('tiempo_limite', 0)
    max_intentos = request.form.get('max_intentos', 1)
    
    controlador_cuestionarios.actualizar_cuestionario(id, titulo, descripcion, id_docente, categoria, tiempo_limite, max_intentos)
    return redirect(url_for('cuestionario'))

@app.route('/publicar_cuestionario', methods=['POST'])
def publicar_cuestionario_dashboard():
    id = request.form['id']
    controlador_cuestionarios.cambiar_estado_cuestionario(id, 'publicado')
    return redirect(url_for('cuestionario'))

@app.route('/despublicar_cuestionario', methods=['POST'])
def despublicar_cuestionario():
    id = request.form['id']
    controlador_cuestionarios.cambiar_estado_cuestionario(id, 'borrador')
    return redirect(url_for('cuestionario'))
#-----FIN-CUESTIONARIO-----#

#-----INICIO-PREGUNTA-----#
@app.route('/pregunta')
def pregunta():
    preguntas = controlador_preguntas.obtener_preguntas()
    return render_template('dashboard/pregunta.html', preguntas=preguntas)

@app.route('/registrar_pregunta')
def registrar_pregunta():
    cuestionarios = controlador_cuestionarios.obtener_cuestionarios()
    return render_template('dashboard/registrar_pregunta.html', cuestionarios=cuestionarios)

@app.route('/insertar_pregunta', methods=['POST'])
def insertar_pregunta():
    enunciado = request.form['enunciado']
    tipo = request.form['tipo']
    puntaje_base = request.form.get('puntaje_base', 1)
    tiempo_limite = request.form.get('tiempo_limite', 30)
    archivo_multimedia = request.form.get('archivo_multimedia', '')
    id_cuestionario = request.form.get('id_cuestionario')
    
    pregunta_id = controlador_preguntas.crear_pregunta(
        enunciado=enunciado,
        tipo=tipo,
        puntaje_base=puntaje_base,
        tiempo_limite=tiempo_limite,
        archivo_multimedia=archivo_multimedia
    )
    
    # Si se especificó un cuestionario, agregar la pregunta
    if id_cuestionario:
        orden = controlador_cuestionario_preguntas.contar_preguntas_cuestionario(id_cuestionario) + 1
        controlador_preguntas.agregar_pregunta_a_cuestionario(id_cuestionario, pregunta_id, orden)
    
    return redirect(url_for('pregunta'))

@app.route('/eliminar_pregunta/<int:id>')
def eliminar_pregunta(id):
    controlador_preguntas.eliminar_pregunta(id)
    return redirect(url_for('pregunta'))

@app.route('/modificar_pregunta', methods=['POST'])
def modificar_pregunta():
    id = request.form['id']
    pregunta = controlador_preguntas.obtener_pregunta_por_id(id)
    cuestionarios = controlador_cuestionarios.obtener_cuestionarios()
    return render_template('dashboard/modificar_pregunta.html', pregunta=pregunta, cuestionarios=cuestionarios)

@app.route('/actualizar_pregunta', methods=['POST'])
def actualizar_pregunta():
    id = request.form['id']
    enunciado = request.form['enunciado']
    tipo = request.form['tipo']
    puntaje_base = request.form.get('puntaje_base', 1)
    tiempo_limite = request.form.get('tiempo_limite', 30)
    archivo_multimedia = request.form.get('archivo_multimedia', '')
    
    controlador_preguntas.actualizar_pregunta(id, enunciado, tipo, puntaje_base, tiempo_limite, archivo_multimedia)
    return redirect(url_for('pregunta'))
#-----FIN-PREGUNTA-----#

#-----INICIO-OPCION-----#
@app.route('/opcion')
def opcion():
    opciones = controlador_opciones.obtener_opciones()
    return render_template('dashboard/opcion.html', opciones=opciones)

@app.route('/registrar_opcion')
def registrar_opcion():
    preguntas = controlador_preguntas.obtener_preguntas()
    return render_template('dashboard/registrar_opcion.html', preguntas=preguntas)

@app.route('/insertar_opcion', methods=['POST'])
def insertar_opcion():
    id_pregunta = request.form['id_pregunta']
    texto_opcion = request.form['texto_opcion']
    es_correcta = 'es_correcta' in request.form
    explicacion = request.form.get('explicacion', '')
    
    controlador_opciones.crear_opcion(
        id_pregunta=id_pregunta,
        texto_opcion=texto_opcion,
        es_correcta=es_correcta,
        explicacion=explicacion
    )
    return redirect(url_for('opcion'))

@app.route('/eliminar_opcion/<int:id>')
def eliminar_opcion(id):
    controlador_opciones.eliminar_opcion(id)
    return redirect(url_for('opcion'))

@app.route('/modificar_opcion', methods=['POST'])
def modificar_opcion():
    id = request.form['id']
    opcion = controlador_opciones.obtener_opcion_por_id(id)
    preguntas = controlador_preguntas.obtener_preguntas()
    return render_template('dashboard/modificar_opcion.html', opcion=opcion, preguntas=preguntas)

@app.route('/actualizar_opcion', methods=['POST'])
def actualizar_opcion():
    id = request.form['id']
    id_pregunta = request.form['id_pregunta']
    texto_opcion = request.form['texto_opcion']
    es_correcta = 'es_correcta' in request.form
    explicacion = request.form.get('explicacion', '')
    
    controlador_opciones.actualizar_opcion(id, id_pregunta, texto_opcion, es_correcta, explicacion)
    return redirect(url_for('opcion'))
#-----FIN-OPCION-----#

#-----INICIO-SALA-----#
@app.route('/sala')
def sala():
    salas = controlador_salas.obtener_salas()
    return render_template('dashboard/sala.html', salas=salas)

@app.route('/registrar_sala')
def registrar_sala():
    cuestionarios = controlador_cuestionarios.obtener_cuestionarios_publicados()
    docentes = controlador_usuario.obtener_usuarios_por_tipo('docente')
    return render_template('dashboard/registrar_sala.html', cuestionarios=cuestionarios, docentes=docentes)

@app.route('/insertar_sala', methods=['POST'])
def insertar_sala():
    nombre = request.form['nombre']
    id_cuestionario = request.form['id_cuestionario']
    id_docente = request.form['id_docente']
    tipo_sala = request.form.get('tipo_sala', 'individual')
    max_participantes = request.form.get('max_participantes', 30)
    tiempo_respuesta = request.form.get('tiempo_respuesta', 30)
    
    controlador_salas.crear_sala(
        nombre=nombre,
        id_cuestionario=id_cuestionario,
        id_docente=id_docente,
        tipo_sala=tipo_sala,
        max_participantes=max_participantes,
        tiempo_respuesta=tiempo_respuesta
    )
    return redirect(url_for('sala'))

@app.route('/eliminar_sala/<int:id>')
def eliminar_sala(id):
    controlador_salas.eliminar_sala(id)
    return redirect(url_for('sala'))

@app.route('/modificar_sala', methods=['POST'])
def modificar_sala():
    id = request.form['id']
    sala = controlador_salas.obtener_sala_por_id(id)
    cuestionarios = controlador_cuestionarios.obtener_cuestionarios_publicados()
    docentes = controlador_usuario.obtener_usuarios_por_tipo('docente')
    return render_template('dashboard/modificar_sala.html', sala=sala, cuestionarios=cuestionarios, docentes=docentes)

@app.route('/actualizar_sala', methods=['POST'])
def actualizar_sala():
    id = request.form['id']
    nombre = request.form['nombre']
    id_cuestionario = request.form['id_cuestionario']
    id_docente = request.form['id_docente']
    tipo_sala = request.form.get('tipo_sala', 'individual')
    max_participantes = request.form.get('max_participantes', 30)
    tiempo_respuesta = request.form.get('tiempo_respuesta', 30)
    
    controlador_salas.actualizar_sala(id, nombre, id_cuestionario, id_docente, tipo_sala, max_participantes, tiempo_respuesta)
    return redirect(url_for('sala'))

@app.route('/iniciar_sala', methods=['POST'])
def iniciar_sala_dashboard():
    id = request.form['id']
    controlador_salas.cambiar_estado_sala(id, 'activa')
    return redirect(url_for('sala'))

@app.route('/cerrar_sala', methods=['POST'])
def cerrar_sala_dashboard():
    id = request.form['id']
    controlador_salas.cambiar_estado_sala(id, 'finalizada')
    return redirect(url_for('sala'))
#-----FIN-SALA-----#

#-----INICIO-PARTICIPACION-----#
@app.route('/participacion')
def participacion():
    participaciones = controlador_participaciones.obtener_participaciones()
    return render_template('dashboard/participacion.html', participaciones=participaciones)

@app.route('/ver_participacion/<int:id>')
def ver_participacion(id):
    participacion = controlador_participaciones.obtener_participacion_por_id(id)
    respuestas = controlador_respuestas.obtener_respuestas_por_participacion(id)
    return render_template('dashboard/ver_participacion.html', participacion=participacion, respuestas=respuestas)

@app.route('/finalizar_participacion', methods=['POST'])
def finalizar_participacion():
    id = request.form['id']
    puntaje_total = request.form.get('puntaje_total', 0)
    controlador_participaciones.finalizar_participacion(id, puntaje_total)
    return redirect(url_for('participacion'))

@app.route('/eliminar_participacion/<int:id>')
def eliminar_participacion(id):
    controlador_participaciones.eliminar_participacion(id)
    return redirect(url_for('participacion'))
#-----FIN-PARTICIPACION-----#

#-----INICIO-RESPUESTA-----#
@app.route('/respuesta')
def respuesta():
    respuestas = controlador_respuestas.obtener_respuestas()
    return render_template('dashboard/respuesta.html', respuestas=respuestas)

@app.route('/calificar_respuesta', methods=['POST'])
def calificar_respuesta():
    id = request.form['id']
    puntaje_obtenido = request.form['puntaje_obtenido']
    es_correcta = 'es_correcta' in request.form
    controlador_respuestas.calificar_respuesta(id, puntaje_obtenido, es_correcta)
    return redirect(url_for('respuesta'))

@app.route('/ver_respuesta/<int:id>')
def ver_respuesta(id):
    respuesta = controlador_respuestas.obtener_respuesta_por_id(id)
    return render_template('dashboard/ver_respuesta.html', respuesta=respuesta)

@app.route('/eliminar_respuesta/<int:id>')
def eliminar_respuesta(id):
    controlador_respuestas.eliminar_respuesta(id)
    return redirect(url_for('respuesta'))
#-----FIN-RESPUESTA-----#

#-----INICIO-RANKING-----#
@app.route('/ranking')
def ranking():
    ranking_global = controlador_ranking.obtener_ranking_global()
    return render_template('dashboard/ranking.html', ranking=ranking_global)

@app.route('/ranking_cuestionario/<int:id_cuestionario>')
def ranking_cuestionario(id_cuestionario):
    ranking = controlador_ranking.obtener_ranking_cuestionario(id_cuestionario)
    cuestionario = controlador_cuestionarios.obtener_cuestionario_por_id(id_cuestionario)
    return render_template('dashboard/ranking_cuestionario.html', ranking=ranking, cuestionario=cuestionario)

@app.route('/ranking_sala/<int:id_sala>')
def ranking_sala(id_sala):
    ranking = controlador_ranking.obtener_ranking_sala(id_sala)
    sala = controlador_salas.obtener_sala_por_id(id_sala)
    return render_template('dashboard/ranking_sala.html', ranking=ranking, sala=sala)

@app.route('/actualizar_ranking_cuestionario', methods=['POST'])
def actualizar_ranking_cuestionario():
    id_cuestionario = request.form['id_cuestionario']
    controlador_ranking.actualizar_ranking_completo(id_cuestionario)
    return redirect(url_for('ranking_cuestionario', id_cuestionario=id_cuestionario))

@app.route('/estadisticas_ranking')
def estadisticas_ranking():
    estadisticas = controlador_ranking.obtener_estadisticas_ranking(1)  # Ejemplo con ID 1
    return render_template('dashboard/estadisticas_ranking.html', estadisticas=estadisticas)
#-----FIN-RANKING-----#

#-----INICIO-RECOMPENSA-----#
@app.route('/recompensa')
def recompensa():
    recompensas = controlador_recompensas.obtener_recompensas()
    return render_template('dashboard/recompensa.html', recompensas=recompensas)

@app.route('/registrar_recompensa')
def registrar_recompensa():
    return render_template('dashboard/registrar_recompensa.html')

@app.route('/insertar_recompensa', methods=['POST'])
def insertar_recompensa():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    puntos_requeridos = request.form['puntos_requeridos']
    tipo = request.form['tipo']
    
    controlador_recompensas.crear_recompensa(
        nombre=nombre,
        descripcion=descripcion,
        puntos_requeridos=puntos_requeridos,
        tipo=tipo
    )
    return redirect(url_for('recompensa'))

@app.route('/eliminar_recompensa/<int:id>')
def eliminar_recompensa(id):
    controlador_recompensas.eliminar_recompensa(id)
    return redirect(url_for('recompensa'))

@app.route('/modificar_recompensa', methods=['POST'])
def modificar_recompensa():
    id = request.form['id']
    recompensa = controlador_recompensas.obtener_recompensa_por_id(id)
    return render_template('dashboard/modificar_recompensa.html', recompensa=recompensa)

@app.route('/actualizar_recompensa', methods=['POST'])
def actualizar_recompensa():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    puntos_requeridos = request.form['puntos_requeridos']
    tipo = request.form['tipo']
    
    controlador_recompensas.actualizar_recompensa(id, nombre, descripcion, puntos_requeridos, tipo)
    return redirect(url_for('recompensa'))

@app.route('/otorgar_recompensa', methods=['POST'])
def otorgar_recompensa():
    id_estudiante = request.form['id_estudiante']
    id_recompensa = request.form['id_recompensa']
    controlador_recompensas.otorgar_recompensa(id_estudiante, id_recompensa)
    return redirect(url_for('recompensa'))

@app.route('/revocar_recompensa', methods=['POST'])
def revocar_recompensa():
    id_estudiante = request.form['id_estudiante']
    id_recompensa = request.form['id_recompensa']
    controlador_recompensas.revocar_recompensa(id_estudiante, id_recompensa)
    return redirect(url_for('recompensa'))
#-----FIN-RECOMPENSA-----#

#-----INICIO-ROL-----#
@app.route('/rol')
def rol():
    roles = controlador_roles.obtener_roles()
    return render_template('dashboard/rol.html', roles=roles)

@app.route('/registrar_rol')
def registrar_rol():
    return render_template('dashboard/registrar_rol.html')

@app.route('/insertar_rol', methods=['POST'])
def insertar_rol():
    nombre_rol = request.form['nombre_rol']
    descripcion = request.form['descripcion']
    
    controlador_roles.crear_rol(
        nombre_rol=nombre_rol,
        descripcion=descripcion
    )
    return redirect(url_for('rol'))

@app.route('/eliminar_rol/<int:id>')
def eliminar_rol(id):
    controlador_roles.eliminar_rol(id)
    return redirect(url_for('rol'))

@app.route('/modificar_rol', methods=['POST'])
def modificar_rol():
    id = request.form['id']
    rol = controlador_roles.obtener_rol_por_id(id)
    return render_template('dashboard/modificar_rol.html', rol=rol)

@app.route('/actualizar_rol', methods=['POST'])
def actualizar_rol():
    id = request.form['id']
    nombre_rol = request.form['nombre_rol']
    descripcion = request.form['descripcion']
    
    controlador_roles.actualizar_rol(id, nombre_rol, descripcion)
    return redirect(url_for('rol'))

@app.route('/asignar_rol', methods=['POST'])
def asignar_rol():
    id_usuario = request.form['id_usuario']
    id_rol = request.form['id_rol']
    controlador_roles.asignar_rol_usuario(id_usuario, id_rol)
    return redirect(url_for('rol'))

@app.route('/remover_rol', methods=['POST'])
def remover_rol():
    id_usuario = request.form['id_usuario']
    id_rol = request.form['id_rol']
    controlador_roles.remover_rol_usuario(id_usuario, id_rol)
    return redirect(url_for('rol'))

@app.route('/usuarios_por_rol/<int:id_rol>')
def usuarios_por_rol(id_rol):
    usuarios = controlador_roles.obtener_usuarios_por_rol(id_rol)
    rol = controlador_roles.obtener_rol_por_id(id_rol)
    return render_template('dashboard/usuarios_por_rol.html', usuarios=usuarios, rol=rol)
#-----FIN-ROL-----#

###############################
# RUTAS API ADICIONALES
###############################

@app.route('/api/cuestionarios_por_docente/<int:id_docente>')
def api_cuestionarios_por_docente(id_docente):
    try:
        cuestionarios = controlador_cuestionarios.obtener_cuestionarios_por_docente(id_docente)
        return jsonify({'success': True, 'cuestionarios': cuestionarios})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/preguntas_por_cuestionario/<int:id_cuestionario>')
def api_preguntas_por_cuestionario(id_cuestionario):
    try:
        preguntas = controlador_preguntas.obtener_preguntas_por_cuestionario(id_cuestionario)
        return jsonify({'success': True, 'preguntas': preguntas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/opciones_por_pregunta/<int:id_pregunta>')
def api_opciones_por_pregunta(id_pregunta):
    try:
        opciones = controlador_opciones.obtener_opciones_por_pregunta(id_pregunta)
        return jsonify({'success': True, 'opciones': opciones})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/estadisticas_sistema')
def api_estadisticas_sistema():
    try:
        stats = {
            'total_usuarios': len(controlador_usuario.obtener_usuarios()),
            'total_cuestionarios': len(controlador_cuestionarios.obtener_cuestionarios()),
            'total_preguntas': len(controlador_preguntas.obtener_preguntas()),
            'total_salas': len(controlador_salas.obtener_salas()),
            'total_participaciones': len(controlador_participaciones.obtener_participaciones())
        }
        return jsonify({'success': True, 'estadisticas': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/validar_email/<email>')
def api_validar_email(email):
    try:
        usuario = controlador_usuario.obtener_usuario_por_email(email)
        existe = usuario is not None
        return jsonify({'success': True, 'existe': existe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/buscar_usuarios/<termino>')
def api_buscar_usuarios(termino):
    try:
        usuarios = controlador_usuario.buscar_usuarios(termino)
        return jsonify({'success': True, 'usuarios': usuarios})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recompensas_disponibles/<int:id_estudiante>')
def api_recompensas_disponibles(id_estudiante):
    try:
        recompensas = controlador_recompensas.verificar_recompensas_disponibles(id_estudiante)
        return jsonify({'success': True, 'recompensas': recompensas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/otorgar_recompensas_automaticas/<int:id_estudiante>', methods=['POST'])
def api_otorgar_recompensas_automaticas(id_estudiante):
    try:
        recompensas_otorgadas = controlador_recompensas.otorgar_recompensas_automaticas(id_estudiante)
        return jsonify({'success': True, 'recompensas_otorgadas': recompensas_otorgadas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# APIs para manejo de salas en tiempo real
@app.route('/api/sala/<int:sala_id>/usuarios', methods=['GET'])
def api_obtener_usuarios_sala(sala_id):
    """Obtener usuarios conectados a una sala"""
    try:
        # Verificar que la sala existe
        sala = controlador_salas.obtener_sala_por_id(sala_id)
        if not sala:
            return jsonify({'success': False, 'error': 'Sala no encontrada'}), 404
        
        # Obtener usuarios de la sala (simulado por ahora)
        # En una implementación real, esto vendría de WebSockets o base de datos
        usuarios = controlador_salas.obtener_participantes_sala(sala_id)
        
        usuarios_formateados = []
        if usuarios:
            for usuario in usuarios:
                usuarios_formateados.append({
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'estado': 'conectado',
                    'puntuacion': usuario[3] if len(usuario) > 3 else 0
                })
        
        return jsonify({
            'success': True,
            'usuarios': usuarios_formateados
        })
        
    except Exception as e:
        print(f"DEBUG: Error en api_obtener_usuarios_sala: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sala/<int:sala_id>/iniciar', methods=['POST'])
def api_iniciar_juego_sala(sala_id):
    """Iniciar el juego en una sala"""
    try:
        # Verificar que la sala existe
        sala = controlador_salas.obtener_sala_por_id(sala_id)
        if not sala:
            return jsonify({'success': False, 'error': 'Sala no encontrada'}), 404
        
        # Verificar que hay usuarios conectados
        usuarios = controlador_salas.obtener_participantes_sala(sala_id)
        if not usuarios or len(usuarios) == 0:
            return jsonify({'success': False, 'error': 'No hay estudiantes conectados'}), 400
        
        # Cambiar estado de la sala a 'en_progreso'
        success = controlador_salas.actualizar_estado_sala(sala_id, 'en_progreso')
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Juego iniciado exitosamente'
            })
        else:
            return jsonify({'success': False, 'error': 'Error al iniciar el juego'}), 500
            
    except Exception as e:
        print(f"DEBUG: Error en api_iniciar_juego_sala: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sala/<int:sala_id>/cerrar', methods=['POST'])
def api_cerrar_sala(sala_id):
    """Cerrar una sala"""
    try:
        # Verificar que la sala existe
        sala = controlador_salas.obtener_sala_por_id(sala_id)
        if not sala:
            return jsonify({'success': False, 'error': 'Sala no encontrada'}), 404
        
        # Cambiar estado de la sala a 'finalizada'
        success = controlador_salas.actualizar_estado_sala(sala_id, 'finalizada')
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Sala cerrada exitosamente'
            })
        else:
            return jsonify({'success': False, 'error': 'Error al cerrar la sala'}), 500
            
    except Exception as e:
        print(f"DEBUG: Error en api_cerrar_sala: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Verificar conexión e inicializar usuarios de prueba
    print("Iniciando Brain RUSH...")
    if verificar_conexion():
        print("✅ Conexión a base de datos exitosa")
        inicializar_usuarios_prueba()
    else:
        print("❌ Error de conexión a la base de datos")
    
    print("🚀 Iniciando servidor Flask en http://127.0.0.1:8081")
    app.run(debug=True, port=8081)
