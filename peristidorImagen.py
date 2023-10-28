import sqlite3
from sqlite3 import Error

def crear_conexion(base_datos):
    conexion = None
    try:
        conexion = sqlite3.connect(base_datos)
        return conexion
    except Error as e:
        print(e)
    return conexion

conexion = crear_conexion("mi_base_de_datos.db")

def crear_tabla(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS imagenes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                imagen BLOB NOT NULL
            )
        """)
        conexion.commit()
    except Error as e:
        print(e)

crear_tabla(conexion)


def leer_imagen(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        imagen = archivo.read()
    return imagen

"""ruta_imagen = 'perro.jpg'  # Reemplaza esto con la ruta de tu imagen"""



def insertar_imagen(conexion, nombre, imagen):
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO imagenes (nombre, imagen) VALUES (?, ?)", (nombre, imagen))
        conexion.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)




def obtener_imagen_por_id(conexion, id):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT imagen FROM imagenes WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
    except Error as e:
        print(e)




imagen = leer_imagen('perro.jpg')

nombre_imagen = 'perro.jpg'  # Reemplaza esto con el nombre que desees
id_imagen = insertar_imagen(conexion, nombre_imagen, imagen)

imagen_recuperada = obtener_imagen_por_id(conexion, id_imagen)
