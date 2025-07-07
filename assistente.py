import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random

# Calcular IMC
def calcular_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)

# Filtrar exercícios com base no nível e IMC
def filtrar_exercicios(df, nivel, imc):
    if imc >= 30:
        return df[(df["Nivel"] == nivel) & (df["DemandaEnergetica"] == "Alta")]
    else:
        return df[df["Nivel"] == nivel]

# Gerar ficha com 1 exercício por grupo
def gerar_ficha(df):
    ficha = []
    for grupo in df["Grupo"].unique():
        opcoes = df[df["Grupo"] == grupo]
        if not opcoes.empty:
            exercicio = opcoes.sample(1).iloc[0]
            ficha.append([exercicio["Nome"], grupo, "3", "6-8"])
    return ficha

# Substituir exercício da ficha
def substituir_exercicio(grupo):
    global ficha, df_filtrado
    opcoes = df_filtrado[df_filtrado["Grupo"] == grupo]
    if not opcoes.empty:
        novo = opcoes.sample(1).iloc[0]["Nome"]
        for item in ficha:
            if item[1] == grupo:
                item[0] = novo
                break
    exibir_ficha()

# Exibir ficha na tabela
def exibir_ficha():
    for row in tree.get_children():
        tree.delete(row)
    for ex in ficha:
        tree.insert("", "end", values=ex)

# Gerar ficha após entrada do usuário
def gerar():
    global ficha, df_filtrado

    try:
        idade = int(entrada_idade.get())
        altura = float(entrada_altura.get())
        peso = float(entrada_peso.get())
        nivel = nivel_var.get()

        imc = calcular_imc(peso, altura)
        imc_label.config(text=f"IMC: {imc:.2f}")

        df_filtrado = filtrar_exercicios(df_exercicios, nivel, imc)
        ficha = gerar_ficha(df_filtrado)
        exibir_ficha()

        botoes_frame.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Verifique os dados inseridos.\n{e}")

# Interface gráfica
janela = tk.Tk()
janela.title("GYM Assistant - Ficha de Treino")
janela.geometry("720x480")

df_exercicios = pd.read_csv("exercicios.csv")
ficha = []
df_filtrado = pd.DataFrame()

# Entradas
tk.Label(janela, text="Idade:").pack()
entrada_idade = tk.Entry(janela)
entrada_idade.pack()

tk.Label(janela, text="Altura (cm):").pack()
entrada_altura = tk.Entry(janela)
entrada_altura.pack()

tk.Label(janela, text="Peso (kg):").pack()
entrada_peso = tk.Entry(janela)
entrada_peso.pack()

tk.Label(janela, text="Nível de treino:").pack()
nivel_var = tk.StringVar()
nivel_combo = ttk.Combobox(janela, textvariable=nivel_var, values=["Básico", "Intermediário", "Avançado"], state="readonly")
nivel_combo.pack()

tk.Button(janela, text="Gerar Ficha", command=gerar).pack(pady=10)
imc_label = tk.Label(janela, text="")
imc_label.pack()

# Tabela de exercícios
colunas = ["Exercício", "Grupo", "Séries", "Repetições"]
tree = ttk.Treeview(janela, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=10)

# Botões para troca de exercício
botoes_frame = tk.Frame(janela)
def criar_botoes_substituir():
    for widget in botoes_frame.winfo_children():
        widget.destroy()
    for grupo in df_exercicios["Grupo"].unique():
        btn = tk.Button(botoes_frame, text=f"Trocar {grupo}", command=lambda g=grupo: substituir_exercicio(g))
        btn.pack(side="left", padx=5)
criar_botoes_substituir()

janela.mainloop()