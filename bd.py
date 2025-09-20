
import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                port=3327,
                                user='root',
                                password='',
                                db='brain_rush')