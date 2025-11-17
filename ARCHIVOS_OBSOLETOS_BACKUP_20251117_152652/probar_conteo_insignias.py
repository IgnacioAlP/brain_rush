# -*- coding: utf-8 -*-
"""
Script para probar el conteo de insignias en el perfil
"""

from controladores import controlador_xp
from bd import obtener_conexion

def probar_conteo_insignias():
    print("🔢 PRUEBA DE CONTEO DE INSIGNIAS")
    print("=" * 60)
    
    # Obtener un usuario
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT id_usuario, nombre, apellidos
                FROM usuarios
                WHERE tipo_usuario = 'estudiante'
                LIMIT 1
            ''')
            
            usuario = cursor.fetchone()
            if not usuario:
                print("❌ No hay usuarios")
                return
            
            id_usuario, nombre, apellidos = usuario
            print(f"\n👤 Usuario: {nombre} {apellidos} (ID: {id_usuario})")
            
            # Contar directamente desde la BD
            cursor.execute('''
                SELECT COUNT(*) FROM insignias_usuarios WHERE id_usuario = %s
            ''', (id_usuario,))
            count_bd = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM insignias_catalogo WHERE activo = TRUE
            ''', ())
            total_bd = cursor.fetchone()[0]
            
            print(f"\n📊 CONTEO DIRECTO DESDE BD:")
            print(f"   Insignias desbloqueadas: {count_bd}")
            print(f"   Total insignias: {total_bd}")
            
    finally:
        conexion.close()
    
    # Obtener perfil usando la función
    print(f"\n📋 USANDO obtener_perfil_xp():")
    perfil = controlador_xp.obtener_perfil_xp(id_usuario)
    
    if perfil:
        print(f"   Nombre: {perfil['nombre_completo']}")
        print(f"   Nivel: {perfil['nivel_actual']}")
        print(f"   XP Total: {perfil['xp_total_acumulado']}")
        print(f"   Insignias: {perfil['insignias_desbloqueadas']}/{perfil['total_insignias']}")
        print(f"   Ranking: #{perfil['posicion_ranking']}")
        
        print("\n✅ RESULTADO:")
        if perfil['insignias_desbloqueadas'] == count_bd and perfil['total_insignias'] == total_bd:
            print(f"   ✓ Conteo correcto: {perfil['insignias_desbloqueadas']}/{perfil['total_insignias']}")
        else:
            print(f"   ✗ Conteo incorrecto")
            print(f"   Esperado: {count_bd}/{total_bd}")
            print(f"   Obtenido: {perfil['insignias_desbloqueadas']}/{perfil['total_insignias']}")
    else:
        print("   ❌ No se pudo obtener el perfil")

if __name__ == "__main__":
    probar_conteo_insignias()
