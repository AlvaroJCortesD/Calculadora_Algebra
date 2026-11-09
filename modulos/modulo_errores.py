import tkinter as tk
from tkinter import ttk, messagebox


def abrir_gui(parent):
    win = tk.Toplevel(parent)
    win.title("Cálculo de Errores Numéricos")
    win.geometry("400x350")
    win.grab_set()

    tk.Label(win, text="Valor Verdadero (V):").pack(pady=5)
    ent_v = tk.Entry(win, width=20)
    ent_v.pack(pady=5)

    tk.Label(win, text="Valor Aproximado (Va):").pack(pady=5)
    ent_va = tk.Entry(win, width=20)
    ent_va.pack(pady=5)

    frame_res = tk.LabelFrame(win, text="Resultados", padx=10, pady=10)
    frame_res.pack(pady=20, fill=tk.X, padx=20)

    lbl_ea = tk.Label(frame_res, text="Error Absoluto (Ea): -")
    lbl_ea.pack(anchor="w")

    lbl_er = tk.Label(frame_res, text="Error Relativo (Er): -")
    lbl_er.pack(anchor="w")

    lbl_ep = tk.Label(frame_res, text="Error Porcentual (Ep): -")
    lbl_ep.pack(anchor="w")

    def calcular_errores():
        try:
            v = float(ent_v.get())
            va = float(ent_va.get())

            ea = abs(v - va)
            er = ea / abs(v) if v != 0 else 0
            ep = er * 100

            lbl_ea.config(text=f"Error Absoluto (Ea): {ea:.6g}")
            lbl_er.config(text=f"Error Relativo (Er): {er:.6g}")
            lbl_ep.config(text=f"Error Porcentual (Ep): {ep:.4f} %")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos.")

    ttk.Button(win, text="Calcular", command=calcular_errores).pack(pady=5)