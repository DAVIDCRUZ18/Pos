import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.compras_logic import ComprasLogic
from app.logic.proveedores_logic import ProveedoresLogic
from app.logic.inventario_logic import InventarioLogic

class ComprasView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.productos_compra = []
        self.productos_dict = {}
        
        self.crear_widgets()
        self.cargar_proveedores()
        self.cargar_productos()
        self.cargar_compras()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(main_frame, text="Gestión de Compras", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario de compra
        form_frame = ttk.LabelFrame(main_frame, text="Nueva Compra", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        self.crear_formulario_compra(form_frame)
        
        # Frame de productos de compra
        productos_frame = ttk.LabelFrame(main_frame, text="Detalles de Compra", padding=10)
        productos_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.crear_detalle_productos(productos_frame)
        
        # Frame de lista de compras
        list_frame = ttk.LabelFrame(main_frame, text="Compras Realizadas", padding=10)
        list_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
        
        self.crear_lista_compras(list_frame)
        
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
    
    def crear_formulario_compra(self, parent):
        ttk.Label(parent, text="Proveedor*:").grid(row=0, column=0, sticky="w", pady=5)
        self.proveedor_combo = ttk.Combobox(parent, width=30, state="readonly")
        self.proveedor_combo.grid(row=0, column=1, pady=5)
        
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Nueva Compra", command=self.nueva_compra).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Guardar Compra", command=self.guardar_compra).pack(side="left", padx=5)
    
    def crear_detalle_productos(self, parent):
        add_frame = ttk.Frame(parent)
        add_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(add_frame, text="Producto*:").grid(row=0, column=0, padx=5, pady=5)
        self.producto_combo = ttk.Combobox(add_frame, width=30, state="readonly")
        self.producto_combo.grid(row=0, column=1, padx=5, pady=5)
        self.producto_combo.bind("<<ComboboxSelected>>", self.on_producto_select)
        
        ttk.Label(add_frame, text="Cantidad*:").grid(row=0, column=2, padx=5, pady=5)
        self.cantidad_spin = ttk.Spinbox(add_frame, from_=1, to=1000, width=10)
        self.cantidad_spin.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Costo U.*:").grid(row=0, column=4, padx=5, pady=5)
        self.costo_entry = ttk.Entry(add_frame, width=10)
        self.costo_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=6, padx=10, pady=5)
        
        columns = ("Producto", "Cantidad", "Costo U.", "Subtotal", "Acciones")
        self.tree_productos = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        self.tree_productos.heading("Producto", text="Producto")
        self.tree_productos.heading("Cantidad", text="Cantidad")
        self.tree_productos.heading("Costo U.", text="Costo U.")
        self.tree_productos.heading("Subtotal", text="Subtotal")
        self.tree_productos.heading("Acciones", text="Acciones")
        
        self.tree_productos.column("Producto", width=250)
        self.tree_productos.column("Cantidad", width=80)
        self.tree_productos.column("Costo U.", width=80)
        self.tree_productos.column("Subtotal", width=80)
        self.tree_productos.column("Acciones", width=80)
        
        self.tree_productos.pack(fill="both", expand=True)
        
        total_frame = ttk.Frame(parent)
        total_frame.pack(fill="x", pady=(10, 0))
        
        self.total_label = ttk.Label(total_frame, text="Total: $0.00", 
                                  font=("Arial", 12, "bold"))
        self.total_label.pack(side="right")
    
    def crear_lista_compras(self, parent):
        columns = ("ID", "Fecha", "Proveedor", "Total", "Usuario")
        self.tree_compras = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        self.tree_compras.heading("ID", text="ID")
        self.tree_compras.heading("Fecha", text="Fecha")
        self.tree_compras.heading("Proveedor", text="Proveedor")
        self.tree_compras.heading("Total", text="Total")
        self.tree_compras.heading("Usuario", text="Usuario")
        
        self.tree_compras.column("ID", width=50)
        self.tree_compras.column("Fecha", width=120)
        self.tree_compras.column("Proveedor", width=150)
        self.tree_compras.column("Total", width=80)
        self.tree_compras.column("Usuario", width=100)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree_compras.yview)
        self.tree_compras.configure(yscrollcommand=scrollbar.set)
        
        self.tree_compras.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(parent, text="Ver Detalles", command=self.ver_detalles_compra).pack(pady=(10, 0))
    
    def cargar_proveedores(self):
        proveedores = ProveedoresLogic.obtener_proveedores()
        self.proveedor_combo['values'] = [f"{p['id']} - {p['nombre']}" for p in proveedores]
    
    def cargar_productos(self):
        productos = InventarioLogic.obtener_productos()
        self.producto_combo['values'] = [f"{p['id']} - {p['nombre']}" for p in productos]
        self.productos_dict = {f"{p['id']} - {p['nombre']}": p for p in productos}
    
    def cargar_compras(self):
        for item in self.tree_compras.get_children():
            self.tree_compras.delete(item)
        
        compras = ComprasLogic.obtener_todas_compras()
        
        for compra in compras:
            self.tree_compras.insert("", "end", values=(
                compra['id'],
                compra['fecha'],
                compra['proveedor_nombre'] or 'N/A',
                f"${compra['total']:.2f}",
                compra['usuario_nombre'] or 'N/A'
            ))
    
    def on_producto_select(self, event):
        seleccion = self.producto_combo.get()
        if seleccion and seleccion in self.productos_dict:
            producto = self.productos_dict[seleccion]
            self.costo_entry.delete(0, "end")
            self.costo_entry.insert(0, str(producto.get('costo', 0)))
    
    def agregar_producto(self):
        producto_seleccionado = self.producto_combo.get()
        cantidad_str = self.cantidad_spin.get()
        costo_str = self.costo_entry.get()
        
        if not producto_seleccionado or not cantidad_str or not costo_str:
            messagebox.showerror("Error", "Complete todos los campos del producto")
            return
        
        try:
            cantidad = int(cantidad_str)
            costo = float(costo_str)
            
            if cantidad <= 0 or costo <= 0:
                messagebox.showerror("Error", "La cantidad y el costo deben ser mayores a cero")
                return
            
            producto = self.productos_dict[producto_seleccionado]
            subtotal = cantidad * costo
            
            self.tree_productos.insert("", "end", values=(
                producto['nombre'],
                cantidad,
                f"${costo:.2f}",
                f"${subtotal:.2f}",
                "Quitar"
            ), tags=(producto['id'],))
            
            self.productos_compra.append({
                'producto_id': producto['id'],
                'cantidad': cantidad,
                'costo_unitario': costo,
                'subtotal': subtotal
            })
            
            self.producto_combo.set("")
            self.cantidad_spin.delete(0, "end")
            self.costo_entry.delete(0, "end")
            
            self.actualizar_total()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
    
    def actualizar_total(self):
        total = sum(p['subtotal'] for p in self.productos_compra)
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def nueva_compra(self):
        self.proveedor_combo.set("")
        self.productos_compra = []
        
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        self.actualizar_total()
    
    def guardar_compra(self):
        proveedor_seleccionado = self.proveedor_combo.get()
        
        if not proveedor_seleccionado:
            messagebox.showerror("Error", "Seleccione un proveedor")
            return
        
        if not self.productos_compra:
            messagebox.showerror("Error", "Agregue productos a la compra")
            return
        
        try:
            proveedor_id = int(proveedor_seleccionado.split(' - ')[0])
            
            resultado = ComprasLogic.crear_compra(
                proveedor_id=proveedor_id,
                productos=self.productos_compra,
                usuario_id=self.usuario_actual['id']
            )
            
            if resultado['exito']:
                messagebox.showinfo("Éxito", resultado['mensaje'])
                self.nueva_compra()
                self.cargar_compras()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
                
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Seleccione un proveedor válido")
    
    def ver_detalles_compra(self):
        seleccion = self.tree_compras.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una compra para ver sus detalles")
            return
        
        item = self.tree_compras.item(seleccion[0])
        compra_id = item['values'][0]
        
        compra = ComprasLogic.obtener_compra_por_id(compra_id)
        
        if not compra:
            messagebox.showerror("Error", "No se encontraron detalles de la compra")
            return
        
        ventana_detalles = tk.Toplevel(self.parent)
        ventana_detalles.title(f"Detalles de Compra #{compra_id}")
        ventana_detalles.geometry("700x500")
        
        info_frame = ttk.LabelFrame(ventana_detalles, text="Información General", padding=10)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"ID: {compra['id']}").grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, text=f"Fecha: {compra['fecha']}").grid(row=0, column=1, sticky="w")
        ttk.Label(info_frame, text=f"Proveedor: {compra['proveedor_nombre']}").grid(row=0, column=2, sticky="w")
        ttk.Label(info_frame, text=f"Total: ${compra['total']:.2f}").grid(row=1, column=0, sticky="w")
        
        detalles_frame = ttk.LabelFrame(ventana_detalles, text="Productos", padding=10)
        detalles_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Producto", "Cantidad", "Costo U.", "Subtotal")
        tree_detalles = ttk.Treeview(detalles_frame, columns=columns, show="headings")
        
        for col in columns:
            tree_detalles.heading(col, text=col)
            tree_detalles.column(col, width=150)
        
        for detalle in compra['detalles']:
            tree_detalles.insert("", "end", values=(
                detalle['producto_nombre'],
                detalle['cantidad'],
                f"${detalle['costo_unitario']:.2f}",
                f"${detalle['subtotal']:.2f}"
            ))
        
        tree_detalles.pack(fill="both", expand=True)

def crear_vista_compras(parent, usuario_actual):
    return ComprasView(parent, usuario_actual)