# -*- coding: utf-8 -*-
"""
Script para probar una compra de insignia
"""

from controladores import controlador_xp
from bd import obtener_conexion

def probar_compra():
    print("🧪 PRUEBA DE COMPRA DE INSIGNIA")
    print("=" * 60)
    
    # Obtener un usuario
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT u.id_usuario, u.nombre, u.apellidos,
                       e.xp_total_acumulado, e.nivel_actual, e.xp_actual
                FROM usuarios u
                JOIN experiencia_usuarios e ON u.id_usuario = e.id_usuario
                WHERE u.tipo_usuario = 'estudiante'
                LIMIT 1
            ''')
            
            usuario = cursor.fetchone()
            if not usuario:
                print("❌ No hay usuarios")
                return
            
            id_usuario, nombre, apellidos, xp_total, nivel, xp_actual = usuario
            
            print(f"\n👤 Usuario: {nombre} {apellidos}")
            print(f"   Nivel: {nivel}")
            print(f"   XP Actual: {xp_actual}")
            print(f"   XP Total: {xp_total}")
            
            # Obtener una insignia comprable
            cursor.execute('''
                SELECT id_insignia, nombre, precio_xp
                FROM insignias_catalogo
                WHERE precio_xp > 0 AND precio_xp <= %s
                AND id_insignia NOT IN (
                    SELECT id_insignia FROM insignias_usuarios WHERE id_usuario = %s
                )
                ORDER BY precio_xp ASC
                LIMIT 1
            ''', (xp_total, id_usuario))
            
            insignia = cursor.fetchone()
            if not insignia:
                print("\n⚠️ No hay insignias que puedas comprar")
                return
            
            id_insignia, nombre_insignia, precio = insignia
            
            print(f"\n🏪 Insignia a comprar: {nombre_insignia}")
            print(f"   Precio: {precio} XP")
            print(f"\n⏳ Procesando compra...")
            
    finally:
        conexion.close()
    
    # Realizar la compra
    resultado = controlador_xp.comprar_insignia(id_usuario, id_insignia)
    
    print("\n" + "=" * 60)
    if resultado['success']:
        print("✅ COMPRA EXITOSA")
        print(f"   Mensaje: {resultado['mensaje']}")
        print(f"   XP Gastado: {resultado['xp_gastado']}")
        print(f"   XP Restante: {resultado['xp_restante']}")
        print(f"   Nivel Anterior: {resultado['nivel_anterior']}")
        print(f"   Nivel Nuevo: {resultado['nivel_nuevo']}")
        if resultado['bajo_nivel']:
            print(f"   ⚠️ BAJASTE DE NIVEL")
    else:
        print("❌ ERROR EN LA COMPRA")
        print(f"   Error: {resultado['error']}")

if __name__ == "__main__":
    probar_compra()
