# 🚀 Guía Rápida: Enviar Correos Reales con Gmail

## ✅ Pasos Completados Automáticamente:

1. ✅ config.py actualizado para usar Gmail
2. ✅ python-dotenv instalado
3. ✅ main.py modificado para cargar .env
4. ✅ Archivo .env creado

## 📝 Lo que DEBES hacer TÚ:

### Paso 1: Configurar Gmail

1. **Activar verificación en 2 pasos:**
   - Ve a: https://myaccount.google.com/security
   - Busca "Verificación en 2 pasos"
   - Actívala (sigue los pasos de Google)

2. **Generar Contraseña de Aplicación:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Si no ves esta opción, primero activa la verificación en 2 pasos
   - Selecciona app: "Correo"
   - Selecciona dispositivo: "Otro (nombre personalizado)"
   - Escribe: "Brain RUSH"
   - Clic en "Generar"
   - **IMPORTANTE:** Copia la contraseña de 16 caracteres (con espacios)

### Paso 2: Editar el archivo .env

Abre el archivo `.env` en la raíz del proyecto y reemplaza:

```env
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
```

Con tus datos reales:

```env
MAIL_USERNAME=TU_CORREO_REAL@gmail.com
MAIL_PASSWORD=la contraseña de 16 caracteres que copiaste
```

**IMPORTANTE:** 
- Usa tu correo de Gmail completo
- Usa la contraseña de aplicación (NO tu contraseña normal de Gmail)
- Guarda el archivo

### Paso 3: Reiniciar Flask

1. **Detén el servidor Flask** (Ctrl+C en la terminal donde está corriendo)
2. **Ya NO necesitas el servidor SMTP local** - Ciérralo si está abierto
3. **Inicia Flask nuevamente:**
   ```bash
   python main.py
   ```

### Paso 4: Probar

1. Ve a http://127.0.0.1:8081
2. Regístrate con un **correo REAL** (Gmail, Outlook, etc.)
3. El correo llegará a la bandeja de entrada real (revisa spam si no lo ves)
4. Haz clic en el enlace de confirmación del correo
5. Inicia sesión

## 🎯 Diferencias Importantes:

### Antes (Servidor Local):
- ✅ Correos aparecían en la consola
- ✅ Instantáneo
- ❌ No llegaban a correos reales

### Ahora (Gmail):
- ✅ Correos llegan a direcciones REALES
- ✅ Funciona con cualquier email (Gmail, Outlook, Yahoo, etc.)
- ⏱️ Tarda 5-30 segundos en llegar
- ⚠️ Puede caer en spam la primera vez

## 🔒 Seguridad:

**El archivo .env está en .gitignore**, por lo que NO se subirá a GitHub.
Tus credenciales están seguras.

## ⚠️ Límites de Gmail:

- **500 correos por día** (más que suficiente para desarrollo)
- Si necesitas más, considera servicios como SendGrid o Mailgun

## 🐛 Solución de Problemas:

### Error: "Username and Password not accepted"
- Verifica que usaste la contraseña de aplicación (16 caracteres)
- Verifica que el correo sea correcto
- Asegúrate de tener la verificación en 2 pasos activada

### El correo no llega:
- Espera 1-2 minutos
- Revisa la carpeta de SPAM
- Verifica los logs de Flask (debe decir "✅ Correo enviado")

### Error: "SMTPAuthenticationError"
- La contraseña de aplicación está mal
- Genera una nueva contraseña de aplicación

## 📖 Archivos Modificados:

- ✅ `config.py` - Configuración de Gmail
- ✅ `main.py` - Carga de variables de entorno
- ✅ `.env` - Credenciales (EDÍTALO con tus datos)

## 🔄 Para volver al servidor local:

Si quieres volver a usar el servidor SMTP local de debugging, cambia en `config.py`:

```python
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
```
