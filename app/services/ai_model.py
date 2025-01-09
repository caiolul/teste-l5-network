from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os

model = RandomForestClassifier()
MODEL_FILE = "model.pkl"
mapping = {"": 0, "X": 1, "O": 2}


def convert_board_to_numeric(board):
    try:
        return [[mapping[cell] for cell in row] for row in board]
    except KeyError:
        raise ValueError("Invalid board symbols. Only '', 'X', and 'O' are allowed.")


def convert_numeric_to_board(numeric_board):
    reverse_mapping = {0: "", 1: "X", 2: "O"}
    return [[reverse_mapping[cell] for cell in row] for row in numeric_board]


def update_board_with_move(numeric_board, move, player_value):
    row, col = move
    if numeric_board[row][col] != 0:
        raise ValueError("Invalid move. Cell is already occupied.")
    numeric_board[row][col] = player_value
    return numeric_board


def preprocess_board_states(board_states):
    return [list(map(lambda x: mapping[x], board)) for board in board_states]


def load_existing_dataset():
    if not os.path.exists(MODEL_FILE):
        print("Model file not found")
        return None
    try:
        with open(MODEL_FILE, "rb") as file:
            saved_model = pickle.load(file)
            print(saved_model)
        if hasattr(saved_model, "X_") and hasattr(saved_model, "y_"):
            return {
                "board_states": saved_model.X_,
                "next_moves": saved_model.y_,
            }
    except Exception as e:
        print(f"Failed to load dataset from model file: {e}")
    return None


def train_model(dataset):
    global model
    x = np.array(preprocess_board_states(dataset["board_states"]))
    y = np.array(dataset["next_moves"])
    model.fit(x, y)
    save_model()

def is_valid_move(board, row, col):
    return board[row][col] == 0

def find_next_valid_move(board):
    for row in range(3):
        for col in range(3):
            if is_valid_move(board, row, col):
                return [row, col]
    return None  # No valid moves left
def predict_move(board):
    if not model:
        load_model()
    board_array = np.array(board).reshape(1, -1)
    predicted_index = model.predict(board_array)[0]
    row = predicted_index // 3
    col = predicted_index % 3
    
    if is_valid_move(board, row, col):
        return [row, col]
    else:
        next_move = find_next_valid_move(board)
        if next_move:
            return next_move
        else:
            raise ValueError("Não há movimentos válidos restantes no tabuleiro")


def save_model():
    with open(MODEL_FILE, "wb") as file:
        pickle.dump(model, file)


def load_model():
    global model
    try:
        with open(MODEL_FILE, "rb") as file:
            model = pickle.load(file)
    except FileNotFoundError:
        model = RandomForestClassifier()
