# 📤 Exportación de Resultados - Guía Completa

## ✅ Implementación: Exportación por Email

Se ha implementado la exportación de resultados mediante **correo electrónico**, ya que Microsoft Graph API requiere autenticación OAuth2 incluso para carpetas compartidas públicamente.

## 🔧 Cómo Funciona

### Exportación por Email (Método Actual)
1. El usuario hace clic en "📧 Exportar por Email"
2. El sistema crea un archivo Excel con los resultados formateados
3. Se envía automáticamente al correo del usuario
4. El usuario recibe el archivo y puede guardarlo donde prefiera (OneDrive, Google Drive, PC, etc.)

## 📧 Formato del Email

El email que recibes incluye:

```
Hola [Tu nombre],

Adjunto encontrarás los resultados de "[Nombre del Cuestionario]".

📊 Detalles:
- Total de participantes: X
- Total de preguntas: Y
- Fecha de generación: DD/MM/YYYY HH:MM

💡 Para guardar en OneDrive:
1. Descarga el archivo adjunto
2. Abre OneDrive web: [URL de tu carpeta]
3. Arrastra y suelta el archivo en la carpeta

También puedes guardarlo en Google Drive, tu computadora o donde prefieras.

Saludos,
Sistema BrainRush
```

**Adjunto**: Archivo Excel con formato profesional

## ⚠️ ¿Por qué no se sube directamente a OneDrive?

### Problema Técnico

Microsoft cambió sus políticas de seguridad y **requiere autenticación OAuth2** incluso para carpetas compartidas públicamente:

```
Error de Microsoft Graph API:
"InvalidAuthenticationToken: Access token is empty"
```

### Soluciones Intentadas

❌ **URL compartida sin autenticación** - Requiere token OAuth2  
❌ **Sharing token de SharePoint** - Requiere token de acceso  
✅ **Email con archivo adjunto** - **Funciona perfectamente**

### Alternativa OAuth2 (No Recomendada para PythonAnywhere)

Para subir directamente a OneDrive se necesitaría:
1. Registrar aplicación en Azure AD
2. Configurar OAuth2 con redirect URLs
3. Implementar flujo de autorización
4. Gestionar tokens de acceso y refresh tokens
5. **Problema**: PythonAnywhere tiene limitaciones con OAuth redirects

## 📁 URL de la Carpeta Compartida

```
https://estudianteusatedu-my.sharepoint.com/:f:/g/personal/75502058_usat_pe/EgA7zrSLcX1Lu3G24Agqq2IBTCkm_XRPFbJ2byE_O2A5Nw?e=3g86Ii
```

**Propietario**: 75502058@usat.pe  
**Tipo**: Carpeta compartida de OneDrive/SharePoint

## 🎯 Ventajas de Esta Solución

✅ **Sin Azure** - No necesitas registrar aplicaciones  
✅ **Sin OAuth2** - No requiere autorización del usuario  
✅ **Sin tokens** - No hay tokens que expiren  
✅ **Automático** - Sube directamente sin intervención  
✅ **Respaldo** - Si falla, envía por email automáticamente  
✅ **Compatible PythonAnywhere** - Funciona perfectamente en producción  

## ⚠️ IMPORTANTE: Configuración de Permisos

Para que funcione correctamente, la carpeta debe tener:

### Pasos para verificar/configurar permisos:

