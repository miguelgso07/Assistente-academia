#configurações do programa
# aqui são criadas as constantes de arquivos e dados, não precisa mexer 
CSV_FILE_PATH = "data/exercicios.csv" 
REQUIRED_COLUMNS = ["Nome", "Grupo", "Nivel", "DemandaEnergetica", "Tipo", "DescricaoDetalhada", "GifURL"]

# paleta de cores, aqui são somente tons de azul 
PRIMARY_BLUE = '#2196F3'
DARK_BLUE = '#1976D2'
LIGHT_BLUE = '#E3F2FD'
MEDIUM_BLUE = '#BBDEFB'
DARKER_BLUE = '#1565C0'
DEEP_BLUE = '#0D47A1'


Niveis_de_treino = ["Básico", "Intermediário", "Avançado"]

#estilos visuais do tkinter 
def setup_styles(style):
    style.theme_use('clam')
    style.configure('TFrame', background=LIGHT_BLUE)
    style.configure('TLabel', background=LIGHT_BLUE, font=('Arial', 11), foreground=DARK_BLUE)
    style.configure('TEntry', font=('Arial', 11))
    style.configure('TButton', font=('Arial', 11, 'bold'), background=PRIMARY_BLUE, foreground='white', borderwidth=0)
    style.map('TButton', background=[('active', DARKER_BLUE)])
    style.configure('TCombobox', font=('Arial', 11))
    style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), background=MEDIUM_BLUE, foreground=DARK_BLUE)
    style.map('TNotebook.Tab', background=[('selected', PRIMARY_BLUE)], foreground=[('selected', 'white')])
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background=DARKER_BLUE, foreground='white')
    style.configure('Treeview', font=('Arial', 10), rowheight=25)