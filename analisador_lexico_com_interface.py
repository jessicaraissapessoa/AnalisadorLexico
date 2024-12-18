# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re  # Biblioteca para trabalhar com expressões regulares (Regex)
import tkinter as tk  # Biblioteca para criação de interfaces gráficas
from tkinter import scrolledtext  # Biblioteca para criação de áreas de texto com barras de rolagem
from tkinter import ttk  # Biblioteca para temas modernos
import keyword  # Biblioteca para obter palavras reservadas do Python

# Constantes - Cores
BG_COLOR = "#263238"
FG_COLOR = "#ffffff"
BTN_BG_COLOR = "#37474F"
BTN_RED_COLOR = "#D32F2F"
BTN_GREEN_COLOR = "#388E3C"
BTN_HOVER_COLOR = "#546E7A"
BTN_RED_HOVER_COLOR = "#B71C1C"
BTN_GREEN_HOVER_COLOR = "#1B5E20"
HINT_COLOR = "#808080"
COMMENT_COLOR = "#9E9E9E"
SUMARIO_HOVER_COLOR = "#455A64"
SUMARIO_SELECTED_COLOR = "#1B5E20"

# constantes - Fontes
FONT_ARIAL_12 = ("Arial", 12)
FONT_COURIER_BOLD_12 = ("Courier New", 12, "bold")

# Constantes - Textos
PALAVRAS_RESERVADAS = keyword.kwlist
HINT_CODIGO = "Escreva aqui seu código em Python"
RESULTADO_ANALISE_TITULO = "Resultado da análise léxica"

# Definição dos padrões de tokens que o analisador léxico irá reconhecer
TOKEN_REGEX = [
  (r'\bTrue\b|\bFalse\b', 'VALOR BOOLEANO'), # Valores do tipo booleano (True ou False)
  (r'\bNone\b', 'VALOR NULO'), # Valor nulo (None)
  (rf'\b({"|".join(PALAVRAS_RESERVADAS)})\b', 'PALAVRAS RESERVADAS'), # Palavras reservadas pela linguagem (Python)
  (r'(?<=\bclass\s)\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - CLASSE'), # Identificador de classe
  (r'(?<=\bdef\s)\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - FUNÇÃO'), # Identificador de definição de função
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*\()', 'IDENTIFICADOR - CHAMADA FUNÇÃO'), # Identificadores que são chamadas de função
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*=)', 'IDENTIFICADOR - VARIÁVEL'), # Identificadores que são variáveis
  (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR - GERAL'), # Identificador geral
  (r'".*?"|\'.*?\'', 'STRING'), # Valores de string entre aspas simples ou duplas
  (r'\d+\.\d+', 'VALOR DECIMAL'), # Valores de ponto flutuante (números decimais)
  (r'\b\d+[eE][+-]?\d+\b', 'NOTAÇÃO CIENTÍFICA'), # Notação científica (e.g., 1e10, 2.5E-3)
  (r'\d+', 'VALOR INTEIRO'), # Valores inteiros
  (r'[+\-*/%=<>!]+', 'OPERADOR'), # Operadores matemáticos e lógicos
  (r'[(){}\[\],.:]', 'DELIMITADOR'), # Delimitadores: parênteses, chaves, colchetes, vírgulas, etc.
  (r'\#.*', 'COMENTÁRIO'), # Comentários iniciados por #
  (r' ', 'ESPAÇO') # Espaços em branco
]

# Classe do analisador léxico
class Analisador_lexico:

  # Construtor da classe
  def __init__(self, codigo):
    self.codigo = codigo # Código a ser analisado
    self.posicao = 0 # Posição inicial da análise

  # Tokenização do código-fonte
  def tokenizar(self):
    tokens = []
    while self.posicao < len(self.codigo):
      match = None
      for token_regex, tipo_token in TOKEN_REGEX:
        regex = re.compile(token_regex)
        match = regex.match(self.codigo, self.posicao)
        if match:
          if tipo_token:
            valor_token = match.group(0)
            if tipo_token == 'IDENTIFICADOR - GERAL':
                if tokens and tokens[-1][1] == 'def':
                    tipo_token = 'IDENTIFICADOR - FUNÇÃO'
                elif tokens and tokens[-1][1] == 'class':
                    tipo_token = 'IDENTIFICADOR - CLASSE'
            tokens.append((tipo_token, valor_token, self.posicao))
          self.posicao = match.end(0)
          break
      if not match:
        self.posicao += 1
    return tokens

# Função para colorir texto como editor de código: destaque de comentários
def destacar_sintaxe(event=None):
    text_area.tag_remove("comment", "1.0", tk.END)

    inicio = "1.0"
    while True:
        inicio = text_area.search(r'\#.*', inicio, stopindex=tk.END, regexp=True)
        if not inicio:
            break
        fim = f"{inicio} lineend"
        text_area.tag_add("comment", inicio, fim)
        inicio = fim

