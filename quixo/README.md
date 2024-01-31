# Agents

## CleverPlayer

Choose a move randomly from the available moves that do not make you loss, favoring those that allow you to claim a square that 
is still without a symbol. If there is a move that leads to your victory, makes that move immediately.

## MinMaxPlayer

A standard MinMax algorithm with a maximum depth = 2 to maintain acceptable execution times per move and with pruning alpha>=beta. 

## QLearningPlayer

A fundamental Q-learning implementation, trained without relying on the recursive Bellman equation. Instead, it utilizes the trajectory, focusing only on the states of the Q-learning player. Due to its memory-intensive nature, both the state and the action are compressed.

## MonteCarloPlayer

The player uses Monte Carlo simulation technique to make decisions about its moves. Iterates over a randomly selected subset of available moves and simulates multiple games to evaluate the potential outcomes of a move. Simulates the game until there is a winner and updates the total score based on the outcome of the simulation. At the end it will choose the best move based on the total score of the simulations.

## ExperimentPlayer

Mix of MontecarloPlayer and CleverPlayer. It makes intelligent moves in a little number of simulations and it chooses the best. Each time it evaluates only a subset of the possible moves, otherwise it would be too slow. The moves it evaluates are filtered in any case, excluding those that would make you lose on the next move, and if there is a move that leads to your victory, makes that move, similar to CleverPlayer.

# Evaluations

Simulating 1000 games against the RandomPlayer, let's examine the results obtained:
- QLearningPlayer Win Rate: 55.1%
- MinMaxPlayer Win Rate: 64.1%
- MonteCarloPlayer(500 simulations 40 analyzed moves) Win Rate: 75.5%
- CleverPlayer Win Rate: 89.2%
- ExperimentPlayer(3 simulations 8 analyzed moves) Win Rate: 99.8%
- ExperimentPlayer(5 simulations 10 analyzed moves) Win Rate: 100%