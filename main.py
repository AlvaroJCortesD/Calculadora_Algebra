#! /usr/bin/env python3
# Importar el módulo con la clase Matrix y funciones auxiliares
import matriz


# Función principal para ejecutar la interfaz por consola
def main():
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
    print(matrix)

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


# Bloque de ejecución principal
if __name__ == "__main__":
    main()



#.