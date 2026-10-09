"""
Módulo de Determinantes.
Contiene los algoritmos para calcular determinantes por expansión
de cofactores, reducción triangular y generación de matriz de cofactores.
"""
from fractions import Fraction


def menor_array(array, fila, columna):
    n = len(array)
    return [[array[i][j] for j in range(n) if j != columna] for i in range(n) if i != fila]


def determinante_cofactores(array):
    n = len(array)
    if n == 1:
        return Fraction(array[0][0])
    if n == 2:
        return (Fraction(array[0][0]) * Fraction(array[1][1]) -
                Fraction(array[0][1]) * Fraction(array[1][0]))

    det = Fraction(0)
    for j in range(n):
        signo = Fraction(1) if j % 2 == 0 else Fraction(-1)
        det += signo * Fraction(array[0][j]) * determinante_cofactores(menor_array(array, 0, j))
    return det


def determinante_triangular(array):
    n = len(array)
    temp = [[Fraction(array[i][j]) for j in range(n)] for i in range(n)]
    det = Fraction(1)
    intercambios = 0

    for i in range(n):
        if temp[i][i] == 0:
            pivote = False
            for k in range(i + 1, n):
                if temp[k][i] != 0:
                    temp[i], temp[k] = temp[k], temp[i]
                    intercambios += 1
                    pivote = True
                    break
            if not pivote:
                return Fraction(0)

        for j in range(i + 1, n):
            factor = temp[j][i] / temp[i][i]
            for k in range(i, n):
                temp[j][k] -= factor * temp[i][k]

    for i in range(n):
        det *= temp[i][i]

    if intercambios % 2 != 0:
        det *= Fraction(-1)

    return det


def matriz_cofactores(array):
    n = len(array)
    cof = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
            cof[i][j] = signo * determinante_cofactores(menor_array(array, i, j))
    return cof