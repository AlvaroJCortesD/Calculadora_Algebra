"""
Módulo de Sistemas de Ecuaciones Lineales.
Resuelve sistemas Ax = b mediante Gauss-Jordan paso a paso en la matriz
aumentada [A | b] y mediante x = A⁻¹ · b.
"""
from fractions import Fraction
from modulos.modulo_matrices import Matrix, fmt_val


def format_augmented_system(aumentada, cols_A):
    """Formatea la matriz aumentada [A | b]."""
    lines = []
    for row in aumentada:
        parte_A = "  ".join(f"{fmt_val(num):>6}" for num in row[:cols_A])
        parte_b = "  ".join(f"{fmt_val(num):>6}" for num in row[cols_A:])
        lines.append(f"│ {parte_A}  │  {parte_b} │")
    return "\n".join(lines)


def resolver_sistema_gauss_jordan_paso_a_paso(A, b_mat):
    """
    Resuelve Ax = b usando Gauss-Jordan paso a paso en [A | b].
    Devuelve: (x_matriz_o_None, procedimiento_str)
    """
    if A.rows != b_mat.rows:
        raise ValueError(
            "El número de filas de A debe coincidir con el número de elementos de b."
        )

    m = A.rows
    n = A.columns

    # Construcción de la matriz aumentada [A | b]
    aumentada = []
    for i in range(m):
        fila = [Fraction(A.array[i][j]) for j in range(n)] + [
            Fraction(b_mat.array[i][0])
        ]
        aumentada.append(fila)

    pasos = [
        "======================================================",
        "   RESOLUCIÓN DE SISTEMA Ax = b POR GAUSS-JORDAN",
        "======================================================",
        "\nMatriz Aumentada Inicial [A | b]:",
        format_augmented_system(aumentada, n),
    ]

    fila_pivote_actual = 0
    pivotes_columnas = []

    for col in range(n):
        if fila_pivote_actual >= m:
            break

        sel_fila = None
        for r in range(fila_pivote_actual, m):
            if aumentada[r][col] != 0:
                sel_fila = r
                break

        if sel_fila is None:
            pasos.append(
                f"\nColumna {col + 1}: Sin pivote no nulo (Variable libre x_{col + 1})."
            )
            continue

        pasos.append(f"\n--- PASO COLUMNA {col + 1} ---")
        if sel_fila != fila_pivote_actual:
            aumentada[fila_pivote_actual], aumentada[sel_fila] = (
                aumentada[sel_fila],
                aumentada[fila_pivote_actual],
            )
            pasos.append(
                f"Intercambio: F{fila_pivote_actual + 1} <-> F{sel_fila + 1}"
            )
            pasos.append(format_augmented_system(aumentada, n))

        val_pivote = aumentada[fila_pivote_actual][col]
        if val_pivote != 1:
            pasos.append(
                f"Normalizar pivote en F{fila_pivote_actual + 1}: F{fila_pivote_actual + 1} -> F{fila_pivote_actual + 1} / ({val_pivote})"
            )
            for j in range(n + 1):
                aumentada[fila_pivote_actual][j] /= val_pivote
            pasos.append(format_augmented_system(aumentada, n))

        for r in range(m):
            if r != fila_pivote_actual:
                factor = aumentada[r][col]
                if factor != 0:
                    pasos.append(
                        f"Hacer cero en F{r + 1}: F{r + 1} -> F{r + 1} - ({factor}) * F{fila_pivote_actual + 1}"
                    )
                    for j in range(n + 1):
                        aumentada[r][j] -= factor * aumentada[fila_pivote_actual][j]

        pasos.append("Estado actual [A | b]:")
        pasos.append(format_augmented_system(aumentada, n))
        pivotes_columnas.append((fila_pivote_actual, col))
        fila_pivote_actual += 1

    # Detección de inconsistencias: [0 0 ... 0 | k] con k != 0
    inconsistente = False
    for r in range(m):
        es_cero_A = all(aumentada[r][j] == 0 for j in range(n))
        val_b = aumentada[r][n]
        if es_cero_A and val_b != 0:
            inconsistente = True
            pasos.append(
                f"\n[INCONSISTENCIA]: La fila {r + 1} indica la contradicción 0 = {val_b}."
            )
            break

    if inconsistente:
        pasos.append(
            "\n[DIAGNÓSTICO]: El sistema es INCONSISTENTE (No tiene solución)."
        )
        return None, "\n".join(pasos)

    num_pivotes = len(pivotes_columnas)
    if num_pivotes < n:
        pasos.append(
            f"\n[DIAGNÓSTICO]: El sistema es CONSISTENTE INDETERMINADO (Infinitas soluciones)."
        )
        pasos.append(
            f"Número de pivotes = {num_pivotes}, Número de variables = {n}."
        )
        pasos.append(f"Variables libres = {n - num_pivotes}.")
        return None, "\n".join(pasos)

    # Solución única
    x = Matrix(n, 1)
    for r, c in pivotes_columnas:
        x.modify(c, 0, aumentada[r][n])

    pasos.append(
        "\n[DIAGNÓSTICO]: El sistema es CONSISTENTE DETERMINADO (Solución única):"
    )
    for j in range(n):
        pasos.append(f"  x_{j + 1} = {x.array[j][0]}")

    pasos.append("\nVector solución x:")
    pasos.append(str(x))

    return x, "\n".join(pasos)


def resolver_sistema_inversa_paso_a_paso(A, b_mat):
    """
    Resuelve Ax = b mediante x = A⁻¹ · b.
    Devuelve: (x_matriz, procedimiento_str)
    """
    if A.rows != A.columns:
        raise ValueError(
            "La matriz A debe ser cuadrada (n x n) para resolver mediante matriz inversa."
        )
    if A.rows != b_mat.rows:
        raise ValueError("Las dimensiones de A y b no son compatibles.")

    pasos = [
        "======================================================",
        "   RESOLUCIÓN DE SISTEMA Ax = b POR MATRIZ INVERSA",
        "   Fórmula: x = A⁻¹ · b",
        "======================================================",
    ]

    inv_A, pas_inv = A.inversa_gauss_jordan_paso_a_paso()
    pasos.append(pas_inv)

    x = inv_A.multiplicar(b_mat)
    pasos.append("\n--- MULTIPLICACIÓN x = A⁻¹ · b ---")
    pasos.append(f"A⁻¹ · b =\n{x}")

    pasos.append("\nSolución del sistema:")
    for j in range(x.rows):
        pasos.append(f"  x_{j + 1} = {x.array[j][0]}")

    return x, "\n".join(pasos)