import tkinter as tk
from tkinter import ttk, messagebox
import math


def evaluar_funcion(expr, x):
    funciones_permitidas = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    funciones_permitidas['x'] = x
    return eval(expr, {"__builtins__": {}}, funciones_permitidas)


def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Método de Bisección")
    win.geometry("700x500")
    win.grab_set()

    frame_inputs = tk.Frame(win)
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Función f(x):").grid(row=0, column=0, padx=5, pady=5)
    ent_func = tk.Entry(frame_inputs, width=20)
    ent_func.insert(0, "x**3 - x - 2")
    ent_func.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Intervalo a:").grid(row=0, column=2, padx=5, pady=5)
    ent_a = tk.Entry(frame_inputs, width=5)
    ent_a.insert(0, "1")
    ent_a.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_inputs, text="Intervalo b:").grid(row=0, column=4, padx=5, pady=5)
    ent_b = tk.Entry(frame_inputs, width=5)
    ent_b.insert(0, "2")
    ent_b.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(frame_inputs, text="Tolerancia:").grid(row=0, column=6, padx=5, pady=5)
    ent_tol = tk.Entry(frame_inputs, width=8)
    ent_tol.insert(0, "0.001")
    ent_tol.grid(row=0, column=7, padx=5, pady=5)

    txt_salida = tk.Text(win, height=20, font=("Consolas", 10), state=tk.DISABLED)
    txt_salida.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def calcular():
        txt_salida.config(state=tk.NORMAL)
        txt_salida.delete(1.0, tk.END)

        func = ent_func.get()
        try:
            a = float(ent_a.get())
            b = float(ent_b.get())
            tol = float(ent_tol.get())

            fa = evaluar_funcion(func, a)
            fb = evaluar_funcion(func, b)

            if fa * fb >= 0:
                messagebox.showerror("Error", "f(a) y f(b) deben tener signos opuestos.")
                return

            encabezado = f"{'Iter':<5} | {'a':<8} | {'b':<8} | {'c':<8} | {'f(c)':<10} | {'Error':<8}\n"
            txt_salida.insert(tk.END, encabezado)
            txt_salida.insert(tk.END, "-" * 65 + "\n")

            iteracion = 1
            error = abs(b - a)
            c_ant = a

            while error > tol and iteracion <= 100:
                c = (a + b) / 2
                fc = evaluar_funcion(func, c)

                if iteracion > 1:
                    error = abs(c - c_ant)

                linea = f"{iteracion:<5} | {a:<8.4f} | {b:<8.4f} | {c:<8.4f} | {fc:<10.4f} | {error:<8.4f}\n"
                txt_salida.insert(tk.END, linea)

                if abs(fc) < 1e-10:
                    break

                if fa * fc < 0:
                    b = c
                else:
                    a = c
                    fa = fc

                c_ant = c
                iteracion += 1

            txt_salida.insert(tk.END, f"\nRaíz aproximada: {c:.6f}\n")
        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))
        finally:
            txt_salida.config(state=tk.DISABLED)

    ttk.Button(win, text="Calcular Raíz", command=calcular).pack(pady=10)