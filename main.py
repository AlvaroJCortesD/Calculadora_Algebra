#! /usr/bin/env python3
import matriz
from fractions import Fraction


def main():
    filas = matriz.asking_for_input("Ingrese el numero de filas (m): ", type=int)
    columnas = matriz.asking_for_input("Ingrese el numero de columnas (n): ", type=int)

    matrix = matriz.Matrix(filas, columnas)
    print(f"\nMatriz {filas}x{columnas} inicializada.")

    print("\n--- INGRESO DE VALORES PARA LA MATRIZ A ---")
    for i in range(filas):
        for j in range(columnas):
            valor = matriz.asking_for_input(
                f"Valor para la posicion [{i}][{j}]: ", type=float
            )
            if valor.is_integer():
                valor = int(valor)
            matrix.modify(i, j, valor)

    print("\n--- INGRESO DE VALORES PARA EL VECTOR B ---")
    vector_b = []
    for i in range(filas):
        valor = matriz.asking_for_input(
            f"Valor del vector b para la fila {i + 1}: ", type=float
        )
        if valor.is_integer():
            valor = int(valor)
        vector_b.append(valor)

    # Copia de la matriz de coeficientes original para la posterior comprobación
    matriz_original = [fila[:] for fila in matrix.array]

    matrix.add_vector_b(vector_b)
    print("\n--- MATRIZ AUMENTADA [A | b] ---")
    print(matrix)

    # Algoritmo de Gauss-Jordan
    matriz_rref, pivotes, libres, soluciones, forma_vectorial = matrix.gauss_jordan()

    # Impresión requerida
    print("--- IDENTIFICACIÓN DE PIVOTES Y VARIABLES ---")
    cols_pivote_str = ", ".join(str(p + 1) for p in pivotes) if pivotes else "Ninguna"
    vars_basicas_str = ", ".join(f"x{matriz.to_subscript(p + 1)}" for p in pivotes) if pivotes else "Ninguna"
    vars_libres_str = ", ".join(f"x{matriz.to_subscript(l + 1)}" for l in libres) if libres else "Ninguna"

    print(f"Posición de las columnas pivote: {cols_pivote_str}")
    print(f"Variables Básicas: {vars_basicas_str}")
    print(f"Variables Libres : {vars_libres_str}\n")

    # Muestra de soluciones
    if soluciones is not None:
        print("Valores de las variables (Solución Única):")
        for idx, sol in enumerate(soluciones):
            sub_indice = matriz.to_subscript(idx + 1)
            if isinstance(sol, Fraction):
                decimal_val = float(sol)
                print(
                    f"Variable x{sub_indice} = {sol}  (En numero real: {decimal_val:.4f})"
                )
            else:
                print(f"Variable x{sub_indice} = {sol}")

        print("\n--- VERIFICACIÓN AUTOMÁTICA ---")
        matriz.verificar_solucion(matriz_original, vector_b, soluciones)

    elif forma_vectorial is not None:
        print("--- ESTRUCTURA DE LA SOLUCIÓN GENERAL (FORMA VECTORIAL) ---")
        print(forma_vectorial)
        print()


if __name__ == "__main__":
    main()