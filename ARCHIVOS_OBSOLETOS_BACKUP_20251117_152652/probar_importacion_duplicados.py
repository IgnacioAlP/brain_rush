# -*- coding: utf-8 -*-
"""
Script para probar la importación de preguntas duplicadas
Verifica que no se dupliquen las preguntas al importar el mismo archivo dos veces
"""

from bd import obtener_conexion

def verificar_duplicados():
    """Verifica si hay preguntas duplicadas en un cuestionario"""
    conexion = obtener_conexion()
    
    print("\n=== VERIFICACIÓN DE PREGUNTAS DUPLICADAS ===\n")
    
    try:
        with conexion.cursor() as cursor:
            # Buscar preguntas duplicadas en cada cuestionario
            cursor.execute("""
                SELECT 
                    c.id_cuestionario,
                    c.titulo,
                    p.enunciado,
                    COUNT(*) as cantidad
                FROM cuestionario_preguntas cp
                INNER JOIN cuestionarios c ON cp.id_cuestionario = c.id_cuestionario
                INNER JOIN preguntas p ON cp.id_pregunta = p.id_pregunta
                GROUP BY c.id_cuestionario, c.titulo, p.enunciado
                HAVING COUNT(*) > 1
                ORDER BY c.id_cuestionario, cantidad DESC
            """)
            
            duplicados = cursor.fetchall()
            
            if duplicados:
                print(f"⚠️ Se encontraron {len(duplicados)} preguntas duplicadas:\n")
                for dup in duplicados:
                    id_cuestionario, titulo, enunciado, cantidad = dup
                    print(f"📝 Cuestionario #{id_cuestionario} '{titulo}':")
                    print(f"   Pregunta: '{enunciado[:60]}...'")
                    print(f"   Aparece: {cantidad} veces\n")
            else:
                print("✅ No se encontraron preguntas duplicadas\n")
            
            # Mostrar resumen por cuestionario
            print("\n=== RESUMEN POR CUESTIONARIO ===\n")
            cursor.execute("""
                SELECT 
                    c.id_cuestionario,
                    c.titulo,
                    COUNT(DISTINCT cp.id_pregunta) as total_preguntas
                FROM cuestionarios c
                LEFT JOIN cuestionario_preguntas cp ON c.id_cuestionario = cp.id_cuestionario
                GROUP BY c.id_cuestionario, c.titulo
                ORDER BY c.id_cuestionario
            """)
            
            cuestionarios = cursor.fetchall()
            for cuest in cuestionarios:
                id_cuest, titulo, total = cuest
                print(f"📚 Cuestionario #{id_cuest}: '{titulo}'")
                print(f"   Total de preguntas: {total}\n")
                
    finally:
        conexion.close()

if __name__ == "__main__":
    verificar_duplicados()
