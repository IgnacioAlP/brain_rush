-- Script para agregar campo id_cuestionario a la tabla recompensas
-- Ejecutar este SQL en MySQL Workbench o phpMyAdmin

USE brain_rush;

-- Agregar columna id_cuestionario a la tabla recompensas
ALTER TABLE `recompensas` 
ADD COLUMN `id_cuestionario` INT NULL AFTER `tipo`,
ADD CONSTRAINT `FK_recompensas_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`) ON DELETE CASCADE;

-- Crear índice para mejor rendimiento
CREATE INDEX `idx_recompensas_cuestionario` ON `recompensas` (`id_cuestionario`);
