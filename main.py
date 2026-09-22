#!/usr/bin/env python3
# Importar el módulo con la clase Matrix y funciones auxiliares
import matriz


def resolver_sistema_ecuacion_matricial():
    # Solicitar las dimensiones de la matriz al usuario
    filas = matriz.asking_for_input("Ingrese el numero de filas (m): ", type=int)
    columnas = matriz.asking_for_input(
        "Ingrese el numero de columnas (n): ", type=int
    )

    # Crear e inicializar la matriz con ceros
    matrix = matriz.Matrix(filas, columnas)
    print(f"\nMatriz {filas}x{columnas} inicializada.")

    # Solicitar los elementos de la matriz A posición por posición
    print("\n--- INGRESO DE VALORES PARA LA MATRIZ A ---")
    for i in range(filas):
        for j in range(columnas):
            valor = matriz.asking_for_input(
                f"Valor para la posicion [{i}][{j}]: ", type=float
            )
            matrix.modify(i, j, valor)

    # Solicitar los valores del vector independiente b
    print("\n--- INGRESO DE VALORES PARA EL VECTOR B ---")
    vector_b = []
    for i in range(filas):
        valor = matriz.asking_for_input(
            f"Valor del vector b para la fila {i + 1}: ", type=float
        )
        vector_b.append(valor)

    # Guardar una copia exacta de la matriz A para la verificación posterior
    matriz_original = [fila[:] for fila in matrix.array]

    # Unir la matriz A y el vector b para formar la matriz aumentada [A | b]
    matrix.add_vector_b(vector_b)
    print("\n--- MATRIZ AUMENTADA [A | b] ---")
    print(matriz.format_matrix(matrix.array))

    # Ejecutar la eliminación Gauss-Jordan y obtener el análisis del sistema
    matriz_rref, pivotes, libres, soluciones, forma_vectorial = (
        matrix.gauss_jordan()
    )
    # Dar formato de texto a las posiciones de pivotes y variables del sistema
    print("--- IDENTIFICACIÓN DE PIVOTES Y VARIABLES ---")
    cols_pivote_str = (
        ", ".join(str(p + 1) for p in pivotes) if pivotes else "Ninguna"
    )
    vars_basicas_str = (
        ", ".join(f"x{matriz.to_subscript(p + 1)}" for p in pivotes)
        if pivotes
        else "Ninguna"
    )
    vars_libres_str = (
        ", ".join(f"x{matriz.to_subscript(l + 1)}" for l in libres)
        if libres
        else "Ninguna"
    )

    # Imprimir resumen de variables básicas y libres
    print(f"Posición de las columnas pivote: {cols_pivote_str}")
    print(f"Variables Básicas: {vars_basicas_str}")
    print(f"Variables Libres : {vars_libres_str}\n")

    # Mostrar valores y verificar si el sistema tiene solución única
    if soluciones is not None:
        print("Valores de las variables (Solución Única):")
        for idx, sol in enumerate(soluciones):
            sub_indice = matriz.to_subscript(idx + 1)
            print(f"Variable x{sub_indice} = {matriz.formatear_numero(sol)}")

        print("\n--- VERIFICACIÓN AUTOMÁTICA ---")
        matriz.verificar_solucion(matriz_original, vector_b, soluciones)

    # Mostrar la solución en formato paramétrico y vectorial si hay infinitas soluciones
    elif forma_vectorial is not None:
        print("--- ESTRUCTURA DE LA SOLUCIÓN GENERAL (ESTILO PIZARRA) ---")
        print(forma_vectorial)
        print()


def ingresar_matriz_interactiva(nombre="A"):
    filas = matriz.asking_for_input(f"Ingrese las filas de la matriz {nombre}: ", type=int)
    cols = matriz.asking_for_input(f"Ingrese las columnas de la matriz {nombre}: ", type=int)
    m = matriz.Matrix(filas, cols)
    print(f"--- Valores de la Matriz {nombre} ---")
    for i in range(filas):
        for j in range(cols):
            v = matriz.asking_for_input(f"{nombre}[{i}][{j}]: ", type=float)
            m.modify(i, j, v)
    return m


