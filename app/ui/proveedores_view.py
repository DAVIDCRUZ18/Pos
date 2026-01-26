import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.proveedores_logic import ProveedoresLogic

class ProveedoresView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.proveedor_seleccionado = None
        
        self.crear_widgets()
        self.cargar_proveedores()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Proveedores", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Información del Proveedor", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Formulario
        self.crear_formulario_proveedor(form_frame)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Proveedores Registrados", padding=10)
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Treeview y búsqueda
        self.crear_lista_proveedores(list_frame)
        
        # Configurar grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def crear_formulario_proveedor(self, parent):
        # Nombre
        ttk.Label(parent, text="Nombre*:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_entry = ttk.Entry(parent, width=35)
        self.nombre_entry.grid(row=0, column=1, pady=5)
        
        # NIT/RUT
        ttk.Label(parent, text="NIT/RUT:").grid(row=1, column=0, sticky="w", pady=5)
        self.nit_entry = ttk.Entry(parent, width=35)
        self.nit_entry.grid(row=1, column=1, pady=5)
        
        # Teléfono
        ttk.Label(parent, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        self.telefono_entry = ttk.Entry(parent, width=35)
        self.telefono_entry.grid(row=2, column=1, pady=5)
        
        # Contacto
        ttk.Label(parent, text="Contacto:").grid(row=3, column=0, sticky="w", pady=5)
        self.contacto_entry = ttk.Entry(parent, width=35)
        self.contacto_entry.grid(row=3, column=1, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Guardar Proveedor", command=self.guardar_proveedor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_proveedor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_proveedor).pack(side="left", padx=5)
    
    def crear_lista_proveedores(self, parent):
        # Frame de búsqueda
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.buscar_entry = ttk.Entry(search_frame, width=30)
        self.buscar_entry.pack(side="left", padx=5)
        self.buscar_entry.bind("<KeyRelease>", self.on_buscar)
        
        # Treeview
        columns = ("ID", "Nombre", "NIT/RUT", "Teléfono", "Contacto")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("NIT/RUT", text="NIT/RUT")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Contacto", text="Contacto")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("NIT/RUT", width=120)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Contacto", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_proveedor_select)
        
        # Botón de historial
        ttk.Button(parent, text="Ver Historial de Compras", 
                  command=self.ver_historial).pack(pady=(10, 0))
    
    def cargar_proveedores(self):
        """Carga los proveedores en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        proveedores = ProveedoresLogic.obtener_proveedores()
        
        for proveedor in proveedores:
            self.tree.insert("", "end", values=(
                proveedor['id'],
                proveedor['nombre'],
                proveedor['nit_rut'] or '',
                proveedor['telefono'] or '',
                proveedor['contacto'] or ''
            ))
    
    def guardar_proveedor(self):
        """Guarda un nuevo proveedor"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del proveedor es obligatorio")
            return
        
        resultado, mensaje = ProveedoresLogic.crear_proveedor(
            nombre=nombre,
            nit_rut=self.nit_entry.get().strip(),
            telefono=self.telefono_entry.get().strip(),
            contacto=self.contacto_entry.get().strip()
        )
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_proveedor(self):
        """Actualiza el proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para actualizar")
            return
        
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del proveedor es obligatorio")
            return
        
        datos = {
            'nombre': nombre,
            'nit_rut': self.nit_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip(),
            'contacto': self.contacto_entry.get().strip()
        }
        
        resultado, mensaje = ProveedoresLogic.actualizar_proveedor(
            self.proveedor_seleccionado['id'], datos
        )
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_proveedor(self):
        """Elimina el proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar al proveedor '{self.proveedor_seleccionado['nombre']}'?"):
            resultado, mensaje = ProveedoresLogic.eliminar_proveedor(self.proveedor_seleccionado['id'])
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_proveedores()
            else:
                messagebox.showerror("Error", mensaje)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, "end")
        self.nit_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.contacto_entry.delete(0, "end")
        self.proveedor_seleccionado = None
    
    def on_proveedor_select(self, event):
        """Maneja la selección de un proveedor"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])
            
            self.nit_entry.delete(0, "end")
            self.nit_entry.insert(0, values[2])
            
            self.telefono_entry.delete(0, "end")
            self.telefono_entry.insert(0, values[3])
            
            self.contacto_entry.delete(0, "end")
            self.contacto_entry.insert(0, values[4])
            
            self.proveedor_seleccionado = {
                'id': values[0],
                'nombre': values[1],
                'nit_rut': values[2],
                'telefono': values[3],
                'contacto': values[4]
            }
    
    def on_buscar(self, event):
        """Busca proveedores en tiempo real"""
        termino = self.buscar_entry.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        proveedores = ProveedoresLogic.buscar_proveedores(termino) if termino else ProveedoresLogic.obtener_proveedores()
        
        for proveedor in proveedores:
            self.tree.insert("", "end", values=(
                proveedor['id'],
                proveedor['nombre'],
                proveedor['nit_rut'] or '',
                proveedor['telefono'] or '',
                proveedor['contacto'] or ''
            ))
    
    def ver_historial(self):
        """Muestra el historial de compras del proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para ver su historial")
            return
        
        historial = ProveedoresLogic.obtener_historial_compras(self.proveedor_seleccionado['id'])
        
        if not historial:
            messagebox.showinfo("Historial", "El proveedor no tiene compras registradas")
            return
        
        # Crear ventana de historial
        ventana_historial = tk.Toplevel(self.parent)
        ventana_historial.title(f"Historial de {self.proveedor_seleccionado['nombre']}")
        ventana_historial.geometry("600x400")
        
        # Treeview para historial
        columns = ("ID", "Fecha", "Total")
        tree_historial = ttk.Treeview(ventana_historial, columns=columns, show="headings")
        
        for col in columns:
            tree_historial.heading(col, text=col)
            tree_historial.column(col, width=150)
        
        for compra in historial:
            tree_historial.insert("", "end", values=(
                compra['id'],
                compra['fecha'],
                f"${compra['total']:.2f}"
            ))
        
        tree_historial.pack(fill="both", expand=True, padx=10, pady=10)

def crear_vista_proveedores(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    return ProveedoresView(parent, usuario_actual)