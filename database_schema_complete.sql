-- ================================================================================
-- BRAIN RUSH - COMPLETE DATABASE SCHEMA
-- Script de creación completo de todas las tablas para PythonAnywhere
-- ================================================================================
-- MySQL Version: 5.7+
-- Character Set: utf8mb4
-- ================================================================================

-- DROP DATABASE IF EXISTS `ProyectoWeb20252$default`;
-- CREATE DATABASE `ProyectoWeb20252$default` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE `ProyectoWeb20252$default`;

USE `ProyectoWeb20252$default`;

-- ================================================================================
-- 1. TABLA: usuarios
-- ================================================================================
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `apellidos` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `contraseña_hash` VARCHAR(255) NOT NULL COMMENT 'bcrypt hash',
  `tipo_usuario` VARCHAR(20) NOT NULL COMMENT 'administrador, docente, estudiante',
  `fecha_registro` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `estado` VARCHAR(10) DEFAULT 'activo' COMMENT 'activo, inactivo',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `UQ_usuarios_email` (`email`),
  CONSTRAINT `CK_usuarios_tipo_usuario` CHECK (`tipo_usuario` IN ('administrador','docente','estudiante')),
  CONSTRAINT `CK_usuarios_estado` CHECK (`estado` IN ('inactivo','activo'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 2. TABLA: roles
-- ================================================================================
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id_rol` INT NOT NULL AUTO_INCREMENT,
  `nombre_rol` VARCHAR(50) NOT NULL,
  `descripcion` TEXT,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 3. TABLA: usuario_roles
-- ================================================================================
DROP TABLE IF EXISTS `usuario_roles`;
CREATE TABLE `usuario_roles` (
  `id_usuario_rol` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT DEFAULT NULL,
  `id_rol` INT DEFAULT NULL,
  `fecha_asignacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario_rol`),
  CONSTRAINT `FK_usuario_roles_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `FK_usuario_roles_id_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 4. TABLA: cuestionarios
-- ================================================================================
DROP TABLE IF EXISTS `cuestionarios`;
CREATE TABLE `cuestionarios` (
  `id_cuestionario` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(200) NOT NULL,
  `descripcion` TEXT,
  `id_docente` INT DEFAULT NULL,
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `fecha_programada` DATETIME DEFAULT NULL,
  `fecha_publicacion` DATETIME DEFAULT NULL,
  `estado` VARCHAR(20) DEFAULT 'borrador' COMMENT 'borrador, programado, publicado, finalizado',
  PRIMARY KEY (`id_cuestionario`),
  CONSTRAINT `FK_cuestionarios_id_docente` FOREIGN KEY (`id_docente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL,
  CONSTRAINT `CK_cuestionarios_estado` CHECK (`estado` IN ('finalizado','publicado','programado','borrador'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 5. TABLA: preguntas
-- ================================================================================
DROP TABLE IF EXISTS `preguntas`;
CREATE TABLE `preguntas` (
  `id_pregunta` INT NOT NULL AUTO_INCREMENT,
  `enunciado` TEXT NOT NULL,
  `tipo` VARCHAR(20) NOT NULL COMMENT 'respuesta_corta, verdadero_falso, opcion_multiple',
  `puntaje_base` INT DEFAULT '1',
  `tiempo_sugerido` INT DEFAULT '30' COMMENT 'Segundos',
  PRIMARY KEY (`id_pregunta`),
  CONSTRAINT `CK_preguntas_tipo` CHECK (`tipo` IN ('respuesta_corta','verdadero_falso','opcion_multiple'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 6. TABLA: cuestionario_preguntas
-- ================================================================================
DROP TABLE IF EXISTS `cuestionario_preguntas`;
CREATE TABLE `cuestionario_preguntas` (
  `id_cuestionario_pregunta` INT NOT NULL AUTO_INCREMENT,
  `id_cuestionario` INT DEFAULT NULL,
  `id_pregunta` INT DEFAULT NULL,
  `orden` INT NOT NULL,
  PRIMARY KEY (`id_cuestionario_pregunta`),
  CONSTRAINT `FK_cuestionario_preguntas_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `FK_cuestionario_preguntas_id_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 7. TABLA: opciones_respuesta
-- ================================================================================
DROP TABLE IF EXISTS `opciones_respuesta`;
CREATE TABLE `opciones_respuesta` (
  `id_opcion` INT NOT NULL AUTO_INCREMENT,
  `id_pregunta` INT DEFAULT NULL,
  `texto_opcion` TEXT NOT NULL,
  `es_correcta` TINYINT(1) DEFAULT '0',
  PRIMARY KEY (`id_opcion`),
  CONSTRAINT `FK_opciones_respuesta_id_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 8. TABLA: salas_juego
-- ================================================================================
DROP TABLE IF EXISTS `salas_juego`;
CREATE TABLE `salas_juego` (
  `id_sala` INT NOT NULL AUTO_INCREMENT,
  `pin_sala` VARCHAR(8) UNIQUE NOT NULL COMMENT 'Código PIN de acceso a la sala (6 dígitos o AUTO+4)',
  `id_cuestionario` INT DEFAULT NULL,
  `modo_juego` ENUM('individual','grupo','colaborativo') DEFAULT 'individual',
  `estado` ENUM('esperando','en_curso','finalizada') DEFAULT 'esperando',
  `tiempo_por_pregunta` INT DEFAULT '30' COMMENT 'Segundos',
  `max_participantes` INT DEFAULT NULL,
  `grupos_habilitados` TINYINT(1) DEFAULT '0',
  `num_grupos` INT DEFAULT '0',
  `pregunta_actual` INT DEFAULT '0',
  `total_preguntas` INT DEFAULT '0',
  `tiempo_inicio_juego` DATETIME DEFAULT NULL,
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_sala`),
  UNIQUE KEY `UQ_salas_pin` (`pin_sala`),
  CONSTRAINT `FK_salas_juego_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 9. TABLA: grupos_sala
-- ================================================================================
DROP TABLE IF EXISTS `grupos_sala`;
CREATE TABLE `grupos_sala` (
  `id_grupo` INT NOT NULL AUTO_INCREMENT,
  `id_sala` INT NOT NULL,
  `numero_grupo` INT DEFAULT NULL COMMENT 'Número secuencial del grupo',
  `nombre_grupo` VARCHAR(100) DEFAULT NULL,
  `capacidad` INT DEFAULT NULL,
  PRIMARY KEY (`id_grupo`),
  CONSTRAINT `FK_grupos_sala_id_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
  INDEX `idx_grupos_sala_id_sala` (`id_sala`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 10. TABLA: participantes_sala
-- ================================================================================
DROP TABLE IF EXISTS `participantes_sala`;
CREATE TABLE `participantes_sala` (
  `id_participante` INT NOT NULL AUTO_INCREMENT,
  `id_sala` INT NOT NULL,
  `id_usuario` INT DEFAULT NULL,
  `nombre_participante` VARCHAR(100) NOT NULL,
  `id_grupo` INT DEFAULT NULL,
  `fecha_union` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `estado` VARCHAR(20) DEFAULT 'esperando' COMMENT 'esperando, jugando, finalizado, desconectado',
  PRIMARY KEY (`id_participante`),
  CONSTRAINT `FK_participantes_sala_id_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
  CONSTRAINT `FK_participantes_sala_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL,
  CONSTRAINT `FK_participantes_sala_id_grupo` FOREIGN KEY (`id_grupo`) REFERENCES `grupos_sala` (`id_grupo`) ON DELETE SET NULL,
  CONSTRAINT `CK_participantes_sala_estado` CHECK (`estado` IN ('esperando','jugando','finalizado','desconectado')),
  INDEX `idx_participantes_sala_id_sala` (`id_sala`),
  INDEX `idx_participantes_sala_estado` (`estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 11. TABLA: estado_juego_sala
-- ================================================================================
DROP TABLE IF EXISTS `estado_juego_sala`;
CREATE TABLE `estado_juego_sala` (
  `id_estado` INT NOT NULL AUTO_INCREMENT,
  `id_sala` INT NOT NULL,
  `pregunta_actual` INT NOT NULL DEFAULT '0',
  `tiempo_inicio_pregunta` DATETIME DEFAULT NULL,
  `estado_pregunta` VARCHAR(20) DEFAULT 'esperando' COMMENT 'esperando, respondiendo, finalizada',
  PRIMARY KEY (`id_estado`),
  UNIQUE KEY `UK_estado_sala` (`id_sala`),
  CONSTRAINT `FK_estado_juego_id_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 12. TABLA: respuestas_participantes
-- ================================================================================
DROP TABLE IF EXISTS `respuestas_participantes`;
CREATE TABLE `respuestas_participantes` (
  `id_respuesta_participante` INT NOT NULL AUTO_INCREMENT,
  `id_participante` INT NOT NULL,
  `id_sala` INT NOT NULL,
  `id_pregunta` INT NOT NULL,
  `id_opcion_seleccionada` INT DEFAULT NULL,
  `tiempo_respuesta` DECIMAL(10,3) NOT NULL COMMENT 'Segundos',
  `es_correcta` TINYINT(1) DEFAULT '0',
  `puntaje_obtenido` INT DEFAULT '0',
  `fecha_respuesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_respuesta_participante`),
  UNIQUE KEY `UK_participante_pregunta` (`id_participante`,`id_sala`,`id_pregunta`),
  CONSTRAINT `FK_respuestas_part_participante` FOREIGN KEY (`id_participante`) REFERENCES `participantes_sala` (`id_participante`) ON DELETE CASCADE,
  CONSTRAINT `FK_respuestas_part_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
  CONSTRAINT `FK_respuestas_part_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `FK_respuestas_part_opcion` FOREIGN KEY (`id_opcion_seleccionada`) REFERENCES `opciones_respuesta` (`id_opcion`) ON DELETE SET NULL,
  INDEX `idx_respuestas_part_sala` (`id_sala`),
  INDEX `idx_respuestas_part_pregunta` (`id_pregunta`),
  INDEX `idx_respuestas_part_tiempo` (`tiempo_respuesta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 13. TABLA: ranking_sala
-- ================================================================================
DROP TABLE IF EXISTS `ranking_sala`;
CREATE TABLE `ranking_sala` (
  `id_ranking_sala` INT NOT NULL AUTO_INCREMENT,
  `id_participante` INT NOT NULL,
  `id_sala` INT NOT NULL,
  `puntaje_total` INT DEFAULT '0',
  `respuestas_correctas` INT DEFAULT '0',
  `tiempo_total_respuestas` DECIMAL(10,3) DEFAULT '0' COMMENT 'Segundos acumulados',
  `posicion` INT DEFAULT NULL,
  PRIMARY KEY (`id_ranking_sala`),
  UNIQUE KEY `UK_ranking_participante_sala` (`id_participante`,`id_sala`),
  CONSTRAINT `FK_ranking_sala_participante` FOREIGN KEY (`id_participante`) REFERENCES `participantes_sala` (`id_participante`) ON DELETE CASCADE,
  CONSTRAINT `FK_ranking_sala_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
  INDEX `idx_ranking_sala_puntaje` (`id_sala`,`puntaje_total` DESC,`tiempo_total_respuestas` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 14. TABLA: participaciones
-- ================================================================================
DROP TABLE IF EXISTS `participaciones`;
CREATE TABLE `participaciones` (
  `id_participacion` INT NOT NULL AUTO_INCREMENT,
  `id_estudiante` INT DEFAULT NULL,
  `id_cuestionario` INT DEFAULT NULL,
  `fecha_inicio` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `fecha_fin` DATETIME DEFAULT NULL,
  `puntaje_total` INT DEFAULT '0',
  PRIMARY KEY (`id_participacion`),
  CONSTRAINT `FK_participaciones_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `FK_participaciones_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 15. TABLA: respuestas_estudiantes
-- ================================================================================
DROP TABLE IF EXISTS `respuestas_estudiantes`;
CREATE TABLE `respuestas_estudiantes` (
  `id_respuesta` INT NOT NULL AUTO_INCREMENT,
  `id_estudiante` INT DEFAULT NULL,
  `id_cuestionario_pregunta` INT DEFAULT NULL,
  `respuesta_texto` TEXT,
  `id_opcion_seleccionada` INT DEFAULT NULL,
  `fecha_respuesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `puntaje_obtenido` INT DEFAULT '0',
  PRIMARY KEY (`id_respuesta`),
  CONSTRAINT `FK_respuestas_estudiantes_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `FK_respuestas_estudiantes_id_cuestionario_pregunta` FOREIGN KEY (`id_cuestionario_pregunta`) REFERENCES `cuestionario_preguntas` (`id_cuestionario_pregunta`),
  CONSTRAINT `FK_respuestas_estudiantes_id_opcion_seleccionada` FOREIGN KEY (`id_opcion_seleccionada`) REFERENCES `opciones_respuesta` (`id_opcion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 16. TABLA: ranking
-- ================================================================================
DROP TABLE IF EXISTS `ranking`;
CREATE TABLE `ranking` (
  `id_ranking` INT NOT NULL AUTO_INCREMENT,
  `id_estudiante` INT DEFAULT NULL,
  `id_cuestionario` INT DEFAULT NULL,
  `puntaje_total` INT DEFAULT '0',
  `posicion` INT DEFAULT NULL,
  `fecha_actualizacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ranking`),
  CONSTRAINT `FK_ranking_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `FK_ranking_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 17. TABLA: recompensas
-- ================================================================================
DROP TABLE IF EXISTS `recompensas`;
CREATE TABLE `recompensas` (
  `id_recompensa` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT,
  `puntos_requeridos` INT NOT NULL,
  `tipo` VARCHAR(20) NOT NULL COMMENT 'trofeo, insignia, medalla',
  PRIMARY KEY (`id_recompensa`),
  CONSTRAINT `CK_recompensas_tipo` CHECK (`tipo` IN ('trofeo','insignia','medalla'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 18. TABLA: recompensas_otorgadas
-- ================================================================================
DROP TABLE IF EXISTS `recompensas_otorgadas`;
CREATE TABLE `recompensas_otorgadas` (
  `id_recompensa_otorgada` INT NOT NULL AUTO_INCREMENT,
  `id_estudiante` INT DEFAULT NULL,
  `id_recompensa` INT DEFAULT NULL,
  `fecha_otorgacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recompensa_otorgada`),
  CONSTRAINT `FK_recompensas_otorgadas_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `FK_recompensas_otorgadas_id_recompensa` FOREIGN KEY (`id_recompensa`) REFERENCES `recompensas` (`id_recompensa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ================================================================================
-- 19. TABLA: experiencia_usuarios
-- ================================================================================
DROP TABLE IF EXISTS `experiencia_usuarios`;
CREATE TABLE `experiencia_usuarios` (
  `id_experiencia` INT AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` INT NOT NULL,
  `xp_actual` INT DEFAULT '0',
  `nivel_actual` INT DEFAULT '1',
  `xp_total_acumulado` INT DEFAULT '0',
  `fecha_actualizacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id_usuario`) ON DELETE CASCADE,
  UNIQUE KEY `unique_usuario` (`id_usuario`),
  INDEX `idx_nivel` (`nivel_actual`),
  INDEX `idx_xp` (`xp_actual`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================================
-- 20. TABLA: insignias_catalogo
-- ================================================================================
DROP TABLE IF EXISTS `insignias_catalogo`;
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

-- ================================================================================
-- 21. TABLA: insignias_usuarios
-- ================================================================================
DROP TABLE IF EXISTS `insignias_usuarios`;
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

-- ================================================================================
-- 22. TABLA: compras_insignias
-- ================================================================================
DROP TABLE IF EXISTS `compras_insignias`;
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

-- ================================================================================
-- 23. TABLA: estadisticas_juego
-- ================================================================================
DROP TABLE IF EXISTS `estadisticas_juego`;
CREATE TABLE `estadisticas_juego` (
  `id_estadistica` INT AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` INT NOT NULL,
  `total_partidas_jugadas` INT DEFAULT '0',
  `total_partidas_ganadas` INT DEFAULT '0',
  `total_respuestas_correctas` INT DEFAULT '0',
  `total_respuestas_incorrectas` INT DEFAULT '0',
  `racha_actual` INT DEFAULT '0' COMMENT 'Respuestas correctas consecutivas actuales',
  `racha_maxima` INT DEFAULT '0' COMMENT 'Mejor racha histórica',
  `precision_promedio` DECIMAL(5,2) DEFAULT '0.00' COMMENT 'Porcentaje de precisión',
  `tiempo_promedio_respuesta` DECIMAL(6,2) DEFAULT '0.00' COMMENT 'En segundos',
  `puntaje_maximo_obtenido` INT DEFAULT '0',
  `fecha_ultima_partida` TIMESTAMP NULL,
  `fecha_actualizacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id_usuario`) ON DELETE CASCADE,
  UNIQUE KEY `unique_usuario_estadistica` (`id_usuario`),
  INDEX `idx_racha` (`racha_maxima`),
  INDEX `idx_precision` (`precision_promedio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================================
-- 24. TABLA: historial_xp
-- ================================================================================
DROP TABLE IF EXISTS `historial_xp`;
CREATE TABLE `historial_xp` (
  `id_historial` INT AUTO_INCREMENT PRIMARY KEY,
  `id_usuario` INT NOT NULL,
  `cantidad_xp` INT NOT NULL,
  `razon` VARCHAR(255) COMMENT 'respuesta_correcta, insignia_desbloqueada, bonus_nivel, etc.',
  `id_sala` INT DEFAULT NULL,
  `id_pregunta` INT DEFAULT NULL,
  `fecha_ganado` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id_usuario`) ON DELETE CASCADE,
  INDEX `idx_usuario` (`id_usuario`),
  INDEX `idx_fecha` (`fecha_ganado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================================
-- TRIGGERS
-- ================================================================================
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

-- ================================================================================
-- VISTAS
-- ================================================================================
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

-- ================================================================================
-- VERIFICACIÓN Y RESUMEN
-- ================================================================================

SELECT '✅ Base de datos creada exitosamente' as mensaje;

-- Contar tablas creadas
SELECT COUNT(*) as total_tablas FROM information_schema.tables WHERE table_schema = 'ProyectoWeb20252$default';

-- Listar todas las tablas
SELECT GROUP_CONCAT(table_name ORDER BY table_name SEPARATOR ', ') as tablas
FROM information_schema.tables 
WHERE table_schema = 'ProyectoWeb20252$default'
ORDER BY table_name;
