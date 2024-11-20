# -*- coding: utf-8 -*-
# Jéssica Raissa Pessoa Barros - 1362217774

import re  # Biblioteca para trabalhar com expressões regulares (Regex)

# Array de palavras reservadas
PALAVRAS_RESERVADAS = [
  'def', 'class', 'return', 'if', 'else', 'elif', 'while', 'for', 'in',
  'import', 'from', 'as', 'print', 'pass', 'break', 'continue', 'try',
  'except', 'finally', 'raise', 'with', 'assert', 'lambda'
]

# Definição dos padrões de tokens que o analisador léxico irá reconhecer
TOKEN_REGEX = [
  (r'\bTrue\b|\bFalse\b', 'VALOR BOOLEANO'), # Valores do tipo booleano (True ou False)
  (r'\bNone\b', 'VALOR NULO'), # Valor nulo (None)
  (rf'\b({"|".join(PALAVRAS_RESERVADAS)})\b', 'PALAVRAS RESERVADAS'), # Palavras reservadas pela linguagem (Python)
  (r'[a-zA-Z_][a-zA-Z_0-9]*', 'IDENTIFICADOR'), # Identificador: nomes de variáveis, funções, classes, etc.
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
    categorias = {}  # Dicionário para armazenar a quantidade de tokens por categoria
    tokens_por_categoria = {}  # Dicionário para armazenar os tokens específicos de cada categoria
    for tipo_token, valor_token in tokens:
        if tipo_token in categorias:
            categorias[tipo_token] += 1  # Incrementa a contagem de tokens da categoria existente
            tokens_por_categoria[tipo_token].append(valor_token)  # Adiciona o token à lista da categoria existente
        else:
            categorias[tipo_token] = 1  # Inicializa a contagem de tokens da nova categoria
            tokens_por_categoria[tipo_token] = [valor_token]  # Inicializa a lista de tokens da nova categoria

    # Exibe a quantidade de tokens para cada categoria e seus respectivos tokens
    if not tokens:
        print("Por favor, insira um código válido para análise")
    else:
        for categoria, quantidade in categorias.items():
            print(f'{categoria}: {quantidade} token(s)')
            print(f'Tokens encontrados: {tokens_por_categoria[categoria]}\n')
