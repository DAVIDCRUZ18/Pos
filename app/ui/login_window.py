import tkinter as tk
from tkinter import ttk
from six.moves import tkinter as tk

def login_window():
    root = tk.Tk()
    root.title("Punto de Venta Versión 3.1.3")
    root.geometry("1100x600")
    root.resizable(False, False)

    # ===== CONTENEDORES =====
    left = tk.Frame(root, bg="#e6e6e6", width=550, height=600)
    left.pack(side="left", fill="both")

    right = tk.Frame(root, bg="#cfe3ec", width=550, height=600)
    right.pack(side="right", fill="both")

    # ===== LADO IZQUIERDO =====
    tk.Label(
        left,
        text="TkPOS",
        font=("Arial", 40, "bold"),
        bg="#e6e6e6",
        fg="#6c97b5"
    ).pack(pady=40)

    tk.Label(
        left,
        text="Sistema Punto de Venta\nBogotá D.C. Colombia\n+57 322 987 6543",
        font=("Arial", 12),
        bg="#e6e6e6"
    ).pack(pady=10)

    tk.Label(
        left,
        text="Software creado por Kevin Arboleda\nCopyright © InnovaSoft Code 2024",
        font=("Arial", 10),
        bg="#e6e6e6"
    ).pack(side="bottom", pady=30)

    # ===== LADO DERECHO =====
    tk.Label(
        right,
        text="Inicio de sesión",
        font=("Arial", 28, "bold"),
        bg="#cfe3ec"
    ).pack(pady=40)

    # Usuario
    tk.Label(right, text="Nombre de usuario", bg="#cfe3ec", font=("Arial", 12)).pack()
    user_entry = ttk.Entry(right, width=30)
    user_entry.pack(pady=5)

    # Password
    tk.Label(right, text="Contraseña", bg="#cfe3ec", font=("Arial", 12)).pack(pady=(15,0))
    pass_entry = ttk.Entry(right, width=30, show="*")
    pass_entry.pack(pady=5)

    # Botones
    ttk.Button(right, text=" Iniciar ").pack(pady=15)
    ttk.Button(right, text=" Registrar ").pack()

    # Info versión
    tk.Label(
        right,
        text="Versión gratuita 3.1.3",
        bg="#cfe3ec",
        fg="green",
        font=("Arial", 10, "bold")
    ).pack(pady=20)

    tk.Label(
        right,
        text="Nueva versión de pago disponible aquí!\nRealiza tu donación aquí!",
        bg="#cfe3ec",
        font=("Arial", 10)
    ).pack()
    

    class UI(tk.Frame):
        """Docstring."""

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Aqui colocariamos los widgets."""
        self.parent.title("Un titulo para la ventana")

        etiqueta = tk.Label(self.parent, text="Ejemplo simple de Label")
        etiqueta.pack()

    if __name__ == "__main__":
        ROOT = tk.Tk()
        ROOT.geometry("300x100")
        APP = UI(parent=ROOT)
        APP.mainloop()
        ROOT.destroy()


    root.mainloop()
