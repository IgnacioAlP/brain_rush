-- Script para agregar columnas de tokens de OneDrive a la tabla usuarios
-- Ejecutar este script en la base de datos brain_rush

USE brain_rush;

-- Agregar columnas para almacenar tokens de OneDrive
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS onedrive_access_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_refresh_token TEXT NULL,
ADD COLUMN IF NOT EXISTS onedrive_token_expires DATETIME NULL;

-- Verificar que las columnas se agregaron correctamente
DESCRIBE usuarios;

SELECT 'Columnas de OneDrive agregadas exitosamente' AS resultado;
