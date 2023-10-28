import sqlite3
from sqlite3 import Error

def crear_conexion(base_datos):
    """
    Crea una conexión a la base de datos SQLite.

    :param base_datos: Ruta al archivo de la base de datos SQLite.
    :return: Objeto de conexión SQLite.
    
    Ejemplo:
    
    >>> conexion = crear_conexion("mi_base_de_datos.db")
    >>> type(conexion)
    <class 'sqlite3.Connection'>
    """
    conexion = None
    try:
        conexion = sqlite3.connect(base_datos)
        return conexion
    except Error as e:
        print(e)
    return conexion

conexion = crear_conexion("test.db")

def crear_tabla(conexion):
    """
    Crea una tabla en la base de datos para almacenar imágenes.

    :param conexion: Objeto de conexión SQLite.
    
    Ejemplo:
    
    >>> crear_tabla(conexion)
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
    except Error as e:
        print(e)

crear_tabla(conexion)

def leer_imagen(ruta_archivo):
    """
    Lee una imagen desde un archivo y la devuelve en forma de bytes.

    :param ruta_archivo: Ruta al archivo de imagen.
    :return: Bytes de la imagen.
    
    Ejemplo:
    
    >>> imagen = leer_imagen('perro.jpg')
    >>> type(imagen)
    <class 'bytes'>
    """
    with open(ruta_archivo, 'rb') as archivo:
        imagen = archivo.read()
    return imagen

def insertar_imagen(conexion, nombre, imagen):
    """
    Inserta una imagen en la base de datos.

    :param conexion: Objeto de conexión SQLite.
    :param nombre: Nombre de la imagen.
    :param imagen: Bytes de la imagen.
    :return: ID de la imagen insertada.
    
    Ejemplo:
    
    >>> imagen_bytes = leer_imagen('perro.jpg')
    >>> nombre_imagen = 'perro.jpg'
    >>> type(nombre_imagen)
    <class 'str'>
    >>> id_imagen = insertar_imagen(conexion, nombre_imagen, imagen_bytes)
    >>> id_imagen
    1
    >>> type(id_imagen)
    <class 'int'>
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO imagenes (nombre, imagen) VALUES (?, ?)", (nombre, imagen))
        conexion.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

def obtener_imagen_por_id(conexion, id):
    """
    Obtiene una imagen de la base de datos por su ID.

    :param conexion: Objeto de conexión SQLite.
    :param id: ID de la imagen.
    :return: Bytes de la imagen recuperada.
    
    Ejemplo:
    
    
    >>> imagen_recuperada = obtener_imagen_por_id(conexion,1)
    >>> type(imagen_recuperada)
    <class 'bytes'>
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT imagen FROM imagenes WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
    except Error as e:
        print(e)
