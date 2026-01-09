import tkinter as tk
from tkinter import ttk
from datetime import datetime
import app.db.database as db
from app.config.settings import APP_NAME, version

def abrir_sistema_principal(datos_usuario):
    ventana_principal = tk.Toplevel()
    ventana_principal.title(f"{APP_NAME} - Versión {version}")
    ventana_principal.geometry("1400x800")
    ventana_principal.configure(bg="#f0f4f8")
    ventana_principal.resizable(True, True)
    ventana_principal.minsize(1200, 700)
    
    # Variable para mantener la vista actual
    vista_actual = tk.StringVar(value="inicio")
    
    # ================= HEADER CON GRADIENTE ==================
    header = tk.Frame(ventana_principal, bg="#1e3a8a", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)
    
    # Frame para el contenido del header
    header_content = tk.Frame(header, bg="#1e3a8a")
    header_content.pack(fill="both", expand=True)
    
    # Título con icono
    titulo_frame = tk.Frame(header_content, bg="#1e3a8a")
    titulo_frame.pack(side="left", padx=30, pady=20)
    
    tk.Label(
        titulo_frame,
        text="🏪",
        font=("Segoe UI Emoji", 32),
        bg="#1e3a8a",
        fg="white"
    ).pack(side="left", padx=(0, 15))
    
    tk.Label(
        titulo_frame,
        text="SISTEMA PUNTO DE VENTA",
        font=("Segoe UI", 24, "bold"),
        bg="#1e3a8a",
        fg="white"
    ).pack(side="left")
    
    # Información de usuario y hora
    user_info_frame = tk.Frame(header_content, bg="#1e3a8a")
    user_info_frame.pack(side="right", padx=30)
    
    tk.Label(
        user_info_frame,
        text=f"👤 {datos_usuario['usuario']}",
        font=("Segoe UI", 11),
        bg="#1e3a8a",
        fg="#93c5fd"
    ).pack(anchor="e")
    
    tk.Label(
        user_info_frame,
        text=f"🔑 {datos_usuario['rol'].capitalize()}",
        font=("Segoe UI", 10),
        bg="#1e3a8a",
        fg="#bfdbfe"
    ).pack(anchor="e", pady=(5, 0))
    
    # Botón salir moderno
    btn_salir = tk.Button(
        header_content,
        text="✕",
        font=("Arial", 16, "bold"),
        bg="#dc2626",
        fg="white",
        relief="flat",
        width=3,
        height=1,
        cursor="hand2",
        activebackground="#b91c1c",
        activeforeground="white",
        command=ventana_principal.destroy
    )
    btn_salir.pack(side="right", padx=15)
    
    # Efecto hover para botón salir
    def on_enter_salir(e):
        btn_salir.config(bg="#b91c1c")
    def on_leave_salir(e):
        btn_salir.config(bg="#dc2626")
    
    btn_salir.bind("<Enter>", on_enter_salir)
    btn_salir.bind("<Leave>", on_leave_salir)
    
    # ================= CONTENEDOR PRINCIPAL ==================
    main_container = tk.Frame(ventana_principal, bg="#f0f4f8")
    main_container.pack(fill="both", expand=True)
    
    # ================= VARIABLES BASE ==================
    vista_actual = tk.StringVar(value="inicio")

    # ================= SIDEBAR IZQUIERDO ==================
    sidebar_container = tk.Frame(main_container, bg="#ffffff", width=280)
    sidebar_container.pack(side="left", fill="y", padx=(15, 5), pady=15)
    sidebar_container.pack_propagate(False)

    # Canvas scrollable
    sidebar_canvas = tk.Canvas(
        sidebar_container,
        bg="#ffffff",
        highlightthickness=0
    )
    sidebar_canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar
    sidebar_scrollbar = tk.Scrollbar(
        sidebar_container,
        orient="vertical",
        command=sidebar_canvas.yview
    )
    sidebar_scrollbar.pack(side="right", fill="y")

    sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

    # Frame interior del menú
    sidebar = tk.Frame(sidebar_canvas, bg="#ffffff")

    canvas_window = sidebar_canvas.create_window(
        (0, 0),
        window=sidebar,
        anchor="nw"
    )


    # ========= Ajustar scroll al tamaño del contenido =========
    def actualizar_scroll(event=None):
        sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))

    sidebar.bind("<Configure>", actualizar_scroll)


    # ========= Forzar mismo ancho del canvas =========
    def fijar_ancho_canvas(event):
        sidebar_canvas.itemconfig(
            canvas_window,
            width=sidebar_container.winfo_width()
        )

    sidebar_canvas.bind("<Configure>", fijar_ancho_canvas)


    # ========= ACTIVAR SCROLL CON LA RUEDA DEL MOUSE =========
    def scroll_con_rueda(event):
        sidebar_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    # Windows / Linux
    sidebar_canvas.bind_all("<MouseWheel>", scroll_con_rueda)

    # MacOS
    sidebar_canvas.bind_all("<Button-4>", lambda e: sidebar_canvas.yview_scroll(-1, "units"))
    sidebar_canvas.bind_all("<Button-5>", lambda e: sidebar_canvas.yview_scroll(1, "units"))


    # ================= TÍTULO ==================
    tk.Label(
        sidebar,
        text="MENÚ PRINCIPAL",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff",
        fg="#1f2937",
        pady=15
    ).pack(fill="x")

    tk.Frame(sidebar, bg="#e5e7eb", height=1).pack(fill="x", padx=10)


    # ================= FRAME DE BOTONES ==================
    menu_buttons_frame = tk.Frame(sidebar, bg="#ffffff")
    menu_buttons_frame.pack(fill="both", expand=True, pady=10)


    # ================= MÓDULOS ==================
    modulos = [
        {"nombre": "Inicio", "icono": "🏠", "vista": "inicio", "color": "#3b82f6"},
        {"nombre": "Ventas", "icono": "💵", "vista": "ventas", "color": "#10b981"},
        {"nombre": "Inventario", "icono": "📦", "vista": "inventario", "color": "#8b5cf6"},
        {"nombre": "Clientes", "icono": "👥", "vista": "clientes", "color": "#f59e0b"},
        {"nombre": "Proveedores", "icono": "📑", "vista": "proveedores", "color": "#06b6d4"},
        {"nombre": "Compras", "icono": "🧾", "vista": "compras", "color": "#ec4899"},
        {"nombre": "Reportes", "icono": "📊", "vista": "reportes", "color": "#14b8a6"},
        {"nombre": "Gastos", "icono": "💰", "vista": "gastos", "color": "#ef4444"},
        {"nombre": "Usuarios", "icono": "🧑‍💻", "vista": "usuarios", "color": "#6366f1"},
        {"nombre": "Configuración", "icono": "⚙️", "vista": "config", "color": "#64748b"},
    ]


    # ================= CONTENIDO PRINCIPAL ==================
    content_frame = tk.Frame(main_container, bg="#ffffff", bd=0)
    content_frame.pack(side="left", fill="both", expand=True, padx=(5, 15), pady=15)


    # ================= FUNCIÓN CAMBIO DE VISTA ==================
    def mostrar_vista(vista_nombre):

        # Limpiar contenido
        for widget in content_frame.winfo_children():
            widget.destroy()

        vista_actual.set(vista_nombre)

        # Header
        vista_header = tk.Frame(content_frame, bg="#f8fafc", height=80)
        vista_header.pack(fill="x", padx=20, pady=(20, 10))
        vista_header.pack_propagate(False)

        modulo_info = next((m for m in modulos if m["vista"] == vista_nombre), None)

        if modulo_info:
            tk.Label(
                vista_header,
                text=f"{modulo_info['icono']}  {modulo_info['nombre'].upper()}",
                font=("Segoe UI", 22, "bold"),
                bg="#f8fafc",
                fg="#1f2937"
            ).pack(side="left", pady=20, padx=10)

        vista_content = tk.Frame(content_frame, bg="#ffffff")
        vista_content.pack(fill="both", expand=True, padx=20, pady=10)

        # Llamado de vistas
        if vista_nombre == "inicio":
            crear_vista_inicio(vista_content, datos_usuario)
        elif vista_nombre == "ventas":
            crear_vista_ventas(vista_content)
        elif vista_nombre == "inventario":
            crear_vista_inventario(vista_content)
        elif vista_nombre == "clientes":
            crear_vista_clientes(vista_content)
        elif vista_nombre == "proveedores":
            crear_vista_proveedores(vista_content)
        elif vista_nombre == "compras":
            crear_vista_compras(vista_content)
        elif vista_nombre == "reportes":
            crear_vista_reportes(vista_content)
        elif vista_nombre == "gastos":
            crear_vista_gastos(vista_content)
        elif vista_nombre == "usuarios":
            crear_vista_usuarios(vista_content)
        elif vista_nombre == "config":
            crear_vista_configuracion(vista_content)

        actualizar_botones_activos()


    # ================= CREACIÓN DE BOTONES ==================
    botones_menu = {}

    for modulo in modulos:

        btn_frame = tk.Frame(menu_buttons_frame, bg="#ffffff")
        btn_frame.pack(fill="x", padx=15, pady=5)

        btn = tk.Button(
            btn_frame,
            text=f"{modulo['icono']}  {modulo['nombre']}",
            font=("Segoe UI", 11),
            bg="#f3f4f6",
            fg="#374151",
            relief="flat",
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
            activebackground="#e5e7eb",
            command=lambda v=modulo['vista']: mostrar_vista(v)
        )
        btn.pack(fill="x")

        botones_menu[modulo['vista']] = btn

        # Hover
        def on_enter(e, button=btn, vista=modulo["vista"]):
            if vista_actual.get() != vista:
                button.config(bg="#e5e7eb")

        def on_leave(e, button=btn, vista=modulo["vista"]):
            if vista_actual.get() != vista:
                button.config(bg="#f3f4f6")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)


    # ================= BOTÓN ACTIVO ==================
    def actualizar_botones_activos():
        for vista_key, boton in botones_menu.items():
            if vista_key == vista_actual.get():
                modulo = next((m for m in modulos if m["vista"] == vista_key), None)
                boton.config(
                    bg=modulo["color"],
                    fg="white",
                    font=("Segoe UI", 11, "bold")
                )
            else:
                boton.config(
                    bg="#f3f4f6",
                    fg="#374151",
                    font=("Segoe UI", 11)
                )


    # ================= CARGAR VISTA INICIAL ==================
    mostrar_vista("inicio")

    
    # Modificar mostrar_vista para actualizar botones
    original_mostrar_vista = mostrar_vista
    def mostrar_vista_con_actualizacion(vista_nombre):
        original_mostrar_vista(vista_nombre)
        actualizar_botones_activos()
    mostrar_vista = mostrar_vista_con_actualizacion
    
    # ================= FOOTER ==================
    footer = tk.Frame(ventana_principal, bg="#1f2937", height=40)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)
    
    footer_left = tk.Frame(footer, bg="#1f2937")
    footer_left.pack(side="left", padx=20)
    
    tk.Label(
        footer_left,
        text=f"© 2024 David Cruz DCOMUNICACIONES",
        bg="#1f2937",
        fg="#9ca3af",
        font=("Segoe UI", 9)
    ).pack(side="left", pady=10)
    
    footer_right = tk.Frame(footer, bg="#1f2937")
    footer_right.pack(side="right", padx=20)
    
    tk.Label(
        footer_right,
        text=f"Versión {version}",
        bg="#1f2937",
        fg="#9ca3af",
        font=("Segoe UI", 9)
    ).pack(side="right", pady=10)
    
    tk.Label(
        footer_right,
        text="Bogotá D.C - Colombia  |  ",
        bg="#1f2937",
        fg="#9ca3af",
        font=("Segoe UI", 9)
    ).pack(side="right", pady=10)
    
    # Mostrar vista inicial
    mostrar_vista("inicio")
    actualizar_botones_activos()

