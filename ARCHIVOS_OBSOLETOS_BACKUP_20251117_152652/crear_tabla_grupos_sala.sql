-- Migration: crear tablas y campos para grupos en salas
USE brain_rush;

-- Agregar columnas a salas_juego
ALTER TABLE salas_juego
  ADD COLUMN grupos_habilitados TINYINT(1) DEFAULT 0,
  ADD COLUMN num_grupos INT DEFAULT 0;

-- Agregar columna id_grupo a participantes_sala
ALTER TABLE participantes_sala
  ADD COLUMN id_grupo INT NULL;

-- Crear tabla grupos_sala
DROP TABLE IF EXISTS grupos_sala;
CREATE TABLE grupos_sala (
  id_grupo INT NOT NULL AUTO_INCREMENT,
  id_sala INT NOT NULL,
  nombre_grupo VARCHAR(100) NOT NULL, 
  capacidad INT DEFAULT NULL,
  PRIMARY KEY (id_grupo),
  CONSTRAINT FK_grupos_sala_id_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Índice
CREATE INDEX idx_grupos_sala_id_sala ON grupos_sala (id_sala);
