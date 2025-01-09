from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os

model = RandomForestClassifier()
MODEL_FILE = "model.pkl"

def preprocess_board_states(board_states):
    mapping = {"": 0, "X": 1, "O": 2}
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

def predict_move(board):
    if not model:
        load_model()
    return model.predict([board])[0]

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