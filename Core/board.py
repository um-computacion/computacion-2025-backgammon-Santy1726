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

    def obtener_board(self):
        return self.__board__  
         
    def establecer_posicion(self, indice, valor):
        if 0 <= indice < 24:
            self.__board__[indice] = valor
        else:
            raise IndexError("La posición debe estar entre 0 y 23")

    def obtener_posicion(self, indice):
        if 0 <= indice < 24:
            return self.__board__[indice]
        else:
            raise IndexError("La posición debe estar entre 0 y 23")

    def mover_ficha(self, origen, destino):
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise IndexError("Las posiciones deben estar entre 0 y 23")

        if self.__board__[origen] == 0:
            raise ValueError("No hay fichas en la posición de origen")

        jugador = 1 if self.__board__[origen] > 0 else -1

        self.__board__[origen] -= jugador
        self.__board__[destino] += jugador