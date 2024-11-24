# Analisador Léxico em Python

<br>

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina "Teoria da Computação e Compiladores", do curso de Ciência da Computação, e trata de dois analisadores léxicos de código Python desenvolvidos também em Python: um com interface gráfica e outro sem interface. Ambos identificam e categorizam os principais tokens de um código-fonte Python, permitindo a compreensão do processamento de um compilador de linguagem de programação.

<br>

## Estrutura do Repositório

- `analisador_lexico_sem_interface.py`: Arquivo contendo a implementação do analisador léxico sem interface gráfica
- `analisador_lexico_com_interface.py`: Arquivo contendo a implementação do analisador léxico com interface gráfica
- `README.md`: Este arquivo, contendo a descrição do projeto e instruções de uso

<br>

## Categorias de tokens

O analisador léxico faz uso da biblioteca `re` (expressões regulares) para identificar tokens específicos dentro do código-fonte. Os tokens são categorizados nos seguintes tipos (padrões):

- **Palavras Reservadas**: Identificação de palavras reservadas da linguagem Python, como `def`, `class`, `return`, entre outras
- **Identificador - Classe**: Nomes de classes definidos pelo usuário, identificados após a palavra-chave `class`
- **Identificador - Função**: Nomes de funções definidos pelo usuário, identificados após a palavra-chave `def`
- **Identificador - Chamada Função**: Identificadores que representam chamadas de funções
- **Identificador - Variável**: Identificadores que representam variáveis, seguidos por um sinal de atribuição
- **Identificador - Geral**: Identificadores que não se enquadram nas categorias anteriores (nomes de variáveis, funções, etc.)
- **Strings**: Valores de texto entre aspas simples ou duplas
- **Valor Decimal**: Valores numéricos de ponto flutuante (e.g., `3.14`)
- **Valor Inteiro**: Valores numéricos inteiros (e.g., `42`)
- **Valor Booleano**: Valores lógicos `True` e `False`
- **Valor Nulo**: Valor especial `None` que representa ausência de valor
- **Operadores**: Operadores matemáticos e lógicos, como `+`, `-`, `*`, `/`, `=`, `==`, etc
- **Delimitadores**: Parênteses `()`, chaves `{}`, colchetes `[]`, vírgulas `,`, pontos `.` e dois pontos `:`
- **Comentários**: Comentários iniciados pelo caractere `#`
- **Notação Científica**: Números em notação científica, como `1e10` ou `2.5E-3`
- **Espaços em Branco**: São identificados e contabilizados, embora sejam ignorados no processamento

<br>

## Analisador léxico sem interface (analisador\_lexico\_sem\_interface.py)

Essa é uma versão do analisador léxico sem interface e que, portanto, tem sua usabilidade pelo editor de código (para informar código da análise) e terminal para executar o analisador léxico

### Estrutura do Código

O analisador léxico é implementado na classe `Analisador_lexico`, que possui os seguintes métodos:

- **`__init__(self, codigo)`**: Inicializa o analisador com o código-fonte a ser analisado
- **`tokenizar(self)`**: Realiza a tokenização do código, identificando e categorizando todos os tokens presentes

O código de exemplo fornecido na seção principal (`if __name__ == '__main__':`) é utilizado para testar o funcionamento do analisador léxico, verificando diferentes tipos de tokens em um exemplo de código Python

### Como utilizar

1. **Requisitos**: Certifique-se de ter Python instalado em sua máquina
2. Abra o arquivo em um editor de código
3. Insira o código que deseja analisar como valor da variável `codigo` (linha 70). O arquivo do analisador já vem, por padrão, com esse código (valor da variável `codigo`) para análise:
   ```python
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
   ```
5. Este valor de `codigo` é utilizado como demonstração/teste da capacidade do analisador de reconhecer diferentes tipos de tokens, como palavras reservadas, identificadores, operadores, etc.
6. **Execução**:
   - Navegue até o diretório onde o arquivo `analisador_lexico_sem_interface.py` está localizado
   - Inicie o terminal nesse diretório
   - No terminal, execute o arquivo usando o comando:
     ```
     python analisador_lexico_sem_interface.py
     ```
