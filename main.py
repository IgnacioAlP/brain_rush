from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response 

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
        # Procesar datos del formulario de registro aquí
        pass
    return render_template('Registrarse.html')

@app.route('/unirse_a_sala', methods=['GET', 'POST'])
def unirse_a_sala():
    if request.method == 'POST':
        # Procesar datos del formulario de unirse a sala aquí
        pass
    return render_template('UnirseASala.html')

if __name__ == '__main__':
    app.run(debug=True, port=8081)