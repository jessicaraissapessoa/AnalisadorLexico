# Analisador Léxico em Python

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina "Teoria da Computação e Compiladores", do curso de Ciência da Computação, e trata de um analisador léxico de código Python desenvolvido também em Python: ele identifica e categoriza os principais tokens de um código-fonte Python, permitindo a compreensão do processamento de um compilador de linguagem de programação.

## Funcionamento

O analisador léxico faz uso da biblioteca `re` (expressões regulares) para identificar tokens específicos dentro do código-fonte. Os tokens são categorizados nos seguintes tipos (padrões):

- **Palavras Reservadas**: Identificação de palavras reservadas da linguagem Python, como `def`, `class`, `return`, entre outras.
- **Identificadores**: Nomes de variáveis, funções, classes, etc.
- **Strings**: Valores de texto entre aspas simples ou duplas.
- **Valor Decimal**: Valores numéricos de ponto flutuante (e.g., `3.14`).
- **Valor Inteiro**: Valores numéricos inteiros (e.g., `42`).
- **Valor Booleano**: Valores lógicos `True` e `False`.
- **Valor Nulo**: Valor especial `None` que representa ausência de valor.
- **Operadores**: Operadores matemáticos e lógicos, como `+`, `-`, `*`, `/`, `=`, `==`, etc.
- **Delimitadores**: Parênteses `()`, chaves `{}`, colchetes `[]`, vírgulas `,`, pontos `.` e dois pontos `:`.
- **Comentários**: Comentários iniciados pelo caractere `#`.
- **Notação Científica**: Números em notação científica, como `1e10` ou `2.5E-3`.
- **Espaços em Branco**: São ignorados durante a análise léxica.
- **Caractere Não Reconhecido**: Qualquer outro caractere que não se enquadre nas categorias anteriores.

## Estrutura do Código

O analisador léxico é implementado na classe `Analisador_lexico`, que possui os seguintes métodos:

- **`__init__(self, codigo)`**: Inicializa o analisador com o código-fonte a ser analisado.
- **`tokenizar(self)`**: Realiza a tokenização do código, identificando e categorizando todos os tokens presentes.

O código de exemplo fornecido na seção principal (`if __name__ == '__main__':`) é utilizado para testar o funcionamento do analisador léxico, verificando diferentes tipos de tokens em um exemplo de código Python.

## Como Executar

1. **Requisitos**: Certifique-se de ter Python 3 instalado em sua máquina.
2. **Execução**:
   - Navegue até o diretório onde o arquivo `analisador_lexico.py` está localizado.
   - Execute o arquivo usando o comando:
     ```
     python analisador_lexico.py
     ```
3. **Resultado**: O analisador exibirá a quantidade de tokens de cada categoria encontrada e listará os tokens identificados.

## Exemplo de Uso

O analisador léxico foi testado com o seguinte código:

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

Este código é utilizado para demonstrar a capacidade do analisador de reconhecer diferentes tipos de tokens, como palavras reservadas, identificadores, operadores, etc.

## Estrutura do Repositório

- `analisador_lexico.py`: Arquivo principal contendo a implementação do analisador léxico.
- `README.md`: Este arquivo, contendo a descrição do projeto e instruções de uso.
