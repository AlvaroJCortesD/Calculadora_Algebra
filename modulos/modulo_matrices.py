from fractions import Fraction
from teoremas import resumen_teoremas


# ======================================================
# FUNCIONES GENERALES
# ======================================================

# Solicita un número al usuario y permite ingresar fracciones.
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
                "Entrada inválida. Ingresa un número entero, "
                "decimal o fracción. Ejemplo: 3, 0.5 o 1/3."
            )


# Da formato a los valores de las matrices.
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

# Muestra un vector en forma vertical y ajusta
# automáticamente el tamaño del recuadro.
def mostrar_vector(vector):
    valores = [str(valor) for valor in vector]

    # Buscar el valor con más caracteres.
    ancho = max(len(valor) for valor in valores)

    # Espacio adicional a ambos lados.
    ancho += 2

    # Parte superior.
    print("┌" + " " * ancho + "┐")

    # Valores del vector.
    for valor in valores:
        espacios_izquierda = (ancho - len(valor)) // 2
        espacios_derecha = (
            ancho - len(valor) - espacios_izquierda
        )

        print(
            "│"
            + " " * espacios_izquierda
            + valor
            + " " * espacios_derecha
            + "│"
        )

    # Parte inferior.
    print("└" + " " * ancho + "┘")


# Formatea una matriz aumentada [A | b].
def format_matrix(matriz_datos):
    lines = []

    for row in matriz_datos:
        datos_A = row[:-1]
        valor_b = row[-1]

        parte_A = "  ".join(
            fmt_val(num) for num in datos_A
        )

        fmt_b = fmt_val(valor_b)

        lines.append(
            f"{parte_A}  │  {fmt_b}"
        )

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


# ======================================================
# CLASE MATRIX
# ======================================================

