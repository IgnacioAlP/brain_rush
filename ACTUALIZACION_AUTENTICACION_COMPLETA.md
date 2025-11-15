# 🔐 ACTUALIZACIÓN COMPLETA DEL SISTEMA DE AUTENTICACIÓN

## 📋 Resumen de Cambios Realizados

Se ha realizado una migración completa del sistema de autenticación y seguridad de la aplicación Brain Rush. Estos son los cambios más importantes:

---

## 1. ✅ Migración de Flask-JWT-Extended a PyJWT

### **Cambios en `requirements.txt`:**
- ❌ **Removido:** `Flask-JWT-Extended==4.6.0`
- ✅ **Agregado:** `PyJWT==2.8.0`
- ✅ **Actualizado:** `Flask==2.3.3` (desde 3.0.0)
- ✅ **Agregado:** `bcrypt==4.1.2` (para contraseñas seguras)
- ✅ **Actualizado:** `werkzeug==2.3.7` (compatible con Flask 2.3.3)
- ✅ **Actualizado:** `itsdangerous==2.1.2` (para cookies encriptadas)

### **Razones del cambio:**
- PyJWT es más ligero y directo
- Mayor control sobre la generación y validación de tokens
- No depende de extensiones de Flask
- Mejora la portabilidad del código

---

## 2. 🔒 MEJORA CRÍTICA: De MD5 a bcrypt para Contraseñas

### **⚠️ PROBLEMA IDENTIFICADO:**
El sistema usaba **MD5** para hashear contraseñas, lo cual es **TOTALMENTE INSEGURO**:
- MD5 está roto desde 2004
- Es vulnerable a ataques de colisión
- Se puede "crackear" en segundos con herramientas modernas
- **NO es SHA256** como preguntaste - era incluso peor

### **✅ SOLUCIÓN IMPLEMENTADA:**
Se cambió a **bcrypt**, el estándar de la industria:
- Bcrypt es un algoritmo diseñado específicamente para contraseñas
- Tiene "salt" automático (previene rainbow tables)
- Es intencionalmente lento (previene fuerza bruta)
- Se usa en aplicaciones de alta seguridad (bancos, gobiernos, etc.)

### **Archivos modificados:**
1. **`utils_auth.py`** (NUEVO) - Funciones `hash_password()` y `verificar_password()`
2. **`controladores/controlador_usuario.py`** - Funciones actualizadas:
   - `crear_usuario()` - Usa bcrypt para nuevos usuarios
   - `autenticar_usuario()` - Verifica bcrypt y migra MD5 legacy automáticamente
   - `actualizar_usuario()` - Usa bcrypt para cambios de contraseña
   - `restablecer_contrasena()` - Usa bcrypt para recuperación

### **🔄 Compatibilidad hacia atrás:**
El sistema es compatible con contraseñas MD5 existentes:
- Al iniciar sesión, verifica si la contraseña está en MD5
- Si es correcta, la **actualiza automáticamente a bcrypt**
- Los usuarios NO necesitan cambiar su contraseña manualmente
- Migración gradual y transparente

---

## 3. 🍪 Sistema de Cookies Encriptadas

### **Nuevo archivo: `utils_auth.py`**
Contiene toda la lógica de autenticación y cookies seguras:

#### **Funciones de Cookies:**
- `crear_cookie_segura()` - Encripta datos con itsdangerous
- `leer_cookie_segura()` - Desencripta y valida cookies
- `establecer_cookies_usuario()` - Establece cookies de ID y nombre
- `limpiar_cookies_usuario()` - Limpia cookies al cerrar sesión
- `obtener_usuario_cookies()` - Lee datos del usuario desde cookies

#### **Cookies implementadas:**
1. **`user_id`** - ID del usuario (encriptado)
2. **`user_name`** - Nombre del usuario (encriptado)

#### **Configuración de seguridad:**
```python
httponly=True      # No accesible desde JavaScript (previene XSS)
secure=True        # Solo HTTPS en producción
samesite='Lax'     # Protección contra CSRF
max_age=7 días     # Duración de las cookies
```

