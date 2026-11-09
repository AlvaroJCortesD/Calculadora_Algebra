import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np


def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Graficador de Funciones")
    win.geometry("400x250")
    win.grab_set()

    tk.Label(win, text="Función f(x) (ej. np.sin(x) + x**2):").pack(pady=5)
    ent_func = tk.Entry(win, width=30)
    ent_func.insert(0, "x**3 - x - 2")
    ent_func.pack(pady=5)

    frame_limites = tk.Frame(win)
    frame_limites.pack(pady=10)

    tk.Label(frame_limites, text="x min:").grid(row=0, column=0)
    ent_xmin = tk.Entry(frame_limites, width=5)
    ent_xmin.insert(0, "-10")
    ent_xmin.grid(row=0, column=1, padx=5)

    tk.Label(frame_limites, text="x max:").grid(row=0, column=2)
    ent_xmax = tk.Entry(frame_limites, width=5)
    ent_xmax.insert(0, "10")
    ent_xmax.grid(row=0, column=3, padx=5)

    def graficar():
        func_str = ent_func.get()
        try:
            xmin = float(ent_xmin.get())
            xmax = float(ent_xmax.get())

            x = np.linspace(xmin, xmax, 400)
            # Evaluar de forma segura usando numpy
            entorno = {"x": x, "np": np}
            y = eval(func_str, {"__builtins__": {}}, entorno)

            plt.figure("Gráfica de Función")
            plt.plot(x, y, label=f"f(x) = {func_str}", color='blue')
            plt.axhline(0, color='black', linewidth=1)
            plt.axvline(0, color='black', linewidth=1)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            plt.title("Graficador 2D")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error al Graficar", f"Expresión inválida.\nDetalle: {e}")

    ttk.Button(win, text="Generar Gráfica", command=graficar).pack(pady=20)