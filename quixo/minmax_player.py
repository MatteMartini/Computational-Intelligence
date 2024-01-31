from copy import deepcopy
from game import Game, Move, Player
import numpy as np

class MinMaxPlayer(Player):
    def __init__(self, player: int = 0) -> None:
        super().__init__()
        player = player % 2
        self.player = player

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        temp = deepcopy(game)
         #get the best move to choose using Minimax
        move = self.minmax(temp)
        pos = (move[0], move[1])
        slide = move[2]
        return pos, slide

    #The function also performs alpha-beta pruning to avoid exploring branches that would not influence the best choice.
    #Alpha represents the best-known value for the MAX player. Beta represents the best-known value for the MIN player.
    #Pruning occurs when the MAX (or MIN) player finds a move that is already better than what the opponent (MIN or MAX) could achieve.
    def minmax(self, game: 'Game', depth: int = 1, alpha = -np.inf, beta = np.inf) -> tuple[tuple[int, int], Move]:
        player_id = game.current_player_idx
        possible_moves = game.available_moves(player_id)
        max_pruning = 2 #more is slow and don't give big improvements. Playing for Max

        # Initialize the best scores for the current move (both MAX player and MIN player)
        best_score_info = [-1, -1, -1, -np.inf] if player_id == self.player else [-1, -1, -1, +np.inf]

        # If there are no available moves or the maximum depth level has been reached.
        if game.check_winner() != -1 or depth > max_pruning or not possible_moves:
            return [-1, -1, -1, self.calculate_score(game)]

        for move in possible_moves:
            position, slide = move
            # Save the board state before making the move and going into recursion
            temp_board_state = deepcopy(game._board[position[1], :]) if slide in {Move.LEFT, Move.RIGHT} else deepcopy(game._board[:, position[0]])

            # Execute the move and recursively calculate the score.  
            game.my_move(position, slide, player_id)
            reward = self.minmax(game, depth + 1, alpha, beta)

            # restore the value
            if slide == Move.LEFT or slide == Move.RIGHT:
                game._board[position[1]] = temp_board_state
            else:
                game._board[:, position[0]] = temp_board_state

            reward[0] = position[0]  # x
            reward[1] = position[1]  # y
            reward[2] = slide

            #MinMaxPlayer plays for Max
            if player_id == self.player:  
                if reward[3] > best_score_info[3]:
                    best_score_info = reward  # Update for Max player
                    alpha = reward[3]
            else:
                if reward[3] < best_score_info[3]:
                    best_score_info = reward  # Update for Min player
                    beta = reward[3]

            if alpha >= beta:  # without the = more efficient but slower. You prune more the tree
                break

        return best_score_info

    def calculate_score(self, game: 'Game') -> int:
        winner = game.check_winner()
        if winner == self.player:
            return 1  # win
        elif winner == -1:
            return 0  # draw
        else:
            return -1  # lose
