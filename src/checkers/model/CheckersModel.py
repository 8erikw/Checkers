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
            Initializes the legal_moves and pieces
        """
        self.legal_moves = []
        self.pieces = []
        self.init_Game()

    def init_Game(self):
        """
            Starts a new game.
        """




    def isGoalState(self, state):
        if