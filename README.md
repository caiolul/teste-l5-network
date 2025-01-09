# Projeto: Tic Tac Toe com Flask e Machine Learning

## Descrição
Este é um projeto de implementação de um jogo da velha (Tic Tac Toe) utilizando Flask para criação de uma API e integração com Machine Learning. O objetivo é permitir:
- Registro de jogadores.
- Início e gerenciamento de jogos.
- Treinamento de um modelo de Machine Learning para prever a melhor jogada com base em histórico de partidas.
- Mock de dados para simulação e treinamento.

---

## Estrutura do Projeto

### Diretórios e Arquivos

- **main.py**: Ponto de entrada do projeto.
- **app/**: Contém a lógica da aplicação.
  - **__init__.py**: Configuração do Flask e registro de blueprints.
  - **models.py**: Modelos de dados (Player e Game).
  - **routes/**: Contém as rotas do sistema:
    - **player.py**: Registro e gerenciamento de jogadores.
    - **game.py**: Lógica do jogo da velha.
    - **ai.py**: Interação com o modelo de Machine Learning.
    - **mock.py**: Mock de dados e treinamento do modelo.
  - **services/**: Serviços auxiliares, como lógica do jogo e manipulação do modelo de ML.

---

## Como Rodar o Projeto

### 1. Instalação do Ambiente

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd tic_tac_toe
   ```
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Caso tenha o Poetry instalado, execute o comando abaixo para instalar as dependências:

   ```bash
   poetry install
   ```
   
### 2. Inicialização do Servidor

Execute o servidor Flask:
```bash
python main.py
```
A aplicação estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Rotas da API

### 1. Registro de Jogadores
- **POST /api/player/register**
  - **Entrada**: `{ "name": "Jogador1" }`
  - **Saída**: `{ "player_id": "<UUID>" }`

### 2. Início de Jogo
- **POST /api/game/start**
  - **Entrada**: `{ "player1_id": "<UUID>", "player2_id": "<UUID>" }`
  - **Saída**: `{ "game_id": "<UUID>", "board": [["", "", ""], ["", "", ""], ["", "", ""]] }`

### 3. Realizar Jogada
- **POST /api/game/move**
  - **Entrada**: `{ "game_id": "<UUID>", "player_id": "<UUID>", "position": [0, 1] }`
  - **Saída**:
    - Em caso de sucesso: `{ "board": [["X", "", ""], ["", "", ""], ["", "", ""]] }`
    - Em caso de fim de jogo: `{ "winner": "<PLAYER_ID>", "board": [["X", "", ""], ["", "", ""], ["", "", ""]] }`

### 4. Mock de Dados
- **POST /api/mock/populate**
  - Gera 100 jogos simulados e adiciona ao dataset.
  - **Saída**: `{ "message": "Mock data generated", "total_games": 100 }`

### 5. Treinar o Modelo
- **POST /api/mock/train**
  - Treina o modelo utilizando o dataset gerado (mock ou carregado de arquivo).
  - **Saída**: `{ "message": "Model trained successfully", "total_training_samples": 100 }`

### 6. Movimentos do AI
- **GET /api/ai/move?board=<BOARD>**
  - Retorna a próxima jogada sugerida pelo modelo para um estado atual do tabuleiro.
  - **Entrada**: `board` como string JSON, e.g., `[["X", "", ""], ["", "O", ""], ["", "", ""]]`.
  - **Saída**: `{ "next_move": [0, 1], "board": [["X", "X", ""], ["", "O", ""], ["", "", ""]] }`

### 7. Salvar e Carregar Modelo
- **POST /api/ai/save**
  - Salva o modelo treinado em disco (`model.pkl`).
  - **Saída**: `{ "message": "Model saved successfully" }`

- **POST /api/ai/load**
  - Carrega o modelo salvo de disco.
  - **Saída**: `{ "message": "Model loaded successfully" }`

---

## Como Treinar o Modelo

1. Gere dados mock:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/mock/populate
   ```

2. Treine o modelo com os dados:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/mock/train
   ```

3. Opcionalmente, salve o modelo:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/ai/save
   ```

4. Para carregar o modelo em outra execução:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/ai/load
   ```

---

## Observações

- Certifique-se de que o arquivo `model.pkl` está no diretório correto para carregar o modelo.
- Os dados podem ser expandidos para incluir mais variações de jogos e melhorar a performance do modelo.
- Personalize o sistema para incluir mais estatísticas ou regras de jogo.

---

## Tecnologias Utilizadas

- **Python**: Lógica principal.
- **Flask**: Framework para criação de API.
- **scikit-learn**: Biblioteca de Machine Learning para treinamento do modelo.
- **pickle**: Serialização do modelo para armazenamento.

