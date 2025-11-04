-- =========================================
-- AGREGAR INSIGNIAS COMPRABLES ÚNICAS
-- =========================================
-- Estas son insignias EXCLUSIVAS de la tienda
-- No se desbloquean automáticamente

INSERT INTO insignias_catalogo 
(nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, activo)
VALUES
-- LEGENDARIAS (Alto precio)
('Cerebro de Oro', 'Insignia legendaria que otorga +30% de XP permanente en todas las partidas', '🧠', 'oro', 'especial', 0, 30, 'legendario', '#FFD700', 15000, TRUE),
('Rayo Cósmico', 'Insignia épica que aumenta tu velocidad de pensamiento (+25% XP)', '⚡', 'platino', 'especial', 0, 25, 'epico', '#9B59B6', 10000, TRUE),
('Estrella Fugaz', 'Insignia épica para los más rápidos (+20% XP)', '🌟', 'oro', 'especial', 0, 20, 'epico', '#E74C3C', 8000, TRUE),

-- ÉPICAS (Precio medio)
('Búho Sabio', 'Símbolo de sabiduría y conocimiento (+15% XP)', '🦉', 'plata', 'especial', 0, 15, 'raro', '#3498DB', 5000, TRUE),
('Cohete Turbo', 'Acelera tu progreso en el juego (+15% XP)', '🚀', 'plata', 'especial', 0, 15, 'raro', '#1ABC9C', 4500, TRUE),

-- RARAS (Precio accesible)
('Trébol de la Suerte', 'Atrae la buena fortuna (+10% XP)', '🍀', 'bronce', 'especial', 0, 10, 'comun', '#2ECC71', 3000, TRUE),
('Fuego Ardiente', 'Enciende tu pasión por aprender (+10% XP)', '🔥', 'bronce', 'especial', 0, 10, 'comun', '#E67E22', 2500, TRUE),
('Corona Real', 'Demuestra tu dominio del juego (+12% XP)', '👑', 'plata', 'especial', 0, 12, 'raro', '#F39C12', 6000, TRUE);
