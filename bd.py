import pymysql

def verificar_conexion():
    """Verifica si se puede establecer conexión con la base de datos"""
    try:
        conexion = obtener_conexion()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return False

def inicializar_usuarios_prueba():
    """Inicializa usuarios de prueba si no existen"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Verificar si ya existe un usuario admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'admin@brainrush.com'")
        if cursor.fetchone()[0] == 0:
            # Insertar usuario admin
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellidos, email, contraseña_hash, tipo_usuario) 
                VALUES ('Administrador', 'Sistema', 'admin@brainrush.com', 'admin123', 'administrador')
            """)
        
        # Verificar si ya existe un usuario docente de prueba
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'docente@brainrush.com'")
        if cursor.fetchone()[0] == 0:
            # Insertar usuario docente
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellidos, email, contraseña_hash, tipo_usuario) 
                VALUES ('Docente', 'Prueba', 'docente@brainrush.com', 'docente123', 'docente')
            """)
        
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al inicializar usuarios de prueba: {str(e)}")
        if 'conexion' in locals():
            conexion.close()
        return False

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='',
                                db='brain_rush')