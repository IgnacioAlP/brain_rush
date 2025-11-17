# 🚀 Configuración Completa de OneDrive OAuth2

## ✅ Implementación Completada

Se ha implementado la **exportación directa a OneDrive** usando OAuth2 con Azure AD. Ahora los archivos se suben automáticamente a la carpeta **BrainRush** en OneDrive.

---

## 📋 Credenciales de Azure

Ya configuradas en `.env`:

```
Application (client) ID: 82a058ff-b2a1-4de1-b416-23c72399825e
Client Secret: M~_8Q~dZuD1hRHBso22idTksshTyTKfxO7szbcQS
Tenant ID: 8e0398bb-f07c-490e-91b4-f369f3a6b1b0
```

---

## 🔧 Configuración en Azure Portal

### ⚠️ IMPORTANTE: Agregar URLs de Redirección

Debes agregar **AMBAS URLs** en Azure Portal:

1. **Ve a**: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade

2. **Selecciona** tu aplicación: "BrainRush OneDrive Integration"

3. **Ve a** "Authentication" (Autenticación) en el menú lateral

4. **En "Platform configurations"** → Click "Add a platform" → Selecciona **"Web"**

5. **Agrega AMBAS URLs de redirección**:
   ```
   http://localhost:5000/callback/onedrive
   https://proyectoweb20252.pythonanywhere.com/callback/onedrive
   ```

6. **Marca estas opciones**:
   - ✅ Access tokens (used for implicit flows)
   - ✅ ID tokens (used for implicit and hybrid flows)

7. **Click "Save"**

### Verificar Permisos API

1. **Ve a** "API permissions" (Permisos de API)

2. **Verifica que estén**:
   - ✅ `Files.ReadWrite` (Delegated)
   - ✅ `User.Read` (Delegated)

3. Si falta alguno:
   - Click "+ Add a permission"
   - Selecciona "Microsoft Graph"
   - Selecciona "Delegated permissions"
   - Busca y agrega los permisos faltantes

4. **Click "Grant admin consent"** (si tienes permisos de admin)

---

## 💻 Configuración Local (Desarrollo)

### Archivo `.env` (Ya configurado)

```env
# Configuración de correo Gmail
MAIL_USERNAME=alonzopezoi@gmail.com
MAIL_PASSWORD=zjri vsxo jnzk pqsc

# Configuración de OneDrive Azure AD
AZURE_CLIENT_ID=82a058ff-b2a1-4de1-b416-23c72399825e
AZURE_CLIENT_SECRET=M~_8Q~dZuD1hRHBso22idTksshTyTKfxO7szbcQS
AZURE_TENANT_ID=8e0398bb-f07c-490e-91b4-f369f3a6b1b0

# Para LOCAL
ONEDRIVE_REDIRECT_URI=http://localhost:5000/callback/onedrive
```

### Ejecutar localmente

```bash
python main.py
```

Debería abrir en: http://localhost:5000

---

## 🌐 Configuración PythonAnywhere (Producción)

### 1. Subir archivos

Sube todos los archivos modificados a PythonAnywhere:
- `main.py`
- `config.py`
- `Templates/ResultadosJuego.html`
- `Templates/MisCuestionarios.html`
- `requirements.txt`

### 2. Crear archivo `.env`

En PythonAnywhere, crea un archivo `.env` con:

```env
# Configuración de correo Gmail
MAIL_USERNAME=alonzopezoi@gmail.com
MAIL_PASSWORD=zjri vsxo jnzk pqsc

# Configuración de OneDrive Azure AD
AZURE_CLIENT_ID=82a058ff-b2a1-4de1-b416-23c72399825e
AZURE_CLIENT_SECRET=M~_8Q~dZuD1hRHBso22idTksshTyTKfxO7szbcQS
AZURE_TENANT_ID=8e0398bb-f07c-490e-91b4-f369f3a6b1b0

# Para PYTHONANYWHERE
ONEDRIVE_REDIRECT_URI=https://proyectoweb20252.pythonanywhere.com/callback/onedrive
```

### 3. Instalar dependencias

En la consola de PythonAnywhere:

```bash
pip install --user msal requests
```

O desde requirements.txt:

```bash
pip install --user -r requirements.txt
```

### 4. Ejecutar migración SQL

```bash
python agregar_tokens_simple.py
```

### 5. Reload de la aplicación

En PythonAnywhere → Web → Click **"Reload"**

---

## 🎯 Flujo de Uso

### Primera vez (Autorización)

1. **Usuario** hace clic en "☁️ Subir a OneDrive"

2. **Sistema** detecta que no hay token

3. **Aparece mensaje**: "Necesitas autorizar acceso a OneDrive primero. ¿Deseas autorizar OneDrive ahora?"

4. **Usuario** hace clic en "Aceptar"

5. **Redirección** a Microsoft Login:
   - Usuario inicia sesión con su cuenta Microsoft
   - Acepta permisos de BrainRush
   
6. **Callback** regresa a BrainRush

7. **Token guardado** en la base de datos

8. **Mensaje**: "✅ OneDrive conectado exitosamente. Ahora puedes exportar resultados directamente."

### Exportaciones siguientes (Automáticas)

1. **Usuario** hace clic en "☁️ Subir a OneDrive"

2. **Sistema** usa el token guardado

3. **Archivo se sube** automáticamente a OneDrive/BrainRush/

