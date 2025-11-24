# Sistema de Notificaciones Brain RUSH

## 📢 Descripción
Sistema de notificaciones personalizado que reemplaza `alert()`, `confirm()` y `Swal.fire()` con notificaciones consistentes con el diseño de Brain RUSH.

## 🎨 Características
- ✅ Notificaciones tipo toast (esquina superior derecha)
- ✅ Modales de confirmación elegantes
- ✅ Diálogos de éxito, error, advertencia e información
- ✅ Animaciones suaves
- ✅ Responsive
- ✅ Auto-cierre configurable
- ✅ Prevención XSS automática

## 📚 API

### Notificaciones Toast

```javascript
// Notificación simple (auto-cierre en 4 segundos)
BrainNotify.show('Mensaje', 'success'); // success, error, warning, info
BrainNotify.show('Error al cargar', 'error', 3000); // duración personalizada

// Atajos
showNotification('Guardado exitosamente', 'success');
```

### Diálogos Modales

```javascript
// Éxito
BrainNotify.success('¡Éxito!', 'El cuestionario fue publicado correctamente');
showSuccess('¡Éxito!', 'Operación completada');

// Error
BrainNotify.error('Error', 'No se pudo conectar al servidor');
showError('Error', 'Algo salió mal');

// Advertencia
BrainNotify.warning('Advertencia', 'Tienes cambios sin guardar');
showWarning('Advertencia', 'Revisa los datos');

// Información
BrainNotify.info('Información', 'El juego comenzará en 10 segundos');
showInfo('Info', 'Datos importantes');
```

### Confirmaciones

```javascript
// Confirmación simple
const resultado = await BrainNotify.confirm(
    '¿Deseas continuar con esta acción?', 
    'Confirmar'
);
if (resultado) {
    // Usuario confirmó
}

// Atajo
const confirmed = await confirmAction(
    '¿Eliminar este cuestionario?',
    '¿Estás seguro?'
);
```

## 🔄 Migración desde código existente

### Reemplazar `alert()`

**Antes:**
```javascript
alert('Operación exitosa');
alert('Error al procesar');
```

**Después:**
```javascript
showNotification('Operación exitosa', 'success');
showNotification('Error al procesar', 'error');
```

### Reemplazar `confirm()`

**Antes:**
```javascript
if (confirm('¿Eliminar este elemento?')) {
    // Eliminar
}
```

**Después:**
```javascript
const confirmed = await confirmAction('¿Eliminar este elemento?');
if (confirmed) {
    // Eliminar
}
```

### Reemplazar `Swal.fire()`

**Antes:**
```javascript
Swal.fire({
    icon: 'success',
    title: '¡Éxito!',
    text: 'Operación completada'
});
```

**Después:**
```javascript
showSuccess('¡Éxito!', 'Operación completada');
```

**Antes (confirmación):**
```javascript
const result = await Swal.fire({
    title: '¿Continuar?',
    text: 'Esta acción no se puede deshacer',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, continuar',
    cancelButtonText: 'Cancelar'
});

if (result.isConfirmed) {
    // Acción confirmada
}
```

**Después:**
```javascript
const confirmed = await confirmAction(
    'Esta acción no se puede deshacer',
    '¿Continuar?'
);

if (confirmed) {
    // Acción confirmada
}
```

## 🎯 Ejemplos prácticos

### Publicar cuestionario
```javascript
async function publicarCuestionario(id) {
    const confirmed = await confirmAction(
        '¿Estás seguro de que quieres publicar este cuestionario? Una vez publicado, los estudiantes podrán acceder a él.',
        'Confirmar publicación'
    );
    
    if (!confirmed) return;
    
    try {
        const response = await fetch(`/api/cuestionarios/${id}/publicar`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess('¡Publicado!', 'El cuestionario está ahora disponible para los estudiantes');
            // Recargar o actualizar UI
        } else {
            showError('Error', data.error || 'No se pudo publicar el cuestionario');
        }
    } catch (error) {
        showError('Error', 'Error de conexión. Intenta nuevamente.');
    }
}
```

### Exportar resultados
```javascript
async function exportarResultados() {
    showNotification('Generando archivo...', 'info');
    
    try {
        const response = await fetch('/api/exportar-resultados');
        const data = await response.json();
        
        if (data.success) {
            showSuccess('¡Exportado!', `Archivo: ${data.file_name}`);
            if (data.web_url) {
                const openFile = await confirmAction(
                    '¿Deseas abrir el archivo en OneDrive?',
                    'Archivo generado'
                );
                if (openFile) {
                    window.open(data.web_url, '_blank');
                }
            }
        } else {
            showError('Error', 'No se pudo generar el archivo');
        }
    } catch (error) {
        showError('Error', 'Error de conexión');
    }
}
```

### Manejo de errores de formulario
```javascript
document.getElementById('miFormulario').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const datos = new FormData(e.target);
    
    try {
        const response = await fetch('/api/endpoint', {
            method: 'POST',
            body: datos
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess('¡Guardado!', 'Los cambios se guardaron correctamente');
        } else {
            showWarning('Advertencia', result.message || 'Revisa los datos ingresados');
        }
    } catch (error) {
        showError('Error', 'No se pudo completar la operación');
    }
});
```

## 🎨 Personalización

Los estilos se encuentran en `static/css/notifications.css` y pueden personalizarse:

- Colores por tipo de notificación
- Duración de animaciones
- Tamaño y posición
- Bordes y sombras

## 📱 Compatibilidad

- ✅ Chrome, Firefox, Safari, Edge (últimas versiones)
- ✅ Dispositivos móviles (iOS, Android)
- ✅ Responsive design adaptativo
