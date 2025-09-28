from Core.dice import Dice
from Core.board import Board
from Core.player import Player

class Game:
    def __init__(self, jugador1: Player, jugador2: Player, lados_dado: int = 6):
        self.__dice__ = Dice(lados_dado)
        self.__board__ = Board()
        self.__jugadores__ = [jugador1, jugador2]
        self.__jugadores__[0].asignar_turno(True)
        self.__jugadores__[1].asignar_turno(False)

    def __obtener_jugador_actual__(self) -> Player:
        return next(j for j in self.__jugadores__ if j.tiene_turno())

    def __cambiar_turno__(self):
        for j in self.__jugadores__:
            j.asignar_turno(not j.tiene_turno())

    def __turno__(self):
        jugador = self.__obtener_jugador_actual__()
        print(f"\nTurno de {jugador}")

        tirada = self.__dice__.tirar()
        print(f"Tirada: 🎲 {tirada}")

        while True:
            try:
                raw = input("Elige posición de origen (0-23) o 'q' para salir: ")
                if raw.strip().lower() == 'q':
                    raise KeyboardInterrupt
                origen = int(raw)
                destino = origen + tirada if jugador.obtener_color() == "blanco" else origen - tirada
                self.__board__.mover_ficha(origen, destino)
                jugador.agregar_movimiento(origen, destino)
                break
            except KeyboardInterrupt:
                print("Saliendo del juego.")
                return "quit"
            except Exception as e:
                print(f"❌ Error: {e}. Intenta de nuevo.")

        self.__cambiar_turno__()

    def __mostrar_estado__(self):
        print("\n=== Estado del tablero ===")
        print(self.__board__)
        for j in self.__jugadores__:
            print(j)

    def jugar(self):
        print("¡Bienvenido al juego!")
        try:
            while True:
                self.__mostrar_estado__()
                res = self.__turno__()
                if res == "quit":
                    break
        except KeyboardInterrupt:
            print("Juego terminado por interrupción.")
