class player: 
    def __init__(self, nombre, color):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__piezas__ = 15
        self.__turno__ = False
        self.__movimientos__ = []
        self.__capturadas__ = 0 
