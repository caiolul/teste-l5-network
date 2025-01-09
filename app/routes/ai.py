from flask import Blueprint, request, jsonify
from app.services.ai_model import model, predict_move, save_model, load_model
from app.services.dataset import history_dataset

ai_blueprint = Blueprint("ai", __name__)


@ai_blueprint.route("/move", methods=["GET"])
def ai_move():
    board = request.args.get("board")
    if not board:
        return jsonify({"error": "Board state is required"}), 400
    next_move = predict_move(board)
    return jsonify({"next_move": next_move})

@ai_blueprint.route("/history", methods=["GET"])
def get_model_history():
    return jsonify({
        "board_states": history_dataset["board_states"],
        "next_moves": history_dataset["next_moves"]
    })

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