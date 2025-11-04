# 🏅 GUÍA COMPLETA DEL SISTEMA DE INSIGNIAS

## 📊 Sistema de XP

### XP por Acciones
- **Respuesta Correcta**: `10 XP` (base)
- **Bonus Velocidad**: `+5 XP` (responder en menos de 3 segundos)
- **Bonus Racha**: `+3 XP` por cada respuesta consecutiva correcta
- **Victoria en Partida**: `+50 XP`

### Ejemplo de Cálculo
```
Pregunta correcta en 2.5 segundos con racha de 3:
- Base: 10 XP
- Velocidad: +5 XP
- Racha (3): +9 XP
- TOTAL: 24 XP
```

### Sistema de Niveles
- Fórmula: `XP_necesario = 100 × nivel^1.5`
- Nivel 1 → 2: 100 XP
- Nivel 2 → 3: 282 XP
- Nivel 3 → 4: 519 XP
- Nivel 4 → 5: 800 XP

---

## 🏆 INSIGNIAS AUTOMÁTICAS (Se desbloquean jugando)

Estas insignias se otorgan **automáticamente** cuando cumples los requisitos:

### 📈 Insignias de Nivel
| Insignia | Requisito | Recompensa |
|----------|-----------|------------|
| Principiante | Alcanzar Nivel 5 | +5% XP |
| Intermedio | Alcanzar Nivel 10 | +8% XP |
| Avanzado | Alcanzar Nivel 15 | +10% XP |
| Experto | Alcanzar Nivel 20 | +12% XP |
| Maestro | Alcanzar Nivel 25 | +15% XP |
| Leyenda | Alcanzar Nivel 30 | +20% XP |

### 🎮 Insignias de Partidas
| Insignia | Requisito | Recompensa |
|----------|-----------|------------|
| Primera Victoria | Ganar 1 partida | +5% XP |
| Jugador Activo | Jugar 10 partidas | +5% XP |
| Competidor | Jugar 25 partidas | +8% XP |
| Dedicado | Jugar 50 partidas | +10% XP |
| Campeón | Ganar 20 partidas | +12% XP |
| Invicto | Ganar 50 partidas | +15% XP |

### 🔥 Insignias de Racha
| Insignia | Requisito | Recompensa |
|----------|-----------|------------|
| En Llamas | 5 respuestas correctas seguidas | +5% XP |
| Imparable | 10 respuestas correctas seguidas | +10% XP |
| Perfección | Partida completa sin errores | +15% XP |

### 🎯 Insignias de Precisión
| Insignia | Requisito | Recompensa |
|----------|-----------|------------|
| Buen Ojo | 70% de precisión general | +5% XP |
| Tirador Experto | 85% de precisión general | +10% XP |
| Perfeccionista | 95% de precisión general | +15% XP |

### ⚡ Insignias de Velocidad
| Insignia | Requisito | Recompensa |
|----------|-----------|------------|
| Rápido | Tiempo promedio < 5 segundos | +5% XP |
| Veloz | Tiempo promedio < 3 segundos | +10% XP |
| Relámpago | Tiempo promedio < 2 segundos | +15% XP |

---

## 🛒 INSIGNIAS COMPRABLES (Se compran con XP en la tienda)

Estas insignias **NO** se desbloquean jugando. Debes comprarlas en `/tienda-insignias`:

### 💎 Insignias Especiales de Tienda

| Insignia | Precio | Bonus | Rareza |
|----------|--------|-------|--------|
| Escudo Dorado 🛡️ | 3,000 XP | +15% XP | Épica |
| Estrella Brillante ✨ | 1,500 XP | +10% XP | Rara |
| Medalla de Honor 🎖️ | 2,500 XP | +12% XP | Épica |
| Rayo Velocidad ⚡ | 4,000 XP | +15% XP | Épica |
| Cerebro Gigante 🧠 | 5,000 XP | +18% XP | Épica |
| Fuego Imparable 🔥 | 8,000 XP | +20% XP | Legendaria |
| Corona Real 👑 | 10,000 XP | +25% XP | Legendaria |
| Trofeo de Campeón 🏆 | 15,000 XP | +30% XP | Legendaria |

### Cómo Comprar
1. Ve a **Dashboard → Tienda de Insignias**
2. Verás tu XP disponible arriba
3. Haz clic en "Comprar" en la insignia que desees
4. Confirma la compra
5. ¡La insignia se agrega a tu colección!

**IMPORTANTE**: Una vez comprada, **no puedes recuperar el XP gastado**.

---

## 🔍 Cómo Ver el Progreso

### Dashboard de Estudiante
- Widget de XP muestra tu nivel y progreso actual
- Botón "Insignias" muestra cuántas tienes

### Página "Mis Insignias" (`/mis-insignias`)
- **Todas**: Muestra todas las insignias (desbloqueadas y bloqueadas)
- **Desbloqueadas**: Solo las que ya tienes
- **Bloqueadas**: Las que aún no has conseguido
- **Filtros por rareza**: Legendarias, Épicas, Raras, Comunes

### Ranking XP (`/ranking-xp`)
- Ver tu posición global
- Compararte con otros estudiantes
- Ver cuántas insignias tiene cada uno

---

## ⚙️ Detalles Técnicos

### Desbloqueo Automático
El sistema verifica automáticamente después de cada respuesta:
1. ¿Subiste de nivel? → Otorga insignia de nivel
2. ¿Completaste X partidas? → Otorga insignia de partidas
3. ¿Tu racha es récord? → Otorga insignia de racha
4. ¿Tu precisión mejoró? → Otorga insignia de precisión
5. ¿Tu velocidad mejoró? → Otorga insignia de velocidad

### Notificaciones In-Game
Cuando respondes correctamente verás:
- **Notificación XP**: "+10 XP" (con bonus si aplica)
- **Level Up**: Si subiste de nivel
- **Nueva Insignia**: Si desbloqueaste una nueva

### Bonus Acumulativo
Los bonus de XP de las insignias **SE ACUMULAN**:
- Si tienes 3 insignias con +10% cada una
- Tu bonus total es +30%
- Una respuesta de 10 XP te da 13 XP

---

## 💡 Estrategias

### Para Ganar XP Rápido
1. **Responde rápido**: +5 XP por velocidad
2. **Mantén rachas**: +3 XP por respuesta en racha
3. **Juega frecuentemente**: 50 XP por victoria
4. **Desbloquea insignias**: Bonus permanente de XP

### Para Desbloquear Todas las Insignias
1. **Juega muchas partidas**: Desbloquea insignias de partidas
2. **Sé preciso**: 95%+ precisión = +15% XP permanente
3. **Practica velocidad**: <2 seg promedio = +15% XP
4. **Ahorra XP**: Para comprar insignias legendarias

### Para Subir en el Ranking
1. Consigue todas las insignias posibles (bonus de XP)
2. Juega todos los días
3. Responde rápido y correctamente
4. Mantén rachas largas

---

## 📞 Soporte

¿No se te otorgó una insignia que deberías tener?
1. Verifica en `/mis-insignias` que no la tengas
2. Revisa tus estadísticas en el dashboard
3. Algunas insignias requieren estadísticas generales, no solo de una partida

¿No puedes comprar una insignia?
1. Verifica que tengas suficiente XP
2. Asegúrate de no tenerla ya
3. Recarga la página de la tienda

---

**¡Buena suerte desbloqueando todas las insignias!** 🚀
