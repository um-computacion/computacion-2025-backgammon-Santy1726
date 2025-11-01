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

    def obtener_tablero(self):
        return self.__board__

    def jugador_tiene_fichas_en_bar(self, color: str) -> bool:
        return len(self.__bar__[color]) > 0

    def reingresar_ficha(self, destino: int, color: str):
        if len(self.__bar__[color]) == 0:
            raise ValueError("No tienes fichas en la BAR para reingresar.")

        ficha = self.__bar__[color].pop()

        if self.__board__[destino]:
            top = self.__board__[destino][-1]
            if top.obtener_color() != color and len(self.__board__[destino]) == 1:
                capturada = self.__board__[destino].pop()
                capturada.mover("bar")
                self.__bar__[capturada.obtener_color()].append(capturada)

        ficha.mover(destino)
        self.__board__[destino].append(ficha)

    def mover_ficha(self, origen: int, destino: int, color: str):
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise IndexError("Índice fuera de rango (0–23).")

        if not self.__board__[origen]:
            raise ValueError("No hay fichas en el punto de origen.")

        ficha = self.__board__[origen][-1]
        if ficha.obtener_color() != color:
            raise ValueError("No puedes mover fichas del color contrario.")

        if self.__board__[destino]:
            top = self.__board__[destino][-1]
            if top.obtener_color() != ficha.obtener_color() and len(self.__board__[destino]) == 1:
                capturada = self.__board__[destino].pop()
                capturada.mover("bar")
                self.__bar__[capturada.obtener_color()].append(capturada)

        self.__board__[origen].pop()
        ficha.mover(destino)
        self.__board__[destino].append(ficha)

    def obtener_bar(self):
        return {c: list(lst) for c, lst in self.__bar__.items()}

    def juego_terminado(self, color: str) -> bool:
        for casilla in self.__board__:
            for ficha in casilla:
                if ficha.obtener_color() == color and not ficha.esta_fuera():
                    return False

        if len(self.__bar__[color]) > 0:
            return False

        return True

    def __str__(self):
        def simbolos(casilla):
            return ["B" if c.obtener_color() == "blanco" else "N" for c in casilla]

        top = [simbolos(c) for c in self.__board__[12:24]]
        bottom = [simbolos(c) for c in reversed(self.__board__[0:12])]

        filas = []
        filas.append("\n" + "=" * 80)
        filas.append("\n               TABLERO DE  BACKGAMMON\n")
        filas.append("=" * 80 + "\n\n")

        filas.append("        " + "".join(f"{i:^4}" for i in range(12, 24)) + "\n")
        filas.append("      +" + "---+" * 12 + "\n")

        for row in range(5):
            fila = "      │"
            for stack in top:
                if len(stack) > row:
                    fila += f" {stack[row]} │"
                else:
                    fila += "   │"
            filas.append(fila + "\n")
        filas.append("      +" + "---+" * 12 + "\n")

        blancas = len(self.__bar__['blanco'])
        negras = len(self.__bar__['negro'])
        filas.append(f"\n        Fichas en BAR → Blancas: {blancas} | Negras: {negras}\n")
        filas.append("      " + "-" * 55 + "\n")

        filas.append("        " + "".join(f"{i:^4}" for i in range(11, -1, -1)) + "\n")
        filas.append("      +" + "---+" * 12 + "\n")

        for row in range(4, -1, -1):
            fila = "      │"
            for stack in bottom:
                if len(stack) > row:
                    fila += f" {stack[row]} │"
                else:
                    fila += "   │"
            filas.append(fila + "\n")
        filas.append("      +" + "---+" * 12 + "\n")
        filas.append("=" * 80 + "\n")

        return "".join(filas)
