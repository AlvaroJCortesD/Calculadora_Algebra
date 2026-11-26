import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def preparar_funcion(expr_str):
    """Interpreta f(x) con SymPy, obtiene f'(x) y genera evaluadores numéricos."""
    x_sym = sp.Symbol('x')
    expr = sp.sympify(expr_str, locals={'x': x_sym})

    # Validar que no existan variables desconocidas distintas de x
    simbolos_extra = expr.free_symbols - {x_sym}
    if simbolos_extra:
        raise ValueError(f"La expresión contiene variables no permitidas: {simbolos_extra}")

    derivada = sp.diff(expr, x_sym)

    # Funciones numéricas rápidas usando NumPy
    f_num = sp.lambdify(x_sym, expr, modules=['numpy'])
    df_num = sp.lambdify(x_sym, derivada, modules=['numpy'])

    return expr, derivada, f_num, df_num


def evaluar_seguro(func, valor):
    """Evalúa una función numérica y valida que el resultado sea real y finito."""
    res = func(valor)
    if np.iscomplexobj(res) or isinstance(res, complex):
        raise ValueError(f"La evaluación en x = {valor:.6g} produjo un número complejo.")
    res_float = float(res)
    if not np.isfinite(res_float):
        raise ValueError(f"La evaluación en x = {valor:.6g} produjo un valor no finito (NaN o Inf).")
    return res_float


