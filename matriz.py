#! /usr/bin/env python3
from fractions import Fraction



# Función auxiliar para convertir números normales a subíndices Unicode (ej: 1 -> ₁ , 2 -> ₂)
def to_subscript(number):
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(subscripts)


# Función auxiliar para solicitar entrada al usuario (soporta enteros, decimales y fracciones como '1/3')
def asking_for_input(message, type=float):
    while True:
        info = input(message.strip())
        try:
            if type == int:
                return int(info)
            valor = Fraction(info)
            if valor.denominator == 1:
                return valor.numerator
            return valor
        except ValueError:
            print(
                "Entrada invalida. Por favor, ingresa un numero entero, decimal o fraccion (ej: 3, 0.5 o 1/3)."
            )


# Función auxiliar para dar formato de texto a cada elemento
def fmt_val(val):
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return f"{val.numerator:6}"
        return f"{val.numerator}/{val.denominator}":>6
    elif isinstance(val, float):
        frac = Fraction(val).limit_denominator(1000)
        if frac.denominator == 1:
            return f"{frac.numerator:6}"
        return f"{frac.numerator}/{frac.denominator}":>6
    return f"{val:6}"


# Función auxiliar para formatear una matriz en un único bloque de corchetes
def format_matrix(matriz_datos):
    lines = []
    for row in matriz_datos:
        datos_A = row[:-1]  # Coeficientes
        valor_b = row[-1]  # Término independiente

        parte_A = "  ".join(fmt_val(num) for num in datos_A)
        fmt_b = fmt_val(valor_b)

        lines.append(f"{parte_A}  │  {fmt_b}")

    n = len(lines)
    resultado = []

    for i, line in enumerate(lines):
        if n == 1:
            resultado.append(f"[ {line} ]")
        elif i == 0:
            resultado.append(f"┌ {line} ┐")
        elif i == n - 1:
            resultado.append(f"└ {line} ┘")
        else:
            resultado.append(f"│ {line} │")

    return "\n".join(resultado)


# Clase que representa una matriz matemática y sus operaciones
class Matrix:

    def __init__(self, rows, columns, valor_inicial=0):
        self.rows = rows
        self.columns = columns
        self.array = [
            [valor_inicial for _ in range(columns)] for _ in range(rows)
        ]

    def add_vector_b(self, vector_b):
        if len(vector_b) != self.rows:
            raise ValueError(
                "El numero de elementos de vector b debe ser igual al numero de filas"
            )

        for i in range(self.rows):
            self.array[i].append(vector_b[i])

        self.columns += 1

    def modify(self, rows, columns, new_value):
        self.array[rows][columns] = new_value

    def gauss_jordan(self):
        n_equations = self.rows
        clone = [[Fraction(val) for val in row] for row in self.array]

        def imprimir_paso(matriz_clon):
            print(format_matrix(matriz_clon))
            print("-" * 50)

        print("\n=== INICIANDO REDUCCIÓN GAUSS-JORDAN ===")
        print("Transformando la matriz a la FORMA ESCALONADA REDUCIDA...")

        for c in range(n_equations):
            print(f"\nProcesando Columna {c + 1}:")

            # 1. Pivoteo parcial
            max_row = c
            for r in range(c + 1, n_equations):
                if abs(clone[r][c]) > abs(clone[max_row][c]):
                    max_row = r

            if max_row != c:
                clone[c], clone[max_row] = clone[max_row], clone[c]
                print(
                    f"-> Se intercambió la fila {c + 1} con la fila {max_row + 1} (Pivoteo Parcial):"
                )
                imprimir_paso(clone)

            # Verificación de pivote nulo / inconsistencia
            if clone[c][c] == 0:
                coeficientes_cero = all(val == 0 for val in clone[c][:-1])
                termino_independiente = clone[c][-1]

                print(
                    "\n================ RESULTADO DEL ANÁLISIS ================"
                )
                if coeficientes_cero and termino_independiente != 0:
                    print("TIPO DE SISTEMA: INCONSISTENTE")
                    print(
                        "CANTIDAD DE SOLUCIONES: Sin solución (0 soluciones)."
                    )
                    print(
                        "RAZÓN: Se obtuvo una contradicción matemática del tipo [ 0 0 ... 0 │ k ] con k ≠ 0."
                    )
                else:
                    print("TIPO DE SISTEMA: CONSISTENTE INDETERMINADO")
                    print("CANTIDAD DE SOLUCIONES: Infinitas soluciones.")
                    print(
                        "RAZÓN: Existe al menos una variable libre en el sistema."
                    )
                print(
                    "========================================================\n"
                )
                return None

            # 2. Hacer el pivote igual a 1
            pivot = clone[c][c]
            for j in range(c, len(clone[c])):
                clone[c][j] /= pivot
            print(
                f"-> Fila {c + 1} dividida entre su pivote ({pivot}) para obtener el 1 principal:"
            )
            imprimir_paso(clone)

            # 3. Hacer ceros en el resto de la columna
            for f in range(n_equations):
                if f != c:
                    factor = clone[f][c]
                    for j in range(c, len(clone[f])):
                        clone[f][j] -= factor * clone[c][j]

            print(
                f"-> Ceros generados arriba y abajo del pivote de la columna {c + 1}:"
            )
            imprimir_paso(clone)

        print("\n=== PROCESO DE REDUCCIÓN FINALIZADO ===")
        print(
            "ESTADO DE LA MATRIZ: La matriz se encuentra en FORMA ESCALONADA REDUCIDA POR FILAS."
        )

        answers = []
        for row in clone:
            val = row[-1]
            if isinstance(val, Fraction) and val.denominator == 1:
                answers.append(val.numerator)
            else:
                answers.append(val)

        print("\n================ RESULTADO DEL ANÁLISIS ================")
        print("TIPO DE SISTEMA: CONSISTENTE DETERMINADO")
        print("CANTIDAD DE SOLUCIONES: Solución ÚNICA.")
        print("========================================================\n")

        return answers

    def __str__(self):
        return format_matrix(self.array)


# Comprobación automática
def verificar_solucion(matriz_original, vector_b, soluciones):
    for i in range(len(matriz_original)):
        suma = sum(
            Fraction(matriz_original[i][j]) * Fraction(soluciones[j])
            for j in range(len(soluciones))
        )
        if suma != Fraction(vector_b[i]):
            print(f"⚠️ Alerta: La solución no satisface la ecuación {i + 1}")
            return False

    print(
        "✅ Solución verificada con éxito sustituyendo en el sistema original."
    )
    return True