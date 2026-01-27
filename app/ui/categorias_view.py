import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.categorias_logic import CategoriasLogic

class CategoriasView(ttk.Frame):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.categoria_seleccionada = None
        
        self.configurar_estilos()
        self.crear_widgets()
        self.cargar_categorias()
    
    def configurar_estilos(self):
        """Configura los estilos personalizados para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores principales (mismos que ventas_view)
        COLOR_PRIMARY = "#2C3E50"
        COLOR_SECONDARY = "#3498DB"
        COLOR_SUCCESS = "#27AE60"
        COLOR_DANGER = "#E74C3C"
        COLOR_WARNING = "#F39C12"
        COLOR_INFO = "#3498DB"
        COLOR_BG = "#ECF0F1"
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
        
        # Labels
        style.configure("Custom.TLabel",
                       background=COLOR_WHITE,
                       foreground=COLOR_TEXT,
                       font=("Segoe UI", 10))
        
        style.configure("Title.TLabel",
                       background=COLOR_BG,
                       foreground=COLOR_PRIMARY,
                       font=("Segoe UI", 18, "bold"))
        
        # Entry
        style.configure("Custom.TEntry",
                       fieldbackground=COLOR_WHITE,
                       foreground=COLOR_TEXT,
                       borderwidth=1)
        
        # Botones
        style.configure("Primary.TButton",
                       background=COLOR_SECONDARY,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 10))
        style.map("Primary.TButton",
                 background=[("active", "#2980B9")])
        
        style.configure("Success.TButton",
                       background=COLOR_SUCCESS,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 10))
        style.map("Success.TButton",
                 background=[("active", "#229954")])
        
        style.configure("Danger.TButton",
                       background=COLOR_DANGER,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 10))
        style.map("Danger.TButton",
                 background=[("active", "#C0392B")])
        
        style.configure("Warning.TButton",
                       background=COLOR_WARNING,
                       foreground=COLOR_WHITE,
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0,
                       focuscolor="none",
                       padding=(15, 10))
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
        # Configurar frame principal
        self.configure(style="Custom.TFrame")
        self.pack(fill="both", expand=True)
        
        # Frame contenedor con padding
        main_frame = ttk.Frame(self, style="Custom.TFrame", padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título principal
        title_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="📂 Gestión de Categorías",
            style="Title.TLabel"
        )
        title_label.pack()
        
        # Separador
        separator = ttk.Separator(title_frame, orient="horizontal")
        separator.pack(fill="x", pady=(10, 0))
        
        # Frame contenedor de dos columnas
        content_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # --- COLUMNA IZQUIERDA: FORMULARIO ---
        form_frame = ttk.LabelFrame(
            content_frame, 
            text="📝 Datos de la Categoría",
            padding=20,
            style="Custom.TLabelframe"
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Campo Nombre
        ttk.Label(
            form_frame, 
            text="Nombre de la Categoría:",
            style="Custom.TLabel"
        ).pack(anchor="w", pady=(0, 5))
        
        self.nombre_entry = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.nombre_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Campo Descripción
        ttk.Label(
            form_frame, 
            text="Descripción:",
            style="Custom.TLabel"
        ).pack(anchor="w", pady=(0, 5))
        
        # Frame para Text widget con borde
        text_frame = ttk.Frame(form_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self.descripcion_text = tk.Text(
            text_frame, 
            font=("Segoe UI", 10),
            height=6,
            wrap=tk.WORD,
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#BDC3C7",
            highlightcolor="#3498DB",
            padx=10,
            pady=10
        )
        self.descripcion_text.pack(fill="both", expand=True)
        
        # Botones de acción
        btn_frame = ttk.Frame(form_frame, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(
            btn_frame, 
            text="💾 Guardar",
            command=self.guardar_categoria,
            style="Success.TButton"
        ).pack(fill="x", pady=(0, 8))
        
        ttk.Button(
            btn_frame, 
            text="✏️ Actualizar",
            command=self.actualizar_categoria,
            style="Primary.TButton"
        ).pack(fill="x", pady=(0, 8))
        
        ttk.Button(
            btn_frame, 
            text="🗑️ Eliminar",
            command=self.eliminar_categoria,
            style="Danger.TButton"
        ).pack(fill="x", pady=(0, 8))
        
        ttk.Button(
            btn_frame, 
            text="🧹 Limpiar",
            command=self.limpiar_formulario,
            style="Warning.TButton"
        ).pack(fill="x")
        
        # --- COLUMNA DERECHA: LISTA DE CATEGORÍAS ---
        list_frame = ttk.LabelFrame(
            content_frame, 
            text="📋 Categorías Existentes",
            padding=20,
            style="Custom.TLabelframe"
        )
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para Treeview con scrollbar
        tree_container = ttk.Frame(list_frame, style="Custom.TFrame")
        tree_container.pack(fill="both", expand=True)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Treeview
        columns = ("ID", "Nombre", "Descripción")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Nombre", width=180, anchor=tk.W)
        self.tree.column("Descripción", width=300, anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_container,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_categoria_select)
        
        # Info de ayuda
        help_frame = ttk.Frame(list_frame, style="Custom.TFrame")
        help_frame.pack(fill="x", pady=(15, 0))
        
        help_label = ttk.Label(
            help_frame,
            text="💡 Haz clic en una categoría para editar o eliminar",
            style="Custom.TLabel",
            foreground="#7F8C8D",
            font=("Segoe UI", 9, "italic")
        )
        help_label.pack()
    
    def cargar_categorias(self):
        """Carga las categorías en el treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        categorias = CategoriasLogic.obtener_todas_categorias()
        
        for cat in categorias:
            descripcion = cat['descripcion'] if cat['descripcion'] else ""
            descripcion_corta = (descripcion[:50] + "...") if len(descripcion) > 50 else descripcion
            
            self.tree.insert("", "end", values=(
                cat['id'], 
                cat['nombre'], 
                descripcion_corta
            ))
    
    def guardar_categoria(self):
        """Guarda una nueva categoría"""
        nombre = self.nombre_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", "end").strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre de la categoría es obligatorio")
            return
        
        resultado, mensaje = CategoriasLogic.crear_categoria(nombre, descripcion)
        
        if resultado:
            messagebox.showinfo("✅ Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("❌ Error", mensaje)
    
    def actualizar_categoria(self):
        """Actualiza la categoría seleccionada"""
        if not self.categoria_seleccionada:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione una categoría para actualizar")
            return
        
        nombre = self.nombre_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", "end").strip()
        
        if not nombre:
            messagebox.showerror("❌ Error", "El nombre de la categoría es obligatorio")
            return
        
        resultado, mensaje = CategoriasLogic.actualizar_categoria(
            self.categoria_seleccionada['id'], nombre, descripcion
        )
        
        if resultado:
            messagebox.showinfo("✅ Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("❌ Error", mensaje)
    
    def eliminar_categoria(self):
        """Elimina la categoría seleccionada"""
        if not self.categoria_seleccionada:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione una categoría para eliminar")
            return
        
        if messagebox.askyesno("🗑️ Confirmar eliminación", 
                             f"¿Está seguro de eliminar la categoría '{self.categoria_seleccionada['nombre']}'?\n\nEsta acción no se puede deshacer."):
            resultado, mensaje = CategoriasLogic.eliminar_categoria(self.categoria_seleccionada['id'])
            
            if resultado:
                messagebox.showinfo("✅ Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_categorias()
            else:
                messagebox.showerror("❌ Error", mensaje)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, "end")
        self.descripcion_text.delete("1.0", "end")
        self.categoria_seleccionada = None
        self.tree.selection_remove(self.tree.selection())
    
    def on_categoria_select(self, event):
        """Maneja la selección de una categoría"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            # Obtener descripción completa
            categorias = CategoriasLogic.obtener_todas_categorias()
            descripcion_completa = ""
            
            for cat in categorias:
                if cat['id'] == values[0]:
                    descripcion_completa = cat['descripcion'] if cat['descripcion'] else ""
                    break
            
            # Cargar en el formulario
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])
            
            self.descripcion_text.delete("1.0", "end")
            self.descripcion_text.insert("1.0", descripcion_completa)
            
            # Guardar categoría seleccionada
            self.categoria_seleccionada = {
                'id': values[0], 
                'nombre': values[1], 
                'descripcion': descripcion_completa
            }


def crear_vista_categorias(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    # Limpiar el parent antes de crear la nueva vista
    for widget in parent.winfo_children():
        widget.destroy()
    
    vista = CategoriasView(parent, usuario_actual)
    vista.pack(fill=tk.BOTH, expand=True)
    return vista