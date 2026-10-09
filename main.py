"""
Interfaz Gráfica (GUI) - Proyecto Integrador.
Soporta Operaciones con Matrices y Vectores.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from modulos.modulo_matrices import Matrix
from modulos.modulo_vectores import vector_a_lista, producto_punto, norma_vector, producto_cruz_3d
from teoremas.resumen_teoremas import obtener_todos_teoremas

class CalculadoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra Lineal - Proyecto Integrador")
        self.root.geometry("1100x600")

        self.memory = {}

        self.frame_left = tk.LabelFrame(self.root, text="Memoria (Matrices y Vectores)", width=250)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.frame_center = tk.LabelFrame(self.root, text="Crear Elemento")
        self.frame_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_right = tk.LabelFrame(self.root, text="Operaciones y Resultados")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_memory_panel()
        self.setup_creation_panel()
        self.setup_operations_panel()

    def setup_memory_panel(self):
        self.listbox_vars = tk.Listbox(self.frame_left, font=("Consolas", 12))
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
            filas = int(self.ent_filas.get())
            cols = int(self.ent_cols.get())
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones deben ser enteros.")
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
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Asigna un nombre (Ej. A, u, v).")
            return

        filas = len(self.matriz_entries)
        cols = len(self.matriz_entries[0])
        nueva_matriz = Matrix(filas, cols)

        try:
            for i in range(filas):
                for j in range(cols):
                    val_str = self.matriz_entries[i][j].get()
                    nueva_matriz.modify(i, j, Fraction(val_str))

            self.memory[nombre] = nueva_matriz
            self.actualizar_memoria()
            messagebox.showinfo("Éxito", f"'{nombre}' guardado en memoria.")
        except Exception:
            messagebox.showerror("Error", "Usa enteros, decimales o fracciones válidas.")

    def setup_operations_panel(self):
        op_frame = tk.Frame(self.frame_right)
        op_frame.pack(pady=10)

        tk.Label(op_frame, text="Operación:").grid(row=0, column=0, columnspan=4)

        # Opciones agregadas para Vectores
        opciones = [
            "Suma (A+B)",
            "Resta (A-B)",
            "Multiplicar (A*B / A*v)",
            "Escalar (c*A)",
            "Transpuesta (A^T)",
            "Determinante |A|",
            "Inversa (A^-1)",
            "Producto Punto (u · v)",
            "Norma ||u||",
            "Producto Cruz (u x v)"
        ]

        self.cb_op = ttk.Combobox(op_frame, values=opciones, state="readonly", width=22)
        self.cb_op.grid(row=1, column=0, columnspan=4, pady=5)
        self.cb_op.current(0)

        tk.Label(op_frame, text="Matriz 1 / Vector 1:").grid(row=2, column=0)
        self.cb_mat1 = ttk.Combobox(op_frame, width=5, state="readonly")
        self.cb_mat1.grid(row=2, column=1)

        tk.Label(op_frame, text="Matriz 2 / Vector 2 / Escalar:").grid(row=2, column=2)
        self.cb_mat2 = ttk.Combobox(op_frame, width=5)
        self.cb_mat2.grid(row=2, column=3)

        tk.Label(op_frame, text="Guardar resultado como:").grid(row=3, column=0, columnspan=2, pady=10)
        self.ent_res_nombre = tk.Entry(op_frame, width=8)
        self.ent_res_nombre.grid(row=3, column=2, columnspan=2)

        self.btn_calcular = ttk.Button(op_frame, text="Calcular", command=self.calcular)
        self.btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_teoremas = ttk.Button(op_frame, text="Ver Teoremas", command=self.mostrar_teoremas)
        self.btn_teoremas.grid(row=4, column=2, columnspan=2, pady=10)

        self.txt_salida = tk.Text(self.frame_right, height=15, font=("Consolas", 12), state=tk.DISABLED)
        self.txt_salida.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, mensaje):
        self.txt_salida.config(state=tk.NORMAL)
        self.txt_salida.delete(1.0, tk.END)
        self.txt_salida.insert(tk.END, mensaje)
        self.txt_salida.config(state=tk.DISABLED)

    def mostrar_teoremas(self):
        self.log(obtener_todos_teoremas())

    def calcular(self):
        op = self.cb_op.get()
        n1 = self.cb_mat1.get()
        n2 = self.cb_mat2.get()
        res_nombre = self.ent_res_nombre.get().strip()

        if n1 not in self.memory:
            messagebox.showerror("Error", "Selecciona la Matriz 1 / Vector 1.")
            return

        A = self.memory[n1]
        resultado = None
        texto_resultado = ""

        try:
            if "Suma" in op:
                B = self.memory[n2]
                resultado = A.sumar(B)
                texto_resultado = f"--- {n1} + {n2} ---\n{resultado}"
            elif "Resta" in op:
                B = self.memory[n2]
                resultado = A.restar(B)
                texto_resultado = f"--- {n1} - {n2} ---\n{resultado}"
            elif "Multiplicar" in op:
                B = self.memory[n2]
                resultado = A.multiplicar(B)
                texto_resultado = f"--- {n1} · {n2} ---\n{resultado}"
            elif "Escalar" in op:
                c = Fraction(n2)
                resultado = A.escalar_mult(c)
                texto_resultado = f"--- {c} · {n1} ---\n{resultado}"
            elif "Transpuesta" in op:
                resultado = A.traspuesta()
                texto_resultado = f"--- Transpuesta de {n1} ---\n{resultado}"
            elif "Determinante" in op:
                det = A.determinante_triangular()
                texto_resultado = f"--- Determinante de {n1} ---\n|{n1}| = {det}"
            elif "Inversa" in op:
                resultado = A.inversa()
                texto_resultado = f"--- Inversa de {n1} ---\n{resultado}"

            # --- OPERACIONES DE VECTORES ---
            elif "Producto Punto" in op:
                B = self.memory[n2]
                u_list = vector_a_lista(A)
                v_list = vector_a_lista(B)
                p_punto = producto_punto(u_list, v_list)
                texto_resultado = f"--- Producto Punto {n1} · {n2} ---\nResultado = {p_punto}"
            elif "Norma" in op:
                u_list = vector_a_lista(A)
                norma = norma_vector(u_list)
                texto_resultado = f"--- Norma ||{n1}|| ---\nResultado = {norma:.4f}"
            elif "Producto Cruz" in op:
                B = self.memory[n2]
                u_list = vector_a_lista(A)
                v_list = vector_a_lista(B)
                cruz = producto_cruz_3d(u_list, v_list)

                # Convertir resultado a matriz columna 3x1 para guardarlo
                resultado = Matrix(3, 1)
                for i in range(3):
                    resultado.modify(i, 0, cruz[i])
                texto_resultado = f"--- Producto Cruz {n1} x {n2} ---\n{resultado}"

            self.log(texto_resultado)

            if resultado is not None and res_nombre:
                self.memory[res_nombre] = resultado
                self.actualizar_memoria()

        except KeyError:
            messagebox.showerror("Error", "Ingresa una segunda matriz/vector/escalar válido.")
        except ValueError as e:
            messagebox.showerror("Error Matemático", str(e))

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
            self.log(f"'{nombre}' eliminado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGUI(root)
    root.mainloop()