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

    print("\n======================================================")


def teoremas_sistemas():
    print("\n======================================================")
    print("              TEOREMAS CLAVE: SISTEMAS")
    print("======================================================")

    print("\n1. SISTEMA HOMOGÉNEO")
    print("Un sistema homogéneo tiene la forma:")
    print("Ax = 0")

    print("\n2. SISTEMA CONSISTENTE")
    print("Tiene al menos una solución.")

    print("\n3. SISTEMA INCONSISTENTE")
    print("No tiene ninguna solución.")

    print("\n4. GAUSS-JORDAN")
    print("Permite transformar una matriz mediante operaciones")
    print("elementales hasta obtener su forma escalonada reducida.")

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

    print("\n======================================================")