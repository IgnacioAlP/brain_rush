-- ========================================
-- TIENDA DE INSIGNIAS COMPRABLES
-- Sistema para comprar insignias especiales con XP
-- ========================================

-- Agregar columna precio_xp a insignias
ALTER TABLE insignias_catalogo 
ADD COLUMN precio_xp INT DEFAULT 0 COMMENT 'Precio en XP (0 = no se puede comprar)';

-- Actualizar algunas insignias como comprables
UPDATE insignias_catalogo SET precio_xp = 500 WHERE nombre = 'Principiante';
UPDATE insignias_catalogo SET precio_xp = 1000 WHERE nombre = 'Veterano';
UPDATE insignias_catalogo SET precio_xp = 2000 WHERE nombre = 'Maestro';
UPDATE insignias_catalogo SET precio_xp = 5000 WHERE nombre = 'Leyenda';

-- Crear nuevas insignias especiales solo para comprar
INSERT INTO insignias_catalogo (nombre, descripcion, tipo, rareza, icono, requisitos, xp_bonus, precio_xp) VALUES
('Escudo Dorado', 'Protección especial para tu perfil', 'especial', 'epico', '🛡️', '{"comprable": true}', 15, 3000),
('Corona Real', 'Demuestra tu dominio absoluto', 'especial', 'legendario', '👑', '{"comprable": true}', 25, 10000),
('Estrella Brillante', 'Brilla en el ranking', 'especial', 'raro', '✨', '{"comprable": true}', 10, 1500),
('Trofeo de Campeón', 'El premio del verdadero campeón', 'especial', 'legendario', '🏆', '{"comprable": true}', 30, 15000),
('Medalla de Honor', 'Reconocimiento por tu esfuerzo', 'especial', 'epico', '🎖️', '{"comprable": true}', 12, 2500),
('Rayo Velocidad', 'Símbolo de respuestas rápidas', 'velocidad', 'epico', '⚡', '{"comprable": true}', 15, 4000),
('Fuego Imparable', 'Racha infinita de victorias', 'racha', 'legendario', '🔥', '{"comprable": true}', 20, 8000),
('Cerebro Gigante', 'Inteligencia suprema', 'precision', 'epico', '🧠', '{"comprable": true}', 18, 5000);

-- Crear tabla para historial de compras
CREATE TABLE IF NOT EXISTS compras_insignias (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_insignia INT NOT NULL,
    xp_gastado INT NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_insignia) REFERENCES insignias_catalogo(id_insignia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Índices para mejor rendimiento
CREATE INDEX idx_compras_usuario ON compras_insignias(id_usuario);
CREATE INDEX idx_compras_fecha ON compras_insignias(fecha_compra);

SELECT 'Tienda de insignias creada exitosamente' as mensaje;
