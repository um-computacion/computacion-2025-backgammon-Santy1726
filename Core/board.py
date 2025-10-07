from Core.checker import Checker

class Board:
    def __init__(self):
        self.__board__ = [[] for _ in range(24)]
        self.__bar__ = {'blanco': [], 'negro': []}
        self.__inicializar_tablero__()

    def __inicializar_tablero__(self):
        self.__board__[0] = [Checker("blanco", 0) for _ in range(2)]
        self.__board__[5] = [Checker("negro", 5) for _ in range(5)]
        self.__board__[7] = [Checker("negro", 7) for _ in range(3)]
        self.__board__[11] = [Checker("blanco", 11) for _ in range(5)]
        self.__board__[12] = [Checker("negro", 12) for _ in range(5)]
        self.__board__[16] = [Checker("blanco", 16) for _ in range(3)]
        self.__board__[18] = [Checker("blanco", 18) for _ in range(5)]
        self.__board__[23] = [Checker("negro", 23) for _ in range(2)]

    def obtener_posicion(self, indice: int):
        if not (0 <= indice < 24):
            raise IndexError("Índice fuera de rango (0-23).")
        return list(self.__board__[indice])

    def mover_ficha(self, origen: int, destino: int):
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise IndexError("Índice fuera de rango (0-23).")
        if not self.__board__[origen]:
            raise ValueError("No hay fichas en la posición de origen.")

        ficha = self.__board__[origen].pop()

        if self.__board__[destino]:
            top = self.__board__[destino][-1]
            if top.obtener_color() != ficha.obtener_color() and len(self.__board__[destino]) == 1:
                capturada = self.__board__[destino].pop()
                capturada.mover('bar')
                self.__bar__[capturada.obtener_color()].append(capturada)

        ficha.mover(destino)
        self.__board__[destino].append(ficha)

    def obtener_bar(self):
        return {c: list(lst) for c, lst in self.__bar__.items()}

    def __str__(self):
        estado = []
        for i, casilla in enumerate(self.__board__):
            estado.append(f"{i}: {[f.obtener_color()[0] for f in casilla]}")
        return " | ".join(estado)



