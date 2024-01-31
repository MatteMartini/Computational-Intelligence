import random
from game import Game, Move, Player
from copy import deepcopy, copy

#the player uses Monte Carlo simulation technique to make decisions about its moves
class MonteCarloPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        
        return self.monte_carlo_move(game)

    def monte_carlo_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        num_simulations = 500  # Number of Monte Carlo simulations to perform
        num_selected_moves = min(len(game.available_moves(game.get_current_player())), 40)
        best_move = None
        best_score = float('-inf')

        # Iterate over a randomly selected subset of available moves
        for move in random.sample(game.available_moves(game.get_current_player()), num_selected_moves):
            total_score = 0
            # Simulate multiple games to evaluate the potential outcomes of the current move
            for _ in range(num_simulations):
                cloned_game = copy(game)
                cloned_game.my_move(move[0], move[1], game.get_current_player())

                # Simulate the game until there is a winner
                while cloned_game.check_winner() == -1:
                    # Consider only a subset of randomly available moves in each simulation
                    random_move = random.choice(cloned_game.available_moves(cloned_game.get_current_player()))
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

