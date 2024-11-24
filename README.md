# Analisador Léxico em Python

<br>

## Sobre o Projeto

- Este projeto foi desenvolvido para a disciplina "Teoria da Computação e Compiladores", do curso de Ciência da Computação, e trata de dois analisadores léxicos de código Python desenvolvidos também em Python: um com interface gráfica e outro sem interface. Ambos identificam e categorizam os principais tokens de um código-fonte Python, permitindo a compreensão do processamento de um compilador de linguagem de programação
- É necessário de pyhton e tkinter instalados na máquina, caso execute localmente. Ver instruções em [Instalando Python e Tkinter](#instalando-python-e-tkinter)

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

- O analisador léxico é implementado na classe `Analisador_lexico`, que possui os seguintes métodos:
   - **`__init__(self, codigo)`**: Inicializa o analisador com o código-fonte a ser analisado
   - **`tokenizar(self)`**: Realiza a tokenização do código, identificando e categorizando todos os tokens presentes
- O código de exemplo fornecido na seção principal (`if __name__ == '__main__':`) é utilizado para testar o funcionamento do analisador léxico, verificando diferentes tipos de tokens em um exemplo de código Python

### Como utilizar

1. **Requisitos**: Certifique-se de ter Python instalado em sua máquina. Ver instruções de instalações em [Instalando Python e Tkinter](#instalando-python-e-tkinter)
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

Essa é uma versão do analisador léxico com interface gráfica e que, portanto, tem sua usabilidade através de uma janela interativa, onde o código a ser analisado é inserido diretamente na interface gráfica.

### Estrutura do código

- O analisador léxico é implementado na classe `Analisador_lexico`, que possui os seguintes métodos:
   - **`__init__(self, codigo)`**: Inicializa o analisador com o código-fonte a ser analisado
   - **`tokenizar(self)`**: Realiza a tokenização do código, identificando e categorizando todos os tokens presentes
- A interface gráfica foi desenvolvida utilizando a biblioteca `tkinter`, permitindo ao usuário inserir o código diretamente em uma área de texto e visualizar os resultados (versão resumida e versão detalhada) em uma janela separada.
- Além dos métodos da classe `Analisador_lexico`, o arquivo contém funções específicas de interação com a interface gráfica, como destacar a sintaxe, limpar o editor, mostrar mensagem de erro em caso de envio sem código, alternar entre a visão resumida e detalhada dos resultados da análise, navegar entre as categorias (com a lista de seus respectivos tokens) por meio de sumário interativo na visão detalhada

### Como utilizar

1. **Requisitos**: Certifique-se de ter Python instalado em sua máquina. Ver instruções de instalações em [Instalando Python e Tkinter](#instalando-python-e-tkinter)
2. **Execução**:
   - Navegue até o diretório onde o arquivo `analisador_lexico_com_interface.py` está localizado
   - Inicie o terminal nesse diretório
   - No terminal, execute o arquivo usando o comando:
     ```
     python analisador_lexico_com_interface.py
     ```
3. **Uso da Interface**:
   - Uma janela será aberta, permitindo que você insira e edite o código Python para análise na área de texto. Você pode usar o botão "Limpar editor" para apagar todo o código que inseriu
     ![image](https://github.com/user-attachments/assets/c2300112-9f2c-44d2-865f-4a080e14e695)
   - Você pode testar com esse código para demonstração/teste da capacidade do analisador de reconhecer diferentes tipos de tokens:
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
   - Clique no botão "Analisar código" para iniciar a análise.
4. **Resultado**:
   - Inicialmente, uma visão resumida das categorias de tokens e suas respectivas quantidades será exibida. Enviando o código sugerido em tópico 3, a exibição resumida dos resultados é:
     ![image](https://github.com/user-attachments/assets/2735abcd-2de2-40af-8f61-60c3a9a8da16)
   - Você pode clicar no botão "Ver detalhes" para expandir e visualizar todos os tokens identificados em cada categoria. Seguindo com a sugestão feita no tópico 4, a exibição detalhada dos resultados é:
     ![image](https://github.com/user-attachments/assets/27877a2b-b871-4144-b027-e555c693953d)
   - Você pode ter uma navegação rápida entre a listagem de tokens da visão detalhada ao clicar na categoria de interesse no menu da lateral
   - Você pode alternar livremente entre a visão resumida e a visão detalhada dos resultados clicando no botão na parte inferior da tela de resultados ("Ver detalhes"/"Ver resumo")

### Vídeo demonstrativo do uso

https://github.com/user-attachments/assets/cc04fa44-c0fe-41dc-8a49-16dfe3b62080

<br>

## Instalando Python e Tkinter

Para o analisador léxico sem interface, você pode ajustar as instruções de instalação para instalar apenas `python`, pois o `tkinter` é pré-requisito apenas para a versão do analisador léxico com interface. Siga as instruções de acordo com o seu sistema operacional:

<br>

### Linux

Em distribuições baseadas no Debian, como Ubuntu:

```bash
# Atualizar os repositórios
sudo apt update

# Instalar o Python (se não estiver instalado)
sudo apt install python3 python3-pip -y

# Instalar o tkinter
sudo apt install python3-tk -y
```

Para outras distribuições, troque o `apt` pelo gerenciador de pacotes correspondente (por exemplo, `dnf` no Fedora ou `yum` no CentOS).

<br>

### Windows

No Windows, o Python geralmente vem com o `tkinter` incluído. Caso não esteja instalado, siga estas etapas:

1. Baixe o instalador do Python no site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Durante a instalação, certifique-se de marcar a opção **"Add Python to PATH"**.
3. Após a instalação, verifique se o `tkinter` está presente:
   ```bash
   # Verificar instalação do tkinter no Windows
   python -m tkinter
   ```
Caso o `tkinter` não esteja instalado, reinstale o Python, garantindo que o módulo `tkinter` seja incluído na instalação.

<br>

### MacOS

O macOS já vem com Python e `tkinter` instalados. Para garantir que você tenha a versão mais recente:

```bash
# Atualizar o Homebrew (caso esteja usando)
brew update

# Instalar o Python mais recente
brew install python

# O tkinter vem junto com o Python no macOS.
# Caso precise garantir:
brew install python-tk
```

Verifique se o `tkinter` está funcionando:

```bash
python3 -m tkinter
```
