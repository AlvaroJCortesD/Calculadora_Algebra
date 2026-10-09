"""
Módulo de Álgebra de Matrices.
Implementa operaciones matriciales, determinantes y matrices inversas
(por Gauss-Jordan y Adjunta), y verifica propiedades clave del álgebra.
"""

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

    def es_igual(self, B):
        """Verifica si dos matrices son iguales comparando cada elemento."""
        if self.rows != B.rows or self.columns != B.columns:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.array[i][j] != B.array[i][j]:
                    return False
        return True

    # ==================================================
    # SUMA Y RESTA
    # ==================================================

    def sumar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        resultado = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                resultado.modify(i, j, Fraction(self.array[i][j]) + Fraction(B.array[i][j]))
        return resultado

    def restar(self, B):
        if self.rows != B.rows or self.columns != B.columns:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        resultado = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                resultado.modify(i, j, Fraction(self.array[i][j]) - Fraction(B.array[i][j]))
        return resultado

    # ==================================================
    # MULTIPLICACIÓN POR ESCALAR Y MATRICES
    # ==================================================

    def escalar_mult(self, c):
        resultado = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                resultado.modify(i, j, Fraction(c) * Fraction(self.array[i][j]))
        return resultado

    def multiplicar(self, B):
        if self.columns != B.rows:
            raise ValueError(f"Columnas de A ({self.columns}) ≠ Filas de B ({B.rows}).")
        resultado = Matrix(self.rows, B.columns)
        for i in range(self.rows):
            for j in range(B.columns):
                suma = Fraction(0)
                for k in range(self.columns):
                    suma += (Fraction(self.array[i][k]) * Fraction(B.array[k][j]))
                resultado.modify(i, j, suma)
        return resultado

    # ==================================================
    # TRASPUESTA
    # ==================================================

    def traspuesta(self):
        resultado = Matrix(self.columns, self.rows)
        for i in range(self.rows):
            for j in range(self.columns):
                resultado.modify(j, i, self.array[i][j])
        return resultado

    # ==================================================
    # DETERMINANTES
    # ==================================================

    def menor(self, fila, columna):
        """Devuelve la matriz menor eliminando la fila y columna dadas."""
        n = self.rows
        m_menor = Matrix(n - 1, n - 1)
        f_menor = 0
        for i in range(n):
            if i == fila: continue
            c_menor = 0
            for j in range(n):
                if j == columna: continue
                m_menor.modify(f_menor, c_menor, self.array[i][j])
                c_menor += 1
            f_menor += 1
        return m_menor

    def determinante_cofactores(self):
        """Calcula el determinante de una matriz cuadrada por expansión de cofactores."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")
        n = self.rows
        if n == 1:
            return Fraction(self.array[0][0])
        if n == 2:
            return Fraction(self.array[0][0]) * Fraction(self.array[1][1]) - Fraction(self.array[0][1]) * Fraction(
                self.array[1][0])

        det = Fraction(0)
        # Expansión a lo largo de la primera fila
        for j in range(n):
            # El signo alterna según la posición de la columna.
            signo = Fraction(1) if j % 2 == 0 else Fraction(-1)
            det += signo * Fraction(self.array[0][j]) * self.menor(0, j).determinante_cofactores()
        return det

    def determinante_triangular(self):
        """Calcula el determinante reduciendo la matriz a forma triangular superior."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")
        n = self.rows
        temp = [[Fraction(self.array[i][j]) for j in range(n)] for i in range(n)]
        det = Fraction(1)
        intercambios = 0

        for i in range(n):
            if temp[i][i] == 0:
                pivote_valido = False
                for k in range(i + 1, n):
                    if temp[k][i] != 0:
                        # Se intercambian filas si el pivote es 0: sin pivote no se elimina la columna.
                        temp[i], temp[k] = temp[k], temp[i]
                        intercambios += 1
                        pivote_valido = True
                        break
                if not pivote_valido:
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

    # ==================================================
    # MATRIZ ADJUNTA Y COFACTORES
    # ==================================================

    def matriz_cofactores(self):
        """Construye la matriz de cofactores usando el cálculo de menores."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada.")
        n = self.rows
        cof = Matrix(n, n)
        for i in range(n):
            for j in range(n):
                signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
                cof.modify(i, j, signo * self.menor(i, j).determinante_cofactores())
        return cof

    def adjunta(self):
        """Devuelve la matriz adjunta, que es la transpuesta de la matriz de cofactores."""
        return self.matriz_cofactores().traspuesta()

    def inversa_adjunta(self):
        """Calcula la matriz inversa multiplicando la adjunta por 1/det(A)."""
        det = self.determinante_triangular()
        if det == 0:
            raise ValueError("La matriz es singular y no tiene inversa.")
        return self.adjunta().escalar_mult(Fraction(1) / det)

    # ==================================================
    # INVERSA (GAUSS-JORDAN)
    # ==================================================

    def inversa(self):
        """Calcula la matriz inversa utilizando el método de Gauss-Jordan."""
        if self.rows != self.columns:
            raise ValueError("La matriz debe ser cuadrada para calcular su inversa.")

        n = self.rows
        aumentada = []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(Fraction(self.array[i][j]))
            for j in range(n):
                fila.append(Fraction(1) if i == j else Fraction(0))
            aumentada.append(fila)

        for columna in range(n):
            fila_pivote = None
            for fila in range(columna, n):
                if aumentada[fila][columna] != 0:
                    fila_pivote = fila
                    break

            # Sin n pivotes la matriz es singular: se detiene la reducción.
            if fila_pivote is None:
                raise ValueError("La matriz es singular y no tiene inversa.")
            if fila_pivote != columna:
                aumentada[columna], aumentada[fila_pivote] = aumentada[fila_pivote], aumentada[columna]

            pivote = aumentada[columna][columna]
            for j in range(2 * n):
                aumentada[columna][j] /= pivote
            for fila in range(n):
                if fila != columna:
                    factor = aumentada[fila][columna]
                    for j in range(2 * n):
                        aumentada[fila][j] -= factor * aumentada[columna][j]

        inversa = Matrix(n, n)
        for i in range(n):
            for j in range(n):
                inversa.modify(i, j, aumentada[i][j + n])
        return inversa


# ======================================================
# MENÚ Y FUNCIONES INTERACTIVAS
# ======================================================

def encabezado():
    print("\n======================================================")
    print("[ A ][ B ]   MÓDULO: ÁLGEBRA DE MATRICES")
    print("[ C ][ D ]   Operaciones, Traspuesta, Determinante e Inversa")
    print("======================================================")


def crear_matriz_interactiva(nombre="A"):
    filas = asking_for_input(f"Filas de {nombre}: ", type=int)
    columnas = asking_for_input(f"Columnas de {nombre}: ", type=int)
    A = Matrix(filas, columnas)
    print(f"\n--- INGRESO DE DATOS DE LA MATRIZ {nombre} ---")
    for i in range(filas):
        for j in range(columnas):
            valor = asking_for_input(f"{nombre}[{i + 1}][{j + 1}]: ")
            A.modify(i, j, valor)
    return A


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


def multiplicacion_escalar():
    encabezado()
    A = crear_matriz_interactiva("A")
    c = asking_for_input("\nIngrese el escalar c: ")
    print(f"\n--- {c} · A ---")
    print(A.escalar_mult(c))


def multiplicacion_matrices():
    encabezado()
    A = crear_matriz_interactiva("A")
    B = crear_matriz_interactiva("B")
    try:
        print("\n--- A · B ---")
        print(A.multiplicar(B))
    except ValueError as e:
        print(f"\n[ERROR]: {e}")


def calcular_traspuesta():
    encabezado()
    A = crear_matriz_interactiva("A")
    print("\n--- MATRIZ ORIGINAL A ---")
    print(A)
    print("\n--- MATRIZ TRASPUESTA Aᵀ ---")
    print(A.traspuesta())


def calcular_determinante():
    encabezado()
    A = crear_matriz_interactiva("A")
    try:
        print("\n--- MATRIZ ORIGINAL A ---")
        print(A)

        det_cofactores = A.determinante_cofactores()
        det_triangular = A.determinante_triangular()

        print("\n--- DETERMINANTE ---")
        print(f"Por cofactores: {det_cofactores}")
        print(f"Por reducción a forma triangular: {det_triangular}")

        if A.rows == 3:
            # Mostramos el método de Sarrus adicionalmente si es 3x3.
            a = A.array
            s_pos = (Fraction(a[0][0]) * Fraction(a[1][1]) * Fraction(a[2][2]) +
                     Fraction(a[0][1]) * Fraction(a[1][2]) * Fraction(a[2][0]) +
                     Fraction(a[0][2]) * Fraction(a[1][0]) * Fraction(a[2][1]))
            s_neg = (Fraction(a[0][2]) * Fraction(a[1][1]) * Fraction(a[2][0]) +
                     Fraction(a[0][0]) * Fraction(a[1][2]) * Fraction(a[2][1]) +
                     Fraction(a[0][1]) * Fraction(a[1][0]) * Fraction(a[2][2]))
            print(f"Por Sarrus (3x3): {s_pos - s_neg}")

        if det_triangular != 0:
            print(
                "\nDiagnóstico: La matriz es invertible: det(A) ≠ 0, tiene n posiciones pivote, sus columnas son L.I. y generan Rn")
        else:
            print("\nDiagnóstico: La matriz es singular (no tiene inversa): det(A) = 0")
    except ValueError as e:
        print(f"\n[ERROR]: {e}")


def calcular_inversa_gauss():
    encabezado()
    A = crear_matriz_interactiva("A")
    print("\n--- MATRIZ ORIGINAL A ---")
    print(A)
    try:
        det = A.determinante_triangular()
        if det == 0:
            print("\nDiagnóstico: La matriz es singular (no tiene inversa): det(A) = 0")
            return

        resultado = A.inversa()
        print(
            "\nDiagnóstico: La matriz es invertible: det(A) ≠ 0, tiene n posiciones pivote, sus columnas son L.I. y generan Rn")
        print("\n--- MATRIZ INVERSA A⁻¹ (Gauss-Jordan) ---")
        print(resultado)

        print("\n--- COMPROBACIÓN A · A⁻¹ = I ---")
        print(A.multiplicar(resultado))
    except ValueError as e:
        print(f"\n[ERROR]: {e}")


def calcular_inversa_adjunta():
    encabezado()
    A = crear_matriz_interactiva("A")
    print("\n--- MATRIZ ORIGINAL A ---")
    print(A)
    try:
        det = A.determinante_triangular()
        if det == 0:
            print("\nDiagnóstico: La matriz es singular (no tiene inversa): det(A) = 0")
            return

        print(
            "\nDiagnóstico: La matriz es invertible: det(A) ≠ 0, tiene n posiciones pivote, sus columnas son L.I. y generan Rn")
        print("\n--- MATRIZ ADJUNTA adj(A) ---")
        print(A.adjunta())

        resultado = A.inversa_adjunta()
        print("\n--- MATRIZ INVERSA A⁻¹ (Por Adjunta) ---")
        print(resultado)

        print("\n--- COMPROBACIÓN A · A⁻¹ = I ---")
        print(A.multiplicar(resultado))
    except ValueError as e:
        print(f"\n[ERROR]: {e}")


def verificador_propiedades():
    encabezado()
    print("\n--- VERIFICADOR DE PROPIEDADES ---")
    A = crear_matriz_interactiva("A (cuadrada e invertible)")
    B = crear_matriz_interactiva("B (cuadrada e invertible, mismo orden)")

    try:
        invA = A.inversa()
        invB = B.inversa()

        print("\n[ Propiedad 1: (A⁻¹)⁻¹ = A ]")
        if invA.inversa().es_igual(A):
            print("Resultado: Se cumple.")
        else:
            print("Resultado: No se cumple.")

        print("\n[ Propiedad 2: (AB)⁻¹ = B⁻¹ A⁻¹ ]")
        AB = A.multiplicar(B)
        AB_inv = AB.inversa()
        Binv_Ainv = invB.multiplicar(invA)
        if AB_inv.es_igual(Binv_Ainv):
            print("Resultado: Se cumple.")
        else:
            print("Resultado: No se cumple.")

        print("\n[ Propiedad 3: (Aᵀ)⁻¹ = (A⁻¹)ᵀ ]")
        At_inv = A.traspuesta().inversa()
        invA_t = invA.traspuesta()
        if At_inv.es_igual(invA_t):
            print("Resultado: Se cumple.")
        else:
            print("Resultado: No se cumple.")

        print("\n[ Propiedad 4: det(A⁻¹) = 1 / det(A) ]")
        det_invA = invA.determinante_triangular()
        det_A = A.determinante_triangular()
        if det_invA == Fraction(1) / det_A:
            print("Resultado: Se cumple.")
        else:
            print("Resultado: No se cumple.")

        print("\n[ Propiedad 6 (Matriz Triangular): Det = Producto Diagonal ]")
        print("Calculando y comparando determinante con y sin cofactores...")
        det_cof = A.determinante_cofactores()
        if det_cof == det_A:
            print("Resultado: Se cumple (ambos métodos arrojaron el mismo determinante exacto).")
        else:
            print("Resultado: No se cumple.")

    except ValueError as e:
        print(f"\n[ERROR en Validación]: {e}")


# ======================================================
# MENÚ DEL MÓDULO
# ======================================================

def menu_matrices():
    while True:

        encabezado()

        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación por Escalar")
        print("4. Producto Matricial")
        print("5. Transposición")
        print("6. Determinante")
        print("7. Inversa por Gauss-Jordan")
        print("8. Inversa por Matriz Adjunta")
        print("9. Verificador de propiedades")
        print("0. Ver Teoremas Clave del Módulo")
        print("10. Regresar al menú principal")

        opcion = asking_for_input("\nSeleccione una opción: ", type=int)

        if opcion == 1:
            suma_resta()
        elif opcion == 2:
            encabezado()  # Agrupado en suma_resta para simplificar
            encabezado()
        elif opcion == 2:  # Manejo de resta fusionado
            suma_resta()
        elif opcion == 3:
            multiplicacion_escalar()
        elif opcion == 4:
            multiplicacion_matrices()
        elif opcion == 5:
            calcular_traspuesta()
        elif opcion == 6:
            calcular_determinante()
        elif opcion == 7:
            calcular_inversa_gauss()
        elif opcion == 8:
            calcular_inversa_adjunta()
        elif opcion == 9:
            verificador_propiedades()
        elif opcion == 0:
            resumen_teoremas.teoremas_matrices()
        elif opcion == 10:
            break
        else:
            if opcion == 1 or opcion == 2:
                # Opciones 1 y 2 resuelven juntas en el método `suma_resta` definido.
                suma_resta()
            else:
                print("\n[ERROR] Opción no válida.")