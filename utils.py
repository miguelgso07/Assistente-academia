# utils.py
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from config import CSV_FILE_PATH, REQUIRED_COLUMNS


def calcular_imc(peso, altura_cm):
    """Calcula o Índice de Massa Corporal."""
    if altura_cm <= 0:
        return 0
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)

def get_imc_classification(imc):
    """Retorna a classificação do IMC."""
    if imc < 18.5: return "Abaixo do peso"
    elif 18.5 <= imc < 24.9: return "Peso normal"
    elif 25 <= imc < 29.9: return "Sobrepeso"
    elif 30 <= imc < 34.9: return "Obesidade Grau I"
    elif 35 <= imc < 39.9: return "Obesidade Grau II"
    else: return "Obesidade Grau III (Mórbida)"

def get_aerobic_time(imc_classification):
    """Retorna o tempo de aeróbico recomendado."""
    if "Obesidade" in imc_classification or "Sobrepeso" in imc_classification:
        return "30-45 min"
    elif "Peso normal" in imc_classification:
        return "20-30 min"
    else: # Abaixo do peso
        return "15-20 min"

# --- Gerenciamento de Dados ---

def load_exercise_data():
    """Carrega os exercícios do arquivo CSV e valida os dados."""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            raise FileNotFoundError
        
        df = pd.read_csv(CSV_FILE_PATH)
        
        if df.empty:
            raise pd.errors.EmptyDataError
            
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            messagebox.showerror("Erro de Dados", f"O arquivo 'exercicios.csv' está faltando as colunas: {', '.join(missing_cols)}.")
            return None
            
        return df

    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{CSV_FILE_PATH}' não encontrado.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Erro de Dados", f"O arquivo '{CSV_FILE_PATH}' está vazio.")
        return None
    except Exception as e:
        messagebox.showerror("Erro ao Carregar CSV", f"Erro ao ler '{CSV_FILE_PATH}': {e}")
        return None

# --- Gerenciador de Animação de GIF ---

class GifManager:
    """Uma classe para lidar com o carregamento e animação de GIFs em um widget Label."""
    def __init__(self, master, label_widget):
        self.master = master
        self.label = label_widget
        self.frames = []
        self.animation_id = None
        self.current_image = None

    def load_and_play(self, gif_path):
        self.stop()
        if not gif_path or not os.path.exists(gif_path):
            self.label.config(text="GIF não disponível.", image='')
            return

        try:
            gif_info = tk.PhotoImage(file=gif_path)
            num_frames = gif_info.cget("nframes")
            self.frames = [tk.PhotoImage(file=gif_path, format=f"gif -index {i}") for i in range(num_frames)]
            self.animate_loop(0)
        except Exception as e:
            self.label.config(text=f"Erro ao carregar GIF: {e}", image='')
            self.frames = []

    def animate_loop(self, frame_index):
        if not self.frames:
            return
            
        frame = self.frames[frame_index]
        self.label.config(image=frame)
        self.current_image = frame # Mantém referência para evitar garbage collection
        
        next_frame_index = (frame_index + 1) % len(self.frames)
        self.animation_id = self.master.after(100, self.animate_loop, next_frame_index)

    def stop(self):
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        self.frames = []
        self.current_image = None