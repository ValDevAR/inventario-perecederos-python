# Inventario de Productos Perecederos

Sistema simple en Python + MySQL para gestionar productos perecederos (agregar, listar, actualizar, eliminar, controlar fechas de vencimiento, etc.)

## Tecnologías utilizadas

- Python 3
- MySQL / MariaDB
- mysql-connector-python
- python-dotenv (para manejar las credenciales de forma segura)

## Requisitos previos

1. Tener **Python 3.8 o superior** instalado
2. Tener **MySQL** o **MariaDB** instalado y corriendo
3. Crear una base de datos (por ejemplo: `inventario_perecederos`)

## Instalación paso a paso

1. Clonar el repositorio:
Bash
git clone https://github.com/ValDevAR/inventario-perecederos-python.git
cd inventario-perecederos-python

2.Crear y activar un entorno virtual (muy recomendado):
Bash
# Windows
python -m venv venv
venv\Scripts\activate

3.Instalar las dependencias:
Bash
pip install -r requirements.txt

4.Crear el archivo .env en la raíz del proyecto con tus datos de MySQL:
env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_aquí
DB_NAME=inventario_perecederos
DB_PORT=3306

5.(Opcional) Crear la base de datos y las tablas si no existen todavía (puedes tener un archivo crear_tablas.sql o hacerlo manualmente).

6.Ejecutar el programa
Bash
python main.py

Funcionalidades principales

Agregar producto
Ver lista de productos
Buscar por nombre o categoría
Actualizar stock
Eliminar producto
Ver productos próximos a vencer (¡lo más útil!)

Capturas de pantalla

<img width="1366" height="768" alt="main" src="https://github.com/user-attachments/assets/045da734-2084-4031-806a-61e6d064ba10" />




git clone https://github.com/ValDevAR/inventario-perecederos-python.git
cd i
nventario-perecederos-python
