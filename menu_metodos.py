import tkinter as tk
from tkinter import ttk, messagebox

try:
    from modulos import modulo_biseccion
except ImportError:
    modulo_biseccion = None

try:
    from modulos import modulo_graficador
except ImportError:
    modulo_graficador = None

try:
    from modulos import modulo_notacion
except ImportError:
    modulo_notacion = None

try:
    from modulos import modulo_errores
except ImportError:
    modulo_errores = None


def construir_ventana(ventana, root_menu):
    ventana.title("Módulo de Métodos Numéricos")
    ventana.geometry("450x450")

    # Manejo de error por si el comando de centrado no es compatible con el gestor de ventanas
    try:
        ventana.eval('tk::PlaceWindow . center')
    except Exception:
        pass

    lbl_titulo = tk.Label(ventana, text="MÉTODOS NUMÉRICOS", font=("Arial", 14, "bold"))
    lbl_titulo.pack(pady=20)

    def lanzar_biseccion():
        if modulo_biseccion:
            modulo_biseccion.abrir_gui(ventana)
        else:
            messagebox.showerror("Error", "No se encontró el archivo modulos/modulo_biseccion.py")

    def lanzar_graficador():
        if modulo_graficador:
            modulo_graficador.abrir_gui(ventana)
        else:
            messagebox.showerror("Error", "No se encontró el archivo modulos/modulo_graficador.py")

    def lanzar_notacion():
        if modulo_notacion:
            modulo_notacion.abrir_gui(ventana)
        else:
            messagebox.showerror("Error", "No se encontró el archivo modulos/modulo_notacion.py")

    def lanzar_errores():
        if modulo_errores:
            modulo_errores.abrir_gui(ventana)
        else:
            messagebox.showerror("Error", "No se encontró el archivo modulos/modulo_errores.py")

    def volver():
        ventana.destroy()
        root_menu.deiconify()

    ttk.Button(ventana, text="1. Método de Bisección", width=40, command=lanzar_biseccion).pack(pady=10, ipady=5)
    ttk.Button(ventana, text="2. Graficador de funciones", width=40, command=lanzar_graficador).pack(pady=10, ipady=5)
    ttk.Button(ventana, text="3. Notación Posicional (Base 10 y 2)", width=40, command=lanzar_notacion).pack(pady=10,
                                                                                                             ipady=5)
    ttk.Button(ventana, text="4. Errores Numéricos y Punto Flotante", width=40, command=lanzar_errores).pack(pady=10,
                                                                                                             ipady=5)

    tk.Label(ventana, text="").pack(pady=5)
    ttk.Button(ventana, text="Volver al Menú Principal", width=40, command=volver).pack(pady=10, ipady=5)