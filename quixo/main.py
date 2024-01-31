import random
from tqdm import tqdm
from game import Game, Move, Player
from minmax_player import MinMaxPlayer
from qlearning_player import QLearningPlayer
from monte_carlo_player import MonteCarloPlayer
from experiment_player import ExperimentPlayer
from clever_player import CleverPlayer


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]: 

        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    

if __name__ == '__main__':

    g = Game()
    #player1 = MinMaxPlayer()
    #player1 = QLearningPlayer()
    #player1 = MonteCarloPlayer()
    player1 = ExperimentPlayer()
    player2 = RandomPlayer()
    #player2 = CleverPlayer()

    player1_wins=0
    for i in tqdm(range(1,1001)):
        winner = g.play(player1, player2)
        g.print()
        if winner==0:
            player1_wins+=1
        tqdm.write(f"Game: {i}, wins: {player1_wins}")
        g=Game()

    print(f"Wins: {player1_wins}/1000")
    print(f"Winner: Player {winner}")

#MinMax with recursion of depth=2 with pruning alpha>=beta results: 641/1000 = 64.1% of wins 
#QleaningPlayer  55.1% win
#Montecarlo 74.5% win with 500 simulations 40 analyzed moves
#CleverPlayer 89.2% win
#Experiment Player with 3 simulations e 8 analyzed moves: 99.8% win
#Experiment Player with 5 simulations e 10 analyzed moves: 100% win
