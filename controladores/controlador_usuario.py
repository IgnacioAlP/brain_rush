from typing import Dict, Any, Optional, Tuple, List

from bd import obtener_conexion


# ---------------------------------
# Operaciones de BD para usuarios
# (validaciones se hacen en el frontend)
# ---------------------------------

def crear_usuario(nombre: str, apellidos: str, email: str, password_plano: str, tipo_usuario: str = "estudiante") -> int:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"""
				INSERT INTO usuarios (`nombre`, `apellidos`, `email`, `contraseña_hash`, `tipo_usuario`)
				VALUES (%s, %s, %s, %s, %s)
				""",
				(nombre, apellidos, email, password_plano, tipo_usuario),
			)
			conexion.commit()
			return cursor.lastrowid  # type: ignore[attr-defined]
	finally:
		conexion.close()


def obtener_usuarios() -> List[tuple]:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"""
				SELECT `id_usuario`, `nombre`, `apellidos`, `email`, `tipo_usuario`, `estado`, `fecha_registro`
				FROM `usuarios`
				ORDER BY `fecha_registro` DESC
				"""
			)
			return cursor.fetchall()
	finally:
		conexion.close()


def obtener_usuario_por_id(id_usuario: int) -> Optional[tuple]:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"""
				SELECT `id_usuario`, `nombre`, `apellidos`, `email`, `tipo_usuario`, `estado`, `fecha_registro`
				FROM `usuarios` WHERE `id_usuario` = %s
				""",
				(id_usuario,),
			)
			return cursor.fetchone()
	finally:
		conexion.close()


def obtener_usuario_por_email(email: str) -> Optional[tuple]:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"SELECT `id_usuario`, `nombre`, `apellidos`, `email`, `contraseña_hash`, `tipo_usuario`, `estado` FROM `usuarios` WHERE `email` = %s",
				(email,),
			)
			return cursor.fetchone()
	finally:
		conexion.close()


def eliminar_usuario(id_usuario: int) -> None:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute("DELETE FROM `usuarios` WHERE `id_usuario` = %s", (id_usuario,))
		conexion.commit()
	finally:
		conexion.close()


def actualizar_password(id_usuario: int, password_plano: str) -> None:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"UPDATE `usuarios` SET `contraseña_hash` = %s WHERE `id_usuario` = %s",
				(password_plano, id_usuario),
			)
		conexion.commit()
	finally:
		conexion.close()


def actualizar_datos_usuario(id_usuario: int, nombre: str, apellidos: str, tipo_usuario: str, estado: str) -> None:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute(
				"""
				UPDATE `usuarios`
				SET `nombre` = %s, `apellidos` = %s, `tipo_usuario` = %s, `estado` = %s
				WHERE `id_usuario` = %s
				""",
				(nombre, apellidos, tipo_usuario, estado, id_usuario),
			)
		conexion.commit()
	finally:
		conexion.close()


def suspender_usuario(id_usuario: int) -> None:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute("UPDATE `usuarios` SET `estado` = 'inactivo' WHERE `id_usuario` = %s", (id_usuario,))
		conexion.commit()
	finally:
		conexion.close()


def activar_usuario(id_usuario: int) -> None:
	conexion = obtener_conexion()
	try:
		with conexion.cursor() as cursor:
			cursor.execute("UPDATE `usuarios` SET `estado` = 'activo' WHERE `id_usuario` = %s", (id_usuario,))
		conexion.commit()
	finally:
		conexion.close()


def autenticar(email: str, password_plano: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
	fila = obtener_usuario_por_email(email)
	if not fila:
		return False, None
	# fila: (id_usuario, nombre, apellidos, email, contraseña_hash, tipo_usuario, estado)
	if fila[4] != password_plano:
		return False, None
	usuario = {
		"id_usuario": fila[0],
		"nombre": fila[1],
		"apellidos": fila[2],
		"email": fila[3],
		"tipo_usuario": fila[5],
		"estado": fila[6],
	}
	return True, usuario

