"""
Módulo Verificador de Propiedades.
Para cada teorema calcula AMBOS miembros de la igualdad con las funciones internas de la
Calculadora (modulo_matrices) y diagnostica "Se cumple" o "No se cumple". Si las dimensiones
o la invertibilidad no permiten evaluar una propiedad, la marca como "No aplicable" y explica
el motivo.

Son funciones puras sobre listas anidadas: los resultados intermedios (por ejemplo AB) se
calculan una sola vez, se guardan en variables y se reutilizan como argumentos.
"""
from fractions import Fraction
from modulos.modulo_matrices import (
    fmt_val, identidad, producto, transpuesta, suma, escalar,
    inversa, determinante, son_iguales
)
from modulos.modulo_determinantes import determinante_cofactores

SE_CUMPLE = "Se cumple"
NO_SE_CUMPLE = "No se cumple"
NO_APLICABLE = "No aplicable"

CAT_TRANSPOSICION = "Operaciones y transposición"
CAT_INVERSA = "Matriz inversa"
CAT_DETERMINANTES = "Determinantes"


class PropiedadNoAplicable(ValueError):
    """Se lanza cuando faltan datos o las dimensiones no permiten evaluar la propiedad."""


# ----------------------------------------------------------------------
# Utilidades internas
# ----------------------------------------------------------------------

def _requerir(matriz, nombre):
    """Falla con PropiedadNoAplicable si la matriz opcional no fue proporcionada."""
    if matriz is None:
        raise PropiedadNoAplicable(f"falta la matriz {nombre}")
    return matriz


def _requerir_cuadrada(matriz, nombre):
    """Falla con PropiedadNoAplicable si la matriz no es cuadrada."""
    _requerir(matriz, nombre)
    if len(matriz) != len(matriz[0]):
        raise PropiedadNoAplicable(f"{nombre} debe ser cuadrada")
    return matriz


def _invertir(matriz, nombre):
    """Inversa de una matriz cuadrada; PropiedadNoAplicable si es singular."""
    _requerir_cuadrada(matriz, nombre)
    try:
        return inversa(matriz)
    except ValueError:
        raise PropiedadNoAplicable(f"{nombre} es singular (det = 0), no tiene inversa")


def _intercambiar_filas(A, i, j):
    """Copia de A con las filas i y j intercambiadas."""
    R = [fila[:] for fila in A]
    R[i], R[j] = R[j], R[i]
    return R


def _reemplazar_fila(A, destino, origen, k):
    """Copia de A con Fdestino <- Fdestino + k·Forigen."""
    R = [fila[:] for fila in A]
    R[destino] = [Fraction(a) + k * Fraction(b) for a, b in zip(R[destino], R[origen])]
    return R


def _escalar_fila(A, i, k):
    """Copia de A con la fila i multiplicada por k."""
    R = [fila[:] for fila in A]
    R[i] = [k * Fraction(a) for a in R[i]]
    return R


def _triangular_superior(A):
    """Copia de A con ceros bajo la diagonal."""
    return [[A[i][j] if j >= i else Fraction(0) for j in range(len(A))] for i in range(len(A))]


def _triangular_inferior(A):
    """Copia de A con ceros sobre la diagonal."""
    return [[A[i][j] if j <= i else Fraction(0) for j in range(len(A))] for i in range(len(A))]


def _producto_diagonal(T):
    """Producto de los elementos de la diagonal principal."""
    p = Fraction(1)
    for i in range(len(T)):
        p *= Fraction(T[i][i])
    return p


def _en_linea(valor):
    """Representa un escalar o una lista anidada en una sola línea."""
    if isinstance(valor, list):
        return "[ " + " ; ".join("  ".join(fmt_val(Fraction(x)) for x in fila) for fila in valor) + " ]"
    return fmt_val(Fraction(valor))


def _det_por_cofactores(T):
    """Determinante por cofactores (método independiente); para n > 7 usa reducción triangular."""
    # La expansión por cofactores cuesta n! operaciones, por eso se limita a matrices pequeñas.
    return determinante_cofactores(T) if len(T) <= 7 else determinante(T)


def _iguales(izq, der):
    """Compara dos miembros, sean escalares o listas anidadas."""
    if isinstance(izq, list):
        return son_iguales(izq, der)
    return Fraction(izq) == Fraction(der)


# ----------------------------------------------------------------------
# Propiedades: cada una devuelve (miembro_izquierdo, miembro_derecho)
# ----------------------------------------------------------------------

def _p_transpuesta_doble(A, B, C, k):
    """Miembros de (Aᵀ)ᵀ = A."""
    return transpuesta(transpuesta(A)), A


def _p_transpuesta_suma(A, B, C, k):
    """Miembros de (A + B)ᵀ = Aᵀ + Bᵀ."""
    _requerir(B, "B")
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise PropiedadNoAplicable("A y B deben tener el mismo tamaño")
    return transpuesta(suma(A, B)), suma(transpuesta(A), transpuesta(B))


def _p_transpuesta_escalar(A, B, C, k):
    """Miembros de (kA)ᵀ = kAᵀ."""
    return transpuesta(escalar(k, A)), escalar(k, transpuesta(A))


