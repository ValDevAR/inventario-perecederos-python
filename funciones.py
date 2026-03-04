# funciones.py
from datetime import date, timedelta, datetime
import database
from config import DIAS_ADVERTENCIA_CADUCIDAD, DIAS_CRITICO_CADUCIDAD, CANTIDAD_MINIMA_STOCK


def agregar_producto(nombre, categoria=None, precio_unitario=0.0, fecha_vencimiento=None, stock_inicial=0, stock_minimo=5):
    if not nombre.strip():
        return False, "El nombre es obligatorio"

    query = """
    INSERT INTO productos 
    (nombre, categoria, precio_unitario, fecha_vencimiento, stock_actual, stock_minimo)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        nombre.strip(),
        categoria.strip() if categoria else None,
        float(precio_unitario),
        fecha_vencimiento,
        stock_inicial,
        stock_minimo
    )

    ok, msg = database.execute_query(query, params, commit=True)
    if not ok:
        return False, msg

    producto_id = ok  # lastrowid
    if stock_inicial > 0:
        registrar_movimiento(producto_id, 'entrada', stock_inicial, 'Ingreso inicial')

    return True, f"Producto agregado correctamente (ID: {producto_id})"


def registrar_movimiento(id_producto, tipo, cantidad, descripcion=""):
    tipo = tipo.lower().strip()
    if tipo not in ['entrada', 'salida']:
        return False, "Tipo inválido (solo 'entrada' o 'salida')"

    if tipo == 'salida':
        rows, _ = database.execute_query(
            "SELECT stock_actual FROM productos WHERE id_producto = %s",
            (id_producto,), fetch=True
        )
        if not rows or rows[0]['stock_actual'] < cantidad:
            return False, "Stock insuficiente"

    delta = cantidad if tipo == 'entrada' else -cantidad
    ok, msg = database.execute_query(
        "UPDATE productos SET stock_actual = stock_actual + %s WHERE id_producto = %s",
        (delta, id_producto), commit=True
    )
    if not ok:
        return False, msg

    query_mov = """
    INSERT INTO movimientos 
    (id_producto, tipo, cantidad, fecha, descripcion)
    VALUES (%s, %s, %s, CURDATE(), %s)
    """
    ok, msg = database.execute_query(
        query_mov,
        (id_producto, tipo, cantidad, descripcion.strip()),
        commit=True
    )
    
    return ok, "Movimiento registrado" if ok else msg


def eliminar_producto(id_producto):
    query = "DELETE FROM productos WHERE id_producto = %s"
    ok, msg = database.execute_query(query, (id_producto,), commit=True)
    return ok, "Producto eliminado correctamente" if ok else msg


def listar_productos():
    query = """
    SELECT id_producto, nombre, categoria, precio_unitario, fecha_vencimiento, stock_actual, stock_minimo
    FROM productos
    ORDER BY nombre ASC
    """
    rows, _ = database.execute_query(query, fetch=True)
    return rows or []


def obtener_productos_por_vencer(dias=7):
    fecha_limite = date.today() + timedelta(days=dias)
    query = """
    SELECT id_producto, nombre, categoria, fecha_vencimiento, 
           DATEDIFF(fecha_vencimiento, CURDATE()) AS dias_restantes,
           stock_actual, stock_minimo
    FROM productos
    WHERE fecha_vencimiento IS NOT NULL
      AND fecha_vencimiento <= %s
      AND fecha_vencimiento >= CURDATE()
    ORDER BY fecha_vencimiento ASC
    """
    rows, _ = database.execute_query(query, (fecha_limite,), fetch=True)
    return rows or []


def obtener_productos_vencidos():
    query = """
    SELECT id_producto, nombre, categoria, fecha_vencimiento, stock_actual
    FROM productos
    WHERE fecha_vencimiento IS NOT NULL
      AND fecha_vencimiento < CURDATE()
    ORDER BY fecha_vencimiento DESC
    """
    rows, _ = database.execute_query(query, fetch=True)
    return rows or []


def obtener_alerta_stock_bajo():
    query = """
    SELECT id_producto, nombre, categoria, stock_actual, stock_minimo
    FROM productos
    WHERE stock_actual <= stock_minimo
    ORDER BY stock_actual ASC
    """
    rows, _ = database.execute_query(query, fetch=True)
    return rows or []


def obtener_productos_para_combo():
    query = """
    SELECT id_producto, nombre 
    FROM productos 
    ORDER BY nombre ASC
    """
    rows, _ = database.execute_query(query, fetch=True)
    return [(row['nombre'], row['id_producto']) for row in rows] if rows else []


def obtener_id_por_nombre(nombre):
    query = "SELECT id_producto FROM productos WHERE nombre = %s LIMIT 1"
    rows, _ = database.execute_query(query, (nombre,), fetch=True)
    return rows[0]['id_producto'] if rows else None


def convertir_fecha_ddmmaaaa_a_yyyymmdd(fecha_str):
    try:
        dt = datetime.strptime(fecha_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None
