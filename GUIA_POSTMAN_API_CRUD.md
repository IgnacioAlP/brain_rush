# 📚 Guía: Colección Postman - Brain Rush API CRUD

## 📋 Descripción General

Esta colección Postman contiene todas las APIs CRUD para las tablas principales de Brain Rush con seguridad JWT.

**Total de Endpoints:** 30 (5 por cada tabla)
**Autenticación:** JWT Bearer Token
**Base URL:** `http://localhost:5000` (configurable en variables)

---

## 🔐 Autenticación (JWT)

### Paso 1: Obtener el Token

Antes de usar cualquier endpoint, debes obtener un token JWT haciendo login.

**Endpoint:** `POST /jwt_login`

**Body:**
```json
{
  "email": "admin@brainrush.com",
  "password": "admin123"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id_usuario": 1,
    "email": "admin@brainrush.com",
    "nombre": "Admin",
    "tipo_usuario": "administrador"
  }
}
```

### Paso 2: Guardar el Token en Variables

1. Copia el valor de `access_token` de la respuesta
2. Ve a **Variables** de la colección
3. Pega el token en la variable `jwt_token`:
   ```
   jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   ```
4. ¡Listo! Ahora puedes usar todos los endpoints

### Paso 3: Usar el Token en las Peticiones

Todos los endpoints usarán automáticamente el token desde la variable `{{jwt_token}}` en el header:
```
Authorization: Bearer {{jwt_token}}
```

---

## 📊 Endpoints Disponibles

### 1. **👥 USUARIOS** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/usuarios` | Crear usuario |
| GET | `/api/usuarios` | Obtener todos los usuarios |
| GET | `/api/usuarios/{id}` | Obtener usuario por ID |
| PUT | `/api/usuarios/{id}` | Actualizar usuario |
| DELETE | `/api/usuarios/{id}` | Eliminar usuario |

**Ejemplo - Crear Usuario:**
```bash
POST http://localhost:5000/api/usuarios
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "nombre": "Juan",
  "apellidos": "Pérez García",
  "email": "juan.perez@example.com",
  "contraseña_hash": "$2b$12$hashedpassword...",
  "tipo_usuario": "estudiante",
  "estado": "activo"
}
```

---

### 2. **❓ CUESTIONARIOS** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/cuestionarios` | Crear cuestionario |
| GET | `/api/cuestionarios` | Obtener todos los cuestionarios |
| GET | `/api/cuestionarios/{id}` | Obtener cuestionario por ID |
| PUT | `/api/cuestionarios/{id}` | Actualizar cuestionario |
| DELETE | `/api/cuestionarios/{id}` | Eliminar cuestionario |

**Ejemplo - Crear Cuestionario:**
```bash
POST http://localhost:5000/api/cuestionarios
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "titulo": "Matemáticas Básicas",
  "descripcion": "Cuestionario sobre operaciones matemáticas",
  "estado": "borrador"
}
```

---

### 3. **🎯 PREGUNTAS** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/preguntas` | Crear pregunta |
| GET | `/api/preguntas` | Obtener todas las preguntas |
| GET | `/api/preguntas/{id}` | Obtener pregunta por ID |
| PUT | `/api/preguntas/{id}` | Actualizar pregunta |
| DELETE | `/api/preguntas/{id}` | Eliminar pregunta |

**Ejemplo - Crear Pregunta:**
```bash
POST http://localhost:5000/api/preguntas
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "enunciado": "¿Cuál es la raíz cuadrada de 16?",
  "tipo": "opcion_multiple",
  "puntaje_base": 10,
  "tiempo_sugerido": 30
}
```

---

### 4. **🔘 OPCIONES DE RESPUESTA** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/opciones-respuesta` | Crear opción |
| GET | `/api/opciones-respuesta` | Obtener todas las opciones |
| GET | `/api/opciones-respuesta/{id}` | Obtener opción por ID |
| PUT | `/api/opciones-respuesta/{id}` | Actualizar opción |
| DELETE | `/api/opciones-respuesta/{id}` | Eliminar opción |

**Ejemplo - Crear Opción:**
```bash
POST http://localhost:5000/api/opciones-respuesta
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "id_pregunta": 1,
  "texto_opcion": "4",
  "es_correcta": 1
}
```

---

### 5. **🎮 SALAS DE JUEGO** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/salas-juego` | Crear sala |
| GET | `/api/salas-juego` | Obtener todas las salas |
| GET | `/api/salas-juego/{id}` | Obtener sala por ID |
| PUT | `/api/salas-juego/{id}` | Actualizar sala |
| DELETE | `/api/salas-juego/{id}` | Eliminar sala |

**Ejemplo - Crear Sala:**
```bash
POST http://localhost:5000/api/salas-juego
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "pin_sala": "123456",
  "id_cuestionario": 1,
  "modo_juego": "individual",
  "estado": "esperando",
  "tiempo_por_pregunta": 30
}
```

---

