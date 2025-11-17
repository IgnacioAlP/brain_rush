# 🔑 Cómo Obtener Tokens de OneDrive para el Sistema

Este documento explica cómo obtener los tokens necesarios para que Brain RUSH pueda guardar archivos en tu cuenta de OneDrive.

## 📋 ¿Qué son estos tokens?

Los tokens son credenciales que permiten a Brain RUSH acceder a tu OneDrive para:
- ✅ Guardar archivos exportados
- ✅ Crear carpeta BrainRush
- ✅ Compartir archivos automáticamente
- ✅ Enviar links por correo a los usuarios

## 🚀 Método Automático (Recomendado)

### Paso 1: Iniciar la Aplicación

```bash
python main.py
```

### Paso 2: Iniciar Sesión como Administrador

1. Ve a http://localhost:5000
2. Inicia sesión con tu cuenta de **administrador**
3. Verifica que tu usuario tenga tipo `admin` en la base de datos

### Paso 3: Autorizar OneDrive del Sistema

**Opción A - Desde el navegador:**

1. Ve a esta URL:
   ```
   http://localhost:5000/auth/onedrive-sistema
   ```

2. Te redirigirá a Microsoft para que autorices la aplicación

3. **IMPORTANTE**: Inicia sesión con la cuenta de OneDrive donde quieres que se guarden los archivos
   - Puede ser tu cuenta personal (@hotmail.com, @outlook.com)
   - Puede ser una cuenta organizacional
   - Esta será la cuenta del "sistema" donde se centralizan todos los archivos

4. Acepta los permisos solicitados:
   - ✅ Acceso a tus archivos
   - ✅ Mantener acceso a los datos que le has dado permiso
   - ✅ offline_access (para refrescar tokens)

5. Después de autorizar, verás una página de confirmación con:
   ```
   ✅ Configuración de OneDrive Exitosa
   
   📋 Tokens Obtenidos:
   ONEDRIVE_ACCESS_TOKEN=EwBoA8l6BA...
   ONEDRIVE_REFRESH_TOKEN=M.R3_BAY...
   ONEDRIVE_TOKEN_EXPIRES=2024-10-28T16:30:45.123456
   ```

6. **Los tokens ya están guardados automáticamente en tu archivo .env** ✅

### Paso 4: Verificar el archivo .env

Abre tu archivo `.env` y verifica que tenga esto:

```properties
# Tokens de OneDrive del sistema
ONEDRIVE_ACCESS_TOKEN=EwBoA8l6BAAUO9... (cadena larga)
ONEDRIVE_REFRESH_TOKEN=M.R3_BAY.-CQ... (cadena larga)
ONEDRIVE_TOKEN_EXPIRES=2024-10-28T16:30:45.123456
```

### Paso 5: ¡Listo! 🎉

Ya puedes usar la funcionalidad de exportar a OneDrive. Los archivos se guardarán en la cuenta que autorizaste.

---

## 🔧 Método Manual (Avanzado)

Si prefieres obtener los tokens manualmente usando Postman o similar:

### 1. Obtener Authorization Code

Abre esta URL en tu navegador (reemplaza los valores):

```
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
client_id=f1996472-dd17-447c-bcdb-f8b76dd9b861
&response_type=code
&redirect_uri=http://localhost:5000/callback/onedrive
&response_mode=query
&scope=Files.ReadWrite.All%20offline_access
```

Inicia sesión y autoriza. Serás redirigido a:
```
http://localhost:5000/callback/onedrive?code=M.R3_BAY.abc123...
```

Copia el valor del parámetro `code`.

### 2. Intercambiar Code por Tokens

Usa Postman o curl:

```bash
curl -X POST https://login.microsoftonline.com/common/oauth2/v2.0/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=f1996472-dd17-447c-bcdb-f8b76dd9b861" \
  -d "client_secret=Enu8Q~u0BPSAQKsQcZBUgXSOTrUiCidHk3IIVcB-" \
  -d "code=M.R3_BAY.abc123..." \
  -d "redirect_uri=http://localhost:5000/callback/onedrive" \
  -d "grant_type=authorization_code" \
  -d "scope=Files.ReadWrite.All offline_access"
```

Respuesta:
```json
{
  "access_token": "EwBoA8l6BAAUO9...",
  "refresh_token": "M.R3_BAY.-CQ...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### 3. Agregar al .env

Copia los valores a tu archivo `.env`:

```properties
ONEDRIVE_ACCESS_TOKEN=EwBoA8l6BAAUO9...
ONEDRIVE_REFRESH_TOKEN=M.R3_BAY.-CQ...
ONEDRIVE_TOKEN_EXPIRES=2024-10-28T16:30:45.123456
```

Para `ONEDRIVE_TOKEN_EXPIRES`, calcula:
```python
from datetime import datetime, timedelta
expires = datetime.now() + timedelta(seconds=3600)
print(expires.isoformat())
```

---

## 🔄 Renovación Automática de Tokens

### ¿Cuándo expiran los tokens?

- **Access Token**: Expira en ~1 hora
- **Refresh Token**: Válido por ~90 días (si se usa regularmente)

### ¿Qué hace el sistema automáticamente?

1. **Al exportar un archivo**:
   - Verifica si el `access_token` sigue válido
   - Si expiró, usa el `refresh_token` para obtener uno nuevo
   - Actualiza automáticamente el archivo `.env` con los nuevos tokens
   - ✅ **No necesitas hacer nada manual**

2. **Si el refresh_token expira**:
   - El sistema intentará usar Client Credentials Flow (si tienes Application Permissions)
   - Si falla, te mostrará un mensaje para que vuelvas a autorizar

### Renovar manualmente (si es necesario)

Si por alguna razón los tokens expiran y quieres renovarlos manualmente:

1. Ve a: http://localhost:5000/auth/onedrive-sistema
2. Autoriza nuevamente
3. Los nuevos tokens se guardarán automáticamente

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE: Protege tus tokens

```bash
# Asegúrate de que .env esté en .gitignore
echo ".env" >> .gitignore

