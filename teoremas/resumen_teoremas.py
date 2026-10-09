# ======================================================
# TEOREMAS Y PROPIEDADES DE ÁLGEBRA LINEAL
# ======================================================
import io
import sys


def teoremas_vectores():
    print("\n======================================================")
    print("              TEOREMAS CLAVE: VECTORES")
    print("======================================================")

    print("\n1. COMBINACIÓN LINEAL")
    print("Un vector b es combinación lineal de otros vectores")
    print("si puede escribirse como:")
    print("b = c₁v₁ + c₂v₂ + ... + cₖvₖ")

    print("\n2. INDEPENDENCIA LINEAL")
    print("Los vectores son linealmente independientes (L.I.)")
    print("si la única solución de:")
    print("c₁v₁ + c₂v₂ + ... + cₖvₖ = 0")
    print("es:")
    print("c₁ = c₂ = ... = cₖ = 0")

    print("\n3. DEPENDENCIA LINEAL")
    print("Los vectores son linealmente dependientes (L.D.)")
    print("si existe una solución NO TRIVIAL del sistema:")
    print("Ax = 0")

    print("\n4. CRITERIO DE PIVOTES")
    print("Si cada columna tiene pivote, los vectores son L.I.")
    print("Si existe una variable libre, los vectores son L.D.")

    print("\n5. VECTOR CERO")
    print("Un conjunto que contiene al vector cero")
    print("es linealmente dependiente.")

    print("\n6. CANTIDAD DE VECTORES")
    print("Si hay más vectores que la dimensión del espacio,")
    print("los vectores son necesariamente linealmente dependientes.")

    print("\n7. BASE")
    print("Una base de un espacio vectorial es un conjunto")
    print("de vectores linealmente independientes que genera")
    print("todo el espacio.")

    print("\n======================================================")


def teoremas_matrices():
    print("\n======================================================")
    print("              TEOREMAS CLAVE: MATRICES")
    print("======================================================")

    print("\n1. MATRIZ INVERSA")
    print("Una matriz cuadrada A tiene inversa si:")
    print("A · A⁻¹ = I")

    print("\n2. MATRIZ IDENTIDAD")
    print("La matriz identidad I tiene 1 en la diagonal")
    print("principal y 0 en las demás posiciones.")

    print("\n3. PRODUCTO DE MATRICES")
    print("Para multiplicar A · B:")
    print("el número de columnas de A debe ser igual")
    print("al número de filas de B.")

    print("\n4. TRASPOSICIÓN")
    print("La traspuesta intercambia filas por columnas.")

    print("\n5. PRODUCTO MATRIZ-VECTOR")
    print("Si A es una matriz de m × n y u es un vector")
    print("con n componentes, el producto Au está definido.")
    print("El resultado es un vector con m componentes.")

    print("\n6. PROPIEDAD DISTRIBUTIVA")
    print("El producto de una matriz por una suma de vectores")
    print("cumple:")
    print("A(u + v) = Au + Av")

    print("\n7. COMPATIBILIDAD CON ESCALARES")
    print("Si c es un escalar y u es un vector:")
    print("A(cu) = c(Au)")

    print("\n8. NO CONMUTATIVIDAD")
    print("En general, el producto de matrices")
    print("no es conmutativo:")
    print("A · B ≠ B · A")

    print("\n9. TRASPOSICIÓN DE UN PRODUCTO")
    print("La traspuesta de un producto invierte")
    print("el orden de las matrices:")
    print("(A · B)ᵀ = Bᵀ · Aᵀ")

    print("\n10. INVERSA DE UN PRODUCTO")
    print("Si A y B son matrices invertibles:")
    print("(A · B)⁻¹ = B⁻¹ · A⁻¹")

    print("\n======================================================")


