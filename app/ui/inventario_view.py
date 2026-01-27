import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.inventario_logic import InventarioLogic
from app.logic.categorias_logic import CategoriasLogic

class InventarioView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        
        self.crear_widgets()
        self.cargar_productos()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Nuevo/Editar Producto", padding=10)
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Formulario
        self.crear_formulario_producto(form_frame)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Productos Registrados", padding=10)
        list_frame.pack(fill="both", expand=True)
        
        # Treeview
        self.crear_lista_productos(list_frame)
    
    def crear_formulario_producto(self, parent):
        # Grid layout para formulario
        # Fila 1: Nombre y Código
        ttk.Label(parent, text="Nombre*:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nombre_entry = ttk.Entry(parent, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Código:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.codigo_entry = ttk.Entry(parent, width=20)
        self.codigo_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Fila 2: Categoría y Proveedor
        ttk.Label(parent, text="Categoría:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.categoria_combo = ttk.Combobox(parent, width=28, state="readonly")
        self.categoria_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Proveedor:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.proveedor_entry = ttk.Entry(parent, width=20)
        self.proveedor_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Fila 3: Precio y Costo
        ttk.Label(parent, text="Precio Venta*:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.precio_entry = ttk.Entry(parent, width=20)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Costo:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.costo_entry = ttk.Entry(parent, width=20)
        self.costo_entry.grid(row=2, column=3, padx=5, pady=5)
        
        # Fila 4: Stock y Stock Mínimo
        ttk.Label(parent, text="Stock*:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.stock_spin = ttk.Spinbox(parent, from_=0, to=10000, width=20)
        self.stock_spin.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(parent, text="Stock Mínimo:").grid(row=3, column=2, sticky="w", padx=5, pady=5)
        self.min_stock_spin = ttk.Spinbox(parent, from_=0, to=1000, width=20)
        self.min_stock_spin.set("5")
        self.min_stock_spin.grid(row=3, column=3, padx=5, pady=5)
        
        # Fila 5: Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        ttk.Button(btn_frame, text="Guardar Producto", command=self.guardar_producto).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=5)
        
        # Cargar categorías
        self.cargar_categorias()
    
    def crear_lista_productos(self, parent):
        # Frame de búsqueda
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.buscar_entry = ttk.Entry(search_frame, width=40)
        self.buscar_entry.pack(side="left", padx=5)
        self.buscar_entry.bind("<KeyRelease>", self.on_buscar)
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_productos).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Categoría", "Stock", "Precio", "Costo", "Proveedor")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Proveedor", text="Proveedor")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("Categoría", width=120)
        self.tree.column("Stock", width=60)
        self.tree.column("Precio", width=80)
        self.tree.column("Costo", width=80)
        self.tree.column("Proveedor", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_producto_select)
    
    def cargar_categorias(self):
        """Carga las categorías en el combobox"""
        try:
            categorias = CategoriasLogic.obtener_todas_categorias()
            categoria_nombres = ["Sin categoría"] + [cat['nombre'] for cat in categorias]
            self.categoria_combo['values'] = categoria_nombres
            if categoria_nombres:
                self.categoria_combo.set("Sin categoría")
        except Exception as e:
            print(f"Error cargando categorías: {e}")
            self.categoria_combo['values'] = ["Sin categoría"]
            self.categoria_combo.set("Sin categoría")
    
    def cargar_productos(self):
        """Carga los productos en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            productos = InventarioLogic.obtener_productos()
            
            for producto in productos:
                self.tree.insert("", "end", values=(
                    producto['id'],
                    producto['nombre'],
                    producto.get('categoria_nombre') or 'Sin categoría',
                    producto['stock'],
                    f"${producto['precio']:.2f}",
                    f"${producto.get('costo', 0):.2f}",
                    producto.get('proveedor_nombre') or 'N/A'
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {str(e)}")
    
    def guardar_producto(self):
        """Guarda un nuevo producto"""
        nombre = self.nombre_entry.get().strip()
        precio_str = self.precio_entry.get().strip()
        stock_str = self.stock_spin.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre del producto es obligatorio")
            return
        
        if not precio_str:
            messagebox.showerror("Error", "El precio es obligatorio")
            return
        
        if not stock_str:
            messagebox.showerror("Error", "El stock es obligatorio")
            return
        
        try:
            precio = float(precio_str)
            stock = int(stock_str)
            costo = float(self.costo_entry.get().strip() or "0")
            min_stock = int(self.min_stock_spin.get().strip() or "5")
            
            # Obtener ID de categoría (implementar lógica)
            categoria_id = None  # Simplificado por ahora
            
            InventarioLogic.crear_producto(
                codigo=self.codigo_entry.get().strip(),
                nombre=nombre,
                categoria=self.categoria_combo.get(),
                precio=precio,
                costo=costo,
                stock=stock,
                min_stock=min_stock,
                proveedor=self.proveedor_entry.get().strip()
            )
            
            messagebox.showinfo("Éxito", "Producto guardado exitosamente")
            self.limpiar_formulario()
            self.cargar_productos()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {str(e)}")
    
    def actualizar_producto(self):
        """Actualiza el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar")
            return
        
        item = self.tree.item(seleccion[0])
        values = item['values']
        producto_id = values[0]
        
        try:
            datos = {
                'nombre': self.nombre_entry.get().strip(),
                'codigo': self.codigo_entry.get().strip(),
                'precio': float(self.precio_entry.get().strip()),
                'costo': float(self.costo_entry.get().strip() or "0"),
                'stock': int(self.stock_spin.get().strip()),
                'min_stock': int(self.min_stock_spin.get().strip() or "5"),
                'categoria': self.categoria_combo.get(),
                'proveedor': self.proveedor_entry.get().strip()
            }
            
            InventarioLogic.actualizar_producto(producto_id, datos)
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
            self.limpiar_formulario()
            self.cargar_productos()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        item = self.tree.item(seleccion[0])
        values = item['values']
        producto_id = values[0]
        nombre_producto = values[1]
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar el producto '{nombre_producto}'?"):
            try:
                InventarioLogic.eliminar_producto(producto_id)
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
                self.limpiar_formulario()
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.precio_entry.delete(0, "end")
        self.costo_entry.delete(0, "end")
        self.stock_spin.delete(0, "end")
        self.min_stock_spin.set("5")
        self.categoria_combo.set("Sin categoría")
        self.proveedor_entry.delete(0, "end")
        
        # Limpiar selección del treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def on_producto_select(self, event):
        """Maneja la selección de un producto"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            # Cargar datos en el formulario
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])
            
            self.codigo_entry.delete(0, "end")
            # El código de barras no está en esta vista simplificada
            # self.codigo_entry.insert(0, values[?] if len(values) > ? else "")
            
            self.precio_entry.delete(0, "end")
            self.precio_entry.insert(0, str(values[4]).replace("$", ""))
            
            self.costo_entry.delete(0, "end")
            self.costo_entry.insert(0, str(values[5]).replace("$", ""))
            
            self.stock_spin.delete(0, "end")
            self.stock_spin.insert(0, str(values[3]))
            
            self.proveedor_entry.delete(0, "end")
            self.proveedor_entry.insert(0, values[6] if len(values) > 6 else "")
            
            categoria_nombre = values[2] if len(values) > 2 else "Sin categoría"
            self.categoria_combo.set(categoria_nombre)
    
    def on_buscar(self, event):
        """Busca productos en tiempo real"""
        termino = self.buscar_entry.get().strip()
        self.buscar_productos(termino)
    
    def buscar_productos(self, termino=None):
        """Busca productos"""
        if termino is None:
            termino = self.buscar_entry.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if termino:
            try:
                productos = InventarioLogic.buscar_productos(termino)
                
                for producto in productos:
                    self.tree.insert("", "end", values=(
                        producto['id'],
                        producto['nombre'],
                        producto.get('categoria_nombre') or 'Sin categoría',
                        producto['stock'],
                        f"${producto['precio']:.2f}",
                        f"${producto.get('costo', 0):.2f}",
                        producto.get('proveedor_nombre') or 'N/A'
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron buscar los productos: {str(e)}")
        else:
            self.cargar_productos()

def crear_vista_inventario(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    return InventarioView(parent, usuario_actual)