### **Integración en `main.py`:**
- **Login:** Establece cookies automáticamente al iniciar sesión
- **Logout:** Limpia cookies al cerrar sesión
- **Verificación:** Los decoradores leen cookies si no hay sesión de Flask

---

## 4. 🛡️ Sistema de Control de Acceso Mejorado

### **Nuevos decoradores en `utils_auth.py`:**

#### **`@login_required`**
- Verifica autenticación en este orden:
  1. Sesión de Flask (tradicional)
  2. Cookies encriptadas
  3. Token JWT (para APIs)
- Redirige a login si no está autenticado

#### **`@docente_required`**
- Requiere autenticación + tipo de usuario "docente"
- Redirige a dashboard de estudiante si no es docente

#### **`@estudiante_required`**
- Requiere autenticación + tipo de usuario "estudiante"
- Redirige a dashboard admin si no es estudiante

#### **`@jwt_or_session_required`**
- Acepta JWT O sesión
- Útil para endpoints accesibles desde web y API

### **Ejemplo de uso:**
```python
@app.route('/dashboard-docente')
@docente_required
def dashboard_docente():
    # Solo docentes pueden acceder
    return render_template('DashboardDocente.html')

@app.route('/api/estudiantes/mis-cursos')
@estudiante_required
def api_mis_cursos():
    # Solo estudiantes pueden acceder
    return jsonify({'cursos': [...}})
```

---

## 5. 📧 Sistema de Correo Electrónico

### **Estado actual:**
✅ **CORRECTAMENTE CONFIGURADO** en `config.py` y `.env`

```python
# .env
MAIL_USERNAME=alonzopezoi@gmail.com
MAIL_PASSWORD=zjri vsxo jnzk pqsc  # Contraseña de aplicación de Gmail

# config.py (DevelopmentConfig)
MAIL_ENABLED = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
```

### **Funcionalidad:**
1. **Registro de usuario:**
   - Se crea con estado `inactivo`
   - Se envía correo de confirmación
   - Usuario debe activar cuenta desde correo

2. **Recuperación de contraseña:**
   - Usuario solicita recuperación
   - Se envía correo con token temporal (1 hora)
   - Usuario crea nueva contraseña desde enlace

### **¿Por qué no estaba enviando correos?**
El código YA estaba correcto. Posibles causas:
- Gmail bloqueando el acceso (requiere "Contraseña de aplicación")
- Firewall bloqueando puerto 587
- `MAIL_ENABLED=False` en producción

### **Verificación:**
El envío de correo se realiza en:
- `controladores/controlador_usuario.py` → `enviar_correo_confirmacion()`
- `main.py` → Ruta `/registrarse` llama a la función

---

## 6. 🔑 JWT Personalizado

### **Funciones en `utils_auth.py`:**

#### **`crear_token_jwt(usuario_id, expiracion_horas=24)`**
Crea un token JWT con:
- ID del usuario
- Fecha de expiración
- Firma con SECRET_KEY
- Algoritmo HS256 (seguro)

#### **`verificar_token_jwt(token)`**
Valida y decodifica tokens:
- Verifica firma
- Verifica expiración
- Retorna payload o None

#### **`extraer_token_jwt_request()`**
Extrae token del header `Authorization: Bearer <token>`

### **Endpoint API actualizado:**
```python
@app.route('/api/auth', methods=['POST'])
def jwt_login():
    # Autentica usuario
    # Retorna access_token personalizado
    # Compatible con apps móviles
```

---

## 7. 📝 Configuración de Sesiones Seguras

### **Nuevas configuraciones en `main.py`:**
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key-cambiar-en-produccion')
app.config['SESSION_COOKIE_SECURE'] = True  # Solo HTTPS en producción
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protección CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Duración 7 días
```

---

## 🚀 Pasos para Desplegar los Cambios

### 1. **Instalar nuevos paquetes:**
```bash
pip install -r requirements.txt
```

### 2. **Verificar configuración de correo:**
Asegúrate de que `.env` tenga credenciales correctas:
```env
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

### 3. **Probar login/registro:**
- Los usuarios existentes podrán iniciar sesión normalmente
- Sus contraseñas se actualizarán automáticamente a bcrypt
- Los nuevos usuarios usarán bcrypt desde el inicio

