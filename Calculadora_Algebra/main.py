"""
Interfaz Gráfica (GUI) - Proyecto Integrador.
Soporta Matrices, Vectores, Sistemas de Ecuaciones Lineales Ax = b,
Factorización LU y verificación de propiedades (teoremas).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from modulos.modulo_matrices import Matrix, matriz_desde_lista
from modulos.modulo_vectores import vector_a_lista, producto_punto, norma_vector, producto_cruz_3d
from modulos.modulo_sistemas import (
    resolver_sistema_gauss_jordan_paso_a_paso,
    resolver_sistema_inversa_paso_a_paso
)
from modulos.modulo_validaciones import (
    parsear_numero, parsear_entero, validar_nombre, parsear_cuadricula,
    validar_sistema, ErrorCelda
)
from modulos.modulo_lu import resolver_lu, LOGO_ASCII_LU, MENU_LU, teoremas_lu
from modulos.modulo_propiedades import verificar_propiedades, reporte_propiedades
from teoremas.resumen_teoremas import obtener_todos_teoremas


class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra Lineal - Proyecto Integrador")
        self.root.geometry("1180x680")

        self.memory = {}

        self.frame_left = tk.LabelFrame(self.root, text="Memoria (Variables)", width=250)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.frame_center = tk.LabelFrame(self.root, text="Crear Elemento")
        self.frame_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_right = tk.LabelFrame(self.root, text="Operaciones, Procedimiento y Resultados")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_memory_panel()
        self.setup_creation_panel()
        self.setup_operations_panel()

    def setup_memory_panel(self):
        self.listbox_vars = tk.Listbox(self.frame_left, font=("Consolas", 11))
        self.listbox_vars.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox_vars.bind('<<ListboxSelect>>', self.ver_matriz_guardada)

        self.btn_delete = ttk.Button(self.frame_left, text="Eliminar Seleccionada", command=self.eliminar_matriz)
        self.btn_delete.pack(pady=5)

    def actualizar_memoria(self):
        self.listbox_vars.delete(0, tk.END)
        for nombre, matriz in self.memory.items():
            tipo = "Vector" if matriz.columns == 1 else "Matriz"
            self.listbox_vars.insert(tk.END, f"{nombre} [{tipo} {matriz.rows}x{matriz.columns}]")

        nombres = list(self.memory.keys())
        self.cb_mat1['values'] = nombres
        self.cb_mat2['values'] = nombres
        self.cb_mat3['values'] = nombres

    def setup_creation_panel(self):
        top_frame = tk.Frame(self.frame_center)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="Variable:").grid(row=0, column=0)
        self.ent_nombre = tk.Entry(top_frame, width=5)
        self.ent_nombre.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Filas:").grid(row=0, column=2)
        self.ent_filas = tk.Entry(top_frame, width=3)
        self.ent_filas.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="Columnas:").grid(row=0, column=4)
        self.ent_cols = tk.Entry(top_frame, width=3)
        self.ent_cols.grid(row=0, column=5, padx=5)

        self.btn_grid = ttk.Button(top_frame, text="Generar", command=self.generar_cuadricula)
        self.btn_grid.grid(row=0, column=6, padx=10)

        self.grid_frame = tk.Frame(self.frame_center)
        self.grid_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.btn_guardar = ttk.Button(self.frame_center, text="Guardar en Memoria", command=self.guardar_matriz)
        self.btn_guardar.pack(pady=5)
        self.btn_guardar.pack_forget()

        self.matriz_entries = []

    def generar_cuadricula(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.matriz_entries.clear()

        try:
            filas = parsear_entero(self.ent_filas.get(), "Las filas")
            cols = parsear_entero(self.ent_cols.get(), "Las columnas")
        except ValueError as e:
            messagebox.showerror("Dimensiones inválidas", str(e))
            return

        for i in range(filas):
            fila_entries = []
            for j in range(cols):
                ent = tk.Entry(self.grid_frame, width=5, justify='center')
                ent.grid(row=i, column=j, padx=2, pady=2)
                ent.insert(0, "0")
                fila_entries.append(ent)
            self.matriz_entries.append(fila_entries)

        self.btn_guardar.pack(pady=5)

    def guardar_matriz(self):
        if not self.matriz_entries:
            messagebox.showerror("Error", "Primero genera la cuadrícula con las dimensiones.")
            return

        for fila_entries in self.matriz_entries:
            for ent in fila_entries:
                ent.config(bg="white")

        try:
            nombre = validar_nombre(self.ent_nombre.get(), "El nombre de la variable")
            valores = parsear_cuadricula([[ent.get() for ent in fila] for fila in self.matriz_entries])
        except ErrorCelda as e:
            ent = self.matriz_entries[e.fila][e.columna]
            ent.config(bg="#ffcccc")
            ent.focus_set()
            ent.selection_range(0, tk.END)
            messagebox.showerror("Dato inválido", f"{e}\nCorrígelo (celda marcada en rojo) y vuelve a guardar.")
            return
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if nombre in self.memory and not messagebox.askyesno(
                "Sobrescribir", f"'{nombre}' ya existe en memoria. ¿Deseas reemplazarla?"):
            return

        filas = len(valores)
        cols = len(valores[0])
        nueva_matriz = Matrix(filas, cols)
        for i in range(filas):
            for j in range(cols):
                nueva_matriz.modify(i, j, valores[i][j])

        self.memory[nombre] = nueva_matriz
        self.actualizar_memoria()
        messagebox.showinfo("Éxito", f"'{nombre}' guardado en memoria.")

    def setup_operations_panel(self):
        op_frame = tk.Frame(self.frame_right)
        op_frame.pack(pady=10)

        tk.Label(op_frame, text="Operación a realizar:").grid(row=0, column=0, columnspan=4)

        opciones = [
            "Suma (A+B)",
            "Resta (A-B)",
            "Multiplicar (A*B / A*v)",
            "Escalar (c*A)",
            "Transpuesta (A^T)",
            "Determinante (Triangular Paso a Paso)",
            "Determinante (Cofactores Paso a Paso)",
            "Inversa (Gauss-Jordan Paso a Paso)",
            "Inversa (por Adjunta Paso a Paso)",
            "Matriz Adjunta (adj A)",
            "Matriz de Menores (M_ij Paso a Paso)",
            "Matriz de Cofactores (C_ij Paso a Paso)",
            "Sistema Ax = b (Gauss-Jordan en [A|b] Paso a Paso)",
            "Sistema Ax = b (Por Inversa x = A^-1*b Paso a Paso)",
            "Producto Punto (u · v)",
            "Norma ||u||",
            "Producto Cruz (u x v)",
            "Factorización LU y solución Ax = b",
            "Verificar Propiedades (teoremas con A, B, C, k)"
        ]

        self.cb_op = ttk.Combobox(op_frame, values=opciones, state="readonly", width=55)
        self.cb_op.grid(row=1, column=0, columnspan=4, pady=5)
        self.cb_op.current(0)
        self.cb_op.bind('<<ComboboxSelected>>', self.al_cambiar_operacion)

        tk.Label(op_frame, text="Matriz A / Vector 1:").grid(row=2, column=0)
        self.cb_mat1 = ttk.Combobox(op_frame, width=5, state="readonly")
        self.cb_mat1.grid(row=2, column=1)

        tk.Label(op_frame, text="Matriz B / Vector b / Escalar:").grid(row=2, column=2)
        self.cb_mat2 = ttk.Combobox(op_frame, width=5)
        self.cb_mat2.grid(row=2, column=3)

        tk.Label(op_frame, text="Matriz C (propiedades):").grid(row=3, column=0)
        self.cb_mat3 = ttk.Combobox(op_frame, width=5, state="readonly")
        self.cb_mat3.grid(row=3, column=1)

        tk.Label(op_frame, text="Escalar k (propiedades):").grid(row=3, column=2)
        self.ent_k = tk.Entry(op_frame, width=7)
        self.ent_k.insert(0, "2")
        self.ent_k.grid(row=3, column=3)

        tk.Label(op_frame, text="Guardar resultado como:").grid(row=4, column=0, columnspan=2, pady=10)
        self.ent_res_nombre = tk.Entry(op_frame, width=8)
        self.ent_res_nombre.grid(row=4, column=2, columnspan=2)

        self.btn_calcular = ttk.Button(op_frame, text="Calcular y Mostrar Paso a Paso", command=self.calcular)
        self.btn_calcular.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_teoremas = ttk.Button(op_frame, text="Ver Teoremas Clave", command=self.mostrar_teoremas)
        self.btn_teoremas.grid(row=5, column=2, columnspan=2, pady=10)

        self.btn_teoremas_lu = ttk.Button(op_frame, text=MENU_LU, command=self.mostrar_teoremas_lu)
        self.btn_teoremas_lu.grid(row=6, column=0, columnspan=4, pady=2)

        self.txt_salida = tk.Text(self.frame_right, height=18, font=("Consolas", 11), state=tk.DISABLED)
        self.txt_salida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, mensaje):
        self.txt_salida.config(state=tk.NORMAL)
        self.txt_salida.delete(1.0, tk.END)
        self.txt_salida.insert(tk.END, mensaje)
        self.txt_salida.config(state=tk.DISABLED)

    def mostrar_teoremas(self):
        self.log(obtener_todos_teoremas())

    def mostrar_teoremas_lu(self):
        self.log(LOGO_ASCII_LU + "\n" + teoremas_lu())

    def al_cambiar_operacion(self, event=None):
        """Al elegir el módulo LU se muestra su logotipo y el menú del módulo."""
        if "Factorización LU" in self.cb_op.get():
            self.log(
                LOGO_ASCII_LU
                + "\n  Menú del módulo:\n"
                + f"    {MENU_LU}  (botón inferior)\n"
                + "    1. Elige A (m x n) como Matriz A y el vector b (m x 1) como Matriz B / Vector b.\n"
                + "    2. Pulsa 'Calcular y Mostrar Paso a Paso'.\n"
                + "    Con un nombre en 'Guardar resultado como' se guardan <nombre>_L, _U, _y y _x."
            )

    def calcular(self):
        op = self.cb_op.get()
        n1 = self.cb_mat1.get()
        n2 = self.cb_mat2.get()
        res_nombre = self.ent_res_nombre.get().strip()

        if n1 not in self.memory:
            messagebox.showerror("Error", "Selecciona la Matriz A / Vector 1 de la memoria.")
            return

        if res_nombre:
            try:
                validar_nombre(res_nombre, "El nombre del resultado")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

        usa_b_obligatoria = any(t in op for t in (
            "Suma", "Resta", "Multiplicar", "Sistema Ax", "Producto Punto",
            "Producto Cruz", "Factorización LU"))
        if usa_b_obligatoria and n2 not in self.memory:
            messagebox.showerror("Error", "Selecciona de la memoria la segunda variable "
                                          "(Matriz B / Vector b) que requiere esta operación.")
            return
        if "Verificar Propiedades" in op:
            for etiqueta, nombre in (("B", n2), ("C", self.cb_mat3.get())):
                if nombre and nombre not in self.memory:
                    messagebox.showerror("Error", f"La matriz {etiqueta} '{nombre}' no existe en memoria.")
                    return

        A = self.memory[n1]
        resultado = None
        texto_resultado = ""
        extras = {}

        try:
            if "Factorización LU" in op:
                B = self.memory[n2]
                validar_sistema(A.rows, B.rows, B.columns)
                lu = resolver_lu(A.array, B.array)
                texto_resultado = LOGO_ASCII_LU + "\n" + lu["procedimiento"]
                for sufijo in ("L", "U", "y", "x"):
                    if lu[sufijo] is not None:
                        extras[sufijo] = lu[sufijo]
            elif "Verificar Propiedades" in op:
                k = parsear_numero(self.ent_k.get(), "El escalar k")
                B_arr = self.memory[n2].array if n2 in self.memory else None
                nombre_c = self.cb_mat3.get()
                C_arr = self.memory[nombre_c].array if nombre_c in self.memory else None
                texto_resultado = reporte_propiedades(verificar_propiedades(A.array, B_arr, C_arr, k))
            elif "Suma" in op:
                B = self.memory[n2]
                resultado = A.sumar(B)
                texto_resultado = f"--- SUMA: {n1} + {n2} ---\n{resultado}"
            elif "Resta" in op:
                B = self.memory[n2]
                resultado = A.restar(B)
                texto_resultado = f"--- RESTA: {n1} - {n2} ---\n{resultado}"
            elif "Multiplicar" in op:
                B = self.memory[n2]
                resultado = A.multiplicar(B)
                texto_resultado = f"--- MULTIPLICACIÓN: {n1} · {n2} ---\n{resultado}"
            elif "Escalar" in op:
                c = parsear_numero(n2, "El escalar")
                resultado = A.escalar_mult(c)
                texto_resultado = f"--- MULTIPLICACIÓN POR ESCALAR: {c} · {n1} ---\n{resultado}"
            elif "Transpuesta" in op:
                resultado = A.traspuesta()
                texto_resultado = f"--- TRANSPUESTA DE {n1} ---\n{resultado}"
            elif "Determinante (Triangular" in op:
                det, pas_str = A.determinante_triangular_paso_a_paso()
                texto_resultado = f"{pas_str}\n\nRESULTADO FINAL: det({n1}) = {det}"
            elif "Determinante (Cofactores" in op:
                det, pas_str = A.determinante_cofactores_paso_a_paso()
                texto_resultado = f"{pas_str}\n\nRESULTADO FINAL: det({n1}) = {det}"
            elif "Gauss-Jordan Paso a Paso)" in op and "Sistema" not in op:
                resultado, texto_resultado = A.inversa_gauss_jordan_paso_a_paso()
            elif "por Adjunta Paso a Paso" in op:
                resultado, texto_resultado = A.inversa_adjunta_paso_a_paso()
            elif "Matriz de Menores" in op:
                resultado, texto_resultado = A.menores_paso_a_paso()
            elif "Matriz de Cofactores" in op:
                resultado, texto_resultado = A.cofactores_paso_a_paso()
            elif "Matriz Adjunta" in op:
                resultado = A.adjunta()
                texto_resultado = f"--- MATRIZ ADJUNTA DE {n1} ---\nadj({n1}) =\n{resultado}"

            # --- SISTEMAS DE ECUACIONES LINEALES ---
            elif "Sistema Ax = b (Gauss-Jordan" in op:
                B = self.memory[n2] # Vector b (matriz n x 1)
                validar_sistema(A.rows, B.rows, B.columns)
                resultado, texto_resultado = resolver_sistema_gauss_jordan_paso_a_paso(A, B)
            elif "Sistema Ax = b (Por Inversa" in op:
                B = self.memory[n2] # Vector b (matriz n x 1)
                validar_sistema(A.rows, B.rows, B.columns)
                resultado, texto_resultado = resolver_sistema_inversa_paso_a_paso(A, B)

            # --- OPERACIONES DE VECTORES ---
            elif "Producto Punto" in op:
                B = self.memory[n2]
                u_list = vector_a_lista(A)
                v_list = vector_a_lista(B)
                p_punto = producto_punto(u_list, v_list)
                texto_resultado = f"--- PRODUCTO PUNTO: {n1} · {n2} ---\nResultado = {p_punto}"
            elif "Norma" in op:
                u_list = vector_a_lista(A)
                norma = norma_vector(u_list)
                texto_resultado = f"--- NORMA ||{n1}|| ---\nResultado = {norma:.4f}"
            elif "Producto Cruz" in op:
                B = self.memory[n2]
                u_list = vector_a_lista(A)
                v_list = vector_a_lista(B)
                cruz = producto_cruz_3d(u_list, v_list)
                resultado = Matrix(3, 1)
                for i in range(3):
                    resultado.modify(i, 0, cruz[i])
                texto_resultado = f"--- PRODUCTO CRUZ: {n1} x {n2} ---\n{resultado}"

            if res_nombre and extras:
                for sufijo, valor in extras.items():
                    self.memory[f"{res_nombre}_{sufijo}"] = matriz_desde_lista(valor)
                texto_resultado += "\n\nGuardado en memoria: " + ", ".join(
                    f"{res_nombre}_{sufijo}" for sufijo in extras)
                self.actualizar_memoria()

            self.log(texto_resultado)

            if resultado is not None and res_nombre:
                self.memory[res_nombre] = resultado
                self.actualizar_memoria()

        except KeyError:
            messagebox.showerror("Error", "Ingresa un segundo elemento (Matriz B / Vector b / Escalar) válido de la memoria.")
        except ValueError as e:
            self.log(f"[ERROR]: {e}")
            messagebox.showerror("Error Matemático", str(e))
        except Exception as e:
            self.log(f"[ERROR INESPERADO]: {type(e).__name__}: {e}")
            messagebox.showerror("Error inesperado", f"{type(e).__name__}: {e}")

    def ver_matriz_guardada(self, event):
        seleccion = self.listbox_vars.curselection()
        if seleccion:
            index = seleccion[0]
            texto_item = self.listbox_vars.get(index)
            nombre = texto_item.split()[0]
            matriz = self.memory[nombre]
            self.log(f"--- {nombre} ---\n{matriz}")

    def eliminar_matriz(self):
        seleccion = self.listbox_vars.curselection()
        if seleccion:
            index = seleccion[0]
            texto_item = self.listbox_vars.get(index)
            nombre = texto_item.split()[0]
            del self.memory[nombre]
            self.actualizar_memoria()
            self.log(f"'{nombre}' eliminado de la memoria.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()