def teoremas_sistemas():
    print("\n======================================================")
    print("              TEOREMAS CLAVE: SISTEMAS")
    print("======================================================")

    print("\n1. SISTEMA HOMOGÉNEO")
    print("Un sistema homogéneo tiene la forma:")
    print("Ax = 0")

    print("\n2. SISTEMA CONSISTENTE")
    print("Un sistema es consistente si tiene")
    print("al menos una solución.")

    print("\n3. SISTEMA INCONSISTENTE")
    print("Un sistema es inconsistente si")
    print("no tiene ninguna solución.")

    print("\n4. GAUSS-JORDAN")
    print("Permite transformar una matriz mediante operaciones")
    print("elementales hasta obtener su forma escalonada reducida.")

    print("\n5. SOLUCIÓN TRIVIAL")
    print("Todo sistema homogéneo Ax = 0 siempre tiene")
    print("al menos la solución:")
    print("x = 0")

    print("\n6. SOLUCIÓN ÚNICA")
    print("Un sistema tiene solución única cuando")
    print("no existen variables libres.")

    print("\n7. INFINITAS SOLUCIONES")
    print("Un sistema consistente tiene infinitas soluciones")
    print("cuando existe al menos una variable libre.")

    print("\n8. CRITERIO DE INCONSISTENCIA")
    print("Si aparece una fila de la forma:")
    print("[ 0  0  ...  0 | k ]")
    print("con k ≠ 0, el sistema es inconsistente.")

    print("\n9. RANGO")
    print("El rango de una matriz es la cantidad de pivotes")
    print("que aparecen después de reducirla.")

    print("\n10. TEOREMA RANGO-NULIDAD")
    print("Para una matriz A con n columnas:")
    print("rango(A) + nulidad(A) = n")

    print("\n======================================================")


def teoremas_determinantes():
    print("\n======================================================")
    print("            TEOREMAS CLAVE: DETERMINANTES")
    print("======================================================")

    print("\n1. MATRIZ SINGULAR")
    print("Si det(A) = 0, la matriz no tiene inversa.")

    print("\n2. MATRIZ NO SINGULAR")
    print("Si det(A) ≠ 0, la matriz tiene inversa.")

    print("\n3. INTERCAMBIO DE FILAS")
    print("Al intercambiar dos filas, el determinante cambia")
    print("de signo.")

    print("\n4. FILA DE CEROS")
    print("Si una matriz tiene una fila completamente cero,")
    print("su determinante es 0.")

    print("\n5. DOS FILAS IGUALES")
    print("Si una matriz tiene dos filas iguales,")
    print("su determinante es 0.")

    print("\n6. OPERACIONES ELEMENTALES")
    print("Sumar a una fila un múltiplo de otra fila")
    print("no cambia el valor del determinante.")

    print("\n7. DETERMINANTE DE LA MATRIZ IDENTIDAD")
    print("El determinante de la matriz identidad es:")
    print("det(I) = 1")

    print("\n8. DETERMINANTE DE UN PRODUCTO")
    print("El determinante del producto de dos matrices")
    print("es igual al producto de sus determinantes:")
    print("det(A · B) = det(A) · det(B)")

    print("\n9. DETERMINANTE DE LA TRASPUESTA")
    print("El determinante de una matriz es igual")
    print("al determinante de su traspuesta:")
    print("det(Aᵀ) = det(A)")

    print("\n10. MATRIZ TRIANGULAR")
    print("El determinante de una matriz triangular")
    print("es el producto de los elementos de su diagonal.")

    print("\n======================================================")


def capturar_salida(func):
    """Ejecuta una función e intercepta sus print() para retornarlos como texto."""
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        func()
    finally:
        sys.stdout = sys.__stdout__
    return buffer.getvalue()


def obtener_todos_teoremas():
    """Concatena todas las secciones de teoremas para mostrarlas en la GUI."""
    texto = ""
    texto += capturar_salida(teoremas_vectores)
    texto += capturar_salida(teoremas_sistemas)
    texto += capturar_salida(teoremas_matrices)
    texto += capturar_salida(teoremas_determinantes)
    return texto