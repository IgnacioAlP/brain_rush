-- ================================================================================
-- INSERTAR INSIGNIAS EN LA BASE DE DATOS BRAIN RUSH
-- ================================================================================
USE brain_rush;

-- ================================================================================
-- RECREAR LA TABLA INSIGNIAS_CATALOGO DESDE CERO
-- ================================================================================
-- Desactivar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar tablas relacionadas y recrearlas
DROP TABLE IF EXISTS `compras_insignias`;
DROP TABLE IF EXISTS `insignias_usuarios`;
DROP TABLE IF EXISTS `insignias_catalogo`;

-- Recrear tabla insignias_catalogo
CREATE TABLE `insignias_catalogo` (
  `id_insignia` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT,
  `icono` VARCHAR(50) DEFAULT '🏆' COMMENT 'Emoji o clase de ícono',
  `tipo` ENUM('bronce','plata','oro','platino','diamante') DEFAULT 'bronce',
  `requisito_tipo` ENUM('nivel','partidas','racha','precision','velocidad','especial') NOT NULL,
  `requisito_valor` INT NOT NULL COMMENT 'Valor numérico del requisito',
  `xp_bonus` INT DEFAULT '0' COMMENT 'XP extra al desbloquear',
  `rareza` ENUM('comun','raro','epico','legendario') DEFAULT 'comun',
  `color_hex` VARCHAR(7) DEFAULT '#FFD700',
  `precio_xp` INT DEFAULT '0' COMMENT 'Precio en XP (0 = no se puede comprar)',
  `orden_visualizacion` INT DEFAULT '0',
  `activo` BOOLEAN DEFAULT TRUE,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_tipo` (`tipo`),
  INDEX `idx_requisito` (`requisito_tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Recrear tabla insignias_usuarios
CREATE TABLE `insignias_usuarios` (
  `id_insignia_usuario` INT AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` INT NOT NULL,
  `id_insignia` INT NOT NULL,
  `fecha_desbloqueo` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `mostrar_perfil` BOOLEAN DEFAULT FALSE COMMENT 'Si se muestra en el perfil',
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id_usuario`) ON DELETE CASCADE,
  FOREIGN KEY (`id_insignia`) REFERENCES `insignias_catalogo`(`id_insignia`) ON DELETE CASCADE,
  UNIQUE KEY `unique_usuario_insignia` (`id_usuario`,`id_insignia`),
  INDEX `idx_usuario` (`id_usuario`),
  INDEX `idx_fecha` (`fecha_desbloqueo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Recrear tabla compras_insignias
CREATE TABLE `compras_insignias` (
  `id_compra` INT AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` INT NOT NULL,
  `id_insignia` INT NOT NULL,
  `xp_gastado` INT NOT NULL,
  `fecha_compra` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id_usuario`) ON DELETE CASCADE,
  FOREIGN KEY (`id_insignia`) REFERENCES `insignias_catalogo`(`id_insignia`) ON DELETE CASCADE,
  INDEX `idx_compras_usuario` (`id_usuario`),
  INDEX `idx_compras_fecha` (`fecha_compra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;    -- ================================================================================
    -- INSERTAR INSIGNIAS
    -- ================================================================================

    -- ================================================================================
    -- INSIGNIAS DE BRONCE (Básicas)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Primera Victoria', 'Gana tu primera partida', '🥉', 'bronce', 'partidas', 1, 50, 'comun', '#CD7F32', 0, 1, TRUE),
    ('Aprendiz', 'Alcanza el nivel 5', '📚', 'bronce', 'nivel', 5, 100, 'comun', '#CD7F32', 0, 2, TRUE),
    ('Estudiante Activo', 'Juega 10 partidas', '🎮', 'bronce', 'partidas', 10, 150, 'comun', '#CD7F32', 0, 3, TRUE),
    ('Racha Inicial', 'Consigue 5 respuestas correctas seguidas', '🔥', 'bronce', 'racha', 5, 100, 'comun', '#CD7F32', 0, 4, TRUE);

    -- ================================================================================
    -- INSIGNIAS DE PLATA (Intermedias)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Cinco Victorias', 'Gana 5 partidas', '🥈', 'plata', 'partidas', 5, 200, 'raro', '#C0C0C0', 0, 5, TRUE),
    ('Conocedor', 'Alcanza el nivel 10', '🎓', 'plata', 'nivel', 10, 250, 'raro', '#C0C0C0', 0, 6, TRUE),
    ('Jugador Dedicado', 'Juega 25 partidas', '🎯', 'plata', 'partidas', 25, 300, 'raro', '#C0C0C0', 0, 7, TRUE),
    ('Racha Sólida', 'Consigue 10 respuestas correctas seguidas', '🔥', 'plata', 'racha', 10, 250, 'raro', '#C0C0C0', 0, 8, TRUE),
    ('Precisión', 'Mantén 80% de precisión', '🎯', 'plata', 'precision', 80, 300, 'raro', '#C0C0C0', 0, 9, TRUE);

    -- ================================================================================
    -- INSIGNIAS DE ORO (Avanzadas)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Diez Victorias', 'Gana 10 partidas', '🥇', 'oro', 'partidas', 10, 400, 'epico', '#FFD700', 0, 10, TRUE),
    ('Experto', 'Alcanza el nivel 20', '👑', 'oro', 'nivel', 20, 500, 'epico', '#FFD700', 0, 11, TRUE),
    ('Veterano', 'Juega 50 partidas', '⭐', 'oro', 'partidas', 50, 600, 'epico', '#FFD700', 0, 12, TRUE),
    ('Racha Impresionante', 'Consigue 15 respuestas correctas seguidas', '🔥', 'oro', 'racha', 15, 500, 'epico', '#FFD700', 0, 13, TRUE),
    ('Maestro de Precisión', 'Mantén 90% de precisión', '🎯', 'oro', 'precision', 90, 600, 'epico', '#FFD700', 0, 14, TRUE),
    ('Velocista', 'Responde en menos de 5 segundos promedio', '⚡', 'oro', 'velocidad', 5, 550, 'epico', '#FFD700', 0, 15, TRUE);

    -- ================================================================================
    -- INSIGNIAS DE PLATINO (Elite)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Campeón', 'Gana 25 partidas', '🏆', 'platino', 'partidas', 25, 800, 'legendario', '#E5E4E2', 0, 16, TRUE),
    ('Maestro', 'Alcanza el nivel 30', '💎', 'platino', 'nivel', 30, 1000, 'legendario', '#E5E4E2', 0, 17, TRUE),
    ('Jugador Legendario', 'Juega 100 partidas', '🌟', 'platino', 'partidas', 100, 1200, 'legendario', '#E5E4E2', 0, 18, TRUE),
    ('Racha Extraordinaria', 'Consigue 20 respuestas correctas seguidas', '🔥', 'platino', 'racha', 20, 1000, 'legendario', '#E5E4E2', 0, 19, TRUE),
    ('Perfeccionista', 'Mantén 95% de precisión', '💯', 'platino', 'precision', 95, 1200, 'legendario', '#E5E4E2', 0, 20, TRUE);

    -- ================================================================================
    -- INSIGNIAS DE DIAMANTE (Máximo nivel)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Leyenda', 'Gana 50 partidas', '💎', 'diamante', 'partidas', 50, 1500, 'legendario', '#B9F2FF', 0, 21, TRUE),
    ('Gran Maestro', 'Alcanza el nivel 50', '👑', 'diamante', 'nivel', 50, 2000, 'legendario', '#B9F2FF', 0, 22, TRUE),
    ('Inmortal', 'Juega 250 partidas', '🌠', 'diamante', 'partidas', 250, 2500, 'legendario', '#B9F2FF', 0, 23, TRUE),
    ('Racha Imposible', 'Consigue 30 respuestas correctas seguidas', '🔥', 'diamante', 'racha', 30, 2000, 'legendario', '#B9F2FF', 0, 24, TRUE),
    ('Dios de Brain Rush', 'Mantén 99% de precisión', '⚡', 'diamante', 'precision', 99, 3000, 'legendario', '#B9F2FF', 0, 25, TRUE);

    -- ================================================================================
    -- INSIGNIAS ESPECIALES (Eventos/Logros únicos)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Madrugador', 'Juega antes de las 6 AM', '🌅', 'oro', 'especial', 1, 400, 'epico', '#FF6B6B', 0, 26, TRUE),
    ('Nocturno', 'Juega después de las 11 PM', '🌙', 'oro', 'especial', 1, 400, 'epico', '#4A5568', 0, 27, TRUE),
    ('Fin de Semana', 'Juega en fin de semana', '🎉', 'plata', 'especial', 1, 200, 'raro', '#9B59B6', 0, 28, TRUE),
    ('Primer Lugar', 'Termina primero en una sala', '👑', 'oro', 'especial', 1, 500, 'epico', '#FFD700', 0, 29, TRUE),
    ('Estudiante del Mes', 'Insignia otorgada por el docente', '🎖️', 'platino', 'especial', 1, 1000, 'legendario', '#E74C3C', 0, 30, TRUE);

    -- ================================================================================
    -- INSIGNIAS COMPRABLES (Tienda de XP)
    -- ================================================================================
    INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, precio_xp, orden_visualizacion, activo)
    VALUES 
    ('Cerebro de Bronce', 'Insignia comprable básica', '🧠', 'bronce', 'especial', 0, 0, 'comun', '#CD7F32', 500, 31, TRUE),
    ('Cerebro de Plata', 'Insignia comprable intermedia', '🧠', 'plata', 'especial', 0, 0, 'raro', '#C0C0C0', 1000, 32, TRUE),
    ('Cerebro de Oro', 'Insignia comprable avanzada', '🧠', 'oro', 'especial', 0, 0, 'epico', '#FFD700', 2000, 33, TRUE),
    ('Estrella Fugaz', 'Insignia de colección', '💫', 'platino', 'especial', 0, 0, 'legendario', '#9B59B6', 3000, 34, TRUE),
    ('Rayo Dorado', 'Insignia de élite', '⚡', 'diamante', 'especial', 0, 0, 'legendario', '#FFD700', 5000, 35, TRUE);

    -- ================================================================================
    -- VERIFICACIÓN
    -- ================================================================================
    SELECT '✅ Insignias insertadas correctamente' as resultado;

    SELECT 
        COUNT(*) as total_insignias,
        SUM(CASE WHEN tipo = 'bronce' THEN 1 ELSE 0 END) as bronce,
        SUM(CASE WHEN tipo = 'plata' THEN 1 ELSE 0 END) as plata,
        SUM(CASE WHEN tipo = 'oro' THEN 1 ELSE 0 END) as oro,
        SUM(CASE WHEN tipo = 'platino' THEN 1 ELSE 0 END) as platino,
        SUM(CASE WHEN tipo = 'diamante' THEN 1 ELSE 0 END) as diamante,
        SUM(CASE WHEN precio_xp > 0 THEN 1 ELSE 0 END) as comprables,
        SUM(CASE WHEN requisito_tipo = 'especial' THEN 1 ELSE 0 END) as especiales
    FROM insignias_catalogo;

    -- Ver todas las insignias insertadas
    SELECT 
        id_insignia,
        nombre,
        tipo,
        requisito_tipo,
        requisito_valor,
        xp_bonus,
        rareza,
        precio_xp,
        orden_visualizacion
    FROM insignias_catalogo
    ORDER BY orden_visualizacion;
