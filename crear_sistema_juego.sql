-- Migración: Sistema de juego en tiempo real con puntuación
USE brain_rush;

-- Tabla para el estado del juego en cada sala
DROP TABLE IF EXISTS estado_juego_sala;
CREATE TABLE estado_juego_sala (
  id_estado INT NOT NULL AUTO_INCREMENT,
  id_sala INT NOT NULL,
  pregunta_actual INT NOT NULL DEFAULT 0,
  tiempo_inicio_pregunta DATETIME NULL,
  estado_pregunta VARCHAR(20) DEFAULT 'esperando', -- esperando, mostrando, finalizada
  PRIMARY KEY (id_estado),
  UNIQUE KEY UK_estado_sala (id_sala),
  CONSTRAINT FK_estado_juego_id_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla para respuestas de participantes en tiempo real
DROP TABLE IF EXISTS respuestas_participantes;
CREATE TABLE respuestas_participantes (
  id_respuesta_participante INT NOT NULL AUTO_INCREMENT,
  id_participante INT NOT NULL,
  id_sala INT NOT NULL,
  id_pregunta INT NOT NULL,
  id_opcion_seleccionada INT NULL,
  tiempo_respuesta DECIMAL(10,3) NOT NULL, -- Tiempo en segundos desde que se mostró la pregunta
  es_correcta TINYINT(1) DEFAULT 0,
  puntaje_obtenido INT DEFAULT 0,
  fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_respuesta_participante),
  UNIQUE KEY UK_participante_pregunta (id_participante, id_sala, id_pregunta),
  CONSTRAINT FK_respuestas_part_participante FOREIGN KEY (id_participante) REFERENCES participantes_sala (id_participante) ON DELETE CASCADE,
  CONSTRAINT FK_respuestas_part_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE,
  CONSTRAINT FK_respuestas_part_pregunta FOREIGN KEY (id_pregunta) REFERENCES preguntas (id_pregunta) ON DELETE CASCADE,
  CONSTRAINT FK_respuestas_part_opcion FOREIGN KEY (id_opcion_seleccionada) REFERENCES opciones_respuesta (id_opcion) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Índices para optimizar consultas
CREATE INDEX idx_respuestas_part_sala ON respuestas_participantes (id_sala);
CREATE INDEX idx_respuestas_part_pregunta ON respuestas_participantes (id_pregunta);
CREATE INDEX idx_respuestas_part_tiempo ON respuestas_participantes (tiempo_respuesta);

-- Tabla para el ranking de cada sala
DROP TABLE IF EXISTS ranking_sala;
CREATE TABLE ranking_sala (
  id_ranking_sala INT NOT NULL AUTO_INCREMENT,
  id_participante INT NOT NULL,
  id_sala INT NOT NULL,
  puntaje_total INT DEFAULT 0,
  respuestas_correctas INT DEFAULT 0,
  tiempo_total_respuestas DECIMAL(10,3) DEFAULT 0, -- Suma de tiempos de respuesta
  posicion INT DEFAULT NULL,
  PRIMARY KEY (id_ranking_sala),
  UNIQUE KEY UK_ranking_participante_sala (id_participante, id_sala),
  CONSTRAINT FK_ranking_sala_participante FOREIGN KEY (id_participante) REFERENCES participantes_sala (id_participante) ON DELETE CASCADE,
  CONSTRAINT FK_ranking_sala_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Índices para ranking
CREATE INDEX idx_ranking_sala_puntaje ON ranking_sala (id_sala, puntaje_total DESC, tiempo_total_respuestas ASC);

-- Agregar columnas a salas_juego si no existen
ALTER TABLE salas_juego 
  ADD COLUMN IF NOT EXISTS pregunta_actual INT DEFAULT 0,
  ADD COLUMN IF NOT EXISTS total_preguntas INT DEFAULT 0,
  ADD COLUMN IF NOT EXISTS tiempo_inicio_juego DATETIME NULL;
