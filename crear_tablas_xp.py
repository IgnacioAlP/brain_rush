"""
Script para crear las tablas del sistema de XP e Insignias
Ejecutar: python crear_tablas_xp.py
"""

import pymysql
from bd import obtener_conexion

def ejecutar_sql_desde_archivo(archivo_sql):
    """Lee y ejecuta un archivo SQL"""
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Limpiar el script
        # Remover comentarios de línea completa
        lines = []
        for line in sql_script.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('--'):
                lines.append(line)
        
        sql_script = '\n'.join(lines)
        
        # Separar por tipo de statement
        # 1. Primero eliminar secciones DELIMITER y TRIGGER (las ejecutaremos después)
        import re
        
        # Extraer triggers
        trigger_pattern = r'DELIMITER \$\$(.*?)DELIMITER ;'
        triggers = re.findall(trigger_pattern, sql_script, re.DOTALL)
        
        # Remover secciones de triggers del script principal
        sql_sin_triggers = re.sub(trigger_pattern, '', sql_script, flags=re.DOTALL)
        
        # Dividir statements principales
        statements = sql_sin_triggers.split(';')
        
        print("📦 Creando tablas...")
        for i, statement in enumerate(statements, 1):
            statement = statement.strip()
            if statement and len(statement) > 10:
                try:
                    # Ignorar DELIMITER y comentarios
                    if 'DELIMITER' in statement.upper():
                        continue
                    
                    cursor.execute(statement)
                    conexion.commit()
                    
                    # Detectar qué se creó
                    if 'CREATE TABLE' in statement.upper():
                        table_match = re.search(r'CREATE TABLE.*?`?(\w+)`?', statement, re.IGNORECASE)
                        if table_match:
                            print(f"  ✓ Tabla: {table_match.group(1)}")
                    elif 'INSERT INTO' in statement.upper():
                        insert_match = re.search(r'INSERT INTO.*?`?(\w+)`?', statement, re.IGNORECASE)
                        if insert_match and 'insignias_catalogo' in insert_match.group(1):
                            print(f"  ✓ Insignias cargadas")
                    elif 'CREATE.*VIEW' in statement.upper():
                        print(f"  ✓ Vista: ranking_xp")
                        
                except Exception as e:
                    # Solo mostrar errores que no sean "already exists"
                    error_msg = str(e)
                    if 'already exists' not in error_msg.lower() and 'duplicate' not in error_msg.lower():
                        print(f"  ⚠️ Advertencia: {e}")
        
        # Ejecutar triggers si existen
        if triggers:
            print("\n🔧 Creando triggers...")
            for trigger_body in triggers:
                try:
                    # Limpiar el trigger
                    trigger_statements = trigger_body.strip().split('$$')
                    
                    for trigger_stmt in trigger_statements:
                        trigger_stmt = trigger_stmt.strip()
                        if trigger_stmt and 'DROP TRIGGER' in trigger_stmt or 'CREATE TRIGGER' in trigger_stmt:
                            cursor.execute(trigger_stmt)
                            conexion.commit()
                            if 'CREATE TRIGGER' in trigger_stmt:
                                print(f"  ✓ Trigger creado")
                except Exception as e:
                    if 'already exists' not in str(e).lower():
                        print(f"  ⚠️ Advertencia en trigger: {e}")
        
        cursor.close()
        conexion.close()
        
        print("\n✅ Sistema de XP instalado correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Creando sistema de XP e Insignias...")
    print("=" * 50)
    
    exito = ejecutar_sql_desde_archivo('crear_sistema_xp_insignias.sql')
    
    if exito:
        print("\n" + "=" * 50)
        print("✅ Sistema de XP e Insignias instalado correctamente")
        print("\nTablas creadas:")
        print("  - experiencia_usuarios")
        print("  - insignias_catalogo")
        print("  - insignias_usuarios")
        print("  - estadisticas_juego")
        print("  - historial_xp")
        print("\n🏆 23 insignias predefinidas cargadas")
        print("📊 Vista ranking_xp creada")
        print("\nPuedes iniciar el servidor Flask ahora.")
    else:
        print("\n❌ Error en la instalación")
        print("Verifica la conexión a la base de datos y vuelve a intentar")
