"""
Módulo de Determinantes con Procedimiento Paso a Paso.
Contiene algoritmos para reducción triangular y expansión por cofactores.
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
        det = a*d - b*c
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
        pasos.append(f"  Elemento A[1][{j+1}] = {val_elem}: Coeficiente = {signo_str}({val_elem}) * det(Menor_1,{j+1}) = {signo * val_elem * sub_det}")
        det += signo * val_elem * sub_det
        terminos.append(f"({signo * val_elem * sub_det})")

    pasos.append(f"\nSuma de cofactores: {' + '.join(terminos)} = {det}")
    return det, "\n".join(pasos)

def determinante_triangular_paso_a_paso(array):
    """Devuelve (det, procedimiento_str) mediante reducción a forma triangular."""
    n = len(array)
    temp = [[Fraction(array[i][j]) for j in range(n)] for i in range(n)]
    pasos = ["--- REDUCCIÓN A FORMA TRIANGULAR ---"]

    intercambios = 0

    for i in range(n):
        pasos.append(f"\n[ Columna {i+1} ]")
        if temp[i][i] == 0:
            pivote_encontrado = False
            for k in range(i + 1, n):
                if temp[k][i] != 0:
                    temp[i], temp[k] = temp[k], temp[i]
                    intercambios += 1
                    pivote_encontrado = True
                    pasos.append(f"  Intercambio Fila {i+1} <-> Fila {k+1} (el signo del det cambia)")
                    break
            if not pivote_encontrado:
                pasos.append(f"  Columna {i+1} sin pivote ≠ 0 -> det = 0")
                return Fraction(0), "\n".join(pasos)

        pivote = temp[i][i]
        pasos.append(f"  Pivote en A[{i+1}][{i+1}] = {pivote}")

        for j in range(i + 1, n):
            if temp[j][i] != 0:
                factor = temp[j][i] / temp[i][i]
                pasos.append(f"  Operación de fila: F{j+1} -> F{j+1} - ({factor}) * F{i+1}")
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
        pasos.append(f"Ajuste por {intercambios} intercambio(s) de fila: det = {det}")
    else:
        det = prod_diag

    return det, "\n".join(pasos)

def matriz_cofactores(array):
    """Calcula la matriz de cofactores."""
    n = len(array)
    if n == 1:
        # El menor de una matriz 1x1 es el determinante de la matriz vacía (= 1).
        return [[Fraction(1)]]
    cof = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
            cof[i][j] = signo * determinante_cofactores(menor_array(array, i, j))
    return cof

def _fmt(v):
    v = Fraction(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"

def _fmt_sub(sub):
    """Submatriz en una sola línea, ej. [ 1  2 ; 3  4 ]."""
    return "[ " + " ; ".join("  ".join(_fmt(x) for x in fila) for fila in sub) + " ]"

def _fmt_bloque(array):
    return "\n".join("│ " + "  ".join(f"{_fmt(x):>6}" for x in fila) + " │" for fila in array)

def _det_2x2_texto(sub):
    a, b, c, d = (Fraction(sub[0][0]), Fraction(sub[0][1]),
                  Fraction(sub[1][0]), Fraction(sub[1][1]))
    return f"({_fmt(a)})*({_fmt(d)}) - ({_fmt(b)})*({_fmt(c)})"

def matriz_menores(array):
    """Matriz de menores: M[i][j] = det(submatriz sin fila i ni columna j)."""
    n = len(array)
    if n < 2:
        raise ValueError("Los menores requieren una matriz de al menos 2x2.")
    return [[determinante_cofactores(menor_array(array, i, j)) for j in range(n)]
            for i in range(n)]

def menores_paso_a_paso(array):
    """Devuelve (matriz_menores, procedimiento_str)."""
    n = len(array)
    if n < 2:
        raise ValueError("Los menores requieren una matriz de al menos 2x2.")
    pasos = [
        "======================================================",
        "   MATRIZ DE MENORES  M_ij",
        "   M_ij = det de la submatriz que resulta de eliminar",
        "   la fila i y la columna j de A",
        "======================================================",
    ]
    menores = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sub = menor_array(array, i, j)
            m = determinante_cofactores(sub)
            menores[i][j] = m
            pasos.append(f"\nM{i+1}{j+1}: se elimina fila {i+1} y columna {j+1}")
            pasos.append(_fmt_bloque(sub))
            if n == 2:
                pasos.append(f"  det = {_fmt(sub[0][0])} = {_fmt(m)}")
            elif n == 3:
                pasos.append(f"  det = {_det_2x2_texto(sub)} = {_fmt(m)}")
            else:
                pasos.append(f"  det = {_fmt(m)}")
    pasos.append("\n--- MATRIZ DE MENORES M ---")
    pasos.append(_fmt_bloque(menores))
    return menores, "\n".join(pasos)

def cofactores_paso_a_paso(array):
    """Devuelve (matriz_cofactores, procedimiento_str) con cada C_ij."""
    n = len(array)
    if n < 2:
        raise ValueError("Los cofactores requieren una matriz de al menos 2x2.")
    pasos = [
        "======================================================",
        "   MATRIZ DE COFACTORES  C_ij",
        "   C_ij = (-1)^(i+j) · M_ij",
        "======================================================",
    ]
    cof = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sub = menor_array(array, i, j)
            m = determinante_cofactores(sub)
            signo = 1 if (i + j) % 2 == 0 else -1
            c = signo * m
            cof[i][j] = c
            pasos.append(f"\nC{i+1}{j+1} = (-1)^({i+1}+{j+1}) · M{i+1}{j+1}")
            pasos.append(f"  Submatriz (sin fila {i+1}, col {j+1}): {_fmt_sub(sub)}")
            if n == 3:
                pasos.append(f"  M{i+1}{j+1} = {_det_2x2_texto(sub)} = {_fmt(m)}")
            else:
                pasos.append(f"  M{i+1}{j+1} = {_fmt(m)}")
            pasos.append(f"  C{i+1}{j+1} = ({signo:+d}) · ({_fmt(m)}) = {_fmt(c)}")
    pasos.append("\n--- MATRIZ DE COFACTORES C ---")
    pasos.append(_fmt_bloque(cof))
    return cof, "\n".join(pasos)