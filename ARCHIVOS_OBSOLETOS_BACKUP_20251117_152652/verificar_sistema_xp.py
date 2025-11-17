"""
Script de verificación del sistema XP
"""
from bd import obtener_conexion

def verificar_sistema():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        print("\n📊 VERIFICACIÓN DEL SISTEMA XP")
        print("=" * 50)
        
        # Verificar tablas
        tablas_requeridas = [
            'experiencia_usuarios',
            'insignias_catalogo', 
            'insignias_usuarios',
            'estadisticas_juego',
            'historial_xp'
        ]
        
        print("\n✅ TABLAS:")
        for tabla in tablas_requeridas:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"  ✓ {tabla}: {count} registros")
            else:
                print(f"  ❌ {tabla}: NO EXISTE")
        
        # Verificar vista
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        vistas = cursor.fetchall()
        print("\n📈 VISTAS:")
        if any('ranking_xp' in v[0] for v in vistas):
            print("  ✓ ranking_xp: OK")
        else:
            print("  ⚠️ ranking_xp: NO ENCONTRADA")
        
        # Verificar insignias
        cursor.execute("SELECT tipo, COUNT(*) FROM insignias_catalogo GROUP BY tipo")
        print("\n🏆 INSIGNIAS POR TIPO:")
        for tipo, count in cursor.fetchall():
            print(f"  {tipo}: {count} insignias")
        
        # Verificar triggers
        cursor.execute("SHOW TRIGGERS LIKE 'crear_experiencia_nuevo_estudiante'")
        if cursor.fetchone():
            print("\n⚙️ TRIGGER: ✓ crear_experiencia_nuevo_estudiante")
        else:
            print("\n⚙️ TRIGGER: ⚠️ No encontrado")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ Sistema XP verificado correctamente\n")
        
    except Exception as e:
        print(f"\n❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verificar_sistema()
