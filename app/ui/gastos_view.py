import tkinter as tk
from tkinter import ttk, messagebox
from app.logic.gastos_logic import GastosLogic

class GastosView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.gasto_seleccionado = None
        
        self.crear_widgets()
        self.cargar_gastos()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Gastos", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Gasto", padding=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Formulario
        self.crear_formulario_gasto(form_frame)
        
        # Frame de lista
        list_frame = ttk.LabelFrame(main_frame, text="Gastos Registrados", padding=10)
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Treeview y controles
        self.crear_lista_gastos(list_frame)
        
        # Configurar grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def crear_formulario_gasto(self, parent):
        # Descripción
        ttk.Label(parent, text="Descripción*:").grid(row=0, column=0, sticky="w", pady=5)
        self.descripcion_entry = ttk.Entry(parent, width=35)
        self.descripcion_entry.grid(row=0, column=1, pady=5)
        
        # Monto
        ttk.Label(parent, text="Monto*:").grid(row=1, column=0, sticky="w", pady=5)
        self.monto_entry = ttk.Entry(parent, width=35)
        self.monto_entry.grid(row=1, column=1, pady=5)
        
        # Categoría
        ttk.Label(parent, text="Categoría:").grid(row=2, column=0, sticky="w", pady=5)
        self.categoria_combo = ttk.Combobox(parent, width=33, values=[
            "Servicios", "Suministros", "Mantenimiento", "Alquiler",
            "Impuestos", "Marketing", "Otros"
        ])
        self.categoria_combo.grid(row=2, column=1, pady=5)
        self.categoria_combo.set("Otros")
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Guardar Gasto", command=self.guardar_gasto).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_gasto).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_gasto).pack(side="left", padx=5)
        
        # Frame de estadísticas
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas del Mes", padding=10)
        stats_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.stats_label = ttk.Label(stats_frame, text="Cargando...", font=("Arial", 10))
        self.stats_label.pack()
        
        # Botón actualizar estadísticas
        ttk.Button(stats_frame, text="Actualizar Estadísticas", 
                  command=self.actualizar_estadisticas).pack(pady=5)
    
    def crear_lista_gastos(self, parent):
        # Frame de filtros
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Mes:").pack(side="left", padx=5)
        self.mes_combo = ttk.Combobox(filter_frame, width=15, state="readonly")
        self.mes_combo.pack(side="left", padx=5)
        
        ttk.Label(filter_frame, text="Año:").pack(side="left", padx=5)
        self.anio_combo = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.anio_combo.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Filtrar", command=self.filtrar_gastos).pack(side="left", padx=10)
        ttk.Button(filter_frame, text="Mostrar Todos", command=self.cargar_gastos).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Fecha", "Descripción", "Categoría", "Monto", "Usuario")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Usuario", text="Usuario")
        
        self.tree.column("ID", width=50)
        self.tree.column("Fecha", width=120)
        self.tree.column("Descripción", width=200)
        self.tree.column("Categoría", width=100)
        self.tree.column("Monto", width=80)
        self.tree.column("Usuario", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_gasto_select)
        
        # Configurar meses y años
        self.cargar_meses_anios()
        
        # Frame de resumen
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill="x", pady=(10, 0))
        
        self.total_label = ttk.Label(summary_frame, text="Total: $0.00", 
                                   font=("Arial", 12, "bold"))
        self.total_label.pack(side="right")
    
    def cargar_meses_anios(self):
        """Carga los meses y años en los combobox"""
        import datetime
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        año_actual = datetime.datetime.now().year
        años = list(range(año_actual - 5, año_actual + 1))
        
        self.mes_combo['values'] = meses
        self.anio_combo['values'] = años
        
        # Mes y año actual
        mes_actual = meses[datetime.datetime.now().month - 1]
        self.mes_combo.set(mes_actual)
        self.anio_combo.set(str(año_actual))
    
    def cargar_gastos(self):
        """Carga los gastos en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        gastos = GastosLogic.obtener_gastos()
        total = 0
        
        for gasto in gastos:
            self.tree.insert("", "end", values=(
                gasto['id'],
                gasto['fecha'],
                gasto['descripcion'][:50] + "..." if len(gasto['descripcion']) > 50 else gasto['descripcion'],
                gasto['categoria'] or 'Sin categoría',
                f"${gasto['monto']:.2f}",
                gasto['usuario_nombre'] or 'Sistema'
            ))
            total += gasto['monto']
        
        self.total_label.config(text=f"Total: ${total:.2f}")
        self.actualizar_estadisticas()
    
    def guardar_gasto(self):
        """Guarda un nuevo gasto"""
        descripcion = self.descripcion_entry.get().strip()
        monto_str = self.monto_entry.get().strip()
        categoria = self.categoria_combo.get()
        
        if not descripcion:
            messagebox.showerror("Error", "La descripción del gasto es obligatoria")
            return
        
        if not monto_str:
            messagebox.showerror("Error", "El monto del gasto es obligatorio")
            return
        
        try:
            monto = float(monto_str)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a cero")
                return
            
            GastosLogic.crear_gasto(
                descripcion=descripcion,
                monto=monto,
                categoria=categoria,
                usuario_id=self.usuario_actual['id']
            )
            
            messagebox.showinfo("Éxito", "Gasto registrado exitosamente")
            self.limpiar_formulario()
            self.cargar_gastos()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
    
    def actualizar_gasto(self):
        """Actualiza el gasto seleccionado"""
        if not self.gasto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para actualizar")
            return
        
        descripcion = self.descripcion_entry.get().strip()
        monto_str = self.monto_entry.get().strip()
        categoria = self.categoria_combo.get()
        
        if not descripcion:
            messagebox.showerror("Error", "La descripción del gasto es obligatoria")
            return
        
        if not monto_str:
            messagebox.showerror("Error", "El monto del gasto es obligatorio")
            return
        
        try:
            monto = float(monto_str)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a cero")
                return
            
            datos = {
                'descripcion': descripcion,
                'monto': monto,
                'categoria': categoria
            }
            
            GastosLogic.actualizar_gasto(self.gasto_seleccionado['id'], datos)
            
            messagebox.showinfo("Éxito", "Gasto actualizado exitosamente")
            self.limpiar_formulario()
            self.cargar_gastos()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
    
    def eliminar_gasto(self):
        """Elimina el gasto seleccionado"""
        if not self.gasto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"¿Está seguro de eliminar el gasto '{self.gasto_seleccionado['descripcion']}'?"):
            GastosLogic.eliminar_gasto(self.gasto_seleccionado['id'])
            messagebox.showinfo("Éxito", "Gasto eliminado exitosamente")
            self.limpiar_formulario()
            self.cargar_gastos()
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.descripcion_entry.delete(0, "end")
        self.monto_entry.delete(0, "end")
        self.categoria_combo.set("Otros")
        self.gasto_seleccionado = None
    
    def on_gasto_select(self, event):
        """Maneja la selección de un gasto"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            values = item['values']
            
            self.descripcion_entry.delete(0, "end")
            self.descripcion_entry.insert(0, values[2])
            
            self.monto_entry.delete(0, "end")
            self.monto_entry.insert(0, str(values[4]).replace("$", ""))
            
            self.categoria_combo.set(values[3] or 'Otros')
            
            self.gasto_seleccionado = {
                'id': values[0],
                'descripcion': values[2],
                'categoria': values[3],
                'monto': float(str(values[4]).replace("$", ""))
            }
    
    def filtrar_gastos(self):
        """Filtra gastos por mes y año"""
        mes = self.mes_combo.get()
        año = self.anio_combo.get()
        
        if not mes or not año:
            messagebox.showwarning("Advertencia", "Seleccione mes y año para filtrar")
            return
        
        # Convertir mes a número
        meses = {
            "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
            "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
            "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
        }
        
        mes_num = meses[mes]
        
        # Obtener gastos del período
        fecha_inicio = f"{año}-{mes_num}-01"
        fecha_fin = f"{año}-{mes_num}-31"
        
        gastos = GastosLogic.obtener_gastos_por_fecha(fecha_inicio, fecha_fin) if hasattr(GastosLogic, 'obtener_gastos_por_fecha') else GastosLogic.obtener_gastos()
        
        # Limpiar y cargar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total = 0
        for gasto in gastos:
            self.tree.insert("", "end", values=(
                gasto['id'],
                gasto['fecha'],
                gasto['descripcion'][:50] + "..." if len(gasto['descripcion']) > 50 else gasto['descripcion'],
                gasto['categoria'] or 'Sin categoría',
                f"${gasto['monto']:.2f}",
                gasto['usuario_nombre'] or 'Sistema'
            ))
            total += gasto['monto']
        
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas de gastos"""
        stats = GastosLogic.obtener_estadisticas_gastos()
        
        texto = f"Total del mes: ${stats['total_mes']:.2f} | "
        texto += f"Cantidad: {stats['cantidad_mes']} | "
        texto += f"Categorías: {len(stats['por_categoria'])}"
        
        self.stats_label.config(text=texto)

def crear_vista_gastos(parent, usuario_actual):
    """Función para mantener compatibilidad con el código existente"""
    return GastosView(parent, usuario_actual)