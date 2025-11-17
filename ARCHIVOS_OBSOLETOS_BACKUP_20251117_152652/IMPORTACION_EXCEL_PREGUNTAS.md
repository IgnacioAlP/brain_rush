# 📊 Importación de Preguntas desde Excel

## 🎯 Descripción General

Esta funcionalidad permite a los docentes importar múltiples preguntas de forma masiva a un cuestionario utilizando archivos de Excel. Esto agiliza significativamente el proceso de creación de cuestionarios con muchas preguntas.

## ✨ Características

### 1. Descarga de Plantilla
- **Ubicación**: Pestaña "Preguntas" en el editor de cuestionarios
- **Formato**: Archivo Excel (.xlsx) con estructura predefinida
- **Contenido**: 
  - Encabezados con formato visual (azul)
  - Fila de instrucciones (amarillo)
  - Ejemplo de pregunta completa (verde)
  - 20 filas vacías listas para completar

### 2. Estructura de la Plantilla

| Columna | Descripción | Requerido | Ejemplo |
|---------|-------------|-----------|---------|
| **Pregunta** | Texto de la pregunta | ✅ Sí | ¿Cuál es la capital de Francia? |
| **Opción A** | Primera opción de respuesta | ✅ Sí | Madrid |
| **Opción B** | Segunda opción de respuesta | ✅ Sí | París |
| **Opción C** | Tercera opción de respuesta | ❌ Opcional | Roma |
| **Opción D** | Cuarta opción de respuesta | ❌ Opcional | Berlín |
| **Respuesta Correcta** | Letra de la opción correcta (A/B/C/D) | ✅ Sí | B |
| **Tiempo (segundos)** | Tiempo límite para responder | ✅ Sí | 30 |

### 3. Proceso de Importación
1. Click en "📥 Importar desde Excel"
2. Seleccionar archivo .xlsx o .xls
3. Validación automática de formato
4. Importación y creación de preguntas
5. Visualización de resultados (éxitos y errores)
6. Actualización automática de la lista de preguntas

## 🔧 Implementación Técnica

### Archivos Modificados

#### 1. `Templates/EditarCuestionario.html`
**Líneas añadidas**: ~100 líneas

**CSS agregado**:
```css
.import-actions {
    /* Contenedor de botones de importación */
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
}

.import-btn, .template-btn {
    /* Estilos de botones */
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.progress-modal {
    /* Modal de progreso durante importación */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    z-index: 9999;
}
```

**HTML agregado** (en pestaña de preguntas):
```html
<div class="import-actions">
    <button type="button" class="template-btn" onclick="descargarPlantillaExcel()">
        <i class="fas fa-download"></i> Descargar Plantilla Excel
    </button>
    <button type="button" class="import-btn" onclick="importarPreguntasExcel()">
        <i class="fas fa-file-import"></i> Importar desde Excel
    </button>
</div>
<input type="file" id="import-file-input" accept=".xlsx,.xls" style="display: none;">
```

**JavaScript agregado**:
```javascript
function descargarPlantillaExcel() {
    // Descarga plantilla con estructura predefinida
    const link = document.createElement('a');
    link.href = `/cuestionario/{{ cuestionario.id_cuestionario }}/descargar-plantilla`;
    link.click();
}

function importarPreguntasExcel() {
    // Abre selector de archivos
    const fileInput = document.getElementById('import-file-input');
    fileInput.click();
}

function procesarImportacionExcel(file) {
    // Envía archivo al servidor
    // Muestra progreso
    // Procesa respuesta
    // Actualiza lista de preguntas
}
```

#### 2. `main.py`
**Rutas agregadas**: 2 nuevas

**Ruta 1: Descarga de Plantilla**
```python
@app.route('/cuestionario/<int:id_cuestionario>/descargar-plantilla', methods=['GET'])
@login_required
def descargar_plantilla_excel(id_cuestionario):
    """
    Genera y descarga plantilla Excel para importar preguntas
    
    Características:
    - Validación de permisos (solo docente propietario)
    - Creación de archivo Excel con openpyxl
    - Encabezados con formato (azul, negrita, blanco)
    - Fila de instrucciones (amarillo, cursiva)
    - Ejemplo de pregunta (verde)
    - 20 filas vacías para completar
    - Anchos de columna optimizados
    
    Returns:
        - Archivo Excel descargable
        - Flash error si no hay permisos
    """
```