# ================= FUNCIONES PARA CREAR VISTAS ==================

def crear_vista_inicio(parent, datos_usuario):
    # Banner de bienvenida
    banner = tk.Frame(parent, bg="#dbeafe", bd=0)
    banner.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        banner,
        text=f"¡Bienvenido/a, {datos_usuario['usuario']}!",
        font=("Segoe UI", 18, "bold"),
        bg="#dbeafe",
        fg="#1e40af"
    ).pack(pady=20)
    
    tk.Label(
        banner,
        text=f"Hora actual: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}",
        font=("Segoe UI", 11),
        bg="#dbeafe",
        fg="#1e40af"
    ).pack(pady=(0, 20))
    
    # Tarjetas de estadísticas
    stats_frame = tk.Frame(parent, bg="#ffffff")
    stats_frame.pack(fill="both", expand=True, pady=10)
    
    stats = [
        {"titulo": "Ventas del Día", "valor": "$1,250,000", "icono": "💰", "color": "#10b981"},
        {"titulo": "Productos", "valor": "248", "icono": "📦", "color": "#3b82f6"},
        {"titulo": "Clientes", "valor": "86", "icono": "👥", "color": "#f59e0b"},
        {"titulo": "Pendientes", "valor": "12", "icono": "⏰", "color": "#ef4444"}
    ]
    
    for i, stat in enumerate(stats):
        card = tk.Frame(stats_frame, bg="#f9fafb", bd=0, relief="solid", highlightbackground="#e5e7eb", highlightthickness=1)
        card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        stats_frame.columnconfigure(i, weight=1)
        
        tk.Label(
            card,
            text=stat['icono'],
            font=("Segoe UI Emoji", 32),
            bg="#f9fafb"
        ).pack(pady=(20, 10))
        
        tk.Label(
            card,
            text=stat['titulo'],
            font=("Segoe UI", 11),
            bg="#f9fafb",
            fg="#6b7280"
        ).pack()
        
        tk.Label(
            card,
            text=stat['valor'],
            font=("Segoe UI", 20, "bold"),
            bg="#f9fafb",
            fg=stat['color']
        ).pack(pady=(5, 20))
    
    # Información de contacto
    info_frame = tk.Frame(parent, bg="#f9fafb", bd=0)
    info_frame.pack(fill="x", pady=20)
    
    tk.Label(
        info_frame,
        text="📍 Bogotá D.C - Colombia  |  📞 +3152115619",
        font=("Segoe UI", 11),
        bg="#f9fafb",
        fg="#6b7280"
    ).pack(pady=15)

