# -*- coding: utf-8 -*-
from bd import obtener_conexion

conn = obtener_conexion()
cursor = conn.cursor()

cursor.execute('''
    SELECT id_sala, pin_sala, modo_juego, estado, LENGTH(pin_sala) as longitud 
    FROM salas_juego 
    WHERE modo_juego = 'individual' 
    ORDER BY id_sala DESC 
    LIMIT 10
''')

print("\n🔍 SALAS INDIVIDUALES/AUTOMÁTICAS:")
print("=" * 80)
print(f"{'ID':<5} | {'PIN':<15} | {'Modo':<12} | {'Estado':<12} | {'Longitud':<8}")
print("-" * 80)

for row in cursor.fetchall():
    id_sala, pin_sala, modo, estado, longitud = row
    
    # Verificar si es formato correcto
    es_correcto = pin_sala.startswith('AUTO') and longitud == 8 if longitud >= 4 else False
    estado_formato = "✅ CORRECTO" if es_correcto else "❌ INCORRECTO"
    
    print(f"{id_sala:<5} | {pin_sala:<15} | {modo:<12} | {estado:<12} | {longitud:<8} {estado_formato}")

print("=" * 80)

# Contar cuántas están mal formateadas
cursor.execute('''
    SELECT COUNT(*) FROM salas_juego 
    WHERE modo_juego = 'individual' 
    AND (LENGTH(pin_sala) != 8 OR pin_sala NOT LIKE 'AUTO%')
''')
mal_formateadas = cursor.fetchone()[0]

cursor.execute('''
    SELECT COUNT(*) FROM salas_juego 
    WHERE modo_juego = 'individual' 
    AND LENGTH(pin_sala) = 8 AND pin_sala LIKE 'AUTO%'
''')
bien_formateadas = cursor.fetchone()[0]

print(f"\n📊 RESUMEN:")
print(f"   ✅ Bien formateadas (AUTO + 4 chars): {bien_formateadas}")
print(f"   ❌ Mal formateadas: {mal_formateadas}")

conn.close()
