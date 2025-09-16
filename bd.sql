-- ----------------------------
-- Table structure for cuestionario_preguntas
-- ----------------------------
DROP TABLE IF EXISTS `cuestionario_preguntas`;
CREATE TABLE `cuestionario_preguntas` (
  `id_cuestionario_pregunta` int NOT NULL AUTO_INCREMENT,
  `id_cuestionario` int DEFAULT NULL,
  `id_pregunta` int DEFAULT NULL,
  `orden` int NOT NULL,
  PRIMARY KEY (`id_cuestionario_pregunta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for cuestionarios
-- ----------------------------
DROP TABLE IF EXISTS `cuestionarios`;
CREATE TABLE `cuestionarios` (
  `id_cuestionario` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `descripcion` text,
  `id_docente` int DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_programada` datetime DEFAULT NULL,
  `fecha_publicacion` datetime DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'borrador',
  PRIMARY KEY (`id_cuestionario`),
  CONSTRAINT `CK_cuestionarios_estado` CHECK (`estado` in ('finalizado','publicado','programado','borrador'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for opciones_respuesta
-- ----------------------------
DROP TABLE IF EXISTS `opciones_respuesta`;
CREATE TABLE `opciones_respuesta` (
  `id_opcion` int NOT NULL AUTO_INCREMENT,
  `id_pregunta` int DEFAULT NULL,
  `texto_opcion` text NOT NULL,
  `es_correcta` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_opcion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for participaciones
-- ----------------------------
DROP TABLE IF EXISTS `participaciones`;
CREATE TABLE `participaciones` (
  `id_participacion` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int DEFAULT NULL,
  `id_cuestionario` int DEFAULT NULL,
  `fecha_inicio` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_fin` datetime DEFAULT NULL,
  `puntaje_total` int DEFAULT '0',
  PRIMARY KEY (`id_participacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for preguntas
-- ----------------------------
DROP TABLE IF EXISTS `preguntas`;
CREATE TABLE `preguntas` (
  `id_pregunta` int NOT NULL AUTO_INCREMENT,
  `enunciado` text NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `puntaje_base` int DEFAULT '1',
  PRIMARY KEY (`id_pregunta`),
  CONSTRAINT `CK_preguntas_tipo` CHECK (`tipo` in ('respuesta_corta','verdadero_falso','opcion_multiple'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for ranking
-- ----------------------------
DROP TABLE IF EXISTS `ranking`;
CREATE TABLE `ranking` (
  `id_ranking` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int DEFAULT NULL,
  `id_cuestionario` int DEFAULT NULL,
  `puntaje_total` int DEFAULT '0',
  `posicion` int DEFAULT NULL,
  `fecha_actualizacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ranking`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for recompensas
-- ----------------------------
DROP TABLE IF EXISTS `recompensas`;
CREATE TABLE `recompensas` (
  `id_recompensa` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `puntos_requeridos` int NOT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`id_recompensa`),
  CONSTRAINT `CK_recompensas_tipo` CHECK (`tipo` in ('trofeo','insignia','medalla'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for recompensas_otorgadas
-- ----------------------------
DROP TABLE IF EXISTS `recompensas_otorgadas`;
CREATE TABLE `recompensas_otorgadas` (
  `id_recompensa_otorgada` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int DEFAULT NULL,
  `id_recompensa` int DEFAULT NULL,
  `fecha_otorgacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recompensa_otorgada`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for respuestas_estudiantes
-- ----------------------------
DROP TABLE IF EXISTS `respuestas_estudiantes`;
CREATE TABLE `respuestas_estudiantes` (
  `id_respuesta` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int DEFAULT NULL,
  `id_cuestionario_pregunta` int DEFAULT NULL,
  `respuesta_texto` text,
  `id_opcion_seleccionada` int DEFAULT NULL,
  `fecha_respuesta` datetime DEFAULT CURRENT_TIMESTAMP,
  `puntaje_obtenido` int DEFAULT '0',
  PRIMARY KEY (`id_respuesta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for usuario_roles
-- ----------------------------
DROP TABLE IF EXISTS `usuario_roles`;
CREATE TABLE `usuario_roles` (
  `id_usuario_rol` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `id_rol` int DEFAULT NULL,
  `fecha_asignacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for usuarios
-- ----------------------------
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña_hash` varchar(255) NOT NULL,
  `tipo_usuario` varchar(20) NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` varchar(10) DEFAULT 'activo',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `UQ_usuarios_email` (`email`),
  CONSTRAINT `CK_usuarios_tipo_usuario` CHECK (`tipo_usuario` in ('administrador','docente','estudiante')),
  CONSTRAINT `CK_usuarios_estado` CHECK (`estado` in ('inactivo','activo'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Foreign Keys
-- ----------------------------
ALTER TABLE `cuestionario_preguntas`
  ADD CONSTRAINT `FK_cuestionario_preguntas_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_cuestionario_preguntas_id_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE;

ALTER TABLE `cuestionarios`
  ADD CONSTRAINT `FK_cuestionarios_id_docente` FOREIGN KEY (`id_docente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL;

ALTER TABLE `opciones_respuesta`
  ADD CONSTRAINT `FK_opciones_respuesta_id_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE;

ALTER TABLE `participaciones`
  ADD CONSTRAINT `FK_participaciones_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `FK_participaciones_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`);

ALTER TABLE `ranking`
  ADD CONSTRAINT `FK_ranking_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `FK_ranking_id_cuestionario` FOREIGN KEY (`id_cuestionario`) REFERENCES `cuestionarios` (`id_cuestionario`);

ALTER TABLE `recompensas_otorgadas`
  ADD CONSTRAINT `FK_recompensas_otorgadas_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `FK_recompensas_otorgadas_id_recompensa` FOREIGN KEY (`id_recompensa`) REFERENCES `recompensas` (`id_recompensa`);

ALTER TABLE `respuestas_estudiantes`
  ADD CONSTRAINT `FK_respuestas_estudiantes_id_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `FK_respuestas_estudiantes_id_cuestionario_pregunta` FOREIGN KEY (`id_cuestionario_pregunta`) REFERENCES `cuestionario_preguntas` (`id_cuestionario_pregunta`),
  ADD CONSTRAINT `FK_respuestas_estudiantes_id_opcion_seleccionada` FOREIGN KEY (`id_opcion_seleccionada`) REFERENCES `opciones_respuesta` (`id_opcion`);

ALTER TABLE `usuario_roles`
  ADD CONSTRAINT `FK_usuario_roles_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_usuario_roles_id_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE CASCADE;