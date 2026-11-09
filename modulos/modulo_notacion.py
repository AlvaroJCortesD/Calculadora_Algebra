import tkinter as tk
from tkinter import ttk, messagebox


def dec_a_binario_con_decimales(numero, precision=10):
    entero = int(numero)
    decimal = abs(numero - entero)

    bin_entero = bin(entero).replace("0b", "")

    if decimal == 0:
        return bin_entero

    bin_decimal = "."
    while decimal > 0 and len(bin_decimal) <= precision + 1:
        decimal *= 2
        bit = int(decimal)
        bin_decimal += str(bit)
        decimal -= bit

    return bin_entero + bin_decimal


def binario_a_dec_con_decimales(bin_str):
    if "." in bin_str:
        entero_str, decimal_str = bin_str.split(".")
    else:
        entero_str, decimal_str = bin_str, ""

    # Convertir parte entera
    entero_dec = int(entero_str, 2) if entero_str else 0

    # Convertir parte decimal
    decimal_dec = 0.0
    for i, bit in enumerate(decimal_str):
        if bit == '1':
            decimal_dec += 2 ** -(i + 1)

    return entero_dec + decimal_dec


def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Notación Posicional (Base 10 ↔ Base 2)")
    win.geometry("450x450")
    win.grab_set()

    # --- SECCIÓN: DECIMAL A BINARIO ---
    frame_dec_bin = tk.LabelFrame(win, text="Decimal a Binario", padx=10, pady=10)
    frame_dec_bin.pack(pady=10, fill=tk.X, padx=20)

    tk.Label(frame_dec_bin, text="Número Decimal (Base 10):").pack()
    ent_num_dec = tk.Entry(frame_dec_bin, width=25, font=("Arial", 11))
    ent_num_dec.pack(pady=5)

    lbl_res_bin = tk.Label(frame_dec_bin, text="Binario: ", font=("Arial", 11, "bold"), fg="blue")
    lbl_res_bin.pack(pady=5)

    def convertir_a_binario():
        try:
            num = float(ent_num_dec.get())
            binario = dec_a_binario_con_decimales(num)
            lbl_res_bin.config(text=f"Binario: {binario}")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número decimal válido.")

    ttk.Button(frame_dec_bin, text="Convertir a Binario", command=convertir_a_binario).pack(pady=5)

    # --- SECCIÓN: BINARIO A DECIMAL ---
    frame_bin_dec = tk.LabelFrame(win, text="Binario a Decimal", padx=10, pady=10)
    frame_bin_dec.pack(pady=10, fill=tk.X, padx=20)

    tk.Label(frame_bin_dec, text="Número Binario (Base 2):").pack()
    ent_num_bin = tk.Entry(frame_bin_dec, width=25, font=("Arial", 11))
    ent_num_bin.pack(pady=5)

    lbl_res_dec = tk.Label(frame_bin_dec, text="Decimal: ", font=("Arial", 11, "bold"), fg="blue")
    lbl_res_dec.pack(pady=5)

    def convertir_a_decimal():
        try:
            bin_str = ent_num_bin.get().strip()

            # Validación básica para asegurar que solo contenga 0, 1 y un solo punto
            if not all(c in "01." for c in bin_str) or bin_str.count(".") > 1:
                raise ValueError

            decimal = binario_a_dec_con_decimales(bin_str)

            # Si el resultado no tiene decimales, mostrarlo como entero limpio
            if decimal.is_integer():
                lbl_res_dec.config(text=f"Decimal: {int(decimal)}")
            else:
                lbl_res_dec.config(text=f"Decimal: {decimal}")

        except ValueError:
            messagebox.showerror("Error", "Ingresa un número binario válido (solo 0, 1 y máximo un punto).")

    ttk.Button(frame_bin_dec, text="Convertir a Decimal", command=convertir_a_decimal).pack(pady=5)