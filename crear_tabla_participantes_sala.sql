-- Script para crear tabla participantes_sala
-- Ejecutar este SQL en MySQL Workbench o phpMyAdmin

USE brain_rush;

-- Tabla para participantes de salas de juego
DROP TABLE IF EXISTS `participantes_sala`;
CREATE TABLE `participantes_sala` (
  `id_participante` INT NOT NULL AUTO_INCREMENT,
  `id_sala` INT NOT NULL,
  `id_usuario` INT DEFAULT NULL,
  `nombre_participante` VARCHAR(100) NOT NULL,
  `fecha_union` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `estado` VARCHAR(20) DEFAULT 'esperando',
  PRIMARY KEY (`id_participante`),
  CONSTRAINT `FK_participantes_sala_id_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
  CONSTRAINT `FK_participantes_sala_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL,
  CONSTRAINT `CK_participantes_sala_estado` CHECK (`estado` IN ('esperando', 'jugando', 'finalizado', 'desconectado'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Índices para mejor rendimiento
CREATE INDEX `idx_participantes_sala_id_sala` ON `participantes_sala` (`id_sala`);
CREATE INDEX `idx_participantes_sala_estado` ON `participantes_sala` (`estado`);
