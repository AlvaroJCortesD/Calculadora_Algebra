"""
Módulo de Factorización LU.
Obtiene A = LU usando únicamente operaciones de reemplazo de fila (Fi <- Fi - l*Fj),
verifica L·U == A y resuelve Ax = b mediante sustitución hacia adelante (Ly = b)
y hacia atrás (Ux = y).

Son funciones puras: reciben listas anidadas y devuelven resultados (sin input ni print),
de modo que cada salida pueda pasar directamente como argumento de la siguiente función.
"""
from fractions import Fraction
from modulos.modulo_matrices import (
    matriz_desde_lista, identidad, producto, son_iguales
)
from modulos.modulo_sistemas import resolver_sistema_gauss_jordan_paso_a_paso

MENSAJE_PERMUTACION = (
    "La matriz no admite Factorización LU sin permutación "
    "(requiere pivoteo parcial PA = LU)"
)
MENSAJE_LU_OK = "La factorización es correcta (L · U == A)"
MENSAJE_LU_FALLA = "ERROR: la factorización NO es correcta (L · U ≠ A)"
MENSAJE_SOLUCION_OK = "Comprobación exitosa: A · x == b"
MENSAJE_SOLUCION_FALLA = "ERROR: la comprobación falló (A · x ≠ b)"

_LINEAS_LOGO = [
    "",
    "  _        _   _        A  =  L · U",
    " | |      | | | |",
    " | |      | | | |       L y = b   (adelante)",
    " | |____  | |_| |       U x = y   (atrás)",
    " |______|  \\___/",
    "",
    "  FACTORIZACIÓN LU  Y  SOLUCIÓN  A x = b",
    "",
]
LOGO_ASCII_LU = "\n".join(
    ["╔" + "═" * 46 + "╗"]
    + ["║" + linea.ljust(46) + "║" for linea in _LINEAS_LOGO]
    + ["╚" + "═" * 46 + "╝"]
)

MENU_LU = "0. Ver Teoremas Clave del Módulo"


class RequierePermutacionError(ValueError):
    """Se lanza cuando un pivote nulo exige intercambiar filas (A no admite LU directa)."""


def _texto_matriz(lista):
    """Formatea una lista anidada con el mismo estilo visual de la Calculadora."""
    return str(matriz_desde_lista(lista))


def _a_columna(b):
    """Normaliza b (lista plana o columna n x 1) a una lista anidada n x 1 de Fraction."""
    if len(b) == 0:
        raise ValueError("El vector b no puede estar vacío.")
    if isinstance(b[0], (list, tuple)):
        if any(len(fila) != 1 for fila in b):
            raise ValueError("El vector b debe ser una columna (n x 1).")
        return [[Fraction(fila[0])] for fila in b]
    return [[Fraction(x)] for x in b]


def factorizacion_lu(A):
    """
    Calcula A = L·U con operaciones de reemplazo de fila.
    Devuelve (L, U, historial): L es m x m triangular inferior con unos en la diagonal,
    U es m x n escalonada y el historial lista cada paso de eliminación.
    Lanza RequierePermutacionError si un pivote nulo obliga a intercambiar filas.
    """
    m = len(A)
    n = len(A[0])
    U = [[Fraction(x) for x in fila] for fila in A]
    L = identidad(m)
    historial = []
    fila_pivote = 0

    for col in range(n):
        if fila_pivote >= m:
            break
        pivote = U[fila_pivote][col]

        if pivote == 0:
            # Con elementos no nulos debajo del pivote cero haría falta permutar filas.
            if any(U[i][col] != 0 for i in range(fila_pivote + 1, m)):
                raise RequierePermutacionError(MENSAJE_PERMUTACION)
            # Columna sin pivote: no se avanza de fila (variable libre), nada que eliminar.
            historial.append({"columna": col, "fila": fila_pivote, "pivote": None,
                              "operaciones": [], "U": [f[:] for f in U]})
            continue

        operaciones = []
        for i in range(fila_pivote + 1, m):
            if U[i][col] != 0:
                # Multiplicador l = elemento a eliminar / pivote; se guarda en L[i][pivote].
                l = U[i][col] / pivote
                for j in range(col, n):
                    U[i][j] -= l * U[fila_pivote][j]
                L[i][fila_pivote] = l
                operaciones.append((i, fila_pivote, l))
        historial.append({"columna": col, "fila": fila_pivote, "pivote": pivote,
                          "operaciones": operaciones, "U": [f[:] for f in U]})
        fila_pivote += 1

    return L, U, historial


