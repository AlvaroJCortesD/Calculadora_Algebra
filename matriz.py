#! /usr/bin/env python3
from fractions import Fraction

# Convierte números enteros a subíndices en formato Unicode (ej: 1 -> ₁).
def to_subscript(number):
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(subscripts)

# Solicita entrada al usuario permitiendo enteros, decimales y fracciones (ej: 1/3).
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
            print("Entrada invalida. Por favor, ingresa un numero entero, decimal o fraccion (ej: 3, 0.5 o 1/3).")

# Formatea valores numéricos para mantener alineación de columnas al imprimir.
def fmt_val(val):
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return f"{val.numerator:6}"
        texto = f"{val.numerator}/{val.denominator}"
        return f"{texto:>6}"
    elif isinstance(val, float):
        frac = Fraction(val).limit_denominator(1000)
        if frac.denominator == 1:
            return f"{frac.numerator:6}"
        texto = f"{frac.numerator}/{frac.denominator}"
        return f"{texto:>6}"
    return f"{val:6}"

# Genera una representación en texto con bordes y línea divisoria para matriz aumentada [A|b].
def format_matrix(matriz_datos):
    lines = []
    for row in matriz_datos:
        datos_A = row[:-1]
        valor_b = row[-1]
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

# Realiza la suma componente a componente entre dos vectores u + v de R^n.
def sumar_vectores(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [Fraction(u[i]) + Fraction(v[i]) for i in range(len(u))]

# Realiza la resta componente a componente entre dos vectores u - v de R^n.
def restar_vectores(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [Fraction(u[i]) - Fraction(v[i]) for i in range(len(u))]

# Multiplica un escalar c por cada componente de un vector v.
def escalar_por_vector(c, v):
    return [Fraction(c) * Fraction(x) for x in v]

# Evalúa mediante Gauss-Jordan si el vector b se puede expresar como combinación lineal del conjunto.
def es_combinacion_lineal(conjunto_vectores, b):
    m = len(b)
    k = len(conjunto_vectores)
    mat = Matrix(m, k)
    for j in range(k):
        if len(conjunto_vectores[j]) != m:
            raise ValueError("Todos los vectores deben tener la misma dimensión que b.")
        for i in range(m):
            mat.modify(i, j, conjunto_vectores[j][i])
    
    mat.add_vector_b(b)
    _, _, _, soluciones, forma_vectorial = mat.gauss_jordan()
    return (soluciones is not None or forma_vectorial is not None)

# Clase para representar y realizar operaciones sobre matrices rectangulares de m x n.
class Matrix:
    # Inicializa una matriz de tamaño rows x columns rellena con un valor inicial.
    def __init__(self, rows, columns, valor_inicial=0):
        self.rows = rows
        self.columns = columns
        self.array = [[valor_inicial for _ in range(columns)] for _ in range(rows)]

    # Anexa el vector columna b a la derecha para transformar la matriz en [A|b].
    def add_vector_b(self, vector_b):
        if len(vector_b) != self.rows:
            raise ValueError("El numero de elementos de vector b debe ser igual al numero de filas")
        for i in range(self.rows):
            self.array[i].append(vector_b[i])
        self.columns += 1

    # Modifica el valor almacenado en una posición específica (fila, columna) de la matriz.
    def modify(self, rows, columns, new_value):
        self.array[rows][columns] = new_value

    # Retorna la representación en texto de la matriz estándar encerrada entre corchetes.
    def __str__(self):
        lines = []
        for row in self.array:
            parte = "  ".join(fmt_val(num) for num in row)
            lines.append(f"│ {parte} │")
        return "\n".join(lines)

    # Realiza la suma elemento a elemento entre la matriz actual y B (A + B).
    def sumar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Incompatibilidad de dimensiones: Las matrices deben ser de igual tamaño (m x n).")
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(self.array[i][j]) + Fraction(B.array[i][j]))
        return res

    # Realiza la resta elemento a elemento entre la matriz actual y B (A - B).
    def restar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Incompatibilidad de dimensiones: Las matrices deben ser de igual tamaño (m x n).")
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(self.array[i][j]) - Fraction(B.array[i][j]))
        return res

    # Multiplica cada entrada de la matriz por una constante escalar c.
    def escalar_mult(self, c):
        res = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                res.modify(i, j, Fraction(c) * Fraction(self.array[i][j]))
        return res

    # Calcula el producto matricial A * B mediante un algoritmo de 3 bucles anidados (i-j-k).
    def multiplicar(self, B):
        if self.columns != B.rows:
            raise ValueError(f"Incompatibilidad de dimensiones: Columnas de A ({self.columns}) ≠ Filas de B ({B.rows}).")
        
        res = Matrix(self.rows, B.columns)
        for i in range(self.rows):
            for j in range(B.columns):
                suma = Fraction(0)
                for k in range(self.columns):
                    suma += Fraction(self.array[i][k]) * Fraction(B.array[k][j])
                res.modify(i, j, suma)
        return res

    # Ejecuta la reducción por filas de Gauss-Jordan imprimiendo el procedimiento paso a paso.
    def gauss_jordan(self):
        m_filas = self.rows
        n_variables = self.columns - 1
        clone = [[Fraction(val) for val in row] for row in self.array]

        # Muestra en consola el estado actual de la matriz durante cada transformación.
        def imprimir_paso(matriz_clon):
            print(format_matrix(matriz_clon))
            print("-" * 50)

        print("\n=== INICIANDO REDUCCIÓN GAUSS-JORDAN ===")
        print("Transformando la matriz a la FORMA ESCALONADA REDUCIDA...")

        columnas_pivote = []
        fila_pivote = 0

        for c in range(n_variables):
            if fila_pivote >= m_filas:
                break

            print(f"\nProcesando Columna {c + 1}:")
            max_row = fila_pivote
            for r in range(fila_pivote + 1, m_filas):
                if abs(clone[r][c]) > abs(clone[max_row][c]):
                    max_row = r

            if clone[max_row][c] == 0:
                print(f"-> La columna {c + 1} no tiene pivote (variable libre).")
                continue

            if max_row != fila_pivote:
                clone[fila_pivote], clone[max_row] = clone[max_row], clone[fila_pivote]
                print(f"-> Se intercambió la fila {fila_pivote + 1} con la fila {max_row + 1} (Pivoteo Parcial):")
                imprimir_paso(clone)

            pivot = clone[fila_pivote][c]
            for j in range(self.columns):
                clone[fila_pivote][j] /= pivot
            print(f"-> Fila {fila_pivote + 1} dividida entre su pivote ({pivot}) para obtener el 1 principal:")
            imprimir_paso(clone)

            for f in range(m_filas):
                if f != fila_pivote:
                    factor = clone[f][c]
                    for j in range(self.columns):
                        clone[f][j] -= factor * clone[fila_pivote][j]

            print(f"-> Ceros generados arriba y abajo del pivote de la columna {c + 1}:")
            imprimir_paso(clone)

            columnas_pivote.append(c)
            fila_pivote += 1

        print("\n=== PROCESO DE REDUCCIÓN FINALIZADO ===")
        print("ESTADO DE LA MATRIZ: La matriz se encuentra en FORMA ESCALONADA REDUCIDA POR FILAS.")

        variables_libres = [col for col in range(n_variables) if col not in columnas_pivote]

        inconsistente = False
        for row in clone:
            if all(val == 0 for val in row[:-1]) and row[-1] != 0:
                inconsistente = True
                break

        print("\n================ RESULTADO DEL ANÁLISIS ================")
        if inconsistente:
            print("TIPO DE SISTEMA: INCONSISTENTE")
            print("CANTIDAD DE SOLUCIONES: Sin solución (0 soluciones).")
            print("RAZÓN: Se obtuvo una contradicción del tipo [ 0 0 ... 0 │ k ] con k ≠ 0.")
            print("========================================================\n")
            return clone, columnas_pivote, variables_libres, None, None

        elif len(variables_libres) > 0:
            print("TIPO DE SISTEMA: CONSISTENTE INDETERMINADO")
            print("CANTIDAD DE SOLUCIONES: Infinitas soluciones.")
            print("RAZÓN: Existe al menos una variable libre en el sistema.\n")

            v_particular = [Fraction(0)] * n_variables
            v_direccionales = {lib: [Fraction(0)] * n_variables for lib in variables_libres}

            for lib in variables_libres:
                v_direccionales[lib][lib] = Fraction(1)

            for idx, p in enumerate(columnas_pivote):
                v_particular[p] = clone[idx][-1]
                for lib in variables_libres:
                    v_direccionales[lib][p] = -clone[idx][lib]

            forma_vectorial = f"Vector X = {v_particular}"
            for lib in variables_libres:
                sub = to_subscript(lib + 1)
                forma_vectorial += f" + x{sub} * {v_direccionales[lib]}"

            print("========================================================\n")
            return clone, columnas_pivote, variables_libres, None, forma_vectorial

        else:
            print("TIPO DE SISTEMA: CONSISTENTE DETERMINADO")
            print("CANTIDAD DE SOLUCIONES: Solución ÚNICA.")
            print("========================================================\n")

            answers = []
            for row in clone:
                val = row[-1]
                if isinstance(val, Fraction) and val.denominator == 1:
                    answers.append(val.numerator)
                else:
                    answers.append(val)

            return clone, columnas_pivote, variables_libres, answers, None

