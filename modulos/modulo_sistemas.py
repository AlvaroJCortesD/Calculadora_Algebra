from fractions import Fraction

from modulos import modulo_matrices
from teoremas import resumen_teoremas


def to_subscript(number):
    subscripts = str.maketrans(
        "0123456789",
        "₀₁₂₃₄₅₆₇₈₉"
    )

    return str(number).translate(subscripts)


def encabezado():

    print("\n======================================================")
    print("[  [1 2 | 3]  ]  MÓDULO: SISTEMAS DE ECUACIONES (SEL)")
    print("[  [0 1 | 5]  ]  Métodos: Gauss, Gauss-Jordan")
    print("======================================================")


def gauss_jordan(matrix):

    m_filas = matrix.rows
    n_variables = matrix.columns - 1

    clone = [
        [Fraction(valor) for valor in fila]
        for fila in matrix.array
    ]

    def imprimir_paso(matriz_clon):

        print(
            modulo_matrices.format_matrix(
                matriz_clon
            )
        )

        print("-" * 50)

    print("\n=== INICIANDO REDUCCIÓN GAUSS-JORDAN ===")

    print(
        "Transformando la matriz a la "
        "FORMA ESCALONADA REDUCIDA..."
    )

    columnas_pivote = []
    fila_pivote = 0

    for c in range(n_variables):

        if fila_pivote >= m_filas:
            break

        print(f"\nProcesando Columna {c + 1}:")

        max_row = fila_pivote

        for r in range(
            fila_pivote + 1,
            m_filas
        ):

            if (
                abs(clone[r][c])
                > abs(clone[max_row][c])
            ):

                max_row = r

        if clone[max_row][c] == 0:

            print(
                f"-> La columna {c + 1} "
                "no tiene pivote (variable libre)."
            )

            continue

        if max_row != fila_pivote:

            clone[fila_pivote], clone[max_row] = (
                clone[max_row],
                clone[fila_pivote]
            )

            print(
                f"-> Se intercambió la fila "
                f"{fila_pivote + 1} con la fila "
                f"{max_row + 1}:"
            )

            imprimir_paso(clone)

        pivot = clone[fila_pivote][c]

        for j in range(matrix.columns):

            clone[fila_pivote][j] /= pivot

        print(
            f"-> Fila {fila_pivote + 1} "
            f"dividida entre su pivote ({pivot}):"
        )

        imprimir_paso(clone)

        for f in range(m_filas):

            if f != fila_pivote:

                factor = clone[f][c]

                for j in range(matrix.columns):

                    clone[f][j] -= (
                        factor
                        * clone[fila_pivote][j]
                    )

        print(
            f"-> Ceros generados arriba y abajo "
            f"del pivote de la columna {c + 1}:"
        )

        imprimir_paso(clone)

        columnas_pivote.append(c)
        fila_pivote += 1

    print("\n=== PROCESO DE REDUCCIÓN FINALIZADO ===")

    print(
        "ESTADO: FORMA ESCALONADA REDUCIDA "
        "POR FILAS."
    )

    variables_libres = [
        col
        for col in range(n_variables)
        if col not in columnas_pivote
    ]

    inconsistente = False

    for row in clone:

        if (
            all(
                val == 0
                for val in row[:-1]
            )
            and row[-1] != 0
        ):

            inconsistente = True
            break

    print(
        "\n================ RESULTADO DEL ANÁLISIS ================"
    )

    if inconsistente:

        print("TIPO DE SISTEMA: INCONSISTENTE")
        print(
            "CANTIDAD DE SOLUCIONES: "
            "Sin solución."
        )

        print(
            "RAZÓN: Se obtuvo una contradicción "
            "[0 0 ... 0 | k], k ≠ 0."
        )

        print(
            "========================================================\n"
        )

        return (
            clone,
            columnas_pivote,
            variables_libres,
            None,
            None
        )

    elif len(variables_libres) > 0:

        print(
            "TIPO DE SISTEMA: "
            "CONSISTENTE INDETERMINADO"
        )

        print(
            "CANTIDAD DE SOLUCIONES: "
            "Infinitas soluciones."
        )

        v_particular = [
            Fraction(0)
            for _ in range(n_variables)
        ]

        v_direccionales = {
            lib: [
                Fraction(0)
                for _ in range(n_variables)
            ]
            for lib in variables_libres
        }

        for lib in variables_libres:

            v_direccionales[lib][lib] = Fraction(1)

        for idx, p in enumerate(columnas_pivote):

            v_particular[p] = clone[idx][-1]

            for lib in variables_libres:

                v_direccionales[lib][p] = (
                    -clone[idx][lib]
                )

        forma_vectorial = (
            f"Vector X = {v_particular}"
        )

        for lib in variables_libres:

            sub = to_subscript(lib + 1)

            forma_vectorial += (
                f" + x{sub} * "
                f"{v_direccionales[lib]}"
            )

        print(
            "========================================================\n"
        )

        return (
            clone,
            columnas_pivote,
            variables_libres,
            None,
            forma_vectorial
        )

    else:

        print(
            "TIPO DE SISTEMA: "
            "CONSISTENTE DETERMINADO"
        )

        print(
            "CANTIDAD DE SOLUCIONES: "
            "Solución ÚNICA."
        )

        print(
            "========================================================\n"
        )

        answers = []

        for row in clone:

            val = row[-1]

            if (
                isinstance(val, Fraction)
                and val.denominator == 1
            ):

                answers.append(val.numerator)

            else:

                answers.append(val)

        return (
            clone,
            columnas_pivote,
            variables_libres,
            answers,
            None
        )


