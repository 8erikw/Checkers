RED, BLUE = -1, 1


class Pieces:
    def __init__(self, x_position, y_position, team, king=False):
        self.position = (x_position, y_position)
        self.team = team
        self.king = king

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

    def deep_copy_piece(self):
        x = self.position[0]
        y = self.position[1]
        team = BLUE
        if self.team == RED:
            team = RED
        new_king = False
        if self.king:
            new_king = True
        return Pieces(x, y, team, king=new_king)

    def getString(self):
        if self.team == 0:
            return "__"
        if self.team == RED:
            if self.king:
                return "R*"
            return "R."
        if self.king:
            return "B*"
        return "B."

