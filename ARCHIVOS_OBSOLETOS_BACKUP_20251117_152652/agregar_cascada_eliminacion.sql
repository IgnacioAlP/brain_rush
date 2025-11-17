-- ========================================
-- AGREGAR ON DELETE CASCADE A FOREIGN KEYS
-- ========================================

USE brain_rush;

-- Primero eliminar las foreign keys existentes sin CASCADE
-- y volver a crearlas con CASCADE

-- ==================== PARTICIPACIONES ====================
ALTER TABLE participaciones
    DROP FOREIGN KEY IF EXISTS FK_participaciones_id_estudiante,
    DROP FOREIGN KEY IF EXISTS FK_participaciones_id_cuestionario;

ALTER TABLE participaciones
    ADD CONSTRAINT FK_participaciones_id_estudiante 
        FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    ADD CONSTRAINT FK_participaciones_id_cuestionario 
        FOREIGN KEY (id_cuestionario) REFERENCES cuestionarios(id_cuestionario) ON DELETE CASCADE;

-- ==================== RANKING ====================
ALTER TABLE ranking
    DROP FOREIGN KEY IF EXISTS FK_ranking_id_estudiante,
    DROP FOREIGN KEY IF EXISTS FK_ranking_id_cuestionario;

ALTER TABLE ranking
    ADD CONSTRAINT FK_ranking_id_estudiante 
        FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    ADD CONSTRAINT FK_ranking_id_cuestionario 
        FOREIGN KEY (id_cuestionario) REFERENCES cuestionarios(id_cuestionario) ON DELETE CASCADE;

-- ==================== RECOMPENSAS OTORGADAS ====================
ALTER TABLE recompensas_otorgadas
    DROP FOREIGN KEY IF EXISTS FK_recompensas_otorgadas_id_estudiante,
    DROP FOREIGN KEY IF EXISTS FK_recompensas_otorgadas_id_recompensa;

ALTER TABLE recompensas_otorgadas
    ADD CONSTRAINT FK_recompensas_otorgadas_id_estudiante 
        FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    ADD CONSTRAINT FK_recompensas_otorgadas_id_recompensa 
        FOREIGN KEY (id_recompensa) REFERENCES recompensas(id_recompensa) ON DELETE CASCADE;

-- ==================== RESPUESTAS ESTUDIANTES ====================
ALTER TABLE respuestas_estudiantes
    DROP FOREIGN KEY IF EXISTS FK_respuestas_estudiantes_id_estudiante,
    DROP FOREIGN KEY IF EXISTS FK_respuestas_estudiantes_id_cuestionario_pregunta,
    DROP FOREIGN KEY IF EXISTS FK_respuestas_estudiantes_id_opcion_seleccionada;

ALTER TABLE respuestas_estudiantes
    ADD CONSTRAINT FK_respuestas_estudiantes_id_estudiante 
        FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    ADD CONSTRAINT FK_respuestas_estudiantes_id_cuestionario_pregunta 
        FOREIGN KEY (id_cuestionario_pregunta) REFERENCES cuestionario_preguntas(id_cuestionario_pregunta) ON DELETE CASCADE,
    ADD CONSTRAINT FK_respuestas_estudiantes_id_opcion_seleccionada 
        FOREIGN KEY (id_opcion_seleccionada) REFERENCES opciones_respuesta(id_opcion) ON DELETE SET NULL;

-- ==================== CUESTIONARIOS ====================
-- Mantener SET NULL para docentes (no eliminar cuestionarios cuando se borra un docente)
ALTER TABLE cuestionarios
    DROP FOREIGN KEY IF EXISTS FK_cuestionarios_id_docente;

ALTER TABLE cuestionarios
    ADD CONSTRAINT FK_cuestionarios_id_docente 
        FOREIGN KEY (id_docente) REFERENCES usuarios(id_usuario) ON DELETE SET NULL;

-- ==================== TABLAS DEL SISTEMA DE JUEGO ====================
-- Verificar si existen estas tablas antes de modificarlas

-- SALAS DE JUEGO
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'salas_juego');

-- Solo ejecutar si la tabla existe
SET @sql_salas = IF(@table_exists > 0,
    'ALTER TABLE salas_juego
        DROP FOREIGN KEY IF EXISTS FK_salas_juego_id_cuestionario,
        DROP FOREIGN KEY IF EXISTS FK_salas_juego_id_docente;
     ALTER TABLE salas_juego
        ADD CONSTRAINT FK_salas_juego_id_cuestionario 
            FOREIGN KEY (id_cuestionario) REFERENCES cuestionarios(id_cuestionario) ON DELETE CASCADE,
        ADD CONSTRAINT FK_salas_juego_id_docente 
            FOREIGN KEY (id_docente) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;',
    'SELECT "Tabla salas_juego no existe" as mensaje');

PREPARE stmt FROM @sql_salas;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- PARTICIPANTES SALA
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'participantes_sala');

