from flask import Blueprint, jsonify
from app.services.ai_model import train_model
import random
from app.services.dataset import history_dataset

mock_blueprint = Blueprint("mock", __name__)

@mock_blueprint.route("/populate", methods=["POST"])
def populate_mock_data():
    for _ in range(100):
        board = [""] * 9
        next_move = random.randint(0, 8)
        while board[next_move] != "":
            next_move = random.randint(0, 8)
        board[next_move] = "X"
        history_dataset["board_states"].append(board)
        history_dataset["next_moves"].append(next_move)
    return jsonify({"message": "Mock data generated", "total_games": len(history_dataset["board_states"])})

@mock_blueprint.route("/train", methods=["POST"])
def train_with_mock_data():
    if len(history_dataset["board_states"]) < 10:
        return jsonify({"error": "Not enough data to train the model"}), 400
    train_model(history_dataset)
    return jsonify({"message": "Model trained successfully"})