def _p_transpuesta_producto(A, B, C, k):
    """Miembros de (AB)ᵀ = BᵀAᵀ; AB se calcula una vez y se reutiliza."""
    _requerir(B, "B")
    if len(A[0]) != len(B):
        raise PropiedadNoAplicable("columnas de A deben ser iguales a filas de B")
    AB = producto(A, B)
    izquierda = transpuesta(AB)
    derecha = producto(transpuesta(B), transpuesta(A))
    return izquierda, derecha


def _p_distributiva(A, B, C, k):
    """Miembros de A(B + C) = AB + AC."""
    _requerir(B, "B")
    _requerir(C, "C")
    if len(B) != len(C) or len(B[0]) != len(C[0]):
        raise PropiedadNoAplicable("B y C deben tener el mismo tamaño")
    if len(A[0]) != len(B):
        raise PropiedadNoAplicable("columnas de A deben ser iguales a filas de B y C")
    izquierda = producto(A, suma(B, C))
    derecha = suma(producto(A, B), producto(A, C))
    return izquierda, derecha


def _p_asociativa(A, B, C, k):
    """Miembros de (AB)C = A(BC)."""
    _requerir(B, "B")
    _requerir(C, "C")
    if len(A[0]) != len(B) or len(B[0]) != len(C):
        raise PropiedadNoAplicable("las dimensiones no permiten A·B·C")
    AB = producto(A, B)
    BC = producto(B, C)
    return producto(AB, C), producto(A, BC)


def _p_inversa_doble(A, B, C, k):
    """Miembros de (A⁻¹)⁻¹ = A."""
    Ainv = _invertir(A, "A")
    return inversa(Ainv), A


def _p_inversa_producto(A, B, C, k):
    """Miembros de (AB)⁻¹ = B⁻¹A⁻¹."""
    _requerir_cuadrada(A, "A")
    _requerir_cuadrada(B, "B")
    if len(A) != len(B):
        raise PropiedadNoAplicable("A y B deben tener el mismo orden")
    Ainv = _invertir(A, "A")
    Binv = _invertir(B, "B")
    AB = producto(A, B)
    return inversa(AB), producto(Binv, Ainv)


def _p_inversa_transpuesta(A, B, C, k):
    """Miembros de (Aᵀ)⁻¹ = (A⁻¹)ᵀ."""
    Ainv = _invertir(A, "A")
    return inversa(transpuesta(A)), transpuesta(Ainv)


def _p_a_por_inversa(A, B, C, k):
    """Miembros de A · A⁻¹ = I."""
    Ainv = _invertir(A, "A")
    return producto(A, Ainv), identidad(len(A))


def _p_det_transpuesta(A, B, C, k):
    """Miembros de det(Aᵀ) = det(A)."""
    _requerir_cuadrada(A, "A")
    return determinante(transpuesta(A)), determinante(A)


def _p_det_producto(A, B, C, k):
    """Miembros de det(AB) = det(A) · det(B)."""
    _requerir_cuadrada(A, "A")
    _requerir_cuadrada(B, "B")
    if len(A) != len(B):
        raise PropiedadNoAplicable("A y B deben tener el mismo orden")
    AB = producto(A, B)
    return determinante(AB), determinante(A) * determinante(B)


def _p_det_inversa(A, B, C, k):
    """Miembros de det(A⁻¹) = 1 / det(A)."""
    _requerir_cuadrada(A, "A")
    Ainv = _invertir(A, "A")
    return determinante(Ainv), Fraction(1) / determinante(A)


def _p_det_escalar(A, B, C, k):
    """Miembros de det(kA) = kⁿ · det(A) para A de orden n."""
    _requerir_cuadrada(A, "A")
    n = len(A)
    return determinante(escalar(k, A)), (k ** n) * determinante(A)


def _p_det_permutacion(A, B, C, k):
    """Miembros de Intercambiar dos filas cambia el signo del determinante."""
    _requerir_cuadrada(A, "A")
    if len(A) < 2:
        raise PropiedadNoAplicable("se necesitan al menos 2 filas")
    return determinante(_intercambiar_filas(A, 0, 1)), -determinante(A)


def _p_det_reemplazo(A, B, C, k):
    """Miembros de Reemplazar F2 por F2 + k·F1 conserva el determinante."""
    _requerir_cuadrada(A, "A")
    if len(A) < 2:
        raise PropiedadNoAplicable("se necesitan al menos 2 filas")
    return determinante(_reemplazar_fila(A, 1, 0, k)), determinante(A)


def _p_det_multiplicacion_fila(A, B, C, k):
    """Miembros de Multiplicar una fila por k multiplica el determinante por k."""
    _requerir_cuadrada(A, "A")
    return determinante(_escalar_fila(A, 0, k)), k * determinante(A)


def _p_det_triangular_superior(A, B, C, k):
    """Miembros de det de una triangular superior = producto de su diagonal."""
    _requerir_cuadrada(A, "A")
    T = _triangular_superior(A)
    return _det_por_cofactores(T), _producto_diagonal(T)