# Função para analisar o código e exibir os resultados
def analisar_codigo():
    codigo = text_area.get("1.0", tk.END)
    if not codigo.strip() or codigo.strip() == HINT_CODIGO:
        mostrar_mensagem("Por favor, insira um código válido para análise")
        return

    analisador_lexico = Analisador_lexico(codigo)
    tokens = analisador_lexico.tokenizar()

    tokens = [token for token in tokens if token[1] != HINT_CODIGO]  # Remover tokens que correspondem ao hint

    if not tokens:
        mostrar_mensagem("Por favor, insira um código válido para análise")
        return

    resultado_janela = tk.Toplevel(janela)
    resultado_janela.title(RESULTADO_ANALISE_TITULO)
    resultado_janela.configure(bg=BG_COLOR)

    # Frame principal para dividir o sumário e os resultados
    frame_principal = tk.Frame(resultado_janela, bg=BG_COLOR)
    frame_principal.pack(fill='both', expand=True)

    # Criação do sumário para as categorias encontradas
    frame_sumario = tk.Frame(frame_principal, bg=BG_COLOR)
    frame_sumario.pack(side='left', padx=10, pady=10, anchor='n', fill='y')

    # Container para os resultados
    text_resultados = scrolledtext.ScrolledText(frame_principal, font=FONT_COURIER_BOLD_12, wrap=tk.WORD, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, highlightthickness=0, borderwidth=0, state='normal')
    text_resultados.pack(side='left', padx=20, pady=(20, 0), fill="both", expand=True)

    for categoria, valores in agrupar_tokens(tokens).items():
        text_resultados.insert(tk.END, f"\n{categoria}: {len(valores)} token(s)\n")

    text_resultados.config(state='disabled')

    # Frame para os botões na parte inferior
    frame_botoes_resultado = tk.Frame(resultado_janela, bg=BG_COLOR)
    frame_botoes_resultado.pack(side='bottom', pady=20)

    # Botão "Ver detalhes"
    btn_detalhes = ttk.Button(frame_botoes_resultado, text="Ver detalhes", command=lambda: exibir_detalhes(tokens, text_resultados, btn_detalhes, frame_sumario))
    btn_detalhes.configure(style='Green.TButton')
    btn_detalhes.pack(side="left", padx=10)

# Função para exibir os detalhes dos tokens
def exibir_detalhes(tokens, text_widget, btn_detalhes, frame_sumario):
    global categoria_selecionada
    categoria_selecionada = None

    text_widget.config(state='normal')
    if btn_detalhes['text'] == "Ver detalhes":
        text_widget.delete("1.0", tk.END)
        categorias_posicoes = {}
        for categoria, valores in agrupar_tokens(tokens).items():
            posicao_inicio = text_widget.index(tk.END)
            text_widget.insert(tk.END, f"\n\n{categoria}: {len(valores)} token(s)\n{'=' * 80}\n")
            categorias_posicoes[categoria] = posicao_inicio
            for valor in valores:
                if categoria == 'ESPAÇO':
                    text_widget.insert(tk.END, f"\u2022 Espaço em posição [{valor[1]}]\n")
                else:
                    text_widget.insert(tk.END, f"\u2022 {valor[0]}\n")

        # Limpar frame do sumário e recriar botões
        for widget in frame_sumario.winfo_children():
            widget.destroy()

        label_sumario = tk.Label(frame_sumario, text="Selecione categoria:", font=FONT_ARIAL_12, fg=FG_COLOR, bg=BG_COLOR)
        label_sumario.pack(pady=(0, 10))

        for categoria in categorias_posicoes.keys():
            btn_categoria = tk.Button(
                frame_sumario, text=categoria,
                command=lambda cat=categoria: destacar_categoria(cat, categorias_posicoes, text_widget, frame_sumario),
                bg=BTN_BG_COLOR, fg=FG_COLOR, relief="flat",
                activebackground=SUMARIO_HOVER_COLOR
            )
            btn_categoria.pack(fill='x', pady=2)
            btn_categoria.bind("<Enter>", lambda e, b=btn_categoria: b.config(bg=SUMARIO_HOVER_COLOR))
            btn_categoria.bind("<Leave>", lambda e, b=btn_categoria: b.config(bg=BTN_BG_COLOR if b.cget("text") != categoria_selecionada else SUMARIO_SELECTED_COLOR))

        text_widget.bind("<MouseWheel>", lambda e: atualizar_destacado(text_widget, categorias_posicoes, frame_sumario))

        btn_detalhes.config(text="Ver resumo", style='Red.TButton')
    else:
        text_widget.delete("1.0", tk.END)
        for categoria, valores in agrupar_tokens(tokens).items():
            text_widget.insert(tk.END, f"\n{categoria}: {len(valores)} token(s)\n")

        # Remover sumário ao voltar para a visão resumida
        for widget in frame_sumario.winfo_children():
            widget.destroy()

        categoria_selecionada = None

        btn_detalhes.config(text="Ver detalhes", style='Green.TButton')
    text_widget.config(state='disabled')

