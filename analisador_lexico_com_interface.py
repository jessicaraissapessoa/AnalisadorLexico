# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import keyword

PALAVRAS_RESERVADAS = keyword.kwlist

TOKEN_REGEX = [
    (r'\bTrue\b|\bFalse\b', 'VALOR BOOLEANO'),
    (r'\bNone\b', 'VALOR NULO'),
    (rf'\b({"|".join(PALAVRAS_RESERVADAS)})\b', 'PALAVRAS RESERVADAS'),
    (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*\()', 'IDENTIFICADOR FUNÇÃO'),
    (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b(?=\s*=)', 'IDENTIFICADOR VARIÁVEL'),
    (r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', 'IDENTIFICADOR ISOLADO'),
    (r'".*?"|\'.*?\'', 'STRING'),
    (r'\d+\.\d+', 'VALOR DECIMAL'),
    (r'\b\d+[eE][+-]?\d+\b', 'NOTAÇÃO CIENTÍFICA'),
    (r'\d+', 'VALOR INTEIRO'),
    (r'[+\-*/%=<>!]+', 'OPERADOR'),
    (r'[(){}\[\],.:]', 'DELIMITADOR'),
    (r'\#.*', 'COMENTÁRIO'),
    (r'\s+', None),
    (r'.', 'CARACTERE NÃO RECONHECIDO')
]

class Analisador_lexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0

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
                        tokens.append((tipo_token, valor_token))
                    self.posicao = match.end(0)
                    break
            if not match:
                self.posicao += 1
        return tokens

def destacar_sintaxe(event=None):
    text_area.tag_remove("keyword", "1.0", tk.END)
    text_area.tag_remove("string", "1.0", tk.END)
    text_area.tag_remove("comment", "1.0", tk.END)

    for palavra_reservada in PALAVRAS_RESERVADAS:
        inicio = "1.0"
        while True:
            inicio = text_area.search(rf'\b{palavra_reservada}\b', inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fim = f"{inicio}+{len(palavra_reservada)}c"
            text_area.tag_add("keyword", inicio, fim)
            inicio = fim

    for padrao in [r'".*?"', r'\'.*?\'']:
        inicio = "1.0"
        while True:
            inicio = text_area.search(padrao, inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fim = f"{inicio}+{len(text_area.get(inicio, tk.END).split('\n', 1)[0])}c"
            text_area.tag_add("string", inicio, fim)
            inicio = fim

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

    analisador = Analisador_lexico(codigo)
    tokens = analisador.tokenizar()

    tokens_por_tipo = {}
    for tipo, valor in tokens:
        if tipo not in tokens_por_tipo:
            tokens_por_tipo[tipo] = []
        tokens_por_tipo[tipo].append(valor)

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

    for tipo, valores in tokens_por_tipo.items():
        resultado_texto.insert(tk.END, f"{tipo}: {len(valores)} token(s)\n")
        resultado_texto.insert(tk.END, f"Tokens encontrados: {valores}\n\n")

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
    janela.configure(bg="#263238")

    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure("TButton", foreground="#ffffff", background="#37474F", font=("Arial", 12), padding=6)
    estilo.map("TButton", background=[("active", "#455A64")])

    text_area = scrolledtext.ScrolledText(janela, font=("Courier New", 12), wrap=tk.WORD, bg="#263238", fg="#808080", insertbackground="#ffffff")
    text_area.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)
    text_area.insert("1.0", "Escreva aqui seu código em Python")
    
    text_area.bind("<FocusIn>", on_focus_in)
    text_area.bind("<FocusOut>", on_focus_out)
    text_area.bind("<KeyRelease>", destacar_sintaxe)

    text_area.tag_configure("keyword", foreground="#FF5722")
    text_area.tag_configure("string", foreground="#4CAF50")
    text_area.tag_configure("comment", foreground="#9E9E9E")

    btn_analisar = ttk.Button(janela, text="Analisar Código", command=analisar_codigo, width=15)
    btn_analisar.place(relx=0.5, rely=0.75, anchor='center')

    janela.mainloop()
