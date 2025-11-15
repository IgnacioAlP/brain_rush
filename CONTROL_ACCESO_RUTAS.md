# CONTROL DE ACCESO - RUTAS PROTEGIDAS CON @docente_required

## ✅ RUTAS YA PROTEGIDAS (Aplicadas en esta sesión)

### Dashboards
- `/estudiante` → @estudiante_required ✅
- `/docente` → @docente_required ✅  
- `/admin` → @admin_required ✅ (ya existía)

### Cuestionarios
- `/crear-cuestionario` → @docente_required ✅
- `/mis-cuestionarios` → @docente_required ✅
- `/editar-cuestionario/<int:cuestionario_id>` → @docente_required ✅
- `/eliminar-cuestionario/<int:cuestionario_id>` → requiere verificación manual dentro del código

### Salas
- `/crear-sala` → @docente_required ✅
- `/mis-salas` → @docente_required ✅
- `/monitorear-sala/<int:sala_id>` → @docente_required ✅
- `/sala/<int:sala_id>/iniciar` → @docente_required ✅
- `/sala/<int:sala_id>/finalizar` → @docente_required ✅

## ⚠️ RUTAS QUE AÚN NECESITAN PROTECCIÓN

### Preguntas (requieren @docente_required o @login_required + verificación)
- `/agregar-preguntas/<int:cuestionario_id>` → tiene verificación manual
- `/crear-pregunta/<int:cuestionario_id>` 
- `/editar-pregunta/<int:pregunta_id>`
- `/pregunta/<int:pregunta_id>/eliminar`
- `/pregunta/<int:pregunta_id>/obtener`
- `/pregunta/<int:pregunta_id>/editar`
- `/cuestionario/<int:id_cuestionario>/importar-preguntas` → @login_required ✅
- `/cuestionario/<int:id_cuestionario>/descargar-plantilla` → @login_required ✅
- `/cuestionario/<int:cuestionario_id>/agregar-pregunta` → @login_required ✅

### Salas (más rutas)
- `/crear-sala-cuestionario/<int:cuestionario_id>`
- `/sala/<int:sala_id>/configurar-grupos`
- `/sala/<int:sala_id>/cerrar`
- `/sala/<int:sala_id>/detalle-respuestas` 

### Publicación de Cuestionarios
- `/publicar-cuestionario/<int:cuestionario_id>` → tiene verificación manual
- `/despublicar-cuestionario/<int:cuestionario_id>` → @login_required ✅

### Monitoreo y Reportes (ya tienen @admin_required)
- `/monitoreo/salas` → @admin_required ✅
- `/reportes/sistema` → @admin_required ✅
- `/configuracion/sistema` → @admin_required ✅

### Gestión de Recompensas
- `/gestionar_recompensas/<int:id_cuestionario>` → sin protección
- `/api/recompensas/<int:id_cuestionario>` → sin protección
- `/insertar_recompensa` → sin protección

### Exportación
- `/api/exportar-resultados/<int:sala_id>/excel` → sin protección
- `/api/exportar-resultados/<int:sala_id>/onedrive` → sin protección

## 🔄 RUTAS QUE DEBEN SER ACCESIBLES PARA AMBOS (estudiantes y docentes)

### Juego
- `/sala/<int:sala_id>/juego` → acceso según rol
- `/api/sala/<int:sala_id>/pregunta-actual` → acceso según rol
- `/api/sala/<int:sala_id>/responder` → solo estudiantes
- `/api/sala/<int:sala_id>/siguiente-pregunta` → docente o estudiante en modo individual
- `/api/sala/<int:sala_id>/ranking` → ambos
- `/sala/<int:sala_id>/resultados` → ambos

### Unirse a Sala
- `/sala/<string:codigo>/unirse` → estudiantes
- `/unirse_a_sala` → estudiantes

## 📝 RECOMENDACIONES

1. **Verificación Manual**: Algunas rutas tienen verificación manual dentro del código en lugar de decoradores. Es mejor usar decoradores para consistencia.

2. **API Routes**: Las rutas `/api/*` que modifican datos deben tener @jwt_or_session_required y verificación de tipo de usuario.

3. **Rutas de Juego**: Las rutas relacionadas con el juego en tiempo real necesitan lógica especial:
   - Docentes: acceso completo a monitoreo
   - Estudiantes: solo acceso a responder preguntas y ver resultados

4. **Consolidación**: Considera consolidar las verificaciones manuales `if session.get('usuario_tipo') != 'docente':` en decoradores para mayor mantenibilidad.

## 🚀 PRÓXIMOS PASOS

1. Aplicar @docente_required a las rutas de preguntas que faltan
2. Proteger rutas de gestión de recompensas  
3. Proteger rutas de exportación
4. Revisar rutas de juego para asegurar acceso correcto según rol
5. Probar exhaustivamente el acceso con usuarios estudiante y docente

## 🧪 SCRIPT DE PRUEBA

Ejecutar `test_control_acceso.py` para verificar que:
- Estudiantes NO pueden acceder a rutas de docente
- Docentes NO pueden acceder a rutas de estudiante  
- Ambos tipos pueden acceder a rutas compartidas
