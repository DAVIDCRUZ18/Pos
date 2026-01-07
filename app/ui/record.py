import tkinter as tk
from tkinter import ttk, messagebox
import app.db.database as db

# ===== CÓDIGO MAESTRO PARA CREAR USUARIOS =====
CODIGO_MAESTRO = "14448"  # Cambia este código según necesites

def abrir_registro(root):
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrar Nuevo Usuario")
    ventana_registro.geometry("500x700")
    ventana_registro.configure(bg="white")
    ventana_registro.resizable(False, False)

    ventana_registro.transient(root)
    ventana_registro.grab_set()

    # ===== ESTILOS =====
    style = ttk.Style()
    
    style.configure(
        "Primary.TButton",
        font=("Arial", 12, "bold"),
        background="#3498db",
        foreground="white",
        borderwidth=0,
        relief="flat"
    )
    
    style.configure(
        "Secondary.TButton",
        font=("Arial", 12),
        background="#95a5a6",
        foreground="white",
        borderwidth=0,
        relief="flat"
    )
    
    style.configure(
        "Custom.TEntry",
        fieldbackground="white",
        borderwidth=1
    )

    # ===== TÍTULO =====
    tk.Label(
        ventana_registro,
        text="Registro de Nuevo Usuario",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#2c3e50"
    ).pack(pady=30)

    # ===== FRAME DE CAMPOS =====
    campos_frame = tk.Frame(ventana_registro, bg="white")
    campos_frame.pack(pady=10, padx=50, fill="both")

    # ===== Código de Autorización (MODIFICADO) =====
    tk.Label(campos_frame, text="Código de Autorización:",
            font=("Arial", 11, "bold"), bg="white", anchor="w", fg="#e74c3c"
    ).pack(fill="x", pady=(5,5))

    entry_codigo = ttk.Entry(
        campos_frame,
        width=40,
        style="Custom.TEntry",
        font=("Arial", 11),
        show="●"  # Ocultar el código
    )
    entry_codigo.pack(ipady=8, fill="x")

    # Nota informativa
    tk.Label(
        campos_frame,
        text="⚠ Requiere código de autorización del administrador",
        font=("Arial", 9, "italic"),
        bg="white",
        fg="#7f8c8d"
    ).pack(fill="x", pady=(2,0))

    # ===== Usuario =====
    tk.Label(campos_frame, text="Usuario:",
            font=("Arial", 11), bg="white", anchor="w"
    ).pack(fill="x", pady=(10,5))

    entry_new_user = ttk.Entry(campos_frame, width=40,
                            style="Custom.TEntry", font=("Arial", 11))
    entry_new_user.pack(ipady=8, fill="x")

    # ===== Nombre completo =====
    tk.Label(campos_frame, text="Nombre Completo:",
            font=("Arial", 11), bg="white", anchor="w"
    ).pack(fill="x", pady=(10,5))

    entry_nombre = ttk.Entry(campos_frame, width=40,
                            style="Custom.TEntry", font=("Arial", 11))
    entry_nombre.pack(ipady=8, fill="x")

    # ===== Contraseña =====
    tk.Label(campos_frame, text="Contraseña:",
            font=("Arial", 11), bg="white", anchor="w"
    ).pack(fill="x", pady=(10,5))

    entry_new_pass = ttk.Entry(
        campos_frame, width=40, show="●",
        style="Custom.TEntry", font=("Arial", 11)
    )
    entry_new_pass.pack(ipady=8, fill="x")

    # ===== Confirmar contraseña =====
    tk.Label(campos_frame, text="Confirmar Contraseña:",
            font=("Arial", 11), bg="white", anchor="w"
    ).pack(fill="x", pady=(10,5))

    entry_confirm_pass = ttk.Entry(
        campos_frame, width=40, show="●",
        style="Custom.TEntry", font=("Arial", 11)
    )
    entry_confirm_pass.pack(ipady=8, fill="x")

    # ===== Rol =====
    tk.Label(campos_frame, text="Rol:",
            font=("Arial", 11), bg="white", anchor="w"
    ).pack(fill="x", pady=(10,5))

    combo_rol = ttk.Combobox(
        campos_frame,
        values=["vendedor", "admin"],
        state="readonly",
        font=("Arial", 11)
    )
    combo_rol.current(0)
    combo_rol.pack(ipady=8, fill="x")

    # ===== Función Guardar (MODIFICADA) =====
    def guardar_usuario():
        codigo_ingresado = entry_codigo.get().strip()
        nuevo_user = entry_new_user.get().strip()
        nombre = entry_nombre.get().strip()
        nueva_pass = entry_new_pass.get()
        confirmar_pass = entry_confirm_pass.get()
        rol = combo_rol.get()

        # VALIDACIÓN 1: Verificar código de autorización
        if not codigo_ingresado:
            messagebox.showerror("Error", "Debe ingresar el código de autorización")
            entry_codigo.focus()
            return

        if codigo_ingresado != CODIGO_MAESTRO:
            messagebox.showerror(
                "Acceso Denegado",
                "Código de autorización incorrecto.\nSolo el administrador puede crear usuarios."
            )
            entry_codigo.delete(0, tk.END)
            entry_codigo.focus()
            return

        # VALIDACIÓN 2: Campos obligatorios
        if not nuevo_user or not nombre or not nueva_pass:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return

        # VALIDACIÓN 3: Contraseñas coinciden
        if nueva_pass != confirmar_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            entry_confirm_pass.delete(0, tk.END)
            return

        # VALIDACIÓN 4: Longitud de contraseña
        if len(nueva_pass) < 6:
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres")
            return

        # Registrar en DB (sin código, ya no se guarda)
        exito, mensaje = db.registrar_usuario(
            nuevo_user,
            nueva_pass,
            nombre,
            rol
        )

        if exito:
            messagebox.showinfo("Éxito", f"{mensaje}")
            ventana_registro.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    # ===== FRAME DE BOTONES =====
    btn_frame = tk.Frame(ventana_registro, bg="white")
    btn_frame.pack(pady=30, padx=50, fill="x")

    # Botón Registrar
    btn_registrar = tk.Button(
        btn_frame,
        text="REGISTRAR",
        font=("Arial", 12, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        cursor="hand2",
        border=0,
        command=guardar_usuario
    )
    btn_registrar.pack(fill="x", ipady=10)

    # Botón Cancelar
    btn_cancelar = tk.Button(
        btn_frame,
        text="CANCELAR",
        font=("Arial", 12),
        bg="#95a5a6",
        fg="white",
        activebackground="#7f8c8d",
        activeforeground="white",
        cursor="hand2",
        border=0,
        command=ventana_registro.destroy
    )
    btn_cancelar.pack(fill="x", pady=(10,0), ipady=10)