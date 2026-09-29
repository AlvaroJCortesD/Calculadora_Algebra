from modulos import modulo_vectores
from modulos import modulo_matrices
from modulos import modulo_sistemas
from modulos import modulo_determinantes


def main():

    while True:

        print("\n======================================================")
        print("           CALCULADORA DE ÁLGEBRA LINEAL")
        print("======================================================")

        print("1. Vectores e Independencia Lineal")
        print("2. Operaciones Matriciales")
        print("3. Sistemas de Ecuaciones Lineales")
        print("4. Determinantes")
        print("5. Salir")

        opcion = modulo_matrices.asking_for_input(
            "\nSeleccione una opción (1-5): ",
            type=int
        )

        if opcion == 1:

            modulo_vectores.menu_vectores()

        elif opcion == 2:

            modulo_matrices.menu_matrices()

        elif opcion == 3:

            modulo_sistemas.menu_sistemas()

        elif opcion == 4:

            modulo_determinantes.menu_determinantes()

        elif opcion == 5:

            print("\n¡Programa finalizado!")
            break

        else:

            print("\n[ERROR] Opción no válida.")


if __name__ == "__main__":
    main()