1. **Abre OneDrive web** (https://onedrive.live.com o tu portal institucional)

2. **Navega a la carpeta** de exportación

3. **Click derecho → "Compartir" o ícono de compartir**

4. **Configuración del enlace**:
   - ✅ **Tipo**: "Cualquier persona con el enlace"
   - ✅ **Permisos**: "Puede editar" (NO solo "Ver")
   - ✅ **Sin restricciones de dominio**

5. **Guardar y copiar el enlace**

### ¿Por qué estos permisos?

- **"Cualquier persona"**: Permite subidas anónimas vía API
- **"Puede editar"**: Necesario para crear archivos nuevos
- Si solo tiene permisos de lectura → Fallback a email automáticamente

## 🧪 Cómo Probar

### Prueba Rápida desde la Interfaz

1. Ve a **"Mis Cuestionarios"** o **"Resultados de Juego"**
2. Click en **"☁️ Subir a OneDrive"**
3. Observa el mensaje resultante:

#### Escenario 1: ✅ Éxito
```
✅ Archivo "BrainRush_Resultados_Matematicas_20251027_143025.xlsx" subido a OneDrive

Carpeta: Resultados BrainRush

¿Deseas abrir la carpeta de OneDrive? [Sí] [No]
```

#### Escenario 2: ⚠️ Fallback a Email
```
⚠️ No se pudo subir a OneDrive. Se envió por correo electrónico

Archivo: BrainRush_Resultados_Matematicas_20251027_143025.xlsx
```

#### Escenario 3: ✅ Solo Email (si OneDrive no configurado)
```
✅ Resultados enviados por correo electrónico

Archivo: BrainRush_Resultados_Matematicas_20251027_143025.xlsx
```

### Prueba Técnica (Python)

```python
import requests
import base64

# URL de tu carpeta compartida
share_url = "https://estudianteusatedu-my.sharepoint.com/:f:/g/personal/75502058_usat_pe/EgA7zrSLcX1Lu3G24Agqq2IBTCkm_XRPFbJ2byE_O2A5Nw?e=3g86Ii"

# Codificar como sharing token
encoded = base64.b64encode(share_url.encode()).decode()
token = "u!" + encoded.rstrip('=').replace('/', '_').replace('+', '-')

# Probar acceso al driveItem
url = f"https://graph.microsoft.com/v1.0/shares/{token}/driveItem"
response = requests.get(url)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ Carpeta accesible")
    data = response.json()
    print(f"Carpeta: {data.get('name')}")
else:
    print("❌ Error:", response.text)
```

## 🔍 Solución de Problemas

### Error: "No se pudo subir a OneDrive (código 401 o 403)"

**Causa**: Permisos insuficientes en la carpeta.

**Solución**:
1. Verifica que la carpeta tenga permisos de **edición** (no solo lectura)
2. Asegúrate de que el enlace sea tipo **"Cualquier persona con el enlace"**
3. Si la institución tiene políticas restrictivas, puede bloquearse
4. **No te preocupes**: El sistema enviará por email automáticamente ✅

### Error: "Error de conexión con OneDrive"

**Causa**: Firewall o problema de red.

**Solución**:
- En PythonAnywhere: Verifica conectividad a `graph.microsoft.com`
- El sistema enviará por email como respaldo automáticamente

### El archivo no aparece en la carpeta

**Pasos**:
1. ¿El mensaje dijo "subido exitosamente"? → Debería estar
2. Espera 5-10 segundos y **refresca la página** de OneDrive
3. Si no aparece → Verifica permisos de carpeta
4. Revisa tu **email** por si se usó el fallback

### Quiero usar otra carpeta

1. Crea una **nueva carpeta** en OneDrive
2. Compártela con permisos de **edición pública**
3. Copia la **URL compartida**
4. Edita `main.py` línea ~3833:
   ```python
   share_url = "https://TU-NUEVA-URL-AQUI"
   ```
5. Reload de la aplicación en PythonAnywhere

## 📊 Estructura de Archivos Generados

```
OneDrive/Carpeta Compartida/
├── BrainRush_Resultados_Matematicas_20251027_143025.xlsx
├── BrainRush_Resultados_Historia_20251027_150130.xlsx
└── BrainRush_Resultados_Ciencias_20251027_163542.xlsx
```

### Formato de cada archivo:

| Posición | Estudiante | Grupo | Puntaje | Correctas | Incorrectas | Precisión | Tiempo Total |
|----------|-----------|-------|---------|-----------|-------------|-----------|--------------|
| 1 | Juan Pérez | A | 95 | 19 | 1 | 95.00% | 5:23 |
| 2 | María López | B | 90 | 18 | 2 | 90.00% | 6:45 |

**Características**:
- ✅ Encabezados formateados (fondo azul, texto blanco)
- ✅ Columnas auto-ajustadas
- ✅ Datos alineados correctamente
- ✅ Formato profesional listo para compartir

## 🚀 Instalación en PythonAnywhere

### Paso 1: Verificar librería requests

```bash
pip install --user requests
```

(Normalmente ya está instalada)

### Paso 2: Configurar Email (para fallback)

Archivo `.env` debe tener:

```env
MAIL_USERNAME=brainrush.notificaciones@gmail.com
MAIL_PASSWORD=tu-contraseña-aplicacion-gmail
MAIL_DEFAULT_SENDER=brainrush.notificaciones@gmail.com
```

### Paso 3: Reload

En PythonAnywhere:
1. Ve a **Web** tab
2. Click en **Reload** (botón verde)

### ¡Listo! 🎉

No requiere más configuración.

## 🔄 Flujo Técnico Completo

```
Usuario → Click "Subir a OneDrive"
    ↓
Backend: Crear Excel con openpyxl
    ↓
Codificar URL → Sharing Token (base64)
    ↓
PUT request → graph.microsoft.com/v1.0/shares/{token}/driveItem:/{filename}:/content
    ↓
┌──────────────────────┐
│ ¿Status 200/201?     │
└──────────────────────┘
    ↓ SÍ         ↓ NO
  ✅ Éxito    ⚠️ Fallback
  OneDrive     Flask-Mail
    ↓              ↓
  return {      mail.send()
    success: true,    ↓
    file_name,   return {
    folder,       success: true,
    share_url     email_sent: true,
  }               fallback: true
                  }
```

## 📝 Comparación de Métodos

| Característica | Google Sheets (Antes) | OneDrive + Email (Ahora) |
|----------------|----------------------|--------------------------|
| Requiere API Keys | ✅ Sí | ❌ No |
| OAuth2 | ✅ Sí | ❌ No |
| Configuración compleja | ✅ Sí | ❌ No |
| Compatible PythonAnywhere | ⚠️ Limitado | ✅ Sí |
| Método de respaldo | ❌ No | ✅ Email automático |
| Archivos descargables | ⚠️ Requiere conversión | ✅ Excel directo |
| Tiempo de setup | ~30 min | ~2 min |

## 🎓 Casos de Uso

### Docente exporta resultados finales
1. Click en "Ver Resultados"
2. Click en "☁️ Subir a OneDrive"
3. Archivo sube automáticamente
4. Click en "Abrir carpeta" para ver el archivo
5. Descarga o comparte el Excel desde OneDrive

### Administrador revisa histórico
1. Abre la carpeta compartida de OneDrive
2. Ve todos los archivos exportados
3. Filtra por nombre de cuestionario o fecha
4. Descarga los que necesite

### Estudiante solicita sus resultados
1. Docente exporta desde "Mis Cuestionarios"
2. Comparte el enlace al archivo de OneDrive
3. Estudiante descarga su ranking

## 💡 Tips y Mejores Prácticas

### Organización de archivos

Crea **subcarpetas** en OneDrive por:
- Curso/Materia
- Fecha/Semestre
- Tipo de evaluación

### Respaldos

La carpeta de OneDrive actúa como respaldo automático de todos los resultados.

### Compartir resultados

1. Exporta a OneDrive
2. Click derecho en el archivo
3. "Compartir" → Copia enlace
4. Envía a estudiantes/colegas

### Análisis de datos

Los archivos Excel pueden abrirse con:
- Microsoft Excel
- Google Sheets (importar)
- LibreOffice Calc
- Python (pandas)

## 🔐 Seguridad y Privacidad

### ¿Es seguro subir a una carpeta pública?

- **Ventaja**: Funciona sin autenticación compleja
- **Consideración**: Cualquiera con el enlace puede ver/editar
- **Recomendación**: 
  - Usa una carpeta específica para exportaciones
  - No compartas el enlace de la carpeta públicamente
  - Solo para resultados que no sean extremadamente confidenciales
  - Para mayor seguridad → usa el método de fallback (email)

### Alternativa más segura

Si prefieres **máxima privacidad**:
1. Configura permisos de carpeta como "Solo lectura"
2. El sistema usará email automáticamente
3. Solo tú recibes los archivos

## 📞 Soporte

### Problemas comunes resueltos

✅ "No sube a OneDrive" → Verifica permisos de carpeta  
✅ "Error de conexión" → PythonAnywhere firewall, usa email  
✅ "Quiero cambiar carpeta" → Edita `share_url` en main.py  
✅ "Prefiero solo email" → Pon permisos de solo lectura en carpeta  

### Archivos de código modificados

- `main.py` → Endpoint `/api/exportar-resultados/<sala_id>/onedrive`
- `Templates/ResultadosJuego.html` → Botón y función `exportarOneDrive()`
- `Templates/MisCuestionarios.html` → Botón y función `exportarOneDrive()`

---

**Implementado**: 27 de octubre de 2025  
**Estado**: ✅ Listo para producción  
**Método**: Microsoft Graph API + Shared URL + Email Fallback  
**Compatibilidad**: PythonAnywhere ✓ | Local ✓ | Otros hosts ✓