def procedimiento_factorizacion(A, L, U, historial):
    """Construye el texto paso a paso de la obtención de U y el registro de L."""
    pasos = [
        "======================================================",
        "   FACTORIZACIÓN LU (solo reemplazos de fila)",
        "   Fi <- Fi - l·Fj   con   l = elemento a eliminar / pivote",
        "======================================================",
        "\nMatriz A inicial:",
        _texto_matriz(A),
    ]
    for paso in historial:
        c, r = paso["columna"] + 1, paso["fila"] + 1
        if paso["pivote"] is None:
            pasos.append(f"\n--- COLUMNA {c}: sin pivote en la fila {r} (se continúa con la siguiente columna) ---")
            continue
        pasos.append(f"\n--- COLUMNA {c}: pivote = {paso['pivote']} en A[{r}][{c}] ---")
        if not paso["operaciones"]:
            pasos.append("Nada que eliminar debajo del pivote.")
        for i, j, l in paso["operaciones"]:
            pasos.append(f"F{i + 1} <- F{i + 1} - ({l}) · F{j + 1}      guardamos L[{i + 1}][{j + 1}] = {l}")
        pasos.append("U parcial:")
        pasos.append(_texto_matriz(paso["U"]))
    pasos.append("\n--- MATRIZ L (triangular inferior, unos en la diagonal) ---")
    pasos.append(_texto_matriz(L))
    pasos.append("\n--- MATRIZ U (forma escalonada) ---")
    pasos.append(_texto_matriz(U))
    return "\n".join(pasos)


def lu_paso_a_paso(A):
    """Devuelve (L, U, procedimiento_str) de la factorización A = LU."""
    L, U, historial = factorizacion_lu(A)
    return L, U, procedimiento_factorizacion(A, L, U, historial)


def verificar_factorizacion(A, L, U):
    """Multiplica L·U con el producto de la Calculadora. Devuelve (es_correcta, L·U)."""
    LU = producto(L, U)
    return son_iguales(LU, A), LU


def _resolver_por_reduccion(M, rhs):
    """Resuelve M z = rhs por Gauss-Jordan sobre [M | rhs] reutilizando modulo_sistemas."""
    z, texto = resolver_sistema_gauss_jordan_paso_a_paso(
        matriz_desde_lista(M), matriz_desde_lista(rhs)
    )
    return (z.array if z is not None else None), texto


def sustitucion_adelante(L, b):
    """Resuelve L y = b reduciendo [L | b]. Devuelve (y_columna, procedimiento_str)."""
    return _resolver_por_reduccion(L, _a_columna(b))


def sustitucion_atras(U, y):
    """Resuelve U x = y reduciendo [U | y]. Devuelve (x_columna o None, procedimiento_str)."""
    return _resolver_por_reduccion(U, _a_columna(y))