def menu_vectores():
    print("\n--- MÓDULO DE VECTORES (R^n) ---")
    print("1. Suma / Resta de vectores")
    print("2. Multiplicación de vector por escalar")
    print("3. Evaluación de Combinación Lineal (b es comb. lineal de {v1, ..., vk})")
    op = matriz.asking_for_input("Seleccione una opción: ", type=int)

    if op in [1, 2]:
        dim = matriz.asking_for_input("Dimensión de los vectores (n): ", type=int)
        print("Ingrese el Vector 1:")
        v1 = [matriz.asking_for_input(f"v1[{i+1}]: ") for i in range(dim)]

        if op == 1:
            print("Ingrese el Vector 2:")
            v2 = [matriz.asking_for_input(f"v2[{i+1}]: ") for i in range(dim)]
            print(f"v1 + v2 = {matriz.vector_suma(v1, v2)}")
            print(f"v1 - v2 = {matriz.vector_resta(v1, v2)}")
        else:
            c = matriz.asking_for_input("Escalar c: ", type=float)
            print(f"c * v1 = {matriz.vector_por_escalar(c, v1)}")

    elif op == 3:
        n = matriz.asking_for_input("Dimensión n de los vectores: ", type=int)
        k = matriz.asking_for_input("Cantidad de vectores en el conjunto k: ", type=int)
        vectores = []
        for j in range(k):
            print(f"\nVector v_{j+1}:")
            v = [matriz.asking_for_input(f"v_{j+1}[{i+1}]: ") for i in range(n)]
            vectores.append(v)

        print("\nIngrese el vector b:")
        b = [matriz.asking_for_input(f"b[{i+1}]: ") for i in range(n)]

        es_comb, msg = matriz.es_combinacion_lineal(vectores, b)
        print(f"\nRESULTADO: {msg}")


def menu_operaciones_matriciales():
    print("\n--- MÓDULO DE OPERACIONES MATRICIALES BÁSICAS ---")
    print("1. Suma / Resta de matrices")
    print("2. Multiplicación de matriz por escalar")
    print("3. Multiplicación de matrices (A * B)")
    op = matriz.asking_for_input("Seleccione una opción: ", type=int)

    if op == 1:
        A = ingresar_matriz_interactiva("A")
        B = ingresar_matriz_interactiva("B")
        try:
            print("\n--- A + B ---")
            print(A.sumar(B))
            print("\n--- A - B ---")
            print(A.restar(B))
        except ValueError as e:
            print(f"Error: {e}")

    elif op == 2:
        A = ingresar_matriz_interactiva("A")
        c = matriz.asking_for_input("Escalar c: ", type=float)
        print("\n--- c * A ---")
        print(A.escalar_mult(c))

    elif op == 3:
        A = ingresar_matriz_interactiva("A")
        B = ingresar_matriz_interactiva("B")
        try:
            print("\n--- A * B ---")
            print(A.multiplicar(B))
        except ValueError as e:
            print(f"Error: {e}")


# Función principal para ejecutar la interfaz por consola
def main():
    while True:
        print("\n==========================================")
        print("     SISTEMA DE ÁLGEBRA LINEAL COMPUTACIONAL")
        print("==========================================")
        print("1. Resolver Ecuación Matricial (Ax = b)")
        print("2. Operaciones con Vectores (R^n)")
        print("3. Operaciones Matriciales Básicas")
        print("4. Salir")
        
        op = matriz.asking_for_input("Elija una opción (1-4): ", type=int)

        if op == 1:
            resolver_sistema_ecuacion_matricial()
        elif op == 2:
            menu_vectores()
        elif op == 3:
            menu_operaciones_matriciales()
        elif op == 4:
            print("¡Hasta luego!")
            break


# Bloque de ejecución principal
if __name__ == "__main__":
    main()