# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re  # Biblioteca para trabalhar com expressões regulares (Regex)
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk  # Biblioteca para temas modernos
import keyword  # Biblioteca para obter palavras reservadas do Python

# Array de palavras reservadas
PALAVRAS_RESERVADAS = keyword.kwlist

# Definição dos padrões de tokens que o analisador léxico irá reconhecer
TOKEN_REGEX = [
  (r'\bTrue\b|\bFalse\b', 'VALOR BOOLEANO'), # Valores do tipo booleano (True ou False)
  (r'\bNone\b', 'VALOR NULO'), # Valor nulo (None)
  (rf'\b({"|".join(PALAVRAS_RESERVADAS)})\b', 'PALAVRAS RESERVADAS'), # Palavras reservadas pela linguagem (Python)
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*\()', 'IDENTIFICADOR FUNÇÃO'), # Identificadores que são funções
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*=)', 'IDENTIFICADOR VARIÁVEL'), # Identificadores que são variáveis
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR ISOLADO'), # Identificador isolado
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

      # Variável que armazena correspondência com padrão inializa como None
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

def analisar_codigo():
    codigo = text_area.get("1.0", tk.END).strip()
    if codigo == "Escreva aqui seu código em Python" or not codigo:
        resultado_janela = tk.Toplevel(janela)
        resultado_janela.title("Resultado da Análise Léxica")
        resultado_janela.configure(bg="#263238")
        resultado_texto = tk.Label(
            resultado_janela, 
            text="Por favor, insira um código válido para análise.", 
            font=("Arial", 12), 
            bg="#263238", 
            fg="#ffffff", 
            justify="left"
        )
        resultado_texto.pack(padx=20, pady=20)
        btn_fechar = ttk.Button(resultado_janela, text="Fechar", command=resultado_janela.destroy)
        btn_fechar.pack(pady=(0, 10))
        return
    
    # Analisar o código com o analisador léxico
    analisador = Analisador_lexico(codigo)
    tokens = analisador.tokenizar()
    
    # Exibir o resultado da análise em uma nova janela
    resultado_janela = tk.Toplevel(janela)
    resultado_janela.title("Resultado da Análise Léxica")
    resultado_janela.configure(bg="#263238")
    
    resultado_texto = scrolledtext.ScrolledText(
        resultado_janela, 
        font=("Courier New", 12), 
        wrap=tk.WORD, 
        bg="#263238", 
        fg="#ffffff", 
        insertbackground="#ffffff"
    )
    resultado_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    for tipo, valor in tokens:
        resultado_texto.insert(tk.END, f"{tipo}: {valor}\n")
    
    btn_fechar = ttk.Button(resultado_janela, text="Fechar", command=resultado_janela.destroy)
    btn_fechar.pack(pady=(0, 10))

def on_focus_in(event):
    if text_area.get("1.0", tk.END).strip() == "Escreva aqui seu código em Python":
        text_area.delete("1.0", tk.END)
        text_area.config(fg="#ffffff")

def on_focus_out(event):
    if not text_area.get("1.0", tk.END).strip():
        text_area.insert("1.0", "Escreva aqui seu código em Python")
        text_area.config(fg="#808080")

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
    estilo.map("TButton", background=[("active", "#455A64")])

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

    # Botão para executar a análise léxica
    btn_analisar = ttk.Button(janela, text="Analisar Código", command=analisar_codigo, width=15)
    btn_analisar.place(relx=0.5, rely=0.75, anchor='center')

    # Execução da interface gráfica
    janela.mainloop()
