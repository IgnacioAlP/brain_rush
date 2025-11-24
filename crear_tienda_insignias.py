"""
Script para crear la tienda de insignias
"""
from bd import obtener_conexion

def crear_tienda():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        print("\n🏪 CREANDO TIENDA DE INSIGNIAS")
        print("=" * 60)
        
        # Leer archivo SQL
        with open('crear_tienda_insignias.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Separar por punto y coma
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"✓ Ejecutado correctamente")
                except Exception as e:
                    if 'Duplicate column' in str(e):
                        print(f"⚠️  Columna ya existe (ignorando)")
                    else:
                        print(f"⚠️  {e}")
        
        conn.commit()
        
        # Verificar insignias comprables
        cursor.execute("SELECT COUNT(*) FROM insignias_catalogo WHERE precio_xp > 0")
        comprables = cursor.fetchone()[0]
        
        print("\n" + "=" * 60)
        print(f"✅ TIENDA CREADA")
        print(f"   • Insignias comprables: {comprables}")
        print(f"   • Tabla de compras: ✓")
        print("\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    crear_tienda()