**Ruta 2: Importación de Preguntas**
```python
@app.route('/cuestionario/<int:id_cuestionario>/importar-preguntas', methods=['POST'])
@login_required
def importar_preguntas_excel(id_cuestionario):
    """
    Procesa archivo Excel e importa preguntas al cuestionario
    
    Validaciones:
    - Permisos de docente propietario
    - Formato de archivo (.xlsx, .xls)
    - Texto de pregunta no vacío
    - Mínimo 2 opciones (A y B)
    - Respuesta correcta válida (A/B/C/D)
    - Respuesta correcta con opción asociada
    - Tiempo entre 5 y 300 segundos
    
    Proceso:
    1. Cargar archivo Excel
    2. Iterar filas (desde fila 4)
    3. Validar datos de cada fila
    4. Crear pregunta con controlador_preguntas
    5. Crear opciones con controlador_opciones
    6. Asociar al cuestionario con orden secuencial
    7. Revertir cambios si falla algún paso
    
    Returns:
        JSON {
            success: bool,
            total_importadas: int,
            errores: [string],
            preguntas: [{id_pregunta, texto, orden}]
        }
    """
```

#### 3. `controladores/controlador_cuestionarios.py`
**Método agregado**:
```python
def asociar_pregunta(id_cuestionario, id_pregunta, orden):
    """
    Asocia una pregunta a un cuestionario con orden específico
    
    Args:
        id_cuestionario (int): ID del cuestionario
        id_pregunta (int): ID de la pregunta a asociar
        orden (int): Posición de la pregunta en el cuestionario
    
    Returns:
        bool: True si se asoció correctamente, False en caso de error
    
    Database:
        INSERT INTO cuestionario_preguntas (id_cuestionario, id_pregunta, orden)
    """
```

## 📋 Validaciones Implementadas

### Frontend (JavaScript)
1. **Tipo de archivo**: Solo .xlsx y .xls
2. **Archivo vacío**: No permitir archivos sin nombre
3. **Progreso visual**: Modal con spinner durante carga
4. **Manejo de errores**: SweetAlert2 con mensajes descriptivos

### Backend (Python)
1. **Permisos**: Verificar que usuario es docente propietario
2. **Formato Excel**: Validar extensión de archivo
3. **Por cada fila**:
   - Pregunta no vacía
   - Al menos 2 opciones (A y B obligatorias)
   - Respuesta correcta en formato A/B/C/D
   - Respuesta correcta debe corresponder a opción existente
   - Tiempo entre 5-300 segundos
4. **Transaccionalidad**: Si falla creación de opciones o asociación, se elimina la pregunta creada

## 🎨 Experiencia de Usuario

### Flujo Completo
```
1. Docente entra a editar cuestionario
   ↓
2. Va a pestaña "Preguntas"
   ↓
3. Click en "Descargar Plantilla Excel"
   ↓
4. Se descarga archivo: plantilla_preguntas_[titulo].xlsx
   ↓
5. Docente completa preguntas en Excel
   ↓
6. Guarda archivo con sus preguntas
   ↓
7. Click en "Importar desde Excel"
   ↓
8. Selecciona archivo guardado
   ↓
9. Modal muestra: "Procesando importación..."
   ↓
10. SweetAlert2 muestra resultados:
    - "✅ 15 preguntas importadas exitosamente"
    - Si hay errores: lista detallada por fila
   ↓
11. Lista de preguntas se actualiza automáticamente
```

### Mensajes de Error Posibles
- **Fila X**: "La pregunta no puede estar vacía"
- **Fila X**: "Se requieren al menos 2 opciones (A y B)"
- **Fila X**: "La respuesta correcta debe ser A, B, C o D"
- **Fila X**: "La respuesta correcta 'C' no tiene opción asociada"
- **Fila X**: "El tiempo debe estar entre 5 y 300 segundos"
- **Fila X**: "Error al crear la pregunta en la base de datos"
- **Fila X**: "Error al crear las opciones de respuesta"
- **Fila X**: "Error al asociar la pregunta al cuestionario"

