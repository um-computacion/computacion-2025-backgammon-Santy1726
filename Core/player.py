class Player:
    def __init__(self, nombre: str, color: str, piezas: int = 15):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__piezas__ = piezas
        self.__capturadas__ = 0
        self.__turno__ = False
        self.__movimientos__ = []

    def obtener_movimientos(self):
        return self.__movimientos__

    def obtener_capturadas(self) -> int:
        return self.__capturadas__

    def asignar_turno(self, turno: bool):
        self.__turno__ = turno

    def agregar_movimiento(self, origen: int, destino: int):
        self.__movimientos__.append((origen, destino))

    def perder_pieza(self):
        if self.__piezas__ > 0:
            self.__piezas__ -= 1
        else:
            raise ValueError("El jugador no tiene más piezas.")

    def capturar(self):
        self.__capturadas__ += 1

    def devolver_pieza(self):
        self.__piezas__ += 1

    def tiene_turno(self) -> bool:
        return self.__turno__

    def obtener_color(self) -> str:
        return self.__color__

    def __str__(self):
        return (f"Jugador: {self.__nombre__} | Color: {self.__color__} | "
                f"Piezas: {self.__piezas__} | Capturadas: {self.__capturadas__} | "
                f"Turno: {'Sí' if self.__turno__ else 'No'}")
