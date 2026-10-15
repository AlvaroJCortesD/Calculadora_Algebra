"""
Módulo de Vectores.
Contiene operaciones vectoriales puras: producto punto, norma y producto cruz.
"""
from fractions import Fraction

def vector_a_lista(matriz_vector):
    """Convierte un objeto Matrix de n x 1 a una lista simple de valores."""
    if matriz_vector.columns != 1:
        raise ValueError("Se esperaba un vector columna (n x 1), no una matriz de varias columnas.")
    return [matriz_vector.array[i][0] for i in range(matriz_vector.rows)]

def producto_punto(u_list, v_list):
    """Calcula el producto punto u · v."""
    if len(u_list) != len(v_list):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return sum(Fraction(u_list[i]) * Fraction(v_list[i]) for i in range(len(u_list)))

def norma_vector(u_list):
    """Calcula la norma ||u|| de un vector."""
    p_punto = producto_punto(u_list, u_list)
    # ||u|| = (u·u)^(1/2); el exponente 0.5 evita importar math
    return float(p_punto) ** 0.5

def producto_cruz_3d(u_list, v_list):
    """Calcula el producto cruz u x v para vectores en R^3."""
    if len(u_list) != 3 or len(v_list) != 3:
        raise ValueError("El producto cruz solo está definido para vectores en R^3.")
    u1, u2, u3 = [Fraction(x) for x in u_list]
    v1, v2, v3 = [Fraction(x) for x in v_list]
    return [
        u2 * v3 - u3 * v2,
        u3 * v1 - u1 * v3,
        u1 * v2 - u2 * v1
    ]