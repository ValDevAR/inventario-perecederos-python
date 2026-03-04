# config.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'inventario_perecederos',
    'port': 3306,
    'raise_on_warnings': True
}

DIAS_ADVERTENCIA_CADUCIDAD = 7
DIAS_CRITICO_CADUCIDAD    = 3
CANTIDAD_MINIMA_STOCK     = 5