def crear_vista_ventas(parent):
    crear_vista_generica(parent, "Ventas", "💵", 
        "Módulo de registro y gestión de ventas.\nAquí puedes crear nuevas ventas, consultar historial y generar facturas.")

def crear_vista_inventario(parent):
    crear_vista_generica(parent, "Inventario", "📦",
        "Control de stock y productos.\nRegistra entradas, salidas y mantén actualizado tu inventario.")

def crear_vista_clientes(parent):
    crear_vista_generica(parent, "Clientes", "👥",
        "Gestión de base de datos de clientes.\nRegistra, consulta y administra información de tus clientes.")

def crear_vista_proveedores(parent):
    crear_vista_generica(parent, "Proveedores", "📑",
        "Administración de proveedores.\nMantén el registro de tus proveedores y sus datos de contacto.")

def crear_vista_compras(parent):
    crear_vista_generica(parent, "Compras", "🧾",
        "Registro de compras a proveedores.\nLleva el control de tus adquisiciones y pagos.")

def crear_vista_reportes(parent):
    crear_vista_generica(parent, "Reportes", "📊",
        "Análisis y reportes del negocio.\nGenera reportes de ventas, inventario y estadísticas.")

def crear_vista_gastos(parent):
    crear_vista_generica(parent, "Gastos", "💰",
        "Control de gastos operativos.\nRegistra y categoriza los gastos del negocio.")

