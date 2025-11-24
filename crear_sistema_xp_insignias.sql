-- ========================================
-- SISTEMA DE XP, NIVELES E INSIGNIAS
-- ========================================

-- Tabla de experiencia y niveles por usuario
CREATE TABLE IF NOT EXISTS experiencia_usuarios (
    id_experiencia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    xp_actual INT DEFAULT 0,
    nivel_actual INT DEFAULT 1,
    xp_total_acumulado INT DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario (id_usuario),
    INDEX idx_nivel (nivel_actual),
    INDEX idx_xp (xp_actual)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de catálogo de insignias disponibles
CREATE TABLE IF NOT EXISTS insignias_catalogo (
    id_insignia INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50) DEFAULT '🏆', -- Emoji o clase de ícono
    tipo ENUM('bronce', 'plata', 'oro', 'platino', 'diamante') DEFAULT 'bronce',
    requisito_tipo ENUM('nivel', 'partidas', 'racha', 'precision', 'velocidad', 'especial') NOT NULL,
    requisito_valor INT NOT NULL, -- Valor numérico del requisito
    xp_bonus INT DEFAULT 0, -- XP extra al desbloquear
    rareza ENUM('comun', 'raro', 'epico', 'legendario') DEFAULT 'comun',
    color_hex VARCHAR(7) DEFAULT '#FFD700',
    orden_visualizacion INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tipo (tipo),
    INDEX idx_requisito (requisito_tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de insignias desbloqueadas por usuarios
CREATE TABLE IF NOT EXISTS insignias_usuarios (
    id_insignia_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_insignia INT NOT NULL,
    fecha_desbloqueo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mostrar_perfil BOOLEAN DEFAULT FALSE, -- Si se muestra en el perfil
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_insignia) REFERENCES insignias_catalogo(id_insignia) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_insignia (id_usuario, id_insignia),
    INDEX idx_usuario (id_usuario),
    INDEX idx_fecha (fecha_desbloqueo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de estadísticas de juego por usuario (para calcular insignias)
CREATE TABLE IF NOT EXISTS estadisticas_juego (
    id_estadistica INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    total_partidas_jugadas INT DEFAULT 0,
    total_partidas_ganadas INT DEFAULT 0,
    total_respuestas_correctas INT DEFAULT 0,
    total_respuestas_incorrectas INT DEFAULT 0,
    racha_actual INT DEFAULT 0, -- Respuestas correctas consecutivas actuales
    racha_maxima INT DEFAULT 0, -- Mejor racha histórica
    precision_promedio DECIMAL(5,2) DEFAULT 0.00, -- Porcentaje de precisión
    tiempo_promedio_respuesta DECIMAL(6,2) DEFAULT 0.00, -- En segundos
    puntaje_maximo_obtenido INT DEFAULT 0,
    fecha_ultima_partida TIMESTAMP NULL,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_estadistica (id_usuario),
    INDEX idx_racha (racha_maxima),
    INDEX idx_precision (precision_promedio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de historial de XP ganado
CREATE TABLE IF NOT EXISTS historial_xp (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    cantidad_xp INT NOT NULL,
    razon VARCHAR(255), -- 'respuesta_correcta', 'insignia_desbloqueada', 'bonus_nivel', etc.
    id_sala INT NULL,
    id_pregunta INT NULL,
    fecha_ganado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX idx_usuario (id_usuario),
    INDEX idx_fecha (fecha_ganado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- DATOS INICIALES: INSIGNIAS
-- ========================================

INSERT INTO insignias_catalogo (nombre, descripcion, icono, tipo, requisito_tipo, requisito_valor, xp_bonus, rareza, color_hex, orden_visualizacion) VALUES
-- Insignias por nivel
('Principiante', 'Alcanza el nivel 5', '🌱', 'bronce', 'nivel', 5, 50, 'comun', '#CD7F32', 1),
('Aprendiz', 'Alcanza el nivel 10', '📚', 'plata', 'nivel', 10, 100, 'comun', '#C0C0C0', 2),
('Conocedor', 'Alcanza el nivel 20', '🎓', 'oro', 'nivel', 20, 200, 'raro', '#FFD700', 3),
('Experto', 'Alcanza el nivel 35', '🏆', 'platino', 'nivel', 35, 350, 'epico', '#E5E4E2', 4),
('Maestro', 'Alcanza el nivel 50', '👑', 'diamante', 'nivel', 50, 500, 'legendario', '#B9F2FF', 5),

-- Insignias por partidas jugadas
('Primera Victoria', 'Completa tu primera partida', '🎮', 'bronce', 'partidas', 1, 25, 'comun', '#CD7F32', 10),
('Jugador Frecuente', 'Juega 10 partidas', '🎯', 'plata', 'partidas', 10, 75, 'comun', '#C0C0C0', 11),
('Veterano', 'Juega 50 partidas', '⚔️', 'oro', 'partidas', 50, 150, 'raro', '#FFD700', 12),
('Incansable', 'Juega 100 partidas', '🔥', 'platino', 'partidas', 100, 300, 'epico', '#E5E4E2', 13),
('Leyenda', 'Juega 250 partidas', '💎', 'diamante', 'partidas', 250, 600, 'legendario', '#B9F2FF', 14),

-- Insignias por racha
('En Racha', 'Responde 5 preguntas correctas seguidas', '⚡', 'bronce', 'racha', 5, 40, 'comun', '#CD7F32', 20),
('Imparable', 'Responde 10 preguntas correctas seguidas', '🌟', 'plata', 'racha', 10, 100, 'raro', '#C0C0C0', 21),
('Perfeccionista', 'Responde 20 preguntas correctas seguidas', '✨', 'oro', 'racha', 20, 250, 'epico', '#FFD700', 22),
('Invencible', 'Responde 50 preguntas correctas seguidas', '💫', 'diamante', 'racha', 50, 500, 'legendario', '#B9F2FF', 23),

-- Insignias por precisión
('Buen Ojo', 'Mantén una precisión del 70%', '👁️', 'bronce', 'precision', 70, 50, 'comun', '#CD7F32', 30),
('Tirador Experto', 'Mantén una precisión del 85%', '🎯', 'plata', 'precision', 85, 125, 'raro', '#C0C0C0', 31),
('Francotirador', 'Mantén una precisión del 95%', '🏹', 'oro', 'precision', 95, 300, 'epico', '#FFD700', 32),
('Perfección Absoluta', 'Mantén una precisión del 100%', '🎖️', 'diamante', 'precision', 100, 1000, 'legendario', '#B9F2FF', 33),

-- Insignias por velocidad
('Rápido', 'Promedio de respuesta bajo 5 segundos', '⏱️', 'bronce', 'velocidad', 5, 60, 'comun', '#CD7F32', 40),
('Relámpago', 'Promedio de respuesta bajo 3 segundos', '⚡', 'plata', 'velocidad', 3, 150, 'raro', '#C0C0C0', 41),
('Supersónico', 'Promedio de respuesta bajo 2 segundos', '🚀', 'oro', 'velocidad', 2, 400, 'epico', '#FFD700', 42),

-- Insignias especiales
('Madrugador', 'Juega antes de las 6 AM', '🌅', 'oro', 'especial', 1, 100, 'raro', '#FFD700', 50),
('Noctámbulo', 'Juega después de las 11 PM', '🌙', 'oro', 'especial', 1, 100, 'raro', '#FFD700', 51),
('Fin de Semana', 'Juega en fin de semana', '🎉', 'plata', 'especial', 1, 75, 'comun', '#C0C0C0', 52),
('Explorador', 'Juega cuestionarios de 3 áreas diferentes', '🗺️', 'oro', 'especial', 3, 200, 'raro', '#FFD700', 53);

-- ========================================
-- INICIALIZAR EXPERIENCIA PARA USUARIOS EXISTENTES (SOLO ESTUDIANTES)
-- ========================================
INSERT INTO experiencia_usuarios (id_usuario, xp_actual, nivel_actual, xp_total_acumulado)
SELECT id_usuario, 0, 1, 0
FROM usuarios
WHERE tipo_usuario = 'estudiante'
ON DUPLICATE KEY UPDATE id_usuario = id_usuario;

-- ========================================
-- INICIALIZAR ESTADÍSTICAS PARA USUARIOS EXISTENTES (SOLO ESTUDIANTES)
-- ========================================
INSERT INTO estadisticas_juego (id_usuario)
SELECT id_usuario
FROM usuarios
WHERE tipo_usuario = 'estudiante'
ON DUPLICATE KEY UPDATE id_usuario = id_usuario;

-- ========================================
-- TRIGGER: Crear experiencia al registrar nuevo estudiante
-- ========================================
DELIMITER $$

DROP TRIGGER IF EXISTS crear_experiencia_nuevo_estudiante$$
CREATE TRIGGER crear_experiencia_nuevo_estudiante
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.tipo_usuario = 'estudiante' THEN
        INSERT INTO experiencia_usuarios (id_usuario, xp_actual, nivel_actual, xp_total_acumulado)
        VALUES (NEW.id_usuario, 0, 1, 0);
        
        INSERT INTO estadisticas_juego (id_usuario)
        VALUES (NEW.id_usuario);
    END IF;
END$$

DELIMITER ;

-- ========================================
-- VISTA: Ranking de XP
-- ========================================
DROP VIEW IF EXISTS ranking_xp;

CREATE VIEW ranking_xp AS
SELECT 
    u.id_usuario,
    CONCAT(u.nombre, ' ', u.apellidos) as nombre_completo,
    u.email,
    e.nivel_actual,
    e.xp_actual,
    e.xp_total_acumulado,
    (SELECT COUNT(DISTINCT id_insignia) 
     FROM insignias_usuarios 
     WHERE id_usuario = u.id_usuario) as total_insignias,
    ROW_NUMBER() OVER (ORDER BY e.nivel_actual DESC, e.xp_actual DESC) as posicion_ranking
FROM usuarios u
JOIN experiencia_usuarios e ON u.id_usuario = e.id_usuario
WHERE u.tipo_usuario = 'estudiante'
ORDER BY e.nivel_actual DESC, e.xp_actual DESC;

-- ========================================
-- VERIFICACIÓN
-- ========================================
SELECT 'Tablas creadas exitosamente' as mensaje;
SELECT COUNT(*) as total_insignias FROM insignias_catalogo;
SELECT COUNT(*) as estudiantes_con_xp FROM experiencia_usuarios;
