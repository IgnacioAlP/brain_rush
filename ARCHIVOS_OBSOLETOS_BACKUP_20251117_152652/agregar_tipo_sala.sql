-- Script para agregar el campo tipo_sala a la tabla salas_juego
-- Este campo diferencia entre salas creadas por docentes y juegos individuales

-- Agregar columna tipo_sala si no existe
ALTER TABLE salas_juego 
ADD COLUMN IF NOT EXISTS tipo_sala ENUM('docente', 'individual') DEFAULT 'docente' 
COMMENT 'Tipo de sala: docente (control manual) o individual (automático)';

-- Actualizar salas existentes basándose en si tienen id_docente
UPDATE salas_juego 
SET tipo_sala = IF(id_docente IS NOT NULL, 'docente', 'individual')
WHERE tipo_sala IS NULL;

-- Ver resultado
SELECT id_sala, pin_sala, tipo_sala, modo_juego, estado FROM salas_juego LIMIT 10;