SET @sql_participantes = IF(@table_exists > 0,
    'ALTER TABLE participantes_sala
        DROP FOREIGN KEY IF EXISTS FK_participantes_sala_id_sala,
        DROP FOREIGN KEY IF EXISTS FK_participantes_sala_id_usuario;
     ALTER TABLE participantes_sala
        ADD CONSTRAINT FK_participantes_sala_id_sala 
            FOREIGN KEY (id_sala) REFERENCES salas_juego(id_sala) ON DELETE CASCADE,
        ADD CONSTRAINT FK_participantes_sala_id_usuario 
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;',
    'SELECT "Tabla participantes_sala no existe" as mensaje');

PREPARE stmt FROM @sql_participantes;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- RANKING SALA
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'ranking_sala');

SET @sql_ranking_sala = IF(@table_exists > 0,
    'ALTER TABLE ranking_sala
        DROP FOREIGN KEY IF EXISTS FK_ranking_sala_id_participante,
        DROP FOREIGN KEY IF EXISTS FK_ranking_sala_id_sala;
     ALTER TABLE ranking_sala
        ADD CONSTRAINT FK_ranking_sala_id_participante 
            FOREIGN KEY (id_participante) REFERENCES participantes_sala(id_participante) ON DELETE CASCADE,
        ADD CONSTRAINT FK_ranking_sala_id_sala 
            FOREIGN KEY (id_sala) REFERENCES salas_juego(id_sala) ON DELETE CASCADE;',
    'SELECT "Tabla ranking_sala no existe" as mensaje');

PREPARE stmt FROM @sql_ranking_sala;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ESTADO JUEGO SALA
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'estado_juego_sala');

SET @sql_estado = IF(@table_exists > 0,
    'ALTER TABLE estado_juego_sala
        DROP FOREIGN KEY IF EXISTS FK_estado_juego_sala_id_sala;
     ALTER TABLE estado_juego_sala
        ADD CONSTRAINT FK_estado_juego_sala_id_sala 
            FOREIGN KEY (id_sala) REFERENCES salas_juego(id_sala) ON DELETE CASCADE;',
    'SELECT "Tabla estado_juego_sala no existe" as mensaje');

PREPARE stmt FROM @sql_estado;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- RESPUESTAS PARTICIPANTES
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'respuestas_participantes');

SET @sql_respuestas = IF(@table_exists > 0,
    'ALTER TABLE respuestas_participantes
        DROP FOREIGN KEY IF EXISTS FK_respuestas_participantes_id_participante,
        DROP FOREIGN KEY IF EXISTS FK_respuestas_participantes_id_sala,
        DROP FOREIGN KEY IF EXISTS FK_respuestas_participantes_id_pregunta,
        DROP FOREIGN KEY IF EXISTS FK_respuestas_participantes_id_opcion;
     ALTER TABLE respuestas_participantes
        ADD CONSTRAINT FK_respuestas_participantes_id_participante 
            FOREIGN KEY (id_participante) REFERENCES participantes_sala(id_participante) ON DELETE CASCADE,
        ADD CONSTRAINT FK_respuestas_participantes_id_sala 
            FOREIGN KEY (id_sala) REFERENCES salas_juego(id_sala) ON DELETE CASCADE,
        ADD CONSTRAINT FK_respuestas_participantes_id_pregunta 
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE,
        ADD CONSTRAINT FK_respuestas_participantes_id_opcion 
            FOREIGN KEY (id_opcion) REFERENCES opciones_respuesta(id_opcion) ON DELETE CASCADE;',
    'SELECT "Tabla respuestas_participantes no existe" as mensaje');

PREPARE stmt FROM @sql_respuestas;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- COMPRAS INSIGNIAS
SET @table_exists = (SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'brain_rush' AND table_name = 'compras_insignias');

SET @sql_compras = IF(@table_exists > 0,
    'ALTER TABLE compras_insignias
        DROP FOREIGN KEY IF EXISTS FK_compras_insignias_id_usuario,
        DROP FOREIGN KEY IF EXISTS FK_compras_insignias_id_insignia;
     ALTER TABLE compras_insignias
        ADD CONSTRAINT FK_compras_insignias_id_usuario 
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
        ADD CONSTRAINT FK_compras_insignias_id_insignia 
            FOREIGN KEY (id_insignia) REFERENCES insignias_catalogo(id_insignia) ON DELETE CASCADE;',
    'SELECT "Tabla compras_insignias no existe" as mensaje');

PREPARE stmt FROM @sql_compras;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ========================================
-- VERIFICACIÓN FINAL
-- ========================================
SELECT 'ON DELETE CASCADE agregado exitosamente a todas las foreign keys' as resultado;

-- Mostrar todas las foreign keys con sus opciones de DELETE
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    DELETE_RULE,
    UPDATE_RULE
FROM information_schema.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'brain_rush'
ORDER BY TABLE_NAME, CONSTRAINT_NAME;
