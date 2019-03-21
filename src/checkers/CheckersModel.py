"""
    This is the implementation of the Checkers board
"""

# Author: Erik Wong
# Date: February 1, 2019

from Pieces import Pieces

RED, BLUE = 0, 1
DEPTH = 5


# RED pieces will always go first
# TO BE IMPLEMENTED : Players can choose which color piece they want to play at the start of the game

# RED and BLUE are the two different players of the game
# RED pieces start from the bottom of the board and move up
# BLUE pieces start from the top of the board and move down
# All pieces move diagonally
# A piece must move if it is that respective player's turn and it is going to "Eat" an opposing player's piece

class CheckersModel:
    def __init__(self, upload=False, state=None):
        """
        Initializes the board
        """
        self.size = 8
        self.state = []
        self.red_pieces = []
        self.blue_pieces = []
        self.turn = RED
        self.init_Game()
        self.piece_taken = False
        self.board = dict([((x, y), "__") for x in range(self.size) for y in range(self.size)])

        if upload:
            self.state = state

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
                self.board[(5, i)] = "R."
                self.board[(7, i)] = "R."
                self.board[(1, i)] = "B."
                self.red_pieces.append(Pieces(5, i, RED))
                self.red_pieces.append(Pieces(7, i, RED))
                self.blue_pieces.append(Pieces(1, i, BLUE))
            else:
                self.board[(0, i)] = "B."
                self.board[(2, i)] = "B."
                self.board[(6, i)] = "R."
                self.blue_pieces.append(Pieces(0, i, BLUE))
                self.blue_pieces.append(Pieces(2, i, BLUE))
                self.red_pieces.append(Pieces(6, i, RED))

        self.state.append(self.red_pieces)
        self.state.append(self.blue_pieces)

    def isTerminalState(self):
        """
        Returns whether the current state of the game is over, regardless of who won or lost
        :return: A boolean value denoting whether the game is over
        """
        return len(self.red_pieces) == 0 or len(self.blue_pieces) == 0

    def force_jump(self):
        for team in self.state:
            for piece in team:
                if self.jump_possible(piece):
                    return True
        return False

    def jump_possible(self, piece):
        if piece.is_king():
            try:
                self.try_move(piece, (2, -2))
                self.try_move(piece, (-2, -2))
            except ValueError:
                return False
        try:
            self.try_move(piece, (2, 2))
            self.try_move(piece, (2, 2))
        except ValueError:
            return False

        return True

    def move(self, curr_piece, move):
        """

        :param curr_piece: A piece object
        :param move: A tuple holding the change in coordinates (dx, dy) of the given piece
        :return: The next state of the board after the move is played
        """
        # Checking so that a non-king piece is not moving backwards
        if move[1] < 0 and not curr_piece.is_king():
            raise ValueError("Invalid Move")

        # Checking so that a move strictly diagonal and within a 1 or 2 unit radius
        if abs(move[1]) != abs(move[0]) and (abs(move[0]) > 2 or move[0] == 0):
            raise ValueError("Invalid Move")

        curr_pos = curr_piece.get_position()
        # new_spot is the new location of the curr_piece
        new_spot = (curr_pos[0] + move[0], curr_pos[1] + move[1])

        # Checks if the new_spot is within the board's boundaries
        if new_spot[0] < 0 or new_spot[1] < 0 or new_spot[0] > self.size - 1 or new_spot[1] > self.size - 1:
            raise ValueError("Invalid Move")

        # Checking so that moves are valid

        # Checking if a piece is not currently at the new_spot
        if abs(move[0]) == 1:
            for team in self.state:
                for piece in team:
                    if piece.get_position() == new_spot:
                        raise ValueError("Invalid Move")
            # After exiting the double for loop, we are sure that there are no pieces occupying the new square,
            # as no exceptions were raised
            curr_piece.change_position(new_spot)
            self.board[curr_pos] = "__"

            promotion_row = curr_piece.get_team() * self.size
            if new_spot[1] == promotion_row and not curr_piece.is_king():
                curr_piece.promote()
            self.board[new_spot] = curr_piece.getString()
            self.piece_taken = False
            return

        # A jump is taking place, so an opposing color piece must be in between the jump
        else:
            # Calculate the space on the board that is jumped over
            jump_spot = (curr_pos[0] + move[0] / 2, curr_pos[1] + move[1] / 2)

            # Calculate the current and opposite teams
            curr_team = curr_piece.get_team()
            opp_team = RED
            if curr_team == RED:
                opp_team = BLUE

            for piece in self.state[opp_team]:
                if piece.get_position == jump_spot:
                    curr_piece.change_position(new_spot)
                    self.state[opp_team].remove(piece)

                    promotion_row = curr_piece.get_team() * self.size
                    if new_spot[1] == promotion_row and not curr_piece.is_king():
                        curr_piece.promote()

                    self.board[jump_spot] = "__"
                    self.board[curr_pos] = "__"
                    self.board[new_spot] = curr_piece.getString()
                    self.piece_taken = True
                    return
            # Program reaches here if there is no opposing team's piece is in the jump_spot
            raise ValueError("Invalid Move")

    def deep_copy_state(self):
        new_state = []
        teams = 0
        state = self.state
        for team in state:
            new_state.append([])
            for piece in team:
                new_piece = piece.deep_copy()
                new_state[teams].append(new_piece)
            teams += 1
        return new_state

    def try_move(self, curr_piece, move):
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
        if abs(move[0]) == 1 and not self.jump_possible(curr_piece):
            for team in self.state:
                for piece in team:
                    if piece.get_position == new_spot:
                        raise ValueError("Invalid Move")
            # After exiting the double for loop, we are sure that there are no pieces occupying the new square,
            # as no exceptions were raised

            # In try_moves, so does not make any changes to the state
            return

        # A jump is taking place, so an opposing color piece must be in between the jump
        elif abs(move[0] == 2):
            # Calculate the space on the board that is jumped over
            jump_spot = (curr_piece[0] + move[0] / 2, curr_piece[1] + move[1] / 2)

            # Calculate the current and opposite teams
            curr_team = curr_piece.get_team()
            opp_team = RED
            if curr_team == RED:
                opp_team = BLUE

            for piece in self.state[opp_team]:
                if piece.get_position == jump_spot:
                    return
            # Program reaches here if there is no opposing team piece in the jump_spot
            raise ValueError("Invalid Move")

        else:
            raise ValueError("Invalid Move")

    def possibleMoves(self, team_turn):
        moves = []
        if self.force_jump():
            for piece in self.state[team_turn]:
                try:
                    self.try_move(piece, (2, 2))
                    moves.append((piece, (2, 2)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (2, -2))
                    moves.append((piece, (2, -2)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (-2, 2))
                    moves.append((piece, (-2, 2)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (-2, -2))
                    moves.append((piece, (-2, -2)))
                except ValueError:
                    pass
        else:
            for piece in self.state[team_turn]:
                try:
                    self.try_move(piece, (1, 1))
                    moves.append((piece, (1, 1)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (1, -1))
                    moves.append((piece, (1, -1)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (-1, 1))
                    moves.append((piece, (-1, 1)))
                except ValueError:
                    pass
                try:
                    self.try_move(piece, (-1, -1))
                    moves.append((piece, (-1, -1)))
                except ValueError:
                    pass
        return moves

    def printBoard(self):
        print("  0  1  2  3  4  5  6  7 ")
        for i in range(self.size):
            line = str(i)
            for j in range(self.size):
                line += self.board[(i, j)]
            print(line)

    # Current Calculation for best move, which will be updated in the future
    def utility(self):
        return len(self.blue_pieces) - len(self.red_pieces)

    # Finally beginning to implement some AI algorithmns
    def generateSuccessor(self, action):
        try:
            new_state = self.deep_copy_state()
            new_model = CheckersModel(upload=True, state=new_state)
            new_model.move(action[0], action[1])
            return new_model
        except ValueError:
            return

    def alpha_beta_pruning(self, model, depth, alpha, beta, player, b_action=None):
        new_turn = RED
        if model.turn == RED:
            new_turn = BLUE

        minimize = True
        if player == BLUE:
            minimize = False

        if model.turn == player:
            minimize = not minimize

        if depth == 0 or model.isTerminalState():
            util_action = (model.utility(), b_action)
            return util_action
        best_action = b_action

        if minimize:
            minimum = -50
            for action in model.possibleMoves(model.turn):
                new_model = model.generateSuccessor(action)
                if model.turn == new_model.turn:
                    curr_action = model.alpha_beta_pruning(new_model, depth, alpha, beta, player, b_action=action)
                else:
                    curr_action = model.alpha_beta_pruning(new_model, depth - 1, alpha, beta, player, b_action=action)

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
            for action in model.possibleMoves(model.turn):
                new_model = model.generateSuccessor(action)
                if model.turn == new_model.turn:
                    curr_action = model.alpha_beta_pruning(new_model, depth, alpha, beta, player, b_action=action)
                else:
                    curr_action = model.alpha_beta_pruning(new_model, depth - 1, alpha, beta, player, b_action=action)

                if maximum > curr_action[0]:
                    maximum = curr_action[0]
                    best_action = action
                alpha = max(alpha, maximum)
                if alpha >= beta:
                    break
            util_action = (maximum, best_action)
            return util_action
