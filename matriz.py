#! /usr/bin/env python3


# Función auxiliar para convertir números normales a subíndices Unicode (ej: 1 -> ₁ , 2 -> ₂)
def to_subscript(number):
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(subscripts)


# Función auxiliar para formatear floats como enteros o fracciones en texto
def formatear_numero(val, tol=1e-7):
    if abs(val - round(val)) < tol:
        return str(int(round(val)))

    # Convertir a fracción equivalente en texto
    for den in range(1, 100):
        num = val * den
        if abs(num - round(num)) < tol:
            n = int(round(num))
            d = den
            if d < 0:
                n, d = -n, -d
            return f"{n}/{d}" if d != 1 else f"{n}"

    return f"{val:.2f}"


# Función auxiliar para solicitar entrada al usuario
def asking_for_input(message, type=float):
    while True:
        info = input(message.strip())
        try:
            if type == int:
                return int(info)
            if "/" in info:
                num, den = info.split("/")
                return float(num) / float(den)
            return float(info)
        except ValueError:
            print(
                "Entrada invalida. Por favor, ingresa un numero entero, decimal o fraccion (ej: 3, 0.5 o 1/3)."
            )


# Función auxiliar para dar formato de texto a cada elemento
def fmt_val(val):
    texto = formatear_numero(val)
    return f"{texto:>7}"


# Función auxiliar para formatear una matriz en un único bloque de corchetes
def format_matrix(matriz_datos):
    lines = []
    for row in matriz_datos:
        datos_A = row[:-1]
        valor_b = row[-1]

        parte_A = "  ".join(fmt_val(num) for num in datos_A)
        fmt_b = fmt_val(valor_b)

        lines.append(f"{parte_A}  │  {fmt_b}")

    n = len(lines)
    resultado = []

    for i, line in enumerate(lines):
        if n == 1:
            resultado.append(f"[ {line} ]")
        elif i == 0:
            resultado.append(f"┌ {line} ┐")
        elif i == n - 1:
            resultado.append(f"└ {line} ┘")
        else:
            resultado.append(f"│ {line} │")

    return "\n".join(resultado)


