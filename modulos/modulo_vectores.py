from fractions import Fraction
from modulos import modulo_matrices
from modulos import modulo_sistemas
from teoremas import resumen_teoremas


# Muestra el encabezado del módulo de vectores.
def encabezado():
    print("\n======================================================")
    print("        MÓDULO: VECTORES E INDEPENDENCIA LINEAL")
    print("        Combinaciones Lineales, L.I. y L.D.")
    print("                         Ax = 0")
    print("======================================================")


# Suma dos vectores de la misma dimensión.
def sumar_vectores(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [Fraction(u[i]) + Fraction(v[i]) for i in range(len(u))]


# Resta dos vectores de la misma dimensión.
def restar_vectores(u, v):
    if len(u) != len(v):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return [Fraction(u[i]) - Fraction(v[i]) for i in range(len(u))]


# Multiplica cada componente del vector por un escalar.
def escalar_por_vector(c, v):
    return [Fraction(c) * Fraction(x) for x in v]


# Solicita los vectores y los almacena como columnas de una matriz.
def leer_vectores():
    print("\n--- DATOS DEL CONJUNTO DE VECTORES ---")

    k = modulo_matrices.asking_for_input(
        "Cantidad de vectores (k): ", type=int
    )

    n = modulo_matrices.asking_for_input(
        "Dimensión de los vectores (n): ", type=int
    )

    A = modulo_matrices.Matrix(n, k)

    print("\nIngrese los vectores.")
    print("Cada vector será almacenado como una columna.")

    for j in range(k):
        print(f"\nVector v{j + 1}:")

        for i in range(n):
            valor = modulo_matrices.asking_for_input(
                f"v{j + 1}[{i + 1}]: "
            )
            A.modify(i, j, valor)

    return A, k, n


# Determina si los vectores son linealmente independientes o dependientes.
def independencia_lineal():
    encabezado()

    # Se reciben los vectores y se construye la matriz A.
    A, k, n = leer_vectores()

    print("\n--- MATRIZ DE LOS VECTORES ---")
    print(A)

    # Se construye el sistema homogéneo Ax = 0.
    print("\nConstruyendo el sistema homogéneo:")
    print("Ax = 0")

    sistema = modulo_matrices.Matrix(n, k)

    for i in range(n):
        for j in range(k):
            sistema.modify(i, j, A.array[i][j])

    vector_cero = [Fraction(0) for _ in range(n)]
    sistema.add_vector_b(vector_cero)

    # Se aplica Gauss-Jordan para encontrar pivotes y variables libres.
    print("\n--- REDUCCIÓN POR GAUSS-JORDAN ---")

    reducido, pivotes, libres, _, _ = modulo_sistemas.gauss_jordan(
        sistema
    )

    print("\n--- MATRIZ REDUCIDA ---")
    print(modulo_matrices.format_matrix(reducido))

    print("\n--- RESULTADO DEL ANÁLISIS ---")
    print(f"Cantidad de vectores: {k}")
    print(f"Dimensión: {n}")
    print(f"Cantidad de pivotes: {len(pivotes)}")
    print(f"Cantidad de variables libres: {len(libres)}")

    # Si existen variables libres, los vectores son dependientes.
    if libres:
        print("\n[RESULTADO]")
        print("Los vectores son LINEALMENTE DEPENDIENTES (L.D.).")
        print("Existe al menos una variable libre.")

    # Si no existen variables libres, son independientes.
    else:
        print("\n[RESULTADO]")
        print("Los vectores son LINEALMENTE INDEPENDIENTES (L.I.).")
        print("La única solución de Ax = 0 es la solución trivial.")


# Permite realizar operaciones básicas entre dos vectores.
def operaciones_vectores():
    encabezado()

    n = modulo_matrices.asking_for_input(
        "Dimensión de los vectores: ", type=int
    )

    print("\nVector u:")
    u = [
        modulo_matrices.asking_for_input(f"u[{i + 1}]: ")
        for i in range(n)
    ]

    print("\nVector v:")
    v = [
        modulo_matrices.asking_for_input(f"v[{i + 1}]: ")
        for i in range(n)
    ]

    print("\n--- RESULTADOS ---")

    print("\nu + v =")
    modulo_matrices.mostrar_vector(sumar_vectores(u, v))

    print("\nu - v =")
    modulo_matrices.mostrar_vector(restar_vectores(u, v))

    c = modulo_matrices.asking_for_input("\nEscalar c: ")

    print("\nc · u =")
    modulo_matrices.mostrar_vector(escalar_por_vector(c, u))


# Comprueba si b puede expresarse como combinación lineal de los vectores.
def es_combinacion_lineal(conjunto_vectores, b):
    m = len(b)
    k = len(conjunto_vectores)

    A = modulo_matrices.Matrix(m, k)

    # Los vectores se colocan como columnas de la matriz.
    for j in range(k):
        if len(conjunto_vectores[j]) != m:
            raise ValueError(
                "Todos los vectores deben tener la misma dimensión que b."
            )

        for i in range(m):
            A.modify(i, j, conjunto_vectores[j][i])

    # Se agrega b para resolver Ax = b.
    A.add_vector_b(b)

    _, _, _, soluciones, forma_vectorial = (
        modulo_sistemas.gauss_jordan(A)
    )

    return soluciones is not None or forma_vectorial is not None

# Solicita un conjunto de vectores y determina si b es combinación lineal.
def combinacion_lineal():

    encabezado()

    n = modulo_matrices.asking_for_input(
        "Dimensión de los vectores: ",
        type=int
    )

    k = modulo_matrices.asking_for_input(
        "Cantidad de vectores: ",
        type=int
    )

    conjunto = []

    for j in range(k):

        print(f"\nVector v{j + 1}:")

        vector = [
            modulo_matrices.asking_for_input(
                f"v{j + 1}[{i + 1}]: "
            )
            for i in range(n)
        ]

        conjunto.append(vector)

    print("\nVector b:")

    b = [
        modulo_matrices.asking_for_input(
            f"b[{i + 1}]: "
        )
        for i in range(n)
    ]

    resultado = es_combinacion_lineal(
        conjunto,
        b
    )

    if resultado:

        print("\n[RESULTADO]")
        print(
            "b SÍ es combinación lineal "
            "de los vectores."
        )

    else:

        print("\n[RESULTADO]")
        print(
            "b NO es combinación lineal "
            "de los vectores."
        )


def es_combinacion_lineal(
    conjunto_vectores,
    b
):

    m = len(b)
    k = len(conjunto_vectores)

    A = modulo_matrices.Matrix(m, k)

    for j in range(k):

        if len(conjunto_vectores[j]) != m:

            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimensión que b."
            )

        for i in range(m):

            A.modify(
                i,
                j,
                conjunto_vectores[j][i]
            )

    A.add_vector_b(b)

    _, _, _, soluciones, forma_vectorial = (
        modulo_sistemas.gauss_jordan(A)
    )

    return (
        soluciones is not None
        or forma_vectorial is not None
    )


def menu_vectores():

    while True:

        encabezado()

        print("1. Operaciones con vectores")
        print("2. Combinación lineal")
        print("3. Independencia lineal")
        print("0. Ver Teoremas Clave del Módulo")
        print("9. Regresar al menú principal")

        opcion = modulo_matrices.asking_for_input(
            "\nSeleccione una opción: ",
            type=int
        )

        if opcion == 1:

            operaciones_vectores()

        elif opcion == 2:

            combinacion_lineal()

        elif opcion == 3:

            independencia_lineal()

        elif opcion == 0:

            resumen_teoremas.teoremas_vectores()

        elif opcion == 9:

            break

        else:

            print("\n[ERROR] Opción no válida.")