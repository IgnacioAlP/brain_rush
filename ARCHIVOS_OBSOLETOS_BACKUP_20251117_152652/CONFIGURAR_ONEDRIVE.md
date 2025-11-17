# Configuración de OneDrive para Exportación de Resultados

Este documento explica cómo configurar la integración con OneDrive para exportar los resultados de BrainRush directamente a la cuenta de OneDrive del usuario.

## Requisitos Previos

1. Una cuenta de Microsoft (Office 365, Outlook, Hotmail, etc.)
2. Acceso al portal de Azure para registrar la aplicación

## Paso 1: Registrar la Aplicación en Azure

1. Ve al [Portal de Azure](https://portal.azure.com/)
2. Inicia sesión con tu cuenta de Microsoft
3. Busca "Azure Active Directory" o "Microsoft Entra ID"
4. En el menú lateral, selecciona **"App registrations"** (Registros de aplicaciones)
5. Haz clic en **"+ New registration"** (Nuevo registro)

### Configuración del Registro:

- **Name**: BrainRush (o el nombre que prefieras)
- **Supported account types**: Selecciona una de estas opciones:
  - **Accounts in this organizational directory only** - Solo para tu organización (recomendado para uso institucional)
  - **Accounts in any organizational directory** - Para cualquier organización con Azure AD
  - **Accounts in any organizational directory and personal Microsoft accounts** - Para uso general (recomendado si usas cuentas personales)
- **Redirect URI**: 
  - Tipo: **Web**
  - URI: `http://localhost:8081/auth/onedrive/callback`
  - (Cambia el puerto si tu aplicación Flask usa otro puerto)

6. Haz clic en **"Register"**

## Paso 2: Configurar Permisos de API

1. En la página de tu aplicación registrada, ve a **"API permissions"** (Permisos de API)
2. Haz clic en **"+ Add a permission"** (Agregar un permiso)
3. Selecciona **"Microsoft Graph"**
4. Selecciona **"Delegated permissions"** (Permisos delegados)
5. Busca y agrega los siguientes permisos:
   - `Files.ReadWrite` - Para leer y escribir archivos en OneDrive
   - `User.Read` - Para leer información básica del perfil del usuario
6. Haz clic en **"Add permissions"**
7. **IMPORTANTE**: Haz clic en **"Grant admin consent for [tu organización]"** si tienes permisos de administrador

## Paso 3: Crear un Client Secret

1. En la página de tu aplicación, ve a **"Certificates & secrets"** (Certificados y secretos)
2. En la sección **"Client secrets"**, haz clic en **"+ New client secret"**
3. Agrega una descripción (ej: "BrainRush Production")
4. Selecciona una expiración (recomendado: 24 meses)
5. Haz clic en **"Add"**
6. **¡IMPORTANTE!**: Copia el **Value** (valor) del secreto INMEDIATAMENTE
   - Este valor solo se muestra una vez
   - Si lo pierdes, tendrás que crear un nuevo secreto

## Paso 4: Obtener las Credenciales

En la página **"Overview"** de tu aplicación, encontrarás:

- **Application (client) ID**: Un GUID como `12345678-1234-1234-1234-123456789012`
- **Directory (tenant) ID**: Otro GUID (o usa `common` para cuentas personales)

## Paso 5: Configurar Variables de Entorno

Crea o edita el archivo `.env` en la raíz del proyecto BrainRush y agrega:

```env
# Configuración de OneDrive
ONEDRIVE_CLIENT_ID=tu-application-client-id-aqui
ONEDRIVE_CLIENT_SECRET=tu-client-secret-value-aqui
ONEDRIVE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=http://localhost:8081/auth/onedrive/callback
```

### Notas sobre TENANT_ID:
- Usa `common` para cuentas personales de Microsoft (Outlook, Hotmail, etc.)
- Usa `organizations` para cualquier cuenta organizacional
- Usa el GUID específico del tenant para limitar a tu organización

### Ejemplo completo:
```env
ONEDRIVE_CLIENT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890
ONEDRIVE_CLIENT_SECRET=AbC123~dEf456.GhI789-JkL012
ONEDRIVE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=http://localhost:8081/auth/onedrive/callback
```

## Paso 6: Instalar Dependencias

Ejecuta el siguiente comando en la terminal:

```bash
pip install msal requests
```

## Paso 7: Actualizar la Base de Datos

Ejecuta el script SQL para agregar las columnas necesarias:

```bash
python ejecutar_sql.py agregar_onedrive_tokens.sql
```

O manualmente en tu cliente MySQL/MariaDB:

```sql
USE brain_rush;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS onedrive_access_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_refresh_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_token_expires DATETIME NULL;
```

## Paso 8: Reiniciar la Aplicación

1. Detén el servidor Flask si está corriendo
2. Reinicia con: `python main.py`

## Uso de la Exportación a OneDrive

### Primera vez (Autorización):

1. Ve a **Mis Cuestionarios** o **Resultados de Juego**
2. Haz clic en **"📁 Subir a OneDrive"**
3. Se abrirá una ventana de Microsoft pidiendo autorización
4. Inicia sesión con tu cuenta de Microsoft
5. Acepta los permisos solicitados
6. Serás redirigido de vuelta a BrainRush
7. El archivo se subirá automáticamente a tu OneDrive

### Exportaciones posteriores:

- Una vez autorizado, las exportaciones futuras se realizarán automáticamente
- Los archivos se guardarán en la carpeta **"BrainRush"** en tu OneDrive
- No necesitarás autorizar nuevamente (a menos que revoques los permisos)

## Estructura de Archivos en OneDrive

Los archivos exportados se guardarán en:
```
OneDrive/
└── BrainRush/
    ├── BrainRush_Resultados_Cuestionario1_20251027_143025.xlsx
    ├── BrainRush_Resultados_Cuestionario2_20251027_150130.xlsx
    └── ...
```

## Solución de Problemas

### Error: "Librerías de Microsoft no instaladas"
```bash
pip install msal requests
```

### Error: "La integración con OneDrive requiere configuración"
- Verifica que las variables de entorno estén configuradas correctamente
- Asegúrate de que el archivo `.env` esté en la raíz del proyecto
- Reinicia el servidor Flask

### Error: "Token de acceso expirado"
- Vuelve a exportar, se te pedirá autorizar nuevamente
- El token se refrescará automáticamente

### Error: "Error al subir archivo: 401"
- Revoca los permisos en tu cuenta de Microsoft
- Autoriza nuevamente la aplicación
- Verifica que los permisos en Azure incluyan `Files.ReadWrite`

### Error en producción (dominio diferente)
1. En Azure, ve a **"Authentication"** (Autenticación)
2. Agrega tu URL de producción como Redirect URI:
   ```
   https://tu-dominio.com/auth/onedrive/callback
   ```
3. Actualiza `ONEDRIVE_REDIRECT_URI` en el `.env` de producción

## Seguridad

- **NUNCA** subas el archivo `.env` a un repositorio público
- Agrega `.env` a tu `.gitignore`
- Los tokens se almacenan encriptados en la base de datos
- Usa HTTPS en producción para proteger los tokens en tránsito
- Revisa periódicamente los permisos en tu [cuenta de Microsoft](https://account.microsoft.com/privacy/app-access)

## Revocar Acceso

Si deseas revocar el acceso de BrainRush a tu OneDrive:

1. Ve a [Permisos de aplicaciones de Microsoft](https://account.microsoft.com/privacy/app-access)
2. Busca "BrainRush"
3. Haz clic en **"Remover estos permisos"**

## Referencias

- [Microsoft Graph API - OneDrive](https://docs.microsoft.com/en-us/graph/api/resources/onedrive)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Azure App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

## Soporte

Si encuentras problemas con la configuración, verifica:
1. Que el Client ID y Client Secret sean correctos
2. Que los Redirect URIs coincidan exactamente
3. Que los permisos estén configurados correctamente
4. Que la aplicación tenga consentimiento de administrador (si es necesario)

---

**Última actualización**: Octubre 2025
**Versión de la API**: Microsoft Graph v1.0