def _p_det_triangular_inferior(A, B, C, k):
    """Miembros de det de una triangular inferior = producto de su diagonal."""
    _requerir_cuadrada(A, "A")
    T = _triangular_inferior(A)
    return _det_por_cofactores(T), _producto_diagonal(T)


PROPIEDADES = [
    (CAT_TRANSPOSICION, "(Aᵀ)ᵀ = A", _p_transpuesta_doble),
    (CAT_TRANSPOSICION, "(A + B)ᵀ = Aᵀ + Bᵀ", _p_transpuesta_suma),
    (CAT_TRANSPOSICION, "(kA)ᵀ = kAᵀ", _p_transpuesta_escalar),
    (CAT_TRANSPOSICION, "(AB)ᵀ = BᵀAᵀ", _p_transpuesta_producto),
    (CAT_TRANSPOSICION, "A(B + C) = AB + AC", _p_distributiva),
    (CAT_TRANSPOSICION, "(AB)C = A(BC)", _p_asociativa),
    (CAT_INVERSA, "(A⁻¹)⁻¹ = A", _p_inversa_doble),
    (CAT_INVERSA, "(AB)⁻¹ = B⁻¹A⁻¹", _p_inversa_producto),
    (CAT_INVERSA, "(Aᵀ)⁻¹ = (A⁻¹)ᵀ", _p_inversa_transpuesta),
    (CAT_INVERSA, "A · A⁻¹ = I", _p_a_por_inversa),
    (CAT_DETERMINANTES, "det(Aᵀ) = det(A)", _p_det_transpuesta),
    (CAT_DETERMINANTES, "det(AB) = det(A) · det(B)", _p_det_producto),
    (CAT_DETERMINANTES, "det(A⁻¹) = 1 / det(A)", _p_det_inversa),
    (CAT_DETERMINANTES, "det(kA) = kⁿ · det(A)", _p_det_escalar),
    (CAT_DETERMINANTES, "Permutación de filas (F1 ↔ F2): det cambia de signo", _p_det_permutacion),
    (CAT_DETERMINANTES, "Reemplazo de fila (F2 ← F2 + k·F1): det se conserva", _p_det_reemplazo),
    (CAT_DETERMINANTES, "Multiplicar fila 1 por k: det se escala por k", _p_det_multiplicacion_fila),
    (CAT_DETERMINANTES, "det(triangular superior) = producto de la diagonal", _p_det_triangular_superior),
    (CAT_DETERMINANTES, "det(triangular inferior) = producto de la diagonal", _p_det_triangular_inferior),
]


def verificar_propiedades(A, B=None, C=None, k=2):
    """
    Evalúa todas las propiedades con las matrices dadas (listas anidadas; B y C opcionales).
    Devuelve una lista de diccionarios con: categoria, propiedad, izquierda, derecha,
    estado (Se cumple / No se cumple / No aplicable) y motivo (solo si no es aplicable).
    """
    k = Fraction(k)
    resultados = []
    for categoria, nombre, funcion in PROPIEDADES:
        registro = {"categoria": categoria, "propiedad": nombre,
                    "izquierda": None, "derecha": None, "estado": None, "motivo": ""}
        try:
            izquierda, derecha = funcion(A, B, C, k)
            registro["izquierda"] = izquierda
            registro["derecha"] = derecha
            registro["estado"] = SE_CUMPLE if _iguales(izquierda, derecha) else NO_SE_CUMPLE
        except PropiedadNoAplicable as e:
            registro["estado"] = NO_APLICABLE
            registro["motivo"] = str(e)
        except ValueError as e:
            # Los errores de dimensiones de las funciones internas indican que no se puede evaluar.
            registro["estado"] = NO_APLICABLE
            registro["motivo"] = str(e)
        resultados.append(registro)
    return resultados


def reporte_propiedades(resultados):
    """Convierte la lista de resultados en un texto legible con ambos miembros de cada igualdad."""
    lineas = [
        "======================================================",
        "   VERIFICADOR DE PROPIEDADES (ambos miembros)",
        "======================================================",
    ]
    categoria_actual = None
    for r in resultados:
        if r["categoria"] != categoria_actual:
            categoria_actual = r["categoria"]
            lineas.append(f"\n### {categoria_actual.upper()} ###")
        lineas.append(f"\n{r['propiedad']}")
        if r["estado"] == NO_APLICABLE:
            lineas.append(f"   -> No aplicable: {r['motivo']}")
        else:
            lineas.append(f"   Izquierda: {_en_linea(r['izquierda'])}")
            lineas.append(f"   Derecha:   {_en_linea(r['derecha'])}")
            lineas.append(f"   -> {r['estado']}")

    cumplen = sum(1 for r in resultados if r["estado"] == SE_CUMPLE)
    fallan = sum(1 for r in resultados if r["estado"] == NO_SE_CUMPLE)
    no_aplican = sum(1 for r in resultados if r["estado"] == NO_APLICABLE)
    lineas.append("\n------------------------------------------------------")
    lineas.append(f"RESUMEN: {cumplen} se cumplen, {fallan} no se cumplen, {no_aplican} no aplicables.")
    return "\n".join(lineas)