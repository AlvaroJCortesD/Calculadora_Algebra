#! /usr/bin/env python3
import matriz
from fractions import Fraction

# Solicita filas, columnas y entradas para construir e instanciar una nueva objeto Matrix.
def crear_matriz_interactiva(nombre="A"):
    filas = matriz.asking_for_input(f"Filas de {nombre} (m): ", type=int)
    cols = matriz.asking_for_input(f"Columnas de {nombre} (n): ", type=int)
    m = matriz.Matrix(filas, cols)
    for i in range(filas):
        for j in range(cols):
            v = matriz.asking_for_input(f"Posición [{i}][{j}]: ")
            m.modify(i, j, v)
    return m

# Despliega el menú principal interactivo de la calculadora de álgebra lineal.
def main():
    while True:
        print("\n==================================================")
        print("    CALCULADORA DE ÁLGEBRA LINEAL")
        print("==================================================")
        print("1. Módulo de Vectores (R^n) y Combinación Lineal")
        print("2. Módulo de Operaciones Matriciales Básicas")
        print("3. Ecuaciones Matriciales (Ax = b)")
        print("4. Salir")
        
        opcion = matriz.asking_for_input("Seleccione una opción (1-4): ", type=int)

        if opcion == 1:
            print("\n--- MÓDULO DE VECTORES ---")
            dim = matriz.asking_for_input("Dimensión n de los vectores: ", type=int)
            u = [matriz.asking_for_input(f"u[{i+1}]: ") for i in range(dim)]
            v = [matriz.asking_for_input(f"v[{i+1}]: ") for i in range(dim)]
            
            print(f"\nSuma u + v: {matriz.sumar_vectores(u, v)}")
            print(f"Resta u - v: {matriz.restar_vectores(u, v)}")
            c = matriz.asking_for_input("Escalar c: ")
            print(f"Escalar c * u: {matriz.escalar_por_vector(c, u)}")

            print("\n-- Evaluación de Combinación Lineal --")
            k = matriz.asking_for_input("Cantidad de vectores en el conjunto: ", type=int)
            conjunto = []
            for idx in range(k):
                print(f"Vector v{idx+1}:")
                conjunto.append([matriz.asking_for_input(f"v{idx+1}[{i+1}]: ") for i in range(dim)])
            b = [matriz.asking_for_input(f"b[{i+1}]: ") for i in range(dim)]
            
            es_cl = matriz.es_combinacion_lineal(conjunto, b)
            if es_cl:
                print("\n[RESULTADO]: El vector b SÍ es combinación lineal del conjunto.")
            else:
                print("\n[RESULTADO]: El vector b NO es combinación lineal del conjunto.")

        elif opcion == 2:
            print("\n--- MÓDULO DE OPERACIONES MATRICIALES ---")
            print("1. Suma / Resta")
            print("2. Multiplicación por Escalar")
            print("3. Multiplicación de Matrices (A * B)")
            sub_op = matriz.asking_for_input("Opción: ", type=int)

            if sub_op == 1:
                A = crear_matriz_interactiva("A")
                B = crear_matriz_interactiva("B")
                try:
                    print("\nMatriz A + B:\n", A.sumar(B))
                    print("\nMatriz A - B:\n", A.restar(B))
                except ValueError as e:
                    print(f"\n[ERROR DE DIMENSIONES]: {e}")
            elif sub_op == 2:
                A = crear_matriz_interactiva("A")
                c = matriz.asking_for_input("Escalar c: ")
                print(f"\nMatriz {c} * A:\n", A.escalar_mult(c))
            elif sub_op == 3:
                A = crear_matriz_interactiva("A")
                B = crear_matriz_interactiva("B")
                try:
                    print("\nMatriz Producto (A * B):\n", A.multiplicar(B))
                except ValueError as e:
                    print(f"\n[ERROR DE DIMENSIONES]: {e}")

        elif opcion == 3:
            print("\n--- ECUACIONES MATRICIALES (Ax = b) ---")
            filas = matriz.asking_for_input("Número de filas (m): ", type=int)
            columnas = matriz.asking_for_input("Número de columnas (n): ", type=int)
            matrix = matriz.Matrix(filas, columnas)

            print("\n--- INGRESO DE VALORES PARA LA MATRIZ A ---")
            for i in range(filas):
                for j in range(columnas):
                    valor = matriz.asking_for_input(f"Posición [{i}][{j}]: ")
                    matrix.modify(i, j, valor)

            print("\n--- INGRESO DE VALORES PARA EL VECTOR B ---")
            vector_b = [matriz.asking_for_input(f"Fila {i + 1}: ") for i in range(filas)]

            matriz_original = [fila[:] for fila in matrix.array]
            matrix.add_vector_b(vector_b)

            print("\n--- MATRIZ AUMENTADA [A | b] ---")
            print(matriz.format_matrix(matrix.array))

            matriz_rref, pivotes, libres, soluciones, forma_vectorial = matrix.gauss_jordan()

            print("--- IDENTIFICACIÓN DE PIVOTES Y VARIABLES ---")
            cols_pivote_str = ", ".join(str(p + 1) for p in pivotes) if pivotes else "Ninguna"
            vars_basicas_str = ", ".join(f"x{matriz.to_subscript(p + 1)}" for p in pivotes) if pivotes else "Ninguna"
            vars_libres_str = ", ".join(f"x{matriz.to_subscript(l + 1)}" for l in libres) if libres else "Ninguna"

            print(f"Posición de las columnas pivote: {cols_pivote_str}")
            print(f"Variables Básicas: {vars_basicas_str}")
            print(f"Variables Libres : {vars_libres_str}\n")

            if soluciones is not None:
                print("Valores de las variables (Solución Única):")
                for idx, sol in enumerate(soluciones):
                    sub_indice = matriz.to_subscript(idx + 1)
                    if isinstance(sol, Fraction):
                        decimal_val = float(sol)
                        print(f"Variable x{sub_indice} = {sol}  (En numero real: {decimal_val:.4f})")
                    else:
                        print(f"Variable x{sub_indice} = {sol}")

                print("\n--- VERIFICACIÓN AUTOMÁTICA ---")
                matriz.verificar_solucion(matriz_original, vector_b, soluciones)

            elif forma_vectorial is not None:
                print("--- ESTRUCTURA DE LA SOLUCIÓN GENERAL (FORMA VECTORIAL) ---")
                print(forma_vectorial)

        elif opcion == 4:
            print("¡Programa finalizado!")
            break


if __name__ == "__main__":
    main()