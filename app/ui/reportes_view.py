import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as scrolledtext
from datetime import datetime, timedelta
from app.logic.reportes_logic import ReportesLogic

class ReportesView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        
        self.crear_widgets()
        self.cargar_resumen_general()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(main_frame, text="Reportes del Sistema", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook para diferentes tipos de reportes
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Pestaña de Resumen General
        self.crear_pestana_resumen()
        
        # Pestaña de Reportes de Ventas
        self.crear_pestana_ventas()
        
        # Pestaña de Productos Más Vendidos
        self.crear_pestana_productos()
        
        # Pestaña de Clientes
        self.crear_pestana_clientes()
        
        # Pestaña de Inventario Valorizado
        self.crear_pestana_inventario()
    
    def crear_pestana_resumen(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Resumen General")
        
        # Frame de contenido
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón de actualización
        ttk.Button(content_frame, text="Actualizar Resumen", 
                  command=self.cargar_resumen_general).pack(pady=(0, 10))
        
        # Frame para mostrar el resumen
        self.resumen_frame = ttk.Frame(content_frame)
        self.resumen_frame.pack(fill="both", expand=True)
    
    def crear_pestana_ventas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Ventas")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Filtros
        filter_frame = ttk.LabelFrame(content_frame, text="Filtros", padding=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Fecha Inicio:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio_entry = ttk.Entry(filter_frame, width=15)
        self.fecha_inicio_entry.grid(row=0, column=1, padx=5, pady=5)
        self.fecha_inicio_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ttk.Label(filter_frame, text="Fecha Fin:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_fin_entry = ttk.Entry(filter_frame, width=15)
        self.fecha_fin_entry.grid(row=0, column=3, padx=5, pady=5)
        self.fecha_fin_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(filter_frame, text="Generar Reporte", 
                  command=self.generar_reporte_ventas).grid(row=0, column=4, padx=20, pady=5)
        
        # Treeview para ventas
        columns = ("ID", "Fecha", "Cliente", "Método", "Total")
        self.tree_ventas = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=120 if col == "Total" else 150)
        
        # Scrollbar
        scrollbar_ventas = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar_ventas.pack(side="right", fill="y")
        
        # Total de ventas
        self.total_ventas_label = ttk.Label(content_frame, text="Total Ventas: $0.00", 
                                          font=("Arial", 12, "bold"))
        self.total_ventas_label.pack(pady=(10, 0))
    
    def crear_pestana_productos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Productos Más Vendidos")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Controls
        control_frame = ttk.Frame(content_frame)
        control_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(control_frame, text="Top:").pack(side="left", padx=5)
        self.top_spin = ttk.Spinbox(control_frame, from_=5, to=50, width=10)
        self.top_spin.set(10)
        self.top_spin.pack(side="left", padx=5)
        
        ttk.Button(control_frame, text="Actualizar", 
                  command=self.actualizar_productos_vendidos).pack(side="left", padx=10)
        
        # Treeview
        columns = ("Producto", "Cantidad", "Total Recaudado")
        self.tree_productos = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
        
        self.tree_productos.heading("Producto", text="Producto")
        self.tree_productos.heading("Cantidad", text="Cantidad Vendida")
        self.tree_productos.heading("Total Recaudado", text="Total Recaudado")
        
        self.tree_productos.column("Producto", width=300)
        self.tree_productos.column("Cantidad", width=120)
        self.tree_productos.column("Total Recaudado", width=120)
        
        scrollbar_productos = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")
    
    def crear_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes Frecuentes")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(content_frame, text="Actualizar Lista", 
                  command=self.actualizar_clientes_frecuentes).pack(pady=(0, 10))
        
        # Treeview
        columns = ("Cliente", "Total Compras", "Total Gastado")
        self.tree_clientes = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
        
        self.tree_clientes.heading("Cliente", text="Cliente")
        self.tree_clientes.heading("Total Compras", text="Total Compras")
        self.tree_clientes.heading("Total Gastado", text="Total Gastado")
        
        self.tree_clientes.column("Cliente", width=300)
        self.tree_clientes.column("Total Compras", width=120)
        self.tree_clientes.column("Total Gastado", width=120)
        
        scrollbar_clientes = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar_clientes.set)
        
        self.tree_clientes.pack(side="left", fill="both", expand=True)
        scrollbar_clientes.pack(side="right", fill="y")
    
    def crear_pestana_inventario(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Inventario Valorizado")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(content_frame, text="Actualizar Inventario", 
                  command=self.actualizar_inventario_valorizado).pack(pady=(0, 10))
        
        # Treeview
        columns = ("Producto", "Stock", "Costo Unitario", "Valor Costo", "Valor Venta")
        self.tree_inventario = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
        
        self.tree_inventario.heading("Producto", text="Producto")
        self.tree_inventario.heading("Stock", text="Stock")
        self.tree_inventario.heading("Costo Unitario", text="Costo Unitario")
        self.tree_inventario.heading("Valor Costo", text="Valor Costo")
        self.tree_inventario.heading("Valor Venta", text="Valor Venta")
        
        self.tree_inventario.column("Producto", width=250)
        self.tree_inventario.column("Stock", width=80)
        self.tree_inventario.column("Costo Unitario", width=100)
        self.tree_inventario.column("Valor Costo", width=100)
        self.tree_inventario.column("Valor Venta", width=100)
        
        scrollbar_inventario = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree_inventario.yview)
        self.tree_inventario.configure(yscrollcommand=scrollbar_inventario.set)
        
        self.tree_inventario.pack(side="left", fill="both", expand=True)
        scrollbar_inventario.pack(side="right", fill="y")
        
        # Totales de inventario
        self.totales_inventario_frame = ttk.Frame(content_frame)
        self.totales_inventario_frame.pack(fill="x", pady=(10, 0))
    
    def cargar_resumen_general(self):
        """Carga el resumen general del negocio"""
        # Limpiar frame anterior
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        
        resumen = ReportesLogic.reporte_general_negocio()
        
        # Ventas del mes
        ventas_frame = ttk.LabelFrame(self.resumen_frame, text="Ventas del Mes", padding=10)
        ventas_frame.pack(fill="x", pady=5)
        
        ttk.Label(ventas_frame, text=f"Cantidad: {resumen['resumen_mes']['ventas']['total_ventas']}").pack(anchor="w")
        ttk.Label(ventas_frame, text=f"Monto: ${resumen['resumen_mes']['ventas']['monto_ventas']:.2f}").pack(anchor="w")
        
        # Compras del mes
        compras_frame = ttk.LabelFrame(self.resumen_frame, text="Compras del Mes", padding=10)
        compras_frame.pack(fill="x", pady=5)
        
        ttk.Label(compras_frame, text=f"Cantidad: {resumen['resumen_mes']['compras']['total_compras']}").pack(anchor="w")
        ttk.Label(compras_frame, text=f"Monto: ${resumen['resumen_mes']['compras']['monto_compras']:.2f}").pack(anchor="w")
        
        # Gastos del mes
        gastos_frame = ttk.LabelFrame(self.resumen_frame, text="Gastos del Mes", padding=10)
        gastos_frame.pack(fill="x", pady=5)
        
        ttk.Label(gastos_frame, text=f"Cantidad: {resumen['resumen_mes']['gastos']['total_gastos']}").pack(anchor="w")
        ttk.Label(gastos_frame, text=f"Monto: ${resumen['resumen_mes']['gastos']['monto_gastos']:.2f}").pack(anchor="w")
        
        # Utilidad
        utilidad_frame = ttk.LabelFrame(self.resumen_frame, text="Utilidad Operativa", padding=10)
        utilidad_frame.pack(fill="x", pady=5)
        
        utilidad = resumen['resumen_mes']['utilidad_operativa']
        color = "green" if utilidad >= 0 else "red"
        ttk.Label(utilidad_frame, text=f"${utilidad:.2f}", 
                 font=("Arial", 14, "bold"), foreground=color).pack()
        
        # Inventario
        inventario_frame = ttk.LabelFrame(self.resumen_frame, text="Estado Inventario", padding=10)
        inventario_frame.pack(fill="x", pady=5)
        
        ttk.Label(inventario_frame, text=f"Total Productos: {resumen['inventario']['total_productos']}").pack(anchor="w")
        
        if resumen['inventario']['stock_critico']:
            ttk.Label(inventario_frame, text="⚠️ Productos con stock bajo", foreground="orange").pack(anchor="w")
        else:
            ttk.Label(inventario_frame, text="✅ Stock OK", foreground="green").pack(anchor="w")
    
    def generar_reporte_ventas(self):
        """Genera reporte de ventas según fechas"""
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()
        
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Ingrese ambas fechas")
            return
        
        reporte = ReportesLogic.reporte_ventas_periodo(fecha_inicio, fecha_fin)
        
        # Limpiar treeview
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        # Cargar datos
        total = 0
        for venta in reporte:
            self.tree_ventas.insert("", "end", values=(
                venta['id'],
                venta['fecha'],
                venta['cliente_nombre'] or 'Consumidor Final',
                venta['metodo_pago'],
                f"${venta['total']:.2f}"
            ))
            total += venta['total']
        
        self.total_ventas_label.config(text=f"Total Ventas: ${total:.2f}")
    
    def actualizar_productos_vendidos(self):
        """Actualiza la lista de productos más vendidos"""
        try:
            limite = int(self.top_spin.get())
        except ValueError:
            limite = 10
        
        productos = ReportesLogic.reporte_productos_mas_vendidos(limite)
        
        # Limpiar treeview
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Cargar datos
        for producto in productos:
            self.tree_productos.insert("", "end", values=(
                producto['nombre'],
                producto['total_vendido'],
                f"${producto['total_recaudado']:.2f}"
            ))
    
    def actualizar_clientes_frecuentes(self):
        """Actualiza la lista de clientes frecuentes"""
        clientes = ReportesLogic.reporte_clientes_frecuentes()
        
        # Limpiar treeview
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Cargar datos
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=(
                cliente['nombre'],
                cliente['total_compras'],
                f"${cliente['total_gastado']:.2f}"
            ))
    
    def actualizar_inventario_valorizado(self):
        """Actualiza el inventario valorizado"""
        reporte = ReportesLogic.reporte_inventario_valorizado()
        
        # Limpiar treeview
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        
        # Cargar datos
        for producto in reporte['productos']:
            self.tree_inventario.insert("", "end", values=(
                producto['nombre'],
                producto['stock'],
                f"${producto['costo']:.2f}",
                f"${producto['valor_costo']:.2f}",
                f"${producto['valor_venta']:.2f}"
            ))
        
        # Mostrar totales
        for widget in self.totales_inventario_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.totales_inventario_frame, 
                 text=f"Valor Costo Total: ${reporte['totales']['valor_costo_total']:.2f}").pack(side="left", padx=10)
        ttk.Label(self.totales_inventario_frame, 
                 text=f"Valor Venta Total: ${reporte['totales']['valor_venta_total']:.2f}").pack(side="left", padx=10)
        ttk.Label(self.totales_inventario_frame, 
                 text=f"Utilidad Potencial: ${reporte['totales']['utilidad_potencial']:.2f}", 
                 font=("Arial", 10, "bold")).pack(side="left", padx=10)

def crear_vista_reportes(parent, usuario_actual):
    return ReportesView(parent, usuario_actual)