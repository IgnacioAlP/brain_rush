# Migración de Google Sheets a OneDrive

## Resumen de Cambios

Se ha reemplazado la integración con Google Sheets por OneDrive para exportar los resultados de BrainRush directamente a la cuenta de OneDrive del usuario.

## Archivos Creados

1. **CONFIGURAR_ONEDRIVE.md** - Guía completa de configuración paso a paso
2. **agregar_onedrive_tokens.sql** - Script SQL para agregar columnas necesarias
3. **instalar_onedrive.py** - Script para instalar dependencias automáticamente
4. **requirements_onedrive.txt** - Lista de nuevas dependencias

## Archivos Modificados

1. **main.py**:
   - Reemplazado endpoint `/api/exportar-resultados/<id>/google-sheets` por `/api/exportar-resultados/<id>/onedrive`
   - Agregado endpoint `/auth/onedrive/callback` para OAuth2
   - Implementación completa de Microsoft Graph API

2. **Templates/ResultadosJuego.html**:
   - Botón "📈 Subir a Google Sheets" → "📁 Subir a OneDrive"
   - Función `exportarGoogleSheets()` → `exportarOneDrive()`

3. **Templates/MisCuestionarios.html**:
   - Botón "Subir a Google Sheets" → "Subir a OneDrive"
   - Función `exportarGoogleSheets()` → `exportarOneDrive()`

## Instalación Rápida

### Paso 1: Instalar Dependencias

```bash
python instalar_onedrive.py
```

O manualmente:
```bash
pip install msal requests
```

### Paso 2: Actualizar Base de Datos

```bash
python ejecutar_sql.py agregar_onedrive_tokens.sql
```

O manualmente en MySQL:
```sql
USE brain_rush;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS onedrive_access_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_refresh_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_token_expires DATETIME NULL;
```

### Paso 3: Configurar Azure App

1. Ve a [Azure Portal](https://portal.azure.com/)
2. Registra una nueva aplicación
3. Configura permisos: `Files.ReadWrite` y `User.Read`
4. Crea un Client Secret
5. Copia el Application ID y el Secret

### Paso 4: Configurar Variables de Entorno

Agrega al archivo `.env`:

```env
ONEDRIVE_CLIENT_ID=tu-application-id
ONEDRIVE_CLIENT_SECRET=tu-client-secret
ONEDRIVE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=http://localhost:8081/auth/onedrive/callback
```

### Paso 5: Reiniciar Servidor

```bash
python main.py
```

## Uso

### Primera Exportación (Autorización)

1. Ve a "Mis Cuestionarios" o "Resultados de Juego"
2. Haz clic en "📁 Subir a OneDrive"
3. Autoriza el acceso cuando se te solicite
4. El archivo se subirá automáticamente

### Exportaciones Posteriores

Una vez autorizado, las exportaciones se realizan automáticamente sin necesidad de volver a autorizar.

## Estructura en OneDrive

Los archivos se guardan en:
```
OneDrive/
└── BrainRush/
    ├── BrainRush_Resultados_Cuestionario1_20251027_143025.xlsx
    ├── BrainRush_Resultados_Cuestionario2_20251027_150130.xlsx
    └── ...
```

## Características

✅ **Autenticación OAuth2**: Segura y estándar
✅ **Tokens Persistentes**: Se guardan en la base de datos
✅ **Refresh Automático**: Los tokens se renuevan automáticamente
✅ **Formato Excel**: Archivos .xlsx con formato profesional
✅ **Carpeta Dedicada**: Archivos organizados en carpeta "BrainRush"
✅ **Compatible con Cuentas**: @usat.pe, @usat.edu.pe, y cualquier cuenta Microsoft

## Diferencias con Google Sheets

| Característica | Google Sheets (Anterior) | OneDrive (Nuevo) |
|----------------|--------------------------|------------------|
| Formato | Hoja de cálculo en línea | Archivo Excel (.xlsx) |
| Ubicación | Google Drive | OneDrive |
| Autenticación | Google OAuth2 | Microsoft OAuth2 |
| Almacenamiento | Requiere cuenta Google | Requiere cuenta Microsoft |
| Compatibilidad | Institucional USAT | Institucional USAT (@usat.pe) |
| Ventajas | Edición colaborativa | Integración con Office 365 |

## Ventajas de OneDrive

1. **Integración Institucional**: Compatible con cuentas @usat.pe que usan Office 365
2. **Almacenamiento**: Incluido con cuentas educativas (1TB+)
3. **Sincronización**: Los archivos se sincronizan automáticamente con el PC
4. **Excel Nativo**: Formato compatible con Microsoft Excel
5. **Seguridad**: Autenticación robusta con Azure AD

## Solución de Problemas

### Error: "Librerías no instaladas"
```bash
pip install msal requests
```

### Error: "Requiere configuración"
Verifica el archivo `.env` y las variables de entorno.

### Error: "Token expirado"
Vuelve a exportar, se te pedirá autorizar nuevamente.

### Error 401 al subir
Revoca permisos en [account.microsoft.com](https://account.microsoft.com/privacy/app-access) y autoriza nuevamente.

## Seguridad

- Los tokens se almacenan encriptados en la base de datos
- Nunca compartas tu Client Secret
- Agrega `.env` a `.gitignore`
- Usa HTTPS en producción

## Soporte

Para más información, consulta:
- **CONFIGURAR_ONEDRIVE.md** - Guía detallada de configuración
- **Microsoft Graph API Docs**: https://docs.microsoft.com/graph
- **MSAL Python Docs**: https://msal-python.readthedocs.io/

---

**Fecha de migración**: Octubre 2025
**Versión**: Brain Rush v3.0
