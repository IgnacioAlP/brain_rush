# 🔧 Configuración de OneDrive para Producción

## Problema Identificado
Cuando intentas autorizar OneDrive en producción, estás siendo redirigido a `localhost` en lugar de tu dominio de producción `http://proyectoweb20252.pythonanywhere.com`.

## Solución

### 1. Configurar Variable de Entorno en PythonAnywhere

Debes agregar la siguiente variable de entorno en tu servidor de PythonAnywhere:

**Variable:** `ONEDRIVE_REDIRECT_URI`  
**Valor:** `http://proyectoweb20252.pythonanywhere.com/callback/onedrive`

#### ¿Cómo agregar variables de entorno en PythonAnywhere?

**Opción A: Archivo .env (Recomendado)**

1. Accede a tu consola de PythonAnywhere
2. Navega a tu directorio del proyecto:
   ```bash
   cd ~/proyectoweb20252.pythonanywhere.com
   ```
3. Edita o crea el archivo `.env`:
   ```bash
   nano .env
   ```
4. Agrega la línea:
   ```
   ONEDRIVE_REDIRECT_URI=http://proyectoweb20252.pythonanywhere.com/callback/onedrive
   ```
5. Guarda y cierra (Ctrl+X, luego Y, luego Enter)

**Opción B: En el archivo WSGI**

Si estás usando el archivo WSGI de PythonAnywhere, agrega antes de importar tu aplicación:

```python
import os
os.environ['ONEDRIVE_REDIRECT_URI'] = 'http://proyectoweb20252.pythonanywhere.com/callback/onedrive'
```

### 2. Configurar Azure AD (Portal de Azure)

**IMPORTANTE:** También debes agregar esta URL en tu aplicación de Azure AD.

1. Ve a [Azure Portal](https://portal.azure.com)
2. Ve a **Azure Active Directory** → **App registrations**
3. Selecciona tu aplicación (la que tiene tu `AZURE_CLIENT_ID`)
4. Ve a **Authentication** (Autenticación)
5. En la sección **Platform configurations** → **Web**
6. Agrega una nueva **Redirect URI**:
   ```
   http://proyectoweb20252.pythonanywhere.com/callback/onedrive
   ```
7. Haz clic en **Save** (Guardar)

### 3. Reiniciar Aplicación

Después de hacer los cambios:

1. Ve a la pestaña **Web** en PythonAnywhere
2. Haz clic en el botón **Reload** (Recargar) para reiniciar tu aplicación

### 4. Probar la Configuración

Ahora prueba accediendo a:
```
http://proyectoweb20252.pythonanywhere.com/auth/onedrive-sistema
```

Deberías ser redirigido a Microsoft para autorizar, y luego de regreso a tu aplicación en producción.

## Variables de Entorno Necesarias en Producción

Asegúrate de tener TODAS estas variables configuradas en tu `.env` de producción:

```bash
# Flask
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
FLASK_ENV=production

# Azure AD / OneDrive
AZURE_CLIENT_ID=tu-client-id-de-azure
AZURE_CLIENT_SECRET=tu-client-secret-de-azure
AZURE_TENANT_ID=tu-tenant-id-de-azure
ONEDRIVE_REDIRECT_URI=http://proyectoweb20252.pythonanywhere.com/callback/onedrive

# Tokens del sistema (se generarán después de autorizar)
# ONEDRIVE_ACCESS_TOKEN=se-genera-automaticamente
# ONEDRIVE_REFRESH_TOKEN=se-genera-automaticamente
# ONEDRIVE_TOKEN_EXPIRES=se-genera-automaticamente
```

## Notas Importantes

### Sobre HTTP vs HTTPS
- Si tu dominio de PythonAnywhere usa **HTTPS** (recomendado), usa:
  ```
  https://proyectoweb20252.pythonanywhere.com/callback/onedrive
  ```
- Verifica qué protocolo usa tu app en producción

### Para Desarrollo Local
- En local (tu computadora), la variable debe seguir siendo:
  ```
  ONEDRIVE_REDIRECT_URI=http://localhost:5000/callback/onedrive
  ```
- Por eso es importante usar variables de entorno diferentes para cada entorno

### Múltiples Redirect URIs en Azure
Puedes tener AMBAS URLs configuradas en Azure AD:
- `http://localhost:5000/callback/onedrive` (para desarrollo)
- `http://proyectoweb20252.pythonanywhere.com/callback/onedrive` (para producción)

Esto te permite trabajar en ambos entornos sin tener que cambiar la configuración de Azure constantemente.

## Solución de Problemas

### Error: "redirect_uri mismatch"
- Verifica que la URL en Azure AD sea EXACTAMENTE igual a la variable de entorno
- Revisa mayúsculas/minúsculas
- Verifica http vs https

### Error: "AADSTS50011: The reply URL specified in the request does not match"
- La URL de redirección no está registrada en Azure AD
- Ve a Azure Portal y agrégala como se indica en el paso 2

### Los tokens no se guardan
- Asegúrate de tener permisos de escritura en el archivo `.env`
- Verifica que el código tenga acceso para actualizar el archivo

## Verificación Final

Después de configurar todo, verifica:

✅ Variable `ONEDRIVE_REDIRECT_URI` configurada en producción  
✅ URL agregada en Azure AD → Authentication  
✅ Aplicación reiniciada en PythonAnywhere  
✅ Puedes acceder a `/auth/onedrive-sistema` sin errores  
✅ La autorización redirige correctamente a tu dominio de producción  

---

**¿Necesitas ayuda?** Si sigues teniendo problemas, revisa los logs de tu aplicación en PythonAnywhere:
- Ve a **Web** → **Log files**
- Revisa el **Error log** para ver mensajes de error detallados
