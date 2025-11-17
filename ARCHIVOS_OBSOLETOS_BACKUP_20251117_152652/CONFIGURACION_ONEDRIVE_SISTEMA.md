# 🔧 Configuración de OneDrive con Credenciales del Sistema

Este documento explica cómo configurar OneDrive para que los archivos se guarden en **TU OneDrive** (del sistema) y se compartan automáticamente con los usuarios.

## 📋 Ventajas de este Enfoque

✅ **Centralizado**: Todos los archivos en un solo OneDrive del sistema  
✅ **Seguro**: No requiere OAuth de cada usuario  
✅ **Compartición automática**: Se genera link público para cada archivo  
✅ **Fácil gestión**: Puedes ver todos los archivos exportados en un solo lugar  
✅ **Sin límites**: No depende de la cuenta OneDrive de cada usuario  

## 🔐 Configuración en Azure Portal

### Paso 1: Ir a Azure Portal
1. Abre https://portal.azure.com
2. Inicia sesión con tu cuenta de Microsoft
3. Ve a **Azure Active Directory**

### Paso 2: Registrar Aplicación (si no la tienes)
1. En el menú izquierdo, selecciona **App registrations**
2. Click en **+ New registration**
3. Nombre: `BrainRush OneDrive Integration`
4. Supported account types: **Accounts in any organizational directory and personal Microsoft accounts**
5. Redirect URI: 
   - Platform: **Web**
   - URI: `http://localhost:5000/callback/onedrive` (para desarrollo)
6. Click **Register**

### Paso 3: Configurar Permisos de API ⚠️ IMPORTANTE

Esto es lo que hace que el sistema use TU OneDrive en lugar del usuario:

1. En tu aplicación registrada, ve a **API permissions**
2. Click **+ Add a permission**
3. Selecciona **Microsoft Graph**
4. Selecciona **Application permissions** (NO Delegated permissions)
5. Busca y marca estos permisos:

   ```
   ✅ Files.ReadWrite.All
      (Permite leer y escribir archivos en OneDrive)
   
   ✅ Sites.ReadWrite.All  
      (Opcional, para SharePoint si lo necesitas)
   ```

6. Click **Add permissions**
7. ⚠️ **MUY IMPORTANTE**: Click en **Grant admin consent for [Tu organización]**
   - Esto te pedirá confirmar como administrador
   - Sin esto, los permisos no funcionarán

### Paso 4: Obtener Credenciales

1. **Client ID**: 
   - En la página Overview de tu app
   - Copia el **Application (client) ID**
   - Ya lo tienes: `f1996472-dd17-447c-bcdb-f8b76dd9b861`

2. **Client Secret**:
   - Ve a **Certificates & secrets**
   - Click **+ New client secret**
   - Description: `BrainRush Secret`
   - Expires: **24 months** (o el tiempo que prefieras)
   - Click **Add**
   - **⚠️ COPIA EL VALUE INMEDIATAMENTE** (solo se muestra una vez)
   - Ya lo tienes: `Enu8Q~u0BPSAQKsQcZBUgXSOTrUiCidHk3IIVcB-`

3. **Tenant ID**:
   - En la página Overview
   - Copia el **Directory (tenant) ID**
   - Para cuentas personales, usa: `common` o `consumers`
   - Ya lo tienes configurado como: `common`

### Paso 5: Actualizar .env

Tu archivo `.env` ya está configurado correctamente:

```properties
AZURE_CLIENT_ID=f1996472-dd17-447c-bcdb-f8b76dd9b861
AZURE_CLIENT_SECRET=Enu8Q~u0BPSAQKsQcZBUgXSOTrUiCidHk3IIVcB-
AZURE_TENANT_ID=common
```

## 🔄 Cómo Funciona el Nuevo Sistema

### Flujo de Exportación

```
1. Usuario hace click en "Exportar a OneDrive"
   ↓
2. Sistema genera archivo Excel con datos del usuario
   ↓
3. Sistema obtiene token de aplicación (NO de usuario)
   usando Client Credentials Flow
   ↓
4. Sistema sube archivo a TU OneDrive
   en carpeta: /BrainRush/
   ↓
5. Sistema crea link de compartición público
   tipo: "view" (solo lectura)
   scope: "anonymous" (cualquiera con el link)
   ↓
6. Sistema envía email al usuario con:
   - Link directo al archivo
   - Nombre del archivo
   - Estadísticas del historial
   ↓
7. Usuario recibe email y puede:
   - Ver el archivo en línea
   - Descargar el archivo
   - Compartirlo con otros
```

### Diferencias con el Sistema Anterior

| Característica | Sistema Anterior (OAuth) | Sistema Nuevo (Aplicación) |
|----------------|-------------------------|---------------------------|
| **OneDrive usado** | De cada usuario | Del sistema (TU cuenta) |
| **Requiere login** | Sí, cada usuario | No |
| **Gestión** | Descentralizada | Centralizada |
| **Compartición** | Manual | Automática |
| **Permisos** | Delegated | Application |
| **Token** | Por usuario | Del sistema |

## 📁 Estructura de Archivos en OneDrive

Los archivos se guardarán así en TU OneDrive:

