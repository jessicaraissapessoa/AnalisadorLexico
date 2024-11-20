# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re  # Biblioteca para trabalhar com expressões regulares (Regex)
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  # Biblioteca para temas modernos
import keyword  # Biblioteca para obter palavras reservadas do Python

# Array de palavras reservadas
PALAVRAS_RESERVADAS = keyword.kwlist

# Definição dos padrões de tokens que o analisador léxico irá reconhecer
TOKEN_REGEX = [
  (r'\bTrue\b|\bFalse\b', 'VALOR BOOLEANO'), # Valores do tipo booleano (True ou False)
  (r'\bNone\b', 'VALOR NULO'), # Valor nulo (None)
  (rf'\b({'|'.join(PALAVRAS_RESERVADAS)})\b', 'PALAVRAS RESERVADAS'), # Palavras reservadas pela linguagem (Python)
  (r'(?<=\bclass\s)\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - CLASSE'), # Identificador de classe
  (r'(?<=\bdef\s)\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - FUNÇÃO'), # Identificador de definição de função
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*\()', 'IDENTIFICADOR - CHAMADA FUNÇÃO'), # Identificadores que são chamadas de função
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*=)', 'IDENTIFICADOR - VARIÁVEL'), # Identificadores que são variáveis
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - GERAL'), # Identificador geral
  (r'\".*?\"|\'.*?\'', 'STRING'), # Valores de string entre aspas simples ou duplas
  (r'\d+\.\d+', 'VALOR DECIMAL'), # Valores de ponto flutuante (números decimais)
  (r'\b\d+[eE][+-]?\d+\b', 'NOTAÇÃO CIENTÍFICA'), # Notação científica (e.g., 1e10, 2.5E-3)
  (r'\d+', 'VALOR INTEIRO'), # Valores inteiros
  (r'[+\-*/%=<>!]+', 'OPERADOR'), # Operadores matemáticos e lógicos
  (r'[(){}\[\],.:]', 'DELIMITADOR'), # Delimitadores: parênteses, chaves, colchetes, vírgulas, etc.
  (r'\#.*', 'COMENTÁRIO'), # Comentários iniciados por #
  (r'\s+', None),  # Ignorar espaços em branco
  (r'.', 'CARACTERE NÃO RECONHECIDO')  # Qualquer outro caractere que não se enquadre nas categorias anteriores
]

# Classe do analisador léxico
class Analisador_lexico:

  # Construtor da classe
  def __init__(self, codigo):
    # Inicializa o analisador léxico com o código fonte a ser analisado
    self.codigo = codigo # Código a ser analisado
    self.posicao = 0 # Posição inicial da análise

  # Tokenização do código-fonte
  def tokenizar(self):
    # Lista que armazena os tokens encontrados
    tokens = []
    # Percorrendo o código-fonte até a posição ser igual ao comprimento do código
    while self.posicao < len(self.codigo):
      # Variável que armazena correspondência com padrão inicializa como None
      match = None
      # Iteração sobre os padrões definidos em TOKEN_REGEX
      for token_regex, tipo_token in TOKEN_REGEX:
        # Compila a expressão regular do token atual
        regex = re.compile(token_regex)
        # Tenta encontrar uma correspondência no código a partir da posição atual
        match = regex.match(self.codigo, self.posicao)
        # Se o tipo do token não for None (ou seja, se não for um espaço em branco)
        if match:
          if tipo_token:  # Se não for um espaço em branco
            valor_token = match.group(0) # Captura o valor do token correspondente
            if tipo_token == 'IDENTIFICADOR - GERAL':
                if tokens and tokens[-1][1] == 'def':
                    tipo_token = 'IDENTIFICADOR - FUNÇÃO'
                elif tokens and tokens[-1][1] == 'class':
                    tipo_token = 'IDENTIFICADOR - CLASSE'
            tokens.append((tipo_token, valor_token)) # Adiciona o token à lista de tokens
          self.posicao = match.end(0) # Atualiza a posição do analisador
          break
      # Se nenhum padrão corresponder ao caractere atual, ignora o caractere não esperado para evitar erro
      if not match:
        self.posicao += 1 # Avança para o próximo caractere para evitar ficar preso em um caractere inválido
    # Retorna a lista de tokens identificados
    return tokens