def verificar_solucion(
    matriz_original,
    vector_b,
    soluciones
):

    for i in range(
        len(matriz_original)
    ):

        suma = sum(
            Fraction(matriz_original[i][j])
            * Fraction(soluciones[j])
            for j in range(len(soluciones))
        )

        if suma != Fraction(vector_b[i]):

            print(
                f"Alerta: la solución no satisface "
                f"la ecuación {i + 1}."
            )

            return False

    print(
        "Solución verificada correctamente."
    )

    return True


def es_homogeneo(vector_b):

    return all(
        Fraction(valor) == 0
        for valor in vector_b
    )


def crear_sistema():

    filas = modulo_matrices.asking_for_input(
        "Número de ecuaciones (m): ",
        type=int
    )

    columnas = modulo_matrices.asking_for_input(
        "Número de variables (n): ",
        type=int
    )

    A = modulo_matrices.Matrix(
        filas,
        columnas
    )

    print("\n--- INGRESO DE LA MATRIZ A ---")

    for i in range(filas):

        for j in range(columnas):

            valor = modulo_matrices.asking_for_input(
                f"A[{i + 1}][{j + 1}]: "
            )

            A.modify(
                i,
                j,
                valor
            )

    print("\n--- INGRESO DEL VECTOR b ---")

    b = []

    for i in range(filas):

        valor = modulo_matrices.asking_for_input(
            f"b[{i + 1}]: "
        )

        b.append(valor)

    return A, b


def resolver_sistema():

    encabezado()

    A, b = crear_sistema()

    matriz_original = [
        fila[:]
        for fila in A.array
    ]

    A.add_vector_b(b)

    print("\n--- MATRIZ AUMENTADA [A | b] ---")

    print(
        modulo_matrices.format_matrix(
            A.array
        )
    )

    (
        reducido,
        pivotes,
        libres,
        soluciones,
        forma_vectorial
    ) = gauss_jordan(A)

    print(
        "\n--- MATRIZ REDUCIDA ---"
    )

    print(
        modulo_matrices.format_matrix(
            reducido
        )
    )

    print(
        f"\nCantidad de pivotes: "
        f"{len(pivotes)}"
    )

    print(
        f"Variables libres: "
        f"{len(libres)}"
    )

    if soluciones is not None:

        print("\n[RESULTADO]")
        print("El sistema tiene SOLUCIÓN ÚNICA.")

        print("\nValores de las variables:")

        for i, solucion in enumerate(
            soluciones
        ):

            subindice = to_subscript(
                i + 1
            )

            print(
                f"x{subindice} = {solucion}"
            )

        print("\n--- VERIFICACIÓN ---")

        verificar_solucion(
            matriz_original,
            b,
            soluciones
        )

    elif forma_vectorial is not None:

        print("\n[RESULTADO]")
        print(
            "El sistema tiene INFINITAS SOLUCIONES."
        )

        print("\nForma vectorial:")
        print(forma_vectorial)

    else:

        print("\n[RESULTADO]")
        print("El sistema es INCONSISTENTE.")
        print("No existe ninguna solución.")


def verificar_homogeneidad():

    encabezado()

    A, b = crear_sistema()

    if es_homogeneo(b):

        print("\n[RESULTADO]")
        print("El sistema ES HOMOGÉNEO.")
        print("Tiene la forma Ax = 0.")

    else:

        print("\n[RESULTADO]")
        print("El sistema NO ES HOMOGÉNEO.")
        print(
            "El vector b contiene elementos "
            "diferentes de cero."
        )


def menu_sistemas():

    while True:

        encabezado()

        print("1. Resolver sistema Ax = b")
        print("2. Verificar sistema homogéneo")
        print("0. Ver Teoremas Clave del Módulo")
        print("9. Regresar al menú principal")

        opcion = modulo_matrices.asking_for_input(
            "\nSeleccione una opción: ",
            type=int
        )

        if opcion == 1:

            resolver_sistema()

        elif opcion == 2:

            verificar_homogeneidad()

        elif opcion == 0:

            resumen_teoremas.teoremas_sistemas()

        elif opcion == 9:

            break

        else:

            print("\n[ERROR] Opción no válida.")