# 🎮 Sistema de XP, Niveles e Insignias - Brain RUSH

## 📋 Descripción General

Sistema completo de gamificación para estudiantes que incluye:
- **Experiencia (XP)** por respuestas correctas
- **Niveles** con progresión exponencial
- **Insignias** desbloqueables por logros
- **Estadísticas** detalladas de juego
- **Ranking global** de XP

---

## 🚀 Instalación

### 1. Crear las Tablas en la Base de Datos

```bash
python crear_tablas_xp.py
```

Este script creará:
- ✅ `experiencia_usuarios` - XP y niveles
- ✅ `insignias_catalogo` - 23 insignias predefinidas
- ✅ `insignias_usuarios` - Insignias desbloqueadas
- ✅ `estadisticas_juego` - Stats de rendimiento
- ✅ `historial_xp` - Registro de XP ganado
- ✅ Vista `ranking_xp` - Ranking global

### 2. El Sistema ya está Integrado

El controlador de XP (`controlador_xp.py`) ya está importado en `main.py` y se ejecuta automáticamente cuando un estudiante responde preguntas.

---

## 💎 Sistema de XP

### Ganancia de XP

| Acción | XP Ganado |
|--------|-----------|
| Respuesta correcta | **20 XP** base |
| Respuesta rápida (<3s) | **+10 XP** bonus |
| Racha (por respuesta) | **+5 XP** (máx 50) |
| Victoria en partida | **+100 XP** |
| Insignia desbloqueada | Varía según rareza |
| Subir de nivel | **+50 XP** por nivel |

### Sistema de Niveles

**Fórmula**: `XP_necesario = 100 × nivel^1.5`

| Nivel | XP Necesario | XP Acumulado |
|-------|--------------|--------------|
| 1 → 2 | 100 | 0 |
| 2 → 3 | 283 | 100 |
| 3 → 4 | 520 | 383 |
| 5 → 6 | 1,118 | 1,616 |
| 10 → 11 | 3,162 | 15,000~ |
| 20 → 21 | 8,944 | 90,000~ |
| 50 → 51 | 35,355 | 1,000,000~ |

---

## 🏆 Sistema de Insignias

### 23 Insignias Predefinidas

#### 📈 Por Nivel (5 insignias)
- 🌱 **Principiante** - Nivel 5 (Bronce, +50 XP)
- 📚 **Aprendiz** - Nivel 10 (Plata, +100 XP)
- 🎓 **Conocedor** - Nivel 20 (Oro, +200 XP)
- 🏆 **Experto** - Nivel 35 (Platino, +350 XP)
- 👑 **Maestro** - Nivel 50 (Diamante, +500 XP)

#### 🎮 Por Partidas Jugadas (5 insignias)
- 🎮 **Primera Victoria** - 1 partida (+25 XP)
- 🎯 **Jugador Frecuente** - 10 partidas (+75 XP)
- ⚔️ **Veterano** - 50 partidas (+150 XP)
- 🔥 **Incansable** - 100 partidas (+300 XP)
- 💎 **Leyenda** - 250 partidas (+600 XP)

#### ⚡ Por Racha (4 insignias)
- ⚡ **En Racha** - 5 correctas seguidas (+40 XP)
- 🌟 **Imparable** - 10 correctas seguidas (+100 XP)
- ✨ **Perfeccionista** - 20 correctas seguidas (+250 XP)
- 💫 **Invencible** - 50 correctas seguidas (+500 XP)

#### 🎯 Por Precisión (4 insignias)
- 👁️ **Buen Ojo** - 70% precisión (+50 XP)
- 🎯 **Tirador Experto** - 85% precisión (+125 XP)
- 🏹 **Francotirador** - 95% precisión (+300 XP)
- 🎖️ **Perfección Absoluta** - 100% precisión (+1000 XP)

#### ⏱️ Por Velocidad (3 insignias)
- ⏱️ **Rápido** - Promedio <5s (+60 XP)
- ⚡ **Relámpago** - Promedio <3s (+150 XP)
- 🚀 **Supersónico** - Promedio <2s (+400 XP)

#### 🌟 Especiales (2 insignias)
- 🌅 **Madrugador** - Jugar antes de 6 AM (+100 XP)
- 🌙 **Noctámbulo** - Jugar después de 11 PM (+100 XP)
- 🎉 **Fin de Semana** - Jugar sábado/domingo (+75 XP)
- 🗺️ **Explorador** - Jugar 3 áreas diferentes (+200 XP)

### Rareza de Insignias

| Rareza | Color | Descripción |
|--------|-------|-------------|
| 🔵 Común | `#87CEEB` | Fácil de obtener |
| 🟣 Raro | `#C0C0C0` | Requiere esfuerzo |
| 🟠 Épico | `#FFD700` | Difícil de conseguir |
| 🔴 Legendario | `#B9F2FF` | Máxima dificultad |

---

## 📊 Estadísticas Rastreadas

El sistema rastrea automáticamente:

- ✅ Total de partidas jugadas
- ✅ Total de partidas ganadas
- ✅ Respuestas correctas/incorrectas
- ✅ Racha actual y máxima
- ✅ Precisión promedio (%)
- ✅ Tiempo promedio de respuesta
- ✅ Puntaje máximo obtenido
- ✅ Fecha de última partida

---

## 🔌 API Endpoints

### GET `/api/perfil-xp/<usuario_id>`
Obtiene perfil completo de XP de un usuario

