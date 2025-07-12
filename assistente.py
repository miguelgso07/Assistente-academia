import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random
import os # Para verificar a existência de arquivos

class GymAssistantApp:
    def __init__(self, master):
        self.master = master
        master.title("GYM Assistant - Ficha de Treino")
        master.geometry("1200x800") # Mantém a escala da tela, mas não fullscreen
        # master.attributes('-fullscreen', True) # Removido para não iniciar em tela cheia
        master.bind("<Escape>", self.exit_fullscreen) # Permite sair do fullscreen com ESC (ainda útil se o usuário maximizar a janela manualmente)

        # Estilos - Paleta de cores azul
        self.style = ttk.Style()
        self.style.theme_use('clam') # Um tema moderno para ttk

        # Cores principais (paleta de azul)
        self.primary_blue = '#2196F3' # Blue 500
        self.dark_blue = '#1976D2'    # Blue 700
        self.light_blue = '#E3F2FD'   # Blue 50
        self.medium_blue = '#BBDEFB'  # Blue 100
        self.darker_blue = '#1565C0'  # Blue 800
        self.deep_blue = '#0D47A1'    # Blue 900 para textos mais escuros

        self.style.configure('TFrame', background=self.light_blue)
        self.style.configure('TLabel', background=self.light_blue, font=('Arial', 11), foreground=self.dark_blue)
        self.style.configure('TEntry', font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 11, 'bold'), background=self.primary_blue, foreground='white', borderwidth=0, relief='raised')
        self.style.map('TButton', background=[('active', self.darker_blue)])
        self.style.configure('TCombobox', font=('Arial', 11))
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), background=self.medium_blue, foreground=self.dark_blue)
        self.style.map('TNotebook.Tab', background=[('selected', self.primary_blue)], foreground=[('selected', 'white')])
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background=self.darker_blue, foreground='white')
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)

        # Carregar dados dos exercícios
        try:
            self.df_exercicios = pd.read_csv("data\exercicios.csv")
            required_columns = ["Nome", "Grupo", "Nivel", "DemandaEnergetica", "Tipo", "DescricaoDetalhada", "GifURL"]
            if not all(col in self.df_exercicios.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in self.df_exercicios.columns]
                messagebox.showerror("Erro de Dados", f"O arquivo 'exercicios.csv' está faltando as seguintes colunas: {', '.join(missing_cols)}. Por favor, verifique o arquivo e o cabeçalho.")
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

        # Variável para armazenar a imagem GIF do exercício
        self.current_gif_image = None
        self.gif_frames = [] # Para animação de GIFs
        self.gif_animation_id = None # Para controlar a animação do GIF

        # Atributos para IMC e classificação (agora são atributos da classe)
        self.imc = None
        self.imc_classificacao = None

        self.show_welcome_screen()

    def exit_fullscreen(self, event=None):
        """Sai do modo tela cheia ao pressionar ESC."""
        self.master.attributes('-fullscreen', False)

    def show_welcome_screen(self):
        """Exibe a tela de boas-vindas com gradiente e elementos visuais."""
        self.clear_frame()

        self.welcome_frame = ttk.Frame(self.master, style='TFrame')
        self.welcome_frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.welcome_frame, highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Vincula o método de atualização de layout ao evento <Configure> do canvas
        # Isso garante que o posicionamento seja feito após o canvas ter suas dimensões finais
        self.canvas.bind("<Configure>", self._update_welcome_screen_layout)

        # Cria os widgets, mas não os posiciona ainda. Eles serão posicionados no _update_welcome_screen_layout
        self.welcome_title_label = ttk.Label(self.canvas, text="GYM Assistant", font=('Helvetica', 64, 'bold'), foreground=self.deep_blue, background='')
        self.start_button = ttk.Button(self.canvas, text="Iniciar", command=self.show_main_app)

    def _update_welcome_screen_layout(self, event=None):
        """
        Atualiza o layout da tela de boas-vindas, centralizando os elementos
        com base nas dimensões atuais do canvas.
        """
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Limpa elementos antigos para redesenhar
        self.canvas.delete("all")

        # Desenha o gradiente de fundo
        self.draw_gradient(self.canvas)

        # Adiciona elementos visuais de academia (emojis como placeholder)
        self.canvas.create_text(canvas_width/2 - 300, canvas_height/2 - 200, text="🏋️‍♂️", font=("Arial", 120), fill=self.dark_blue, anchor=tk.CENTER)
        self.canvas.create_text(canvas_width/2 + 300, canvas_height/2 + 100, text="💪", font=("Arial", 80), fill=self.dark_blue, anchor=tk.CENTER)
        self.canvas.create_text(canvas_width/2, canvas_height/2 + 250, text="🏃‍♀️", font=("Arial", 90), fill=self.dark_blue, anchor=tk.CENTER)
        self.canvas.create_text(canvas_width/2 + 400, canvas_height/2 - 150, text="🤸", font=("Arial", 70), fill=self.dark_blue, anchor=tk.CENTER)

        # Centraliza o título e o botão
        self.canvas.create_window(canvas_width/2, canvas_height/2 - 100, window=self.welcome_title_label, anchor=tk.CENTER)
        self.canvas.create_window(canvas_width/2, canvas_height/2 + 50, window=self.start_button, anchor=tk.CENTER)


    def draw_gradient(self, canvas):
        """Desenha um gradiente vertical no canvas."""
        width = canvas.winfo_width() # Usa a largura do canvas
        height = canvas.winfo_height() # Usa a altura do canvas
        
        # Define as cores do gradiente (de um azul claro para um azul mais escuro)
        color1_rgb = tuple(int(self.light_blue[i:i+2], 16) for i in (1, 3, 5))
        color2_rgb = tuple(int(self.medium_blue[i:i+2], 16) for i in (1, 3, 5))

        for i in range(height):
            # Interpolação linear entre as cores
            r = int(color1_rgb[0] + (color2_rgb[0] - color1_rgb[0]) * (i / height))
            g = int(color1_rgb[1] + (color2_rgb[1] - color1_rgb[1]) * (i / height))
            b = int(color1_rgb[2] + (color2_rgb[2] - color1_rgb[2]) * (i / height))
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1, tags="gradient") # Adiciona tag para facilitar a exclusão
        
        # O bind para redesenhar já está no _update_welcome_screen_layout, então não precisamos duplicar aqui.

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

        self.imc_label = ttk.Label(self.main_frame, text="", font=('Arial', 12, 'bold'), background=self.light_blue, foreground=self.dark_blue)
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

            tree.column("Exercício", width=200, anchor=tk.W) # Aumenta largura para nome do exercício
            tree.column("Grupo Muscular", width=120, anchor=tk.W)
            tree.column("Séries", width=80, anchor=tk.CENTER)
            tree.column("Repetições", width=100, anchor=tk.CENTER)
            tree.column("Tipo", width=100, anchor=tk.W)

            tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.daily_trees[day_name] = tree
            # Torna os exercícios clicáveis
            tree.bind("<Double-1>", self.on_exercise_click) # Duplo clique

    def clear_frame(self):
        """Limpa todos os widgets do frame mestre."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_input_field(self, parent_frame, label_text, entry_name):
        """Cria um rótulo e um campo de entrada."""
        frame = ttk.Frame(parent_frame, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, background=self.light_blue, foreground=self.dark_blue).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
        setattr(self, entry_name, entry)

    def create_combobox_field(self, parent_frame, label_text, var_name, values):
        """Cria um rótulo e uma combobox."""
        frame = ttk.Frame(parent_frame, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, background=self.light_blue, foreground=self.dark_blue).pack(side=tk.LEFT, padx=5)
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
            idade = self.entrada_idade.get()
            altura = self.entrada_altura.get()
            peso = self.entrada_peso.get()
            nivel = self.nivel_var.get()

            # Validação de entrada para números
            if not idade.isdigit() or not (altura.replace('.', '', 1).isdigit() and altura.count('.') <= 1) or not (peso.replace('.', '', 1).isdigit() and peso.count('.') <= 1):
                messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos para Idade, Altura e Peso.")
                return

            idade = int(idade)
            altura = float(altura)
            peso = float(peso)

            if altura <= 0 or peso <= 0 or idade <= 0:
                messagebox.showerror("Erro de Entrada", "Idade, Altura e Peso devem ser valores positivos.")
                return

            self.imc = self.calcular_imc(peso, altura) # Atribui a self.imc
            self.imc_classificacao = self.get_imc_classification(self.imc) # Atribui a self.imc_classificacao
            aerobic_time = self.get_aerobic_time(self.imc_classificacao)

            self.imc_label.config(text=f"IMC: {self.imc:.2f} ({self.imc_classificacao})")

            self.ficha_semanal = self.generate_weekly_plan(nivel, self.imc_classificacao, aerobic_time)
            self.display_weekly_plan()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def generate_weekly_plan(self, nivel, imc_classificacao, aerobic_time):
        """Gera o plano de treino semanal com base no nível e IMC."""
        plan = {}
        # Filtra exercícios com base no nível. Inclui níveis mais básicos para maior variedade.
        exercicios_base = self.df_exercicios[self.df_exercicios["Nivel"].isin([nivel, "Básico", "Intermediário"])].copy()

        if nivel == "Básico":
            plan = self._generate_abc_plan(exercicios_base, aerobic_time, imc_classificacao)
        elif nivel == "Intermediário":
            plan = self._generate_ppl_upper_lower_plan(exercicios_base, aerobic_time, imc_classificacao)
        elif nivel == "Avançado":
            plan = self._generate_upper_lower_plan(exercicios_base, aerobic_time, imc_classificacao)
        
        return plan

    def _get_random_exercises(self, df, group, num_exercises, exercise_type=None, exclude_names=None, include_high_demand=False):
        """
        Seleciona exercícios aleatórios de um grupo, com opção de tipo e exclusão.
        'exclude_names' é usado para evitar repetição DENTRO da mesma ficha diária.
        'include_high_demand' prioriza exercícios de alta demanda se True.
        """
        if exclude_names is None:
            exclude_names = set()

        # Filtra por grupo e exclui exercícios já selecionados para o dia
        available_exercises = df[(df["Grupo"] == group) & (~df["Nome"].isin(exclude_names))].copy()

        if available_exercises.empty:
            return []

        # Tenta filtrar por tipo primeiro se especificado
        if exercise_type and 'Tipo' in available_exercises.columns:
            typed_exercises = available_exercises[available_exercises["Tipo"] == exercise_type]
            if not typed_exercises.empty:
                available_exercises = typed_exercises
            # else: Se não houver exercícios do tipo específico, continua com o conjunto mais amplo
            # Isso garante que a ficha não fique vazia se o filtro de tipo for muito restritivo

        selected_exercises = pd.DataFrame()

        # Prioriza alta demanda se solicitado e disponível
        if include_high_demand and not available_exercises[available_exercises["DemandaEnergetica"] == "Alta"].empty:
            high_demand_options = available_exercises[available_exercises["DemandaEnergetica"] == "Alta"]
            num_high_demand_to_select = min(len(high_demand_options), num_exercises)
            selected_high_demand = high_demand_options.sample(num_high_demand_to_select, replace=False)
            selected_exercises = pd.concat([selected_exercises, selected_high_demand])
            
            num_remaining = num_exercises - len(selected_exercises)
            if num_remaining > 0:
                remaining_options = available_exercises[~available_exercises["Nome"].isin(selected_exercises["Nome"])]
                if not remaining_options.empty:
                    selected_remaining = remaining_options.sample(min(len(remaining_options), num_remaining), replace=False)
                    selected_exercises = pd.concat([selected_exercises, selected_remaining])
        else:
            # Se não há prioridade de alta demanda ou não há exercícios de alta demanda, apenas amostra do disponível
            selected_exercises = available_exercises.sample(min(len(available_exercises), num_exercises), replace=False)
        
        if selected_exercises.empty:
            # Fallback final: se após todos os filtros, nada for selecionado, tenta pegar QUALQUER exercício
            # do grupo inicial (filtrado apenas por grupo e exclusão) para evitar ficha vazia.
            initial_group_exercises = df[(df["Grupo"] == group) & (~df["Nome"].isin(exclude_names))].copy()
            if not initial_group_exercises.empty:
                selected_exercises = initial_group_exercises.sample(min(len(initial_group_exercises), num_exercises), replace=False)

        if selected_exercises.empty:
            return []

        return selected_exercises.to_dict('records')

    def _generate_abc_plan(self, df, aerobic_time, imc_classificacao):
        """Gera um plano de treino ABC (A: Peito/Tríceps/Abdômen, B: Costas/Bíceps, C: Pernas/Ombros)."""
        plan = {}
        
        # Determina se deve incluir alta demanda para sobrepeso/obesidade
        include_high_demand_strength = "Obesidade" in imc_classificacao or "Sobrepeso" in imc_classificacao

        # Dia 1: Peito, Tríceps, Abdômen
        day1_picked_names = set()
        day1_exercises = []
        
        exercises_peito_comp = self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names, include_high_demand_strength)
        day1_exercises.extend(exercises_peito_comp)
        day1_picked_names.update([ex["Nome"] for ex in exercises_peito_comp if "Nome" in ex])
        
        exercises_peito_iso = self._get_random_exercises(df, "Peito", 1, "Isolado", day1_picked_names, include_high_demand_strength)
        day1_exercises.extend(exercises_peito_iso)
        day1_picked_names.update([ex["Nome"] for ex in exercises_peito_iso if "Nome" in ex])

        exercises_triceps = self._get_random_exercises(df, "Tríceps", 2, None, day1_picked_names, include_high_demand_strength)
        day1_exercises.extend(exercises_triceps)
        day1_picked_names.update([ex["Nome"] for ex in exercises_triceps if "Nome" in ex])

        exercises_abdomen = self._get_random_exercises(df, "Abdômen", 1, None, day1_picked_names, include_high_demand_strength)
        day1_exercises.extend(exercises_abdomen)
        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Costas, Bíceps
        day2_picked_names = set()
        day2_exercises = []
        exercises_costas_comp = self._get_random_exercises(df, "Costas", 3, "Composto", day2_picked_names, include_high_demand_strength)
        day2_exercises.extend(exercises_costas_comp)
        day2_picked_names.update([ex["Nome"] for ex in exercises_costas_comp if "Nome" in ex])

        exercises_biceps = self._get_random_exercises(df, "Bíceps", 2, None, day2_picked_names, include_high_demand_strength)
        day2_exercises.extend(exercises_biceps)
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Pernas, Ombros
        day3_picked_names = set()
        day3_exercises = []
        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 3, "Composto", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])

        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 1, "Isolado", day3_picked_names, include_high_demand_strength) )
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])

        exercises_ombros_comp = self._get_random_exercises(df, "Ombros", 2, "Composto", day3_picked_names, include_high_demand_strength)
        day3_exercises.extend(exercises_ombros_comp)
        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        plan["Dia 4"] = [{"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}]
        plan["Dia 5"] = [{"Nome": "Descanso Ativo / Aeróbico", "Grupo": "Descanso", "Séries": "-", "Repetições": "-", "Tipo": "Recuperação"}]

        return plan

    def _generate_ppl_upper_lower_plan(self, df, aerobic_time, imc_classificacao):
        """Gera um plano de treino PPL (Push/Pull/Legs) + Upper/Lower."""
        plan = {}
        include_high_demand_strength = "Obesidade" in imc_classificacao or "Sobrepeso" in imc_classificacao

        # Dia 1: Push (Peito, Ombros, Tríceps)
        day1_picked_names = set()
        day1_exercises = []
        day1_exercises.extend(self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Tríceps", 2, None, day1_picked_names, include_high_demand_strength))
        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Pull (Costas, Bíceps)
        day2_picked_names = set()
        day2_exercises = []
        day2_exercises.extend(self._get_random_exercises(df, "Costas", 3, "Composto", day2_picked_names, include_high_demand_strength) )
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Bíceps", 2, None, day2_picked_names, include_high_demand_strength))
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Legs (Pernas, Abdômen)
        day3_picked_names = set()
        day3_exercises = []
        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 3, "Composto", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Pernas", 1, "Isolado", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day3_picked_names, include_high_demand_strength))
        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 4: Upper Body (Peito, Costas, Ombros, Bíceps, Tríceps)
        day4_picked_names = set()
        day4_exercises = []
        day4_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Composto", day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Composto", day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day4_picked_names, include_high_demand_strength))
        plan["Dia 4"] = day4_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 5: Lower Body (Pernas, Abdômen)
        day5_picked_names = set()
        day5_exercises = []
        day5_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Composto", day5_picked_names, include_high_demand_strength))
        day5_picked_names.update([ex["Nome"] for ex in day5_exercises])
        day5_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day5_picked_names, include_high_demand_strength))
        plan["Dia 5"] = day5_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        return plan

    def _generate_upper_lower_plan(self, df, aerobic_time, imc_classificacao):
        """Gera um plano de treino Upper/Lower para avançados."""
        plan = {}
        include_high_demand_strength = "Obesidade" in imc_classificacao or "Sobrepeso" in imc_classificacao

        # Dia 1: Upper Body
        day1_picked_names = set()
        day1_exercises = []
        day1_exercises.extend(self._get_random_exercises(df, "Peito", 2, "Composto", day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Costas", 2, "Composto", day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Composto", day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day1_picked_names, include_high_demand_strength))
        day1_picked_names.update([ex["Nome"] for ex in day1_exercises])
        day1_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day1_picked_names, include_high_demand_strength))
        plan["Dia 1"] = day1_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 2: Lower Body
        day2_picked_names = set()
        day2_exercises = []
        day2_exercises.extend(self._get_random_exercises(df, "Pernas", 3, "Composto", day2_picked_names, include_high_demand_strength))
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Isolado", day2_picked_names, include_high_demand_strength))
        day2_picked_names.update([ex["Nome"] for ex in day2_exercises])
        day2_exercises.extend(self._get_random_exercises(df, "Abdômen", 2, None, day2_picked_names, include_high_demand_strength))
        plan["Dia 2"] = day2_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 3: Upper Body (Variação)
        day3_picked_names = set()
        day3_exercises = []
        day3_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Composto", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Peito", 1, "Isolado", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Composto", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Costas", 1, "Isolado", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Ombros", 1, "Isolado", day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Bíceps", 1, None, day3_picked_names, include_high_demand_strength))
        day3_picked_names.update([ex["Nome"] for ex in day3_exercises])
        day3_exercises.extend(self._get_random_exercises(df, "Tríceps", 1, None, day3_picked_names, include_high_demand_strength))
        plan["Dia 3"] = day3_exercises + [{"Nome": f"Aeróbico ({aerobic_time})", "Grupo": "Cardio", "Séries": "-", "Repetições": "-", "Tipo": "Aeróbico"}]

        # Dia 4: Lower Body (Variação)
        day4_picked_names = set()
        day4_exercises = []
        day4_exercises.extend(self._get_random_exercises(df, "Pernas", 2, "Composto", day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Pernas", 1, "Isolado", day4_picked_names, include_high_demand_strength))
        day4_picked_names.update([ex["Nome"] for ex in day4_exercises])
        day4_exercises.extend(self._get_random_exercises(df, "Abdômen", 1, None, day4_picked_names, include_high_demand_strength))
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

    def on_exercise_click(self, event):
        """Exibe detalhes do exercício clicado."""
        tree = event.widget
        item_id = tree.selection()[0]
        item_values = tree.item(item_id, 'values')
        
        exercise_name = item_values[0]
        
        # Busca detalhes do exercício no DataFrame original
        exercise_details = self.df_exercicios[self.df_exercicios["Nome"] == exercise_name]

        if not exercise_details.empty:
            details = exercise_details.iloc[0]
            self.show_exercise_details_popup(details)
        else:
            messagebox.showinfo("Detalhes do Exercício", "Descrição não disponível para este exercício.")

    def show_exercise_details_popup(self, details):
        """Cria um popup para exibir a descrição e o GIF do exercício."""
        popup = tk.Toplevel(self.master)
        popup.title(details["Nome"])
        popup.geometry("700x600") # Aumenta o tamanho do popup
        popup.transient(self.master) # Torna o popup modal
        popup.grab_set() # Captura eventos enquanto o popup está aberto
        popup.focus_set() # Dá foco ao popup

        # Frame para o conteúdo do popup
        content_frame = ttk.Frame(popup, padding="15", style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Título do exercício
        ttk.Label(content_frame, text=details["Nome"], font=('Helvetica', 20, 'bold'), foreground=self.deep_blue, background=self.light_blue).pack(pady=10)

        # Frame para descrição e GIF (lado a lado)
        details_viz_frame = ttk.Frame(content_frame, style='TFrame')
        details_viz_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Descrição
        description_label = ttk.Label(details_viz_frame, text=details["DescricaoDetalhada"], wraplength=300, justify=tk.LEFT, font=('Arial', 11), foreground=self.dark_blue, background=self.light_blue)
        description_label.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # GIF
        gif_frame = ttk.Frame(details_viz_frame, style='TFrame')
        gif_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.gif_label = ttk.Label(gif_frame, background=self.light_blue)
        self.gif_label.pack(expand=True)

        gif_path = details["GifURL"]
        if gif_path and os.path.exists(gif_path):
            try:
                # Tenta carregar o GIF
                self.load_and_animate_gif(gif_path)
            except Exception as e:
                ttk.Label(gif_frame, text=f"Erro ao carregar GIF: {e}", foreground='red', background=self.light_blue).pack()
                print(f"Erro ao carregar GIF {gif_path}: {e}")
        else:
            ttk.Label(gif_frame, text="GIF de demonstração não disponível.", foreground=self.dark_blue, background=self.light_blue).pack()
            if gif_path:
                print(f"Aviso: GIF não encontrado em {gif_path}")

        # Botão Fechar
        close_button = ttk.Button(content_frame, text="Fechar", command=popup.destroy)
        close_button.pack(pady=10)

        # Garante que o popup seja destruído ao fechar a janela
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)
        # Interrompe a animação do GIF quando o popup é fechado
        popup.bind("<Destroy>", self.stop_gif_animation)

    def stop_gif_animation(self, event=None):
        """Para a animação do GIF."""
        if self.gif_animation_id:
            self.master.after_cancel(self.gif_animation_id)
            self.gif_animation_id = None
        self.gif_frames = [] # Limpa os frames
        self.current_gif_image = None # Libera a referência da imagem

    def load_and_animate_gif(self, gif_path):
        """Carrega e anima um GIF."""
        self.stop_gif_animation() # Para qualquer animação anterior

        try:
            gif_info = tk.PhotoImage(file=gif_path)
            num_frames = gif_info.cget("nframes")

            for i in range(num_frames):
                frame = tk.PhotoImage(file=gif_path, format=f"gif -index {i}")
                self.gif_frames.append(frame)
            
            self.animate_gif_loop(0) # Inicia a animação
        except Exception as e:
            messagebox.showerror("Erro de GIF", f"Não foi possível carregar ou animar o GIF: {e}")
            self.gif_label.config(image='') # Limpa imagem se houver erro
            self.gif_frames = [] # Limpa frames para evitar loop de erro

    def animate_gif_loop(self, frame_index):
        """Atualiza o frame do GIF para animá-lo em loop."""
        if not self.gif_frames:
            return # Para a animação se não houver frames

        frame = self.gif_frames[frame_index]
        self.gif_label.config(image=frame)
        self.current_gif_image = frame # Mantém uma referência para evitar que seja coletado pelo GC

        # Próximo frame
        next_frame_index = (frame_index + 1) % len(self.gif_frames)
        # Ajusta o tempo de delay (pode ser lido do GIF ou um valor padrão)
        delay = 100 # ms (ajuste conforme a velocidade desejada)
        self.gif_animation_id = self.master.after(delay, self.animate_gif_loop, next_frame_index)


# Cria a janela principal e executa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = GymAssistantApp(root)
    root.mainloop()
