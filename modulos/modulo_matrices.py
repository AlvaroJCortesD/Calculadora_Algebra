"""
Módulo de Álgebra de Matrices.
Importa la lógica de determinantes del módulo respectivo.
"""
from fractions import Fraction
from modulos.modulo_determinantes import determinante_triangular, determinante_cofactores, matriz_cofactores

def fmt_val(val):
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"
    return str(val)

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

    def determinante_triangular(self):
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        return determinante_triangular(self.array)

    def determinante_cofactores(self):
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        return determinante_cofactores(self.array)

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

    def inversa(self):
        det = self.determinante_triangular()
        if det == 0:
            raise ValueError("La matriz es singular y no tiene inversa.")
        return self.adjunta().escalar_mult(Fraction(1) / det)