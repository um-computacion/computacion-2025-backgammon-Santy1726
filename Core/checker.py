class Checker:
    def __init__(self, color: str, posicion):
        if color not in ("blanco", "negro"):
            raise ValueError("color debe ser 'blanco' o 'negro'")
        if not (isinstance(posicion, int) and 0 <= posicion < 24) and posicion not in ("off", "bar"):
            raise TypeError("posicion debe ser int 0-23 o 'off'/'bar'")
        self.__color__ = color
        self.__posicion__ = posicion

    def mover(self, nueva_posicion):
        if not (isinstance(nueva_posicion, int) and 0 <= nueva_posicion < 24) and nueva_posicion not in ("off", "bar"):
            raise TypeError("nueva_posicion debe ser int 0-23 o 'off'/'bar'")
        self.__posicion__ = nueva_posicion

    def esta_fuera(self) -> bool:
        return self.__posicion__ == "off"

    def obtener_color(self) -> str:
        return self.__color__

    def obtener_posicion(self):
        return self.__posicion__

    def __int__(self):
        if isinstance(self.__posicion__, int):
            return self.__posicion__
        raise TypeError("No se puede convertir a int: la ficha está fuera")

    def __str__(self):
        return f"Ficha {self.__color__} en {self.__posicion__}"