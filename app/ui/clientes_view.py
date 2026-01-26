import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.clientes_logic import ClientesLogic

class ClientesView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.cliente_seleccionado = None
        
        self.crear_widgets()
        self.cargar_clientes()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Clientes", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Información del Cliente", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Formulario
        self.crear_formulario_cliente(form_frame)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Clientes Registrados", padding=10)
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Treeview y búsqueda
        self.crear_lista_clientes(list_frame)
        
        # Configurar grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def crear_formulario_cliente(self, parent):
        # Nombre
        ttk.Label(parent, text="Nombre*:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_entry = ttk.Entry(parent, width=35)
        self.nombre_entry.grid(row=0, column=1, pady=5)
        
        # Documento
        ttk.Label(parent, text="Documento:").grid(row=1, column=0, sticky="w", pady=5)
        self.documento_entry = ttk.Entry(parent, width=35)
        self.documento_entry.grid(row=1, column=1, pady=5)
        
        # Teléfono
        ttk.Label(parent, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        self.telefono_entry = ttk.Entry(parent, width=35)
        self.telefono_entry.grid(row=2, column=1, pady=5)
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(parent, width=35)
        self.email_entry.grid(row=3, column=1, pady=5)
        
        # Dirección
        ttk.Label(parent, text="Dirección:").grid(row=4, column=0, sticky="w", pady=5)
        self.direccion_text = tk.Text(parent, width=35, height=3)
        self.direccion_text.grid(row=4, column=1, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Guardar Cliente", command=self.guardar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cliente).pack(side="left", padx=5)
    
    def crear_lista_clientes(self, parent):
        # Frame de búsqueda
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.buscar_entry = ttk.Entry(search_frame, width=30)
        self.buscar_entry.pack(side="left", padx=5)
        self.buscar_entry.bind("<KeyRelease>", self.on_buscar)
        
        # Treeview
        columns = ("ID", "Nombre", "Documento", "Teléfono", "Email")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("Documento", width=120)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Email", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_cliente_select)
        
        # Botón de historial
        ttk.Button(parent, text="Ver Historial de Compras", 
                  command=self.ver_historial).pack(pady=(10, 0))
    
    def cargar_clientes(self):
        """Carga los clientes en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        clientes = ClientesLogic.obtener_clientes()
        
        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente['id'],
                cliente['nombre'],
                cliente['documento'] or '',
                cliente['telefono'] or '',
                cliente['email'] or ''
            ))
    
    def guardar_cliente(self):
        """Guarda un nuevo cliente"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return
        
        resultado, mensaje = ClientesLogic.crear_cliente(
            nombre=nombre,
            documento=self.documento_entry.get().strip(),
            telefono=self.telefono_entry.get().strip(),
            email=self.email_entry.get().strip(),
            direccion=self.direccion_text.get("1.0", "end").strip()
        )
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_cliente(self):
        """Actualiza el cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return
        
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return
        
        datos = {
            'nombre': nombre,
            'documento': self.documento_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'direccion': self.direccion_text.get("1.0", "end").strip()
        }
        
        resultado, mensaje = ClientesLogic.actualizar_cliente(
            self.cliente_seleccionado['id'], datos
        )
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar al cliente '{self.cliente_seleccionado['nombre']}'?"):
            resultado, mensaje = ClientesLogic.eliminar_cliente(self.cliente_seleccionado['id'])
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", mensaje)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, "end")
        self.documento_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.direccion_text.delete("1.0", "end")
        self.cliente_seleccionado = None
    
    def on_cliente_select(self, event):
        """Maneja la selección de un cliente"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])
            
            self.documento_entry.delete(0, "end")
            self.documento_entry.insert(0, values[2])
            
            self.telefono_entry.delete(0, "end")
            self.telefono_entry.insert(0, values[3])
            
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, values[4])
            
            self.cliente_seleccionado = {
                'id': values[0],
                'nombre': values[1],
                'documento': values[2],
                'telefono': values[3],
                'email': values[4]
            }
    
    def on_buscar(self, event):
        """Busca clientes en tiempo real"""
        termino = self.buscar_entry.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if termino:
            clientes = ClientesLogic.buscar_cliente(termino)
        else:
            clientes = ClientesLogic.obtener_clientes()
        
        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente['id'],
                cliente['nombre'],
                cliente['documento'] or '',
                cliente['telefono'] or '',
                cliente['email'] or ''
            ))
    
    def ver_historial(self):
        """Muestra el historial de compras del cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para ver su historial")
            return
        
        historial = ClientesLogic.obtener_historial_compras(self.cliente_seleccionado['id'])
        
        if not historial:
            messagebox.showinfo("Historial", "El cliente no tiene compras registradas")
            return
        
        # Crear ventana de historial
        ventana_historial = tk.Toplevel(self.parent)
        ventana_historial.title(f"Historial de {self.cliente_seleccionado['nombre']}")
        ventana_historial.geometry("600x400")
        
        # Treeview para historial
        columns = ("ID", "Fecha", "Total", "Estado", "Método")
        tree_historial = ttk.Treeview(ventana_historial, columns=columns, show="headings")
        
        for col in columns:
            tree_historial.heading(col, text=col)
            tree_historial.column(col, width=100)
        
        for compra in historial:
            tree_historial.insert("", "end", values=(
                compra['id'],
                compra['fecha'],
                f"${compra['total']:.2f}",
                compra['estado'],
                compra['metodo_pago']
            ))
        
        tree_historial.pack(fill="both", expand=True, padx=10, pady=10)

def crear_vista_clientes(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    return ClientesView(parent, usuario_actual)