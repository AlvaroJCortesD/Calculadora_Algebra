from fractions import Fraction

from modulos import modulo_matrices
from teoremas import resumen_teoremas


def encabezado():

    print("\n======================================================")
    print("          MÓDULO: DETERMINANTES")
    print("          Cálculo y propiedades")
    print("======================================================")


def crear_matriz_cuadrada():

    n = modulo_matrices.asking_for_input(
        "Orden de la matriz cuadrada: ",
        type=int
    )

    A = modulo_matrices.Matrix(n, n)

    print("\n--- INGRESO DE DATOS DE LA MATRIZ ---")

    for i in range(n):

        for j in range(n):

            valor = modulo_matrices.asking_for_input(
                f"A[{i + 1}][{j + 1}]: "
            )

            A.modify(
                i,
                j,
                valor
            )

    return A


def calcular_determinante(A):

    # El determinante solamente existe
    # para matrices cuadradas.
    if A.rows != A.columns:

        raise ValueError(
            "El determinante solamente existe "
            "para matrices cuadradas."
        )

    # Creamos una copia de la matriz.
    matriz_temp = [
        [
            Fraction(valor)
            for valor in fila
        ]
        for fila in A.array
    ]

    n = len(matriz_temp)

    determinante = Fraction(1)

    # Reducción por filas.
    for columna in range(n):

        fila_pivote = None

        # Buscar un pivote diferente de cero.
        for fila in range(columna, n):

            if matriz_temp[fila][columna] != 0:

                fila_pivote = fila
                break

        # Si no existe pivote,
        # el determinante es cero.
        if fila_pivote is None:

            return Fraction(0)

        # Si hay que intercambiar filas,
        # cambia el signo del determinante.
        if fila_pivote != columna:

            matriz_temp[columna], matriz_temp[fila_pivote] = (
                matriz_temp[fila_pivote],
                matriz_temp[columna]
            )

            determinante *= -1

        # Guardamos el pivote.
        pivote = matriz_temp[columna][columna]

        # Multiplicamos el determinante
        # por el pivote.
        determinante *= pivote

        # Hacemos cero debajo del pivote.
        for fila in range(columna + 1, n):

            factor = (
                matriz_temp[fila][columna]
                / pivote
            )

            for j in range(columna, n):

                matriz_temp[fila][j] -= (
                    factor
                    * matriz_temp[columna][j]
                )

    return determinante


def calcular():

    encabezado()

    A = crear_matriz_cuadrada()

    print("\n--- MATRIZ A ---")
    print(A)

    try:

        determinante = calcular_determinante(A)

        print("\n--- RESULTADO ---")
        print(f"det(A) = {determinante}")

        if determinante == 0:

            print("\nLa matriz es SINGULAR.")
            print("La matriz NO tiene inversa.")

        else:

            print("\nLa matriz es NO SINGULAR.")
            print("La matriz SÍ tiene inversa.")

    except ValueError as e:

        print(f"\n[ERROR]: {e}")


def menu_determinantes():

    while True:

        encabezado()

        print("1. Calcular determinante")
        print("0. Ver Teoremas Clave del Módulo")
        print("9. Regresar al menú principal")

        opcion = modulo_matrices.asking_for_input(
            "\nSeleccione una opción: ",
            type=int
        )

        if opcion == 1:

            calcular()

        elif opcion == 0:

            resumen_teoremas.teoremas_determinantes()

        elif opcion == 9:

            break

        else:

            print("\n[ERROR] Opción no válida.")