7. **Resultado**: O analisador exibirá inicialmente a versão resumida dos resultados (categorias + quantidade de tokens). Para o código que já vem como valor em `codigo` (etapa 3), é exibido o seguinte resultado:
   ```
   1. ESPAÇO: 250 token(s)
   2. PALAVRAS RESERVADAS: 19 token(s)
   3. IDENTIFICADOR - FUNÇÃO: 3 token(s)
   4. DELIMITADOR: 44 token(s)
   5. IDENTIFICADOR - GERAL: 23 token(s)
   6. COMENTÁRIO: 1 token(s)
   7. OPERADOR: 13 token(s)
   8. IDENTIFICADOR - CLASSE: 1 token(s)
   9. IDENTIFICADOR - VARIÁVEL: 8 token(s)
   10. IDENTIFICADOR - CHAMADA FUNÇÃO: 10 token(s)
   11. VALOR INTEIRO: 8 token(s)
   12. STRING: 6 token(s)
   13. VALOR BOOLEANO: 2 token(s)
   14. VALOR DECIMAL: 1 token(s)
   15. NOTAÇÃO CIENTÍFICA: 1 token(s)
   16. VALOR NULO: 1 token(s)
   ```      
8. O usuário pode selecionar categoria, informando o número dela na lista, para ter uma visão detalhdada dessa (listagem dos tokens identificados). Seguindo com o resultado do tópico 7, por exemplo, ao informar `2` para selecionar a categoria `PALAVRAS RESERVADAS`, é exibido o seguinte resultado:
   ```
   Tokens da categoria "PALAVRAS RESERVADAS":
    - def (Posição: 5)
    - return (Posição: 82)
    - class (Posição: 100)
    - def (Posição: 127)
    - pass (Posição: 159)
    - def (Posição: 173)
    - return (Posição: 211)
    - try (Posição: 229)
    - except (Posição: 295)
    - as (Posição: 312)
    - for (Posição: 340)
    - in (Posição: 346)
    - if (Posição: 367)
    - else (Posição: 422)
    - while (Posição: 467)
    - break (Posição: 487)
    - with (Posição: 498)
    - as (Posição: 526)
    - lambda (Posição: 724)
   ```
10. Você poderá permanecer no loop, selecionando outras categorias para ver detalhes, até que decida responder que não deseja ver detalhes de nenhuma categoria ou até encerrar a execução

### Vídeo demonstrativo do uso

https://github.com/user-attachments/assets/987e5c7a-0504-44b4-9892-33a4b7c2250c

<br>

## Analisador léxico com interface (analisador\_lexico\_com\_interface.py)

## Estrutura do Código

O analisador léxico com interface é implementado na classe `Analisador_lexico`, juntamente com uma interface gráfica desenvolvida utilizando a biblioteca `tkinter`. A interface permite ao usuário digitar ou colar o código a ser analisado e ver o resultado diretamente na aplicação, tanto na visão resumida quanto na visão detalhada.

Além dos métodos da classe `Analisador_lexico`, o arquivo contém funções específicas para interagir com a interface gráfica, como destacar a sintaxe, limpar o editor, e mostrar mensagens de erro.

## Como Executar

1. **Requisitos**: Certifique-se de ter Python e a biblioteca `tkinter` instalados em sua máquina.
2. **Execução**:
   - Navegue até o diretório onde o arquivo `analisador_lexico_com_interface.py` está localizado.
   - Execute o arquivo usando o comando:
     ```
     python analisador_lexico_com_interface.py
     ```
3. **Resultado**: Uma janela será aberta, permitindo que você insira o código Python para análise. Após clicar em "Analisar código", a interface exibirá a quantidade de tokens de cada categoria encontrada e permitirá que você veja os detalhes dos tokens identificados por categoria.

## Exemplo de Uso

Após iniciar o analisador léxico com interface, você poderá colar o seguinte exemplo de código na área de texto e clicar no botão "Analisar código":

```python
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
```

A interface exibirá inicialmente uma visão resumida com as categorias de tokens e suas respectivas quantidades. Você poderá clicar no botão "Ver detalhes" para expandir e visualizar todos os tokens identificados em cada categoria.

Este exemplo é utilizado para demonstrar a capacidade do analisador de reconhecer diferentes tipos de tokens, como palavras reservadas, identificadores, operadores, etc. Para testar/aplicar em outro código Python, basta inserir o código na área de texto do analisador léxico com interface.

