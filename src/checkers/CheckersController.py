import CheckersModel as Cm

RED = -1
BLUE = 1


class CheckersController:
    def __init__(self):
        self.model = Cm.CheckersModel()
        self.player = 0

    def play(self, by_self=False):
        print("Welcome! Start playing Checkers by choosing which team you would like to be on:")
        while True:
            choice = input("Would you like to play as the Red pieces (first), or the Blue pieces (second)? ")
            choice = choice.lower()
            if choice == "red":
                self.player = RED
                break
            elif choice == "blue":
                self.player = BLUE
                break
            else:
                print("I'm sorry, I couldn't recognize your input. Try Again!")

        while not self.model.isTerminalState():
            print("Turn: ", self.model.turn)
            move_made = False
            while not self.model.isTurnOver() or not move_made:
                move_made = True
                print(self.model.force_jump())
                self.model.printBoard()
                if self.model.turn == self.player:
                    while True:
                        try:
                            x = int(input("Enter the x position of the piece you would like to move: "))
                            y = int(input("Enter the y position of the piece you would like to move: "))

                            dx = int(input("Enter the x position of the new position of the piece: "))
                            dy = int(input("Enter the y position of the new position of the piece: "))
                            self.model.move(self.model.board[(x, y)], (dx - x, dy - y))
                            break
                        except ValueError:
                            print("Try again!")

                else:
                    comp_action = self.model.alpha_beta_pruning(5, -49, 49, self.player)
                    print("Computer: I calculate a score of ", comp_action[0])
                    print("Computer: I move ", comp_action[1][0].get_position(), " by ", comp_action[1][1])
                    self.model.move(comp_action[1][0], comp_action[1][1])

        print("The winner is ", self.model.winner())
