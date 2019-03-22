"""
    This is the implementation of the Checkers board
"""

# Author: Erik Wong
# Date: February 1, 2019

from Pieces import Pieces

RED = -1
BLUE = 1
DEPTH = 5


# RED pieces will always go first
# TO BE IMPLEMENTED : Players can choose which color piece they want to play at the start of the game

# RED and BLUE are the two different players of the game
# RED pieces start from the bottom of the board and move up
# BLUE pieces start from the top of the board and move down
# All pieces move diagonally
# A piece must move if it is that respective player's turn and it is going to "Eat" an opposing player's piece

class CheckersModel:
    def __init__(self, copy=False, size=None, turn=None, board=None, piece_taken=None):
        """
        Initializes the board
        """
        if copy:
            self.size = size
            self.turn = turn
            self.board = board
            self.piece_taken = piece_taken
        else:
            self.size = 8
            self.turn = RED
            self.board = dict([((x, y), Pieces(x, y, 0)) for x in range(self.size) for y in range(self.size)])
            self.init_Game()
            self.piece_taken = False

    def deepcopy(self):
        size = self.size + 0
        turn = self.turn * 1
        board = dict([((x, y), self.board[(x, y)].deep_copy_piece()) for x in range(size) for y in range(size)])
        piece_taken = self.piece_taken

        new_model = CheckersModel(copy=True, size=size, turn=turn, board=board, piece_taken=piece_taken)
        return new_model

    def init_Game(self):
        """
        Starts a new game.

        Here is the normal start state of a standard 8 by 8 checkerboard

              0  1  2  3  4  5  6  7
            0 __ B  __ B  __ B  __ B
            1 B  __ B  __ B  __ B  __
            2 __ B  __ B  __ B  __ B
            3 __ __ __ __ __ __ __ __
            4 __ __ __ __ __ __ __ __
            5 R  __ R  __ R  __ R  __
            6 __ R  __ R  __ R  __ R
            7 R  __ R  __ R  __ R  __

        """
        size = self.size

        for i in range(size):
            if i % 2 == 0:
                self.board[(i, 5)] = Pieces(i, 5, RED)
                self.board[(i, 7)] = Pieces(i, 7, RED)
                self.board[(i, 1)] = Pieces(i, 1, BLUE)
            else:
                self.board[(i, 0)] = Pieces(i, 0, BLUE)
                self.board[(i, 2)] = Pieces(i, 2, BLUE)
                self.board[(i, 6)] = Pieces(i, 6, RED)

    def isTerminalState(self):
        """
        Returns whether the current state of the game is over, regardless of who won or lost
        :return: A boolean value denoting whether the game is over
        """
        red = 0
        blue = 0
        for piece in self.board.values():
            if piece.get_team() == RED:
                red += 1
            elif piece.get_team() == BLUE:
                blue += 1

        return red == 0 or blue == 0

    def winner(self):
        if self.isTerminalState():
            return self.turn * -1

    def force_jump(self):
        for piece in self.board.values():
            if piece.get_team() == self.turn and self.jump_possible(piece):
                return True
        return False

    def inBounds(self, position):
        x = position[0]
        y = position[1]
        if -1 < x < self.size and -1 < y < self.size:
            return True
        return False

    def jump_possible(self, piece):
        curr_pos = piece.get_position()
        x = curr_pos[0]
        y = curr_pos[1]

        opp_team = piece.get_team() * -1

        if piece.is_king():
            jump_pos1 = (x + 1, y - 1 * piece.get_team())
            land_pos1 = (x + 2, y - 2 * piece.get_team())
            jump_pos2 = (x - 1, y - 1 * piece.get_team())
            land_pos2 = (x - 2, y - 2 * piece.get_team())
            if self.inBounds(jump_pos1) and self.inBounds(land_pos1):
                if self.board[jump_pos1].get_team() == opp_team and self.board[land_pos1].get_team() == 0:
                    return True
            if self.inBounds(jump_pos2) and self.inBounds(land_pos2):
                if self.board[jump_pos2].get_team() == opp_team and self.board[land_pos2].get_team() == 0:
                    return True

        jump_pos1 = (x + 1, y + 1 * piece.get_team())
        land_pos1 = (x + 2, y + 2 * piece.get_team())
        jump_pos2 = (x - 1, y + 1 * piece.get_team())
        land_pos2 = (x - 2, y + 2 * piece.get_team())

        if self.inBounds(jump_pos1) and self.inBounds(land_pos1):
            if self.board[jump_pos1].get_team() == opp_team and self.board[land_pos1].get_team() == 0:
                return True
        if self.inBounds(jump_pos2) and self.inBounds(land_pos2):
            if self.board[jump_pos2].get_team() == opp_team and self.board[land_pos2].get_team() == 0:
                return True
        return False

    def move(self, curr_piece, move):
        """

        :param curr_piece: A piece object
        :param move: A tuple holding the change in coordinates (dx, dy) of the given piece
        :return: The next state of the board after the move is played
        """
        if curr_piece.get_team() == 0:
            raise ValueError("Invalid Move, Blank spot has no piece")

        # Checking so that a non-king piece is not moving backwards

        if curr_piece.get_team() * move[1] < 0 and not curr_piece.is_king():
            raise ValueError("Invalid Move, not a king")

        # Checking so that a move strictly diagonal and within a 1 or 2 unit radius
        if abs(move[1]) != abs(move[0]) or (abs(move[0]) > 2 or move[0] == 0):
            raise ValueError("Invalid Move, bad move")

        curr_pos = curr_piece.get_position()
        # new_spot is the new location of the curr_piece
        new_spot = (curr_pos[0] + move[0], curr_pos[1] + move[1])

        # Checks if the new_spot is within the board's boundaries
        if not self.inBounds(new_spot):
            raise ValueError("Invalid Move, out of bounds")

        # Checking so that moves are valid

        # Checking if a piece is not currently at the new_spot

        if self.board[new_spot].get_team() != 0:
            raise ValueError("Invalid Move, new spot is occupied")

        # Calculate the current and opposite teams
        curr_team = curr_piece.get_team()
        opp_team = RED
        if curr_team == RED:
            opp_team = BLUE
        opp_index = int((opp_team + 1) / 2)

        if abs(move[0]) == 1:
            curr_piece.change_position(new_spot[0], new_spot[1])
            self.board[curr_pos] = Pieces(curr_pos[0], curr_pos[1], 0)

            promotion_row = (opp_index * (self.size - 1) - self.size + 1) * -1
            if new_spot[1] == promotion_row and not curr_piece.is_king():
                curr_piece.promote()
            self.board[new_spot] = curr_piece
            self.piece_taken = False
            self.turn *= -1
            return

        # A jump is taking place, so an opposing color piece must be in between the jump
        else:
            # Calculate the space on the board that is jumped over
            jump_spot = (curr_pos[0] + move[0] / 2, curr_pos[1] + move[1] / 2)

            if self.board[jump_spot].get_team() == self.turn * -1:
                curr_piece.change_position(new_spot[0], new_spot[1])
                self.board[curr_pos] = Pieces(curr_pos[0], curr_pos[1], 0)

                promotion_row = (opp_index * (self.size - 1) - self.size + 1) * -1
                if new_spot[1] == promotion_row and not curr_piece.is_king():
                    curr_piece.promote()

                self.board[jump_spot] = Pieces(jump_spot[0], jump_spot[1], 0)
                self.board[curr_pos] = Pieces(curr_pos[0], curr_pos[1], 0)
                self.board[new_spot] = curr_piece
                self.piece_taken = True

                return
            # Program reaches here if there is no opposing team's piece is in the jump_spot
            raise ValueError("Invalid Move, empty jump")

    def try_move(self, curr_piece, move):
        """

        :param curr_piece: A tuple holding the (x,y) coordinates of a piece
        :param move: A tuple holding the change in coordinates (dx, dy) of the given piece
        :return: The next state of the board after the move is played
        """
        if curr_piece.get_team() == 0:
            raise ValueError("Invalid Move, Blank spot has no piece")

        # Checking so that a non-king piece is not moving backwards
        if curr_piece.get_team() * move[1] < 0 and not curr_piece.is_king():
            raise ValueError("Invalid Move")

        # Checking so that a move strictly diagonal and within a 1 or 2 unit radius
        if abs(move[1]) != abs(move[0]) or (abs(move[0]) > 2 or move[0] == 0):
            raise ValueError("Invalid Move")

        # new_spot is the new location of the curr_piece
        curr_position = curr_piece.get_position()

        new_spot = (curr_position[0] + move[0], curr_position[1] + move[1])

        # Checks if the new_spot is within the board's boundaries
        if not self.inBounds(new_spot):
            raise ValueError("Invalid Move")

        # Checking so that moves are valid

        # Checking if a piece is not currently at the new_spot

        if self.board[new_spot].get_team() != 0:
            raise ValueError("Invalid Move, new spot is occupied")

        if abs(move[0]) == 1 and not self.jump_possible(curr_piece):
            return

        # A jump is taking place, so an opposing color piece must be in between the jump
        elif abs(move[0] == 2):
            # Calculate the space on the board that is jumped over
            jump_spot = (curr_position[0] + move[0] / 2, curr_position[1] + move[1] / 2)

            if self.board[jump_spot].get_team() == self.turn * -1:
                return

            # Program reaches here if there is no opposing team piece in the jump_spot
            raise ValueError("Invalid Move")

        else:
            raise ValueError("Invalid Move")

    def possibleMoves(self):
        moves = []
        must_jump = self.force_jump()
        for piece in self.board.values():
            if self.turn == piece.get_team():
                if must_jump:
                    try:
                        self.try_move(piece, (2, 2))
                        print("Adding 2,2", piece.get_position)
                        moves.append((piece, (2, 2)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (2, -2))
                        print("Adding 2,-2", piece.get_position)
                        moves.append((piece, (2, -2)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (-2, 2))
                        print("Adding -2,2", piece.get_position)
                        moves.append((piece, (-2, 2)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (-2, -2))
                        print("Adding -2,-2", piece.get_position()[0], piece.get_position()[1])
                        moves.append((piece, (-2, -2)))
                    except ValueError:
                        pass
                else:
                    try:
                        self.try_move(piece, (1, 1))
                        print("Adding 1,1", piece.get_position()[0], piece.get_position()[1])
                        moves.append((piece, (1, 1)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (1, -1))
                        print("Adding 1,-1", piece.get_position()[0], piece.get_position()[1])
                        moves.append((piece, (1, -1)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (-1, 1))
                        print("Adding -1,1", piece.get_position()[0], piece.get_position()[1])
                        moves.append((piece, (-1, 1)))
                    except ValueError:
                        pass
                    try:
                        self.try_move(piece, (-1, -1))
                        print("Adding -1,-1", piece.get_position()[0], piece.get_position()[1])
                        moves.append((piece, (-1, -1)))
                    except ValueError:
                        pass
        print("Next turn")
        return moves

    def isTurnOver(self):
        return not self.piece_taken

    def printBoard(self):
        print("   0  1  2  3  4  5  6  7")
        for j in range(self.size):
            line = " " + str(j) + " "
            for i in range(self.size):
                line += self.board[(i, j)].getString() + " "
            print(line)
        print("")

    # Current Calculation for best move, which will be updated in the future
    def utility(self):
        score = 0
        for piece in self.board.values():
            score += piece.get_team()
        return score

    # Finally beginning to implement some AI algorithms
    def generateSuccessor(self, action):

        new_copy = self.deepcopy()

        # new_model = CheckersModel(upload=True, new=new_copy)
        position = action[0].get_position()
        new_copy.move(new_copy.board[position], action[1])
        # new_model.move(new_model.board[position], action[1])
        return new_copy

    def alpha_beta_pruning(self, depth, alpha, beta, player, b_action=None):
        minimize = True
        if player == BLUE:
            minimize = False

        if self.turn == player:
            minimize = not minimize

        if depth == 0 or self.isTerminalState():
            util_action = (self.utility(), b_action)
            return util_action
        best_action = b_action

        if minimize:
            minimum = -50
            for action in self.possibleMoves():

                new_model = self.generateSuccessor(action)

                if self.turn == new_model.turn:
                    curr_action = new_model.alpha_beta_pruning(depth, alpha, beta, player, b_action=action)
                else:
                    curr_action = new_model.alpha_beta_pruning(depth - 1, alpha, beta, player, b_action=action)

                if minimum < curr_action[0]:
                    minimum = curr_action[0]
                    best_action = action
                beta = min(beta, minimum)
                if alpha >= beta:
                    break
            util_action = (minimum, best_action)
            return util_action
        else:
            maximum = 50
            for action in self.possibleMoves():
                new_model = self.generateSuccessor(action)
                if self.turn == new_model.turn:
                    curr_action = new_model.alpha_beta_pruning(depth, alpha, beta, player, b_action=action)
                else:
                    curr_action = new_model.alpha_beta_pruning(depth - 1, alpha, beta, player, b_action=action)

                if maximum > curr_action[0]:
                    maximum = curr_action[0]
                    best_action = action
                alpha = max(alpha, maximum)
                if alpha >= beta:
                    break
            util_action = (maximum, best_action)
            return util_action