```
📁 OneDrive (Tu cuenta)
└── 📁 BrainRush/
    ├── 📄 BrainRush_MiHistorial_Juan_Perez_20241028_153045.xlsx
    ├── 📄 BrainRush_MiHistorial_Maria_Lopez_20241028_154130.xlsx
    ├── 📄 BrainRush_Resultados_Quiz_Matematicas_20241028_160215.xlsx
    └── 📄 BrainRush_Resultados_Quiz_Historia_20241028_161530.xlsx
```

## 🧪 Probar la Configuración

### Opción 1: Desde la Aplicación

1. Inicia sesión como estudiante
2. Ve a "Mi Historial"
3. Click en "Exportar mi Historial a OneDrive"
4. Verifica:
   - ✅ No debería pedir login de OneDrive
   - ✅ Debería mostrar mensaje de éxito
   - ✅ Debería enviar email con link
   - ✅ El link debe abrir el archivo en OneDrive

### Opción 2: Verificar en OneDrive

1. Ve a https://onedrive.live.com
2. Inicia sesión con TU cuenta de Microsoft
3. Verifica que exista la carpeta `BrainRush`
4. Dentro debe aparecer el archivo exportado
5. Click derecho > Compartir > Debe mostrar que ya está compartido

## ❌ Solución de Problemas

### Error: "No se pudo obtener token de acceso"

**Causa**: Permisos de aplicación no configurados correctamente

**Solución**:
1. Ve a Azure Portal > Tu App > API permissions
2. Verifica que los permisos sean **Application** (no Delegated)
3. Click en "Grant admin consent"
4. Espera 5 minutos para que se propague

### Error: "Access denied"

**Causa**: Falta consentimiento de administrador

**Solución**:
1. Azure Portal > API permissions
2. Click en "Grant admin consent for Default Directory"
3. Confirma con tu cuenta de administrador

### Error: "Invalid tenant"

**Causa**: Tenant ID incorrecto para cuenta personal

**Solución**:
- Para cuentas personales (@hotmail, @outlook), usa:
  ```
  AZURE_TENANT_ID=consumers
  ```
- Para cuentas organizacionales, usa el GUID real del tenant

### El archivo se sube pero no se comparte

**Causa**: Permisos insuficientes para crear links

**Solución**:
1. Agrega permiso: `Sites.ReadWrite.All`
2. Grant admin consent nuevamente

## 🔒 Seguridad

### Consideraciones Importantes

✅ **Links anónimos**: Los archivos son de solo lectura  
✅ **No listables**: Solo quien tiene el link puede acceder  
✅ **Expirables**: Puedes configurar expiración en Azure  
✅ **Auditoría**: OneDrive registra quién accede a los archivos  

### Recomendaciones

1. **Revisa periódicamente** los archivos en la carpeta BrainRush
2. **Limpia archivos antiguos** si es necesario
3. **Monitorea el uso** de tu cuenta OneDrive
4. **Configura alertas** en Azure para accesos inusuales

## 📊 Monitoreo

### Ver estadísticas en Azure

1. Azure Portal > Tu App > Monitoring
2. Click en "Sign-ins" para ver autenticaciones
3. Click en "Usage" para ver llamadas a la API

### Ver archivos compartidos

1. OneDrive web > Compartido
2. Ahí verás todos los links activos
3. Puedes revocar acceso si es necesario

## 🚀 Para Producción (PythonAnywhere)

### Cambios necesarios

1. En PythonAnywhere, agrega las mismas variables de entorno:
   ```bash
   AZURE_CLIENT_ID=f1996472-dd17-447c-bcdb-f8b76dd9b861
   AZURE_CLIENT_SECRET=Enu8Q~u0BPSAQKsQcZBUgXSOTrUiCidHk3IIVcB-
   AZURE_TENANT_ID=common
   ```

2. Instala MSAL:
   ```bash
   pip install msal
   ```

3. Reinicia la aplicación

4. **No necesitas** cambiar redirect URI porque no usamos OAuth de usuario

## 📧 Template del Email

Los usuarios recibirán un email así:

```
De: Brain RUSH <alonzopezoi@gmail.com>
Para: estudiante@ejemplo.com
Asunto: 📊 Tu Historial de Brain RUSH está listo

¡Tu Historial está listo! 📊

Hola Juan Pérez,

Tu historial de participaciones ha sido exportado exitosamente a OneDrive.

📁 Archivo: BrainRush_MiHistorial_Juan_Perez_20241028_153045.xlsx

📊 Estadísticas:
Total de juegos: 15
Puntos acumulados: 12,450
Promedio: 830.0 pts/juego

[Ver mi Historial en OneDrive]
(Botón grande y bonito)

💡 Puedes descargar y guardar este archivo para tus registros personales.
```

## ✅ Checklist de Configuración

- [ ] App registrada en Azure Portal
- [ ] Permisos de Application configurados (`Files.ReadWrite.All`)
- [ ] Admin consent otorgado
- [ ] Client ID copiado al .env
- [ ] Client Secret copiado al .env
- [ ] Tenant ID configurado (`common` para cuentas personales)
- [ ] MSAL instalado (`pip install msal`)
- [ ] Email configurado en .env
- [ ] Probado localmente
- [ ] Verificado que se crea carpeta BrainRush
- [ ] Verificado que se comparte el archivo
- [ ] Verificado que se envía email con link

---

**Creado**: 28/10/2024  
**Última actualización**: 28/10/2024  
**Versión**: 2.0 - Sistema centralizado con Application Permissions