def newton_raphson(f_num, df_num, x0, tol_pct, max_iter, limite_pasos=10, eps_derivada=1e-12):
    """
    Implementación propia del método abierto de Newton-Raphson con registro paso a paso.
    Retorna: diccionario con historial, pasos detallados, aproximación final, residuo y estado.
    """
    historial = []
    pasos = ["Fórmula iterativa: x_i = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})\n"]
    xi = float(x0)
    estado = "Máximo de iteraciones alcanzado sin cumplir la tolerancia."
    convergio = False
    error_final = None
    tipo_error_final = "%"

    for i in range(1, max_iter + 1):
        registrar_paso = (i <= limite_pasos)

        if i == limite_pasos + 1:
            pasos.append(
                f"... [Se omiten los pasos detallados a partir de la iteración {i} para evitar saturación] ...\n"
            )

        try:
            fxi = evaluar_seguro(f_num, xi)
            dfxi = evaluar_seguro(df_num, xi)
        except ValueError as err:
            estado = f"Detenido en iteración {i}: {err}"
            pasos.append(f"--- Iteración {i} (x_{i-1} = {xi:.6f}) ---")
            pasos.append(f"  [ERROR] {err}\n")
            break

        if registrar_paso:
            pasos.append(f"--- Iteración {i} (x_{i-1} = {xi:.6f}) ---")
            pasos.append(f"  1. Evaluar función y derivada en x_{i-1} = {xi:.6f}:")
            pasos.append(f"     f({xi:.6f})  = {fxi:.6f}")
            pasos.append(f"     f'({xi:.6f}) = {dfxi:.6f}")

        # Control de derivada nula o demasiado cercana a cero antes de dividir
        if abs(dfxi) < eps_derivada:
            historial.append({
                "i": i,
                "x_i": xi,
                "f(x_i)": fxi,
                "f'(x_i)": dfxi,
                "x_{i+1}": np.nan,
                "Error Aprox.": np.nan,
                "Tipo Error": "N/A"
            })
            estado = (
                f"Detenido en iteración {i}: derivada nula o cercana a cero "
                f"(|f'(x_i)| = {abs(dfxi):.2e} < {eps_derivada:.0e}). No es posible dividir."
            )
            if not registrar_paso:
                pasos.append(f"--- Iteración {i} (x_{i-1} = {xi:.6f}) ---")
            pasos.append(
                f"  2. [DETENIDO] Derivada nula o cercana a cero (|f'({xi:.6f})| = {abs(dfxi):.2e}). "
                f"Recta tangente horizontal; división imposible.\n"
            )
            break

        # Fórmula iterativa de Newton-Raphson
        cociente = fxi / dfxi
        x_next = xi - cociente

        if not np.isfinite(x_next):
            estado = f"Detenido en iteración {i}: la nueva aproximación no es finita."
            pasos.append(f"  2. [DETENIDO] La nueva aproximación x_{i} no es finita.\n")
            break

        # Cálculo del error relativo aproximado porcentual (evitando división por cero si x_{i+1} == 0)
        if abs(x_next) > 1e-15:
            error_aprox = abs((x_next - xi) / x_next) * 100.0
            tipo_error = "% (relativo)"
            err_formula_str = f"ε_a = |({x_next:.6f} - {xi:.6f}) / {x_next:.6f}| * 100 = {error_aprox:.6f}%"
            comp_str = f"{error_aprox:.6f}% <= {tol_pct}%" if error_aprox <= tol_pct else f"{error_aprox:.6f}% > {tol_pct}%"
        else:
            error_aprox = abs(x_next - xi)
            tipo_error = "absoluto (x_{i+1}=0)"
            err_formula_str = f"ε_a = |{x_next:.6f} - {xi:.6f}| = {error_aprox:.6f} (absoluto, x_{i} = 0)"
            comp_str = f"{error_aprox:.6f} <= {tol_pct}" if error_aprox <= tol_pct else f"{error_aprox:.6f} > {tol_pct}"

        if registrar_paso:
            pasos.append(f"  2. Calcular siguiente aproximación x_{i}:")
            pasos.append(f"     x_{i} = {xi:.6f} - ({fxi:.6f} / {dfxi:.6f})")
            pasos.append(f"     x_{i} = {xi:.6f} - ({cociente:.6f}) = {x_next:.6f}")
            pasos.append(f"  3. Calcular error aproximado:")
            pasos.append(f"     {err_formula_str}")
            if error_aprox <= tol_pct:
                pasos.append(f"  4. Verificación ({comp_str}): ¡Criterio de parada cumplido!\n")
            else:
                pasos.append(f"  4. Verificación ({comp_str}): continúa iterando.\n")

        historial.append({
            "i": i,
            "x_i": xi,
            "f(x_i)": fxi,
            "f'(x_i)": dfxi,
            "x_{i+1}": x_next,
            "Error Aprox.": error_aprox,
            "Tipo Error": tipo_error
        })

        xi = x_next
        error_final = error_aprox
        tipo_error_final = tipo_error

        # Criterio de parada por tolerancia
        if error_aprox <= tol_pct:
            estado = f"Convergencia alcanzada en la iteración {i} (error <= {tol_pct}%)."
            convergio = True
            if not registrar_paso:
                pasos.append(f">> Criterio de parada alcanzado en la iteración {i} ({comp_str}).\n")
            break

    # Evaluar residuo |f(x_aprox)| en la última aproximación válida
    try:
        residuo = abs(evaluar_seguro(f_num, xi))
    except ValueError:
        residuo = np.nan

    return {
        "historial": historial,
        "pasos": "\n".join(pasos),
        "x_aprox": xi,
        "iteraciones": len(historial),
        "error_final": error_final,
        "tipo_error": tipo_error_final,
        "residuo": residuo,
        "estado": estado,
        "convergio": convergio
    }


