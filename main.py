# main.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
import database
import funciones
from config import DIAS_ADVERTENCIA_CADUCIDAD

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class InventarioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventario Perecederos - Valeria")
        self.geometry("1200x850")
        self.geometry("1100x750")
        # ...
        self.tabview = ctk.CTkTabview(self, width=950, height=520)
        self.resizable(True,True)

        try:
            self.iconbitmap("icono.ico")
        except:
            pass

        self.productos_combo = []
        self.actualizar_lista_productos()

        if not database.get_connection():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.\nRevisa config.py")
            self.destroy()
            return

        self.crear_widgets()

    def crear_widgets(self):
        self.header = ctk.CTkLabel(self, text="Gestión de Productos Perecederos", font=("Segoe UI", 22, "bold"))
        self.header.pack(pady=(5, 5))

        self.tabview = ctk.CTkTabview(self, width=950, height=520)
        self.tabview.pack(pady=(0, 5), padx=20, fill="both", expand=True)

        self.tab_abm = self.tabview.add("Agregar / Eliminar")
        self.crear_pestana_abm()

        self.tab_listado = self.tabview.add("Listado")
        self.crear_pestana_listado()

        self.tab_vencer = self.tabview.add("Próximos a vencer")
        self.crear_pestana_vencer()

        self.tab_vencidos = self.tabview.add("Ya vencidos")
        self.crear_pestana_vencidos()

        self.tab_bajo = self.tabview.add("Stock bajo")
        self.crear_pestana_bajo()

        self.btn_refresh = ctk.CTkButton(self, text="Actualizar todo", command=self.actualizar_todas_las_pestanas)
        self.btn_refresh.pack(pady=10)

    
    def crear_pestana_abm(self):

        frame = ctk.CTkFrame(self.tab_abm)
        frame.pack(padx=20, pady=(5, 10), fill="both", expand=True)

        ctk.CTkLabel(frame, text="Gestión de Productos", font=("Segoe UI", 18, "bold")).pack(pady=(5, 5))

        # Contenedor de las tres columnas
        columns = ctk.CTkFrame(frame)
        columns.pack(fill="both", expand=True, pady=(4, 4))

        # ────────────────────── 1. AGREGAR ──────────────────────
                # Columna AGREGAR (reemplaza esta parte completa)

        add_frame = ctk.CTkFrame(columns, border_width=1, border_color="#2ecc71")
        add_frame.pack(side="left", padx=6, pady=5, fill="both", expand=True)

        ctk.CTkLabel(add_frame, text="Agregar producto", font=("Segoe UI", 14, "bold")).pack(pady=(8, 6))

        ctk.CTkLabel(add_frame, text="Nombre:").pack(anchor="w", padx=12, pady=(2,0))
        self.entry_nombre = ctk.CTkEntry(add_frame, width=280, height=26)
        self.entry_nombre.pack(pady=3, padx=12, fill="x")

        ctk.CTkLabel(add_frame, text="Categoría:").pack(anchor="w", padx=12, pady=(4,0))
        self.combo_categoria = ctk.CTkComboBox(
            add_frame,
            values=["Almacén", "Bebidas", "Lácteos", "Frutas", "Verduras", "Congelados", "Otros"],
            width=280,
            height=26
        )
        self.combo_categoria.set("Selecciona categoría")
        self.combo_categoria.pack(pady=3, padx=12, fill="x")

        ctk.CTkLabel(add_frame, text="Precio unitario:").pack(anchor="w", padx=12, pady=(4,0))
        self.entry_precio = ctk.CTkEntry(add_frame, width=280, height=26)
        self.entry_precio.pack(pady=3, padx=12, fill="x")

        ctk.CTkLabel(add_frame, text="Fecha venc.:").pack(anchor="w", padx=12, pady=(4,0))
        self.entry_venc = ctk.CTkEntry(add_frame, width=280, height=26)
        self.entry_venc.pack(pady=3, padx=12, fill="x")

        ctk.CTkLabel(add_frame, text="Stock inicial:").pack(anchor="w", padx=12, pady=(4,0))
        self.entry_stock_ini = ctk.CTkEntry(add_frame, width=280, height=26)
        self.entry_stock_ini.pack(pady=3, padx=12, fill="x")

        ctk.CTkLabel(add_frame, text="Stock mínimo:").pack(anchor="w", padx=12, pady=(4,0))
        self.entry_stock_min = ctk.CTkEntry(add_frame, width=280, height=26)
        self.entry_stock_min.pack(pady=3, padx=12, fill="x")

        ctk.CTkButton(
            add_frame,
            text="Guardar producto",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=32,
            font=("Segoe UI", 12),
            command=self.agregar_producto_gui
        ).pack(pady=(10, 10), padx=25, fill="x")

        # ────────────────────── 2. ELIMINAR ──────────────────────
        del_frame = ctk.CTkFrame(columns, border_width=1, border_color="#e74c3c")
        del_frame.pack(side="left", padx=8, pady=5, fill="both", expand=True)

        ctk.CTkLabel(del_frame, text="Eliminar producto", font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))

        ctk.CTkLabel(del_frame, text="Producto:").pack(anchor="w", padx=15, pady=(20,5))
        self.combo_eliminar = ctk.CTkComboBox(del_frame, values=[n for n,_ in self.productos_combo], width=300)
        self.combo_eliminar.set("Selecciona un producto...")
        self.combo_eliminar.pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(
            del_frame,
            text="Eliminar seleccionado",
            fg_color="#e74c3c",
            hover_color="#c0392d",
            command=self.eliminar_producto_gui
        ).pack(pady=(50, 20), padx=20, fill="x")   # más pady para centrar visualmente

        # ────────────────────── 3. MOVIMIENTOS ──────────────────────
        mov_frame = ctk.CTkFrame(columns, border_width=1, border_color="#3498db")
        mov_frame.pack(side="left", padx=8, pady=5, fill="both", expand=True)

        ctk.CTkLabel(mov_frame, text="Registrar movimiento", font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))

        ctk.CTkLabel(mov_frame, text="Producto:").pack(anchor="w", padx=15, pady=(10,5))
        self.combo_mov_producto = ctk.CTkComboBox(mov_frame, values=[n for n,_ in self.productos_combo], width=300)
        self.combo_mov_producto.set("Selecciona un producto...")
        self.combo_mov_producto.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(mov_frame, text="Tipo:").pack(anchor="w", padx=15, pady=(10,5))
        self.combo_tipo = ctk.CTkComboBox(mov_frame, values=["entrada", "salida"], width=180)
        self.combo_tipo.set("entrada")
        self.combo_tipo.pack(anchor="w", pady=5, padx=15)

        ctk.CTkLabel(mov_frame, text="Cantidad:").pack(anchor="w", padx=15, pady=(10,5))
        self.entry_cant_mov = ctk.CTkEntry(mov_frame, width=180)
        self.entry_cant_mov.pack(anchor="w", pady=5, padx=15)

        ctk.CTkButton(
            mov_frame,
            text="Registrar movimiento",
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.registrar_movimiento_gui
        ).pack(pady=(30, 20), padx=20, fill="x")

    def limpiar_form_alta(self):
        self.entry_nombre.delete(0, "end")
        self.combo_categoria.set("Selecciona categoría")
        self.entry_precio.delete(0, "end")
        self.entry_venc.delete(0, "end")
        self.entry_stock_ini.delete(0, "end")
        self.entry_stock_min.delete(0, "end")

    def agregar_producto_gui(self):
        
        try:
            nombre = self.entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "El nombre es obligatorio")
                return

            categoria = self.combo_categoria.get()
            if categoria == "Selecciona categoría":
                categoria = None
            else:
                categoria = categoria.strip()

            precio_str = self.entry_precio.get().strip()
            precio = 0.0
            if precio_str:
                precio = float(precio_str.replace(',', '.'))

            venc_str = self.entry_venc.get().strip()
            venc = None
            if venc_str:
                venc = funciones.convertir_fecha_ddmmaaaa_a_yyyymmdd(venc_str)
                if not venc:
                    messagebox.showwarning("Atención", "Fecha inválida (usa dd/mm/aaaa)")
                    return

            stock_ini = 0
            stock_ini_str = self.entry_stock_ini.get().strip()
            if stock_ini_str:
                stock_ini = int(stock_ini_str)

            stock_min = 5
            stock_min_str = self.entry_stock_min.get().strip()
            if stock_min_str:
                stock_min = int(stock_min_str)

                ok, msg = funciones.agregar_producto(
                nombre, categoria, precio, venc, stock_ini, stock_min
            )

            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_form_alta()
                self.actualizar_todas_las_pestanas()
            else:
                messagebox.showerror("Error BD", f"No se pudo guardar:\n{msg}")

        except Exception as e:
            messagebox.showerror("Error en agregar", f"Ocurrió un error:\n{str(e)}")

    def eliminar_producto_gui(self):
        nombre = self.combo_eliminar.get().strip()
        if not nombre or nombre == "Selecciona un producto...":
            messagebox.showwarning("Atención", "Debes seleccionar un producto para eliminar")
            return

        id_prod = funciones.obtener_id_por_nombre(nombre)
        if not id_prod:
            messagebox.showerror("Error", f"No se encontró ningún producto con nombre:\n{nombre}")
            return

        if not messagebox.askyesno("Confirmar eliminación", 
                                  f"¿Estás segura de eliminar el producto?\n\n"
                                  f"ID: {id_prod}\nNombre: {nombre}\n\n"
                                  f"Esta acción no se puede deshacer."):
            return

        ok, msg = funciones.eliminar_producto(id_prod)
        if ok:
            messagebox.showinfo("Éxito", msg)
            # Limpiar el combobox
            self.combo_eliminar.set("Selecciona un producto...")
            self.actualizar_todas_las_pestanas()
        else:
            messagebox.showerror("Error al eliminar", msg or "No se pudo eliminar el producto")

    def registrar_movimiento_gui(self):
        try:
            nombre = self.combo_mov_producto.get()
            if nombre == "Selecciona un producto...":
                messagebox.showwarning("Atención", "Selecciona un producto")
                return

            id_prod = funciones.obtener_id_por_nombre(nombre)
            tipo = self.combo_tipo.get()
            cantidad = int(self.entry_cant_mov.get() or 0)

            if cantidad <= 0:
                messagebox.showwarning("Atención", "La cantidad debe ser mayor a 0")
                return

            ok, msg = funciones.registrar_movimiento(id_prod, tipo, cantidad, "Desde la aplicación")
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.entry_cant_mov.delete(0, "end")
                self.actualizar_todas_las_pestanas()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")

    # ────────────────────────────────────────────────
    #    Pestañas de visualización (sin cambios importantes)
    # ────────────────────────────────────────────────

    def crear_pestana_listado(self):
        self.tree_listado = ttk.Treeview(self.tab_listado, columns=("ID","Nombre","Cat","Precio","Venc","Stock","Mín"), show="headings")
        self.tree_listado.heading("ID", text="ID")
        self.tree_listado.heading("Nombre", text="Nombre")
        self.tree_listado.heading("Cat", text="Categoría")
        self.tree_listado.heading("Precio", text="Precio")
        self.tree_listado.heading("Venc", text="Vencimiento")
        self.tree_listado.heading("Stock", text="Stock")
        self.tree_listado.heading("Mín", text="Mínimo")
        self.tree_listado.column("ID", width=50)
        self.tree_listado.column("Nombre", width=220)
        self.tree_listado.column("Cat", width=130)
        self.tree_listado.column("Precio", width=90)
        self.tree_listado.column("Venc", width=110)
        self.tree_listado.column("Stock", width=80)
        self.tree_listado.column("Mín", width=80)
        self.tree_listado.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_tab_listado()

    def actualizar_tab_listado(self):
        for item in self.tree_listado.get_children():
            self.tree_listado.delete(item)
        for p in funciones.listar_productos():
            fecha = "-" if not p.get("fecha_vencimiento") else datetime.strptime(str(p["fecha_vencimiento"]), "%Y-%m-%d").strftime("%d/%m/%Y")
            self.tree_listado.insert("", "end", values=(
                p["id_producto"], p["nombre"], p.get("categoria") or "-", 
                p["precio_unitario"], fecha, p["stock_actual"], p["stock_minimo"]
            ))

    def crear_pestana_vencer(self):
        self.tree_vencer = ttk.Treeview(self.tab_vencer, columns=("ID","Nombre","Vence","Días","Stock"), show="headings")
        self.tree_vencer.heading("ID", text="ID")
        self.tree_vencer.heading("Nombre", text="Producto")
        self.tree_vencer.heading("Vence", text="Vence")
        self.tree_vencer.heading("Días", text="Días")
        self.tree_vencer.heading("Stock", text="Stock")
        self.tree_vencer.column("ID", width=50)
        self.tree_vencer.column("Nombre", width=280)
        self.tree_vencer.column("Vence", width=110)
        self.tree_vencer.column("Días", width=70)
        self.tree_vencer.column("Stock", width=80)
        self.tree_vencer.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_tab_vencer()

    def actualizar_tab_vencer(self):
        for item in self.tree_vencer.get_children():
            self.tree_vencer.delete(item)
        prods = funciones.obtener_productos_por_vencer(DIAS_ADVERTENCIA_CADUCIDAD)
        for p in prods:
            fecha = datetime.strptime(str(p["fecha_vencimiento"]), "%Y-%m-%d").strftime("%d/%m/%Y")
            tag = "rojo" if p["dias_restantes"] <= 3 else "amarillo"
            self.tree_vencer.insert("", "end", values=(p["id_producto"], p["nombre"], fecha, p["dias_restantes"], p["stock_actual"]), tags=(tag,))
        self.tree_vencer.tag_configure("rojo", foreground="red")
        self.tree_vencer.tag_configure("amarillo", foreground="orange")

    def crear_pestana_vencidos(self):
        self.tree_vencidos = ttk.Treeview(self.tab_vencidos, columns=("ID","Nombre","Venció","Stock"), show="headings")
        self.tree_vencidos.heading("ID", text="ID")
        self.tree_vencidos.heading("Nombre", text="Producto")
        self.tree_vencidos.heading("Venció", text="Venció")
        self.tree_vencidos.heading("Stock", text="Stock")
        self.tree_vencidos.column("ID", width=50)
        self.tree_vencidos.column("Nombre", width=300)
        self.tree_vencidos.column("Venció", width=110)
        self.tree_vencidos.column("Stock", width=80)
        self.tree_vencidos.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_tab_vencidos()

    def actualizar_tab_vencidos(self):
        for item in self.tree_vencidos.get_children():
            self.tree_vencidos.delete(item)
        for p in funciones.obtener_productos_vencidos():
            fecha = datetime.strptime(str(p["fecha_vencimiento"]), "%Y-%m-%d").strftime("%d/%m/%Y")
            self.tree_vencidos.insert("", "end", values=(p["id_producto"], p["nombre"], fecha, p["stock_actual"]))

    def crear_pestana_bajo(self):
        self.tree_bajo = ttk.Treeview(self.tab_bajo, columns=("ID","Nombre","Stock","Mínimo"), show="headings")
        self.tree_bajo.heading("ID", text="ID")
        self.tree_bajo.heading("Nombre", text="Producto")
        self.tree_bajo.heading("Stock", text="Stock")
        self.tree_bajo.heading("Mínimo", text="Mínimo")
        self.tree_bajo.column("ID", width=50)
        self.tree_bajo.column("Nombre", width=300)
        self.tree_bajo.column("Stock", width=100)
        self.tree_bajo.column("Mínimo", width=100)
        self.tree_bajo.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_tab_bajo()

    def actualizar_tab_bajo(self):
        for item in self.tree_bajo.get_children():
            self.tree_bajo.delete(item)
        for p in funciones.obtener_alerta_stock_bajo():
            self.tree_bajo.insert("", "end", values=(p["id_producto"], p["nombre"], p["stock_actual"], p["stock_minimo"]))

    # ────────────────────────────────────────────────
    #    Métodos auxiliares
    # ────────────────────────────────────────────────

    def actualizar_lista_productos(self):
        self.productos_combo = funciones.obtener_productos_para_combo()

    def actualizar_todas_las_pestanas(self):
        self.actualizar_lista_productos()
        if hasattr(self, 'combo_eliminar'):
            self.combo_eliminar.configure(values=[n for n,_ in self.productos_combo])
        if hasattr(self, 'combo_mov_producto'):
            self.combo_mov_producto.configure(values=[n for n,_ in self.productos_combo])
        self.actualizar_tab_listado()
        self.actualizar_tab_vencer()
        self.actualizar_tab_vencidos()
        self.actualizar_tab_bajo()


if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()
