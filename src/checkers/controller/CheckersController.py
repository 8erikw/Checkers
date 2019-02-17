import sys
# Trying to import files, might try __init__.py later
sys.path.append("src/checkers/controller/")

from checkers.model.CheckersModel import CheckersModel

class CheckersController:
    def __init__(self):
        self.model = CheckersModel()
        self.player = -1

    def play(self):
        print("Welcome! Start playing Checkers by choosing which team you would like to be on:")
        while(True):
            choice = raw_input("Would you like to play as the Red pieces (first), or the Blue pieces (second)? ")
            choice = choice.lower()
            if choice == "red":
                self.player = 0
                break
            elif choice == "blue":
                self.player = 1
                break
            else:
                print("I'm sorry, I couldn't recognize your input. Try Again!")
        while not self.model.isTerminalState():
            break

