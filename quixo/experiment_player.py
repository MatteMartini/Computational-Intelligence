import random
from game import Game, Move, Player
from copy import deepcopy

#Mix of MontecarloPlayer and clever_player. It makes intelligent moves in a little number of simulations 
#and it chooses the best. Each time it evaluate only a subset of the possible moves, otherwise it would be too slow.
class ExperimentPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:

        return self.experimental_move(game)

    def experimental_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        num_simulations = 5 ## Number of simulations to perform
        num_selected_moves = min(len(game.experimental_available_moves(game.get_current_player())), 10)
        best_move = None
        best_score = float('-inf')

        # Iterate over a randomly selected subset of available moves
        for move in random.sample(game.experimental_available_moves(game.get_current_player()), num_selected_moves):
            total_score = 0
            # Simulate multiple games to evaluate the potential outcomes of the current move
            for _ in range(num_simulations):
                cloned_game = deepcopy(game)
                cloned_game.my_move(move[0], move[1], game.get_current_player())

                # Simulate the game until there is a winner
                while cloned_game.check_winner() == -1:
                    random_move = random.choice(cloned_game.experimental_available_moves(cloned_game.get_current_player()))
                    cloned_game.my_move(random_move[0], random_move[1], cloned_game.get_current_player())

                # Update the total score based on the outcome of the simulation
                if cloned_game.check_winner() == 0:
                    total_score += 1
                elif cloned_game.check_winner() == 1:
                    total_score -= 1
                    
            # Update the best move based on the total score
            if total_score > best_score:
                best_score = total_score
                best_move = move

        return best_move