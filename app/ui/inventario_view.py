import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.inventario_logic import InventarioLogic

class InventarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#f5f5f5')
        self.logic = InventarioLogic()
        self.producto_seleccionado = None
        
        self.configurar_ui()
        self.cargar_productos()
    
    def configurar_ui(self):
        # Header
        header_frame = tk.Frame(self, bg='white', height=80)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame, 
            text="📦 INVENTARIO", 
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(side='left', padx=20, pady=20)
        
        # Barra de herramientas
        toolbar_frame = tk.Frame(self, bg='white')
        toolbar_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Búsqueda
        search_frame = tk.Frame(toolbar_frame, bg='white')
        search_frame.pack(side='left', fill='x', expand=True, padx=10, pady=15)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 12),
            bg='white'
        ).pack(side='left', padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.buscar_productos)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bg='white',
            relief='flat',
            width=40
        )
        search_entry.pack(side='left', fill='x', expand=True)
        search_entry.insert(0, "Buscar por nombre o código...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, 'end') if search_entry.get() == "Buscar por nombre o código..." else None)
        
        # Filtros
        filter_frame = tk.Frame(toolbar_frame, bg='white')
        filter_frame.pack(side='left', padx=10)
        
        tk.Label(
            filter_frame,
            text="Categoría:",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left', padx=(0, 5))
        
        self.categoria_var = tk.StringVar(value="Todas")
        self.categoria_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.categoria_var,
            values=["Todas", "Electrónica", "Accesorios", "Audio", "Computadoras"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10)
        )
        self.categoria_combo.pack(side='left', padx=5)
        self.categoria_combo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())
        
        # Filtro de stock
        self.stock_var = tk.StringVar(value="Todos")
        stock_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.stock_var,
            values=["Todos", "Bajo Stock", "Sin Stock"],
            state='readonly',
            width=12,
            font=('Segoe UI', 10)
        )
        stock_combo.pack(side='left', padx=5)
        stock_combo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())
        
        # Botones de acción
        btn_frame = tk.Frame(toolbar_frame, bg='white')
        btn_frame.pack(side='right', padx=10)
        
        self.btn_nuevo = tk.Button(
            btn_frame,
            text="➕ Nuevo Producto",
            font=('Segoe UI', 10, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.abrir_modal_nuevo
        )
        self.btn_nuevo.pack(side='left', padx=5)
        
        # Tarjetas de estadísticas
        stats_frame = tk.Frame(self, bg='#f5f5f5')
        stats_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        productos = self.logic.obtener_productos()
        total_productos = len(productos)
        bajo_stock = len(self.logic.productos_bajo_stock())
        sin_stock = len([p for p in productos if p.get('stock', 0) == 0])
        valor_total = sum(p.get('precio', 0) * p.get('stock', 0) for p in productos)
        
        self.crear_stat_card(stats_frame, "Total Productos", str(total_productos), "#3b82f6", "📦").pack(side='left', padx=5, fill='x', expand=True)
        self.crear_stat_card(stats_frame, "Bajo Stock", str(bajo_stock), "#f59e0b", "⚠️").pack(side='left', padx=5, fill='x', expand=True)
        self.crear_stat_card(stats_frame, "Sin Stock", str(sin_stock), "#ef4444", "❌").pack(side='left', padx=5, fill='x', expand=True)
        self.crear_stat_card(stats_frame, "Valor Inventario", f"${valor_total:,.0f}", "#10b981", "💰").pack(side='left', padx=5, fill='x', expand=True)
        
        # Tabla de productos
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        columns = ('Código', 'Nombre', 'Categoría', 'Stock', 'Mín.', 'Precio', 'Costo', 'Proveedor', 'Estado')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        column_widths = {
            'Código': 80,
            'Nombre': 200,
            'Categoría': 120,
            'Stock': 60,
            'Mín.': 50,
            'Precio': 100,
            'Costo': 100,
            'Proveedor': 150,
            'Estado': 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor='center' if col in ['Stock', 'Mín.', 'Estado'] else 'w')
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Treeview',
            background='white',
            foreground='#1e293b',
            fieldbackground='white',
            rowheight=35,
            font=('Segoe UI', 10)
        )
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#f1f5f9', foreground='#1e293b')
        style.map('Treeview', background=[('selected', '#8b5cf6')])
        
        # Botones de acciones
        actions_frame = tk.Frame(self, bg='white')
        actions_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        btn_editar = tk.Button(
            actions_frame,
            text="✏️ Editar",
            font=('Segoe UI', 10),
            bg='#3b82f6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.editar_producto
        )
        btn_editar.pack(side='left', padx=5)
        
        btn_ajustar = tk.Button(
            actions_frame,
            text="📊 Ajustar Stock",
            font=('Segoe UI', 10),
            bg='#10b981',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.ajustar_stock
        )
        btn_ajustar.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            font=('Segoe UI', 10),
            bg='#ef4444',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.eliminar_producto
        )
        btn_eliminar.pack(side='left', padx=5)
        
        # Bind doble click
        self.tree.bind('<Double-1>', lambda e: self.editar_producto())
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
    
    def crear_stat_card(self, parent, titulo, valor, color, icono):
        card = tk.Frame(parent, bg='white', relief='flat', bd=0)
        
        # Borde superior colorido
        top_border = tk.Frame(card, bg=color, height=4)
        top_border.pack(fill='x')
        
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=15, pady=12)
        
        tk.Label(
            content,
            text=icono,
            font=('Segoe UI', 20),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        text_frame = tk.Frame(content, bg='white')
        text_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(
            text_frame,
            text=titulo,
            font=('Segoe UI', 9),
            bg='white',
            fg='#64748b'
        ).pack(anchor='w')
        
        tk.Label(
            text_frame,
            text=valor,
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(anchor='w')
        
        return card
    
    def cargar_productos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        productos = self.logic.obtener_productos()
        
        for producto in productos:
            stock = producto.get('stock', 0)
            min_stock = producto.get('min_stock', 0)
            
            # Determinar estado
            if stock == 0:
                estado = "❌ Sin Stock"
                tag = 'sin_stock'
            elif stock <= min_stock:
                estado = "⚠️ Bajo Stock"
                tag = 'bajo_stock'
            else:
                estado = "✅ Normal"
                tag = 'normal'
            
            values = (
                producto.get('codigo', ''),
                producto.get('nombre', ''),
                producto.get('categoria', ''),
                stock,
                min_stock,
                f"${producto.get('precio', 0):,.0f}",
                f"${producto.get('costo', 0):,.0f}",
                producto.get('proveedor', ''),
                estado
            )
            
            item = self.tree.insert('', 'end', values=values, tags=(tag,))
            # Guardar el ID del producto
            self.tree.set(item, '#0', producto.get('id', ''))
        
        # Configurar colores por tag
        self.tree.tag_configure('sin_stock', background='#fee2e2')
        self.tree.tag_configure('bajo_stock', background='#fef3c7')
        self.tree.tag_configure('normal', background='white')
    
    def seleccionar_producto(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            producto_id = self.tree.set(item, '#0')
            productos = self.logic.obtener_productos()
            self.producto_seleccionado = next((p for p in productos if str(p.get('id')) == str(producto_id)), None)
    
    def buscar_productos(self, *args):
        termino = self.search_var.get()
        if termino and termino != "Buscar por nombre o código...":
            resultados = self.logic.buscar_productos(termino)
            self.mostrar_productos(resultados)
        else:
            self.aplicar_filtros()
    
    def aplicar_filtros(self):
        productos = self.logic.obtener_productos()
        
        # Filtrar por categoría
        if self.categoria_var.get() != "Todas":
            productos = [p for p in productos if p.get('categoria') == self.categoria_var.get()]
        
        # Filtrar por stock
        if self.stock_var.get() == "Bajo Stock":
            productos = [p for p in productos if p.get('stock', 0) <= p.get('min_stock', 0)]
        elif self.stock_var.get() == "Sin Stock":
            productos = [p for p in productos if p.get('stock', 0) == 0]
        
        self.mostrar_productos(productos)
    
    def mostrar_productos(self, productos):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for producto in productos:
            stock = producto.get('stock', 0)
            min_stock = producto.get('min_stock', 0)
            
            if stock == 0:
                estado = "❌ Sin Stock"
                tag = 'sin_stock'
            elif stock <= min_stock:
                estado = "⚠️ Bajo Stock"
                tag = 'bajo_stock'
            else:
                estado = "✅ Normal"
                tag = 'normal'
            
            values = (
                producto.get('codigo', ''),
                producto.get('nombre', ''),
                producto.get('categoria', ''),
                stock,
                min_stock,
                f"${producto.get('precio', 0):,.0f}",
                f"${producto.get('costo', 0):,.0f}",
                producto.get('proveedor', ''),
                estado
            )
            
            item = self.tree.insert('', 'end', values=values, tags=(tag,))
            self.tree.set(item, '#0', producto.get('id', ''))
    
    def abrir_modal_nuevo(self):
        self.abrir_modal_producto("nuevo")
    
    def editar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        self.abrir_modal_producto("editar", self.producto_seleccionado)
    
    def abrir_modal_producto(self, modo, producto=None):
        modal = tk.Toplevel(self)
        modal.title("Nuevo Producto" if modo == "nuevo" else "Editar Producto")
        modal.geometry("500x600")
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()
        
        # Header
        header = tk.Frame(modal, bg='#8b5cf6', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📦 " + ("Nuevo Producto" if modo == "nuevo" else "Editar Producto"),
            font=('Segoe UI', 14, 'bold'),
            bg='#8b5cf6',
            fg='white'
        ).pack(pady=15)
        
        # Formulario
        form_frame = tk.Frame(modal, bg='white')
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Campos
        campos = {
            'codigo': ('Código:', producto.get('codigo', '') if producto else ''),
            'nombre': ('Nombre:', producto.get('nombre', '') if producto else ''),
            'categoria': ('Categoría:', producto.get('categoria', '') if producto else ''),
            'precio': ('Precio:', producto.get('precio', '') if producto else ''),
            'costo': ('Costo:', producto.get('costo', '') if producto else ''),
            'stock': ('Stock:', producto.get('stock', '') if producto else ''),
            'min_stock': ('Stock Mínimo:', producto.get('min_stock', '') if producto else ''),
            'proveedor': ('Proveedor:', producto.get('proveedor', '') if producto else '')
        }
        
        entries = {}
        
        for idx, (key, (label, valor)) in enumerate(campos.items()):
            tk.Label(
                form_frame,
                text=label,
                font=('Segoe UI', 10),
                bg='white',
                fg='#1e293b'
            ).grid(row=idx, column=0, sticky='w', pady=8)
            
            if key == 'categoria':
                entries[key] = ttk.Combobox(
                    form_frame,
                    values=["Electrónica", "Accesorios", "Audio", "Computadoras", "Otros"],
                    font=('Segoe UI', 10),
                    width=30
                )
                entries[key].set(valor)
            else:
                entries[key] = tk.Entry(
                    form_frame,
                    font=('Segoe UI', 10),
                    bg='#f8fafc',
                    relief='solid',
                    bd=1,
                    width=32
                )
                entries[key].insert(0, str(valor))
            
            entries[key].grid(row=idx, column=1, pady=8, padx=(10, 0))
        
        # Botones
        btn_frame = tk.Frame(modal, bg='white')
        btn_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Segoe UI', 10),
            bg='#94a3b8',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=modal.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text="Guardar",
            font=('Segoe UI', 10, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=lambda: self.guardar_producto(modo, entries, producto, modal)
        ).pack(side='right', padx=5)
    
    def guardar_producto(self, modo, entries, producto, modal):
        try:
            datos = {
                'codigo': entries['codigo'].get(),
                'nombre': entries['nombre'].get(),
                'categoria': entries['categoria'].get(),
                'precio': float(entries['precio'].get()),
                'costo': float(entries['costo'].get()),
                'stock': int(entries['stock'].get()),
                'min_stock': int(entries['min_stock'].get()),
                'proveedor': entries['proveedor'].get()
            }
            
            if modo == "nuevo":
                self.logic.crear_producto(**datos)
                messagebox.showinfo("Éxito", "Producto creado correctamente")
            else:
                self.logic.actualizar_producto(producto.get('id'), datos)
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            
            modal.destroy()
            self.cargar_productos()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def ajustar_stock(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        modal = tk.Toplevel(self)
        modal.title("Ajustar Stock")
        modal.geometry("400x300")
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()
        
        # Header
        header = tk.Frame(modal, bg='#10b981', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 Ajustar Stock",
            font=('Segoe UI', 14, 'bold'),
            bg='#10b981',
            fg='white'
        ).pack(pady=15)
        
        # Contenido
        content = tk.Frame(modal, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(
            content,
            text=f"Producto: {self.producto_seleccionado.get('nombre')}",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        tk.Label(
            content,
            text=f"Stock Actual: {self.producto_seleccionado.get('stock')}",
            font=('Segoe UI', 10),
            bg='white'
        ).pack()
        
        # Tipo de ajuste
        tipo_frame = tk.Frame(content, bg='white')
        tipo_frame.pack(pady=15)
        
        tipo_var = tk.StringVar(value="entrada")
        
        tk.Radiobutton(
            tipo_frame,
            text="➕ Entrada",
            variable=tipo_var,
            value="entrada",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            tipo_frame,
            text="➖ Salida",
            variable=tipo_var,
            value="salida",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left', padx=10)
        
        # Cantidad
        tk.Label(
            content,
            text="Cantidad:",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(pady=(10, 5))
        
        cantidad_entry = tk.Entry(
            content,
            font=('Segoe UI', 11),
            bg='#f8fafc',
            relief='solid',
            bd=1,
            width=20,
            justify='center'
        )
        cantidad_entry.pack()
        
        # Botones
        btn_frame = tk.Frame(modal, bg='white')
        btn_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        def guardar_ajuste():
            try:
                cantidad = int(cantidad_entry.get())
                self.logic.ajustar_stock(
                    self.producto_seleccionado.get('id'),
                    cantidad,
                    tipo_var.get()
                )
                messagebox.showinfo("Éxito", "Stock ajustado correctamente")
                modal.destroy()
                self.cargar_productos()
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida")
            except Exception as e:
                messagebox.showerror("Error", f"Error al ajustar stock: {str(e)}")
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Segoe UI', 10),
            bg='#94a3b8',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=modal.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text="Guardar",
            font=('Segoe UI', 10, 'bold'),
            bg='#10b981',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=guardar_ajuste
        ).pack(side='right', padx=5)
    
    def eliminar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el producto '{self.producto_seleccionado.get('nombre')}'?"
        )
        
        if respuesta:
            try:
                self.logic.eliminar_producto(self.producto_seleccionado.get('id'))
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.producto_seleccionado = None
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")