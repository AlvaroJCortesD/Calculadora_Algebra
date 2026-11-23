import tkinter as tk
from tkinter import ttk
from main import CalculadoraGUI
import menu_metodos


def abrir_algebra(root_menu):
    # Oculta el menú principal temporalmente
    root_menu.withdraw()

    # Crea una nueva ventana para la Calculadora de Álgebra
    ventana_algebra = tk.Toplevel(root_menu)

    # Al cerrar la calculadora, vuelve a mostrar el menú principal
    ventana_algebra.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_algebra, root_menu))

    # Instancia tu clase original pasándole la nueva ventana
    app = CalculadoraGUI(ventana_algebra)


def abrir_metodos(root_menu):
    root_menu.withdraw()
    ventana_metodos = tk.Toplevel(root_menu)
    ventana_metodos.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_metodos, root_menu))

    # Llama a la función que construye el submenú de métodos
    menu_metodos.construir_ventana(ventana_metodos, root_menu)


def cerrar_ventana(ventana_actual, root_menu):
    ventana_actual.destroy()
    root_menu.deiconify()  # Restaura el menú principal


def iniciar_app():
    root = tk.Tk()
    root.title("Programa 7 - Menú Principal")
    root.geometry("450x350")
    root.eval('tk::PlaceWindow . center')

    # Diseño del menú principal
    lbl_titulo = tk.Label(root, text="SISTEMA MATEMÁTICO INTEGRAL", font=("Arial", 14, "bold"))
    lbl_titulo.pack(pady=30)

    btn_algebra = ttk.Button(root, text="1. Calculadora de Álgebra Lineal", width=40,
                             command=lambda: abrir_algebra(root))
    btn_algebra.pack(pady=15, ipady=5)

    btn_metodos = ttk.Button(root, text="2. Módulo de Métodos Numéricos", width=40,
                             command=lambda: abrir_metodos(root))
    btn_metodos.pack(pady=15, ipady=5)

    btn_salir = ttk.Button(root, text="3. Salir del Sistema", width=40,
                           command=root.destroy)
    btn_salir.pack(pady=15, ipady=5)

    root.mainloop()


if __name__ == "__main__":
    iniciar_app()