def crear_vista_usuarios(parent):
    crear_vista_generica(parent, "Usuarios", "🧑‍💻",
        "Gestión de usuarios del sistema.\nAdministra permisos y accesos de los usuarios.")

def crear_vista_configuracion(parent):
    crear_vista_generica(parent, "Configuración", "⚙️",
        "Configuración del sistema.\nPersonaliza parámetros y ajustes generales del sistema.")

def crear_vista_generica(parent, titulo, icono, descripcion):
    container = tk.Frame(parent, bg="#ffffff")
    container.pack(fill="both", expand=True, pady=20)
    
    # Icono grande
    tk.Label(
        container,
        text=icono,
        font=("Segoe UI Emoji", 64),
        bg="#ffffff"
    ).pack(pady=(40, 20))
    
    # Descripción
    tk.Label(
        container,
        text=descripcion,
        font=("Segoe UI", 12),
        bg="#ffffff",
        fg="#6b7280",
        justify="center"
    ).pack(pady=20)
    
    # Botón de ejemplo
    btn = tk.Button(
        container,
        text=f"Abrir {titulo}",
        font=("Segoe UI", 11, "bold"),
        bg="#3b82f6",
        fg="white",
        relief="flat",
        padx=30,
        pady=12,
        cursor="hand2",
        activebackground="#2563eb"
    )
    btn.pack(pady=20)

# ================= PRUEBA DEL SISTEMA ==================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # Datos de prueba
    datos_prueba = {
        "usuario": "David Cruz",
        "rol": "administrador"
    }
    
    abrir_sistema_principal(datos_prueba)
    root.mainloop()