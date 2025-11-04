# -*- coding: utf-8 -*-
from bd import obtener_conexion

conn = obtener_conexion()
cursor = conn.cursor()

cursor.execute('''
    SELECT u.nombre, e.nivel_actual, e.xp_actual, e.xp_total_acumulado 
    FROM usuarios u 
    JOIN experiencia_usuarios e ON u.id_usuario = e.id_usuario 
    WHERE u.tipo_usuario = 'estudiante' 
    LIMIT 1
''')

row = cursor.fetchone()
print(f'\n👤 Usuario: {row[0]}')
print(f'📊 Nivel: {row[1]}')
print(f'💰 XP Actual en nivel: {row[2]}')
print(f'🏆 XP Total Acumulado: {row[3]}')

cursor.execute('SELECT COUNT(*) FROM insignias_usuarios WHERE id_usuario = 4')
count = cursor.fetchone()[0]
print(f'🎖️ Insignias compradas: {count}')

cursor.execute('SELECT i.nombre, c.precio_pagado FROM compras_insignias c JOIN insignias_catalogo i ON c.id_insignia = i.id_insignia WHERE c.id_usuario = 4 ORDER BY c.fecha_compra DESC LIMIT 1')
compra = cursor.fetchone()
if compra:
    print(f'\n💳 Última compra: {compra[0]} por {compra[1]} XP')

conn.close()
