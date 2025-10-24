-- Migration: Agregar columna numero_grupo a la tabla grupos_sala
USE brain_rush;

-- Agregar columna numero_grupo
ALTER TABLE grupos_sala
  ADD COLUMN numero_grupo INT NOT NULL DEFAULT 1 AFTER nombre_grupo;

-- Renombrar columna capacidad a capacidad_maxima para mayor claridad
ALTER TABLE grupos_sala
  CHANGE COLUMN capacidad capacidad_maxima INT DEFAULT NULL;

-- Crear índice compuesto para mejorar búsquedas
CREATE INDEX idx_grupos_sala_numero ON grupos_sala (id_sala, numero_grupo);
