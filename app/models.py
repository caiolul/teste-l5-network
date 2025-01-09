import uuid

class Player:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.wins = 0
        self.losses = 0
        self.draws = 0

class Game:
    def __init__(self, player1, player2):
        self.id = str(uuid.uuid4())
        self.board = [[""] * 3 for _ in range(3)]
        self.player1 = player1
        self.player2 = player2
        self.turn = player1.id