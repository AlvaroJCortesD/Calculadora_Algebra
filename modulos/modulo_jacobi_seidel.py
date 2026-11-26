import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --- FUNCIONES MATEMÁTICAS ---

def es_diagonal_dominante(A):
    n = A.shape[0]
    for i in range(n):
        suma_fila = sum(abs(A[i, j]) for j in range(n) if i != j)
        if abs(A[i, i]) <= suma_fila:
            return False
    return True


def reordenar_matriz(A, b):
    n = A.shape[0]
    A_mod = A.copy()
    b_mod = b.copy()
    for i in range(n):
        if A_mod[i, i] == 0:
            for k in range(i + 1, n):
                if A_mod[k, i] != 0:
                    A_mod[[i, k]] = A_mod[[k, i]]
                    b_mod[[i, k]] = b_mod[[k, i]]
                    break
            else:
                return None, None
    return A_mod, b_mod


def generar_despejes(A, b):
    n = len(b)
    lineas = []
    for i in range(n):
        expr = f"{b[i]:g}"
        for j in range(n):
            if i != j and A[i, j] != 0:
                coef = A[i, j]
                if coef > 0:
                    expr += f" - {coef:g}*x{j + 1}"
                else:
                    expr += f" + {abs(coef):g}*x{j + 1}"
        lineas.append(f"  x{i + 1} = ( {expr} ) / {A[i, i]:g}")
    return "\n".join(lineas)


def metodo_iterativo(A, b, x0, tol, max_iter, metodo='jacobi', limite_pasos=5):
    n = len(b)
    x = x0.copy()
    historial = []
    errores = []
    pasos = []

    pasos.append(f"Vector inicial x^(0) = {np.round(x, 6).tolist()}\n")

    for k in range(1, max_iter + 1):
        x_new = np.zeros(n)
        registrar_paso = (k <= limite_pasos)

        if registrar_paso:
            pasos.append(f"--- Iteración {k} ---")
        elif k == limite_pasos + 1:
            pasos.append(f"... [Se omiten los pasos detallados a partir de la iteración {k} para evitar saturación] ...\n")

        for i in range(n):
            suma = 0
            terminos_str = []
            for j in range(n):
                if i != j:
                    if metodo == 'jacobi':
                        val = x[j]
                    elif metodo == 'seidel':
                        val = x_new[j] if j < i else x[j]
                    suma += A[i, j] * val
                    if registrar_paso:
                        terminos_str.append(f"({A[i, j]:g})*({val:.6f})")

            x_new[i] = (b[i] - suma) / A[i, i]
            if registrar_paso:
                suma_str = " + ".join(terminos_str)
                pasos.append(f"  x{i + 1}^({k}) = [ {b[i]:g} - ( {suma_str} ) ] / {A[i, i]:g} = {x_new[i]:.6f}")

        error = np.linalg.norm(x_new - x, np.inf)
        historial.append(np.round(x_new, 6))
        errores.append(error)

        if registrar_paso:
            pasos.append(f"  Error ||x^({k}) - x^({k - 1})||_inf = {error:.6f}\n")

        if np.isnan(error) or np.isinf(error):
            pasos.append(f">> Divergencia detectada en la iteración {k}.\n")
            return x_new, historial, errores, "Divergencia detectada", "\n".join(pasos)

        x = x_new
        if error <= tol:
            pasos.append(f">> Criterio de parada alcanzado en la iteración {k} (Error <= {tol}).\n")
            return x, historial, errores, f"Convergencia en iteración {k}", "\n".join(pasos)

    pasos.append(f">> Máximo de iteraciones ({max_iter}) alcanzado.\n")
    return x, historial, errores, "Máximo de iteraciones alcanzado", "\n".join(pasos)


# --- INTERFAZ GRÁFICA ---

