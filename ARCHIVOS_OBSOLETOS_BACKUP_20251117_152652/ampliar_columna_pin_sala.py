# -*- coding: utf-8 -*-
"""
Script para ampliar la columna pin_sala de VARCHAR(6) a VARCHAR(8)
para soportar PINs de modo automático (AUTOXXXX)
"""

from bd import obtener_conexion

def ampliar_columna_pin_sala():
    print("🔧 AMPLIANDO COLUMNA pin_sala")
    print("=" * 60)
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        # Verificar el tamaño actual
        cursor.execute("DESCRIBE salas_juego")
        columnas = cursor.fetchall()
        pin_col = [c for c in columnas if c[0] == 'pin_sala'][0]
        
        print(f"\n📋 ESTADO ACTUAL:")
        print(f"   Columna: pin_sala")
        print(f"   Tipo: {pin_col[1]}")
        
        if 'varchar(6)' in pin_col[1].lower():
            print(f"\n⚠️ La columna está limitada a 6 caracteres")
            print(f"   Esto trunca los PINs de modo automático (AUTOXXXX = 8 chars)")
            
            print(f"\n🔄 Modificando columna a VARCHAR(8)...")
            cursor.execute('''
                ALTER TABLE salas_juego 
                MODIFY COLUMN pin_sala VARCHAR(8) NOT NULL
            ''')
            conexion.commit()
            
            print(f"   ✅ Columna modificada exitosamente")
            
            # Verificar el cambio
            cursor.execute("DESCRIBE salas_juego")
            columnas = cursor.fetchall()
            pin_col = [c for c in columnas if c[0] == 'pin_sala'][0]
            
            print(f"\n📋 ESTADO NUEVO:")
            print(f"   Columna: pin_sala")
            print(f"   Tipo: {pin_col[1]}")
            print(f"   ✅ Ahora puede almacenar hasta 8 caracteres")
            
        else:
            print(f"\n✅ La columna ya tiene el tamaño adecuado")
        
        cursor.close()
        conexion.close()
        
        print("\n" + "=" * 60)
        print("✅ Proceso completado")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if conexion:
            conexion.rollback()
            conexion.close()

if __name__ == "__main__":
    ampliar_columna_pin_sala()
