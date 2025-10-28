# 🚀 INSTALACIÓN RÁPIDA - Exportación por Email (PythonAnywhere)

## ✅ Lo Que Ya Está Listo

Todo el código ya está implementado y funcionando. Solo necesitas asegurarte de tener la configuración SMTP.

## 📋 Checklist de Instalación

### 1. Verificar Dependencias

```bash
pip install --user openpyxl
```

**Nota**: `openpyxl` probablemente ya está instalado.

### 2. Configurar Variables de Entorno

Edita tu archivo `.env` y asegúrate de tener:

```env
# Configuración de Email (Flask-Mail)
MAIL_USERNAME=brainrush.notificaciones@gmail.com
MAIL_PASSWORD=tu-password-de-aplicacion-gmail
```

**Nota**: BrainRush usa **Flask-Mail**, por lo que las variables son `MAIL_USERNAME` y `MAIL_PASSWORD` (no SMTP_*).

**¿Cómo obtener el password de aplicación de Gmail?**

1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos" si no está activada
3. Ve a "Contraseñas de aplicaciones"
4. Genera una contraseña para "Mail" / "Windows Computer"
5. Copia la contraseña de 16 caracteres
6. Pégala en `MAIL_PASSWORD`

### 3. Reload de la Aplicación

**En PythonAnywhere:**
- Ve a la pestaña "Web"
- Haz clic en el botón verde "Reload"

**Localmente:**
```bash
# Detén el servidor (Ctrl+C)
# Reinicia
python main.py
```

### 4. ¡Listo para Usar!

Ahora puedes exportar resultados:

1. Ve a "Mis Cuestionarios"
2. Selecciona una sala finalizada → "Ver Resultados"
3. Click en "📧 Enviar por Correo"
4. Revisa tu correo electrónico (@usat.pe)

## 🎯 Prueba Rápida

```python
# Prueba que el email funciona con Flask-Mail
python -c "
from flask import Flask
from flask_mail import Mail, Message
from config import DevelopmentConfig
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mail = Mail(app)

with app.app_context():
    msg = Message(
        'Test de exportación BrainRush',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=['tu-email@usat.pe']  # Cambia esto
    )
    msg.body = 'Este es un correo de prueba desde BrainRush'
    
    try:
        mail.send(msg)
        print('✅ Email enviado correctamente')
    except Exception as e:
        print(f'❌ Error: {e}')
"
```

## ❓ Solución de Problemas

### Error: "No module named 'openpyxl'"
```bash
pip install --user openpyxl
```

### Error: "Configuración de correo no encontrada"
Verifica que el `.env` tenga `MAIL_USERNAME` y `MAIL_PASSWORD` (no SMTP_*).

### Error: "SMTPAuthenticationError"
La contraseña de aplicación de Gmail es incorrecta. Genera una nueva.

### El email no llega
- Revisa SPAM
- Verifica que el correo del usuario en la BD sea correcto
- En PythonAnywhere, verifica logs: `/var/log/`
- Asegúrate de que `MAIL_ENABLED = True` en `config.py`

## 📊 ¿Qué Recibe el Usuario?

Un email con:
- Asunto: "Resultados de BrainRush - [Nombre del Cuestionario]"
- Archivo adjunto: Excel con resultados formateados
- Instrucciones para guardar en OneDrive/Google Drive

El archivo puede ser guardado donde el usuario quiera.

## 🎉 Ventajas

✅ **Sin configuración de Azure** - No necesitas registrar apps  
✅ **Sin OAuth2** - No necesitas autorización del usuario  
✅ **Compatible con PythonAnywhere** - Sin problemas de redirección  
✅ **Instantáneo** - Funciona inmediatamente  
✅ **Flexible** - El usuario guarda donde quiera  

## 📁 Archivos Modificados

Solo 3 archivos cambiaron:

1. ✅ `main.py` - Endpoint simplificado
2. ✅ `Templates/ResultadosJuego.html` - Botón actualizado
3. ✅ `Templates/MisCuestionarios.html` - Botón actualizado

**No se modificó la base de datos** ✨

---

**¿Necesitas la versión completa con OAuth2 de OneDrive?**  
→ Lee `EXPORTACION_ONEDRIVE_PYTHONANYWHERE.md` para otras opciones

**¿Listo para usar?**  
→ ¡Solo verifica el SMTP y listo! 🚀
