# 📧 CONFIGURACIÓN DE CORREO GMAIL PARA BRAIN RUSH

## ✅ Pasos Completados:

---

## 📝 **PASO 1: Activar Verificación en 2 Pasos en Gmail**

### Opción 1: Enlace Directo
1. Ve a: **https://myaccount.google.com/signinoptions/two-step-verification**
2. Haz clic en **"Comenzar"**
3. Sigue los pasos:
   - Ingresa tu contraseña
   - Agrega tu número de teléfono
   - Ingresa el código que te llega por SMS
   - Confirma la activación

### Opción 2: Manual
1. Ve a: **https://myaccount.google.com/**
2. Clic en **"Seguridad"** (menú izquierdo)
3. Busca **"Verificación en dos pasos"**
4. Clic en **"Comenzar"** y sigue los pasos

**⚠️ IMPORTANTE:** Sin este paso NO podrás crear contraseñas de aplicación.

---

## 🔑 **PASO 2: Generar Contraseña de Aplicación**

Una vez activada la verificación en 2 pasos:

### Método 1: Enlace Directo
1. Ve a: **https://myaccount.google.com/apppasswords**
2. Inicia sesión si te lo pide

### Método 2: Manual
1. Ve a: **https://myaccount.google.com/**
2. Clic en **"Seguridad"**
3. Busca **"Contraseñas de aplicaciones"** (puede estar en "Cómo inicias sesión en Google")
4. Clic en ella

### Crear la contraseña:
1. En **"Seleccionar aplicación"**: Elige **"Correo"**
2. En **"Seleccionar dispositivo"**: Elige **"Otro (nombre personalizado)"**
3. Escribe: **"Brain Rush System"**
4. Clic en **"Generar"**

### Resultado:
Te mostrará una pantalla así:

```
┌─────────────────────────────────────┐
│  Tu contraseña de aplicación para:  │
│         Brain Rush System           │
│                                     │
│      abcd efgh ijkl mnop           │
│                                     │
│  Usa esta contraseña en lugar de   │
│  tu contraseña normal de Google    │
└─────────────────────────────────────┘
```

**⚠️ COPIA ESTA CONTRASEÑA AHORA:**
- Aparece solo UNA VEZ
- No podrás verla de nuevo
- Son 16 caracteres (Gmail los muestra con espacios pero debes copiarlos sin espacios)

**Ejemplo de contraseña:**
```
Mostrado: abcd efgh ijkl mnop
Copiar como: abcdefghijklmnop
```

---

## 📝 **PASO 3: Actualizar archivo .env**

Una vez que tengas tu contraseña de aplicación:

### 3.1 Abrir el archivo `.env`
El archivo está en:
```
C:\Users\laboratorio_computo\Downloads\brain_rush-main\brain_rush-main\.env
```

### 3.2 Actualizar estas líneas:

**ANTES:**
```env
MAIL_USERNAME=alonzopezoi@gmail.com
MAIL_PASSWORD=zjri vsxo jnzk pqsc
```

**DESPUÉS:**
```env
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-16-caracteres
```

**Ejemplo real:**
```env
MAIL_USERNAME=brainrush.app@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
```

### 3.3 Guardar el archivo

---

## ✅ **PASO 4: Verificar Configuración**

### 4.1 Verificar que config.py tenga MAIL_ENABLED = True

Abre `config.py` y verifica la sección `DevelopmentConfig`:

```python
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
    # Configuración de correo Gmail para desarrollo
    MAIL_ENABLED = True  # ← Debe estar en True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
```

### 4.2 Probar envío de correo

Crea un archivo temporal `test_email.py`:

