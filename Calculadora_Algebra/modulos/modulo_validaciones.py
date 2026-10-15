"""
Módulo de Validaciones.
Funciones puras (sin input ni print) que verifican y convierten los datos que
ingresa el usuario. Ante un dato inválido lanzan ValueError con un mensaje claro,
para que la interfaz notifique el problema y solicite la reentrada sin colapsar.
"""
from fractions import Fraction

MAX_DIMENSION = 8  # los cofactores crecen como n!: con más de 8 la GUI se congelaría
MAX_LONGITUD_NUMERO = 25
MAX_LONGITUD_NOMBRE = 12


class ErrorCelda(ValueError):
    """Error de validación asociado a una celda concreta (fila, columna) de la cuadrícula."""

    def __init__(self, mensaje, fila, columna):
        super().__init__(mensaje)
        self.fila = fila
        self.columna = columna


def parsear_numero(texto, etiqueta="El valor"):
    """
    Convierte un texto en Fraction. Acepta enteros, decimales y fracciones (3, -2.5, 7/4).
    Lanza ValueError si el texto está vacío o no es un número válido. Se rechaza la notación
    científica (1e9999) porque permitiría crear enteros gigantes y bloquear el programa.
    """
    if texto is None or str(texto).strip() == "":
        raise ValueError(f"{etiqueta} está vacío.")
    limpio = str(texto).strip()
    if len(limpio) > MAX_LONGITUD_NUMERO:
        raise ValueError(f"{etiqueta} es demasiado largo ('{limpio[:10]}...').")
    if "e" in limpio.lower() or "_" in limpio:
        raise ValueError(f"{etiqueta} ('{limpio}') no es válido: no se admite notación científica ni '_'.")
    try:
        return Fraction(limpio)
    except ZeroDivisionError:
        raise ValueError(f"{etiqueta} ('{limpio}') tiene denominador cero.")
    except ValueError:
        raise ValueError(
            f"{etiqueta} ('{limpio}') no es un número válido. Usa enteros, decimales (2.5) o fracciones (3/4)."
        )


def parsear_entero(texto, etiqueta, minimo=1, maximo=MAX_DIMENSION):
    """Convierte un texto en entero dentro de [minimo, maximo]; lanza ValueError si no cumple."""
    try:
        valor = int(str(texto).strip())
    except ValueError:
        raise ValueError(f"{etiqueta} debe ser un número entero (se recibió '{str(texto).strip()}').")
    if valor < minimo or valor > maximo:
        raise ValueError(f"{etiqueta} debe estar entre {minimo} y {maximo} (se recibió {valor}).")
    return valor


def validar_nombre(nombre, etiqueta="El nombre"):
    """Verifica que el nombre de variable sea corto, sin espacios y con letras, dígitos o '_'."""
    nombre = (nombre or "").strip()
    if nombre == "":
        raise ValueError(f"{etiqueta} no puede estar vacío (Ej. A, b, u).")
    if len(nombre) > MAX_LONGITUD_NOMBRE:
        raise ValueError(f"{etiqueta} no puede superar {MAX_LONGITUD_NOMBRE} caracteres.")
    if not nombre.isidentifier():
        raise ValueError(
            f"{etiqueta} ('{nombre}') solo puede tener letras, dígitos y '_', sin espacios, y no iniciar con dígito."
        )
    return nombre


def parsear_cuadricula(textos):
    """
    Convierte una cuadrícula de textos (lista anidada) en una lista anidada de Fraction.
    Lanza ErrorCelda indicando la fila y columna (base 0) de la primera celda inválida.
    """
    if not textos or not textos[0]:
        raise ValueError("Primero genera la cuadrícula con las dimensiones de la matriz.")
    resultado = []
    for i, fila in enumerate(textos):
        nueva = []
        for j, texto in enumerate(fila):
            try:
                nueva.append(parsear_numero(texto, f"El elemento ({i + 1},{j + 1})"))
            except ValueError as e:
                raise ErrorCelda(str(e), i, j)
        resultado.append(nueva)
    return resultado


def validar_vector_columna(filas, columnas, etiqueta="El vector"):
    """Verifica que un objeto de tamaño filas x columnas sea un vector columna (n x 1)."""
    if columnas != 1:
        raise ValueError(
            f"{etiqueta} debe ser un vector columna (n x 1); tiene {filas}x{columnas}."
        )


def validar_sistema(filas_A, filas_b, columnas_b):
    """Verifica que b sea columna y tenga tantas componentes como filas tiene A (m)."""
    validar_vector_columna(filas_b, columnas_b, "El vector b")
    if filas_A != filas_b:
        raise ValueError(
            f"El vector b debe tener {filas_A} componentes (una por fila de A); tiene {filas_b}."
        )


def validar_cuadrada(filas, columnas, etiqueta="La matriz"):
    """Verifica que una matriz sea cuadrada."""
    if filas != columnas:
        raise ValueError(f"{etiqueta} debe ser cuadrada; tiene {filas}x{columnas}.")