### 6. **🏆 INSIGNIAS** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/insignias-catalogo` | Crear insignia |
| GET | `/api/insignias-catalogo` | Obtener todas las insignias |
| GET | `/api/insignias-catalogo/{id}` | Obtener insignia por ID |
| PUT | `/api/insignias-catalogo/{id}` | Actualizar insignia |
| DELETE | `/api/insignias-catalogo/{id}` | Eliminar insignia |

**Ejemplo - Crear Insignia:**
```bash
POST http://localhost:5000/api/insignias-catalogo
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "nombre": "Maestro",
  "descripcion": "Alcanza el nivel 50",
  "icono": "👑",
  "tipo": "diamante",
  "requisito_tipo": "nivel",
  "requisito_valor": 50,
  "xp_bonus": 500,
  "rareza": "legendario"
}
```

---

### 7. **🎁 RECOMPENSAS** (5 endpoints)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/recompensas` | Crear recompensa |
| GET | `/api/recompensas` | Obtener todas las recompensas |
| GET | `/api/recompensas/{id}` | Obtener recompensa por ID |
| PUT | `/api/recompensas/{id}` | Actualizar recompensa |
| DELETE | `/api/recompensas/{id}` | Eliminar recompensa |

**Ejemplo - Crear Recompensa:**
```bash
POST http://localhost:5000/api/recompensas
Authorization: Bearer {{jwt_token}}
Content-Type: application/json

{
  "nombre": "Trofeo Oro",
  "descripcion": "Recompensa de oro para campeones",
  "puntos_requeridos": 1000,
  "tipo": "trofeo"
}
```

---

## 🎯 Paso a Paso: Usar la Colección Postman

### 1. **Importar la Colección**
   - Abre Postman
   - Click en **Import**
   - Selecciona `Brain_Rush_API_Collection.postman_collection.json`
   - Click en **Import**

### 2. **Configurar Variables (Opcional)**
   - Si quieres cambiar la base URL:
     - Ve a **Variables** → **base_url**
     - Cambia el valor (ejemplo: `http://localhost:8000`)

### 3. **Hacer Login**
   - En la sección **📋 Autenticación**, ejecuta **Login - Obtener JWT Token**
   - Copia el `access_token` de la respuesta
   - Ve a **Variables** → **jwt_token** → pega el token

### 4. **Usar cualquier Endpoint**
   - Selecciona el endpoint que desees (ejemplo: **Crear Usuario**)
   - Modifica el **Body** con tus datos
   - Click en **Send**
   - ¡Listo!

---

## 📝 Estructura de Respuestas

Todas las respuestas siguen este formato:

**Respuesta Exitosa (200, 201):**
```json
{
  "success": true,
  "mensaje": "Operación exitosa",
  "data": {
    "id_usuario": 5,
    "nombre": "Juan",
    "email": "juan@example.com"
  }
}
```

**Respuesta de Error (400, 404, 500):**
```json
{
  "success": false,
  "error": "Descripción del error"
}
```

---

## 🔒 Seguridad JWT

- **Tipo de autenticación:** Bearer Token
- **Header requerido:** `Authorization: Bearer <token>`
- **Duración del token:** 24 horas (configurable en `crear_token_jwt`)
- **Algoritmo:** HS256
- **Renovación:** Hacer login nuevamente

---

## ⚠️ Notas Importantes

1. **Token expirado:** Si recibes error `401 Unauthorized`, vuelve a hacer login
2. **Cambiar base URL:** Modifica la variable `base_url` para apuntar a otro servidor
3. **Métodos HTTP:**
   - **POST:** Crear recursos
   - **GET:** Obtener recursos
   - **PUT:** Actualizar recursos
   - **DELETE:** Eliminar recursos

---

## 📱 Ejemplo Completo: Crear Pregunta con Opciones

```
1. Login: POST /jwt_login
   Obtener token JWT

2. Crear Pregunta: POST /api/preguntas
   Body: {
     "enunciado": "¿Cuánto es 2+2?",
     "tipo": "opcion_multiple",
     "puntaje_base": 5
   }
   Guardar id_pregunta (ejemplo: 1)

3. Crear Opción 1: POST /api/opciones-respuesta
   Body: {
     "id_pregunta": 1,
     "texto_opcion": "3",
     "es_correcta": 0
   }

4. Crear Opción 2: POST /api/opciones-respuesta
   Body: {
     "id_pregunta": 1,
     "texto_opcion": "4",
     "es_correcta": 1
   }

5. Crear Opción 3: POST /api/opciones-respuesta
   Body: {
     "id_pregunta": 1,
     "texto_opcion": "5",
     "es_correcta": 0
   }

6. Verificar: GET /api/preguntas/1
   Respuesta incluirá la pregunta completa
```

---

## 🆘 Solución de Problemas

| Problema | Solución |
|----------|----------|
| `401 Unauthorized` | Token expirado, hacer login nuevamente |
| `404 Not Found` | Recurso no existe, verificar ID |
| `400 Bad Request` | JSON malformado o falta campo requerido |
| `500 Internal Server Error` | Error en servidor, revisar logs |

---

**Autor:** Brain Rush Development Team  
**Versión:** 1.0  
**Última actualización:** 17 de noviembre de 2025