```python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar envío de correo
"""
import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_envio_correo():
    """Probar envío de correo"""
    print("\n" + "="*60)
    print("PRUEBA DE ENVÍO DE CORREO")
    print("="*60)
    
    # Importar después de configurar el path
    from flask import Flask
    from config import config
    from extensions import mail
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear app de Flask
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app_config = config.get(env, config['default'])
    app.config.from_object(app_config)
    
    # Inicializar mail
    mail.init_app(app)
    
    print(f"\n📧 Configuración de correo:")
    print(f"   MAIL_ENABLED: {app.config.get('MAIL_ENABLED')}")
    print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    
    # Pedir correo de destino
    destinatario = input("\n✉️  Ingresa tu correo para recibir el correo de prueba: ").strip()
    
    if not destinatario:
        print("❌ No ingresaste un correo")
        return False
    
    print(f"\n📤 Enviando correo de prueba a: {destinatario}")
    
    try:
        with app.app_context():
            from flask_mail import Message
            
            msg = Message(
                subject='🧠 Prueba de Correo - Brain Rush',
                sender=app.config.get('MAIL_USERNAME'),
                recipients=[destinatario],
                html="""
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background: #f4f4f4; padding: 30px; border-radius: 10px;">
                            <h1 style="color: #4ECDC4; text-align: center;">🧠 Brain Rush</h1>
                            <h2 style="color: #333;">¡Correo de Prueba Exitoso! ✅</h2>
                            <p style="color: #666; font-size: 16px;">
                                Si estás viendo este correo, significa que la configuración de Gmail está correcta.
                            </p>
                            <div style="background: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                                <p style="margin: 0;"><strong>Servidor:</strong> smtp.gmail.com</p>
                                <p style="margin: 0;"><strong>Puerto:</strong> 587</p>
                                <p style="margin: 0;"><strong>Seguridad:</strong> TLS</p>
                            </div>
                            <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                                Este es un correo automático de prueba del sistema Brain Rush.
                            </p>
                        </div>
                    </body>
                </html>
                """
            )
            
            mail.send(msg)
            
            print("\n✅ ¡CORREO ENVIADO EXITOSAMENTE!")
            print(f"   Revisa la bandeja de entrada de: {destinatario}")
            print(f"   Si no lo ves, revisa la carpeta de SPAM")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR al enviar correo:")
        print(f"   {str(e)}")
        print("\n🔍 Posibles causas:")
        print("   1. Contraseña de aplicación incorrecta")
        print("   2. Verificación en 2 pasos no activada")
        print("   3. Correo de Gmail incorrecto")
        print("   4. Firewall bloqueando puerto 587")
        
        import traceback
        print("\n📋 Detalles del error:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        test_envio_correo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
```

Ejecuta:
```bash
python test_email.py
```

---

## 🔍 **SOLUCIÓN DE PROBLEMAS**

### Problema 1: "Username and Password not accepted"
**Causa:** Contraseña de aplicación incorrecta o verificación en 2 pasos no activada

**Solución:**
1. Verifica que la verificación en 2 pasos esté activada
2. Genera una nueva contraseña de aplicación
3. Copia EXACTAMENTE la contraseña (sin espacios)
4. Actualiza el `.env`

### Problema 2: "SMTPAuthenticationError"
**Causa:** Credenciales incorrectas

**Solución:**
1. Verifica que el correo en `.env` sea correcto
2. Verifica que la contraseña sea de APLICACIÓN, no tu contraseña normal
3. Intenta generar una nueva contraseña de aplicación

### Problema 3: "SMTPServerDisconnected"
**Causa:** Problema de conexión o puerto bloqueado

**Solución:**
1. Verifica tu conexión a internet
2. Verifica que el puerto 587 no esté bloqueado por firewall
3. Prueba desactivar temporalmente el antivirus

### Problema 4: "Could not connect to SMTP host"
**Causa:** Firewall o problema de red

**Solución:**
1. Verifica configuración de firewall
2. Prueba con otra red WiFi
3. Verifica que MAIL_PORT sea 587

---

## 📧 **CONFIGURACIONES ALTERNATIVAS**

### Si quieres usar otro servicio de correo:

#### Outlook/Hotmail:
```python
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'tu-correo@outlook.com'
MAIL_PASSWORD = 'tu-contraseña'
```

#### Yahoo:
```python
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'tu-correo@yahoo.com'
MAIL_PASSWORD = 'contraseña-de-aplicación'
```

---

## ✅ **CHECKLIST DE CONFIGURACIÓN**

- [ ] Verificación en 2 pasos activada en Gmail
- [ ] Contraseña de aplicación generada
- [ ] Archivo `.env` actualizado con correo y contraseña
- [ ] `MAIL_ENABLED = True` en `config.py`
- [ ] Prueba de envío ejecutada y exitosa
- [ ] Correo de prueba recibido (revisar spam)

---

## 🎯 **RESUMEN RÁPIDO**

1. **Activa verificación en 2 pasos:** https://myaccount.google.com/signinoptions/two-step-verification
2. **Genera contraseña de aplicación:** https://myaccount.google.com/apppasswords
3. **Actualiza `.env`** con tu correo y la contraseña de 16 caracteres
4. **Ejecuta:** `python test_email.py` para probar

---

## 📞 **¿Necesitas Ayuda?**

Si después de seguir estos pasos aún tienes problemas:

1. Verifica los logs de la aplicación
2. Ejecuta `python test_email.py` y comparte el error exacto
3. Verifica que tu correo de Gmail NO tenga restricciones de seguridad adicionales

---

**¡Con estos pasos deberías poder enviar correos sin problemas! 📧✅**