def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Programa 8: Jacobi y Gauss-Seidel")
    win.geometry("980x760")
    win.grab_set()

    # 1. Marco Superior: Configuración de dimensiones y parámetros
    frame_config = tk.LabelFrame(win, text="Configuración del Sistema", padx=10, pady=5)
    frame_config.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_config, text="Dimensión (n x n):").pack(side=tk.LEFT)
    spin_n = ttk.Spinbox(frame_config, from_=2, to=10, width=4)
    spin_n.set(3)
    spin_n.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_config, text="Tolerancia:").pack(side=tk.LEFT, padx=(12, 4))
    ent_tol = ttk.Entry(frame_config, width=8)
    ent_tol.insert(0, "0.001")
    ent_tol.pack(side=tk.LEFT)

    tk.Label(frame_config, text="Max Iter:").pack(side=tk.LEFT, padx=(12, 4))
    ent_iter = ttk.Entry(frame_config, width=5)
    ent_iter.insert(0, "50")
    ent_iter.pack(side=tk.LEFT)

    tk.Label(frame_config, text="Mostrar N pasos:").pack(side=tk.LEFT, padx=(12, 4))
    ent_mostrar_n = ttk.Entry(frame_config, width=5)
    ent_mostrar_n.insert(0, "5")
    ent_mostrar_n.pack(side=tk.LEFT)

    # 2. Marco Central: Cuadrículas para la Matriz y Vectores
    frame_matrices = tk.Frame(win)
    frame_matrices.pack(fill="x", padx=10, pady=5)

    frame_A = tk.LabelFrame(frame_matrices, text="Matriz A", padx=5, pady=5)
    frame_A.pack(side=tk.LEFT, fill="y", padx=5)

    frame_b = tk.LabelFrame(frame_matrices, text="Vector b", padx=5, pady=5)
    frame_b.pack(side=tk.LEFT, fill="y", padx=5)

    frame_x0 = tk.LabelFrame(frame_matrices, text="Vector Inicial x(0)", padx=5, pady=5)
    frame_x0.pack(side=tk.LEFT, fill="y", padx=5)

    entradas_A = []
    entradas_b = []
    entradas_x0 = []

    def generar_cuadricula():
        """Limpia la pantalla y dibuja n x n cajitas de texto."""
        for widget in frame_A.winfo_children():
            widget.destroy()
        for widget in frame_b.winfo_children():
            widget.destroy()
        for widget in frame_x0.winfo_children():
            widget.destroy()
        entradas_A.clear()
        entradas_b.clear()
        entradas_x0.clear()

        n = int(spin_n.get())

        for i in range(n):
            fila_A = []
            for j in range(n):
                ent = tk.Entry(frame_A, width=5, justify="center")
                ent.grid(row=i, column=j, padx=2, pady=2)
                ent.insert(0, "0")
                fila_A.append(ent)
            entradas_A.append(fila_A)

            ent_b = tk.Entry(frame_b, width=5, justify="center")
            ent_b.grid(row=i, column=0, padx=2, pady=2)
            ent_b.insert(0, "0")
            entradas_b.append(ent_b)

            ent_x = tk.Entry(frame_x0, width=5, justify="center")
            ent_x.grid(row=i, column=0, padx=2, pady=2)
            ent_x.insert(0, "0")
            entradas_x0.append(ent_x)

        if n == 3:
            valores_A = [[4, 1, -1], [2, 7, 1], [1, -3, 12]]
            valores_b = [3, 19, 31]
            for i in range(3):
                entradas_b[i].delete(0, tk.END)
                entradas_b[i].insert(0, str(valores_b[i]))
                for j in range(3):
                    entradas_A[i][j].delete(0, tk.END)
                    entradas_A[i][j].insert(0, str(valores_A[i][j]))

    btn_generar = ttk.Button(frame_config, text="Generar/Limpiar Cuadrícula", command=generar_cuadricula)
    btn_generar.pack(side=tk.LEFT, padx=12)

    generar_cuadricula()

    # 3. Consola de Salida
    txt_salida = tk.Text(win, height=20, font=("Consolas", 9))
    txt_salida.pack(fill="both", expand=True, padx=10, pady=5)

    datos_grafica = {}

    def ejecutar_calculo():
        txt_salida.delete(1.0, tk.END)
        datos_grafica.clear()

        try:
            n = int(spin_n.get())
            tol = float(ent_tol.get())
            max_iter = int(ent_iter.get())
            limite_pasos = int(ent_mostrar_n.get())

            if limite_pasos < 0:
                messagebox.showerror("Error", "El número de pasos a mostrar no puede ser negativo.")
                return

            A = np.array([[float(entradas_A[i][j].get()) for j in range(n)] for i in range(n)])
            b = np.array([float(entradas_b[i].get()) for i in range(n)])
            x0 = np.array([float(entradas_x0[i].get()) for i in range(n)])

            txt_salida.insert(tk.END, "--- ANÁLISIS INICIAL ---\n")
            if es_diagonal_dominante(A):
                txt_salida.insert(tk.END,
                                  "[INFO] La matriz ES estrictamente diagonal dominante. Convergencia garantizada.\n\n")
            else:
                txt_salida.insert(tk.END, "[ADVERTENCIA] La matriz NO es estrictamente diagonal dominante.\n\n")

            if any(A[i, i] == 0 for i in range(n)):
                txt_salida.insert(tk.END, "[INFO] Cero detectado en la diagonal. Intentando reordenar filas...\n")
                A, b = reordenar_matriz(A, b)
                if A is None:
                    txt_salida.insert(tk.END, "[ERROR] No fue posible reordenar la matriz. El cálculo se detendrá.\n")
                    return
                txt_salida.insert(tk.END, "[ÉXITO] Matriz reordenada correctamente.\n\n")

            # Mostrar despeje de ecuaciones antes de iterar
            txt_salida.insert(tk.END, "--- DESPEJE DE VARIABLES ---\n")
            txt_salida.insert(tk.END, generar_despejes(A, b) + "\n\n")

            # Ejecutar Jacobi
            x_jac, hist_jac, err_jac, estado_jac, pasos_jac = metodo_iterativo(
                A, b, x0, tol, max_iter, 'jacobi', limite_pasos
            )
            res_jac = np.linalg.norm(np.dot(A, x_jac) - b, np.inf)
            datos_grafica['jacobi'] = err_jac

            # Ejecutar Gauss-Seidel
            x_sei, hist_sei, err_sei, estado_sei, pasos_sei = metodo_iterativo(
                A, b, x0, tol, max_iter, 'seidel', limite_pasos
            )
            res_sei = np.linalg.norm(np.dot(A, x_sei) - b, np.inf)
            datos_grafica['seidel'] = err_sei

            try:
                x_ref = np.linalg.solve(A, b)
                dif_jac = np.linalg.norm(x_jac - x_ref, np.inf)
                dif_sei = np.linalg.norm(x_sei - x_ref, np.inf)
            except np.linalg.LinAlgError:
                dif_jac = dif_sei = "N/A"

            for nombre, estado, hist, errs, x_final, res, dif, pasos in [
                ("JACOBI", estado_jac, hist_jac, err_jac, x_jac, res_jac, dif_jac, pasos_jac),
                ("GAUSS-SEIDEL", estado_sei, hist_sei, err_sei, x_sei, res_sei, dif_sei, pasos_sei)
            ]:
                txt_salida.insert(tk.END, f"================ MÉTODO DE {nombre} ================\n")
                txt_salida.insert(tk.END, f"=== PASO A PASO (MÁX. {limite_pasos} ITERACIONES) ===\n")
                txt_salida.insert(tk.END, pasos + "\n")

                txt_salida.insert(tk.END, f"=== TABLA RESUMEN ({nombre}) ===\n")
                txt_salida.insert(tk.END, f"Estado final: {estado}\n")
                txt_salida.insert(tk.END, f"Residuo ||Ax-b||_inf: {res:.6e}\n")
                txt_salida.insert(tk.END, f"Diferencia con solución numpy: {dif}\n\n")

                columnas = [f"x{i + 1}" for i in range(len(x0))]
                df = pd.DataFrame(hist, columns=columnas)
                df.index = df.index + 1
                df.index.name = "Iter"
                df["Error"] = errs
                txt_salida.insert(tk.END, df.to_string() + "\n\n")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa solo números válidos en las casillas.")
        except Exception as e:
            messagebox.showerror("Error de Ejecución", str(e))

    def mostrar_grafica():
        if not datos_grafica:
            messagebox.showwarning("Advertencia", "Primero debes ejecutar el cálculo.")
            return

        plt.figure(figsize=(8, 5))
        if 'jacobi' in datos_grafica:
            plt.plot(range(1, len(datos_grafica['jacobi']) + 1), datos_grafica['jacobi'], marker='o', label='Jacobi')
        if 'seidel' in datos_grafica:
            plt.plot(range(1, len(datos_grafica['seidel']) + 1), datos_grafica['seidel'], marker='x',
                     label='Gauss-Seidel')

        plt.yscale('log')
        plt.title('Comparación de Error vs Número de Iteración')
        plt.xlabel('Iteración')
        plt.ylabel('Error (Norma Infinita)')
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.show()

    frame_botones = tk.Frame(win)
    frame_botones.pack(pady=5)
    ttk.Button(frame_botones, text="Ejecutar Métodos", command=ejecutar_calculo).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botones, text="Mostrar Gráfica Comparativa", command=mostrar_grafica).pack(side=tk.LEFT, padx=10)