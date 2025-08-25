class Checker:
    def __init__(self, color, position):
        self.__color__ = color
        self.__position__ = position

    def move(self, new_position):
        self.__position__ = new_position

    def is_off_board(self):
        return self.__position__ == 'off'