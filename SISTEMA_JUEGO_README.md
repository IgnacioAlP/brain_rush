# Sistema de Juego en Tiempo Real - Brain RUSH 🎮

## ✅ Implementación Completada

### 📊 Base de Datos

**Nuevas Tablas Creadas:**

1. **`estado_juego_sala`** - Estado actual del juego en cada sala
   - `id_estado` (PK)
   - `id_sala` (FK → salas_juego)
   - `pregunta_actual` - Número de pregunta que se está mostrando
   - `tiempo_inicio_pregunta` - Timestamp cuando comenzó la pregunta
   - `estado_pregunta` - 'esperando', 'mostrando', 'finalizada'

2. **`respuestas_participantes`** - Respuestas en tiempo real
   - `id_respuesta_participante` (PK)
   - `id_participante` (FK → participantes_sala)
   - `id_sala` (FK → salas_juego)
   - `id_pregunta` (FK → preguntas)
   - `id_opcion_seleccionada` (FK → opciones_respuesta)
   - **`tiempo_respuesta`** - DECIMAL(10,3) - Tiempo en segundos
   - `es_correcta` - TINYINT(1)
   - **`puntaje_obtenido`** - INT - Calculado según tiempo
   - `fecha_respuesta` - DATETIME

3. **`ranking_sala`** - Ranking de cada sala
   - `id_ranking_sala` (PK)
   - `id_participante` (FK → participantes_sala)
   - `id_sala` (FK → salas_juego)
   - **`puntaje_total`** - INT - Suma de todos los puntajes
   - **`respuestas_correctas`** - INT - Cantidad de aciertos
   - **`tiempo_total_respuestas`** - DECIMAL(10,3) - Suma de tiempos
   - **`posicion`** - INT - Posición en el ranking

**Columnas Agregadas a `salas_juego`:**
- `pregunta_actual` - INT - Número de pregunta actual
- `total_preguntas` - INT - Total de preguntas del cuestionario
- `tiempo_inicio_juego` - DATETIME - Cuándo comenzó el juego

### 🎯 Sistema de Puntuación

**Fórmula Implementada:**
```python
PUNTAJE_MAXIMO = 1000
PUNTAJE_MINIMO = 10
DECREMENTO = 100 puntos cada 0.5 segundos

Puntaje = 1000 - (intervalos_de_0.5_seg × 100)
```

**Ejemplos:**
- Responde en 0.4 seg → **1000 puntos**
- Responde en 1.2 seg → **800 puntos**
- Responde en 3.0 seg → **400 puntos**
- Responde en 5.5 seg → **10 puntos** (mínimo)

### 🏆 Sistema de Ranking

**Criterios de Ordenamiento:**
1. **Puntaje Total** (DESC) - Mayor puntaje primero
2. **Tiempo Total** (ASC) - En caso de empate, el más rápido gana

**Ejemplo:**
```
Posición | Nombre      | Puntaje | Correctas | Tiempo Total
---------|-------------|---------|-----------|-------------
1        | Juan        | 8500    | 10        | 12.5 seg
2        | María       | 8500    | 10        | 15.2 seg  ← Empate resuelto por tiempo
3        | Pedro       | 7800    | 9         | 10.3 seg
```

### 🔌 API Endpoints Creados

#### 1. **Iniciar Juego**
```http
POST /sala/<sala_id>/iniciar
```
- Cambia estado de sala a 'en_juego'
- Inicializa ranking de todos los participantes
- Muestra primera pregunta

#### 2. **Obtener Pregunta Actual**
```http
GET /api/sala/<sala_id>/pregunta-actual
```
Respuesta:
```json
{
  "success": true,
  "pregunta": {
    "id_pregunta": 42,
    "enunciado": "¿Cuál es la capital de Francia?",
    "tipo": "opcion_multiple",
    "numero_pregunta": 3,
    "total_preguntas": 10,
    "opciones": [
      {"id_opcion": 1, "texto": "París"},
      {"id_opcion": 2, "texto": "Londres"},
      {"id_opcion": 3, "texto": "Berlín"},
      {"id_opcion": 4, "texto": "Madrid"}
    ],
    "tiempo_inicio": "2025-10-21 18:30:15",
    "estado": "mostrando"
  }
}
```

#### 3. **Enviar Respuesta**
```http
POST /api/sala/<sala_id>/responder
Content-Type: application/json

{
  "id_pregunta": 42,
  "id_opcion": 1,
  "tiempo_respuesta": 2.5
}
```
Respuesta:
```json
{
  "success": true,
  "resultado": {
    "es_correcta": true,
    "puntaje_obtenido": 600,
    "tiempo_respuesta": 2.5
  }
}
```

#### 4. **Avanzar a Siguiente Pregunta** (Solo Docente)
```http
POST /api/sala/<sala_id>/siguiente-pregunta
```
Respuesta:
```json
{
  "success": true,
  "hay_mas_preguntas": true,
  "message": "Siguiente pregunta"
}
```