4. **Mensaje**: "✅ Archivo 'BrainRush_Resultados_...xlsx' subido exitosamente a OneDrive"

5. **Pregunta**: "¿Deseas abrir el archivo en OneDrive?"

6. Si acepta → Se abre OneDrive en nueva pestaña

---

## 📁 Estructura en OneDrive

Los archivos se guardan en:

```
OneDrive/
└── BrainRush/
    ├── BrainRush_Resultados_Matematicas_20251027_153045.xlsx
    ├── BrainRush_Resultados_Historia_20251027_160120.xlsx
    └── BrainRush_Resultados_Ciencias_20251027_173215.xlsx
```

---

## 🔄 Renovación Automática de Tokens

El sistema maneja automáticamente:

1. **Tokens expirados** → Se renuevan automáticamente con refresh token
2. **Refresh token inválido** → Solicita nueva autorización
3. **Error de conexión** → Fallback a email

---

## ⚠️ Solución de Problemas

### Error: "redirect_uri_mismatch"

**Causa**: La URL de redirección no está configurada en Azure

**Solución**:
1. Ve a Azure Portal → Tu aplicación
2. Authentication → Platform configurations → Web
3. Agrega ambas URLs:
   - `http://localhost:5000/callback/onedrive`
   - `https://proyectoweb20252.pythonanywhere.com/callback/onedrive`

### Error: "invalid_client"

**Causa**: Client ID o Secret incorrectos

**Solución**:
1. Verifica `.env` tiene las credenciales correctas
2. Verifica que no haya espacios extra
3. En Azure, crea un nuevo Client Secret si es necesario

### Error: "insufficient_permissions"

**Causa**: Faltan permisos API

**Solución**:
1. Azure Portal → API permissions
2. Agrega `Files.ReadWrite` y `User.Read`
3. Click "Grant admin consent"

### Error: "AADSTS50011: The reply URL specified in the request does not match"

**Causa**: URL de redirección no coincide

**Solución**:
1. Verifica que `.env` tenga la URL correcta para tu entorno
2. Local: `http://localhost:5000/callback/onedrive`
3. PythonAnywhere: `https://proyectoweb20252.pythonanywhere.com/callback/onedrive`

### Los archivos no se suben a OneDrive

**Verificar**:
1. ¿Aparece mensaje "Necesitas autorizar OneDrive"? → Autoriza
2. ¿Expiraron los tokens? → Volverá a pedir autorización automáticamente
3. ¿Hay error de conexión? → Revisa logs en PythonAnywhere
4. ¿Fallback a email? → OneDrive puede estar bloqueado, pero el archivo llega por correo

---

## 🧪 Pruebas

### Prueba 1: Autorización (Primera vez)

```
1. Login como docente
2. Ve a "Mis Cuestionarios"
3. Click "Ver Resultados" en una sala
4. Click "☁️ Subir a OneDrive"
5. Mensaje: "Necesitas autorizar..."
6. Click "Aceptar"
7. Login en Microsoft
8. Aceptar permisos
9. Redirección a dashboard
10. Mensaje: "✅ OneDrive conectado exitosamente"
```

### Prueba 2: Subida Automática

```
1. Click "☁️ Subir a OneDrive" nuevamente
2. Archivo se sube automáticamente
3. Mensaje: "✅ Archivo ... subido exitosamente"
4. Click "Sí" para abrir OneDrive
5. Archivo visible en carpeta BrainRush
```

### Prueba 3: Múltiples Exportaciones

```
1. Exportar varios cuestionarios diferentes
2. Todos se suben a OneDrive/BrainRush/
3. Nombres únicos con timestamp
```

---

## 📊 Comparación: Antes vs Ahora

| Característica | Email (Antes) | OneDrive OAuth2 (Ahora) |
|----------------|--------------|-------------------------|
| **Requiere Azure** | ❌ | ✅ (una sola vez) |
| **Autorización** | ❌ | ✅ (primera vez) |
| **Subida automática** | ❌ | ✅ |
| **Ubicación** | Email | OneDrive/BrainRush/ |
| **Organización** | Manual | Automática |
| **Acceso directo** | ❌ | ✅ (link en mensaje) |
| **Fallback** | N/A | ✅ Email automático |
| **Complejidad setup** | Baja | Media |
| **Experiencia usuario** | Manual | Automática |

---

## 📝 Archivos Modificados

1. **`.env`** → Credenciales Azure (local)
2. **`.env.pythonanywhere`** → Credenciales Azure (producción)
3. **`config.py`** → Configuración Azure
4. **`main.py`** → Endpoints OAuth2 y exportación
5. **`Templates/ResultadosJuego.html`** → Manejo de autorización
6. **`Templates/MisCuestionarios.html`** → Manejo de autorización
7. **`requirements.txt`** → Dependencias msal y requests
8. **`agregar_tokens_simple.py`** → Migración SQL (ya ejecutado)

---

## 🎉 Próximos Pasos

1. ✅ Agregar URLs de redirección en Azure Portal
2. ✅ Probar localmente
3. ✅ Subir a PythonAnywhere
4. ✅ Configurar `.env` en PythonAnywhere
5. ✅ Instalar dependencias
6. ✅ Reload de la app
7. ✅ Probar en producción

---

**Implementado**: 27 de octubre de 2025  
**Estado**: ✅ Listo para probar  
**Método**: OAuth2 con Azure AD  
**Soporte**: Local ✓ | PythonAnywhere ✓