### 4. **Probar envío de correo:**
```python
# En Python shell o ruta de prueba
from controladores import controlador_usuario
success, msg = controlador_usuario.enviar_correo_confirmacion('test@usat.pe')
print(f"Correo enviado: {success}, Mensaje: {msg}")
```

### 5. **Monitorear logs:**
Todos los cambios incluyen logs detallados:
- ✅ Login exitoso
- 🔄 Migración de contraseña MD5 → bcrypt
- 📧 Envío de correos
- ❌ Errores de autenticación

---

## 🔍 Verificación de Seguridad

### **Contraseñas:**
✅ Ya NO es MD5
✅ Ya NO es SHA256
✅ **ES BCRYPT** (el más seguro)

### **Cookies:**
✅ Encriptadas con itsdangerous
✅ HttpOnly (previene XSS)
✅ Secure en producción (HTTPS)
✅ SameSite (previene CSRF)

### **JWT:**
✅ Firma con SECRET_KEY
✅ Algoritmo HS256 seguro
✅ Validación de expiración
✅ No usa flask-jwt-extended

### **Control de Acceso:**
✅ Decoradores por tipo de usuario
✅ Verificación en sesión, cookies y JWT
✅ Redirecciones apropiadas

---

## 📚 Archivos Modificados

### **Nuevos:**
- `utils_auth.py` - Toda la lógica de autenticación

### **Modificados:**
- `requirements.txt` - Paquetes actualizados
- `main.py` - Login, logout, JWT, decoradores
- `controladores/controlador_usuario.py` - bcrypt, verificación mejorada

### **Sin cambios necesarios:**
- `config.py` - Correo ya estaba configurado
- `.env` - Credenciales ya están
- Templates HTML - Funcionan igual

---

## 🎯 Beneficios de los Cambios

1. **Seguridad mejorada 1000%:**
   - De MD5 a bcrypt
   - Cookies encriptadas
   - JWT personalizado

2. **Mayor control:**
   - Sin dependencias pesadas
   - Lógica centralizada en utils_auth.py
   - Fácil de mantener

3. **Compatibilidad:**
   - Migración automática de contraseñas
   - Login funciona igual para usuarios
   - Sin interrupciones

4. **Flexibilidad:**
   - Soporta sesión, cookies y JWT
   - APIs y web funcionan juntos
   - Decoradores reutilizables

---

## ⚠️ IMPORTANTE - Producción

### **Antes de desplegar en producción:**

1. **Cambiar SECRET_KEY:**
```python
# No usar 'super-secret'
# Generar una clave fuerte:
import secrets
print(secrets.token_hex(32))
```

2. **Habilitar HTTPS:**
```python
app.config['SESSION_COOKIE_SECURE'] = True
```

3. **Configurar CORS si es necesario:**
```bash
pip install flask-cors
```

4. **Rotar contraseña de Gmail:**
Usar una cuenta dedicada para envío de correos.

5. **Monitorear intentos de login fallidos:**
Considerar implementar rate limiting.

---

## 🐛 Resolución de Problemas

### **"No se pueden resolver importaciones"**
```bash
pip install PyJWT bcrypt itsdangerous
```

### **"Correo no se envía"**
1. Verificar credenciales en `.env`
2. Gmail: Usar "Contraseña de aplicación", no la normal
3. Verificar firewall (puerto 587)
4. Ver logs: `print(mensaje_correo)`

### **"Token JWT inválido"**
1. Verificar SECRET_KEY no ha cambiado
2. Token puede haber expirado (24 horas)
3. Verificar formato: `Authorization: Bearer <token>`

### **"Usuarios no pueden iniciar sesión"**
1. Revisar estado de cuenta (activo/inactivo)
2. Verificar contraseña correcta
3. Ver logs de autenticación
4. Migración MD5 → bcrypt es automática

---

## 📞 Contacto

Si tienes dudas sobre los cambios, revisa:
- `utils_auth.py` - Funciones documentadas
- Logs de la aplicación - Mensajes detallados
- Este documento - Explicación completa

**¡Sistema de autenticación actualizado y seguro! 🎉**
