import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.usuarios_logic import UsuariosLogic

class UsuariosView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.usuario_seleccionado = None
        
        self.crear_widgets()
        self.cargar_usuarios()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(main_frame, text="Gestión de Usuarios", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Información del Usuario", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        self.crear_formulario_usuario(form_frame)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Usuarios Registrados", padding=10)
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        self.crear_lista_usuarios(list_frame)
        
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def crear_formulario_usuario(self, parent):
        # Usuario
        ttk.Label(parent, text="Usuario*:").grid(row=0, column=0, sticky="w", pady=5)
        self.usuario_entry = ttk.Entry(parent, width=35)
        self.usuario_entry.grid(row=0, column=1, pady=5)
        
        # Nombre completo
        ttk.Label(parent, text="Nombre Completo*:").grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_entry = ttk.Entry(parent, width=35)
        self.nombre_entry.grid(row=1, column=1, pady=5)
        
        # Contraseña
        ttk.Label(parent, text="Contraseña*:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(parent, width=35, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        # Rol
        ttk.Label(parent, text="Rol*:").grid(row=3, column=0, sticky="w", pady=5)
        self.rol_combo = ttk.Combobox(parent, width=33, values=["admin", "vendedor"], state="readonly")
        self.rol_combo.grid(row=3, column=1, pady=5)
        self.rol_combo.set("vendedor")
        
        # Estado
        self.estado_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="Usuario Activo", variable=self.estado_var).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Guardar Usuario", command=self.guardar_usuario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_usuario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cambiar Contraseña", command=self.cambiar_password).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Activar/Desactivar", command=self.toggle_estado).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=5)
    
    def crear_lista_usuarios(self, parent):
        # Treeview
        columns = ("ID", "Usuario", "Nombre", "Rol", "Estado", "Último Acceso")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Nombre", text="Nombre Completo")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Último Acceso", text="Último Acceso")
        
        self.tree.column("ID", width=50)
        self.tree.column("Usuario", width=120)
        self.tree.column("Nombre", width=180)
        self.tree.column("Rol", width=80)
        self.tree.column("Estado", width=80)
        self.tree.column("Último Acceso", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_usuario_select)
    
    def cargar_usuarios(self):
        """Carga los usuarios en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = UsuariosLogic.obtener_usuarios()
        
        for usuario in usuarios:
            estado_text = "Activo" if usuario['activo'] == 1 else "Inactivo"
            self.tree.insert("", "end", values=(
                usuario['id'],
                usuario['usuario'],
                usuario['nombre_completo'],
                usuario['rol'],
                estado_text,
                usuario['ultimo_acceso'] or 'Nunca'
            ))
    
    def guardar_usuario(self):
        """Guarda un nuevo usuario"""
        usuario = self.usuario_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        password = self.password_entry.get().strip()
        rol = self.rol_combo.get()
        
        if not all([usuario, nombre, password, rol]):
            messagebox.showerror("Error", "Todos los campos marcados con * son obligatorios")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        resultado, mensaje = UsuariosLogic.crear_usuario(usuario, password, rol, nombre)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_usuario(self):
        """Actualiza el usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para actualizar")
            return
        
        nombre = self.nombre_entry.get().strip()
        rol = self.rol_combo.get()
        password = self.password_entry.get().strip()
        
        if not nombre or not rol:
            messagebox.showerror("Error", "Nombre y rol son obligatorios")
            return
        
        datos = {
            'nombre_completo': nombre,
            'rol': rol
        }
        
        if password:  # Solo actualizar contraseña si se ingresó una nueva
            if len(password) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                return
            datos['password'] = password
        
        resultado, mensaje = UsuariosLogic.actualizar_usuario(self.usuario_seleccionado['id'], datos)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return
        
        # No permitir eliminar al usuario actual
        if self.usuario_seleccionado['id'] == self.usuario_actual['id']:
            messagebox.showerror("Error", "No puede eliminar su propio usuario")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar al usuario '{self.usuario_seleccionado['nombre_completo']}'?"):
            resultado, mensaje = UsuariosLogic.eliminar_usuario(self.usuario_seleccionado['id'])
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
    
    def toggle_estado(self):
        """Activa o desactiva el usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para cambiar estado")
            return
        
        # No permitir desactivar al usuario actual
        if self.usuario_seleccionado['id'] == self.usuario_actual['id']:
            messagebox.showerror("Error", "No puede desactivar su propio usuario")
            return
        
        nuevo_estado = not (self.usuario_seleccionado['activo'] == 1)
        accion = "activar" if nuevo_estado else "desactivar"
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de {accion} al usuario '{self.usuario_seleccionado['nombre_completo']}'?"):
            resultado, mensaje = UsuariosLogic.activar_desactivar_usuario(
                self.usuario_seleccionado['id'], nuevo_estado
            )
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
    
    def cambiar_password(self):
        """Abre ventana para cambiar contraseña del usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para cambiar contraseña")
            return
        
        ventana_password = tk.Toplevel(self.parent)
        ventana_password.title(f"Cambiar Contraseña - {self.usuario_seleccionado['nombre_completo']}")
        ventana_password.geometry("400x250")
        ventana_password.transient(self.parent)
        ventana_password.grab_set()
        
        # Contraseña actual
        ttk.Label(ventana_password, text="Contraseña Actual:").pack(pady=10)
        password_actual_entry = ttk.Entry(ventana_password, show="*", width=30)
        password_actual_entry.pack(pady=5)
        
        # Nueva contraseña
        ttk.Label(ventana_password, text="Nueva Contraseña:").pack(pady=10)
        password_nueva_entry = ttk.Entry(ventana_password, show="*", width=30)
        password_nueva_entry.pack(pady=5)
        
        # Confirmar contraseña
        ttk.Label(ventana_password, text="Confirmar Contraseña:").pack(pady=10)
        password_confirm_entry = ttk.Entry(ventana_password, show="*", width=30)
        password_confirm_entry.pack(pady=5)
        
        def ejecutar_cambio():
            actual = password_actual_entry.get().strip()
            nueva = password_nueva_entry.get().strip()
            confirm = password_confirm_entry.get().strip()
            
            if not all([actual, nueva, confirm]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if nueva != confirm:
                messagebox.showerror("Error", "Las contraseñas nuevas no coinciden")
                return
            
            if len(nueva) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                return
            
            resultado, mensaje = UsuariosLogic.cambiar_password(
                self.usuario_seleccionado['id'], actual, nueva
            )
            
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                ventana_password.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        ttk.Button(ventana_password, text="Cambiar Contraseña", 
                   command=ejecutar_cambio).pack(pady=20)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.usuario_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.rol_combo.set("vendedor")
        self.estado_var.set(True)
        self.usuario_seleccionado = None
    
    def on_usuario_select(self, event):
        """Maneja la selección de un usuario"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            self.usuario_entry.delete(0, "end")
            self.usuario_entry.insert(0, values[1])
            
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[2])
            
            self.rol_combo.set(values[3])
            self.estado_var.set(values[4] == "Activo")
            
            self.usuario_seleccionado = {
                'id': values[0],
                'usuario': values[1],
                'nombre_completo': values[2],
                'rol': values[3],
                'activo': 1 if values[4] == "Activo" else 0
            }

def crear_vista_usuarios(parent, usuario_actual):
    return UsuariosView(parent, usuario_actual)