class Matrix:

    # Crea una matriz con las dimensiones indicadas.
    def __init__(self, rows, columns, valor_inicial=0):
        self.rows = rows
        self.columns = columns

        self.array = [
            [valor_inicial for _ in range(columns)]
            for _ in range(rows)
        ]

    # Agrega el vector b como última columna.
    def add_vector_b(self, vector_b):

        if len(vector_b) != self.rows:
            raise ValueError(
                "El número de elementos de vector b "
                "debe ser igual al número de filas."
            )

        for i in range(self.rows):
            self.array[i].append(vector_b[i])

        self.columns += 1

    # Modifica una posición de la matriz.
    def modify(self, rows, columns, new_value):
        self.array[rows][columns] = new_value

    # Permite mostrar una matriz directamente con print().
    def __str__(self):
        lines = []

        for row in self.array:
            parte = "  ".join(
                fmt_val(num) for num in row
            )

            lines.append(f"│ {parte} │")

        return "\n".join(lines)

    # ==================================================
    # SUMA
    # ==================================================

    # Suma dos matrices del mismo tamaño.
    def sumar(self, B):

        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError(
                "Las matrices deben tener el mismo tamaño."
            )

        resultado = Matrix(
            self.rows,
            self.columns
        )

        for i in range(self.rows):
            for j in range(self.columns):

                resultado.modify(
                    i,
                    j,
                    Fraction(self.array[i][j])
                    + Fraction(B.array[i][j])
                )

        return resultado

    # ==================================================
    # RESTA
    # ==================================================

    # Resta dos matrices del mismo tamaño.
    def restar(self, B):

        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError(
                "Las matrices deben tener el mismo tamaño."
            )

        resultado = Matrix(
            self.rows,
            self.columns
        )

        for i in range(self.rows):
            for j in range(self.columns):

                resultado.modify(
                    i,
                    j,
                    Fraction(self.array[i][j])
                    - Fraction(B.array[i][j])
                )

        return resultado

    # ==================================================
    # MULTIPLICACIÓN POR ESCALAR
    # ==================================================

    # Multiplica todos los elementos de la matriz por un escalar.
    def escalar_mult(self, c):

        resultado = Matrix(
            self.rows,
            self.columns
        )

        for i in range(self.rows):
            for j in range(self.columns):

                resultado.modify(
                    i,
                    j,
                    Fraction(c)
                    * Fraction(self.array[i][j])
                )

        return resultado

    # ==================================================
    # MULTIPLICACIÓN DE MATRICES
    # ==================================================

    # Multiplica dos matrices si sus dimensiones son compatibles.
    def multiplicar(self, B):

        if self.columns != B.rows:
            raise ValueError(
                f"Columnas de A ({self.columns}) "
                f"≠ Filas de B ({B.rows})."
            )

        resultado = Matrix(
            self.rows,
            B.columns
        )

        for i in range(self.rows):

            for j in range(B.columns):

                suma = Fraction(0)

                for k in range(self.columns):

                    suma += (
                        Fraction(self.array[i][k])
                        * Fraction(B.array[k][j])
                    )

                resultado.modify(
                    i,
                    j,
                    suma
                )

        return resultado

    # ==================================================
    # TRASPUESTA
    # ==================================================

    # Intercambia las filas por las columnas.
    def traspuesta(self):

        resultado = Matrix(
            self.columns,
            self.rows
        )

        for i in range(self.rows):

            for j in range(self.columns):

                resultado.modify(
                    j,
                    i,
                    self.array[i][j]
                )

        return resultado

    # ==================================================
    # INVERSA
    # ==================================================

    # Calcula la matriz inversa utilizando Gauss-Jordan.
    def inversa(self):

        # La inversa solamente existe para matrices cuadradas.
        if self.rows != self.columns:
            raise ValueError(
                "La matriz debe ser cuadrada para calcular su inversa."
            )

        n = self.rows

        # Se crea la matriz aumentada [A | I].
        aumentada = []

        for i in range(n):

            fila = []

            # Copiamos la matriz original.
            for j in range(n):
                fila.append(
                    Fraction(self.array[i][j])
                )

            # Agregamos la matriz identidad.
            for j in range(n):
                if i == j:
                    fila.append(Fraction(1))
                else:
                    fila.append(Fraction(0))

            aumentada.append(fila)

        # ==============================================
        # GAUSS-JORDAN
        # ==============================================

        for columna in range(n):

            fila_pivote = None

            # Buscamos un pivote diferente de cero.
            for fila in range(columna, n):

                if aumentada[fila][columna] != 0:
                    fila_pivote = fila
                    break

            # Si no encontramos pivote, no existe inversa.
            if fila_pivote is None:
                raise ValueError(
                    "La matriz es singular y no tiene inversa."
                )

            # Intercambiamos filas si es necesario.
            if fila_pivote != columna:

                aumentada[columna], aumentada[fila_pivote] = (
                    aumentada[fila_pivote],
                    aumentada[columna]
                )

            # Convertimos el pivote en 1.
            pivote = aumentada[columna][columna]

            for j in range(2 * n):

                aumentada[columna][j] /= pivote

            # Hacemos ceros arriba y abajo del pivote.
            for fila in range(n):

                if fila != columna:

                    factor = aumentada[fila][columna]

                    for j in range(2 * n):

                        aumentada[fila][j] -= (
                            factor
                            * aumentada[columna][j]
                        )

        # ==============================================
        # EXTRAER LA MATRIZ INVERSA
        # ==============================================

        inversa = Matrix(n, n)

        for i in range(n):

            for j in range(n):

                inversa.modify(
                    i,
                    j,
                    aumentada[i][j + n]
                )

        return inversa


# ======================================================
# MENÚ Y FUNCIONES INTERACTIVAS
# ======================================================

def encabezado():

    print("\n======================================================")
    print("[ A ][ B ]   MÓDULO: ÁLGEBRA DE MATRICES")
    print("[ C ][ D ]   Operaciones, Traspuesta y Matriz Inversa")
    print("======================================================")


# Permite ingresar una matriz desde el teclado.
def crear_matriz_interactiva(nombre="A"):

    filas = asking_for_input(
        f"Filas de {nombre}: ",
        type=int
    )

    columnas = asking_for_input(
        f"Columnas de {nombre}: ",
        type=int
    )

    A = Matrix(
        filas,
        columnas
    )

    print(
        f"\n--- INGRESO DE DATOS DE LA MATRIZ {nombre} ---"
    )

    for i in range(filas):

        for j in range(columnas):

            valor = asking_for_input(
                f"{nombre}[{i + 1}][{j + 1}]: "
            )

            A.modify(
                i,
                j,
                valor
            )

    return A


# ======================================================
# SUMA Y RESTA
# ======================================================

def suma_resta():

    encabezado()

    A = crear_matriz_interactiva("A")
    B = crear_matriz_interactiva("B")

    try:

        print("\n--- A + B ---")
        print(A.sumar(B))

        print("\n--- A - B ---")
        print(A.restar(B))

    except ValueError as e:

        print(f"\n[ERROR]: {e}")


# ======================================================
# MULTIPLICACIÓN POR ESCALAR
# ======================================================

def multiplicacion_escalar():

    encabezado()

    A = crear_matriz_interactiva("A")

    c = asking_for_input(
        "\nIngrese el escalar c: "
    )

    print(f"\n--- {c} · A ---")
    print(A.escalar_mult(c))


