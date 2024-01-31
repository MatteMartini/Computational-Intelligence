from abc import ABC, abstractmethod
from copy import deepcopy, copy
from enum import Enum
import numpy as np
import random

# Rules on PDF


class Move(Enum):
    '''
    Selects where you want to place the taken piece. The rest of the pieces are shifted
    '''
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class Player(ABC):
    def __init__(self) -> None:
        '''You can change this for your player if you need to handle state/have memory'''
        pass

    @abstractmethod
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]: 
        '''
        The game accepts coordinates of the type (X, Y). X goes from left to right, while Y goes from top to bottom, as in 2D graphics.
        Thus, the coordinates that this method returns shall be in the (X, Y) format.

        game: the Quixo game. You can use it to override the current game with yours, but everything is evaluated by the main game
        return values: this method shall return a tuple of X,Y positions and a move among TOP, BOTTOM, LEFT and RIGHT
        '''
        pass


class Game(object):
    def __init__(self) -> None: 
        self._board = np.ones((5, 5), dtype=np.uint8) * -1
        self.current_player_idx = 1  

    def get_board(self) -> np.ndarray:
        '''
        Returns the board
        '''
        return deepcopy(self._board)

    def get_current_player(self) -> int:
        '''
        Returns the current player
        '''
        return deepcopy(self.current_player_idx)

    def print(self):
        '''Prints the board. -1 are neutral pieces, 0 are pieces of player 0, 1 pieces of player 1'''
        print(self._board)

    def check_winner(self) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        for x in range(self._board.shape[0]):
            # if a player has completed an entire row
            if self._board[x, 0] != -1 and all(self._board[x, :] == self._board[x, 0]):
                # return the relative id
                return self._board[x, 0]
        # for each column
        for y in range(self._board.shape[1]):
            # if a player has completed an entire column
            if self._board[0, y] != -1 and all(self._board[:, y] == self._board[0, y]):
                # return the relative id
                return self._board[0, y]
        # if a player has completed the principal diagonal
        if self._board[0, 0] != -1 and all(
            [self._board[x, x]
                for x in range(self._board.shape[0])] == self._board[0, 0]
        ):
            # return the relative id
            return self._board[0, 0]
        # if a player has completed the secondary diagonal
        if self._board[0, -1] != -1 and all(
            [self._board[x, -(x + 1)]
             for x in range(self._board.shape[0])] == self._board[0, -1]
        ):
            # return the relative id 
            return self._board[0, -1]
        return -1 #If neither of the two has won yet, return -1

    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move( 
                    self) 
                ok = self.__move(from_pos, slide, self.current_player_idx) #It's the __move function that modifies the board, not make_move.
            winner = self.check_winner()
        return winner
    
    def __move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool: #Takes a position, a move, and a player ID. It performs a move if it is valid
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id) #method __take check if the position of the element is acceptable 
        if acceptable:
            acceptable = self.__slide((from_pos[1], from_pos[0]), slide) 
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def __take(self, from_pos: tuple[int, int], player_id: int) -> bool: #Takes a position and a player ID. It handles the process of a player taking a piece.
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (self._board[from_pos] < 0 or self._board[from_pos] == player_id) #check if in the element there is -1 or your id
        if acceptable:
            self._board[from_pos] = player_id
        return acceptable

    def __slide(self, from_pos: tuple[int, int], slide: Move) -> bool: #Takes a position and a move. It handles the process of sliding pieces after a move.
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = self._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                self._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    self._board[(i, from_pos[1])] = self._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                self._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    self._board[(i, from_pos[1])] = self._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable

