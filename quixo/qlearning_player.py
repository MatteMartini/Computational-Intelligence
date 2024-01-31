from game import Game, Move, Player
from copy import deepcopy
import numpy as np
import struct

class QLearningPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.q_table = {}
        self.load_q_table("Q_table_1.txt")

    def get_q_table(self):
        return self.q_table

    def load_q_table(self, filename):
        # Load Q-table from a file
        with open(filename, 'r') as file:
            for line in file:
                state, action, value = line.split(" ")
                self.q_table[(state, action)] = float(value)

    def get_q_value(self, state, action):
        # Get Q-value from the Q-table, initializing if not present
        if (state, action) not in self.q_table:
            self.q_table[(state, action)] = 0
        return self.q_table[(state, action)]

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        current_player = game.get_current_player()
        available_actions = game.available_moves(current_player)
        current_state = self.compress_matrix(game.get_board())
        compressed_actions = [self.compress_move(action) for action in available_actions]

        q_values = np.array([self.get_q_value(current_state, action) for action in compressed_actions])
        max_q_value = np.max(q_values)

        # Choose a move based on Q-values and exploration strategy
        chosen_move = compressed_actions[np.random.choice(np.where(q_values == max_q_value)[0])]
        return self.decode_compressed_move(chosen_move)
    
    def compress_matrix(self, matrix):
        # Flatten and compress the matrix into a string
        flat_matrix = matrix.flatten()
        compressed_data = struct.pack(f">{len(flat_matrix)}b", *flat_matrix)
        return compressed_data

    def compress_move(self, move):
        # Convert a move tuple to a compacted string
        move_str = f"{move[0][0]}{move[0][1]}{move[1].value}"
        move_bytes = move_str.encode('utf-8')
        return move_bytes

    def decode_compressed_move(self, compressed_move):
        # Decode a compressed move string to a move tuple
        move_str = compressed_move.decode('utf-8')
        return (int(move_str[0]), int(move_str[1])), Move(int(move_str[2]))

