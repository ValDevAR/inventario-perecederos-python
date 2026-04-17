 # 📦 Inventario de Productos Perecederos

**Sistema de gestión de inventario** desarrollado en **Python** con interfaz gráfica moderna.  
Especialmente diseñado para controlar **productos perecederos** (alimentos, lácteos, medicamentos, cosméticos, etc.).  
Permite llevar un seguimiento del stock y recibir **alertas automáticas** cuando los productos están próximos a vencer.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-%2300A4EF?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?style=flat-square&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ Características principales

- ➕ Agregar nuevos productos con fecha de vencimiento
- 📋 Listar todos los productos con stock actual
- 🔎 Buscar productos por nombre o categoría
- ✏️ Actualizar stock y datos del producto
- 🗑️ Eliminar productos
- 🚨 **Alertas automáticas** de productos próximos a vencer (con cambios de color)
- 🎨 Interfaz gráfica moderna y fácil de usar con **CustomTkinter**
- 🗄️ Conexión segura a base de datos MySQL / MariaDB

## 🛠 Tecnologías utilizadas

- **Python 3.8 o superior**
- **CustomTkinter** – Interfaz gráfica moderna
- **MySQL / MariaDB** – Base de datos
- **mysql-connector-python**
- **python-dotenv** – Manejo seguro de credenciales

## 📸 Capturas de pantalla

<img src="https://github.com/user-attachments/assets/045da734-2084-4031-806a-61e6d064ba10" width="800" alt="Pantalla principal">

*(Próximamente: más capturas y GIF demostrando las alertas)*

## 🚀 Instalación y ejecución

Sigue estos pasos para probar el sistema:

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/ValDevAR/inventario-perecederos-python.git
   cd inventario-perecederos-python
2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
3. **Configura la conexión a la base de datos**
   ```bash
   Crea un archivo .env en la raíz del proyecto:
   
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=tu_contraseña_aquí
   DB_NAME=inventario_perecederos
   DB_PORT=3306
5. **Ejecuta el programa**
   ```bash
   python main.py

Nota: La primera vez que ejecutes el programa, se creará automáticamente la base de datos y las tablas necesarias.
   
📋 Requisitos previos

Python 3.8 o superior
MySQL o MariaDB instalado y en ejecución
Una base de datos creada (recomendado: inventario_perecederos)

🤝 Cómo contribuir
Las contribuciones son bienvenidas. Si quieres mejorar el proyecto:

Haz fork del repositorio
Crea una rama nueva (git checkout -b feature/nueva-mejora)
Realiza tus cambios y haz commit
Abre un Pull Request

📄 Licencia
Este proyecto está bajo la licencia MIT.