# ======================================================
# MULTIPLICACIÓN DE MATRICES
# ======================================================

def multiplicacion_matrices():

    encabezado()

    A = crear_matriz_interactiva("A")
    B = crear_matriz_interactiva("B")

    try:

        print("\n--- A · B ---")
        print(A.multiplicar(B))

    except ValueError as e:

        print(f"\n[ERROR]: {e}")


# ======================================================
# TRASPUESTA
# ======================================================

def calcular_traspuesta():

    encabezado()

    A = crear_matriz_interactiva("A")

    print("\n--- MATRIZ ORIGINAL A ---")
    print(A)

    resultado = A.traspuesta()

    print("\n--- MATRIZ TRASPUESTA Aᵀ ---")
    print(resultado)


# ======================================================
# INVERSA
# ======================================================

def calcular_inversa():

    encabezado()

    A = crear_matriz_interactiva("A")

    print("\n--- MATRIZ ORIGINAL A ---")
    print(A)

    try:

        resultado = A.inversa()

        print("\n--- MATRIZ INVERSA A⁻¹ ---")
        print(resultado)

    except ValueError as e:

        print(f"\n[ERROR]: {e}")

# Multiplica una matriz por un vector.
def matriz_por_vector(A, vector):
    if A.columns != len(vector):
        raise ValueError(
            "La cantidad de columnas de A debe coincidir "
            "con la dimensión del vector."
        )

    resultado = []

    for i in range(A.rows):
        suma = Fraction(0)

        for j in range(A.columns):
            suma += (
                Fraction(A.array[i][j])
                * Fraction(vector[j])
            )

        resultado.append(suma)

    return resultado


