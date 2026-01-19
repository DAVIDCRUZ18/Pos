# app/ui/ventas_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.ventas_logic import VentasLogic
import app.db.database as db

class VentasView(ttk.Frame):
    def __init__(self, parent, usuario_id=1):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.productos_carrito = []
        self.crear_widgets()
        self.cargar_productos()
    
    def crear_widgets(self):
        
        # Frame contenedor principal con borde
        frame_principal = ttk.Frame(self, relief=tk.SOLID, borderwidth=1)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # --- PRODUCTOS DISPONIBLES (Izquierda) ---
        frame_izq = ttk.Frame(frame_principal)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título sección productos
        lbl_productos = ttk.Label(
            frame_izq, 
            text="Productos Disponibles", 
            font=("Segoe UI", 12, "bold")
        )
        lbl_productos.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para tabla de productos
        frame_tabla_prod = ttk.Frame(frame_izq)
        frame_tabla_prod.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de productos
        self.tabla_prod = ttk.Treeview(
            frame_tabla_prod,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            height=18
        )
        
        self.tabla_prod.heading("id", text="ID")
        self.tabla_prod.heading("nombre", text="Nombre")
        self.tabla_prod.heading("precio", text="Precio")
        self.tabla_prod.heading("stock", text="Stock")
        
        self.tabla_prod.column("id", width=40, anchor=tk.CENTER)
        self.tabla_prod.column("nombre", width=180)
        self.tabla_prod.column("precio", width=80, anchor=tk.E)
        self.tabla_prod.column("stock", width=60, anchor=tk.CENTER)
        
        # Scrollbar productos
        scroll_prod = ttk.Scrollbar(frame_tabla_prod, orient="vertical", command=self.tabla_prod.yview)
        self.tabla_prod.configure(yscrollcommand=scroll_prod.set)
        
        self.tabla_prod.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_prod.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón agregar
        btn_agregar = ttk.Button(
            frame_izq,
            text="➕ Agregar al Carrito",
            command=self.agregar_producto
        )
        btn_agregar.pack(pady=(10, 0), fill=tk.X)
        
        # --- CARRITO DE COMPRA (Derecha) ---
        frame_der = ttk.Frame(frame_principal)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título sección carrito
        lbl_carrito = ttk.Label(
            frame_der,
            text="Carrito de Compra",
            font=("Segoe UI", 12, "bold")
        )
        lbl_carrito.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para tabla de carrito
        frame_tabla_cart = ttk.Frame(frame_der)
        frame_tabla_cart.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de carrito
        self.tabla_cart = ttk.Treeview(
            frame_tabla_cart,
            columns=("id", "nombre", "cantidad", "precio", "subtotal"),
            show="headings",
            height=18
        )
        
        self.tabla_cart.heading("id", text="ID")
        self.tabla_cart.heading("nombre", text="Producto")
        self.tabla_cart.heading("cantidad", text="Cant.")
        self.tabla_cart.heading("precio", text="Precio")
        self.tabla_cart.heading("subtotal", text="Subtotal")
        
        self.tabla_cart.column("id", width=35, anchor=tk.CENTER)
        self.tabla_cart.column("nombre", width=120)
        self.tabla_cart.column("cantidad", width=50, anchor=tk.CENTER)
        self.tabla_cart.column("precio", width=70, anchor=tk.E)
        self.tabla_cart.column("subtotal", width=85, anchor=tk.E)
        
        # Scrollbar carrito
        scroll_cart = ttk.Scrollbar(frame_tabla_cart, orient="vertical", command=self.tabla_cart.yview)
        self.tabla_cart.configure(yscrollcommand=scroll_cart.set)
        
        self.tabla_cart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_cart.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de carrito
        frame_botones_cart = ttk.Frame(frame_der)
        frame_botones_cart.pack(fill=tk.X, pady=(10, 0))
        
        btn_quitar = ttk.Button(
            frame_botones_cart,
            text="🗑️ Quitar",
            command=self.quitar_producto
        )
        btn_quitar.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        
        btn_limpiar = ttk.Button(
            frame_botones_cart,
            text="🧹 Limpiar",
            command=self.limpiar_carrito
        )
        btn_limpiar.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Total
        frame_total = ttk.Frame(frame_der)
        frame_total.pack(fill=tk.X, pady=15)
        
        self.lbl_total = ttk.Label(
            frame_total,
            text="Total: $0.00",
            font=("Segoe UI", 16, "bold"),
            foreground="#2E7D32"  # Verde
        )
        self.lbl_total.pack()
        
        # Botón registrar venta
        btn_registrar = ttk.Button(
            frame_der,
            text="✅ Registrar Venta",
            command=self.registrar_venta
        )
        btn_registrar.pack(fill=tk.X, ipady=8)
    
    def cargar_productos(self):
        """Carga los productos desde la base de datos"""
        # Limpiar tabla primero
        for item in self.tabla_prod.get_children():
            self.tabla_prod.delete(item)
            
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre")
            for row in cursor.fetchall():
                self.tabla_prod.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def agregar_producto(self):
        """Agrega un producto al carrito"""
        item = self.tabla_prod.focus()
        if not item:
            messagebox.showwarning("Selección", "Por favor selecciona un producto")
            return

        prod = self.tabla_prod.item(item)["values"]
        producto_id, nombre, precio, stock = prod

        # Conversión de tipos
        precio = float(precio)
        stock = int(stock)

        if stock <= 0:
            messagebox.showwarning("Stock", "Producto sin stock disponible")
            return

        # Validar stock en carrito
        cantidad_en_carrito = sum(
            p["cantidad"] for p in self.productos_carrito if p["producto_id"] == producto_id
        )

        if cantidad_en_carrito >= stock:
            messagebox.showwarning("Stock", f"No hay más stock disponible ({stock} unidades)")
            return

        # Buscar si ya existe en el carrito
        encontrado = False
        for p in self.productos_carrito:
            if p["producto_id"] == producto_id:
                p["cantidad"] += 1
                p["subtotal"] = p["cantidad"] * p["precio"]
                encontrado = True
                break

        if not encontrado:
            cantidad = 1
            subtotal = precio * cantidad
            self.productos_carrito.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": subtotal
            })

        self.actualizar_carrito()
    
    def quitar_producto(self):
        """Quita un producto del carrito"""
        item = self.tabla_cart.focus()
        if not item:
            messagebox.showwarning("Selección", "Por favor selecciona un producto del carrito")
            return
        
        valores = self.tabla_cart.item(item)["values"]
        producto_id = valores[0]
        
        # Eliminar del carrito
        self.productos_carrito = [p for p in self.productos_carrito if p["producto_id"] != producto_id]
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
        # Limpiar tabla
        for item in self.tabla_cart.get_children():
            self.tabla_cart.delete(item)
        
        # Recargar productos
        for p in self.productos_carrito:
            # Obtener nombre del producto
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM productos WHERE id = ?", (p["producto_id"],))
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                nombre = resultado[0]
                self.tabla_cart.insert("", tk.END, values=(
                    p["producto_id"],
                    nombre,
                    p["cantidad"],
                    f"${p['precio']:.2f}",
                    f"${p['subtotal']:.2f}"
                ))
        
        self.actualizar_total()
    
    def actualizar_total(self):
        """Actualiza el total de la venta"""
        total = sum(p["subtotal"] for p in self.productos_carrito)
        self.lbl_total.config(text=f"Total: ${total:,.2f}")
    
    def registrar_venta(self):
        """Registra la venta en la base de datos"""
        if not self.productos_carrito:
            messagebox.showwarning("Venta", "No hay productos en el carrito")
            return

        if not messagebox.askyesno("Confirmar", "¿Deseas registrar esta venta?"):
            return

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

        # Elegir comprobante
        opcion = messagebox.askquestion(
            "Comprobante",
            "¿Deseas generar FACTURA?\n\n(Sí = Factura / No = Ticket)"
        )

        if opcion == "yes":
            self.generar_factura(venta_id)
        else:
            self.generar_ticket(venta_id)

        messagebox.showinfo("Éxito", "Venta registrada correctamente")
        
        # Limpiar carrito y recargar
        self.productos_carrito = []
        self.actualizar_carrito()
        self.cargar_productos()
            
    def mostrar_comprobante(self, texto, titulo):
        """Muestra el comprobante en una ventana nueva"""
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry("500x650")
        win.resizable(False, False)
        
        # Centrar ventana
        win.transient(self.winfo_toplevel())
        win.grab_set()

        # Frame principal
        frame = ttk.Frame(win, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        # Texto del comprobante
        txt = tk.Text(
            frame, 
            wrap=tk.WORD, 
            font=("Courier New", 10),
            padx=10,
            pady=10
        )
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert("1.0", texto)
        txt.config(state="disabled")

        # Botones
        frame_btn = ttk.Frame(frame)
        frame_btn.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            frame_btn, 
            text="Cerrar", 
            command=win.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
    def generar_factura(self, venta_id):
        """Genera una factura detallada"""
        venta = VentasLogic.obtener_venta_por_id(venta_id)
        detalle = VentasLogic.obtener_detalle_venta(venta_id)

        texto = f"""
{'='*50}
           FACTURA DE VENTA
{'='*50}

N° Factura: {venta_id:05d}
Fecha: {venta[1]}
Cliente: {venta[5] or "Consumidor Final"}

{'='*50}
DETALLE DE PRODUCTOS
{'='*50}

"""
        for d in detalle:
            producto = d[-1][:28]  # Limitar nombre
            texto += f"{producto:<28} {d[2]:>3} x ${d[3]:>9.2f} = ${d[4]:>10.2f}\n"

        texto += f"""
{'='*50}
              TOTAL A PAGAR: ${venta[2]:>10.2f}
{'='*50}

Método de pago: {venta[4] or 'Efectivo'}

           Gracias por su compra
"""

        self.mostrar_comprobante(texto, "Factura de Venta")
    
    def generar_ticket(self, venta_id):
        """Genera un ticket simple"""
        venta = VentasLogic.obtener_venta_por_id(venta_id)
        detalle = VentasLogic.obtener_detalle_venta(venta_id)

        texto = f"""
{'='*40}
       TICKET DE VENTA
{'='*40}

Venta #: {venta_id:05d}
Fecha: {venta[1]}

{'='*40}

"""
        for d in detalle:
            producto = d[-1][:22]  # Limitar nombre
            texto += f"{producto:<22} x{d[2]:>2}  ${d[4]:>9.2f}\n"

        texto += f"""
{'='*40}
         TOTAL: ${venta[2]:>10.2f}
{'='*40}

      Gracias por su compra
"""

        self.mostrar_comprobante(texto, "Ticket de Venta")


def crear_vista_ventas(parent, ventana_principal):
    """Función para crear la vista de ventas dentro del frame parent"""
    # Limpiar el contenedor
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Obtener usuario_id de la sesión activa
    usuario_id = 1
    
    # Crear la vista como Frame
    vista = VentasView(parent=parent, usuario_id=usuario_id)
    vista.pack(fill=tk.BOTH, expand=True)