## 🗄️ Base de Datos

### Tablas Involucradas
1. **preguntas**: Se insertan nuevas preguntas
2. **opciones_respuesta**: Se insertan 2-4 opciones por pregunta
3. **cuestionario_preguntas**: Se asocian preguntas al cuestionario con orden

### Integridad Referencial
- Si falla creación de opciones → se elimina la pregunta
- Si falla asociación al cuestionario → se eliminan opciones y pregunta
- Garantiza que no queden registros huérfanos

## 📦 Dependencias

### Librería Utilizada
```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
```

Ya incluida en `requirements.txt`:
```
openpyxl==3.1.2
```

## 🚀 Cómo Usar

### Para Docentes

1. **Preparar plantilla**:
   ```
   - Abrir cuestionario en modo edición
   - Ir a pestaña "Preguntas"
   - Click en "📥 Descargar Plantilla Excel"
   ```

2. **Completar preguntas**:
   ```
   - Abrir archivo descargado en Excel
   - Eliminar fila de instrucciones y ejemplo (opcional)
   - Llenar preguntas siguiendo el formato
   - Guardar archivo
   ```

3. **Importar**:
   ```
   - Click en "📂 Importar desde Excel"
   - Seleccionar archivo completado
   - Esperar procesamiento
   - Revisar resultados
   ```

### Ejemplo de Archivo Excel

| Pregunta | Opción A | Opción B | Opción C | Opción D | Respuesta Correcta | Tiempo (segundos) |
|----------|----------|----------|----------|----------|-------------------|-------------------|
| ¿Cuál es la capital de Francia? | Madrid | París | Roma | Berlín | B | 30 |
| ¿Quién pintó La Mona Lisa? | Picasso | Da Vinci | Van Gogh | Dalí | B | 25 |
| ¿Cuántos continentes hay? | 5 | 6 | 7 | 8 | C | 20 |

## ⚠️ Consideraciones

### Limitaciones
- Solo formatos .xlsx y .xls (no CSV)
- Máximo 4 opciones por pregunta (A, B, C, D)
- Mínimo 2 opciones por pregunta (A y B obligatorias)
- Una sola respuesta correcta por pregunta
- Tiempo entre 5 y 300 segundos

### Recomendaciones
- No modificar estructura de encabezados de la plantilla
- Revisar ejemplos antes de completar
- Guardar copia de seguridad del archivo Excel
- Hacer pruebas con pocas preguntas primero
- Revisar mensajes de error y corregir antes de reintentar

## 🐛 Resolución de Problemas

### Problema: "No se encontraron preguntas válidas"
**Solución**: Asegúrate de empezar a escribir en la fila 4 o posterior

### Problema: "La respuesta correcta 'C' no tiene opción asociada"
**Solución**: Si pones respuesta 'C', debes llenar la columna "Opción C"

### Problema: "Error al procesar el archivo"
**Solución**: Verifica que el archivo sea .xlsx y no esté corrupto

### Problema: Preguntas duplicadas
**Solución**: Cada importación agrega nuevas preguntas; elimina duplicados manualmente

## 📊 Estadísticas de Implementación

- **Líneas de código agregadas**: ~400
- **Archivos modificados**: 3
- **Nuevas rutas**: 2
- **Nuevos métodos**: 4 (JavaScript) + 1 (Python)
- **Validaciones**: 11 diferentes
- **Tiempo de desarrollo**: ~2 horas

## ✅ Estado Actual

**Frontend**: ✅ Completo
- Botones de descarga e importación
- Selector de archivos
- Validación de tipo de archivo
- Modal de progreso
- Manejo de respuestas con SweetAlert2
- Actualización automática de lista

**Backend**: ✅ Completo
- Generación de plantilla Excel
- Procesamiento de archivo Excel
- Validaciones completas
- Creación de preguntas y opciones
- Asociación al cuestionario
- Manejo de errores por fila
- Transaccionalidad (rollback en errores)

**Base de Datos**: ✅ Compatible
- Método `asociar_pregunta` agregado
- Utiliza controladores existentes
- Mantiene integridad referencial

---

**Fecha de implementación**: Diciembre 2024
**Versión**: 1.0
**Estado**: ✅ Funcional y probado
