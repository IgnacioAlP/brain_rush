# Migración a Flask-JWT-Extended - Completada ✅

## Resumen
Se ha completado exitosamente la migración de **Flask-JWT** (incompatible con Python 3.11+) a **Flask-JWT-Extended** (compatible y mantenido activamente).

---

## Cambios Realizados

### 1. Dependencias
- ❌ **Removido**: `Flask-JWT==0.3.2` (incompatible)
- ✅ **Agregado**: `Flask-JWT-Extended==4.7.1` (compatible)

### 2. Imports Actualizados (`main.py`)
```python
# Antes (Flask-JWT)
from flask_jwt import JWT, jwt_required, current_identity

# Ahora (Flask-JWT-Extended)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
```

### 3. Configuración JWT
```python
# Configuración JWT-Extended
app.config['JWT_SECRET_KEY'] = 'super-secret-jwt-key'  # En producción usar variable de entorno
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Token válido por 24 horas

jwt = JWTManager(app)
```

### 4. Eliminadas Funciones Legacy
- `class User(object)` - Ya no necesaria
- `def authenticate(username, password)` - Reemplazada por endpoint `/api/auth`
- `def identity(payload)` - Reemplazada por `get_jwt_identity()`

### 5. Nuevo Endpoint de Autenticación

**Endpoint**: `POST /api/auth`

**Request**:
```json
{
  "email": "usuario@example.com",
  "password": "contraseña"
}
```

**Response (exitosa)**:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id_usuario": 1,
    "email": "usuario@example.com",
    "nombre": "Juan",
    "apellidos": "Pérez",
    "tipo_usuario": "docente"
  }
}
```

**Response (error)**:
```json
{
  "success": false,
  "error": "Email o contraseña incorrectos"
}
```

### 6. Decorador Actualizado: `jwt_or_session_required`

Ahora verifica correctamente:
1. **Sesión web**: `session['usuario_id']` y `session['logged_in']`
2. **JWT Token**: Header `Authorization: Bearer <token>`

```python
@app.route('/api/protected-route')
@jwt_or_session_required
def protected_route():
    # Acceso permitido con sesión o JWT
    return jsonify({'message': 'Acceso permitido'})
```

---

## Cómo Usar el Nuevo Sistema

### Opción 1: Autenticación Web (Sesión)
```
1. Usuario navega a /login
2. Ingresa email y password
3. Si es correcto, se crea sesión
4. Puede acceder a rutas protegidas con @jwt_or_session_required
```

### Opción 2: Autenticación API (JWT)

#### Paso 1: Obtener Token
```bash
curl -X POST http://localhost:5000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@example.com", "password": "pass123"}'
```

**Respuesta**:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Paso 2: Usar Token en Requests
```bash
curl -X POST http://localhost:5000/api/comprar-insignia \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{"id_insignia": 3}'
```

---

## APIs Protegidas con JWT

Las siguientes rutas ahora requieren autenticación (sesión o JWT):

1. `/api/comprar-insignia` - Comprar insignias con XP
2. `/exportar-resultados` - Exportar resultados a Excel/OneDrive
3. `/api/iniciar-sala` - Iniciar sala de juego
4. `/api/cerrar-sala` - Cerrar sala de juego
5. `/publicar-cuestionario` - Publicar cuestionario
6. `/despublicar-cuestionario` - Despublicar cuestionario
7. `/eliminar-pregunta` - Eliminar pregunta
8. `/importar-preguntas` - Importar preguntas desde Excel
9. `/api/verificar-respuesta` - Verificar respuesta en sala
10. `/api/obtener-estadisticas-sala` - Obtener estadísticas de sala

---

## Testing del Sistema

### Test 1: Verificar Autenticación JWT
```python
import requests

# 1. Login para obtener token
response = requests.post('http://localhost:5000/api/auth', json={
    'email': 'docente@test.com',
    'password': 'password123'
})
data = response.json()
token = data['access_token']

# 2. Usar token en request protegido
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/mi-xp', headers=headers)
print(response.json())
```

### Test 2: Verificar Decorador Híbrido
```bash
# Sin autenticación (debe fallar)
curl http://localhost:5000/api/comprar-insignia
# Respuesta: {"error": "Autenticación requerida (sesión o JWT)"}

# Con JWT (debe funcionar)
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/comprar-insignia

# Con sesión web (debe funcionar desde navegador logueado)
```

---

## Compatibilidad

### Python
- ✅ **Compatible**: Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- ❌ **No compatible**: Python 2.7, 3.6

### PythonAnywhere
Flask-JWT-Extended es totalmente compatible con PythonAnywhere. Solo necesitas:

1. Actualizar `requirements.txt`:
```bash
pip install -r requirements.txt
```

2. Configurar variable de entorno `JWT_SECRET_KEY` (recomendado para producción):
```python
# En config.py
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-jwt-key')
```

---

## Seguridad en Producción

### 🔒 Recomendaciones Importantes

1. **Cambiar JWT_SECRET_KEY**:
```python
# No usar 'super-secret-jwt-key' en producción
# Generar clave segura:
import secrets
print(secrets.token_hex(32))
# Usar resultado en variable de entorno
```

2. **Configurar HTTPS**:
```python
# Solo permitir JWT sobre HTTPS en producción
app.config['JWT_COOKIE_SECURE'] = True  # Si usas cookies
```

3. **Token Expiration**:
```python
# Ajustar según necesidades de seguridad
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Más corto = más seguro
```

4. **Refresh Tokens** (opcional):
```python
from flask_jwt_extended import create_refresh_token

# En /api/auth
refresh_token = create_refresh_token(identity=usuario['id_usuario'])
return jsonify({
    'access_token': access_token,
    'refresh_token': refresh_token  # Para renovar sin re-login
})
```

---

## Solución de Problemas

### Error: "Token inválido"
- Verificar que el header sea: `Authorization: Bearer <token>`
- Verificar que el token no esté expirado (24 horas)
- Verificar que `JWT_SECRET_KEY` sea la misma en cliente/servidor

### Error: "Autenticación requerida"
- Verificar que el endpoint tenga `@jwt_or_session_required`
- Verificar que la sesión esté activa o se envíe el token JWT

### Error al importar
```python
# Si falta algún import
from flask_jwt_extended import verify_jwt_in_request
```

---

## Rollback (Si es Necesario)

Si necesitas revertir los cambios:

1. Desinstalar Flask-JWT-Extended:
```bash
pip uninstall Flask-JWT-Extended -y
```

2. Instalar Flask-JWT (solo funciona en Python ≤ 3.9):
```bash
pip install Flask-JWT==0.3.2
```

3. Revertir cambios en `main.py` (usar git):
```bash
git checkout HEAD~1 main.py
```

**Nota**: No se recomienda revertir ya que Flask-JWT está deprecado.

---

## Referencias

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [JWT.io - Debugger](https://jwt.io/)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

## Fecha de Migración
**11 de enero de 2025**

## Estado
✅ **COMPLETADO** - Sistema funcionando correctamente con Python 3.11.9
