from flask import Flask
from app.routes.game import game_blueprint
from app.routes.player import player_blueprint
from app.routes.ai import ai_blueprint
from app.routes.mock import mock_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(game_blueprint, url_prefix="/api/game")
    app.register_blueprint(player_blueprint, url_prefix="/api/player")
    app.register_blueprint(ai_blueprint, url_prefix="/api/ai")
    app.register_blueprint(mock_blueprint, url_prefix="/api/mock")
    return app