from flask import Blueprint, request, jsonify
from app.models import Game
from app.services.game_logic import check_winner

game_blueprint = Blueprint("game", __name__)

games = {}

@game_blueprint.route("/start", methods=["POST"])
def start_game():
    data = request.get_json()
    player1_id = data.get("player1_id")
    player2_id = data.get("player2_id")
    if not player1_id or not player2_id:
        return jsonify({"error": "Both player IDs are required"}), 400
    game = Game(player1_id, player2_id)
    games[game.id] = game
    return jsonify({"game_id": game.id, "board": game.board})

@game_blueprint.route("/move", methods=["POST"])
def make_move():
    data = request.get_json()
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    position = data.get("position")
    game = games.get(game_id)

    if not game:
        return jsonify({"error": "Invalid game ID"}), 404
    if game.turn != player_id:
        return jsonify({"error": "Not your turn"}), 400

    row, col = position
    if game.board[row][col] != "":
        return jsonify({"error": "Invalid move"}), 400

    game.board[row][col] = "X" if game.turn == game.player1 else "O"
    game.turn = game.player2 if game.turn == game.player1 else game.player1

    winner = check_winner(game.board)
    if winner:
        return jsonify({"winner": winner, "board": game.board})
    return jsonify({"board": game.board})