#My functions
    def reward(self):
        if self.check_winner()==0:
            return 1
        elif self.check_winner()==1:
            return -1
        else:
            return 0

    #check if it's possible to do a move without use the private functions _take and _slide in a faster way
    def check_move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        app = (from_pos[1], from_pos[0])
        # Check take
        acceptable_take = (
            (app[0] == 0 and app[1] < 5)
            or (app[0] == 4 and app[1] < 5)
            or (app[1] == 0 and app[0] < 5)
            or (app[1] == 4 and app[0] < 5)
        ) and (self._board[app] < 0 or self._board[app] == player_id)

        # Check slide
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        if app not in SIDES:
            acceptable_top = app[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_bottom = app[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_left = app[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            acceptable_right = app[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        else:
            acceptable_top = app == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            acceptable_left = app == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            acceptable_right = app == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            acceptable_bottom = app == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)

        return acceptable_take and (acceptable_top or acceptable_bottom or acceptable_left or acceptable_right)

    # to call the move externally on a game deepcopy.
    def my_move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        #save the state of the board and then you restore it if the move is not valid
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        
        def take_and_slide(pos: tuple[int, int], slide: Move) -> bool:
            nonlocal prev_value #to use a variable out this scope. 
            take_ok = self.__take(pos, player_id)
            if take_ok:
                slide_ok = self.__slide(pos, slide)
                if not slide_ok:
                    self._board[pos] = deepcopy(prev_value)
                return slide_ok
            return False
        
        move_ok = take_and_slide((from_pos[1], from_pos[0]), slide)
        
        if move_ok:
            self.current_player_idx = (self.current_player_idx + 1) % 2  #after the move change the actual player
        
        return move_ok
    
    #used in QlearningPlayer. We don't need to change player here  
    def qlearning_move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool: #Takes a position, a move, and a player ID. It performs a move if it is valid
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id) #il metodo take controlla se la mossa è accettabile, sta qui sotto
        if acceptable:
            acceptable = self.__slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable
    
    #give a list of all the legal moves (position, slide, player_id)
    def available_moves(self, player_idx) -> list:
        possible_moves = []

        # Iterate over the edges
        for y in [0, 4]:
            for x in range(5):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        possible_moves.append((from_pos, slide))

        for x in [0, 4]:
            for y in range(1, 4):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        possible_moves.append((from_pos, slide))

        return possible_moves
    
    #like the function above but you also check if there's a move that allows you to win and it filters the moves that make you loss
    def experimental_available_moves(self, player_idx) -> list:
        possible_moves = []

        # Iterate over the edges
        for y in [0, 4]:
            for x in range(5):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        #if the move bring to the victory, return only it in the possible moves
                        if self.check_victory_move(from_pos, slide, player_idx):
                            return [(from_pos, slide)]  
                        # check if the move make you lose
                        if not self.is_loss_move(from_pos, slide, player_idx):
                            possible_moves.append((from_pos, slide))

        for x in [0, 4]:
            for y in range(1, 4):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        if self.check_victory_move(from_pos, slide, player_idx):
                            return [(from_pos, slide)] 
                        if not self.is_loss_move(from_pos, slide, player_idx):
                            possible_moves.append((from_pos, slide))

        # if every move make you lose, the possible_moves will be empty, so you return the legal moves
        if not possible_moves:
            legal_moves = self.available_moves(player_idx)
            if legal_moves:
                return [random.choice(legal_moves)]

        return possible_moves
    
    #like the function above but when you have to choose an element you prefer the element of the board without your symbol
    #in this way you put more element on the board under your control. At the end you will have an advantage
    def clever_available_moves(self, player_idx) -> list:
        possible_moves = []
        best_possible_moves = []

        # Iterate over the edges
        for y in [0, 4]:
            for x in range(5):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        #if the move bring to the victory, return only it in the possible moves
                        if self.check_victory_move(from_pos, slide, player_idx):
                            return [(from_pos, slide)]  
                        # check if the move make you lose
                        if not self.is_loss_move(from_pos, slide, player_idx):
                            possible_moves.append((from_pos, slide))
                            target_value = self._board[y, x]
                            # add the move only if the target is -1
                            if target_value == -1:
                                best_possible_moves.append((from_pos, slide))


        for x in [0, 4]:
            for y in range(1, 4):
                from_pos = (y, x)
                for slide in Move:
                    if self.check_move(from_pos, slide, player_idx):
                        if self.check_victory_move(from_pos, slide, player_idx):
                            return [(from_pos, slide)]
                        if not self.is_loss_move(from_pos, slide, player_idx):
                            possible_moves.append((from_pos, slide))
                            target_value = self._board[y, x]
                            if target_value == -1:
                                best_possible_moves.append((from_pos, slide))

        # if every move make you lose, the possible_moves will be empty, so you return the legal moves
        if not possible_moves:
            legal_moves = self.available_moves(player_idx)
            if legal_moves:
                return [random.choice(legal_moves)]
        if not best_possible_moves:
            return possible_moves
        return best_possible_moves

    #check if doing the move you loss the game
    def is_loss_move(self, from_pos: tuple[int, int], slide: Move, player_idx: int) -> bool:
        # Save the original board
        original_board = deepcopy(self._board)
        self.__move(from_pos, slide, player_idx)
        is_loss = self.check_winner() == 1 - player_idx

        # Restore the board before the simulation of the move
        self._board = original_board
        return is_loss
 
    
    def check_victory_move(self, from_pos: tuple[int, int], slide: Move, player_idx: int) -> bool:
        # Save the original board
        original_board = deepcopy(self._board)
        self.__move(from_pos, slide, player_idx)
        is_victory = self.check_winner() == player_idx

        # Restore the board before the simulation of the move
        self._board = original_board

        return is_victory
