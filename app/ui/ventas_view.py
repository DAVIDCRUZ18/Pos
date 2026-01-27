# app/ui/ventas_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.ventas_logic import VentasLogic
from app.db.database import get_db
from app.services.pdf_service import generar_pdf
import os

class VentasView(ttk.Frame):
    def __init__(self, parent, usuario_id=1):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.productos_carrito = []
        self.configurar_estilos()
        self.crear_widgets()
        self.cargar_productos()
    
    def configurar_estilos(self):
        """Configura los estilos personalizados para la interfaz"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Colores principales
        COLOR_PRIMARY = "#2C3E50"      # Azul oscuro
        COLOR_SECONDARY = "#3498DB"    # Azul claro
        COLOR_SUCCESS = "#27AE60"      # Verde
        COLOR_DANGER = "#E74C3C"       # Rojo
        COLOR_WARNING = "#F39C12"      # Naranja
        COLOR_BG = "#ECF0F1"           # Gris claro
        COLOR_WHITE = "#FFFFFF"
        COLOR_TEXT = "#2C3E50"
        
        # Frame principal
        style.configure("Custom.TFrame", background=COLOR_BG)
        
        # LabelFrames
        style.configure("Custom.TLabelframe", 
                       background=COLOR_WHITE,
                       borderwidth=2,
                       relief="flat")
        style.configure("Custom.TLabelframe.Label",
                       background=COLOR_WHITE,
                       foreground=COLOR_PRIMARY,
                       font=("Segoe UI", 11, "bold"))
        
        # Botones principales
        style.configure("Primary.TButton",
                       background=COLOR_SECONDARY,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(10, 8))
        style.map("Primary.TButton",
                 background=[("active", "#2980B9")])
        
        # Botón de éxito (registrar venta)
        style.configure("Success.TButton",
                       background=COLOR_SUCCESS,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 12, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 12))
        style.map("Success.TButton",
                 background=[("active", "#229954")])
        
        # Botón de peligro
        style.configure("Danger.TButton",
                       background=COLOR_DANGER,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(10, 8))
        style.map("Danger.TButton",
                 background=[("active", "#C0392B")])
        
        # Botón de advertencia
        style.configure("Warning.TButton",
                       background=COLOR_WARNING,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(10, 8))
        style.map("Warning.TButton",
                 background=[("active", "#D68910")])
        
        # Treeview
        style.configure("Custom.Treeview",
                       background=COLOR_WHITE,
                       foreground=COLOR_TEXT,
                       fieldbackground=COLOR_WHITE,
                       borderwidth=0,
                       font=("Segoe UI", 9))
        style.configure("Custom.Treeview.Heading",
                       background=COLOR_PRIMARY,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0)
        style.map("Custom.Treeview.Heading",
                 background=[("active", COLOR_SECONDARY)])
        style.map("Custom.Treeview",
                 background=[("selected", COLOR_SECONDARY)],
                 foreground=[("selected", COLOR_WHITE)])
    
    def crear_widgets(self):
        # Configurar grid para mejor distribución
        self.configure(style="Custom.TFrame")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame contenedor principal
        frame_principal = ttk.Frame(self, style="Custom.TFrame", padding=15)
        frame_principal.grid(row=0, column=0, sticky="nsew")
        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(1, weight=1)
        
        # --- PRODUCTOS DISPONIBLES (Izquierda) ---
        frame_izq = ttk.LabelFrame(
            frame_principal, 
            text="📦 Productos Disponibles",
            padding=15,
            style="Custom.TLabelframe"
        )
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame_izq.grid_rowconfigure(0, weight=1)
        frame_izq.grid_columnconfigure(0, weight=1)
        
        # Tabla de productos
        frame_tabla_prod = ttk.Frame(frame_izq, style="Custom.TFrame")
        frame_tabla_prod.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        frame_tabla_prod.grid_rowconfigure(0, weight=1)
        frame_tabla_prod.grid_columnconfigure(0, weight=1)
        
        self.tabla_prod = ttk.Treeview(
            frame_tabla_prod,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )
        
        self.tabla_prod.heading("id", text="ID")
        self.tabla_prod.heading("nombre", text="Nombre del Producto")
        self.tabla_prod.heading("precio", text="Precio")
        self.tabla_prod.heading("stock", text="Stock")
        
        self.tabla_prod.column("id", width=50, anchor=tk.CENTER)
        self.tabla_prod.column("nombre", width=250)
        self.tabla_prod.column("precio", width=100, anchor=tk.E)
        self.tabla_prod.column("stock", width=80, anchor=tk.CENTER)
        
        # Scrollbar productos
        scroll_prod = ttk.Scrollbar(
            frame_tabla_prod, 
            orient="vertical", 
            command=self.tabla_prod.yview
        )
        self.tabla_prod.configure(yscrollcommand=scroll_prod.set)
        
        self.tabla_prod.grid(row=0, column=0, sticky="nsew")
        scroll_prod.grid(row=0, column=1, sticky="ns")
        
        # Botón agregar
        btn_agregar = ttk.Button(
            frame_izq,
            text="➕ Agregar al Carrito",
            command=self.agregar_producto,
            style="Primary.TButton"
        )
        btn_agregar.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # --- CARRITO DE COMPRA (Derecha) ---
        frame_der = ttk.LabelFrame(
            frame_principal,
            text="🛒 Carrito de Compra",
            padding=15,
            style="Custom.TLabelframe"
        )
        frame_der.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        frame_der.grid_rowconfigure(0, weight=1)
        frame_der.grid_columnconfigure(0, weight=1)
        
        # Tabla de carrito
        frame_tabla_cart = ttk.Frame(frame_der, style="Custom.TFrame")
        frame_tabla_cart.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        frame_tabla_cart.grid_rowconfigure(0, weight=1)
        frame_tabla_cart.grid_columnconfigure(0, weight=1)
        
        self.tabla_cart = ttk.Treeview(
            frame_tabla_cart,
            columns=("id", "nombre", "cantidad", "precio", "subtotal"),
            show="headings",
            height=20,
            style="Custom.Treeview"
        )
        
        self.tabla_cart.heading("id", text="ID")
        self.tabla_cart.heading("nombre", text="Producto")
        self.tabla_cart.heading("cantidad", text="Cant.")
        self.tabla_cart.heading("precio", text="Precio")
        self.tabla_cart.heading("subtotal", text="Subtotal")
        
        self.tabla_cart.column("id", width=40, anchor=tk.CENTER)
        self.tabla_cart.column("nombre", width=180)
        self.tabla_cart.column("cantidad", width=70, anchor=tk.CENTER)
        self.tabla_cart.column("precio", width=90, anchor=tk.E)
        self.tabla_cart.column("subtotal", width=100, anchor=tk.E)
        
        # Scrollbar carrito
        scroll_cart = ttk.Scrollbar(
            frame_tabla_cart, 
            orient="vertical", 
            command=self.tabla_cart.yview
        )
        self.tabla_cart.configure(yscrollcommand=scroll_cart.set)
        
        self.tabla_cart.grid(row=0, column=0, sticky="nsew")
        scroll_cart.grid(row=0, column=1, sticky="ns")
        
        # Botones de carrito
        frame_botones_cart = ttk.Frame(frame_der, style="Custom.TFrame")
        frame_botones_cart.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        frame_botones_cart.grid_columnconfigure(0, weight=1)
        frame_botones_cart.grid_columnconfigure(1, weight=1)
        
        btn_quitar = ttk.Button(
            frame_botones_cart,
            text="🗑️ Quitar",
            command=self.quitar_producto,
            style="Danger.TButton"
        )
        btn_quitar.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        btn_limpiar = ttk.Button(
            frame_botones_cart,
            text="🧹 Limpiar Todo",
            command=self.limpiar_carrito,
            style="Warning.TButton"
        )
        btn_limpiar.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        # Frame para total
        frame_total = ttk.Frame(frame_der, style="Custom.TFrame")
        frame_total.grid(row=2, column=0, sticky="ew", pady=(10, 15))
        
        # Fondo para el total
        canvas_total = tk.Canvas(frame_total, height=80, bg="#27AE60", highlightthickness=0)
        canvas_total.pack(fill="x")
        
        self.lbl_total = tk.Label(
            canvas_total,
            text="TOTAL: $0.00",
            font=("Segoe UI", 20, "bold"),
            foreground="#FFFFFF",
            background="#27AE60"
        )
        self.lbl_total.place(relx=0.5, rely=0.5, anchor="center")
        
        # Botón registrar venta
        btn_registrar = ttk.Button(
            frame_der,
            text="✅ REGISTRAR VENTA",
            command=self.registrar_venta,
            style="Success.TButton"
        )
        btn_registrar.grid(row=3, column=0, sticky="ew")
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos"""
        for item in self.tabla_prod.get_children():
            self.tabla_prod.delete(item)
            
        try:
            # CORRECCIÓN: Usar context manager correctamente
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre"
                )
                productos = cursor.fetchall()
            
            for row in productos:
                producto_id, nombre, precio, stock = row
                self.tabla_prod.insert("", tk.END, values=(
                    producto_id,
                    nombre,
                    f"${precio:.2f}",
                    stock
                ), tags=('oddrow' if self.tabla_prod.get_children().index(self.tabla_prod.get_children()[-1]) % 2 else 'evenrow',) if self.tabla_prod.get_children() else ('evenrow',))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def agregar_producto(self):
        """Agrega un producto al carrito"""
        item = self.tabla_prod.focus()
        if not item:
            messagebox.showwarning("Selección", "Por favor selecciona un producto")
            return

        prod = self.tabla_prod.item(item)["values"]
        producto_id = prod[0]
        nombre = prod[1]
        precio_str = prod[2]
        stock = int(prod[3])
        
        precio = float(precio_str.replace("$", "").replace(",", ""))

        if stock <= 0:
            messagebox.showwarning("Stock", "Producto sin stock disponible")
            return

        cantidad_en_carrito = sum(
            p["cantidad"] for p in self.productos_carrito if p["producto_id"] == producto_id
        )

        if cantidad_en_carrito >= stock:
            messagebox.showwarning(
                "Stock", 
                f"No hay más stock disponible ({stock} unidades)"
            )
            return

        encontrado = False
        for p in self.productos_carrito:
            if p["producto_id"] == producto_id:
                p["cantidad"] += 1
                p["subtotal"] = p["cantidad"] * p["precio"]
                encontrado = True
                break

        if not encontrado:
            self.productos_carrito.append({
                "producto_id": producto_id,
                "cantidad": 1,
                "precio": precio,
                "subtotal": precio
            })

        self.actualizar_carrito()
    
    def quitar_producto(self):
        """Quita un producto del carrito"""
        item = self.tabla_cart.focus()
        if not item:
            messagebox.showwarning(
                "Selección", 
                "Por favor selecciona un producto del carrito"
            )
            return
        
        valores = self.tabla_cart.item(item)["values"]
        producto_id = valores[0]
        
        self.productos_carrito = [
            p for p in self.productos_carrito if p["producto_id"] != producto_id
        ]
        self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpia todos los productos del carrito"""
        if not self.productos_carrito:
            messagebox.showinfo("Carrito", "El carrito ya está vacío")
            return
        
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todo el carrito?"):
            self.productos_carrito = []
            self.actualizar_carrito()
    
    def actualizar_carrito(self):
        """Actualiza la vista del carrito"""
        for item in self.tabla_cart.get_children():
            self.tabla_cart.delete(item)
        
        try:
            # CORRECCIÓN: Usar context manager correctamente
            with get_db() as conn:
                cursor = conn.cursor()
                
                for p in self.productos_carrito:
                    cursor.execute(
                        "SELECT nombre FROM productos WHERE id = ?", 
                        (p["producto_id"],)
                    )
                    resultado = cursor.fetchone()
                    
                    if resultado:
                        nombre = resultado[0]
                        self.tabla_cart.insert("", tk.END, values=(
                            p["producto_id"],
                            nombre,
                            p["cantidad"],
                            f"${p['precio']:.2f}",
                            f"${p['subtotal']:.2f}"
                        ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar carrito: {e}")
        
        self.actualizar_total()
    
    def actualizar_total(self):
        """Actualiza el total de la venta"""
        total = sum(p["subtotal"] for p in self.productos_carrito)
        self.lbl_total.config(text=f"TOTAL: ${total:,.2f}")
    
    def registrar_venta(self):
        """Registra la venta en la base de datos"""
        if not self.productos_carrito:
            messagebox.showwarning("Venta", "No hay productos en el carrito")
            return

        if not messagebox.askyesno("Confirmar", "¿Deseas registrar esta venta?"):
            return

        try:
            resultado = VentasLogic.crear_venta(
                cliente_id=None,
                productos=self.productos_carrito,
                usuario_id=self.usuario_id,
                metodo_pago="efectivo"
            )

            if not resultado["exito"]:
                messagebox.showerror("Error", resultado["mensaje"])
                return

            venta_id = resultado["venta_id"]

            opcion = messagebox.askquestion(
                "Comprobante",
                "¿Deseas generar FACTURA?\n\n(Sí = Factura / No = Ticket)"
            )

            if opcion == "yes":
                self.generar_factura(venta_id)
            else:
                self.generar_ticket(venta_id)

            messagebox.showinfo("Éxito", "✅ Venta registrada correctamente")
            
            self.productos_carrito = []
            self.actualizar_carrito()
            self.cargar_productos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar venta: {e}")
            
    def generar_factura(self, venta_id):
        try:
            venta = VentasLogic.obtener_venta_por_id(venta_id)
            detalle = VentasLogic.obtener_detalle_venta(venta_id)

            if not venta:
                messagebox.showerror("Error", f"No se encontró la venta con ID: {venta_id}")
                return

            if not detalle:
                messagebox.showwarning("Advertencia", "La venta no tiene productos asociados")
                return

            fecha = venta[1]
            total = venta[2]
            metodo_pago = venta[4] if len(venta) > 4 else "efectivo"
            cliente = venta[5] if len(venta) > 5 else "Consumidor Final"

            texto = f"""{'='*60}
                        FACTURA DE VENTA
    {'='*60}

    N° Factura: {venta_id:05d}
    Fecha: {fecha}
    Cliente: {cliente}

    {'='*60}
    DETALLE DE PRODUCTOS
    {'='*60}
    """

            for d in detalle:
                producto = d[5][:35]
                cantidad = d[2]
                precio = d[3]
                subtotal = d[4]
                texto += f"{producto:<35} {cantidad:>3} x ${precio:>9.2f} = ${subtotal:>10.2f}\n"

            texto += f"""{'='*60}
    TOTAL A PAGAR: ${total:>10.2f}
    {'='*60}

    Método de pago: {metodo_pago}

    Gracias por su compra
    """

            os.makedirs("Facturas", exist_ok=True)
            ruta = os.path.join("Facturas", f"factura_{venta_id:05d}.pdf")
            generar_pdf(texto, ruta, "Factura de Venta")
            messagebox.showinfo("Factura generada", f"✅ Factura guardada en:\n{ruta}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {e}")
            import traceback
            traceback.print_exc()

    def generar_ticket(self, venta_id):
        try:
            venta = VentasLogic.obtener_venta_por_id(venta_id)
            detalle = VentasLogic.obtener_detalle_venta(venta_id)
            
            if not venta:
                messagebox.showerror("Error", f"No se encontró la venta con ID: {venta_id}")
                return
            
            if not detalle:
                messagebox.showwarning("Advertencia", "La venta no tiene productos")
                return
            
            fecha = venta[1]
            total = venta[2]
            
            texto = f"""{'='*45}
            TICKET DE VENTA
    {'='*45}
    Venta #: {venta_id:05d}
    Fecha: {fecha}
    {'='*45}
    PRODUCTOS
    {'='*45}
    """
            
            for d in detalle:
                producto = d[5][:25]
                cantidad = d[2]
                subtotal = d[4]
                texto += f"{producto:<25} x{cantidad:>2}  ${subtotal:>8.2f}\n"
            
            texto += f"""{'='*45}
    TOTAL: ${total:>10.2f}
    {'='*45}
    Gracias por su compra
    """
            
            os.makedirs("Ticket", exist_ok=True)
            ruta = os.path.join("Ticket", f"ticket_{venta_id:05d}.pdf")
            generar_pdf(texto, ruta, "Ticket de Venta")
            messagebox.showinfo("Ticket generado", f"✅ Ticket guardado en:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar ticket: {e}")
            import traceback
            traceback.print_exc()


def crear_vista_ventas(parent, ventana_principal):
    """Función para crear la vista de ventas dentro del frame parent"""
    for widget in parent.winfo_children():
        widget.destroy()
    
    usuario_id = 1
    vista = VentasView(parent=parent, usuario_id=usuario_id)
    vista.pack(fill=tk.BOTH, expand=True)