# Comprueba las propiedades del producto matriz-vector
# mostrando el procedimiento matemático.
def producto_matriz_vector():
    encabezado()

    print("\n--- PRODUCTO MATRIZ-VECTOR ---")
    print("Se comprobarán las propiedades:")
    print("a) A(u + v) = Au + Av")
    print("b) A(cu) = c(Au)")

    # Ingresar la matriz A.
    print("\n--- MATRIZ A ---")
    A = crear_matriz_interactiva("A")

    # Ingresar el vector u.
    print("\n--- VECTOR u ---")
    u = []

    for i in range(A.columns):
        valor = asking_for_input(f"u[{i + 1}]: ")
        u.append(valor)

    # Ingresar el vector v.
    print("\n--- VECTOR v ---")
    v = []

    for i in range(A.columns):
        valor = asking_for_input(f"v[{i + 1}]: ")
        v.append(valor)

    # Ingresar el escalar.
    c = asking_for_input("\nIngrese el escalar c: ")

    # ==================================================
    # PROPIEDAD A(u + v) = Au + Av
    # ==================================================

    print("\n")
    print("======================================================")
    print("   PROPIEDAD 1: A(u + v) = Au + Av")
    print("======================================================")

    # Paso 1: calcular u + v.
    u_mas_v = [
        Fraction(u[i]) + Fraction(v[i])
        for i in range(A.columns)
    ]

    print("\nPASO 1. Calculamos u + v:")

    for i in range(A.columns):
        print(
            f"  {u[i]} + {v[i]} = {u_mas_v[i]}"
        )

    print("\nu + v =")
    mostrar_vector(u_mas_v)

    # Paso 2: calcular A(u + v).
    print("\nPASO 2. Calculamos A(u + v):")

    Au_mas_v = matriz_por_vector(A, u_mas_v)

    for i in range(A.rows):
        operaciones = []

        for j in range(A.columns):
            operaciones.append(
                f"({A.array[i][j]})({u_mas_v[j]})"
            )

        resultado = " + ".join(operaciones)

        print(
            f"  Fila {i + 1}: {resultado} = "
            f"{Au_mas_v[i]}"
        )

    print("\nA(u + v) =")
    mostrar_vector(Au_mas_v)

    # Paso 3: calcular Au.
    print("\nPASO 3. Calculamos Au:")

    Au = matriz_por_vector(A, u)

    for i in range(A.rows):
        operaciones = []

        for j in range(A.columns):
            operaciones.append(
                f"({A.array[i][j]})({u[j]})"
            )

        resultado = " + ".join(operaciones)

        print(
            f"  Fila {i + 1}: {resultado} = "
            f"{Au[i]}"
        )

    print("\nAu =")
    mostrar_vector(Au)

    # Paso 4: calcular Av.
    print("\nPASO 4. Calculamos Av:")

    Av = matriz_por_vector(A, v)

    for i in range(A.rows):
        operaciones = []

        for j in range(A.columns):
            operaciones.append(
                f"({A.array[i][j]})({v[j]})"
            )

        resultado = " + ".join(operaciones)

        print(
            f"  Fila {i + 1}: {resultado} = "
            f"{Av[i]}"
        )

    print("\nAv =")
    mostrar_vector(Av)

    # Paso 5: calcular Au + Av.
    print("\nPASO 5. Calculamos Au + Av:")

    Au_mas_Av = [
        Au[i] + Av[i]
        for i in range(A.rows)
    ]

    for i in range(A.rows):
        print(
            f"  {Au[i]} + {Av[i]} = "
            f"{Au_mas_Av[i]}"
        )

    print("\nAu + Av =")
    mostrar_vector(Au_mas_Av)

    # Paso 6: comparar.
    print("\nPASO 6. Comparamos ambos resultados:")

    if Au_mas_v == Au_mas_Av:
        print("  A(u + v) = Au + Av")
        print("\n  [RESULTADO] La propiedad se cumple.")
    else:
        print("  A(u + v) ≠ Au + Av")
        print("\n  [RESULTADO] La propiedad no se cumple.")

    # ==================================================
    # PROPIEDAD A(cu) = c(Au)
    # ==================================================

    print("\n")
    print("======================================================")
    print("   PROPIEDAD 2: A(cu) = c(Au)")
    print("======================================================")

    # Paso 1: calcular cu.
    print("\nPASO 1. Calculamos cu:")

    cu = [
        Fraction(c) * Fraction(u[i])
        for i in range(A.columns)
    ]

    for i in range(A.columns):
        print(
            f"  {c}({u[i]}) = {cu[i]}"
        )

    print("\ncu =")
    mostrar_vector(cu)

    # Paso 2: calcular A(cu).
    print("\nPASO 2. Calculamos A(cu):")

    A_cu = matriz_por_vector(A, cu)

    for i in range(A.rows):
        operaciones = []

        for j in range(A.columns):
            operaciones.append(
                f"({A.array[i][j]})({cu[j]})"
            )

        resultado = " + ".join(operaciones)

        print(
            f"  Fila {i + 1}: {resultado} = "
            f"{A_cu[i]}"
        )

    print("\nA(cu) =")
    mostrar_vector(A_cu)

    # Paso 3: calcular Au.
    print("\nPASO 3. Calculamos Au:")

    # Au ya fue calculado anteriormente.
    for i in range(A.rows):
        operaciones = []

        for j in range(A.columns):
            operaciones.append(
                f"({A.array[i][j]})({u[j]})"
            )

        resultado = " + ".join(operaciones)

        print(
            f"  Fila {i + 1}: {resultado} = "
            f"{Au[i]}"
        )

    print("\nAu =")
    mostrar_vector(Au)

    # Paso 4: calcular c(Au).
    print("\nPASO 4. Calculamos c(Au):")

    c_Au = [
        Fraction(c) * Fraction(Au[i])
        for i in range(A.rows)
    ]

    for i in range(A.rows):
        print(
            f"  {c}({Au[i]}) = {c_Au[i]}"
        )

    print("\nc(Au) =")
    mostrar_vector(c_Au)

    # Paso 5: comparar.
    print("\nPASO 5. Comparamos ambos resultados:")

    if A_cu == c_Au:
        print("  A(cu) = c(Au)")
        print("\n  [RESULTADO] La propiedad se cumple.")
    else:
        print("  A(cu) ≠ c(Au)")
        print("\n  [RESULTADO] La propiedad no se cumple.")

# ======================================================
# MENÚ DEL MÓDULO
# ======================================================

def menu_matrices():

    while True:

        encabezado()

        print("1. Suma y resta de matrices")
        print("2. Multiplicación por escalar")
        print("3. Multiplicación de matrices")
        print("4. Matriz traspuesta")
        print("5. Matriz inversa")
        print("6. Producto matriz-vector")
        print("0. Ver Teoremas Clave del Módulo")
        print("9. Regresar al menú principal")

        opcion = asking_for_input(
            "\nSeleccione una opción: ",
            type=int
        )

        if opcion == 1:

            suma_resta()

        elif opcion == 2:

            multiplicacion_escalar()

        elif opcion == 3:

            multiplicacion_matrices()

        elif opcion == 4:

            calcular_traspuesta()

        elif opcion == 5:

            calcular_inversa()

        elif opcion == 6:

            producto_matriz_vector()

        elif opcion == 0:

            resumen_teoremas.teoremas_matrices()

        elif opcion == 9:

            break

        else:

            print("\n[ERROR] Opción no válida.")