# Sustituye la solución calculada en la matriz original para comprobar que A*x sea igual a b.
def verificar_solucion(matriz_original, vector_b, soluciones):
    for i in range(len(matriz_original)):
        suma = sum(
            Fraction(matriz_original[i][j]) * Fraction(soluciones[j])
            for j in range(len(soluciones))
        )
        if suma != Fraction(vector_b[i]):
            print(f" Alerta: La solución no satisface la ecuación {i + 1}")
            return False

    print(" Solución verificada con éxito sustituyendo en el sistema original.")
    return True


# Evalúa si el sistema es homogéneo (si todos los elementos del vector b son cero).
def es_homogeneo(vector_b):
    return all(Fraction(val) == 0 for val in vector_b)


# Evalúa la dependencia lineal de los vectores columna de una matriz.
def analizar_dependencia_lineal(matriz_A):
    # Se crea un vector de ceros para formar el sistema homogéneo Ax = 0
    b_cero = [Fraction(0) for _ in range(matriz_A.rows)]

    # Clonamos la matriz en una nueva instancia para no alterar la original
    mat_eval = Matrix(matriz_A.rows, matriz_A.columns)
    for i in range(matriz_A.rows):
        for j in range(matriz_A.columns):
            mat_eval.modify(i, j, matriz_A.array[i][j])

    # Añadimos el vector b (puros ceros)
    mat_eval.add_vector_b(b_cero)

    # Ejecutamos Gauss-Jordan.
    # Si hay variables libres, el sistema tiene soluciones no triviales (Linealmente Dependiente)
    # Si no hay variables libres, solo tiene la solución trivial (Linealmente Independiente)
    _, _, variables_libres, _, _ = mat_eval.gauss_jordan()

    # Retorna True si es linealmente independiente (0 variables libres)
    return len(variables_libres) == 0