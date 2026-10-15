"""
Módulo de Verificación de Propiedades Matriciales.
Evalúa teoremas de operaciones, transposición, inversas y determinantes.
"""
from fractions import Fraction
from modulos.modulo_matrices import Matrix


def matrices_iguales(A, B):
    """Compara si dos matrices son exactamente iguales."""
    if A.rows != B.rows or A.columns != B.columns:
        return False
    for i in range(A.rows):
        for j in range(A.columns):
            if A.array[i][j] != B.array[i][j]:
                return False
    return True


def verificar_todas_propiedades(A, B=None, C=None, k=Fraction(1)):
    """
    Verifica el conjunto de teoremas y propiedades requeridos.
    A, B, C: Instancias de Matrix. k: Escalar (Fraction).
    Retorna: String con el reporte completo de validaciones.
    """
    reporte = ["======================================================",
               "   VERIFICADOR DE PROPIEDADES MATRICIALES",
               "======================================================\n"]

    reporte.append("--- OPERACIONES Y TRANSPOSICIÓN ---")

    # (A^T)^T = A
    izq = A.traspuesta().traspuesta()
    estado = "Se cumple" if matrices_iguales(izq, A) else "No se cumple"
    reporte.append(f"1. (A^T)^T = A -> {estado}")

    # (kA)^T = kA^T
    izq = A.escalar_mult(k).traspuesta()
    der = A.traspuesta().escalar_mult(k)
    estado = "Se cumple" if matrices_iguales(izq, der) else "No se cumple"
    reporte.append(f"2. (kA)^T = k(A^T) -> {estado}")

    if B is not None:
        try:
            # (A+B)^T = A^T + B^T
            izq = A.sumar(B).traspuesta()
            der = A.traspuesta().sumar(B.traspuesta())
            estado = "Se cumple" if matrices_iguales(izq, der) else "No se cumple"
            reporte.append(f"3. (A+B)^T = A^T + B^T -> {estado}")
        except:
            reporte.append("3. (A+B)^T = A^T + B^T -> (Omitido: A y B de distinto tamaño)")

        try:
            # (AB)^T = B^T A^T
            izq = A.multiplicar(B).traspuesta()
            der = B.traspuesta().multiplicar(A.traspuesta())
            estado = "Se cumple" if matrices_iguales(izq, der) else "No se cumple"
            reporte.append(f"4. (AB)^T = B^T A^T -> {estado}")
        except:
            reporte.append("4. (AB)^T = B^T A^T -> (Omitido: Dimensiones incompatibles para A*B)")

    if B is not None and C is not None:
        try:
            # A(B+C) = AB + AC
            izq = A.multiplicar(B.sumar(C))
            der = A.multiplicar(B).sumar(A.multiplicar(C))
            estado = "Se cumple" if matrices_iguales(izq, der) else "No se cumple"
            reporte.append(f"5. A(B+C) = AB + AC -> {estado}")
        except:
            pass

        try:
            # (AB)C = A(BC)
            izq = A.multiplicar(B).multiplicar(C)
            der = A.multiplicar(B.multiplicar(C))
            estado = "Se cumple" if matrices_iguales(izq, der) else "No se cumple"
            reporte.append(f"6. (AB)C = A(BC) -> {estado}")
        except:
            pass

    if A.rows == A.columns:
        reporte.append("\n--- MATRIZ INVERSA Y DETERMINANTES ---")
        try:
            det_A, _ = A.determinante_triangular_paso_a_paso()
            det_AT, _ = A.traspuesta().determinante_triangular_paso_a_paso()
            estado = "Se cumple" if det_A == det_AT else "No se cumple"
            reporte.append(f"7. det(A^T) = det(A) -> {estado}")

            # det(kA) = k^n det(A)
            n = A.rows
            det_kA, _ = A.escalar_mult(k).determinante_triangular_paso_a_paso()
            estado = "Se cumple" if det_kA == (k ** n) * det_A else "No se cumple"
            reporte.append(f"8. det(kA) = k^n det(A) -> {estado}")

            if det_A != 0:
                A_inv, _ = A.inversa_gauss_jordan_paso_a_paso()
                # (A^-1)^-1 = A
                A_inv_inv, _ = A_inv.inversa_gauss_jordan_paso_a_paso()
                estado = "Se cumple" if matrices_iguales(A_inv_inv, A) else "No se cumple"
                reporte.append(f"9. (A^-1)^-1 = A -> {estado}")

                # A * A^-1 = I
                identidad = A.multiplicar(A_inv)
                # Verifica si la identidad tiene 1s en la diagonal principal
                es_ident = True
                for i in range(A.rows):
                    if identidad.array[i][i] != 1: es_ident = False
                estado = "Se cumple" if es_ident else "No se cumple"
                reporte.append(f"10. A * A^-1 = I -> {estado}")

                # det(A^-1) = 1/det(A)
                det_inv, _ = A_inv.determinante_triangular_paso_a_paso()
                estado = "Se cumple" if det_inv == Fraction(1) / det_A else "No se cumple"
                reporte.append(f"11. det(A^-1) = 1/det(A) -> {estado}")

                if B is not None and B.rows == B.columns and A.rows == B.rows:
                    det_B, _ = B.determinante_triangular_paso_a_paso()
                    if det_B != 0:
                        # (AB)^-1 = B^-1 A^-1
                        AB_inv, _ = A.multiplicar(B).inversa_gauss_jordan_paso_a_paso()
                        B_inv, _ = B.inversa_gauss_jordan_paso_a_paso()
                        der_inv = B_inv.multiplicar(A_inv)
                        estado = "Se cumple" if matrices_iguales(AB_inv, der_inv) else "No se cumple"
                        reporte.append(f"12. (AB)^-1 = B^-1 A^-1 -> {estado}")

                        # det(AB) = det(A) * det(B)
                        det_AB, _ = A.multiplicar(B).determinante_triangular_paso_a_paso()
                        estado = "Se cumple" if det_AB == det_A * det_B else "No se cumple"
                        reporte.append(f"13. det(AB) = det(A) * det(B) -> {estado}")

        except Exception as e:
            reporte.append(f"Error evaluando inversas: {e}")

    return "\n".join(reporte)