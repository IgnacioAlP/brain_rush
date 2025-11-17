# 🏆 Sistema de Recompensas Automáticas - Brain RUSH

## Descripción General

El sistema de recompensas automáticas asigna reconocimientos a los 3 primeros puestos cuando finaliza un cuestionario/juego. Las recompensas se asignan basándose en las configuraciones previas del cuestionario.

## 📋 Funcionamiento

### 1. **Configuración Previa**
Antes de crear una sala de juego, el docente debe:
- Ir a "Gestionar Recompensas" en el cuestionario
- Configurar 3 recompensas con tipos:
  - **Trofeo** 🏆 → Para el 1er lugar
  - **Medalla** 🥇 → Para el 2do lugar
  - **Insignia** 🎖️ → Para el 3er lugar

### 2. **Asignación Automática**
Cuando el docente finaliza el juego:
1. El sistema calcula el ranking final
2. Identifica los 3 primeros puestos
3. Busca las recompensas configuradas para ese cuestionario
4. Asigna automáticamente:
   - **Posición 1** → Recompensa tipo "trofeo"
   - **Posición 2** → Recompensa tipo "medalla"
   - **Posición 3** → Recompensa tipo "insignia"

### 3. **Visualización**
Las recompensas otorgadas se muestran:
- ✅ En la pantalla de resultados del juego
- ✅ En el perfil del estudiante ("Mis Recompensas")
- ✅ Con animaciones y diseño atractivo

## 🔧 Implementación Técnica

### Archivos Modificados

1. **`controladores/controlador_recompensas.py`**
   - Nueva función: `asignar_recompensas_top3(sala_id)`
   - Lógica de asignación automática
   - Validaciones para evitar duplicados

2. **`controladores/controlador_juego.py`**
   - Función `finalizar_juego_sala()` actualizada
   - Llama automáticamente a `asignar_recompensas_top3()`
   - Manejo de errores no críticos

3. **`main.py`**
   - Ruta `/sala/<id>/resultados` actualizada
   - Incluye consulta de recompensas otorgadas
   - Pasa datos a la plantilla

4. **`Templates/ResultadosJuego.html`**
   - Nueva sección: "🏆 Recompensas Obtenidas"
   - Tarjetas con animaciones (oro, plata, bronce)
   - Diseño responsive

### Base de Datos

**Migración ejecutada:**
```sql
ALTER TABLE `recompensas` 
ADD COLUMN `id_cuestionario` INT NULL,
ADD CONSTRAINT `FK_recompensas_cuestionario` 
FOREIGN KEY (`id_cuestionario`) 
REFERENCES `cuestionarios` (`id_cuestionario`) 
ON DELETE CASCADE;
```

**Scripts creados:**
- `agregar_cuestionario_recompensas.sql` → Script SQL de migración
- `ejecutar_migracion_recompensas.py` → Script Python para ejecutar migración

## 📊 Flujo de Datos

```
1. Docente crea cuestionario
   ↓
2. Docente configura 3 recompensas (trofeo, medalla, insignia)
   ↓
3. Docente crea sala de juego
   ↓
4. Estudiantes juegan
   ↓
5. Docente finaliza juego
   ↓
6. Sistema calcula ranking
   ↓
7. Sistema asigna recompensas automáticamente
   ↓
8. Pantalla de resultados muestra recompensas
   ↓
9. Estudiantes ven recompensas en su perfil
```

## 🎯 Criterios de Asignación

### Orden de Prioridad
El sistema asigna recompensas en este orden:
1. **Tipo de recompensa** (trofeo > medalla > insignia)
2. **Puntos requeridos** (mayor a menor)

### Validaciones
- ✅ Solo se asignan a participantes con usuario registrado (`id_usuario IS NOT NULL`)
- ✅ No se asignan recompensas duplicadas al mismo usuario
- ✅ Si no hay 3 recompensas configuradas, asigna las disponibles
- ✅ Si hay menos de 3 participantes, asigna solo las correspondientes

## 🚀 Ejemplo de Uso

### Paso 1: Configurar Recompensas
```
Cuestionario: "Matemáticas - Álgebra"

Recompensa 1:
  Nombre: "Maestro del Álgebra"
  Tipo: trofeo
  Puntos: 1000

Recompensa 2:
  Nombre: "Experto en Ecuaciones"
  Tipo: medalla
  Puntos: 800

Recompensa 3:
  Nombre: "Aprendiz Destacado"
  Tipo: insignia
  Puntos: 600
```

### Paso 2: Crear Sala y Jugar
```
PIN: 123456
Participantes: 8 estudiantes
Preguntas: 10
```

### Paso 3: Resultados
```
🥇 1er Lugar: Juan Pérez (1500 pts) → "Maestro del Álgebra" 🏆
🥈 2do Lugar: María López (1200 pts) → "Experto en Ecuaciones" 🥇
🥉 3er Lugar: Pedro García (900 pts) → "Aprendiz Destacado" 🎖️
```

## 🎨 Diseño Visual

### Tarjetas de Recompensas
- **Primer Lugar**: Fondo dorado con gradiente (#FFD700 → #FFA500)
- **Segundo Lugar**: Fondo plateado con gradiente (#C0C0C0 → #A8A8A8)
- **Tercer Lugar**: Fondo bronce con gradiente (#CD7F32 → #B8733E)

### Animaciones
- Efecto shimmer (brillo giratorio)
- Bounce en los iconos
- Hover con elevación (translateY)

## 📝 Notas Importantes

1. **Configuración Obligatoria**: Las recompensas deben configurarse ANTES de crear la sala
2. **No Retroactivo**: No se asignan recompensas a juegos ya finalizados
3. **Error No Crítico**: Si falla la asignación, el juego se finaliza igualmente
4. **Logs Detallados**: Todos los eventos se registran en consola

## 🔍 Debugging

### Ver Logs
Al finalizar un juego, revisar la consola del servidor para:
```
✅ Juego finalizado para sala 123
🏆 Recompensas asignadas: 3
   - Juan Pérez: Maestro del Álgebra (trofeo)
   - María López: Experto en Ecuaciones (medalla)
   - Pedro García: Aprendiz Destacado (insignia)
```

### Errores Comunes
```
⚠️ No hay recompensas configuradas para el cuestionario X
⚠️ No hay participantes con usuarios registrados
⚠️ Usuario ya tiene la recompensa 'Nombre'
```

## 🚀 Mejoras Futuras

- [ ] Notificaciones push al recibir recompensa
- [ ] Envío de email con la recompensa
- [ ] Recompensas personalizadas por pregunta
- [ ] Sistema de puntos acumulables
- [ ] Ranking histórico global
- [ ] Exportar recompensas a PDF

---

**Última actualización**: Octubre 2025
**Versión**: 1.0.0