# Clase Matrix
class Matrix:

    def __init__(self, rows, columns, valor_inicial=0.0):
        self.rows = rows
        self.columns = columns
        self.array = [
            [float(valor_inicial) for _ in range(columns)] for _ in range(rows)
        ]

    def add_vector_b(self, vector_b):
        if len(vector_b) != self.rows:
            raise ValueError(
                "El numero de elementos de vector b debe ser igual al numero de filas"
            )

        for i in range(self.rows):
            self.array[i].append(float(vector_b[i]))

        self.columns += 1

    def modify(self, rows, columns, new_value):
        self.array[rows][columns] = float(new_value)

    def gauss_jordan(self):
        m_filas = self.rows
        n_variables = self.columns - 1
        clone = [[float(val) for val in row] for row in self.array]

        def imprimir_paso(matriz_clon):
            print(format_matrix(matriz_clon))
            print("-" * 50)

        print("\n=== INICIANDO REDUCCIÓN GAUSS-JORDAN ===")
        print("Transformando la matriz a la FORMA ESCALONADA REDUCIDA...")

        columnas_pivote = []
        fila_pivote = 0

        for c in range(n_variables):
            if fila_pivote >= m_filas:
                break

            print(f"\nProcesando Columna {c + 1}:")

            max_row = fila_pivote
            for r in range(fila_pivote + 1, m_filas):
                if abs(clone[r][c]) > abs(clone[max_row][c]):
                    max_row = r

            if abs(clone[max_row][c]) < 1e-9:
                print(
                    f"-> La columna {c + 1} no tiene pivote (variable libre)."
                )
                continue

            if max_row != fila_pivote:
                clone[fila_pivote], clone[max_row] = (
                    clone[max_row],
                    clone[fila_pivote],
                )
                print(
                    f"-> Se intercambió la fila {fila_pivote + 1} con la fila {max_row + 1} (Pivoteo Parcial):"
                )
                imprimir_paso(clone)

            pivot = clone[fila_pivote][c]
            for j in range(self.columns):
                clone[fila_pivote][j] /= pivot

            print(
                f"-> Fila {fila_pivote + 1} dividida entre su pivote ({formatear_numero(pivot)}) para obtener el 1 principal:"
            )
            imprimir_paso(clone)

            for f in range(m_filas):
                if f != fila_pivote:
                    factor = clone[f][c]
                    for j in range(self.columns):
                        clone[f][j] -= factor * clone[fila_pivote][j]

            print(
                f"-> Ceros generados arriba y abajo del pivote de la columna {c + 1}:"
            )
            imprimir_paso(clone)

            columnas_pivote.append(c)
            fila_pivote += 1

        print("\n=== PROCESO DE REDUCCIÓN FINALIZADO ===")
        print(
            "ESTADO DE LA MATRIZ: La matriz se encuentra en FORMA ESCALONADA REDUCIDA POR FILAS."
        )

        variables_libres = [
            col for col in range(n_variables) if col not in columnas_pivote
        ]

        inconsistente = False
        for row in clone:
            if (
                all(abs(val) < 1e-9 for val in row[:-1])
                and abs(row[-1]) > 1e-9
            ):
                inconsistente = True
                break

        print("\n================ RESULTADO DEL ANÁLISIS ================")
        if inconsistente:
            print("TIPO DE SISTEMA: INCONSISTENTE")
            print("CANTIDAD DE SOLUCIONES: Sin solución (0 soluciones).")
            print(
                "RAZÓN: Se obtuvo una contradicción del tipo [ 0 0 ... 0 │ k ] con k ≠ 0."
            )
            print("========================================================\n")
            return clone, columnas_pivote, variables_libres, None, None

        elif len(variables_libres) > 0:
            print("TIPO DE SISTEMA: CONSISTENTE INDETERMINADO")
            print("CANTIDAD DE SOLUCIONES: Infinitas soluciones.")
            print(
                "RAZÓN: Existe al menos una variable libre en el sistema.\n"
            )

            # --- CONSTRUCCIÓN DE LA SOLUCIÓN PARAMÉTRICA Y VECTORIAL ESTILO PROFE ---
            v_particular = [0.0] * n_variables
            v_direccionales = {
                lib: [0.0] * n_variables for lib in variables_libres
            }

            for lib in variables_libres:
                v_direccionales[lib][lib] = 1.0

            for idx, p in enumerate(columnas_pivote):
                v_particular[p] = clone[idx][-1]
                for lib in variables_libres:
                    v_direccionales[lib][p] = -clone[idx][lib]

            # Asignación de parámetros (s, t, u...) a las variables libres
            letras_param = ["s", "t", "u", "v", "w"]
            mapa_param = {}
            for i, lib in enumerate(variables_libres):
                p_nombre = (
                    letras_param[i]
                    if i < len(letras_param)
                    else f"r{i+1}"
                )
                mapa_param[lib] = p_nombre

            desglose = []
            desglose.append("Despeje Parametrizado:")
            for p in range(n_variables):
                sub = to_subscript(p + 1)
                if p in variables_libres:
                    desglose.append(f"  x{sub} = {mapa_param[p]} (Variable Libre)")
                else:
                    idx = columnas_pivote.index(p)
                    cte = formatear_numero(v_particular[p])
                    partes = []
                    if cte != "0" or not variables_libres:
                        partes.append(cte)

                    for lib in variables_libres:
                        coef = v_direccionales[lib][p]
                        if abs(coef) > 1e-9:
                            coef_str = formatear_numero(abs(coef))
                            signo = "+" if coef > 0 else "-"
                            if coef_str == "1":
                                partes.append(f"{signo} {mapa_param[lib]}")
                            else:
                                partes.append(
                                    f"{signo} {coef_str}{mapa_param[lib]}"
                                )

                    expr = " ".join(partes) if partes else "0"
                    desglose.append(f"  x{sub} = {expr}")

            rango_a = len(columnas_pivote)
            desglose.append(
                f"\nRango(A) = {rango_a},  n = {n_variables},  Variables Libres = {n_variables} - {rango_a} = {len(variables_libres)}"
            )

            # Formatear Vectores en Columna
            vector_str = []
            vector_str.append("\nSolución General (Forma Vectorial):")

            # Columna [x1, x2, ...]
            col_x = [f"x{to_subscript(i+1)}" for i in range(n_variables)]
            
            # Bloques
            def build_col(vector):
                return [formatear_numero(v) for v in vector]

            cols_to_print = [("X", col_x), ("=", build_col(v_particular))]
            for lib in variables_libres:
                cols_to_print.append(
                    (f"+ {mapa_param[lib]}", build_col(v_direccionales[lib]))
                )

            max_len = max(
                len(val)
                for _, list_v in cols_to_print
                for val in list_v
            )

            lines_out = ["" for _ in range(n_variables)]
            for idx_c, (header, list_v) in enumerate(cols_to_print):
                for i in range(n_variables):
                    val = list_v[i].center(max_len)
                    if n_variables == 1:
                        bracket = f"[ {val} ]"
                    elif i == 0:
                        bracket = f"┌ {val} ┐"
                    elif i == n_variables - 1:
                        bracket = f"└ {val} ┘"
                    else:
                        bracket = f"│ {val} │"

                    if header in ["X", "="]:
                        prefix = f"{header} = " if header == "X" else "= "
                        lines_out[i] += (
                            f"{prefix if idx_c <= 1 and header == '=' else ''}{bracket} "
                        )
                    else:
                        lines_out[i] += f"{header} {bracket} "

            solucion_vectorial_final = "\n".join(desglose) + "\n\n" + "\n".join(lines_out)

            print("========================================================\n")
            return (
                clone,
                columnas_pivote,
                variables_libres,
                None,
                solucion_vectorial_final,
            )

        else:
            print("TIPO DE SISTEMA: CONSISTENTE DETERMINADO")
            print("CANTIDAD DE SOLUCIONES: Solución ÚNICA.")
            print("========================================================\n")

            answers = [row[-1] for row in clone]
            return clone, columnas_pivote, variables_libres, answers, None

    def __str__(self):
        return format_matrix(self.array)


# Comprobación automática
def verificar_solucion(matriz_original, vector_b, soluciones):
    for i in range(len(matriz_original)):
        suma = sum(
            matriz_original[i][j] * soluciones[j]
            for j in range(len(soluciones))
        )
        if abs(suma - vector_b[i]) > 1e-7:
            print(f" Alerta: La solución no satisface la ecuación {i + 1}")
            return False

    print(
        " Solución verificada con éxito sustituyendo en el sistema original."
    )
    return True