# Função para colorir o texto como em um editor de código
def destacar_sintaxe(event=None):
    text_area.tag_remove("keyword", "1.0", tk.END)
    text_area.tag_remove("string", "1.0", tk.END)
    text_area.tag_remove("comment", "1.0", tk.END)

    # Destacando palavras reservadas
    for palavra_reservada in PALAVRAS_RESERVADAS:
        inicio = "1.0"
        while True:
            inicio = text_area.search(rf'\b{palavra_reservada}\b', inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fim = f"{inicio}+{len(palavra_reservada)}c"
            text_area.tag_add("keyword", inicio, fim)
            inicio = fim

    # Destacando strings
    for padrao in [r'".*?"', r'\'.*?\'']:
        inicio = "1.0"
        while True:
            inicio = text_area.search(padrao, inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fim = f"{inicio}+{len(text_area.get(inicio, tk.END).split('\n', 1)[0])}c"
            text_area.tag_add("string", inicio, fim)
            inicio = fim

    # Destacando comentários
    inicio = "1.0"
    while True:
        inicio = text_area.search(r'\#.*', inicio, stopindex=tk.END, regexp=True)
        if not inicio:
            break
        fim = f"{inicio}+{len(text_area.get(inicio, tk.END).split('\n', 1)[0])}c"
        text_area.tag_add("comment", inicio, fim)
        inicio = fim

# Função para analisar o código e exibir os resultados
def analisar_codigo():
    codigo = text_area.get("1.0", tk.END)
    if codigo.strip() == "Escreva aqui seu código em Python" or not codigo.strip():
        resultado_janela = tk.Toplevel(janela)
        resultado_janela.title("Resultado da Análise Léxica")
        resultado_janela.configure(bg="#263238")
        resultado_texto = tk.Label(resultado_janela, text="Por favor, insira um código válido para análise", font=("Arial", 12), bg="#263238", fg="#ffffff", justify="left")
        resultado_texto.pack(padx=20, pady=20)
        
        # Botão para fechar a janela
        btn_fechar = ttk.Button(resultado_janela, text="Fechar", command=resultado_janela.destroy)
        btn_fechar.configure(style='Red.TButton')
        btn_fechar.pack(pady=10)
        
        return

    analisador_lexico = Analisador_lexico(codigo)
    tokens = analisador_lexico.tokenizar()

    resultado_janela = tk.Toplevel(janela)
    resultado_janela.title("Resultado da Análise Léxica")
    resultado_janela.configure(bg="#263238")

    # Container para os resultados
    text_resultados = scrolledtext.ScrolledText(resultado_janela, font=("Courier New", 12, "bold"), wrap=tk.WORD, bg="#263238", fg="#ffffff", insertbackground="#ffffff", highlightthickness=0, borderwidth=0, state='normal')
    text_resultados.pack(padx=20, pady=(20, 0), fill="both", expand=True)

    if not tokens:
        text_resultados.insert("1.0", "Nenhum token válido encontrado. O código fornecido está vazio =(")
    else:
        for categoria, valores in agrupar_tokens(tokens).items():
            text_resultados.insert(tk.END, f"\n{categoria}: {len(valores)} token(s)\n")

    text_resultados.config(state='disabled')

    # Frame para os botões na parte inferior
    frame_botoes_resultado = tk.Frame(resultado_janela, bg='#263238')
    frame_botoes_resultado.pack(side='bottom', pady=20)

    # Botão "Ver detalhes"
    btn_detalhes = ttk.Button(frame_botoes_resultado, text="Ver detalhes", command=lambda: exibir_detalhes(tokens, text_resultados, btn_detalhes))
    btn_detalhes.configure(style='Green.TButton')
    btn_detalhes.pack(side="left", padx=10)

# Função para exibir os detalhes dos tokens
def exibir_detalhes(tokens, text_widget, btn_detalhes):
    text_widget.config(state='normal')
    if btn_detalhes['text'] == "Ver detalhes":
        text_widget.delete("1.0", tk.END)
        for categoria, valores in agrupar_tokens(tokens).items():
            text_widget.insert(tk.END, f"\n\n{categoria}: {len(valores)} token(s)\n{'=' * 80}\n")
            for token in valores:
                text_widget.insert(tk.END, f"• {token}\n")
        btn_detalhes.config(text="Ver resumo", style='Red.TButton')
    else:
        text_widget.delete("1.0", tk.END)
        for categoria, valores in agrupar_tokens(tokens).items():
            text_widget.insert(tk.END, f"\n{categoria}: {len(valores)} token(s)\n")
        btn_detalhes.config(text="Ver detalhes", style='Green.TButton')
    text_widget.config(state='disabled')

# Função para agrupar os tokens por categoria
def agrupar_tokens(tokens):
    categorias = {}
    for tipo_token, valor_token in tokens:
        if tipo_token not in categorias:
            categorias[tipo_token] = []
        categorias[tipo_token].append(valor_token)
    return categorias

# Funções para interação com o editor de texto
def on_focus_in(event):
    if text_area.get("1.0", tk.END).strip() == "Escreva aqui seu código em Python":
        text_area.delete("1.0", tk.END)
        text_area.config(fg="#ffffff")

def on_focus_out(event):
    if not text_area.get("1.0", tk.END).strip():
        inserir_hint()

def limpar_editor():
    text_area.delete('1.0', tk.END)
    inserir_hint()

def inserir_hint():
    text_area.insert("1.0", "Escreva aqui seu código em Python")
    text_area.config(fg="#808080")

# Código principal da aplicação
if __name__ == '__main__':
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("Analisador léxico para código Python")
    janela.update_idletasks()
    largura_janela = int(janela.winfo_screenwidth() * 0.5)
    altura_janela = int(janela.winfo_screenheight() * 0.6)
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    janela.configure(bg="#263238")  # Cor de fundo em dark mode (Material Design Dark)

    # Estilo moderno para widgets
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Tema moderno

    # Cores inspiradas no Material Design para dark mode
    estilo.configure("TButton", foreground="#ffffff", background="#37474F", font=("Arial", 12), padding=6)
    estilo.configure("Red.TButton", foreground="#ffffff", background="#D32F2F", font=("Arial", 12), padding=6)
    estilo.configure("Green.TButton", foreground="#ffffff", background="#388E3C", font=("Arial", 12), padding=6)
    estilo.map("TButton", background=[("active", "#546E7A")])
    estilo.map("Red.TButton", background=[("active", "#B71C1C")])
    estilo.map("Green.TButton", background=[("active", "#1B5E20")])

    # Criação da área de texto para entrada do código
    text_area = scrolledtext.ScrolledText(janela, font=("Courier New", 12), wrap=tk.WORD, bg="#263238", fg="#808080", insertbackground="#ffffff")
    text_area.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)
    text_area.insert("1.0", "Escreva aqui seu código em Python")
    
    text_area.bind("<FocusIn>", on_focus_in)
    text_area.bind("<FocusOut>", on_focus_out)
    text_area.bind("<KeyRelease>", destacar_sintaxe)  # Vincula a coloração de sintaxe ao evento de tecla pressionada

    # Configuração de tags para sintaxe
    text_area.tag_configure("keyword", foreground="#FF5722")
    text_area.tag_configure("string", foreground="#4CAF50")
    text_area.tag_configure("comment", foreground="#9E9E9E")

    # Frame para os botões
    frame_botoes = tk.Frame(janela, bg='#263238')
    frame_botoes.pack(side='bottom', pady=20)

    # Botão para limpar o editor de texto
    btn_limpar = ttk.Button(frame_botoes, text="Limpar editor", command=lambda: limpar_editor())
    btn_limpar.configure(style='Red.TButton')
    btn_limpar.pack(side='left', padx=10)

    # Botão para executar a análise léxica
    btn_analisar = ttk.Button(frame_botoes, text="Analisar código", command=analisar_codigo)
    btn_analisar.configure(style='Green.TButton')
    btn_analisar.pack(side='left', padx=10)

    # Execução da interface gráfica
    janela.mainloop()