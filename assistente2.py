import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random

class GymAssistantApp:
    def __init__(self, master):
        self.master = master
        master.title("GYM Assistant - Ficha de Treino")
        master.geometry("800x700")
        master.resizable(False, False)

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam') # Um tema moderno para ttk
        self.style.configure('TFrame', background='#e0f7fa') # Light Cyan
        self.style.configure('TLabel', background='#e0f7fa', font=('Arial', 11))
        self.style.configure('TEntry', font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 11, 'bold'), background='#00796b', foreground='white', borderwidth=0, relief='raised') # Teal
        self.style.map('TButton', background=[('active', '#004d40')])
        self.style.configure('TCombobox', font=('Arial', 11))
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), background='#b2dfdb', foreground='#004d40')
        self.style.map('TNotebook.Tab', background=[('selected', '#00796b')], foreground=[('selected', 'white')])
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background='#004d40', foreground='white')
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)

        # Carregar dados dos exercícios
        try:
            self.df_exercicios = pd.read_csv("exercicios.csv")
            # VERIFICAÇÃO ADICIONADA: Garante que a coluna 'Tipo' existe
            if 'Tipo' not in self.df_exercicios.columns:
                messagebox.showerror("Erro de Dados", "O arquivo 'exercicios.csv' não contém a coluna 'Tipo'. Por favor, verifique o arquivo e certifique-se de que o cabeçalho 'Tipo' está presente.")
                master.destroy()
                return
        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo 'exercicios.csv' não foi encontrado. Certifique-se de que ele está na mesma pasta do programa.")
            master.destroy()
            return
        except pd.errors.EmptyDataError:
            messagebox.showerror("Erro de Dados", "O arquivo 'exercicios.csv' está vazio. Por favor, preencha-o com os dados dos exercícios.")
            master.destroy()
            return
        except Exception as e:
            messagebox.showerror("Erro ao Carregar CSV", f"Ocorreu um erro ao ler o arquivo 'exercicios.csv': {e}\nVerifique a formatação do arquivo.")
            master.destroy()
            return

        self.ficha_semanal = {}
        self.df_filtrado = pd.DataFrame()

        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Exibe a tela de boas-vindas."""
        self.clear_frame()

        self.welcome_frame = ttk.Frame(self.master, padding="50 50 50 50", style='TFrame')
        self.welcome_frame.pack(expand=True, fill=tk.BOTH)

        self.welcome_title = ttk.Label(self.welcome_frame, text="GYM Assistant", font=('Arial', 32, 'bold'), foreground='#004d40', background='#e0f7fa')
        self.welcome_title.pack(pady=50)

        self.start_button = ttk.Button(self.welcome_frame, text="Iniciar", command=self.show_main_app)
        self.start_button.pack(pady=20, ipadx=20, ipady=10)

    def show_main_app(self):
        """Exibe a tela principal da aplicação."""
        self.clear_frame()

        self.main_frame = ttk.Frame(self.master, padding="20 20 20 20", style='TFrame')
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Entradas do usuário
        input_frame = ttk.Frame(self.main_frame, style='TFrame')
        input_frame.pack(pady=10, fill=tk.X)

        self.create_input_field(input_frame, "Idade:", "entrada_idade")
        self.create_input_field(input_frame, "Altura (cm):", "entrada_altura")
        self.create_input_field(input_frame, "Peso (kg):", "entrada_peso")
        self.create_combobox_field(input_frame, "Nível de treino:", "nivel_var", ["Básico", "Intermediário", "Avançado"])

        self.gerar_button = ttk.Button(self.main_frame, text="Gerar Fichas de Treino", command=self.gerar_fichas)
        self.gerar_button.pack(pady=15, fill=tk.X)

        self.imc_label = ttk.Label(self.main_frame, text="", font=('Arial', 12, 'bold'), background='#e0f7fa', foreground='#004d40')
        self.imc_label.pack(pady=5)

        # Notebook para as fichas diárias
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)

        self.daily_frames = {}
        self.daily_trees = {}
        for i in range(5):
            day_name = f"Dia {i+1}"
            frame = ttk.Frame(self.notebook, style='TFrame')
            self.notebook.add(frame, text=day_name)
            self.daily_frames[day_name] = frame

            tree = ttk.Treeview(frame, columns=["Exercício", "Grupo Muscular", "Séries", "Repetições", "Tipo"], show="headings", style='Treeview')
            tree.heading("Exercício", text="Exercício")
            tree.heading("Grupo Muscular", text="Grupo Muscular")
            tree.heading("Séries", text="Séries")
            tree.heading("Repetições", text="Repetições")
            tree.heading("Tipo", text="Tipo")

            tree.column("Exercício", width=150, anchor=tk.W)
            tree.column("Grupo Muscular", width=100, anchor=tk.W)
            tree.column("Séries", width=70, anchor=tk.CENTER)
            tree.column("Repetições", width=90, anchor=tk.CENTER)
            tree.column("Tipo", width=80, anchor=tk.W)

            tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.daily_trees[day_name] = tree

    def clear_frame(self):
        """Limpa todos os widgets do frame mestre."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_input_field(self, parent_frame, label_text, entry_name):
        """Cria um rótulo e um campo de entrada."""
        frame = ttk.Frame(parent_frame, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, background='#e0f7fa').pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
        setattr(self, entry_name, entry)

    def create_combobox_field(self, parent_frame, label_text, var_name, values):
        """Cria um rótulo e uma combobox."""
        frame = ttk.Frame(parent_frame, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, background='#e0f7fa').pack(side=tk.LEFT, padx=5)
        var = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
        combobox.set(values[0]) # Define um valor padrão
        setattr(self, var_name, var)
        setattr(self, f"{var_name}_combo", combobox)

    def calcular_imc(self, peso, altura_cm):
        """Calcula o Índice de Massa Corporal."""
        altura_m = altura_cm / 100
        return peso / (altura_m ** 2)

    def get_imc_classification(self, imc):
        """Retorna a classificação do IMC."""
        if imc < 18.5: return "Abaixo do peso"
        elif 18.5 <= imc < 24.9: return "Peso normal"
        elif 25 <= imc < 29.9: return "Sobrepeso"
        elif 30 <= imc < 34.9: return "Obesidade Grau I"
        elif 35 <= imc < 39.9: return "Obesidade Grau II"
        else: return "Obesidade Grau III (Mórbida)"

    def get_aerobic_time(self, imc_classification):
        """Retorna o tempo de aeróbico recomendado baseado na classificação do IMC."""
        if "Obesidade" in imc_classification or "Sobrepeso" in imc_classification:
            return "30-45 min"
        elif "Peso normal" in imc_classification:
            return "20-30 min"
        else: # Abaixo do peso
            return "15-20 min (com foco em ganho de massa)"

    def gerar_fichas(self):
        """Gera as 5 fichas de treino semanais."""
        try:
            idade = int(self.entrada_idade.get())
            altura = float(self.entrada_altura.get())
            peso = float(self.entrada_peso.get())
            nivel = self.nivel_var.get()

            imc = self.calcular_imc(peso, altura)
            imc_classificacao = self.get_imc_classification(imc)
            aerobic_time = self.get_aerobic_time(imc_classificacao)

            self.imc_label.config(text=f"IMC: {imc:.2f} ({imc_classificacao})")

            self.ficha_semanal = self.generate_weekly_plan(nivel, imc_classificacao, aerobic_time)
            self.display_weekly_plan()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos para Idade, Altura e Peso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def generate_weekly_plan(self, nivel, imc_classificacao, aerobic_time):
        """Gera o plano de treino semanal com base no nível e IMC."""
        plan = {}
        # Filtra exercícios com base no nível. Inclui níveis mais básicos para maior variedade.
        exercicios_filtrados = self.df_exercicios[self.df_exercicios["Nivel"].isin([nivel, "Básico", "Intermediário"])].copy()
        
        # Ajusta a demanda energética para obesos/sobrepeso
        if "Obesidade" in imc_classificacao or "Sobrepeso" in imc_classificacao:
            exercicios_filtrados_demanda = exercicios_filtrados[exercicios_filtrados["DemandaEnergetica"] == "Alta"]
            if not exercicios_filtrados_demanda.empty:
                exercicios_filtrados = exercicios_filtrados_demanda
            else:
                # Fallback se não houver exercícios de alta demanda para o nível
                messagebox.showwarning("Aviso", "Não há exercícios de alta demanda para o nível selecionado. Usando exercícios gerais.")


        if nivel == "Básico":
            plan = self._generate_abc_plan(exercicios_filtrados, aerobic_time)
        elif nivel == "Intermediário":
            plan = self._generate_ppl_upper_lower_plan(exercicios_filtrados, aerobic_time)
        elif nivel == "Avançado":
            plan = self._generate_upper_lower_plan(exercicios_filtrados, aerobic_time)
        
        return plan

    def _get_random_exercises(self, df, group, num_exercises, exercise_type=None, exclude_names=None):
        """
        Seleciona exercícios aleatórios de um grupo, com opção de tipo e exclusão.
        'exclude_names' é usado para evitar repetição DENTRO da mesma ficha diária.
        """
        if exclude_names is None:
            exclude_names = []

        # Filtra por grupo e exclui exercícios já selecionados para o dia
        filtered_df = df[(df["Grupo"] == group) & (~df["Nome"].isin(exclude_names))]
        
        if exercise_type:
            # Garante que a coluna 'Tipo' exista antes de tentar filtrar por ela
            if 'Tipo' not in filtered_df.columns:
                print(f"Aviso: Coluna 'Tipo' não encontrada para o grupo '{group}' ao tentar filtrar por tipo '{exercise_type}'.")
                # Retorna sem filtrar por tipo se a coluna não existir
            else:
                filtered_df = filtered_df[filtered_df["Tipo"] == exercise_type]

        if filtered_df.empty:
            return [] # Retorna lista vazia se não houver opções

        # Seleciona aleatoriamente, sem substituição, o mínimo entre o número desejado
        # e o número de exercícios disponíveis.
        selected = filtered_df.sample(min(len(filtered_df), num_exercises), replace=False)
        return selected.to_dict('records')

    def _generate_abc_plan(self, df, aerobic_time):
        """Gera um plano de treino ABC (A: Peito/Tríceps/Abdômen, B: Costas/Bíceps, C: Pernas/Ombros)."""
        plan = {}

        # Dia 1: Peito, Tríceps, Abdômen
        day1_picked_names = set() # Exercícios já selecionados para o Dia 1
        day1_exercises = []
        
        exercises_peito_comp = self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names)
        day1_exercises.extend(exercises_peito_comp)
        day1_picked_names.update([ex["Nome"] for ex in exercises_peito_comp])

        exercises_peito_iso = self._get_random_exercises(df, "Peito", 1, "Isolado", day1_picked_names)
        day1_exercises.extend(exercises_peito_iso)
        day1_picked_names.update([ex["Nome"] for ex in exercises_peito_iso])

        exercises_triceps = self._get_random_exercises(df, "Tríceps", 2, None, day1_picked_names)
        day1_exercises.extend(exercises_triceps)
        day1_picked_names.update([ex["Nome"] for ex in exercises_triceps])

        exercises_abdomen = self._get_random_exercises(df, "Abdômen", 1, None, day1_picked_names)
        day1_exercises.extend(exercises_abdomen)
        day1_picked_names.update([ex["Nome"] for ex in exercises_abdomen])

        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Costas, Bíceps
        day2_picked_names = set()
        day2_exercises = []
        exercises_costas_comp = self._get_random_exercises(df, "Costas", 3, "Composto", day2_picked_names)
        day2_exercises.extend(exercises_costas_comp)
        day2_picked_names.update([ex["Nome"] for ex in exercises_costas_comp])

        exercises_biceps = self._get_random_exercises(df, "Bíceps", 2, None, day2_picked_names)
        day2_exercises.extend(exercises_biceps)
        day2_picked_names.update([ex["Nome"] for ex in exercises_biceps])
        
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Pernas, Ombros
        day3_picked_names = set()
        day3_exercises = []
        exercises_pernas_comp = self._get_random_exercises(df, "Pernas", 3, "Composto", day3_picked_names)
        day3_exercises.extend(exercises_pernas_comp)
        day3_picked_names.update([ex["Nome"] for ex in exercises_pernas_comp])

        exercises_pernas_iso = self._get_random_exercises(df, "Pernas", 1, "Isolado", day3_picked_names)
        day3_exercises.extend(exercises_pernas_iso)
        day3_picked_names.update([ex["Nome"] for ex in exercises_pernas_iso])

        exercises_ombros_comp = self._get_random_exercises(df, "Ombros", 2, "Composto", day3_picked_names)
        day3_exercises.extend(exercises_ombros_comp)
        day3_picked_names.update([ex["Nome"] for ex in exercises_ombros_comp])

        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        plan["Dia 4"] = [{"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}]
        plan["Dia 5"] = [{"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}]

        return plan

    def _generate_ppl_upper_lower_plan(self, df, aerobic_time):
        """Gera um plano de treino PPL (Push/Pull/Legs) + Upper/Lower."""
        plan = {}

        # Dia 1: Push (Peito, Ombros, Tríceps)
        day1_picked_names = set()
        day1_exercises = []
        day1_exercises.extend(self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Tríceps", 2, None, day1_picked_names))
        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Pull (Costas, Bíceps)
        day2_picked_names = set()
        day2_exercises = []
        day2_exercises.extend(self._get_random_exercises(df, "Costas", 3, "Composto", day2_picked_names))
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Bíceps", 2, None, day2_picked_names))
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Legs (Pernas, Abdômen)
        day3_picked_names = set()
        day3_exercises = []
        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 3, "Composto", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 1, "Isolado", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day3_picked_names))
        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 4: Upper Body (Peito, Costas, Ombros, Bíceps, Tríceps)
        day4_picked_names = set()
        day4_exercises = []
        day4_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Composto", day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Composto", day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day4_picked_names))
        plan["Dia 4"] = day4_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 5: Lower Body (Pernas, Abdômen)
        day5_picked_names = set()
        day5_exercises = []
        day5_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Composto", day5_picked_names))
        day5_picked_names.update([ex["Nome"] for ex in day5_exercises])
        day5_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day5_picked_names))
        plan["Dia 5"] = day5_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        return plan

    def _generate_upper_lower_plan(self, df, aerobic_time):
        """Gera um plano de treino Upper/Lower para avançados."""
        plan = {}

        # Dia 1: Upper Body
        day1_picked_names = set()
        day1_exercises = []
        day1_exercises.extend(self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Costas", 2, "Composto", day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day1_picked_names))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day1_picked_names))
        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Lower Body
        day2_picked_names = set()
        day2_exercises = []
        day2_exercises.extend(self._get_random_exercises(df, "Pernas", 3, "Composto", day2_picked_names))
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Isolado", day2_picked_names))
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day2_picked_names))
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Upper Body (Variação)
        day3_picked_names = set()
        day3_exercises = []
        day3_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Composto", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Isolado", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Composto", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Isolado", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Isolado", day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day3_picked_names))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day3_picked_names))
        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 4: Lower Body (Variação)
        day4_picked_names = set()
        day4_exercises = []
        day4_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Composto", day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Pernas", 1, "Isolado", day4_picked_names))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Abdômen", 1, None, day4_picked_names))
        plan["Dia 4"] = day4_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 5: Full Body / Descanso Ativo
        plan["Dia 5"] = [{"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}]

        return plan


    def display_weekly_plan(self):
        """Exibe as fichas de treino nos tabs do notebook."""
        for day_name, tree in self.daily_trees.items():
            for item in tree.get_children():
                tree.delete(item) # Limpa a tabela

            exercises = self.ficha_semanal.get(day_name, [])
            for ex in exercises:
                # Garante que todos os campos existam para evitar KeyError
                nome = ex.get("Nome", "N/A")
                grupo = ex.get("Grupo", "N/A")
                series = ex.get("Séries", "3")
                repeticoes = ex.get("Repetições", "8-12")
                tipo = ex.get("Tipo", "N/A")

                # Ajusta séries/repetições para aeróbicos/descanso
                if tipo == "Aeróbico" or tipo == "Recuperação":
                    series = "-"
                    repeticoes = "-"

                tree.insert("", "end", values=(nome, grupo, series, repeticoes, tipo))


# Cria a janela principal e executa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = GymAssistantApp(root)
    root.mainloop()