def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Programa 9: Método de Newton-Raphson")
    win.geometry("980x730")
    win.grab_set()

    # --- Panel de entradas ---
    frame_inputs = tk.LabelFrame(win, text="Datos de Entrada (Valores predeterminados editables)", padx=10, pady=10)
    frame_inputs.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_inputs, text="Función f(x) [sintaxis SymPy]:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
    ent_func = ttk.Entry(frame_inputs, width=32)
    ent_func.insert(0, "x**3 - x - 2")
    ent_func.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame_inputs, text="Valor inicial x0:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
    ent_x0 = ttk.Entry(frame_inputs, width=12)
    ent_x0.insert(0, "1.5")
    ent_x0.grid(row=0, column=3, padx=5, pady=4)

    tk.Label(frame_inputs, text="Tolerancia ε (%):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
    ent_tol = ttk.Entry(frame_inputs, width=15)
    ent_tol.insert(0, "0.001")
    ent_tol.grid(row=1, column=1, sticky="w", padx=5, pady=4)

    tk.Label(frame_inputs, text="Máx. Iteraciones:").grid(row=1, column=2, sticky="w", padx=5, pady=4)
    ent_iter = ttk.Entry(frame_inputs, width=12)
    ent_iter.insert(0, "50")
    ent_iter.grid(row=1, column=3, padx=5, pady=4)

    tk.Label(frame_inputs, text="Mostrar N pasos:").grid(row=1, column=4, sticky="w", padx=5, pady=4)
    ent_mostrar_n = ttk.Entry(frame_inputs, width=8)
    ent_mostrar_n.insert(0, "10")
    ent_mostrar_n.grid(row=1, column=5, padx=5, pady=4)

    tk.Label(
        frame_inputs,
        text="Ejemplos SymPy: x**3 - x - 2 | cos(x) - x | exp(-x) - x | x**2 - 4",
        fg="gray"
    ).grid(row=2, column=0, columnspan=6, sticky="w", padx=5, pady=(4, 0))

    # --- Área de resultados ---
    txt_salida = tk.Text(win, height=24, font=("Consolas", 9))
    txt_salida.pack(fill="both", expand=True, padx=10, pady=5)

    # Almacena datos de la última ejecución para graficar
    datos_grafica = {}

    def ejecutar_metodo():
        txt_salida.delete(1.0, tk.END)
        datos_grafica.clear()

        expr_str = ent_func.get().strip()
        if not expr_str:
            messagebox.showerror("Error de Entrada", "Debes ingresar una función f(x).")
            return

        # Validar entradas numéricas
        try:
            x0 = float(ent_x0.get())
            tol = float(ent_tol.get())
            max_iter = int(ent_iter.get())
            limite_pasos = int(ent_mostrar_n.get())
            if tol <= 0:
                raise ValueError("La tolerancia debe ser un número positivo.")
            if max_iter <= 0:
                raise ValueError("El máximo de iteraciones debe ser un entero positivo.")
            if limite_pasos < 0:
                raise ValueError("El número de pasos a mostrar no puede ser negativo.")
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Verifica los parámetros numéricos:\n{e}")
            return

        # Interpretar función y derivada con SymPy
        try:
            expr, derivada, f_num, df_num = preparar_funcion(expr_str)
        except Exception as e:
            messagebox.showerror("Error de Sintaxis", f"No se pudo interpretar f(x) con SymPy:\n{e}")
            return

        resultado = newton_raphson(f_num, df_num, x0, tol, max_iter, limite_pasos)

        # Guardar datos para graficar
        datos_grafica["expr"] = expr
        datos_grafica["f_num"] = f_num
        datos_grafica["x0"] = x0
        datos_grafica["resultado"] = resultado

        # Mostrar cabecera y parámetros
        txt_salida.insert(tk.END, "=== MÉTODO DE NEWTON-RAPHSON ===\n")
        txt_salida.insert(tk.END, f"Función ingresada  f(x)  = {expr}\n")
        txt_salida.insert(tk.END, f"Derivada simbólica f'(x) = {derivada}\n")
        txt_salida.insert(
            tk.END,
            f"Parámetros: x0 = {x0} | Tolerancia = {tol}% | Máx. Iteraciones = {max_iter}\n"
        )
        txt_salida.insert(
            tk.END,
            "Criterio de parada: ε_a(%) <= tolerancia (o error absoluto si x_{i+1} = 0) o máx. iteraciones.\n\n"
        )

        # Paso a paso detallado por iteración
        txt_salida.insert(tk.END, f"=== PASO A PASO POR ITERACIÓN (MÁX. {limite_pasos} PASOS) ===\n")
        txt_salida.insert(tk.END, resultado["pasos"] + "\n")

        # Tabla de iteraciones con Pandas
        txt_salida.insert(tk.END, "=== TABLA RESUMEN DE ITERACIONES ===\n")
        if resultado["historial"]:
            df = pd.DataFrame(resultado["historial"])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            txt_salida.insert(
                tk.END,
                df.to_string(
                    index=False,
                    float_format=lambda v: f"{v:.6f}" if abs(v) >= 1e-4 or v == 0 else f"{v:.4e}"
                ) + "\n\n"
            )
        else:
            txt_salida.insert(tk.END, "No se completaron iteraciones.\n\n")

        # Resumen final
        txt_salida.insert(tk.END, "=== RESUMEN DE RESULTADOS ===\n")
        txt_salida.insert(tk.END, f"Estado del proceso    : {resultado['estado']}\n")
        txt_salida.insert(tk.END, f"Iteraciones realizadas: {resultado['iteraciones']}\n")

        if resultado["convergio"]:
            txt_salida.insert(tk.END, f"Aproximación obtenida : {resultado['x_aprox']:.6f}\n")
        else:
            txt_salida.insert(
                tk.END,
                f"Última aproximación   : {resultado['x_aprox']:.6f} (NO cumple criterio de convergencia)\n"
            )

        if resultado["error_final"] is not None:
            txt_salida.insert(
                tk.END,
                f"Error alcanzado       : {resultado['error_final']:.6f} {resultado['tipo_error']}\n"
            )
        else:
            txt_salida.insert(tk.END, "Error alcanzado       : No disponible\n")

        txt_salida.insert(tk.END, f"Residuo |f(x_aprox)|  : {resultado['residuo']:.6e}\n")

    def mostrar_grafica():
        if not datos_grafica:
            messagebox.showwarning("Advertencia", "Primero debes ejecutar el método.")
            return

        res = datos_grafica["resultado"]
        f_num = datos_grafica["f_num"]
        expr = datos_grafica["expr"]
        hist = res["historial"]

        # Recolectar puntos finitos para definir el rango del eje X
        puntos_x = [datos_grafica["x0"]]
        for fila in hist:
            if np.isfinite(fila["x_i"]):
                puntos_x.append(fila["x_i"])
            if np.isfinite(fila["x_{i+1}"]):
                puntos_x.append(fila["x_{i+1}"])

        # Evitar rangos exagerados si el método divergió fuertemente
        puntos_razonables = [p for p in puntos_x if abs(p - datos_grafica["x0"]) < 1e4]
        if not puntos_razonables:
            puntos_razonables = [datos_grafica["x0"]]

        x_min = min(puntos_razonables)
        x_max = max(puntos_razonables)
        margen = max(1.0, (x_max - x_min) * 0.4)
        xs = np.linspace(x_min - margen, x_max + margen, 500)

        with np.errstate(all='ignore'):
            ys = np.array([f_num(val) for val in xs], dtype=float)
            ys = np.where(np.isfinite(ys), ys, np.nan)

        plt.figure(figsize=(9, 5.5))
        plt.plot(xs, ys, label=f"f(x) = {expr}", color="tab:blue", linewidth=2)
        plt.axhline(0, color="black", linewidth=1, linestyle="-")

        # Dibujar rectas tangentes (hasta las primeras 6 iteraciones para mantener claridad visual)
        max_tangentes = min(6, len(hist))
        for idx in range(max_tangentes):
            fila = hist[idx]
            xi = fila["x_i"]
            fxi = fila["f(x_i)"]
            x_next = fila["x_{i+1}"]
            if np.isfinite(xi) and np.isfinite(fxi) and np.isfinite(x_next):
                plt.plot([xi, xi], [0, fxi], color="gray", linestyle=":", linewidth=1)
                etiqueta = "Rectas tangentes" if idx == 0 else None
                plt.plot([xi, x_next], [fxi, 0], color="tab:orange", linestyle="--", linewidth=1.3, label=etiqueta)
                plt.scatter([xi], [fxi], color="tab:orange", s=30, zorder=4)

        # Marcar punto inicial y aproximación obtenida
        plt.scatter([datos_grafica["x0"]], [0], color="green", s=50, zorder=5, label=f"Inicial x0 = {datos_grafica['x0']:.4g}")
        if np.isfinite(res["x_aprox"]):
            lbl_final = (
                f"Raíz aproximada ≈ {res['x_aprox']:.6f}"
                if res["convergio"]
                else f"Última aprox. = {res['x_aprox']:.6f} (sin convergencia)"
            )
            plt.scatter([res["x_aprox"]], [0], color="red", s=65, marker="X", zorder=6, label=lbl_final)

        plt.title("Método de Newton-Raphson: f(x) y aproximaciones por tangentes")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --- Botones ---
    frame_botones = tk.Frame(win)
    frame_botones.pack(pady=6)
    ttk.Button(frame_botones, text="Calcular Raíz", command=ejecutar_metodo).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botones, text="Mostrar Gráfica y Tangentes", command=mostrar_grafica).pack(side=tk.LEFT, padx=10)