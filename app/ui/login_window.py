import tkinter as tk
from tkinter import ttk, messagebox
import app.db.database as db
from app.ui.record import abrir_registro
from app.ui.punto_venta import abrir_sistema_principal
from app.config.settings import APP_NAME , version

# Variable global para almacenar la sesión del usuario
usuario_actual = None

def login_window():
    root = tk.Tk()
    root.title(f"{APP_NAME} - Versión {version}")
    root.geometry("1100x700")
    root.resizable(False, False)
    root.configure(bg="#f5f5f5")
    
    # Inicializar base de datos
    db.inicializar_bd()
    
    # ===== ESTILOS PERSONALIZADOS =====
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("Custom.TEntry",
                fieldbackground="white",
                borderwidth=2,
                relief="flat")
    
    style.configure("Primary.TButton",
                background="#4a90e2",
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                padding=(20, 10),
                font=("Arial", 11, "bold"))
    
    style.map("Primary.TButton",
            background=[("active", "#357abd"), ("pressed", "#2868a8")])
    
    style.configure("Secondary.TButton",
                background="#6c757d",
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                padding=(20, 10),
                font=("Arial", 11))
    
    style.map("Secondary.TButton",
            background=[("active", "#5a6268"), ("pressed", "#495057")])
    
    # ===== FUNCIONES DE LOGIN =====
    def realizar_login():
        usuario = user_entry.get()
        password = pass_entry.get()
        
        # Validar campos vacíos
        if not usuario or usuario == "Ingresa tu usuario":
            messagebox.showwarning("Advertencia", "Por favor ingresa tu usuario")
            user_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("Advertencia", "Por favor ingresa tu contraseña")
            pass_entry.focus()
            return
        
        # Validar credenciales
        exito, resultado = db.validar_login(usuario, password)
        
        if exito:
            global usuario_actual
            usuario_actual = resultado
            messagebox.showinfo("Éxito", f"¡Bienvenido(a) {resultado['nombre_completo']}!")
            root.withdraw()  # Ocultar ventana de login
            abrir_sistema_principal(resultado)
        else:
            messagebox.showerror("Error de Login", resultado)
            pass_entry.delete(0, tk.END)
            pass_entry.focus()
    
    # ===== CONTENEDOR PRINCIPAL =====
    main_container = tk.Frame(root, bg="#f5f5f5")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ===== LADO IZQUIERDO =====
    left = tk.Frame(main_container, bg="white", width=550, height=660)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))
    left.pack_propagate(False)
    
    left_content = tk.Frame(left, bg="white")
    left_content.place(relx=0.5, rely=0.5, anchor="center")
    
    logo_frame = tk.Frame(left_content, bg="#4a90e2", width=80, height=80)
    logo_frame.pack(pady=(0, 20))
    logo_frame.pack_propagate(False)
    
    tk.Label(logo_frame, text="💳", font=("Arial", 40), bg="#4a90e2", fg="white").place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(left_content, text="SISTEMA DE", font=("Arial", 32, "bold"), bg="white", fg="#2c3e50").pack()
    tk.Label(left_content, text="PUNTO DE VENTA", font=("Arial", 32, "bold"), bg="white", fg="#4a90e2").pack(pady=(0, 30))
    
    features = [
        "✓ Gestión de inventario en tiempo real",
        "✓ Control de ventas y reportes",
        "✓ Interfaz intuitiva y moderna",
        "✓ Soporte técnico 24/7"
    ]
    
    for feature in features:
        tk.Label(left_content, text=feature, font=("Arial", 12), bg="white", fg="#555", anchor="w").pack(pady=5, padx=20, fill="x")
    
    contact_frame = tk.Frame(left, bg="white")
    contact_frame.pack(side="bottom", pady=30)
    
    tk.Label(contact_frame, text="📍 Bogotá D.C., Colombia", font=("Arial", 10), bg="white", fg="#777").pack()
    tk.Label(contact_frame, text="📞 +57 315 211 56 19", font=("Arial", 10), bg="white", fg="#777").pack(pady=5)
    tk.Label(contact_frame, text="© 2024 David Cruz DCOMUNICACIONES", font=("Arial", 9), bg="white", fg="#aaa").pack(pady=(10, 0))
    
    # ===== LADO DERECHO =====
    right = tk.Frame(main_container, bg="white", width=490, height=660)
    right.pack(side="right", fill="both", expand=True, padx=(10, 0))
    right.pack_propagate(False)
    
    login_content = tk.Frame(right, bg="white")
    login_content.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(login_content, text="Iniciar Sesión", font=("Arial", 28, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 10))
    tk.Label(login_content, text="Ingresa tus credenciales para continuar", font=("Arial", 10), bg="white", fg="#777").pack(pady=(0, 30))
    
    # Campo Usuario
    user_frame = tk.Frame(login_content, bg="white")
    user_frame.pack(pady=10, fill="x", padx=40)
    
    tk.Label(user_frame, text="👤 Usuario", font=("Arial", 11, "bold"), bg="white", fg="#555", anchor="w").pack(anchor="w", pady=(0, 5))
    
    user_entry = ttk.Entry(user_frame, width=35, style="Custom.TEntry", font=("Arial", 11))
    user_entry.pack(ipady=8, fill="x")
    user_entry.insert(0, "Ingresa tu usuario")
    user_entry.config(foreground="#999")
    
    def on_user_focus_in(event):
        if user_entry.get() == "Ingresa tu usuario":
            user_entry.delete(0, tk.END)
            user_entry.config(foreground="black")
    
    def on_user_focus_out(event):
        if user_entry.get() == "":
            user_entry.insert(0, "Ingresa tu usuario")
            user_entry.config(foreground="#999")
    
    user_entry.bind("<FocusIn>", on_user_focus_in)
    user_entry.bind("<FocusOut>", on_user_focus_out)
    
    # Campo Contraseña
    pass_frame = tk.Frame(login_content, bg="white")
    pass_frame.pack(pady=10, fill="x", padx=40)
    
    tk.Label(pass_frame, text="🔒 Contraseña", font=("Arial", 11, "bold"), bg="white", fg="#555", anchor="w").pack(anchor="w", pady=(0, 5))
    
    pass_entry = ttk.Entry(pass_frame, width=35, show="●", style="Custom.TEntry", font=("Arial", 11))
    pass_entry.pack(ipady=8, fill="x")
    pass_entry.bind("<Return>", lambda e: realizar_login())
    
    # Recordar sesión
    remember_frame = tk.Frame(login_content, bg="white")
    remember_frame.pack(pady=15, fill="x", padx=40)
    
    remember_var = tk.BooleanVar()
    tk.Checkbutton(remember_frame, text="Recordar mi sesión", variable=remember_var, bg="white", fg="#555", 
                    font=("Arial", 9), activebackground="white", selectcolor="white").pack(side="left")
    
    # Botones
    buttons_frame = tk.Frame(login_content, bg="white")
    buttons_frame.pack(pady=20, fill="x", padx=40)
    
    login_btn = ttk.Button(buttons_frame, text="INICIAR SESIÓN", style="Primary.TButton", 
                        cursor="hand2", command=realizar_login)
    login_btn.pack(fill="x", ipady=5)
    
    register_btn = ttk.Button(
        buttons_frame,
        text="CREAR CUENTA",
        style="Secondary.TButton",
        cursor="hand2",
        command=lambda: abrir_registro(root)
    )

    register_btn.pack(fill="x", pady=(10, 0), ipady=5)
    
    # Info de credenciales por defecto
    info_frame = tk.Frame(login_content, bg="#fff3cd", relief="flat", borderwidth=1)
    info_frame.pack(pady=20, fill="x", padx=40)
    
    tk.Label(info_frame, text="ℹ️ Credenciales por defecto:", font=("Arial", 9, "bold"), bg="#fff3cd", fg="#856404").pack(pady=(10,5))
    tk.Label(info_frame, text="Usuario: admin | Contraseña: admin123", font=("Arial", 9), bg="#fff3cd", fg="#856404").pack(pady=(0,10))
    
    # Version info
    tk.Label(login_content, text=f"Versión {version}" , font=("Arial", 9), bg="white", fg="#2e7d32").pack(pady=(10,0))
    
    root.mainloop()

if __name__ == "__main__":
    login_window()