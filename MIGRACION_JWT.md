# Guía de Migración de Flask-JWT a Flask-JWT-Extended

## Problema Actual
Flask-JWT tiene un error de compatibilidad con Python 3.11+:
```
ImportError: cannot import name 'Mapping' from 'collections'
```

## Solución Recomendada: Flask-JWT-Extended

### 1. Instalar Flask-JWT-Extended
```bash
pip install Flask-JWT-Extended
```

### 2. Actualizar requirements.txt
Agregar:
```
Flask-JWT-Extended==4.5.3
```

### 3. Cambios en main.py

#### Antes (Flask-JWT):
```python
from flask_jwt import JWT, jwt_required, current_identity

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and user.password.encode('utf-8') == password.encode('utf-8'):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)
```

#### Después (Flask-JWT-Extended):
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Configuración JWT
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Endpoint de login
@app.route('/api/auth', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Verificar credenciales en BD
    usuario = controlador_usuario.obtener_usuario_por_email(username)
    
    if not usuario:
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
    
    if not controlador_usuario.verificar_contrasena(usuario['contraseña_hash'], password):
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
    
    # Crear token
    access_token = create_access_token(identity=usuario['id_usuario'])
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": usuario['id_usuario'],
            "nombre": usuario['nombre'],
            "email": usuario['email'],
            "tipo": usuario['tipo_usuario']
        }
    })

# Proteger rutas con @jwt_required()
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200
```

### 4. Uso en el Frontend

```javascript
// Login y guardar token
async function login(username, password) {
    const response = await fetch('/api/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
        // Guardar token
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
    }
}

// Hacer peticiones autenticadas
async function fetchProtectedData() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('/api/protected', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}
```

## Ventajas de Flask-JWT-Extended

1. ✅ Compatible con Python 3.11+
2. ✅ Más funcionalidades (refresh tokens, blacklist, custom claims)
3. ✅ Mejor documentación
4. ✅ Activamente mantenido
5. ✅ Protección CSRF nativa con JWT

## Estado Actual

- ✅ CSRF completamente deshabilitado
- ⚠️ Flask-JWT configurado pero no funcional (error de compatibilidad)
- 🔄 Listo para migrar a Flask-JWT-Extended

## Próximos Pasos

1. Desinstalar Flask-JWT:
   ```bash
   pip uninstall Flask-JWT
   ```

2. Instalar Flask-JWT-Extended:
   ```bash
   pip install Flask-JWT-Extended
   ```

3. Implementar los cambios en main.py según este documento

4. Actualizar el frontend para usar tokens JWT
