# Configurar OneDrive en PythonAnywhere

## Problema
La exportación a OneDrive funciona en local pero no en PythonAnywhere.

## Causas comunes

1. **Variables de entorno no configuradas**
2. **Librería `msal` no instalada**
3. **URL de redirección incorrecta**
4. **Firewall o restricciones de red**

---

## Solución paso a paso

### 1. Instalar la librería msal

En la consola Bash de PythonAnywhere:

```bash
pip install msal
```

O agregar `msal` a tu `requirements.txt`:
```
msal==1.24.0
```

Luego ejecutar:
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

En PythonAnywhere, ve a la pestaña **Web** → **Virtualenv** → Sección **Environment variables**.

Agrega las siguientes variables:

| Variable | Valor |
|----------|-------|
| `AZURE_CLIENT_ID` | Tu Application (client) ID de Azure |
| `AZURE_CLIENT_SECRET` | Tu Client Secret de Azure |
| `AZURE_TENANT_ID` | Tu Directory (tenant) ID de Azure |
| `ONEDRIVE_REDIRECT_URI` | `https://TUDOMINIO.pythonanywhere.com/callback/onedrive` |

**⚠️ IMPORTANTE:** Reemplaza `TUDOMINIO` con tu nombre de usuario de PythonAnywhere.

### 3. Actualizar Azure App Registration

Ve a **Azure Portal** → **App registrations** → Tu aplicación → **Authentication**

#### Agregar URI de redirección:
```
https://TUDOMINIO.pythonanywhere.com/callback/onedrive
```

#### Configurar permisos (API permissions):
- `Files.ReadWrite` - Microsoft Graph
- `User.Read` - Microsoft Graph

**Asegúrate de dar consentimiento de administrador** si es necesario.

### 4. Verificar la configuración en PythonAnywhere

Crea un archivo temporal de prueba para verificar que las variables están cargadas:

```python
# test_config.py
import os
from dotenv import load_dotenv

load_dotenv()

print("AZURE_CLIENT_ID:", "✓" if os.getenv('AZURE_CLIENT_ID') else "✗")
print("AZURE_CLIENT_SECRET:", "✓" if os.getenv('AZURE_CLIENT_SECRET') else "✗")
print("AZURE_TENANT_ID:", "✓" if os.getenv('AZURE_TENANT_ID') else "✗")
print("ONEDRIVE_REDIRECT_URI:", os.getenv('ONEDRIVE_REDIRECT_URI'))
```

Ejecuta:
```bash
python test_config.py
```

### 5. Reiniciar la aplicación web

En PythonAnywhere:
1. Ve a la pestaña **Web**
2. Haz clic en el botón **Reload** (verde)

### 6. Probar la autenticación de OneDrive

1. Inicia sesión en tu aplicación
2. Ve a **Mi Perfil** o donde esté la opción de OneDrive
3. Haz clic en **Autorizar OneDrive**
4. Completa el flujo de OAuth2

---

## Verificar logs de error

En PythonAnywhere, puedes ver los logs en:
- **Web** → **Log files** → **Error log**
- **Web** → **Log files** → **Server log**

Busca mensajes como:
- `"Credenciales de Azure no configuradas"`
- `"msal no está instalado"`
- `"Error subiendo a OneDrive"`

---

## Alternativa: Usar solo Email

Si OneDrive sigue sin funcionar, el sistema automáticamente enviará el archivo por email como fallback. Asegúrate de que el email esté configurado correctamente:

```python
# En config.py
MAIL_ENABLED = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
```

Variables de entorno para email:
- `MAIL_USERNAME`: Tu email de Gmail
- `MAIL_PASSWORD`: App Password de Gmail (no tu contraseña normal)

---

## Troubleshooting

### Error: "File is not a zip file"
✅ **Solucionado**: El código ahora guarda los archivos temporalmente antes de procesarlos.

### Error: "msal not found"
```bash
pip install msal
```

### Error: "Invalid redirect URI"
Verifica que el `ONEDRIVE_REDIRECT_URI` en Azure coincida exactamente con el de tu `.env`

### Error: "Token expired"
El sistema intentará refrescar automáticamente el token. Si falla, el usuario debe volver a autorizar.

---

## Checklist final

- [ ] `msal` instalado en PythonAnywhere
- [ ] Variables de entorno configuradas
- [ ] URI de redirección actualizada en Azure
- [ ] Aplicación web reiniciada (Reload)
- [ ] Flujo de OAuth2 completado exitosamente
- [ ] Prueba de exportación realizada

---

## Soporte adicional

Si el problema persiste:
1. Revisa los logs de error
2. Verifica que el access token esté guardado en la base de datos
3. Prueba manualmente la API de Microsoft Graph con Postman o similar
4. Asegúrate de que PythonAnywhere no esté bloqueando conexiones a `graph.microsoft.com`
