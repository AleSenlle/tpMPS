import sqlite3
from sqlite3 import Error
import time

def crear_conexion(base_datos):
    """
    Crea una conexión a la base de datos SQLite.

    :param base_datos: Nombre del archivo de la base de datos.
    :return: Objeto de conexión o None si hay un error.
    >>> conexion = crear_conexion(":memory:")
    >>> isinstance(conexion, sqlite3.Connection)
    True
    """
    conexion = None
    try:
        conexion = sqlite3.connect(base_datos)
        return conexion
    except Error as e:
        return None

conexion = crear_conexion("mi_base_de_datos.db")

def crear_tabla(conexion):
    """
    Crea una tabla en la base de datos para almacenar imágenes.

    :param conexion: Objeto de conexión SQLite.
    
    Ejemplo:
    
    >>> conexion = crear_conexion(":memory:")
    >>> crear_tabla(conexion)
    True
    """
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
        return True
    except Error as e:
        return False

crear_tabla(conexion)

ruta_imagen = './perro.jpg'

def leer_imagen(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        imagen = archivo.read()
    return imagen

imagen = leer_imagen(ruta_imagen)

def insertar_imagen(conexion, nombre, imagen):
    """
    Inserta una imagen en la base de datos.

    :param conexion: Objeto de conexión a la base de datos.
    :param nombre: Nombre de la imagen.
    :param imagen: Datos de la imagen en formato BLOB.
    :return: ID de la imagen insertada.
    >>> id_imagen = insertar_imagen(conexion, 'perro.jpg', imagen)
    >>> isinstance(id_imagen, int)
    True
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO imagenes (nombre, imagen) VALUES (?, ?)", (nombre, imagen))
        conexion.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

id_imagen = insertar_imagen(conexion, 'perro.jpg', imagen)

def obtener_imagen_por_id(conexion, id):
    """
    Recupera una imagen de la base de datos por ID.

    :param conexion: Objeto de conexión a la base de datos.
    :param id: ID de la imagen a recuperar.
    :return: Datos de la imagen en formato BLOB.
    >>> imagen_recuperada = obtener_imagen_por_id(conexion, id_imagen)
    >>> isinstance(imagen_recuperada, bytes)
    True

    Ejemplo de tipo de resultado:
    
    >>> type(imagen_recuperada)
    <class 'bytes'>

     Obtiene una imagen de la base de datos por su ID y verifica el rendimiento.

    :param conexion: Objeto de conexión SQLite.
    :param id: ID de la imagen.
    :return: Bytes de la imagen recuperada.
    
    Ejemplo de rendimiento:
    
    >>> start_time = time.time()
    >>> imagen_recuperada = obtener_imagen_por_id(conexion, 1)
    >>> end_time = time.time()
    >>> elapsed_time = end_time - start_time
    >>> elapsed_time < 1.0  # Verifica que la función se ejecute en menos de 1 segundo
    True
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT imagen FROM imagenes WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
    except Error as e:
        print(e)

imagen_recuperada = obtener_imagen_por_id(conexion, id_imagen)

if __name__ == "__main__":
    import doctest
    doctest.testmod()