# Função para destacar a categoria selecionada no sumário
def destacar_categoria(categoria, categorias_posicoes, text_widget, frame_sumario):
    global categoria_selecionada
    categoria_selecionada = categoria

    # Destacar botão selecionado
    for widget in frame_sumario.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == categoria:
            widget.config(bg=SUMARIO_SELECTED_COLOR)
        elif isinstance(widget, tk.Button):
            widget.config(bg=BTN_BG_COLOR)

    # Scroll até a categoria selecionada
    text_widget.yview_moveto(float(text_widget.index(categorias_posicoes[categoria]).split('.')[0]) / int(text_widget.index(tk.END).split('.')[0]))

# Função para atualizar a cor do botão destacado ao scrollar os resultados
def atualizar_destacado(text_widget, categorias_posicoes, frame_sumario):
    global categoria_selecionada
    if categoria_selecionada:
        posicao_selecionada = text_widget.index(categorias_posicoes[categoria_selecionada]).split('.')[0]
        posicao_atual = text_widget.index("@0,0").split('.')[0]
        if posicao_selecionada != posicao_atual:
            categoria_selecionada = None
            for widget in frame_sumario.winfo_children():
                if isinstance(widget, tk.Button):  # Verificar se o widget é um botão
                    widget.config(bg=BTN_BG_COLOR)

# Função para agrupar os tokens por categoria
def agrupar_tokens(tokens):
    categorias = {}
    for tipo_token, valor_token, posicao in tokens:
        categorias.setdefault(tipo_token, []).append((valor_token, posicao))
    return categorias

# Função para mostrar mensagem de erro
def mostrar_mensagem(mensagem):
    resultado_janela = tk.Toplevel(janela)
    resultado_janela.title(RESULTADO_ANALISE_TITULO)
    resultado_janela.configure(bg=BG_COLOR)
    resultado_texto = tk.Label(resultado_janela, text=mensagem, font=FONT_ARIAL_12, bg=BG_COLOR, fg=FG_COLOR, justify="left")
    resultado_texto.pack(padx=20, pady=20)
    
    # Botão para fechar a janela
    btn_fechar = ttk.Button(resultado_janela, text="Fechar", command=resultado_janela.destroy)
    btn_fechar.configure(style='Red.TButton')
    btn_fechar.pack(pady=10)

# Funções para interação com o editor de texto

def on_focus_in(event):
    if text_area.get("1.0", tk.END).strip() == HINT_CODIGO:
        text_area.delete("1.0", tk.END)
        text_area.config(fg=FG_COLOR)

def on_focus_out(event):
    if not text_area.get("1.0", tk.END).strip():
        inserir_hint()

def limpar_editor():
    text_area.delete('1.0', tk.END)
    inserir_hint()

def inserir_hint():
    text_area.insert("1.0", HINT_CODIGO)
    text_area.config(fg=HINT_COLOR)

# Código principal da aplicação
if __name__ == '__main__':
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("Analisador léxico para código Python")
    largura_janela = int(janela.winfo_screenwidth() * 0.5)
    altura_janela = int(janela.winfo_screenheight() * 0.6)
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    janela.configure(bg=BG_COLOR)  # Cor de fundo em dark mode

    # Estilo para widgets
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Tema mais moderno

    # Aplicação de estilizações nos botões
    estilo.configure("TButton", foreground=FG_COLOR, background=BTN_BG_COLOR, font=FONT_ARIAL_12, padding=6)
    estilo.configure("Red.TButton", foreground=FG_COLOR, background=BTN_RED_COLOR, font=FONT_ARIAL_12, padding=6)
    estilo.configure("Green.TButton", foreground=FG_COLOR, background=BTN_GREEN_COLOR, font=FONT_ARIAL_12, padding=6)
    estilo.map("TButton", background=[("active", BTN_HOVER_COLOR)])
    estilo.map("Red.TButton", background=[("active", BTN_RED_HOVER_COLOR)])
    estilo.map("Green.TButton", background=[("active", BTN_GREEN_HOVER_COLOR)])

    # Criação da área de texto para entrada do código
    text_area = scrolledtext.ScrolledText(janela, font=FONT_COURIER_BOLD_12, wrap=tk.WORD, bg=BG_COLOR, fg=HINT_COLOR, insertbackground=FG_COLOR)
    text_area.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)
    text_area.insert("1.0", HINT_CODIGO)
    
    text_area.bind("<FocusIn>", on_focus_in)
    text_area.bind("<FocusOut>", on_focus_out)
    text_area.bind("<KeyRelease>", destacar_sintaxe)  # Vincula a coloração de sintaxe ao evento de tecla pressionada

    # Configuração de tags para sintaxe
    text_area.tag_configure("comment", foreground=COMMENT_COLOR)

    # Frame para os botões
    frame_botoes = tk.Frame(janela, bg=BG_COLOR)
    frame_botoes.pack(side='bottom', pady=20)

    # Botão para limpar o editor de texto
    btn_limpar = ttk.Button(frame_botoes, text="Limpar editor", command=limpar_editor)
    btn_limpar.configure(style='Red.TButton')
    btn_limpar.pack(side='left', padx=10)

    # Botão para executar a análise léxica
    btn_analisar = ttk.Button(frame_botoes, text="Analisar código", command=analisar_codigo)
    btn_analisar.configure(style='Green.TButton')
    btn_analisar.pack(side='left', padx=10)

    # Execução da interface gráfica
    janela.mainloop()