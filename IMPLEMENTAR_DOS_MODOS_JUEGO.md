# IMPLEMENTACIÓN: DOS MODOS DE JUEGO

## ✅ CAMBIOS COMPLETADOS

### 1. Backend (main.py)
- ✅ Función `obtener_sala_por_id_simple()` actualizada
- ✅ Agregado campo `tiene_docente` que detecta automáticamente:
  - `true` = Sala con docente (modo manual - colaborativo)
  - `false` = Juego individual (modo automático)

### 2. Frontend (JuegoEstudiante.html)
- ✅ Agregada constante `TIENE_DOCENTE` al JavaScript
- ✅ Agregada propiedad `tieneDocente` al gameState
- ✅ Creada función `iniciarPollingPreguntaDocente()` para modo manual

## ⚠️ CAMBIOS PENDIENTES

### Archivo: Templates/JuegoEstudiante.html

Necesitas corregir manualmente la función `seleccionarRespuesta()` (línea ~646) siguiendo esta estructura:

```javascript
async function seleccionarRespuesta(idOpcion) {
  if (gameState.hasAnswered) return;
  
  gameState.hasAnswered = true;
  clearInterval(gameState.timerInterval);
  
  const tiempoRespuesta = (Date.now() - gameState.questionStartTime) / 1000;
  
  // Deshabilitar botones
  const buttons = document.querySelectorAll('.option-button');
  buttons.forEach(btn => btn.disabled = true);
  
  // Marcar selección
  const selectedButton = document.querySelector(`[data-opcion-id="${idOpcion}"]`);
  selectedButton.classList.add('selected');
  
  try {
    // Enviar respuesta al servidor
    const response = await fetch(`/api/sala/${SALA_ID}/responder`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id_pregunta: gameState.currentQuestion.id_pregunta,
        id_opcion: idOpcion,
        tiempo_respuesta: tiempoRespuesta
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      const resultado = data.resultado;
      
      // Mostrar resultado visual
      if (resultado.es_correcta) {
        selectedButton.classList.add('correct');
        gameState.correctAnswers++;
        gameState.score += resultado.puntaje_obtenido;
        document.getElementById('current-score').textContent = gameState.score;
      } else {
        selectedButton.classList.add('incorrect');
      }
      
      // Esperar feedback visual (1.5s), luego decidir según el modo
      setTimeout(async () => {
        await procesarSiguienteAccion();
      }, 1500);
    }
  } catch (error) {
    console.error('Error al enviar respuesta:', error);
    alert('Error al enviar respuesta. Intenta nuevamente.');
    buttons.forEach(btn => btn.disabled = false);
    gameState.hasAnswered = false;
    gameState.questionStartTime = Date.now();
    gameState.timerInterval = setInterval(actualizarPuntajeVisual, 100);
  }
}

// Nueva función auxiliar para procesar la siguiente acción
async function procesarSiguienteAccion() {
  try {
    if (gameState.tieneDocente) {
      // MODO MANUAL: Esperar al docente
      console.log('⏳ Esperando a que el docente avance...');
      mostrarPantallaEspera();
      document.querySelector('.waiting-screen h2').textContent = '✅ Respuesta registrada';
      document.querySelector('.waiting-screen p').textContent = 'Esperando a que el docente avance a la siguiente pregunta...';
      iniciarPollingPreguntaDocente();
    } else {
      // MODO AUTOMÁTICO: Auto-avanzar
      await avanzarModoAutomatico();
    }
  } catch (error) {
    console.error('Error en procesarSiguienteAccion:', error);
    mostrarPantallaEspera();
    if (gameState.tieneDocente) {
      iniciarPollingPreguntaDocente();
    } else {
      iniciarPollingPregunta();
    }
  }
}

// Nueva función para el modo automático
async function avanzarModoAutomatico() {
  try {
    console.log('✅ Respuesta registrada, avanzando automáticamente...');
    
    const response = await fetch(`/api/sala/${SALA_ID}/siguiente-pregunta`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    
    if (data.success) {
      if (data.hay_mas_preguntas) {
        // Hay más preguntas
        console.log('➡️ Cargando siguiente pregunta...');
        mostrarPantallaEspera();
        setTimeout(() => cargarPreguntaActual(), 500);
      } else {
        // Terminó - Mostrar resultados
        await mostrarResultadosFinales();
      }
    } else {
      console.error('Error al avanzar:', data.error);
      mostrarPantallaEspera();
      iniciarPollingPregunta();
    }
  } catch (error) {
    console.error('Error en avanzarModoAutomatico:', error);
    mostrarPantallaEspera();
    iniciarPollingPregunta();
  }
}

// Nueva función para mostrar resultados finales
async function mostrarResultadosFinales() {
  try {
    const response = await fetch(`/api/sala/${SALA_ID}/ranking`);
    const data = await response.json();
    
    if (data.success && data.ranking) {
      if (gameState.totalQuestions === 0) {
        gameState.totalQuestions = gameState.correctAnswers;
      }
      mostrarResultados(data.ranking);
    } else {
      mostrarResultados([]);
    }
  } catch (error) {
    console.error('Error al obtener ranking:', error);
    mostrarResultados([]);
  }
}
```

## 📋 PASOS PARA COMPLETAR LA IMPLEMENTACIÓN

1. **Abre:** `Templates/JuegoEstudiante.html`

2. **Busca** la función `seleccionarRespuesta` (línea ~646)

3. **Reemplaza** toda la función con el código de arriba

4. **Agrega** las nuevas funciones auxiliares después de `seleccionarRespuesta`:
   - `procesarSiguienteAccion()`
   - `avanzarModoAutomatico()`
   - `mostrarResultadosFinales()`

5. **Verifica** que la función `iniciarPollingPreguntaDocente()` ya existe (la agregué antes)

6. **Guarda** el archivo

7. **Prueba** ambos modos:
   - **Modo manual**: Crea sala como docente, inicia juego
   - **Modo automático**: Estudiante juega desde dashboard (si existe esta funcionalidad)

## 🎯 RESULTADOS ESPERADOS

### Modo Manual (Sala con Docente):
1. Estudiante responde → Espera
2. Docente presiona "Siguiente Pregunta" → Estudiante ve nueva pregunta
3. Repite hasta última pregunta
4. Docente presiona "Finalizar Juego" → Todos ven resultados

### Modo Automático (Juego Individual):
1. Estudiante responde → Auto-avanza inmediatamente
2. No espera a nadie
3. Al terminar → Muestra resultados automáticamente

## 🐛 SI HAY ERRORES

- Revisa la consola del navegador (F12)
- Verifica que no haya llaves `{}` sin cerrar
- Asegúrate de que todos los `try-catch` estén correctos
- Comprueba que las funciones auxiliares estén definidas antes de usarse
