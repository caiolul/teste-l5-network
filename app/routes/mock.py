from flask import Blueprint, jsonify
from app.services.ai_model import train_model, load_existing_dataset
import random
from app.services.dataset import history_dataset
from app.models import Game, Player
from app.services.game_logic import check_winner

mock_blueprint = Blueprint("mock", __name__)

@mock_blueprint.route("/populate", methods=["POST"])
def populate_mock_data():
    total_games = 100
    max_moves = 9
    for _ in range(total_games):
        player1 = Player("player1")
        player2 = Player("player2")

        game = Game(player1, player2)
        moves = []
        for move_number in range(max_moves):
            available_positions = [
                (r, c) for r in range(3) for c in range(3) if game.board[r][c] == ""
            ]
            if not available_positions:
                break

            position = random.choice(available_positions)
            symbol = "X" if game.turn == player1 else "O"

            game.board[position[0]][position[1]] = symbol
            moves.append((game.board, position))

            game.turn = player2 if game.turn == player1 else player1

            winner = check_winner(game.board)
            if winner or move_number == max_moves - 1:
                break

        for state, next_move in moves:
            flat_board = [cell for row in state for cell in row]
            next_move_index = next_move[0] * 3 + next_move[1]
            history_dataset["board_states"].append(flat_board)
            history_dataset["next_moves"].append(next_move_index)

    return jsonify(
        {
            "message": f"{total_games} games simulated and added to the dataset.",
            "total_board_states": len(history_dataset["board_states"]),
        }
    )


@mock_blueprint.route("/train", methods=["POST"])
def train_with_mock_data():
    global history_dataset

    existing_dataset = load_existing_dataset()
    if existing_dataset:
        history_dataset["board_states"].extend(existing_dataset["board_states"])
        history_dataset["next_moves"].extend(existing_dataset["next_moves"])

    if len(history_dataset["board_states"]) < 10:
        return jsonify({"error": "Not enough data to train the model"}), 400

    train_model(history_dataset)
    return jsonify({
        "message": "Model trained successfully",
        "total_training_samples": len(history_dataset["board_states"])
    })