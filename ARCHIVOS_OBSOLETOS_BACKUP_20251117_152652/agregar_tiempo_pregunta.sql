-- Script para agregar el campo tiempo_por_pregunta a la tabla salas_juego
-- Ejecutar este script en la base de datos brain_rush

USE brain_rush;

-- Agregar columna si no existe (versión simplificada)
-- Ignora el error si la columna ya existe
ALTER TABLE salas_juego 
ADD COLUMN tiempo_por_pregunta INT DEFAULT 30 AFTER estado;

-- Verificar que se agregó correctamente
DESCRIBE salas_juego;
