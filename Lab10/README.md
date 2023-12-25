# Lab 10: TicTacToe

## Solution


To train my agent, I used the Q-Learning technique, specifically the Model-free Q-Learning. The epsilon parameter that I used dynamically balances exploration and exploitation, ensuring that exploration never goes below 0.15. The trained agent always starts the game first and practices against a player who randomly chooses their move from the available options. TicTacToe is a two player game, so the Q-learning pass from the state S(t) to the state S(t+2), because the intermediate state is played by the other player.

