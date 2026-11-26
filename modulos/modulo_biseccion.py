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
    win.geometry("760x560")
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

    txt_salida = tk.Text(win, height=22, font=("Consolas", 10), state=tk.DISABLED)
    txt_salida.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def calcular():
        txt_salida.config(state=tk.NORMAL)
        txt_salida.delete(1.0, tk.END)

        func = ent_func.get()
        try:
            a = float(ent_a.get())
            b = float(ent_b.get())
            tol = float(ent_tol.get())

            if a >= b:
                messagebox.showerror("Error", "El límite 'a' debe ser menor que 'b'.")
                return
            if tol <= 0:
                messagebox.showerror("Error", "La tolerancia debe ser mayor que cero.")
                return

            fa = evaluar_funcion(func, a)
            fb = evaluar_funcion(func, b)

            txt_salida.insert(tk.END, "=== VERIFICACIÓN INICIAL (TEOREMA DE BOLZANO) ===\n")
            txt_salida.insert(tk.END, f"f({a:.6f}) = {fa:.6f}\n")
            txt_salida.insert(tk.END, f"f({b:.6f}) = {fb:.6f}\n")
            txt_salida.insert(tk.END, f"f(a) * f(b) = {fa * fb:.6f}\n\n")

            if fa * fb >= 0:
                messagebox.showerror("Error", "f(a) y f(b) deben tener signos opuestos.")
                return

            txt_salida.insert(tk.END, "=== PASO A PASO POR ITERACIÓN ===\n")

            tabla = []
            iteracion = 1
            error = abs(b - a)
            c_ant = None
            c = None

            while iteracion <= 100:
                c = (a + b) / 2.0
                fa = evaluar_funcion(func, a)
                fc = evaluar_funcion(func, c)
                producto = fa * fc

                if c_ant is not None:
                    error = abs(c - c_ant)

                txt_salida.insert(tk.END, f"\n--- Iteración {iteracion} ---\n")
                txt_salida.insert(tk.END, f"  1. Intervalo actual: [{a:.6f}, {b:.6f}]\n")
                txt_salida.insert(tk.END, f"  2. Punto medio: c = ({a:.6f} + {b:.6f}) / 2 = {c:.6f}\n")
                txt_salida.insert(tk.END, f"  3. Evaluaciones: f(a) = {fa:.6f} | f(c) = {fc:.6f}\n")
                txt_salida.insert(tk.END, f"  4. Signo/Producto: f(a) * f(c) = {producto:.6f}\n")

                if producto < 0:
                    txt_salida.insert(tk.END, "  5. Cambio de signo en [a, c] -> nuevo intervalo: [a, c], b pasa a valer c.\n")
                    nuevo_a, nuevo_b = a, c
                elif producto > 0:
                    txt_salida.insert(tk.END, "  5. Cambio de signo en [c, b] -> nuevo intervalo: [c, b], a pasa a valer c.\n")
                    nuevo_a, nuevo_b = c, b
                else:
                    txt_salida.insert(tk.END, "  5. f(c) = 0 -> raíz exacta encontrada.\n")
                    error = 0.0
                    nuevo_a, nuevo_b = a, b

                if c_ant is not None and producto != 0:
                    txt_salida.insert(tk.END, f"  6. Error |c_act - c_ant| = |{c:.6f} - {c_ant:.6f}| = {error:.6f}\n")
                else:
                    txt_salida.insert(tk.END, f"  6. Error inicial (ancho del intervalo): {error:.6f}\n")

                tabla.append((iteracion, a, b, c, fc, error))

                if producto == 0 or (c_ant is not None and error <= tol):
                    txt_salida.insert(tk.END, f"  >> Criterio de parada cumplido en iteración {iteracion}.\n")
                    break

                a, b = nuevo_a, nuevo_b
                c_ant = c
                iteracion += 1

            txt_salida.insert(tk.END, "\n=== TABLA RESUMEN ===\n")
            encabezado = f"{'Iter':<5} | {'a':<10} | {'b':<10} | {'c':<10} | {'f(c)':<12} | {'Error':<10}\n"
            txt_salida.insert(tk.END, encabezado)
            txt_salida.insert(tk.END, "-" * 72 + "\n")
            for row in tabla:
                it, va, vb, vc, vfc, verr = row
                txt_salida.insert(tk.END, f"{it:<5} | {va:<10.6f} | {vb:<10.6f} | {vc:<10.6f} | {vfc:<12.6e} | {verr:<10.6f}\n")

            residuo = abs(evaluar_funcion(func, c))
            txt_salida.insert(tk.END, f"\nRaíz aproximada: {c:.6f}\n")
            txt_salida.insert(tk.END, f"Residuo |f(c)|: {residuo:.6e}\n")
        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))
        finally:
            txt_salida.config(state=tk.DISABLED)

    ttk.Button(win, text="Calcular Raíz", command=calcular).pack(pady=10)