#### 5. **Obtener Ranking**
```http
GET /api/sala/<sala_id>/ranking
```
Respuesta:
```json
{
  "success": true,
  "ranking": [
    {
      "posicion": 1,
      "nombre": "Juan Pérez",
      "puntaje": 8500,
      "correctas": 10,
      "tiempo_total": 12.5,
      "grupo": "Grupo 1"
    },
    ...
  ]
}
```

#### 6. **Estadísticas de Pregunta Actual**
```http
GET /api/sala/<sala_id>/estadisticas-pregunta
```
Respuesta:
```json
{
  "success": true,
  "estadisticas": {
    "total": 25,
    "respondieron": 18,
    "pendientes": 7
  }
}
```

### 📝 Funciones del Controlador (`controlador_juego.py`)

1. **`calcular_puntaje(tiempo_respuesta_segundos)`**
   - Calcula puntaje según tiempo de respuesta

2. **`iniciar_juego_sala(sala_id)`**
   - Inicia el juego, configura estado inicial

3. **`obtener_pregunta_actual_sala(sala_id)`**
   - Obtiene pregunta que se está mostrando

4. **`registrar_respuesta_participante(...)`**
   - Guarda respuesta y calcula puntaje

5. **`avanzar_siguiente_pregunta(sala_id)`**
   - Avanza a siguiente pregunta o finaliza juego

6. **`calcular_ranking_final(sala_id)`**
   - Calcula posiciones finales del ranking

7. **`obtener_ranking_sala(sala_id)`**
   - Obtiene ranking ordenado

8. **`obtener_estadisticas_pregunta_actual(sala_id)`**
   - Estadísticas de participación en tiempo real

### 🚀 Flujo del Juego

```
1. Docente crea sala → Estudiantes se unen
2. Docente configura grupos (opcional)
3. Docente hace clic en "Iniciar Juego"
   ↓
4. Sistema muestra primera pregunta a todos
5. Estudiantes responden (tiempo comienza a correr)
6. Sistema calcula puntaje automáticamente
   ↓
7. Docente ve estadísticas en tiempo real
8. Docente avanza a siguiente pregunta
9. Repite pasos 4-8 hasta última pregunta
   ↓
10. Sistema calcula ranking final
11. Muestra pantalla de resultados con posiciones
```

### 📋 Archivos Modificados/Creados

**Creados:**
- ✅ `controladores/controlador_juego.py` - Lógica del juego
- ✅ `migracion_sistema_juego.py` - Script de migración
- ✅ `crear_sistema_juego.sql` - SQL de tablas
- ✅ `SISTEMA_JUEGO_README.md` - Esta documentación

**Modificados:**
- ✅ `main.py` - Rutas API agregadas
- ✅ `controladores/controlador_salas.py` - Funciones de grupos

### 🎮 Próximos Pasos para Completar

**Frontend Pendiente:**

1. **MonitoreoJuego.html** (Vista Docente)
   - Botón "Iniciar Juego"
   - Mostrar pregunta actual
   - Estadísticas en tiempo real (cuántos respondieron)
   - Botón "Siguiente Pregunta"
   - Vista previa del ranking

2. **JuegoEstudiante.html** (Vista Estudiante)
   - Mostrar pregunta actual
   - Opciones de respuesta clicables
   - Timer visual (cuenta regresiva)
   - Feedback inmediato (correcto/incorrecto + puntaje)

3. **ResultadosJuego.html** (Ambos)
   - Tabla de ranking final
   - Gráficos de desempeño
   - Distribución por grupos
   - Botones de exportar resultados

### 🔧 Comandos de Instalación

**En Desarrollo Local:**
```bash
# Ejecutar migración
python migracion_sistema_juego.py

# Verificar tablas creadas
# Usar MySQL Workbench o cliente MySQL
```

**En PythonAnywhere:**
```bash
cd ~/mysite
python migracion_sistema_juego.py
```

### ⚠️ Notas Importantes

1. **Seguridad:** Las rutas de juego validan que el participante_id esté en sesión
2. **Tiempo Real:** Para actualizar UI, usar polling cada 2-3 segundos o WebSockets
3. **Concurrencia:** La tabla respuestas_participantes tiene UNIQUE KEY para evitar duplicados
4. **Performance:** Índices optimizados para consultas de ranking
5. **Grupos:** El ranking muestra el grupo de cada participante

### 📊 Ejemplo de Consulta SQL para Ranking

```sql
SELECT 
    r.posicion,
    p.nombre_participante,
    r.puntaje_total,
    r.respuestas_correctas,
    r.tiempo_total_respuestas,
    g.nombre_grupo
FROM ranking_sala r
JOIN participantes_sala p ON r.id_participante = p.id_participante
LEFT JOIN grupos_sala g ON p.id_grupo = g.id_grupo
WHERE r.id_sala = 44
ORDER BY r.puntaje_total DESC, r.tiempo_total_respuestas ASC;
```

---

## 🎉 Sistema Listo para Uso

El backend del sistema de juego está **100% funcional**. Solo falta implementar el frontend (JavaScript + HTML) para que docentes y estudiantes interactúen con el juego en tiempo real.

**Contacto:** Para dudas sobre la implementación, revisar el código en:
- `controladores/controlador_juego.py`
- Rutas en `main.py` (buscar "SISTEMA DE JUEGO EN TIEMPO REAL")
