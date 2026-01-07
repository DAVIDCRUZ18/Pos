from app.ui.login_window import login_window
from app.services.updater import hay_actualizacion, actualizar_desde_git
from tkinter import messagebox
import tkinter as tk


def main():

    # Iniciar contexto Tk solo para los mensajes
    root = tk.Tk()
    root.withdraw()

    # ====== Verificar actualización antes de abrir login ======
    if hay_actualizacion():

        resp = messagebox.askyesno(
            "Actualización disponible",
            "Hay una nueva versión del sistema.\n¿Deseas actualizar ahora?"
        )

        if resp:
            resultado = actualizar_desde_git()

            messagebox.showinfo("Actualización", resultado)

            messagebox.showinfo(
                "Reinicio requerido",
                "El sistema se actualizó.\nPor favor vuelve a abrir la aplicación."
            )

            return  # <-- importante: no continuar

    root.destroy()

    # ====== Si no hay actualización → abrir login ======
    login_window()


if __name__ == "__main__":
    main()