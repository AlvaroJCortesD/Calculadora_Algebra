#! /usr/bin/env python3
import matriz
from fractions import Fraction


def main():
    filas = matriz.asking_for_input("Ingrese el numero de filas: ", type=int)
    columnas = matriz.asking_for_input("Ingrese el numero de columnas: ", type=int)

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

    soluciones = matrix.gauss_jordan()

    if soluciones is not None:
        print("Valores de las variables:")
        for idx, sol in enumerate(soluciones):
            sub_indice = matriz.to_subscript(idx + 1)
            # Si el resultado es una fracción, muestra la fracción Y su equivalencia en decimales reales
            if isinstance(sol, matriz.Fraction):
                decimal_val = float(sol)
                print(
                    f"Variable x{sub_indice} = {sol}  (En numero real: {decimal_val:.4f})"
                )
            else:
                print(f"Variable x{sub_indice} = {sol}")

        print("\n--- VERIFICACIÓN AUTOMÁTICA ---")
        matriz.verificar_solucion(matriz_original, vector_b, soluciones)


if __name__ == "__main__":
    main()