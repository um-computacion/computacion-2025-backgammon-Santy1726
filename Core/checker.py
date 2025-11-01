class Checker:
    def _init_(self, color: str, posicion):
        if color not in ("blanco", "negro"):
            raise ValueError("color debe ser 'blanco' o 'negro'")
        if not (isinstance(posicion, int) and 0 <= posicion < 24) and posicion not in ("off", "bar"):
            raise TypeError("posicion debe ser int 0-23 o 'off'/'bar'")
        self._color_ = color
        self._posicion_ = posicion

    def mover(self, nueva_posicion):
        if not (isinstance(nueva_posicion, int) and 0 <= nueva_posicion < 24) and nueva_posicion not in ("off", "bar"):
            raise TypeError("nueva_posicion debe ser int 0-23 o 'off'/'bar'")
        self._posicion_ = nueva_posicion

    def esta_fuera(self) -> bool:
        return self._posicion_ == "off"

    def obtener_color(self) -> str:
        return self._color_

    def obtener_posicion(self):
        return self._posicion_

    def _int_(self):
        if isinstance(self._posicion_, int):
            return self._posicion_
        raise TypeError("No se puede convertir a int: la ficha está fuera")

    def _str_(self):
        return f"Ficha {self._color} en {self.posicion_}"

    def _repr_(self):
        return self._str_()