class Checker:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def is_off_board(self):
        return self.position == 'off'