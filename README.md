Assistente de Academia


Este é um aplicativo desktop simples desenvolvido em Python com tkinter e pandas que atua como um assistente de academia. Ele calcula o Índice de Massa Corporal (IMC) do usuário e, com base nessa avaliação, sugere exercícios físicos personalizados.

Funcionalidades
Cálculo de IMC: O usuário insere idade, altura (em cm) e peso (em kg) para obter seu IMC.

Classificação de IMC: O programa classifica o IMC do usuário (Abaixo do peso, Peso normal, Sobrepeso, Obesidade Grau I, II ou III).

Recomendação de Exercícios Personalizada:

Para usuários com obesidade, são sugeridos exercícios com maior demanda energética.

Para usuários com peso normal, é gerada uma ficha de treino com um exercício por grupo muscular, e o usuário pode optar por substituir exercícios.

Interface Gráfica Intuitiva: Desenvolvido com tkinter para uma experiência de usuário simples e direta.

Gerenciamento de Dados de Exercícios: Utiliza pandas para ler e manipular os dados de exercícios a partir de um arquivo CSV.

Tecnologias Utilizadas
Python: Linguagem de programação principal.

Tkinter: Biblioteca padrão do Python para criação de interfaces gráficas.

Pandas: Biblioteca para manipulação e análise de dados, utilizada para gerenciar os exercícios.

Como Executar
Pré-requisitos
Certifique-se de ter Python instalado em sua máquina. Você pode baixá-lo em python.org.

Instale as bibliotecas necessárias:

pip install pandas

Arquivo de Dados (exercicios.csv)
O programa espera um arquivo exercicios.csv na mesma pasta do script principal. Este arquivo deve conter os dados dos exercícios. Um exemplo de estrutura e dados para exercicios.csv é fornecido abaixo:

Nome,Grupo,Nivel,DemandaEnergetica

Pular Corda (25 min),Corpo Inteiro,Intermediário,Alta
Natação (45 min),Corpo Inteiro,Avançado,Alta
Ciclismo (40 min),Pernas,Intermediário,Alta
Supino Reto com Halteres,Peito,Básico,Baixa
Flexão de Braço,Peito,Básico,Baixa
Crucifixo com Halteres,Peito,Intermediário,Baixa
Remada Curvada com Barra,Costas,Intermediário,Baixa


Crie um arquivo chamado exercicios.csv com este conteúdo e salve-o no mesmo diretório do seu script gym_assistant_tkinter.py.

Executando o Aplicativo
Salve o código principal (por exemplo, gym_assistant_tkinter.py) e o arquivo exercicios.csv no mesmo diretório.

Abra um terminal ou prompt de comando.

Navegue até o diretório onde você salvou os arquivos.

Execute o script Python:

python gym_assistant_tkinter.py

Uso
Ao iniciar o aplicativo, insira sua Idade, Altura (cm) e Peso (kg) nos campos correspondentes.

Selecione seu Nível de treino (Básico, Intermediário, Avançado) na caixa de seleção.

Clique no botão "Gerar Ficha".

O aplicativo exibirá seu IMC e uma ficha de treino recomendada na tabela.

Se desejar, você pode usar os botões "Trocar [Grupo Muscular]" para substituir um exercício específico da ficha.

Contribuição
Contribuições são bem-vindas! Se você tiver sugestões de melhorias, detecção de bugs ou novas funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request.
