"""
Módulo de Factorización LU y Resolución de Sistemas.
Unidad: Álgebra Lineal.
Propósito: Descomponer A = LU sin permutaciones y resolver Ax = b mediante
doble sustitución (Ly = b y Ux = y).
"""
from fractions import Fraction
from modulos.modulo_matrices import Matrix


def factorizacion_lu(A_matriz):
    """
    Descompone la matriz A en un producto L * U.
    A_matriz: Instancia de Matrix (m x n).
    Retorna: (L, U, procedimiento_str). L es triangular inferior, U es escalonada.
    """
    m = A_matriz.rows
    n = A_matriz.columns

    L = Matrix(m, m)
    U = Matrix(m, n)

    # Inicializar L con 1s en la diagonal y U como copia de A
    for i in range(m):
        L.modify(i, i, Fraction(1))
        for j in range(n):
            U.modify(i, j, Fraction(A_matriz.array[i][j]))

    pasos = ["--- FACTORIZACIÓN LU (A = LU) ---"]

    for j in range(min(m, n)):
        pivote = U.array[j][j]
        if pivote == 0:
            raise ValueError("La matriz no admite Factorización LU sin permutación (requiere pivoteo parcial PA=LU).")

        for i in range(j + 1, m):
            # El multiplicador se registra en L antes de alterar la fila en U
            multiplicador = U.array[i][j] / pivote
            L.modify(i, j, multiplicador)
            pasos.append(f"Multiplicador l_{i + 1}{j + 1} = {U.array[i][j]} / {pivote} = {multiplicador}")

            for k in range(j, n):
                nuevo_val = U.array[i][k] - multiplicador * U.array[j][k]
                U.modify(i, k, nuevo_val)

    pasos.append("\nMatriz L (Triangular Inferior):")
    pasos.append(str(L))
    pasos.append("\nMatriz U (Escalonada):")
    pasos.append(str(U))

    return L, U, "\n".join(pasos)


def resolver_sistema_lu(L, U, b_mat):
    """
    Resuelve el sistema Ax = b utilizando la factorización LU.
    L, U, b_mat: Instancias de Matrix.
    Retorna: (y, x, procedimiento_str). y es el vector intermedio, x es la solución.
    """
    m = L.rows
    n = U.columns

    pasos = ["\n--- SOLUCIÓN DEL SISTEMA Ax = b POR LU ---"]

    # 1. Sustitución hacia adelante: Ly = b
    pasos.append("1. Sustitución hacia adelante: Resolver Ly = b para hallar el vector intermedio y.")
    y = Matrix(m, 1)
    for i in range(m):
        suma = Fraction(0)
        for j in range(i):
            suma += L.array[i][j] * y.array[j][0]
        y.modify(i, 0, b_mat.array[i][0] - suma)
        pasos.append(f"  y_{i + 1} = {y.array[i][0]}")

    pasos.append("\nVector intermedio y:")
    pasos.append(str(y))

    # 2. Sustitución hacia atrás: Ux = y
    pasos.append("\n2. Sustitución hacia atrás: Resolver Ux = y para determinar la solución final x.")
    x = Matrix(n, 1)
    for i in range(n - 1, -1, -1):
        suma = Fraction(0)
        for j in range(i + 1, n):
            suma += U.array[i][j] * x.array[j][0]
        x_val = (y.array[i][0] - suma) / U.array[i][i]
        x.modify(i, 0, x_val)
        pasos.append(f"  x_{i + 1} = {x.array[i][0]}")

    pasos.append("\nVector solución x:")
    pasos.append(str(x))

    return y, x, "\n".join(pasos)