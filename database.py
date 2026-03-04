# database.py
import mysql.connector
from mysql.connector import Error
import config


def get_connection():
    try:
        conn = mysql.connector.connect(**config.DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Error al conectar a MySQL: {err}")
        return None


def execute_query(query, params=None, fetch=False, commit=False):
    """Función auxiliar para ejecutar consultas de forma más limpia"""
    conn = get_connection()
    if not conn:
        return None, "No se pudo conectar a la base de datos"

    cursor = conn.cursor(dictionary=True) if fetch else conn.cursor()

    try:
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else True, "OK"
        if fetch:
            return cursor.fetchall(), "OK"
        return True, "OK"
    except Error as err:
        if conn.is_connected():
            conn.rollback()
        return None, str(err)
    finally:
        cursor.close()
        conn.close()
