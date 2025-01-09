from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle

model = RandomForestClassifier()
MODEL_FILE = "model.pkl"

def train_model(dataset):
    X = np.array(dataset["board_states"])
    y = np.array(dataset["next_moves"])
    model.fit(X, y)
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