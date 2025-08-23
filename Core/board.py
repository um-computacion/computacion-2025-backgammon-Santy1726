class Board:
    def __init__(self):
        self.__board__ = self.create_board() 
        
    def create_board(self):
        
        board = [0] * 24
        board[0] = 2
        board[5] = -5
        board[7] = -3
        board[11] = 5
        board[12] = -5
        board[16] = 3
        board[18] = 5
        board[23] = -2
        return board




