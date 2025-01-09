from flask import Blueprint, request, jsonify
from app.models import Player

player_blueprint = Blueprint("player", __name__)

players = {}

@player_blueprint.route("/register", methods=["POST"])
def register_player():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    player = Player(name)
    players[player.id] = player
    return jsonify({"player_id": player.id})