"""
    This is the implementation of the Checkers board
"""

# Author: Erik Wong
# Date: February 1, 2019

RED, BLUE = 1, 0
# RED pieces will always go first
# TO BE IMPLEMENTED : Players can choose which color piece they want to play at the start of the game

# RED and BLUE are the two different players of the game
# RED pieces start from the bottom of the board and move up
# BLUE pieces start from the top of the board and move down
# All pieces move diagonally
# A piece must move if it is that respective player's turn and it is going to "Eat" an opposing player's piece

class CheckersModel:
    def __init__(self):
        """
        Initializes the board
        """
        self.size = 8
        self.state = []
        self.red_pieces = []
        self.blue_pieces = []
        self.init_Game()
        self.state = []

    def init_Game(self):
        """
        Starts a new game.

        Here is the normal start state of a standard 8 by 8 checkerboard

              0 1 2 3 4 5 6 7
            0 _ B _ B _ B _ B
            1 B _ B _ B _ B _
            2 _ B _ B _ B _ B
            3 _ _ _ _ _ _ _ _
            4 _ _ _ _ _ _ _ _
            5 R _ R _ R _ R _
            6 _ R _ R _ R _ R
            7 R _ R _ R _ R _

        """
        size = self.size

        for i in range(size):
            if i % 2 == 0:
                self.red_pieces.append(((5, i), False))
                self.red_pieces.append(((7, i), False))
                self.blue_pieces.append(((1, i), False)
            else:
                self.blue_pieces.append((0, i))
                self.blue_pieces.append((2, i))
                self.red_pieces.append((6, i))
        self.state.append(self.red_pieces)
        self.state.append(self.blue_pieces)

    def isTerminalState(self):
        """
        Returns whether the current state of the game is over, regardless of who won or lost
        :return: A boolean value denoting whether the game is over
        """
        return len(self.red_pieces) == 0 or len(self.blue_pieces) == 0

    def move(self, piece, move):
        """

        :param piece: A tuple holding the (x,y) coordinates of a piece
        :param move: A tuple holding the change in coordinates (dx, dy) of the given piece
        :return: The next state of the board after the move is played
        """
        if move[0] != move[1]:
            raise ValueError(Invalid Move)
        new_spot = (piece[0] + move[0], piece[1] + move[1])
        if piece in self.state[1] and ne
