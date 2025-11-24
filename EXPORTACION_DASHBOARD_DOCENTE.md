# 📊 Funcionalidades de Exportación - Dashboard Docente

## ✅ Implementación Completada

Se han implementado tres funcionalidades de exportación completas en el Dashboard del Docente:

### 1. 📊 Exportar a Excel

**Funcionalidad:** Genera un archivo Excel (.xlsx) con el ranking global de estudiantes.

**Contenido del archivo:**
- Título con nombre del docente
- Fecha y hora de generación
- Tabla con columnas:
  - Posición
  - Nombre Completo
  - Puntaje Total
  - Participaciones
  - Promedio
  - Precisión
- Top 3 resaltado con colores (Oro, Plata, Bronce)

**Uso:**
1. Haz clic en el botón "📊 Exportar a Excel"
2. El archivo se descargará automáticamente
3. Abre con Microsoft Excel, Google Sheets o LibreOffice

**Ruta API:** `POST /api/exportar-dashboard-docente/excel`

---

### 2. 📂 Guardar en OneDrive

**Funcionalidad:** Sube el archivo Excel a OneDrive y envía un email con el enlace de acceso.

**Características:**
- Sube el archivo a la carpeta "BrainRUSH" en OneDrive
- Genera un nombre único con fecha y hora
- Envía email al docente con enlace directo
- Permite abrir el archivo inmediatamente

**Uso:**
1. Haz clic en "📂 Guardar en OneDrive"
2. Confirma la acción
3. Espera la subida (verás un mensaje de éxito)
4. Recibirás un email con el enlace
5. Opcionalmente, puedes abrir el archivo inmediatamente

**Requisitos:**
- OneDrive debe estar configurado en el sistema
- Variable de entorno `ONEDRIVE_ACCESS_TOKEN` debe estar configurada
- Ver archivo `CONFIGURACION_ONEDRIVE_PRODUCCION.md` para más detalles

**Ruta API:** `POST /api/exportar-dashboard-docente/onedrive`

---

### 3. 📄 Generar Reporte PDF

**Funcionalidad:** Genera un reporte PDF profesional con estadísticas completas.

**Contenido del reporte:**
- Encabezado con logo y título
- Información del docente
- Estadísticas generales:
  - Cuestionarios creados
  - Cuestionarios activos
  - Estudiantes participantes
  - Promedio general
- Ranking Global (Top 20):
  - Posición
  - Nombre
  - Puntaje
  - Partidas
  - Promedio
  - Precisión
- Top 3 resaltado con colores

**Uso:**
1. Haz clic en "📄 Generar Reporte PDF"
2. El PDF se generará y descargará automáticamente
3. Abre con cualquier lector de PDF

**Ruta API:** `POST /api/exportar-dashboard-docente/pdf`

---

## 🔧 Configuración Técnica

### Librerías Instaladas

```bash
openpyxl==3.1.2      # Para generar archivos Excel
reportlab==4.0.7     # Para generar archivos PDF
pillow==12.0.0       # Dependencia de reportlab para imágenes
msal==1.26.0         # Para integración con OneDrive
requests==2.31.0     # Para llamadas HTTP
```

### Instalación

Si necesitas instalar las librerías manualmente:

```bash
cd C:\Users\laboratorio_computo\Documents\GitHub\brain_rush
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎯 Uso en el Dashboard

### Ubicación

Los botones de exportación se encuentran en el **Dashboard Docente** en la sección "Exportar Resultados" al final de la página.

### Acceso

1. Inicia sesión como docente
2. Ve al Dashboard (automático al iniciar sesión)
3. Desplázate hasta la sección "Exportar Resultados"
4. Haz clic en el botón que desees:
   - **Exportar a Excel** → Descarga inmediata
   - **Guardar en OneDrive** → Sube a la nube y envía email
   - **Generar Reporte PDF** → Descarga reporte profesional

---

## 🔐 Seguridad

- ✅ Todas las rutas requieren autenticación (`@login_required`)
- ✅ Solo docentes pueden acceder (`@docente_required`)
- ✅ Validación de sesión en todas las operaciones
- ✅ Los archivos se generan en memoria (no se guardan en el servidor)
- ✅ Los nombres de archivo incluyen timestamp para evitar conflictos

---

## 📝 Notas Adicionales

### Excel
- Compatible con Microsoft Excel 2007+
- Compatible con Google Sheets
- Compatible con LibreOffice Calc

### PDF
- Formato A4
- Diseño profesional con colores corporativos
- Optimizado para impresión
- Incluye tabla con datos del ranking

### OneDrive
- Requiere configuración previa de Azure AD
- El archivo se guarda en la carpeta "BrainRUSH"
- El enlace de acceso es permanente
- Se puede compartir el enlace con otros usuarios

---

## ⚠️ Solución de Problemas

### Error: "Librería openpyxl no instalada"
**Solución:**
```bash
pip install openpyxl==3.1.2
```

### Error: "Librería reportlab no instalada"
**Solución:**
```bash
pip install reportlab==4.0.7
```

### Error: "OneDrive no está configurado"
**Solución:**
- Revisa el archivo `CONFIGURACION_ONEDRIVE_PRODUCCION.md`
- Configura las variables de entorno necesarias
- Autoriza la aplicación en Azure AD

### Error: "No hay datos de ranking"
**Solución:**
- Asegúrate de que los estudiantes hayan completado al menos un cuestionario
- Verifica que los cuestionarios estén publicados
- Revisa que haya salas finalizadas

---

## 🚀 Mejoras Futuras Sugeridas

1. **Gráficos en PDF:** Agregar gráficos de rendimiento
2. **Filtros de Fecha:** Exportar datos de un rango específico
3. **Comparativas:** Comparar rendimiento entre cuestionarios
4. **Exportación Automática:** Programar exportaciones periódicas
5. **Múltiples Formatos:** Agregar CSV, JSON

---

## 📧 Soporte

Si encuentras algún problema o tienes sugerencias, contacta al equipo de desarrollo.

**Versión:** 1.0  
**Fecha:** 24 de noviembre de 2025  
**Sistema:** Brain RUSH - Plataforma de Evaluación Gamificada
