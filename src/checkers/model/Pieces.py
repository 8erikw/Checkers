RED, BLUE = 0, 1


class Pieces:
    def __init__(self, x_position, y_position, team):
        self.position = (x_position, y_position)
        self.team = team
        self.king = False

    def promote(self):
        if self.is_king():
            raise ValueError("Already Promoted")
        else:
            self.king = True

    def is_king(self):
        return self.king

    def change_position(self, dx, dy):
        x = self.position[0]
        y = self.position[1]
        self.position = (x + dx, y + dy)

    def get_position(self):
        return self.position

    def get_team(self):
        return self.team
