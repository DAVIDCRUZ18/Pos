import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.categorias_logic import CategoriasLogic

class CategoriasView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.categoria_seleccionada = None
        
        self.crear_widgets()
        self.cargar_categorias()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Categorías", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Nueva Categoría", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_entry = ttk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, pady=5)
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky="w", pady=5)
        self.descripcion_text = tk.Text(form_frame, width=30, height=3)
        self.descripcion_text.grid(row=1, column=1, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar_categoria).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_categoria).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_categoria).pack(side="left", padx=5)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Categorías Existentes", padding=10)
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Treeview
        columns = ("ID", "Nombre", "Descripción")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Nombre" else 150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_categoria_select)
        
        # Configurar grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def cargar_categorias(self):
        """Carga las categorías en el treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        categorias = CategoriasLogic.obtener_todas_categorias()
        
        for cat in categorias:
            self.tree.insert("", "end", values=(
                cat['id'], 
                cat['nombre'], 
                cat['descripcion'][:30] + "..." if cat['descripcion'] and len(cat['descripcion']) > 30 else cat['descripcion']
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
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_categoria(self):
        """Actualiza la categoría seleccionada"""
        if not self.categoria_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para actualizar")
            return
        
        nombre = self.nombre_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", "end").strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre de la categoría es obligatorio")
            return
        
        resultado, mensaje = CategoriasLogic.actualizar_categoria(
            self.categoria_seleccionada['id'], nombre, descripcion
        )
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_categoria(self):
        """Elimina la categoría seleccionada"""
        if not self.categoria_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar la categoría '{self.categoria_seleccionada['nombre']}'?"):
            resultado, mensaje = CategoriasLogic.eliminar_categoria(self.categoria_seleccionada['id'])
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_categorias()
            else:
                messagebox.showerror("Error", mensaje)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, "end")
        self.descripcion_text.delete("1.0", "end")
        self.categoria_seleccionada = None
    
    def on_categoria_select(self, event):
        """Maneja la selección de una categoría"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            # Cargar en el formulario
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])
            
            self.descripcion_text.delete("1.0", "end")
            self.descripcion_text.insert("1.0", values[2])
            
            # Guardar categoría seleccionada
            self.categoria_seleccionada = {'id': values[0], 'nombre': values[1], 'descripcion': values[2]}

def crear_vista_categorias(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    return CategoriasView(parent, usuario_actual)