**Response:**
```json
{
  "success": true,
  "perfil": {
    "xp_actual": 450,
    "nivel": 3,
    "xp_total": 1500,
    "xp_para_siguiente_nivel": 520,
    "porcentaje_nivel": 86.5,
    "total_insignias": 5,
    "posicion_ranking": 12,
    "estadisticas": {
      "partidas_jugadas": 15,
      "partidas_ganadas": 8,
      "respuestas_correctas": 45,
      "respuestas_incorrectas": 10,
      "racha_actual": 3,
      "racha_maxima": 12,
      "precision": 81.8,
      "tiempo_promedio": 4.2
    }
  }
}
```

### GET `/api/insignias/<usuario_id>`
Obtiene insignias desbloqueadas

### GET `/api/insignias-progreso/<usuario_id>`
Obtiene progreso hacia insignias bloqueadas

### GET `/api/ranking-xp?limite=100`
Obtiene ranking global de XP

---

## 🎨 Integración en el Frontend

### Dashboard del Estudiante

El dashboard debe mostrar:

```html
<!-- Tarjeta de XP y Nivel -->
<div class="xp-card">
  <h3>Nivel {{ perfil.nivel }}</h3>
  <div class="xp-bar">
    <div class="xp-progress" style="width: {{ perfil.porcentaje_nivel }}%"></div>
  </div>
  <p>{{ perfil.xp_actual }} / {{ perfil.xp_para_siguiente_nivel }} XP</p>
</div>

<!-- Insignias Recientes -->
<div class="insignias-preview">
  {% for insignia in insignias[:3] %}
    <div class="insignia-badge" style="background: {{ insignia.color }}">
      <span class="insignia-icon">{{ insignia.icono }}</span>
      <span class="insignia-nombre">{{ insignia.nombre }}</span>
    </div>
  {% endfor %}
</div>
```

### Notificación al Ganar XP

Cuando un estudiante responde correctamente, mostrar notificación:

```javascript
// El backend ahora devuelve xp_info en la respuesta
if (resultado.xp_info) {
  mostrarNotificacionXP(resultado.xp_info);
  
  if (resultado.xp_info.subio_nivel) {
    mostrarAnimacionSubidaNivel(resultado.xp_info);
  }
  
  if (resultado.xp_info.insignias_nuevas.length > 0) {
    mostrarInsigniasDesbloqueadas(resultado.xp_info.insignias_nuevas);
  }
}
```

---

## 🎯 Funciones del Controlador

### `otorgar_xp(id_usuario, cantidad_xp, razon, id_sala, id_pregunta)`
Otorga XP a un usuario y actualiza nivel automáticamente

### `calcular_xp_por_respuesta(tiempo_respuesta, es_correcta, racha_actual)`
Calcula XP considerando velocidad y racha

### `actualizar_estadisticas_respuesta(id_usuario, es_correcta, tiempo_respuesta)`
Actualiza estadísticas después de responder

### `verificar_y_desbloquear_insignias(id_usuario)`
Verifica requisitos y desbloquea insignias automáticamente

### `obtener_perfil_xp(id_usuario)`
Obtiene perfil completo con XP, nivel, estadísticas e insignias

### `obtener_ranking_global(limite)`
Obtiene ranking ordenado por nivel y XP

---

## 🔧 Personalización

### Ajustar XP por Respuesta

Edita las constantes en `controlador_xp.py`:

```python
XP_POR_RESPUESTA_CORRECTA = 20  # XP base
XP_POR_VICTORIA = 100           # XP por ganar
XP_BONUS_VELOCIDAD = 10         # XP por velocidad
XP_BONUS_RACHA = 5              # XP por racha
```

### Agregar Nuevas Insignias

Inserta en `insignias_catalogo`:

```sql
INSERT INTO insignias_catalogo 
(nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex)
VALUES 
('Tu Insignia', 'Descripción', '🎨', 'oro', 'nivel', 15, 150, 'raro', '#FFD700');
```

### Cambiar Fórmula de Niveles

Modifica la función `calcular_xp_para_nivel()` en `controlador_xp.py`

---

## 📝 Notas Importantes

1. **Solo Estudiantes**: El sistema XP solo se aplica a usuarios con `tipo_usuario = 'estudiante'`

2. **Automático**: El XP se otorga automáticamente al responder preguntas correctamente

3. **Insignias**: Se verifican y desbloquean automáticamente después de cada acción

4. **Persistencia**: Todo se guarda en la base de datos - no se pierde al cerrar sesión

5. **Rendimiento**: Las consultas están optimizadas con índices apropiados

---

## 🐛 Troubleshooting

### Error: "Table doesn't exist"
```bash
# Ejecutar el script de creación
python crear_tablas_xp.py
```

### XP no se otorga
- Verificar que el usuario sea estudiante
- Revisar logs en terminal: `print(f"🎯 XP otorgado...")`
- Verificar que `controlador_xp` esté importado en `main.py`

### Insignias no se desbloquean
- Verificar requisitos en `insignias_catalogo`
- Comprobar estadísticas del usuario en `estadisticas_juego`
- La función se llama automáticamente después de otorgar XP

---

## 🎉 ¡Sistema Listo!

El sistema de XP e insignias está completamente funcional. Los estudiantes ganarán XP automáticamente al:
- ✅ Responder preguntas correctamente
- ✅ Responder rápidamente
- ✅ Mantener rachas
- ✅ Completar partidas

Las insignias se desbloquean automáticamente al cumplir requisitos.

**Próximos pasos:**
1. Ejecutar `python crear_tablas_xp.py`
2. Reiniciar el servidor Flask
3. ¡Jugar y ganar XP! 🎮

---

**Desarrollado para Brain RUSH** 🧠⚡
