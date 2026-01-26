import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.inventario_logic import InventarioLogic

class InventarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#f0f2f5')
        self.logic = InventarioLogic()
        self.producto_seleccionado = None
        self.placeholder_active = True
        
        self.configurar_ui()
        self.cargar_productos()
        self.actualizar_estadisticas()
    
    def configurar_ui(self):
        # ============ HEADER MODERNO ============
        header_frame = tk.Frame(self, bg='#ffffff', height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Línea superior decorativa con gradiente simulado
        top_line = tk.Frame(header_frame, bg='#8b5cf6', height=4)
        top_line.pack(fill='x')
        
        header_content = tk.Frame(header_frame, bg='#ffffff')
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Título con icono
        title_frame = tk.Frame(header_content, bg='#ffffff')
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame,
            text="📦",
            font=('Segoe UI', 32),
            bg='#ffffff'
        ).pack(side='left', padx=(0, 15))
        
        title_text = tk.Frame(title_frame, bg='#ffffff')
        title_text.pack(side='left')
        
        tk.Label(
            title_text,
            text="Gestión de Inventario",
            font=('Segoe UI', 22, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        ).pack(anchor='w')
        
        tk.Label(
            title_text,
            text="Administra tus productos y existencias",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#64748b'
        ).pack(anchor='w')
        
        # Botón principal de acción
        btn_nuevo_principal = tk.Button(
            header_content,
            text="➕ Agregar Producto",
            font=('Segoe UI', 11, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=self.abrir_modal_nuevo,
            activebackground='#7c3aed',
            activeforeground='white'
        )
        btn_nuevo_principal.pack(side='right', pady=10)
        
        # Efecto hover para el botón
        def on_enter(e):
            btn_nuevo_principal['bg'] = '#7c3aed'
        
        def on_leave(e):
            btn_nuevo_principal['bg'] = '#8b5cf6'
        
        btn_nuevo_principal.bind('<Enter>', on_enter)
        btn_nuevo_principal.bind('<Leave>', on_leave)
        
        # ============ TARJETAS DE ESTADÍSTICAS ============
        self.stats_frame = tk.Frame(self, bg='#f0f2f5')
        self.stats_frame.pack(fill='x', padx=30, pady=(20, 15))
        
        # Contenedor para las tarjetas
        cards_container = tk.Frame(self.stats_frame, bg='#f0f2f5')
        cards_container.pack(fill='x')
        
        # IDs de las tarjetas para actualizar después
        self.stat_cards = {}
        
        # ============ BARRA DE HERRAMIENTAS ============
        toolbar_frame = tk.Frame(self, bg='#ffffff')
        toolbar_frame.pack(fill='x', padx=30, pady=(0, 15))
        
        # Aplicar sombra simulada
        shadow = tk.Frame(self, bg='#e2e8f0', height=2)
        shadow.place(in_=toolbar_frame, relx=0, rely=1, relwidth=1)
        
        toolbar_content = tk.Frame(toolbar_frame, bg='#ffffff')
        toolbar_content.pack(fill='x', padx=20, pady=15)
        
        # === BÚSQUEDA MEJORADA ===
        search_container = tk.Frame(toolbar_content, bg='#f8fafc', relief='solid', bd=1)
        search_container.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            search_container,
            text="🔍",
            font=('Segoe UI', 13),
            bg='#f8fafc',
            fg='#64748b'
        ).pack(side='left', padx=(15, 8))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.buscar_productos)
        
        self.search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bg='#f8fafc',
            fg='#1e293b',
            relief='flat',
            width=40,
            insertbackground='#8b5cf6'
        )
        self.search_entry.pack(side='left', fill='x', expand=True, pady=10, padx=(0, 15))
        self.search_entry.insert(0, "Buscar por nombre o código...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # === FILTROS MODERNOS ===
        filters_container = tk.Frame(toolbar_content, bg='#ffffff')
        filters_container.pack(side='left', padx=(20, 0))
        
        # Filtro de categoría
        filter_cat_frame = tk.Frame(filters_container, bg='#ffffff')
        filter_cat_frame.pack(side='left', padx=5)
        
        tk.Label(
            filter_cat_frame,
            text="Categoría:",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#475569'
        ).pack(side='left', padx=(0, 8))
        
        self.categoria_var = tk.StringVar(value="Todas")
        style = ttk.Style()
        style.configure('Custom.TCombobox', padding=5)
        
        self.categoria_combo = ttk.Combobox(
            filter_cat_frame,
            textvariable=self.categoria_var,
            values=["Todas", "Bebidas", "Panadería", "Lácteos", "Granos", "Aceites", "Otros"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10),
            style='Custom.TCombobox'
        )
        self.categoria_combo.pack(side='left')
        self.categoria_combo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())
        
        # Filtro de stock
        filter_stock_frame = tk.Frame(filters_container, bg='#ffffff')
        filter_stock_frame.pack(side='left', padx=5)
        
        tk.Label(
            filter_stock_frame,
            text="Stock:",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#475569'
        ).pack(side='left', padx=(0, 8))
        
        self.stock_var = tk.StringVar(value="Todos")
        stock_combo = ttk.Combobox(
            filter_stock_frame,
            textvariable=self.stock_var,
            values=["Todos", "Bajo Stock", "Sin Stock", "Normal"],
            state='readonly',
            width=12,
            font=('Segoe UI', 10),
            style='Custom.TCombobox'
        )
        stock_combo.pack(side='left')
        stock_combo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())
        
        # ============ TABLA DE PRODUCTOS ============
        table_container = tk.Frame(self, bg='#ffffff')
        table_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Header de la tabla
        table_header = tk.Frame(table_container, bg='#ffffff')
        table_header.pack(fill='x', padx=2, pady=(15, 0))
        
        tk.Label(
            table_header,
            text="Lista de Productos",
            font=('Segoe UI', 13, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        ).pack(side='left', padx=15)
        
        # Contador de productos
        self.contador_label = tk.Label(
            table_header,
            text="0 productos",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#64748b'
        )
        self.contador_label.pack(side='left', padx=10)
        
        # Frame para la tabla y scrollbars
        table_frame = tk.Frame(table_container, bg='#ffffff')
        table_frame.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        
        # Scrollbars personalizadas
        scroll_y = ttk.Scrollbar(table_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview mejorado
        columns = ('Código', 'Nombre', 'Categoría', 'Stock', 'Mín.', 'Precio', 'Costo', 'Proveedor', 'Estado')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=12,
            selectmode='browse'
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas con anchos optimizados
        column_config = {
            'Código': (100, 'center'),
            'Nombre': (220, 'w'),
            'Categoría': (130, 'center'),
            'Stock': (70, 'center'),
            'Mín.': (60, 'center'),
            'Precio': (100, 'e'),
            'Costo': (100, 'e'),
            'Proveedor': (150, 'w'),
            'Estado': (120, 'center')
        }
        
        for col, (width, anchor) in column_config.items():
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=width, anchor=anchor, minwidth=50)
        
        self.tree.pack(fill='both', expand=True)
        
        # Estilo mejorado para la tabla
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            'Treeview',
            background='#ffffff',
            foreground='#1e293b',
            fieldbackground='#ffffff',
            rowheight=38,
            font=('Segoe UI', 10),
            borderwidth=0
        )
        
        style.configure(
            'Treeview.Heading',
            font=('Segoe UI', 10, 'bold'),
            background='#f8fafc',
            foreground='#475569',
            relief='flat',
            borderwidth=0
        )
        
        style.map('Treeview',
            background=[('selected', '#8b5cf6')],
            foreground=[('selected', '#ffffff')]
        )
        
        style.map('Treeview.Heading',
            background=[('active', '#e2e8f0')]
        )
        
        # ============ BOTONES DE ACCIÓN ============
        actions_frame = tk.Frame(table_container, bg='#ffffff')
        actions_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Separador visual
        tk.Frame(actions_frame, bg='#e2e8f0', height=1).pack(fill='x', pady=(0, 15))
        
        buttons_data = [
            ("✏️ Editar", "#3b82f6", "#2563eb", self.editar_producto),
            ("📊 Ajustar Stock", "#10b981", "#059669", self.ajustar_stock),
            ("🗑️ Eliminar", "#ef4444", "#dc2626", self.eliminar_producto),
            ("🔄 Actualizar", "#6366f1", "#4f46e5", self.refrescar_datos)
        ]
        
        for text, bg_color, hover_color, command in buttons_data:
            btn = tk.Button(
                actions_frame,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                bg=bg_color,
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=10,
                command=command,
                activebackground=hover_color,
                activeforeground='white'
            )
            btn.pack(side='left', padx=5)
            
            # Efecto hover
            btn.bind('<Enter>', lambda e, b=btn, c=hover_color: b.configure(bg=c))
            btn.bind('<Leave>', lambda e, b=btn, c=bg_color: b.configure(bg=c))
        
        # Bind eventos
        self.tree.bind('<Double-1>', lambda e: self.editar_producto())
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
        self.tree.bind('<Delete>', lambda e: self.eliminar_producto())
    
    def crear_stat_card(self, parent, titulo, valor, color, icono, key):
        """Crea una tarjeta de estadística moderna"""
        card = tk.Frame(parent, bg='#ffffff', relief='flat', bd=0)
        card.pack(side='left', padx=8, fill='both', expand=True)
        
        # Borde superior colorido
        top_border = tk.Frame(card, bg=color, height=4)
        top_border.pack(fill='x')
        
        # Contenido
        content = tk.Frame(card, bg='#ffffff')
        content.pack(fill='both', expand=True, padx=20, pady=18)
        
        # Icono
        icon_label = tk.Label(
            content,
            text=icono,
            font=('Segoe UI', 28),
            bg='#ffffff'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        # Texto
        text_frame = tk.Frame(content, bg='#ffffff')
        text_frame.pack(side='left', fill='both', expand=True)
        
        titulo_label = tk.Label(
            text_frame,
            text=titulo,
            font=('Segoe UI', 9),
            bg='#ffffff',
            fg='#64748b'
        )
        titulo_label.pack(anchor='w')
        
        valor_label = tk.Label(
            text_frame,
            text=valor,
            font=('Segoe UI', 22, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        )
        valor_label.pack(anchor='w')
        
        # Guardar referencias para actualizar
        self.stat_cards[key] = valor_label
        
        # Sombra sutil
        shadow = tk.Frame(card, bg='#e2e8f0', height=1)
        shadow.pack(fill='x')
        
        return card
    
    def actualizar_estadisticas(self):
        """Actualiza las tarjetas de estadísticas"""
        # Limpiar frame de stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        cards_container = tk.Frame(self.stats_frame, bg='#f0f2f5')
        cards_container.pack(fill='x')
        
        productos = self.logic.obtener_productos()
        total_productos = len(productos)
        bajo_stock = len(self.logic.productos_bajo_stock())
        sin_stock = len([p for p in productos if p.get('stock', 0) == 0])
        valor_total = sum(p.get('precio', 0) * p.get('stock', 0) for p in productos)
        
        self.crear_stat_card(cards_container, "Total Productos", str(total_productos), "#3b82f6", "📦", "total")
        self.crear_stat_card(cards_container, "Bajo Stock", str(bajo_stock), "#f59e0b", "⚠️", "bajo")
        self.crear_stat_card(cards_container, "Sin Stock", str(sin_stock), "#ef4444", "❌", "sin")
        self.crear_stat_card(cards_container, "Valor Inventario", f"${valor_total:,.0f}", "#10b981", "💰", "valor")
    
    def on_search_focus_in(self, event):
        """Maneja el evento cuando el campo de búsqueda recibe el foco"""
        if self.placeholder_active:
            self.search_entry.delete(0, 'end')
            self.search_entry.config(fg='#1e293b')
            self.placeholder_active = False
    
    def on_search_focus_out(self, event):
        """Maneja el evento cuando el campo de búsqueda pierde el foco"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar por nombre o código...")
            self.search_entry.config(fg='#94a3b8')
            self.placeholder_active = True
    
    def cargar_productos(self):
        """Carga todos los productos en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.logic.obtener_productos()
        
        for producto in productos:
            self.insertar_producto_en_tabla(producto)
        
        # Actualizar contador
        self.contador_label.config(text=f"{len(productos)} producto{'s' if len(productos) != 1 else ''}")
        
        # Configurar colores por estado
        self.tree.tag_configure('sin_stock', background='#fee2e2', foreground='#991b1b')
        self.tree.tag_configure('bajo_stock', background='#fef3c7', foreground='#92400e')
        self.tree.tag_configure('normal', background='#ffffff', foreground='#1e293b')
    
    def insertar_producto_en_tabla(self, producto):
        """Inserta un producto en la tabla con formato"""
        stock = producto.get('stock', 0)
        min_stock = producto.get('min_stock', 0)
        
        # Determinar estado y tag
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
            producto.get('codigo', 'N/A'),
            producto.get('nombre', ''),
            producto.get('categoria', 'Sin categoría'),
            stock,
            min_stock,
            f"${producto.get('precio', 0):,.0f}",
            f"${producto.get('costo', 0):,.0f}",
            producto.get('proveedor', 'N/A'),
            estado
        )
        
        # Usar el iid para guardar el ID del producto
        producto_id = producto.get('id', '')
        item = self.tree.insert('', 'end', iid=f"prod_{producto_id}", values=values, tags=(tag,))
    
    def seleccionar_producto(self, event):
        """Maneja la selección de un producto en la tabla"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            # Extraer el ID del iid (formato: prod_123)
            producto_id = item.replace('prod_', '')
            productos = self.logic.obtener_productos()
            self.producto_seleccionado = next(
                (p for p in productos if str(p.get('id')) == str(producto_id)), None
            )
    
    def buscar_productos(self, *args):
        """Busca productos según el término ingresado"""
        termino = self.search_var.get()
        
        if termino and termino != "Buscar por nombre o código..." and not self.placeholder_active:
            resultados = self.logic.buscar_productos(termino)
            self.mostrar_productos(resultados)
        else:
            self.aplicar_filtros()
    
    def aplicar_filtros(self):
        """Aplica filtros de categoría y stock"""
        productos = self.logic.obtener_productos()
        
        # Filtrar por categoría
        if self.categoria_var.get() != "Todas":
            productos = [p for p in productos if p.get('categoria') == self.categoria_var.get()]
        
        # Filtrar por stock
        stock_filter = self.stock_var.get()
        if stock_filter == "Bajo Stock":
            productos = [p for p in productos if 0 < p.get('stock', 0) <= p.get('min_stock', 0)]
        elif stock_filter == "Sin Stock":
            productos = [p for p in productos if p.get('stock', 0) == 0]
        elif stock_filter == "Normal":
            productos = [p for p in productos if p.get('stock', 0) > p.get('min_stock', 0)]
        
        self.mostrar_productos(productos)
    
    def mostrar_productos(self, productos):
        """Muestra una lista filtrada de productos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for producto in productos:
            self.insertar_producto_en_tabla(producto)
        
        # Actualizar contador
        self.contador_label.config(text=f"{len(productos)} producto{'s' if len(productos) != 1 else ''}")
    
    def refrescar_datos(self):
        """Refresca todos los datos de la vista"""
        self.cargar_productos()
        self.actualizar_estadisticas()
        messagebox.showinfo("Actualizado", "Datos actualizados correctamente")
    
    def abrir_modal_nuevo(self):
        """Abre el modal para crear un nuevo producto"""
        self.abrir_modal_producto("nuevo")
    
    def editar_producto(self):
        """Abre el modal para editar el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto de la lista")
            return
        self.abrir_modal_producto("editar", self.producto_seleccionado)
    
    def abrir_modal_producto(self, modo, producto=None):
        """Crea y muestra el modal de producto (nuevo o editar)"""
        if modo not in ("nuevo", "editar"):
            return
        
        modal = tk.Toplevel(self)
        modal.title("Nuevo Producto" if modo == "nuevo" else "Editar Producto")
        modal.geometry("520x680")
        modal.configure(bg='#ffffff')
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)
        
        # Centrar modal
        modal.update_idletasks()
        w, h = 520, 680
        x = (modal.winfo_screenwidth() - w) // 2
        y = (modal.winfo_screenheight() - h) // 2
        modal.geometry(f"{w}x{h}+{x}+{y}")
        
        # ================= HEADER =================
        header = tk.Frame(modal, bg='#8b5cf6', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📦 " + ("Nuevo Producto" if modo == "nuevo" else "Editar Producto"),
            font=('Segoe UI', 15, 'bold'),
            bg='#8b5cf6',
            fg='white'
        ).pack(expand=True)
        
        # ================= CONTENEDOR CON SCROLL =================
        main_container = tk.Frame(modal, bg='#ffffff')
        main_container.pack(fill='both', expand=True)
        
        # Canvas y Scrollbar
        canvas = tk.Canvas(main_container, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ================= FORMULARIO =================
        form_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        form_frame.pack(fill='both', expand=True, padx=35, pady=20)
        
        # Campos del formulario
        campos = [
            ('codigo', 'Código de Barras', 'text'),
            ('nombre', 'Nombre del Producto', 'text'),
            ('categoria', 'Categoría', 'combo'),
            ('precio', 'Precio de Venta', 'number'),
            ('costo', 'Costo del Producto', 'number'),
            ('stock', 'Stock Actual', 'number'),
            ('min_stock', 'Stock Mínimo', 'number'),
            ('proveedor', 'Proveedor', 'text')
        ]
        
        entries = {}
        
        for idx, (key, label, tipo) in enumerate(campos):
            # Label
            tk.Label(
                form_frame,
                text=label + ":",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#1e293b'
            ).grid(row=idx*2, column=0, sticky='w', pady=(0, 4))
            
            valor = producto.get(key, '') if producto else ''
            
            # Campo de entrada
            if tipo == 'combo':
                entry = ttk.Combobox(
                    form_frame,
                    values=["Bebidas", "Panadería", "Lácteos", "Granos", "Aceites", "Otros"],
                    font=('Segoe UI', 11),
                    width=36,
                    state='readonly'
                )
                entry.set(valor if valor else 'Seleccione...')
            else:
                entry = tk.Entry(
                    form_frame,
                    font=('Segoe UI', 11),
                    bg='#f8fafc',
                    fg='#1e293b',
                    relief='solid',
                    bd=1,
                    width=38,
                    insertbackground='#8b5cf6'
                )
                if valor != '':
                    entry.insert(0, str(valor))
            
            entry.grid(row=idx*2+1, column=0, sticky='ew', pady=(0, 12))
            entries[key] = entry
        
        # Configurar grid
        form_frame.columnconfigure(0, weight=1)
        
        # Bind scroll con mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Limpiar bind cuando se cierre el modal
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            modal.destroy()
        
        modal.protocol("WM_DELETE_WINDOW", on_close)
        
        # ================= FOOTER CON BOTONES =================
        footer = tk.Frame(modal, bg='#ffffff', height=80)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        # Línea separadora
        tk.Frame(footer, bg='#e2e8f0', height=1).pack(fill='x')
        
        btn_container = tk.Frame(footer, bg='#ffffff')
        btn_container.pack(fill='both', expand=True, padx=35, pady=15)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            btn_container,
            text="Cancelar",
            font=('Segoe UI', 11),
            bg='#94a3b8',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=on_close,
            activebackground='#64748b'
        )
        btn_cancelar.pack(side='right', padx=(10, 0))
        
        # Botón Guardar
        btn_guardar = tk.Button(
            btn_container,
            text="💾 Guardar Producto",
            font=('Segoe UI', 11, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=lambda: self.guardar_producto(modo, entries, producto, modal),
            activebackground='#7c3aed'
        )
        btn_guardar.pack(side='right')
        
        # Efectos hover
        btn_cancelar.bind('<Enter>', lambda e: btn_cancelar.configure(bg='#64748b'))
        btn_cancelar.bind('<Leave>', lambda e: btn_cancelar.configure(bg='#94a3b8'))
        btn_guardar.bind('<Enter>', lambda e: btn_guardar.configure(bg='#7c3aed'))
        btn_guardar.bind('<Leave>', lambda e: btn_guardar.configure(bg='#8b5cf6'))
    
    def guardar_producto(self, modo, entries, producto, modal):
        """Guarda o actualiza un producto"""
        try:
            # Validar campos vacíos
            campos_requeridos = ['codigo', 'nombre', 'categoria', 'precio', 'stock']
            for campo in campos_requeridos:
                valor = entries[campo].get().strip()
                if not valor or valor == 'Seleccione...':
                    messagebox.showwarning(
                        "Campo requerido",
                        f"El campo '{campo}' es obligatorio"
                    )
                    return
            
            # Construir datos
            datos = {
                'codigo': entries['codigo'].get().strip(),
                'nombre': entries['nombre'].get().strip(),
                'categoria': entries['categoria'].get(),
                'precio': float(entries['precio'].get() or 0),
                'costo': float(entries['costo'].get() or 0),
                'stock': int(entries['stock'].get() or 0),
                'min_stock': int(entries['min_stock'].get() or 5),
                'proveedor': entries['proveedor'].get().strip() or 'N/A'
            }
            
            # Validar que precio y costo sean positivos
            if datos['precio'] < 0 or datos['costo'] < 0:
                messagebox.showerror("Error", "El precio y costo deben ser valores positivos")
                return
            
            # Validar stock
            if datos['stock'] < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo")
                return
            
            # Guardar según el modo
            if modo == "nuevo":
                self.logic.crear_producto(**datos)
                messagebox.showinfo("✅ Éxito", "Producto creado correctamente")
            else:
                self.logic.actualizar_producto(producto.get('id'), datos)
                messagebox.showinfo("✅ Éxito", "Producto actualizado correctamente")
            
            modal.destroy()
            self.cargar_productos()
            self.actualizar_estadisticas()
            
        except ValueError as e:
            messagebox.showerror("Error de validación", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def ajustar_stock(self):
        """Abre el modal para ajustar el stock del producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto de la lista")
            return
        
        modal = tk.Toplevel(self)
        modal.title("Ajustar Stock")
        modal.geometry("450x380")
        modal.configure(bg='#ffffff')
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (450 // 2)
        y = (modal.winfo_screenheight() // 2) - (380 // 2)
        modal.geometry(f"450x380+{x}+{y}")
        
        # Header
        header = tk.Frame(modal, bg='#10b981', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 Ajustar Stock",
            font=('Segoe UI', 16, 'bold'),
            bg='#10b981',
            fg='white'
        ).pack(expand=True)
        
        # Contenido
        content = tk.Frame(modal, bg='#ffffff')
        content.pack(fill='both', expand=True, padx=40, pady=25)
        
        # Información del producto
        info_frame = tk.Frame(content, bg='#f8fafc', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            info_frame,
            text=f"📦 {self.producto_seleccionado.get('nombre')}",
            font=('Segoe UI', 12, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        ).pack(pady=(15, 5))
        
        stock_actual = self.producto_seleccionado.get('stock', 0)
        tk.Label(
            info_frame,
            text=f"Stock Actual: {stock_actual} unidades",
            font=('Segoe UI', 11),
            bg='#f8fafc',
            fg='#64748b'
        ).pack(pady=(0, 15))
        
        # Tipo de ajuste
        tk.Label(
            content,
            text="Tipo de Movimiento:",
            font=('Segoe UI', 10, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        ).pack(anchor='w', pady=(10, 8))
        
        tipo_frame = tk.Frame(content, bg='#ffffff')
        tipo_frame.pack(fill='x', pady=(0, 20))
        
        tipo_var = tk.StringVar(value="entrada")
        
        # Radio buttons personalizados
        rb_entrada = tk.Radiobutton(
            tipo_frame,
            text="➕ Entrada (Agregar)",
            variable=tipo_var,
            value="entrada",
            font=('Segoe UI', 11),
            bg='#ffffff',
            fg='#1e293b',
            selectcolor='#ffffff',
            activebackground='#ffffff',
            activeforeground='#10b981',
            cursor='hand2'
        )
        rb_entrada.pack(anchor='w', pady=5)
        
        rb_salida = tk.Radiobutton(
            tipo_frame,
            text="➖ Salida (Retirar)",
            variable=tipo_var,
            value="salida",
            font=('Segoe UI', 11),
            bg='#ffffff',
            fg='#1e293b',
            selectcolor='#ffffff',
            activebackground='#ffffff',
            activeforeground='#ef4444',
            cursor='hand2'
        )
        rb_salida.pack(anchor='w', pady=5)
        
        # Cantidad
        tk.Label(
            content,
            text="Cantidad:",
            font=('Segoe UI', 10, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        ).pack(anchor='w', pady=(10, 8))
        
        cantidad_entry = tk.Entry(
            content,
            font=('Segoe UI', 13),
            bg='#f8fafc',
            fg='#1e293b',
            relief='solid',
            bd=1,
            width=15,
            justify='center',
            insertbackground='#10b981'
        )
        cantidad_entry.pack(pady=(0, 10))
        cantidad_entry.focus()
        
        # Resultado proyectado
        resultado_label = tk.Label(
            content,
            text="",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#64748b'
        )
        resultado_label.pack(pady=(5, 0))
        
        def actualizar_resultado(*args):
            """Muestra el stock resultante"""
            try:
                cantidad = int(cantidad_entry.get() or 0)
                if tipo_var.get() == "entrada":
                    nuevo_stock = stock_actual + cantidad
                    resultado_label.config(
                        text=f"Stock resultante: {nuevo_stock} unidades",
                        fg='#10b981'
                    )
                else:
                    nuevo_stock = stock_actual - cantidad
                    color = '#ef4444' if nuevo_stock < 0 else '#10b981'
                    resultado_label.config(
                        text=f"Stock resultante: {nuevo_stock} unidades",
                        fg=color
                    )
            except:
                resultado_label.config(text="")
        
        cantidad_entry.bind('<KeyRelease>', actualizar_resultado)
        tipo_var.trace('w', actualizar_resultado)
        
        # Frame de botones
        btn_frame = tk.Frame(modal, bg='#ffffff')
        btn_frame.pack(fill='x', padx=40, pady=(0, 25))
        
        def guardar_ajuste():
            try:
                cantidad = int(cantidad_entry.get())
                
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a cero")
                    return
                
                if tipo_var.get() == "salida" and cantidad > stock_actual:
                    respuesta = messagebox.askyesno(
                        "Stock insuficiente",
                        f"La cantidad a retirar ({cantidad}) es mayor al stock actual ({stock_actual}).\n\n¿Desea continuar de todas formas?"
                    )
                    if not respuesta:
                        return
                
                self.logic.ajustar_stock(
                    self.producto_seleccionado.get('id'),
                    cantidad,
                    tipo_var.get()
                )
                
                messagebox.showinfo("✅ Éxito", "Stock ajustado correctamente")
                modal.destroy()
                self.cargar_productos()
                self.actualizar_estadisticas()
                
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida")
            except Exception as e:
                messagebox.showerror("Error", f"Error al ajustar stock: {str(e)}")
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Segoe UI', 11),
            bg='#94a3b8',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=modal.destroy,
            activebackground='#64748b'
        )
        btn_cancelar.pack(side='right', padx=(10, 0))
        
        # Botón Guardar
        btn_guardar = tk.Button(
            btn_frame,
            text="💾 Guardar Ajuste",
            font=('Segoe UI', 11, 'bold'),
            bg='#10b981',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=guardar_ajuste,
            activebackground='#059669'
        )
        btn_guardar.pack(side='right')
        
        # Efectos hover
        btn_cancelar.bind('<Enter>', lambda e: btn_cancelar.configure(bg='#64748b'))
        btn_cancelar.bind('<Leave>', lambda e: btn_cancelar.configure(bg='#94a3b8'))
        btn_guardar.bind('<Enter>', lambda e: btn_guardar.configure(bg='#059669'))
        btn_guardar.bind('<Leave>', lambda e: btn_guardar.configure(bg='#10b981'))
        
        # Enter para guardar
        cantidad_entry.bind('<Return>', lambda e: guardar_ajuste())
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto de la lista")
            return
        
        # Crear modal personalizado de confirmación
        modal = tk.Toplevel(self)
        modal.title("Confirmar Eliminación")
        modal.geometry("450x280")
        modal.configure(bg='#ffffff')
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (450 // 2)
        y = (modal.winfo_screenheight() // 2) - (280 // 2)
        modal.geometry(f"450x280+{x}+{y}")
        
        # Header de advertencia
        header = tk.Frame(modal, bg='#ef4444', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⚠️ Confirmar Eliminación",
            font=('Segoe UI', 15, 'bold'),
            bg='#ef4444',
            fg='white'
        ).pack(expand=True)
        
        # Contenido
        content = tk.Frame(modal, bg='#ffffff')
        content.pack(fill='both', expand=True, padx=40, pady=25)
        
        tk.Label(
            content,
            text="¿Está seguro de que desea eliminar este producto?",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg='#1e293b'
        ).pack(pady=(0, 15))
        
        # Info del producto
        info_frame = tk.Frame(content, bg='#fef3c7', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            info_frame,
            text=f"📦 {self.producto_seleccionado.get('nombre')}",
            font=('Segoe UI', 11, 'bold'),
            bg='#fef3c7',
            fg='#92400e'
        ).pack(pady=(10, 5))
        
        tk.Label(
            info_frame,
            text=f"Código: {self.producto_seleccionado.get('codigo')}",
            font=('Segoe UI', 9),
            bg='#fef3c7',
            fg='#92400e'
        ).pack(pady=(0, 10))
        
        tk.Label(
            content,
            text="Esta acción no se puede deshacer.",
            font=('Segoe UI', 9, 'italic'),
            bg='#ffffff',
            fg='#64748b'
        ).pack()
        
        # Frame de botones
        btn_frame = tk.Frame(modal, bg='#ffffff')
        btn_frame.pack(fill='x', padx=40, pady=(0, 25))
        
        def confirmar_eliminacion():
            try:
                self.logic.eliminar_producto(self.producto_seleccionado.get('id'))
                messagebox.showinfo("✅ Éxito", "Producto eliminado correctamente")
                self.producto_seleccionado = None
                modal.destroy()
                self.cargar_productos()
                self.actualizar_estadisticas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Segoe UI', 11),
            bg='#94a3b8',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=modal.destroy,
            activebackground='#64748b'
        )
        btn_cancelar.pack(side='right', padx=(10, 0))
        
        # Botón Eliminar
        btn_eliminar = tk.Button(
            btn_frame,
            text="🗑️ Sí, Eliminar",
            font=('Segoe UI', 11, 'bold'),
            bg='#ef4444',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12,
            command=confirmar_eliminacion,
            activebackground='#dc2626'
        )
        btn_eliminar.pack(side='right')
        
        # Efectos hover
        btn_cancelar.bind('<Enter>', lambda e: btn_cancelar.configure(bg='#64748b'))
        btn_cancelar.bind('<Leave>', lambda e: btn_cancelar.configure(bg='#94a3b8'))
        btn_eliminar.bind('<Enter>', lambda e: btn_eliminar.configure(bg='#dc2626'))
        btn_eliminar.bind('<Leave>', lambda e: btn_eliminar.configure(bg='#ef4444'))


def crear_vista_inventario(parent, ventana_principal=None):
    """Función para crear la vista de inventario dentro del frame parent"""
    for widget in parent.winfo_children():
        widget.destroy()
    
    vista = InventarioView(parent=parent)
    vista.pack(fill=tk.BOTH, expand=True)