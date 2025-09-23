from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response 
from werkzeug.exceptions import InternalServerError

from controladores.controlador_usuario import crear_usuario, autenticar

app = Flask(__name__)
app.secret_key = 'clave-temporal'  # Solo para que funcionen los flash messages

#---RUTAS FIJAS---#

@app.route('/')
def maestra():
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

            user_id = crear_usuario(nombre, apellidos, email, password, tipo_usuario)
            respuesta = { 'success': True, 'user_id': user_id }
            if request.is_json:
                return jsonify(respuesta)
            flash('¡Registro completado exitosamente!', 'success')
            return redirect(url_for('maestra'))
        except Exception as e:
            # En caso de error de BD (p. ej., email duplicado)
            if request.is_json:
                return jsonify({ 'success': False, 'error': 'No se pudo registrar el usuario.', 'detail': str(e) }), 400
            flash('No se pudo registrar el usuario.', 'error')
            return redirect(url_for('error_sistema_page'))
    return render_template('Registrarse.html')

@app.route('/unirse_a_sala', methods=['GET', 'POST'])
def unirse_a_sala():
    if request.method == 'POST':
        # Procesar datos del formulario de unirse a sala aquí
        pass
    return render_template('UnirseASala.html')

# Ruta de error de sistema divertida
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        ok, usuario = autenticar(email, password)
        if not ok:
            # Según el requerimiento, ante cualquier error, enviar a /errorsistema
            if request.is_json:
                return jsonify({ 'success': False, 'error': 'Credenciales inválidas' }), 400
            return redirect(url_for('error_sistema_page'))

        # Si autenticó, vamos a la página principal
        if request.is_json:
            return jsonify({ 'success': True, 'usuario': { 'id_usuario': usuario['id_usuario'], 'email': usuario['email'] } })
        return redirect(url_for('maestra'))
    except Exception as e:
        if request.is_json:
            return jsonify({ 'success': False, 'error': 'Error en login', 'detail': str(e) }), 500
        return redirect(url_for('error_sistema_page'))

@app.route('/errorsistema')
def error_sistema_page():
    # Renderiza un template divertido de error interno
    return render_template('ErrorSistema.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=8081)