"""
Módulo de Determinantes con Procedimiento Paso a Paso.
Contiene algoritmos para reducción triangular, expansión por cofactores y Regla de Sarrus.
"""
from fractions import Fraction


def menor_array(array, fila, columna):
    """Devuelve la submatriz eliminando una fila y columna."""
    n = len(array)
    return [[array[i][j] for j in range(n) if j != columna] for i in range(n) if i != fila]


def determinante_cofactores(array):
    """Cálculo directo del determinante por cofactores."""
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


def determinante_cofactores_paso_a_paso(array):
    """Devuelve (det, procedimiento_str) desglosando la expansión por cofactores."""
    n = len(array)
    pasos = ["--- EXPANSIÓN POR COFACTORES (Fila 1) ---"]

    if n == 1:
        det = Fraction(array[0][0])
        pasos.append(f"Matriz 1x1: det = {det}")
        return det, "\n".join(pasos)

    if n == 2:
        a, b = Fraction(array[0][0]), Fraction(array[0][1])
        c, d = Fraction(array[1][0]), Fraction(array[1][1])
        det = a * d - b * c
        pasos.append(f"Fórmula 2x2: ({a})*({d}) - ({b})*({c}) = {det}")
        return det, "\n".join(pasos)

    det = Fraction(0)
    terminos = []
    for j in range(n):
        signo = Fraction(1) if j % 2 == 0 else Fraction(-1)
        val_elem = Fraction(array[0][j])
        sub_mat = menor_array(array, 0, j)
        sub_det = determinante_cofactores(sub_mat)

        signo_str = "+" if signo > 0 else "-"
        pasos.append(
            f"  A[1][{j + 1}] = {val_elem}: Coeficiente = {signo_str}({val_elem}) * det(Menor_1,{j + 1}) = {signo * val_elem * sub_det}")
        det += signo * val_elem * sub_det
        terminos.append(f"({signo * val_elem * sub_det})")

    pasos.append(f"\nSuma de cofactores: {' + '.join(terminos)} = {det}")
    return det, "\n".join(pasos)


def determinante_sarrus_paso_a_paso(array):
    """Devuelve (det, procedimiento_str) usando la Regla de Sarrus para matrices 3x3."""
    n = len(array)
    if n != 3:
        raise ValueError("La regla de Sarrus solo es aplicable a matrices cuadradas de 3x3.")

    pasos = ["--- DETERMINANTE POR REGLA DE SARRUS (3x3) ---"]

    # Diagonales principales
    dp1 = Fraction(array[0][0]) * Fraction(array[1][1]) * Fraction(array[2][2])
    dp2 = Fraction(array[0][1]) * Fraction(array[1][2]) * Fraction(array[2][0])
    dp3 = Fraction(array[0][2]) * Fraction(array[1][0]) * Fraction(array[2][1])
    suma_dp = dp1 + dp2 + dp3

    pasos.append("\nDiagonales principales (+):")
    pasos.append(f"  ({array[0][0]}) * ({array[1][1]}) * ({array[2][2]}) = {dp1}")
    pasos.append(f"  ({array[0][1]}) * ({array[1][2]}) * ({array[2][0]}) = {dp2}")
    pasos.append(f"  ({array[0][2]}) * ({array[1][0]}) * ({array[2][1]}) = {dp3}")
    pasos.append(f"  Suma (+) = {suma_dp}")

    # Diagonales secundarias
    ds1 = Fraction(array[0][2]) * Fraction(array[1][1]) * Fraction(array[2][0])
    ds2 = Fraction(array[0][0]) * Fraction(array[1][2]) * Fraction(array[2][1])
    ds3 = Fraction(array[0][1]) * Fraction(array[1][0]) * Fraction(array[2][2])
    suma_ds = ds1 + ds2 + ds3

    pasos.append("\nDiagonales secundarias (-):")
    pasos.append(f"  ({array[0][2]}) * ({array[1][1]}) * ({array[2][0]}) = {ds1}")
    pasos.append(f"  ({array[0][0]}) * ({array[1][2]}) * ({array[2][1]}) = {ds2}")
    pasos.append(f"  ({array[0][1]}) * ({array[1][0]}) * ({array[2][2]}) = {ds3}")
    pasos.append(f"  Suma (-) = {suma_ds}")

    det = suma_dp - suma_ds
    pasos.append(f"\nCálculo final: {suma_dp} - ({suma_ds}) = {det}")

    return det, "\n".join(pasos)


def determinante_triangular_paso_a_paso(array):
    """Devuelve (det, procedimiento_str) mediante reducción a forma triangular."""
    n = len(array)
    temp = [[Fraction(array[i][j]) for j in range(n)] for i in range(n)]
    pasos = ["--- REDUCCIÓN A FORMA TRIANGULAR ---"]
    intercambios = 0

    for i in range(n):
        pasos.append(f"\n[ Columna {i + 1} ]")
        if temp[i][i] == 0:
            pivote_encontrado = False
            for k in range(i + 1, n):
                if temp[k][i] != 0:
                    temp[i], temp[k] = temp[k], temp[i]
                    intercambios += 1
                    pivote_encontrado = True
                    pasos.append(f"  Intercambio Fila {i + 1} <-> Fila {k + 1} (el signo del det cambia)")
                    break
            if not pivote_encontrado:
                pasos.append(f"  Columna {i + 1} sin pivote ≠ 0 -> det = 0")
                return Fraction(0), "\n".join(pasos)

        pivote = temp[i][i]
        pasos.append(f"  Pivote en A[{i + 1}][{i + 1}] = {pivote}")
        for j in range(i + 1, n):
            if temp[j][i] != 0:
                factor = temp[j][i] / temp[i][i]
                pasos.append(f"  Operación de fila: F{j + 1} -> F{j + 1} - ({factor}) * F{i + 1}")
                for k in range(i, n):
                    temp[j][k] -= factor * temp[i][k]

    prod_diag = Fraction(1)
    diag_vals = []
    for i in range(n):
        prod_diag *= temp[i][i]
        diag_vals.append(str(temp[i][i]))

    pasos.append(f"\nDiagonal principal: {', '.join(diag_vals)}")
    pasos.append(f"Producto diagonal: {' * '.join(diag_vals)} = {prod_diag}")

    if intercambios > 0:
        det = prod_diag * (Fraction(-1) ** intercambios)
        pasos.append(f"Ajuste por {intercambios} intercambio(s): det = {det}")
    else:
        det = prod_diag

    return det, "\n".join(pasos)


def matriz_cofactores(array):
    """Calcula la matriz de cofactores."""
    n = len(array)
    cof = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
            cof[i][j] = signo * determinante_cofactores(menor_array(array, i, j))
    return cof