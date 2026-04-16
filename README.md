 # 📦 Inventario de Productos Perecederos

Sistema de gestión de inventario desarrollado en **Python** con interfaz gráfica moderna.  
Especialmente diseñado para controlar productos perecederos (alimentos, lácteos, medicamentos, cosméticos, etc.), permitiendo llevar un seguimiento del stock y recibir alertas cuando los productos están próximos a vencer.

## ✨ Características principales

- Agregar nuevos productos con fecha de vencimiento
- Listar todos los productos
- Buscar productos por nombre o categoría
- Actualizar stock y datos del producto
- Eliminar productos
- **Alertas automáticas** de productos próximos a vencer
- Interfaz gráfica moderna y fácil de usar (CustomTkinter)
- Conexión segura con base de datos MySQL / MariaDB

## 🛠 Tecnologías utilizadas

- Python 3.8 o superior
- CustomTkinter (para la interfaz gráfica)
- MySQL / MariaDB
- mysql-connector-python
- python-dotenv (para manejar credenciales de forma segura)

## Requisitos previos

- Python 3.8 o superior
- MySQL o MariaDB instalado y corriendo
- Una base de datos creada (recomendado: `inventario_perecederos`)

## 🚀 Instalación y ejecución

Sigue estos pasos para poder ejecutar el programa:

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/ValDevAR/inventario-perecederos-python.git
   cd inventario-perecederos-python
   
2. **Instala las dependencias**
   pip install -r requirements.txt

4. **Configura la conexión a la base de datos**
   ```bash
   Crea un archivo llamado .env en la raíz del proyecto con el siguiente contenido:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=tu_contraseña_aquí
   DB_NAME=inventario_perecederos
   DB_PORT=3306
   
6. **Ejecuta el programa**
   ```bash
   python main.py

## 📸 Capturas de pantalla
<img src="https://github.com/user-attachments/assets/045da734-2084-4031-806a-61e6d064ba10" width="800" alt="Pantalla principal">

