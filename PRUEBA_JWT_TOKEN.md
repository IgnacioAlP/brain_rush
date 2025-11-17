# Prueba de Cambio: Bearer → JWT

## ✅ Cambios Realizados

### 1. Configuración del Servidor (main.py)
Se agregó la configuración para usar "JWT" en lugar de "Bearer":
```python
app.config['JWT_HEADER_TYPE'] = 'JWT'
```

### 2. Colecciones de Postman
Todas las colecciones han sido actualizadas automáticamente:
- `Brain_Rush_API_Collection.postman_collection.json`
- `Brain_Rush_API_Complete_Part1.postman_collection.json`
- `Brain_Rush_API_Complete_Part2.postman_collection.json`
- `Brain_Rush_API_Complete_Part3.postman_collection.json`
- `Brain_Rush_API_Complete_Part4.postman_collection.json`

**Antes:**
```
Authorization: Bearer {{jwt_token}}
```

**Ahora:**
```
Authorization: JWT {{jwt_token}}
```

## 📋 Pasos para Probar

### Opción 1: Probar Localmente

1. **Reinicia el servidor Flask:**
   ```bash
   python main.py
   ```

2. **En Postman:**
   - Importa cualquiera de las colecciones actualizadas
   - Ejecuta el endpoint `POST /api/auth` para obtener el token
   - El token se guardará automáticamente en `{{jwt_token}}`
   - Prueba cualquier otro endpoint (ejemplo: `GET /api/usuarios`)
   - Verifica en el header que se envía: `Authorization: JWT <token>`

### Opción 2: Probar en PythonAnywhere

1. **Sube el archivo actualizado:**
   - `main.py` → `/home/ProyectoWeb20252/mysite/main.py`

2. **Recarga la aplicación web:**
   - Ve a la pestaña "Web"
   - Click en "Reload"

3. **Prueba en Postman:**
   - Cambia la base URL a: `https://proyectoweb20252.pythonanywhere.com/`
   - Ejecuta `POST /api/auth`
   - Prueba otros endpoints

## 🔍 Verificación

### Headers que se envían ahora:
```http
GET /api/usuarios HTTP/1.1
Host: proyectoweb20252.pythonanywhere.com
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

### Antes (Bearer):
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Ahora (JWT):
```http
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## ⚠️ Importante

- **TODOS los clientes** que usen tu API deben actualizar el header de `Bearer` a `JWT`
- Las colecciones de Postman ya están actualizadas automáticamente
- Si tienes código de frontend, actualiza el header también

## 🧪 Prueba Rápida

```bash
# 1. Obtener token (local)
curl -X POST http://127.0.0.1:5000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"email":"tu@email.com","password":"tupassword"}'

# 2. Usar el token con JWT (NO Bearer)
curl -X GET http://127.0.0.1:5000/api/usuarios \
  -H "Authorization: JWT <tu_token_aqui>"
```

## ✅ Estado

- [x] Configuración del servidor actualizada
- [x] Colecciones de Postman actualizadas
- [ ] Probado localmente
- [ ] Subido a PythonAnywhere
- [ ] Probado en producción
