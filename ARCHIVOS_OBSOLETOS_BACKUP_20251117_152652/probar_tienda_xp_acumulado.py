# -*- coding: utf-8 -*-
"""
Script para probar el sistema de tienda con XP acumulado
"""

from bd import obtener_conexion
from controladores import controlador_xp

def probar_sistema_tienda():
    """
    Prueba el sistema de compra de insignias con XP acumulado
    """
    print("🧪 PRUEBA DEL SISTEMA DE TIENDA CON XP ACUMULADO")
    print("=" * 60)
    
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener un usuario de prueba (estudiante)
            cursor.execute('''
                SELECT u.id_usuario, u.nombre, u.apellidos, 
                       e.xp_actual, e.nivel_actual, e.xp_total_acumulado
                FROM usuarios u
                JOIN experiencia_usuarios e ON u.id_usuario = e.id_usuario
                WHERE u.tipo_usuario = 'estudiante'
                LIMIT 1
            ''')
            
            usuario = cursor.fetchone()
            if not usuario:
                print("⚠️ No se encontró ningún estudiante")
                return
            
            id_usuario, nombre, apellidos, xp_actual, nivel, xp_total = usuario
            
            print(f"\n👤 Usuario de Prueba: {nombre} {apellidos}")
            print(f"   ID: {id_usuario}")
            print(f"   Nivel Actual: {nivel}")
            print(f"   XP Actual en el Nivel: {xp_actual}")
            print(f"   XP Total Acumulado: {xp_total}")
            print()
            
            # Obtener insignias disponibles para comprar
            print("🏪 INSIGNIAS DISPONIBLES EN LA TIENDA:")
            print("-" * 60)
            
            cursor.execute('''
                SELECT id_insignia, nombre, descripcion, precio_xp, rareza
                FROM insignias_catalogo
                WHERE precio_xp > 0
                ORDER BY precio_xp ASC
            ''')
            
            insignias = cursor.fetchall()
            
            if not insignias:
                print("⚠️ No hay insignias comprables")
                return
            
            for insignia in insignias:
                id_ins, nombre_ins, desc, precio, rareza = insignia
                
                # Verificar si el usuario ya la tiene
                cursor.execute('''
                    SELECT id_insignia FROM insignias_usuarios
                    WHERE id_usuario = %s AND id_insignia = %s
                ''', (id_usuario, id_ins))
                
                ya_comprada = cursor.fetchone() is not None
                puede_comprar = xp_total >= precio and not ya_comprada
                
                estado = "✅ COMPRADA" if ya_comprada else (
                    "💰 PUEDES COMPRAR" if puede_comprar else 
                    f"🔒 Te faltan {precio - xp_total} XP"
                )
                
                print(f"\n{nombre_ins} ({rareza})")
                print(f"   {desc}")
                print(f"   Precio: {precio} XP")
                print(f"   Estado: {estado}")
            
            print("\n" + "=" * 60)
            print("\n💡 INFORMACIÓN IMPORTANTE:")
            print("   • La tienda ahora usa XP TOTAL ACUMULADO")
            print("   • Al comprar, se resta del XP total acumulado")
            print("   • Tu nivel se recalcula automáticamente")
            print("   • Puedes bajar de nivel si gastas mucho XP")
            
            print("\n📊 SIMULACIÓN DE COMPRA:")
            if insignias:
                insignia_ejemplo = insignias[0]
                precio_ejemplo = insignia_ejemplo[3]
                
                if precio_ejemplo <= xp_total:
                    nuevo_xp_total = xp_total - precio_ejemplo
                    nuevo_nivel, nuevo_xp_actual = controlador_xp.calcular_nivel_por_xp(nuevo_xp_total)
                    
                    print(f"\n   Si compraras '{insignia_ejemplo[1]}' por {precio_ejemplo} XP:")
                    print(f"   • XP Total Actual: {xp_total}")
                    print(f"   • Nivel Actual: {nivel}")
                    print(f"   • → XP Total después: {nuevo_xp_total}")
                    print(f"   • → Nivel después: {nuevo_nivel}")
                    
                    if nuevo_nivel < nivel:
                        print(f"   ⚠️ ADVERTENCIA: Bajarías del nivel {nivel} al nivel {nuevo_nivel}")
                    elif nuevo_nivel == nivel:
                        print(f"   ✓ Mantendrías el nivel {nivel}")
                else:
                    print(f"   No tienes suficiente XP para comprar '{insignia_ejemplo[1]}'")
            
    finally:
        conexion.close()

if __name__ == "__main__":
    probar_sistema_tienda()