def resolver_lu(A, b):
    """
    Flujo completo: A = LU, verificación L·U == A y, si A es cuadrada, Ax = b en dos etapas.
    Devuelve un diccionario con L, U, y, x (listas anidadas o None), los booleanos
    lu_correcta y solucion_correcta, y el texto 'procedimiento'.
    Lanza RequierePermutacionError si A no admite LU sin permutación.
    """
    b_col = _a_columna(b)
    if len(b_col) != len(A):
        raise ValueError(f"El vector b debe tener {len(A)} componentes; tiene {len(b_col)}.")

    L, U, historial = factorizacion_lu(A)
    texto = [procedimiento_factorizacion(A, L, U, historial)]

    lu_ok, LU = verificar_factorizacion(A, L, U)
    texto.append("\n--- VERIFICACIÓN DE LA FACTORIZACIÓN ---")
    texto.append("L · U =")
    texto.append(_texto_matriz(LU))
    texto.append(MENSAJE_LU_OK if lu_ok else MENSAJE_LU_FALLA)

    resultado = {"L": L, "U": U, "y": None, "x": None,
                 "lu_correcta": lu_ok, "solucion_correcta": None}

    if len(A) != len(A[0]):
        texto.append(
            f"\nA es {len(A)}x{len(A[0])}: la resolución de Ax = b mediante LU se realiza "
            "solo para matrices cuadradas n x n."
        )
        resultado["procedimiento"] = "\n".join(texto)
        return resultado

    texto.append("\n######## ETAPA 1: SUSTITUCIÓN HACIA ADELANTE  L y = b ########")
    y, texto_y = sustitucion_adelante(L, b_col)
    texto.append(texto_y)
    resultado["y"] = y

    if y is not None:
        texto.append("\n######## ETAPA 2: SUSTITUCIÓN HACIA ATRÁS  U x = y ########")
        x, texto_x = sustitucion_atras(U, y)
        texto.append(texto_x)
        resultado["x"] = x

        if x is None:
            texto.append("\nA es singular: el sistema no tiene solución única.")
        else:
            ok = son_iguales(producto(A, x), b_col)
            resultado["solucion_correcta"] = ok
            texto.append("\n--- VECTOR INTERMEDIO y ---")
            texto.append(_texto_matriz(y))
            texto.append("\n--- VECTOR SOLUCIÓN x ---")
            texto.append(_texto_matriz(x))
            texto.append("\nA · x =")
            texto.append(_texto_matriz(producto(A, x)))
            texto.append(MENSAJE_SOLUCION_OK if ok else MENSAJE_SOLUCION_FALLA)

    resultado["procedimiento"] = "\n".join(texto)
    return resultado


def teoremas_lu():
    """Devuelve el texto de los teoremas clave de la factorización LU."""
    return "\n".join([
        "======================================================",
        "          TEOREMAS CLAVE: FACTORIZACIÓN LU",
        "======================================================",
        "",
        "1. EXISTENCIA",
        "Si A (m x n) se reduce a forma escalonada U usando solo",
        "reemplazos de fila (sin intercambios), entonces A = L·U.",
        "",
        "2. FORMA DE L",
        "L es m x m, triangular inferior con unos en la diagonal.",
        "En la posición (i,j) guarda el multiplicador l usado en",
        "Fi <- Fi - l·Fj.",
        "",
        "3. FORMA DE U",
        "U es m x n y es la forma escalonada de A.",
        "",
        "4. MULTIPLICADOR",
        "l = (elemento a eliminar) / (pivote).",
        "",
        "5. SOLUCIÓN EN DOS ETAPAS",
        "Si A = L·U, entonces Ax = b equivale a:",
        "   L y = b   (sustitución hacia adelante)",
        "   U x = y   (sustitución hacia atrás)",
        "",
        "6. PIVOTE NULO",
        "Si un pivote es 0 y hay que intercambiar filas, A no admite",
        "LU directa; se requiere pivoteo parcial: P A = L U.",
        "",
        "7. DETERMINANTE",
        "Si A = L·U es cuadrada, det(A) = det(U) = producto de la",
        "diagonal de U (porque det(L) = 1).",
        "",
        "8. INVERTIBILIDAD",
        "A cuadrada es invertible si y solo si U tiene n pivotes",
        "(sin ceros en su diagonal).",
        "",
        "9. VERIFICACIÓN",
        "Siempre se comprueba L·U == A y A·x == b.",
        "",
        "======================================================",
    ])