# NUNCA subas el .env a GitHub
git rm --cached .env  # Si ya lo subiste por error
```

### Permisos otorgados

Los tokens tienen estos permisos:
- ✅ `Files.ReadWrite.All` - Leer y escribir archivos
- ✅ `offline_access` - Refrescar tokens sin interacción

### ¿Qué puede hacer Brain RUSH con estos tokens?

- ✅ Crear carpeta BrainRush
- ✅ Subir archivos Excel
- ✅ Crear links de compartición
- ❌ NO puede eliminar archivos existentes (solo los que sube)
- ❌ NO puede acceder a otras carpetas de OneDrive

---

## 🧪 Probar que Funciona

### Test 1: Verificar tokens en memoria

1. Inicia la aplicación:
   ```bash
   python main.py
   ```

2. En la consola deberías ver:
   ```
   ✅ Usando token de OneDrive del .env (válido)
   ```

### Test 2: Exportar historial

1. Inicia sesión como estudiante
2. Ve a "Mi Historial"
3. Click en "Exportar a OneDrive"
4. Deberías ver:
   - Mensaje de éxito
   - Email enviado con link
   - Archivo en OneDrive

### Test 3: Verificar en OneDrive

1. Ve a https://onedrive.live.com
2. Inicia sesión con la cuenta que autorizaste
3. Verifica:
   - ✅ Existe carpeta "BrainRush"
   - ✅ Hay archivos dentro
   - ✅ Los archivos están compartidos (tienen icono de link)

---

## 🐛 Solución de Problemas

### Error: "No se pudo obtener token de OneDrive"

**Causa**: Los tokens en .env están vacíos o expirados

**Solución**:
```bash
# 1. Ve a la URL de autorización
http://localhost:5000/auth/onedrive-sistema

# 2. Autoriza nuevamente
# 3. Los tokens se actualizarán automáticamente
```

### Error: "Access denied" o "Invalid token"

**Causa**: Token expirado o revocado

**Solución**:
1. Elimina los tokens del .env:
   ```properties
   ONEDRIVE_ACCESS_TOKEN=
   ONEDRIVE_REFRESH_TOKEN=
   ONEDRIVE_TOKEN_EXPIRES=
   ```
2. Vuelve a autorizar: http://localhost:5000/auth/onedrive-sistema

### Error: "Refresh token expired"

**Causa**: El refresh_token solo es válido por 90 días si no se usa

**Solución**:
- Vuelve a autorizar: http://localhost:5000/auth/onedrive-sistema
- Usa la exportación al menos una vez cada 90 días

### Los archivos no aparecen en OneDrive

**Verifica**:
1. Los tokens están en .env
2. La cuenta autorizada es la correcta
3. Hay espacio disponible en OneDrive
4. Revisa la consola de Python para ver errores

---

## 📊 Información de los Tokens

### Access Token

```
Longitud: ~1500-2000 caracteres
Formato: Base64
Ejemplo: EwBoA8l6BAAUO9chh7Xs9sleNTQgkj...
Validez: 1 hora
```

### Refresh Token

```
Longitud: ~400-600 caracteres
Formato: Base64
Ejemplo: M.R3_BAY.-CQY9yVyXn1xRHzGOOz8...
Validez: 90 días (con uso regular)
```

### Token Expires

```
Formato: ISO 8601
Ejemplo: 2024-10-28T16:30:45.123456
```

---

## 📝 Checklist de Configuración

- [ ] Aplicación iniciada (`python main.py`)
- [ ] Sesión iniciada como admin
- [ ] URL visitada: http://localhost:5000/auth/onedrive-sistema
- [ ] Autorización completada en Microsoft
- [ ] Página de confirmación mostrada
- [ ] Tokens verificados en .env
- [ ] Test de exportación exitoso
- [ ] Archivo visible en OneDrive
- [ ] Email recibido con link
- [ ] .env en .gitignore

---

## 🆘 Soporte

Si tienes problemas:

1. **Revisa la consola** de Python para ver errores detallados
2. **Verifica el .env** que tenga los tokens correctos
3. **Prueba refrescar** los tokens visitando `/auth/onedrive-sistema`
4. **Verifica Azure** que los permisos estén configurados

---

**Creado**: 28/10/2024  
**Última actualización**: 28/10/2024  
**Versión**: 1.0 - Sistema de tokens en .env
