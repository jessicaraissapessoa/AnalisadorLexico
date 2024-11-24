# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re  # Biblioteca para trabalhar com expressões regulares (Regex)
import keyword  # Biblioteca para obter palavras reservadas do Python

PALAVRAS_RESERVADAS = keyword.kwlist

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

# Função para agrupar os tokens por categoria
def agrupar_tokens(tokens):
    categorias = {}
    for tipo_token, valor_token, posicao in tokens:
        categorias.setdefault(tipo_token, []).append((valor_token, posicao))
    return categorias

if __name__ == '__main__':
    # Código-fonte de teste do analisador léxico:

    codigo = """
    def soma(a, b):
        # Esta função retorna a soma de dois números
        return a + b

    class Calculadora:
        def __init__(self):
            pass

        def subtrair(self, a, b):
            return a - b

    try:
        resultado = soma(10, 5)
        print(resultado)
    except Exception as e:
        print(e)

    for i in range(5):
        if i % 2 == 0:
            print(f"{i} é par")
        else:
            print(f"{i} é ímpar")

    while True:
        break

    with open('teste.txt', 'w') as f:
        f.write("Exemplo de escrita em arquivo")

    valor_decimal = 3.14
    valor_inteiro = 42
    valor_cientifico = 1e10
    valor_booleano = True
    valor_nulo = None
    lambda_func = lambda x: x * 2
    resultado_lambda = lambda_func(5)
    print(f"Resultado da função lambda: {resultado_lambda}")
    """

    # Inicializa o analisador léxico com o código fornecido
    analisador_lexico = Analisador_lexico(codigo)
    # Executa a tokenização do código
    tokens = analisador_lexico.tokenizar()

    # Agrupa os tokens por categoria e conta a quantidade de cada um
    categorias = agrupar_tokens(tokens)

    # Exibe a quantidade de tokens para cada categoria e seus respectivos tokens
    if not tokens:
        print("Por favor, insira um código válido para análise")
    else:
        primeira_vez = True
        while True:
            if primeira_vez or input("\nGostaria de ver os tokens encontrados para alguma categoria? Digite s para sim ou n para não: ").strip().lower() == 's':
                if not primeira_vez:
                    print("\nCategorias detectadas:")
                for idx, (categoria, valores) in enumerate(categorias.items(), start=1):
                    print(f'{idx}. {categoria}: {len(valores)} token(s)')
                primeira_vez = False
            else:
                print("Até a próxima!")
                break

            try:
                numero_categoria = int(input("Informe o número da categoria para a qual quer ver os tokens listados. EX: 5: "))
                if 1 <= numero_categoria <= len(categorias):
                    categoria_selecionada = list(categorias.keys())[numero_categoria - 1]
                    print(f'\nTokens da categoria "{categoria_selecionada}":')
                    for valor, posicao in categorias[categoria_selecionada]:
                        print(f' - {valor} (Posição: {posicao})')
                else:
                    print("Número de categoria inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número válido.")