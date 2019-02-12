"""
    This is the implementation of the Checkers board
"""

# Author: Erik Wong
# Date: February 1, 2019

from Pieces import Pieces

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
        self.state = []
        self.init_Game()


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
                self.red_pieces.append(Pieces(5, i, RED))
                self.red_pieces.append(Pieces(7, i, RED))
                self.blue_pieces.append(Pieces(1, i, BLUE))
            else:
                self.blue_pieces.append(Pieces(0, i, BLUE))
                self.blue_pieces.append(Pieces(2, i, BLUE))
                self.red_pieces.append(Pieces(6, i, RED))

        self.state.append(self.blue_pieces)
        self.state.append(self.red_pieces)


    def isTerminalState(self):
        """
        Returns whether the current state of the game is over, regardless of who won or lost
        :return: A boolean value denoting whether the game is over
        """
        return len(self.red_pieces) == 0 or len(self.blue_pieces) == 0

    def move(self, curr_piece, move):
        """

        :param curr_piece: A tuple holding the (x,y) coordinates of a piece
        :param move: A tuple holding the change in coordinates (dx, dy) of the given piece
        :return: The next state of the board after the move is played
        """
        # Checking so that a non-king piece is not moving backwards
        if move[1] < 0 and not curr_piece.is_king():
            raise ValueError("Invalid Move")

        # Checking so that a move strictly diagonal and within a 1 or 2 unit radius
        if abs(move[1]) != abs(move[0]) and (abs(move[0]) > 2 or move[0] == 0):
            raise ValueError("Invalid Move")

        # new_spot is the new location of the curr_piece
        new_spot = (curr_piece[0] + move[0], curr_piece[1] + move[1])

        # Checks if the new_spot is within the board's boundaries
        if new_spot[0] < 0 or new_spot[1] < 0 or new_spot[0] > self.size - 1 or new_spot[1] > self.size - 1:
            raise ValueError("Invalid Move")

        # Checking so that moves are valid

        # Checking if a piece is not currently at the new_spot
        if abs(move[0]) == 1:
            for team in self.state:
                for piece in team:
                    if piece.get_position == new_spot:
                        raise ValueError("Invalid Move")
            # After exiting the double for loop, we are sure that there are no pieces occupying the new square,
            # as no exceptions were raised
            curr_piece.change_position(new_spot)
            return

        # A jump is taking place, so an opposing color piece must be in between the jump
        else:
            # Calculate the space on the board that is jumped over
            jump_spot = (curr_piece[0] + move[0] / 2, curr_piece[1] + move[1] / 2)

            # Calculate the current and opposite teams
            curr_team = curr_piece.get_team()
            opp_team = RED
            if curr_team == RED:
                opp_team = BLUE

            for piece in self.state[opp_team]:
                if piece.get_position == jump_spot:
                    curr_piece.change_position(new_spot)
                    return
            # Program reaches here if there is no opposing team's piece is in the jump_spot
            raise ValueError("Invalid Move")





