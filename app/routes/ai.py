from flask import Blueprint, request, jsonify
import numpy as np
from app.services.ai_model import (
    model,
    predict_move,
    save_model,
    load_model,
    preprocess_board_states,
    convert_board_to_numeric,
    update_board_with_move,
    convert_numeric_to_board

)
from app.services.dataset import history_dataset

ai_blueprint = Blueprint("ai", __name__)

@ai_blueprint.route("/move", methods=["POST"])
def ai_move():
    data = request.get_json()
    board = data.get("board")

    if not board or not isinstance(board, list) or len(board) != 3:
        return jsonify({"error": "Invalid board state. Expected a 3x3 matrix."}), 400

    try:
        numeric_board = convert_board_to_numeric(board)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    print(numeric_board) # [[1, 0, 0], [0, 2, 0], [0, 0, 0]]
    next_move = predict_move(numeric_board)
    print(next_move) # [0, 1]
    if next_move is None:
        return jsonify({"error": "Unable to determine a valid move."}), 400

    try:
        numeric_board = update_board_with_move(numeric_board, next_move, player_value=2)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    updated_board = convert_numeric_to_board(numeric_board)

    return jsonify({"next_move": next_move, "updated_board": updated_board})


@ai_blueprint.route("/history", methods=["GET"])
def get_model_history():
    return jsonify(
        {
            "board_states": history_dataset["board_states"],
            "next_moves": history_dataset["next_moves"],
        }
    )


@ai_blueprint.route("/validate", methods=["POST"])
def validate_model():
    global model
    board = request.json.get("board")
    if not board:
        return jsonify({"error": "Board state is required"}), 400
    if not model:
        return jsonify({"error": "Model not trained yet"}), 400
    prediction = model.predict([board])[0]
    return jsonify({"next_move": prediction})


@ai_blueprint.route("/save", methods=["POST"])
def save_trained_model():
    save_model()
    return jsonify({"message": "Model saved successfully"})


@ai_blueprint.route("/load", methods=["POST"])
def load_saved_model():
    load_model()
    return jsonify({"message": "Model loaded successfully"})
