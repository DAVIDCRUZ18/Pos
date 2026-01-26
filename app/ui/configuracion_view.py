import tkinter as tk
from tkinter import ttk, messagebox
from app.config.settings import APP_NAME, version
import platform
import sys

class ConfiguracionView:
    def __init__(self, parent, usuario_actual):
        self.parent = parent
        self.usuario_actual = usuario_actual
        
        self.crear_widgets()
        self.cargar_info_sistema()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Configuración e Información del Sistema", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 30))
        
        # Notebook para diferentes secciones
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Pestaña de Información del Sistema
        self.crear_pestana_informacion()
        
        # Pestaña de Configuración
        self.crear_pestana_configuracion()
        
        # Pestaña de Ayuda
        self.crear_pestana_ayuda()
        
        # Pestaña de Acerca de
        self.crear_pestana_acerca_de()
    
    def crear_pestana_informacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Información del Sistema")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información del sistema
        info_frame = ttk.LabelFrame(content_frame, text="Información del Sistema", padding=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        self.info_labels = {}
        info_items = [
            ("sistema", "Sistema:"),
            ("version", "Versión:"),
            ("python", "Python:"),
            ("plataforma", "Plataforma:"),
            ("arquitectura", "Arquitectura:"),
            ("usuario_actual", "Usuario Actual:"),
            ("rol_usuario", "Rol:"),
            ("ultimo_acceso", "Último Acceso:")
        ]
        
        for i, (key, label) in enumerate(info_items):
            ttk.Label(info_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=3)
            self.info_labels[key] = ttk.Label(info_frame, text="", font=("Arial", 10))
            self.info_labels[key].grid(row=i, column=1, sticky="w", padx=(20, 0), pady=3)
        
        # Estadísticas del sistema
        stats_frame = ttk.LabelFrame(content_frame, text="Estadísticas del Sistema", padding=15)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.stats_labels = {}
        stat_items = [
            ("total_usuarios", "Total Usuarios:"),
            ("total_clientes", "Total Clientes:"),
            ("total_proveedores", "Total Proveedores:"),
            ("total_productos", "Total Productos:"),
            ("total_categorias", "Total Categorías:"),
            ("total_ventas", "Total Ventas:"),
            ("total_compras", "Total Compras:"),
            ("total_gastos", "Total Gastos:")
        ]
        
        for i, (key, label) in enumerate(stat_items):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(stats_frame, text=label, font=("Arial", 10, "bold")).grid(row=row, column=col, sticky="w", pady=3, padx=(0, 10))
            self.stats_labels[key] = ttk.Label(stats_frame, text="0", font=("Arial", 10))
            self.stats_labels[key].grid(row=row, column=col+1, sticky="w", pady=3)
        
        # Botón de refresco
        ttk.Button(content_frame, text="Actualizar Información", 
                  command=self.cargar_info_sistema).pack(pady=10)
    
    def crear_pestana_configuracion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuración")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Preferencias de usuario
        pref_frame = ttk.LabelFrame(content_frame, text="Preferencias de Usuario", padding=15)
        pref_frame.pack(fill="x", pady=(0, 20))
        
        # Tema
        ttk.Label(pref_frame, text="Tema de Interfaz:").grid(row=0, column=0, sticky="w", pady=5)
        self.tema_combo = ttk.Combobox(pref_frame, values=["Claro", "Oscuro", "Sistema"], state="readonly", width=20)
        self.tema_combo.set("Claro")
        self.tema_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Idioma
        ttk.Label(pref_frame, text="Idioma:").grid(row=1, column=0, sticky="w", pady=5)
        self.idioma_combo = ttk.Combobox(pref_frame, values=["Español", "Inglés"], state="readonly", width=20)
        self.idioma_combo.set("Español")
        self.idioma_combo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Formato de fecha
        ttk.Label(pref_frame, text="Formato de Fecha:").grid(row=2, column=0, sticky="w", pady=5)
        self.fecha_combo = ttk.Combobox(pref_frame, values=["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"], state="readonly", width=20)
        self.fecha_combo.set("DD/MM/YYYY")
        self.fecha_combo.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Configuración de copias de seguridad
        backup_frame = ttk.LabelFrame(content_frame, text="Copia de Seguridad", padding=15)
        backup_frame.pack(fill="x", pady=(0, 20))
        
        self.auto_backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(backup_frame, text="Copia de seguridad automática", 
                        variable=self.auto_backup_var).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(backup_frame, text="Frecuencia:").grid(row=1, column=0, sticky="w", pady=5)
        self.backup_frecuencia_combo = ttk.Combobox(backup_frame, 
                                                   values=["Diaria", "Semanal", "Mensual"], 
                                                   state="readonly", width=15)
        self.backup_frecuencia_combo.set("Diaria")
        self.backup_frecuencia_combo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Botones de acción
        action_frame = ttk.Frame(content_frame)
        action_frame.pack(fill="x", pady=20)
        
        ttk.Button(action_frame, text="Guardar Configuración", 
                  command=self.guardar_configuracion).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Crear Copia de Seguridad Ahora", 
                  command=self.crear_backup).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Restaurar Copia de Seguridad", 
                  command=self.restaurar_backup).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Restablecer Configuración", 
                  command=self.restablecer_configuracion).pack(side="left", padx=5)
    
    def crear_pestana_ayuda(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Ayuda")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Secciones de ayuda
        help_text = """
SISTEMA DE PUNTO DE VENTA - GUÍA DE USO

1. VENTAS
   • Desde el módulo de Ventas puede registrar las ventas diarias
   • Agregue productos mediante el código de barras o búsqueda
   • Seleccione cliente (opcional) y método de pago
   • Puede imprimir ticket o recibo

2. INVENTARIO
   • Gestione productos, categorías y existencias
   • Registre nuevos productos con precio y stock inicial
   • Realice ajustes de stock cuando sea necesario
   • Monitoree productos con stock bajo

3. CLIENTES Y PROVEEDORES
   • Mantenga actualizada la base de datos de clientes
   • Registre proveedores para las compras
   • Consulte historial de transacciones

4. COMPRAS Y GASTOS
   • Registre compras para actualizar inventario
   • Controle los gastos operativos del negocio
   • Categorice gastos para mejor control

5. REPORTES
   • Genere reportes de ventas por período
   • Consulte productos más vendidos
   • Analice clientes frecuentes
   • Obtenga inventario valorizado

6. USUARIOS
   • Cree usuarios para el sistema
   • Asigne roles y permisos
   • Cambie contraseñas regularmente

CONTACTO DE SOPORTE
• Email: soporte@sistemapos.com
• Teléfono: (123) 456-7890
• Horario: Lunes a Viernes 8:00-18:00
        """
        
        # Text widget con scrollbar
        text_widget = tk.Text(content_frame, wrap="word", height=25, width=80)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert("1.0", help_text)
        text_widget.configure(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_pestana_acerca_de(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Acerca de")
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo o título grande
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(pady=30)
        
        ttk.Label(title_frame, text=APP_NAME, 
                 font=("Arial", 24, "bold")).pack()
        ttk.Label(title_frame, text=f"Versión {version}", 
                 font=("Arial", 14)).pack()
        
        # Información del programa
        info_frame = ttk.LabelFrame(content_frame, text="Información del Programa", padding=20)
        info_frame.pack(fill="x", pady=20)
        
        info_text = f"""
{APP_NAME} es un sistema completo de punto de venta diseñado para 
pequeñas y medianas empresas.

Características Principales:
• Gestión completa de ventas e inventario
• Control de clientes y proveedores  
• Sistema de compras y gastos
• Reportes detallados y estadísticas
• Gestión de usuarios con roles
• Interfaz intuitiva y fácil de usar

Tecnología:
• Python {sys.version.split()[0]}
• Tkinter para interfaz gráfica
• SQLite para base de datos

Derechos de Autor:
© 2024 {APP_NAME}. Todos los derechos reservados.

Licencia: Software Propietario

Desarrollado por:
Empresa de Desarrollo de Software
contacto@empresa.com
www.empresa.com
        """
        
        info_label = ttk.Label(info_frame, text=info_text.strip(), justify="left")
        info_label.pack()
        
        # Botones
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Ver Licencia", 
                  command=self.ver_licencia).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Ver Registro de Cambios", 
                  command=self.ver_cambios).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Ver Créditos", 
                  command=self.ver_creditos).pack(side="left", padx=5)
    
    def cargar_info_sistema(self):
        """Carga la información del sistema"""
        # Información básica
        self.info_labels["sistema"].config(text=APP_NAME)
        self.info_labels["version"].config(text=version)
        self.info_labels["python"].config(text=f"Python {sys.version.split()[0]}")
        self.info_labels["plataforma"].config(text=platform.system())
        self.info_labels["arquitectura"].config(text=platform.machine())
        self.info_labels["usuario_actual"].config(text=self.usuario_actual['nombre_completo'])
        self.info_labels["rol_usuario"].config(text=self.usuario_actual['rol'])
        self.info_labels["ultimo_acceso"].config(text=self.usuario_actual.get('ultimo_acceso', 'N/A'))
        
        # Cargar estadísticas (simulado por ahora)
        try:
            from app.db.database import get_db
            with get_db() as conn:
                cursor = conn.cursor()
                
                # Contar registros en cada tabla
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                self.stats_labels["total_usuarios"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM clientes")
                self.stats_labels["total_clientes"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM proveedores")
                self.stats_labels["total_proveedores"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM productos")
                self.stats_labels["total_productos"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM categorias")
                self.stats_labels["total_categorias"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM ventas")
                self.stats_labels["total_ventas"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM compras")
                self.stats_labels["total_compras"].config(text=str(cursor.fetchone()[0]))
                
                cursor.execute("SELECT COUNT(*) FROM gastos")
                self.stats_labels["total_gastos"].config(text=str(cursor.fetchone()[0]))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las estadísticas: {str(e)}")
    
    def guardar_configuracion(self):
        """Guarda la configuración del usuario"""
        # Aquí se implementaría el guardado real de configuraciones
        messagebox.showinfo("Configuración", "Configuración guardada exitosamente")
    
    def crear_backup(self):
        """Crea una copia de seguridad"""
        messagebox.showinfo("Copia de Seguridad", "Función de copia de seguridad en desarrollo")
    
    def restaurar_backup(self):
        """Restaura una copia de seguridad"""
        messagebox.showinfo("Copia de Seguridad", "Función de restauración en desarrollo")
    
    def restablecer_configuracion(self):
        """Restablece la configuración a valores por defecto"""
        if messagebox.askyesno("Restablecer", 
                             "¿Está seguro de restablecer la configuración a valores por defecto?"):
            self.tema_combo.set("Claro")
            self.idioma_combo.set("Español")
            self.fecha_combo.set("DD/MM/YYYY")
            self.auto_backup_var.set(True)
            self.backup_frecuencia_combo.set("Diaria")
            messagebox.showinfo("Configuración", "Configuración restablecida")
    
    def ver_licencia(self):
        """Muestra la ventana de licencia"""
        ventana_licencia = tk.Toplevel(self.parent)
        ventana_licencia.title("Licencia de Software")
        ventana_licencia.geometry("600x400")
        ventana_licencia.transient(self.parent)
        
        text_widget = tk.Text(ventana_licencia, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        
        licencia_text = """
LICENCIA DE SOFTWARE

Este es un software propietario protegido por leyes de derechos de autor 
y tratados internacionales.

TERMINOS DE USO:
1. Se requiere una licencia válida para usar este software
2. No se permite la distribución no autorizada
3. No se permite la ingeniería inversa
4. La licencia es por instalación/usuario

LIMITACIÓN DE RESPONSABILIDAD:
El software se proporciona "tal cual" sin garantías de ningún tipo.
El desarrollador no será responsable por daños indirectos o consecuentes.

SOPORTE TÉCNICO:
El soporte técnico está incluido durante el primer año.
Para renovar contacte al departamento de ventas.
        """
        
        text_widget.insert("1.0", licencia_text)
        text_widget.configure(state="disabled")
        
        ttk.Button(ventana_licencia, text="Cerrar", 
                   command=ventana_licencia.destroy).pack(pady=10)
    
    def ver_cambios(self):
        """Muestra el registro de cambios"""
        messagebox.showinfo("Registro de Cambios", "Función en desarrollo")
    
    def ver_creditos(self):
        """Muestra los créditos del programa"""
        ventana_creditos = tk.Toplevel(self.parent)
        ventana_creditos.title("Créditos")
        ventana_creditos.geometry("500x300")
        ventana_creditos.transient(self.parent)
        
        creditos_text = """
CRÉDITOS DEL PROGRAMA

Desarrollo Principal:
• Equipo de Desarrollo
• Arquitectura de Software
• Diseño de Base de Datos

Diseño de Interfaz:
• Diseñador UX/UI
• Experiencia de Usuario

Pruebas y Calidad:
• Equipo de QA
• Testing Automatizado

Agradecimientos especiales a:
• Clientes beta testers
• Comunidad de feedback
• Equipo de documentación

Versión: {version}
Fecha de Compilación: 2024
        """.format(version=version)
        
        label = ttk.Label(ventana_creditos, text=creditos_text.strip(), justify="center")
        label.pack(expand=True, padx=20, pady=20)
        
        ttk.Button(ventana_creditos, text="Cerrar", 
                   command=ventana_creditos.destroy).pack(pady=10)

def crear_vista_configuracion(parent, usuario_actual):
    return ConfiguracionView(parent, usuario_actual)