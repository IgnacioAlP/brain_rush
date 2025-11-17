# ⚡ GUÍA RÁPIDA: Agregar URLs de Redirección en Azure

## 🎯 Objetivo
Agregar las URLs de redirección para que funcione tanto en **local** como en **PythonAnywhere**.

---

## 📍 Paso a Paso

### 1. Abrir Azure Portal

Ve a: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade

### 2. Seleccionar tu Aplicación

Busca y click en: **"BrainRush OneDrive Integration"**

(Application ID: `82a058ff-b2a1-4de1-b416-23c72399825e`)

### 3. Ir a Authentication

En el menú lateral izquierdo, click en **"Authentication"** (Autenticación)

### 4. Agregar Platform Configuration

- Si NO tienes ninguna plataforma configurada:
  1. Click en **"+ Add a platform"**
  2. Selecciona **"Web"**

- Si YA tienes "Web" configurada:
  1. Busca la sección "Web" en "Platform configurations"
  2. Click en **"Add URI"** debajo de "Redirect URIs"

### 5. Agregar la Primera URL

En el campo "Redirect URIs", agrega:

```
http://localhost:5000/callback/onedrive
```

Click en **"Add URI"** para agregar otra

### 6. Agregar la Segunda URL

Agrega:

```
https://proyectoweb20252.pythonanywhere.com/callback/onedrive
```

### 7. Configurar Tokens (IMPORTANTE)

Más abajo, en la sección **"Implicit grant and hybrid flows"**, marca:

- ✅ **Access tokens** (used for implicit flows)
- ✅ **ID tokens** (used for implicit and hybrid flows)

### 8. Guardar

Click en **"Save"** (Guardar) en la parte superior

---

## ✅ Verificación

Después de guardar, deberías ver:

```
Platform configurations:
  Web
    Redirect URIs:
      • http://localhost:5000/callback/onedrive
      • https://proyectoweb20252.pythonanywhere.com/callback/onedrive
    
    Implicit grant and hybrid flows:
      ✅ Access tokens
      ✅ ID tokens
```

---

## 🧪 Probar Configuración

### En Local (http://localhost:5000)

1. Ejecuta: `python main.py`
2. Login como docente
3. Ve a "Mis Cuestionarios"
4. Click "Ver Resultados"
5. Click "☁️ Subir a OneDrive"
6. Debería aparecer: "Necesitas autorizar acceso a OneDrive primero"
7. Click "Aceptar"
8. Te redirige a Microsoft Login
9. Inicia sesión y acepta permisos
10. Vuelve a BrainRush
11. Mensaje: "✅ OneDrive conectado exitosamente"

### En PythonAnywhere (https://proyectoweb20252.pythonanywhere.com)

Mismo proceso, pero asegúrate de que `.env` tenga:

```env
ONEDRIVE_REDIRECT_URI=https://proyectoweb20252.pythonanywhere.com/callback/onedrive
```

---

## ⚠️ Errores Comunes

### Error: "AADSTS50011: The reply URL specified in the request does not match"

**Causa**: La URL no está agregada en Azure

**Solución**: Verifica que agregaste ambas URLs exactamente como se muestra arriba

### Error: "AADSTS700016: Application with identifier was not found"

**Causa**: Client ID incorrecto

**Solución**: Verifica que `.env` tenga el Client ID correcto

### Error: "invalid_client"

**Causa**: Client Secret incorrecto o expirado

**Solución**: 
1. Ve a "Certificates & secrets"
2. Crea un nuevo secret
3. Actualiza `.env` con el nuevo valor

---

## 🎉 ¡Listo!

Una vez agregadas las URLs, puedes:

1. **Ejecutar localmente**: `python main.py`
2. **Probar la autorización** de OneDrive
3. **Exportar resultados** directamente a OneDrive
4. **Subir a PythonAnywhere** cuando esté listo

---

**Fecha**: 27 de octubre de 2025  
**Estado**: Pendiente agregar URLs en Azure  
**Tiempo estimado**: 2-3 minutos
