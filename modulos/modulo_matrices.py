"""
Módulo de Álgebra de Matrices.
Implementa operaciones, Gauss-Jordan paso a paso e Inversa por Adjunta.
"""
from fractions import Fraction
from modulos.modulo_determinantes import (
    determinante_triangular_paso_a_paso,
    determinante_cofactores_paso_a_paso,
    matriz_cofactores
)

def fmt_val(val):
    """Formatea valores como enteros o fracciones."""
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"
    return str(val)

def format_augmented_matrix(aumentada, n):
    """Formatea visualmente la matriz aumentada [A | I]."""
    lines = []
    for row in aumentada:
        parte_A = "  ".join(f"{fmt_val(num):>6}" for num in row[:n])
        parte_I = "  ".join(f"{fmt_val(num):>6}" for num in row[n:])
        lines.append(f"│ {parte_A}  │  {parte_I} │")
    return "\n".join(lines)

class Matrix:
    def __init__(self, rows, columns, valor_inicial=0):
        self.rows = rows
        self.columns = columns
        self.array = [[valor_inicial for _ in range(columns)] for _ in range(rows)]

    def modify(self, rows, columns, new_value):
        self.array[rows][columns] = new_value

    def __str__(self):
        lines = []
        for row in self.array:
            parte = "  ".join(f"{fmt_val(num):>6}" for num in row)
            lines.append(f"│ {parte} │")
        return "\n".join(lines)

    def sumar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(self.array[i][j]) + Fraction(B.array[i][j]))
        return res

    def restar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(self.array[i][j]) - Fraction(B.array[i][j]))
        return res

    def escalar_mult(self, c):
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(c) * Fraction(self.array[i][j]))
        return res

    def multiplicar(self, B):
        if self.columns != B.rows:
            raise ValueError(f"Columnas de A ({self.columns}) ≠ Filas de B ({B.rows}).")
        res = Matrix(self.rows, B.columns)
        for i in range(self.rows):
            for j in range(B.columns):
                suma = Fraction(0)
                for k in range(self.columns):
                    suma += (Fraction(self.array[i][k]) * Fraction(B.array[k][j]))
                res.modify(i, j, suma)
        return res

    def traspuesta(self):
        res = Matrix(self.columns, self.rows)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(j, i, self.array[i][j])
        return res

    def determinante_triangular_paso_a_paso(self):
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        return determinante_triangular_paso_a_paso(self.array)

    def determinante_cofactores_paso_a_paso(self):
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        return determinante_cofactores_paso_a_paso(self.array)

    def adjunta(self):
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        cof_array = matriz_cofactores(self.array)
        n = self.rows
        cof_matrix = Matrix(n, n)
        for i in range(n):
            for j in range(n):
                cof_matrix.modify(i, j, cof_array[i][j])
        return cof_matrix.traspuesta()

    def inversa_gauss_jordan_paso_a_paso(self):
        """Calcula la inversa reduciendo la matriz aumentada [A | I] paso a paso."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada para calcular su inversa.")

        n = self.rows
        pasos = [
            "======================================================",
            "   INVERSA POR GAUSS-JORDAN EN MATRIZ AUMENTADA [A | I]",
            "======================================================"
        ]

        aumentada = []
        for i in range(n):
            fila = [Fraction(self.array[i][j]) for j in range(n)] + [Fraction(1) if i == j else Fraction(0) for j in range(n)]
            aumentada.append(fila)

        pasos.append("\nMatriz Aumentada Inicial [A | I]:")
        pasos.append(format_augmented_matrix(aumentada, n))

        for columna in range(n):
            pasos.append(f"\n--- PASO COLUMNA {columna + 1} ---")

            fila_pivote = None
            for fila in range(columna, n):
                if aumentada[fila][columna] != 0:
                    fila_pivote = fila
                    break

            if fila_pivote is None:
                pasos.append(f"ERROR: Sin pivote en columna {columna + 1}. La matriz es SINGULAR.")
                raise ValueError("La matriz es singular (det = 0) y no tiene inversa.")

            if fila_pivote != columna:
                aumentada[columna], aumentada[fila_pivote] = aumentada[fila_pivote], aumentada[columna]
                pasos.append(f"Intercambio de filas: F{columna + 1} <-> F{fila_pivote + 1}")
                pasos.append(format_augmented_matrix(aumentada, n))

            pivote = aumentada[columna][columna]
            if pivote != 1:
                pasos.append(f"Convertir pivote a 1 en F{columna + 1}: F{columna + 1} -> F{columna + 1} / ({pivote})")
                for j in range(2 * n):
                    aumentada[columna][j] /= pivote
                pasos.append(format_augmented_matrix(aumentada, n))

            for fila in range(n):
                if fila != columna:
                    factor = aumentada[fila][columna]
                    if factor != 0:
                        pasos.append(f"Hacer cero en F{fila + 1}: F{fila + 1} -> F{fila + 1} - ({factor}) * F{columna + 1}")
                        for j in range(2 * n):
                            aumentada[fila][j] -= factor * aumentada[columna][j]

            pasos.append("Estado actual [I | A⁻¹]:")
            pasos.append(format_augmented_matrix(aumentada, n))

        inversa = Matrix(n, n)
        for i in range(n):
            for j in range(n):
                inversa.modify(i, j, aumentada[i][j + n])

        pasos.append("\nMatriz Inversa Obtenida A⁻¹:")
        pasos.append(str(inversa))

        pasos.append("\n--- COMPROBACIÓN AUTOMÁTICA A · A⁻¹ = I ---")
        comprobacion = self.multiplicar(inversa)
        pasos.append(str(comprobacion))
        pasos.append("\nDiagnóstico: La matriz es invertible (det ≠ 0), tiene n posiciones pivote, sus columnas son L.I. y generan R^n.")

        return inversa, "\n".join(pasos)

    def inversa_adjunta_paso_a_paso(self):
        """Calcula la inversa con la fórmula A^-1 = (1/det(A)) * adj(A)."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")

        pasos = [
            "======================================================",
            "   INVERSA POR MATRIZ ADJUNTA A⁻¹ = (1/det(A)) · adj(A)",
            "======================================================"
        ]

        det, pas_det = determinante_triangular_paso_a_paso(self.array)
        pasos.append(pas_det)

        if det == 0:
            pasos.append("\nDiagnóstico: La matriz es singular (det = 0), no tiene inversa.")
            raise ValueError("La matriz es singular (det = 0), no tiene inversa.")

        adj = self.adjunta()
        pasos.append("\n--- MATRIZ ADJUNTA adj(A) ---")
        pasos.append(str(adj))

        inversa = adj.escalar_mult(Fraction(1) / det)
        pasos.append(f"\n--- CÁLCULO A⁻¹ = (1 / {det}) · adj(A) ---")
        pasos.append(str(inversa))

        pasos.append("\n--- COMPROBACIÓN AUTOMÁTICA A · A⁻¹ = I ---")
        comprobacion = self.multiplicar(inversa)
        pasos.append(str(comprobacion))
        pasos.append("\nDiagnóstico: La matriz es invertible (det ≠ 0), tiene n posiciones pivote, sus columnas son L.I. y generan R^n.")

        return inversa, "\n".join(pasos)

    def inversa(self):
        inv, _ = self.inversa_gauss_jordan_paso_a_paso()
        return inv