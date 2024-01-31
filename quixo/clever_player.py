import random
from game import Game, Move, Player

class CleverPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        #Choose a move randomly from the available moves that do not make you loss, 
        #favoring those that allow you to claim a square that is still without a symbol. 
        #If there is a move that leads to your victory, makes that move immediately."
        return random.choice(game.clever_available_moves(game.get_current_player()))