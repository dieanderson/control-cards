# Control-Cards

Control-Cards é uma aplicação em Python que gera relatórios categorizados de faturas de cartões de crédito. Bastando apenas adicionar o arquivo `.csv` da fatura do cartão e configurar o agrupamento dos lançamentos com as categorias desejadas, a ferramenta gera um relatório em PDF contendo gráficos e um resumo detalhado dos seus gastos.

## 📋 Funcionalidades

- **Interface:** Interface amigável multiplataforma(Windows, Linux e MacOs).
- **Importação Fácil:** Basta adicionar o arquivo `.csv` da sua fatura de cartão de crédito.
- **Configuração de Categorias:** Personalize as categorias no editor de categorias ou diretamente no arquivo JSON, vinculando a descrição dos lançamentos às categorias desejadas.
- **Relatórios Detalhados:** Gere um relatório PDF categorizado com gráfico e resumos de gastos.
- **Compatibilidade:** Atualmente, suporta faturas `.csv` dos bancos Bradesco, Nubank e XP(Fácil integração com outros bancos).

## 🚀 Começando

Estas instruções fornecerão uma cópia do projeto em funcionamento na sua máquina local para propósitos de desenvolvimento e teste.

### 🔧 Pré-requisitos

- **Python 3.x**: Certifique-se de ter o Python 3 instalado na sua máquina. Você pode baixar a versão mais recente [aqui](https://www.python.org/downloads/).

### 📦 Instalação

1. **Clone o Repositório**

  Abra o terminal e clone o repositório do GitHub:

  ```bash
  git clone https://github.com/dieanderson/control-cards.git
  ```

2. **Navegue até o Diretório do Projeto**
  
  ```bash
  cd control-cards
  ```

3. **Crie e Ative um Ambiente Virtual (Opcional, mas Recomendado)**
  
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  ```

4. **Instale as Dependências**
  
  ```bash
  pip install -r requirements.txt
  ```

5. **Executando o projeto**
  
  ```bash
  python3 main.py
  ```

## 🛠 Uso

1. **Adicionar o Arquivo `.csv` da Fatura**
  
  Coloque o arquivo `.csv` da sua fatura na pasta raiz do projeto ou em um diretório de sua preferência.

2. **Configurar as Categorias**

  Edite os arquivos de categorias localizados na pasta `src/data`:

  - `categorias.json`: Para faturas padrão.
  - `categorias_xp.json`: Para faturas da XP.

  Vincule a descrição dos lançamentos às categorias desejadas conforme a estrutura JSON fornecida.

3. **Executar a Aplicação**

  Execute o script principal para gerar o relatório PDF:
  
  ```bash
  python main.py
  ```

### 📂 Adicionar Novos Bancos

  Atualmente a aplicação suporta faturas do Bradesco, Nubank e XP. Para adicionar suporte a novos bancos é só seguir os passos:

  1. **Criar um Módulo de Modelo**:
    Adicione um novo arquivo Python na pasta src/models/ com a lógica para processar o .csv do novo banco(verificar padrão já implementado nos arquivos existentes).
  
  2. **Atualizar o `banks.py`**:
    Adicione o novo banco no arquivo `JSON` seguindo o padrão.
  
  3. **Atualizar o `process.py`**:
    Importar o novo arquivo de modelo e adicionar uma nova checagem no `case` utilizando o código do banco.


### 🗂 Estrutura do Projeto

  ```
  control-cards/
  │
  ├── src/
  │   ├── process.py
  │   ├── functions.py
  │   ├── pdf.py
  │   └── models/
  │       ├── bradesco.py
  │       ├── nubank.py
  │       └── xp.py
  ├── img/
  │   ├── bradesco.png
  │   ├── nubank.png
  │   └── xp.png
  ├── data/
  │   └── banks.py
  ├── view/
  │   ├── home.py
  │   └── category_editor.py
  ├── reports/
  │   └── <relatórios são gravados nessa pasta por default>
  ├── main.py
  ├── requirements.txt
  ├── .gitignore 
  ├── LICENSE       
  └── README.md
  ```

## 📞 Contato

Diêgo Anderson - dieanderson@gmail.com

[Link do Projeto](https://github.com/dieanderson/control-cards)
