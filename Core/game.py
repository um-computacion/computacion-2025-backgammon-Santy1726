import os
from typing import Optional, Tuple

from Core.dice import Dice
from Core.board import Board
from Core.player import Player


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self, jugador1: Player, jugador2: Player, lados_dado: int = 6):
        self.__dice__ = Dice(lados_dado)
        self.__board__ = Board()
        self.__jugadores__ = [jugador1, jugador2]
        self.__jugadores__[0].asignar_turno(True)
        self.__jugadores__[1].asignar_turno(False)
        self.__ultima_tirada__ = None

    def __obtener_jugador_actual__(self) -> Player:
        return next(j for j in self.__jugadores__ if j.tiene_turno())

    def __cambiar_turno__(self):
        for j in self.__jugadores__:
            j.asignar_turno(not j.tiene_turno())

    # ---------------------------
    # Utilidades para capturas y BAR
    # ---------------------------
    def __oponente__(self, jugador: Player) -> Player:
        return next(j for j in self.__jugadores__ if j != jugador)

    def __bar_snapshot__(self):
        """Devuelve copia de conteo de bar para ambos colores."""
        bar = self.__board__.obtener_bar()
        return {c: len(lst) for c, lst in bar.items()}

    def __detectar_y_procesar_captura_por_bar__(self, jugador: Player, bar_before: dict, bar_after: dict, modo:str="consola"):
        """
        Si el conteo en la BAR del oponente aumentó, hubo captura:
        - sumamos captura al atacante
        - le restamos pieza al defensor
        - mostramos mensaje apropiado según modo
        """
        oponente = self.__oponente__(jugador)

        if bar_after[oponente.obtener_color()] > bar_before[oponente.obtener_color()]:
            jugador.capturar()
            oponente.perder_pieza()
            msg = f"🎯 ¡{jugador.obtener_nombre()} capturó una ficha de {oponente.obtener_nombre()}!"
            if modo == "consola":
                print(msg)
                print(f"Fichas en BAR → Blancas: {bar_after['blanco']} | Negras: {bar_after['negro']}")
            return True
        return False

    # ---------------------------
    # Reglas auxiliares (bearing off)
    # ---------------------------
    def __home_range__(self, color: str) -> range:
        """Devuelve el rango de indices que conforman la 'home' del color."""
        return range(18, 24) if color == "blanco" else range(0, 6)

    def __todas_en_home__(self, color: str) -> bool:
        """Devuelve True si todas las fichas del color están en su home o 'off'."""
        tablero = self.__board__.obtener_tablero()
        for idx, casilla in enumerate(tablero):
            for ficha in casilla:
                if ficha.obtener_color() == color and idx not in self.__home_range__(color):
                    return False
        
        if self.__board__.jugador_tiene_fichas_en_bar(color):
            return False
        return True

    def __puede_bear_off__(self, origen: int, tirada: int, color: str) -> bool:
        """Comprueba si desde 'origen' y con 'tirada' se puede sacar la ficha."""
        if not self.__todas_en_home__(color):
            return False

        if color == "blanco":
            destino = origen + tirada
    
            if destino == 24:
                return True
            if destino > 24:
                
                tablero = self.__board__.obtener_tablero()
                for i in range(origen + 1, 24):
                    for f in tablero[i]:
                        if f.obtener_color() == color:
                            return False
                return True
        else:  # negro
            destino = origen - tirada
            if destino == -1:
                return True
            if destino < -1:
                tablero = self.__board__.obtener_tablero()
                for i in range(0, origen):
                    for f in tablero[i]:
                        if f.obtener_color() == color:
                            return False
                return True
        return False

    def __hacer_bear_off__(self, origen: int, jugador: Player):
        """Saca la ficha del tablero y la marca como 'off'."""
        tablero = self.__board__.obtener_tablero()
        if not (0 <= origen < 24):
            raise IndexError("Origen fuera de rango para bearing off.")

        if not tablero[origen]:
            raise ValueError("No hay ficha en el origen para sacar.")

        ficha = tablero[origen].pop()
        ficha.mover("off")
        
        jugador.perder_pieza()

    # ---------------------------
    # Turno en consola
    # ---------------------------
    def __turno_consola__(self):
        jugador = self.__obtener_jugador_actual__()
        print(f"\nTurno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
        tirada = self.__dice__.tirar()
        print(f"Tirada: {tirada}")

    
        if self.__board__.jugador_tiene_fichas_en_bar(jugador.obtener_color()):
            print("⚠️ Debes reingresar una ficha desde la BAR.")
            destino = tirada if jugador.obtener_color() == "blanco" else 23 - tirada
            bar_before = self.__bar_snapshot__()
            try:
                self.__board__.reingresar_ficha(destino, jugador.obtener_color())
                jugador.agregar_movimiento("bar", destino)
                bar_after = self.__bar_snapshot__()
                self.__detectar_y_procesar_captura_por_bar__(jugador, bar_before, bar_after, modo="consola")
            except Exception as e:
                print(f"❌ No puedes reingresar: {e}. Pierdes el turno.")
            self.__cambiar_turno__()
            return

        while True:
            try:
                raw = input("Elige posición de origen (0-23) o 'q' para salir: ")
                if raw.strip().lower() == 'q':
                    raise KeyboardInterrupt
                origen = int(raw)
                destino = origen + tirada if jugador.obtener_color() == "blanco" else origen - tirada

                
                if not (0 <= destino < 24):
                    if self.__puede_bear_off__(origen, tirada, jugador.obtener_color()):
                        self.__hacer_bear_off__(origen, jugador)
                        jugador.agregar_movimiento(origen, "off")
                        print("✅ Sacaste una ficha (bearing off).")
                        break
                    else:
                        raise ValueError("No se puede sacar esa ficha (no cumple reglas de bearing off).")

                
                bar_before = self.__bar_snapshot__()
                self.__board__.mover_ficha(origen, destino, jugador.obtener_color())
                jugador.agregar_movimiento(origen, destino)
                bar_after = self.__bar_snapshot__()

                self.__detectar_y_procesar_captura_por_bar__(jugador, bar_before, bar_after, modo="consola")
                break

            except KeyboardInterrupt:
                print("Saliendo del juego.")
                return "quit"
            except Exception as e:
                print(f"❌ Error: {e}. Intenta de nuevo.")

        
        if self.__board__.juego_terminado(jugador.obtener_color()):
            limpiar_pantalla()
            print(self.__board__)
            print(f"🏆 ¡{jugador.obtener_nombre()} ha ganado la partida! 🏆")
            return "quit"

        self.__cambiar_turno__()

    # ---------------------------
    # Juego en consola (público)
    # ---------------------------
    def jugar_consola(self):
        print("¡Bienvenido al juego (modo consola)!")
        try:
            while True:
                limpiar_pantalla()
                print(self.__board__)
                for j in self.__jugadores__:
                    print(j)
                res = self.__turno_consola__()
                if res == "quit":
                    break
        except KeyboardInterrupt:
            print("\nJuego terminado por interrupción.")

    # ---------------------------
    # MODO PYGAME (básico, funcional)
    # ---------------------------
    def jugar_pygame(self, ancho: int = 1000, alto: int = 600):
        """
        Modo gráfico con pygame. Interfaz básica:
        - Presionar SPACE para tirar el dado.
        - Clic izquierdo para seleccionar origen y luego destino.
        - Si hay fichas en BAR, el modo obliga a reingresar.
        - Soporta bearing off.
        """
        try:
            import pygame
        except Exception as e:
            raise RuntimeError("Pygame no está instalado. Instálalo con `pip install pygame`.") from e

        pygame.init()
        screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Backgammon - Modo Pygame (básico)")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 20)

        tablero_visual = self.__board__.obtener_tablero()

        seleccion_origen: Optional[int] = None
        jugador = self.__obtener_jugador_actual__()
        tirada_actual: Optional[int] = None
        mensaje = "Presiona SPACE para tirar el dado."

        def dibujar_tablero():
            screen.fill((200, 170, 120))
            w = ancho
            h = alto
            mid_x = w // 2
            margin = 40
            tri_w = (w - 2 * margin) // 12
        
            for i in range(12):
                idx = 12 + i
                x = margin + i * tri_w
                points = [(x, 60), (x + tri_w, 60), (x + tri_w // 2, 200)]
                pygame.draw.polygon(screen, (80, 40, 0) if (i % 2 == 0) else (220, 200, 150), points)
                label = font.render(str(idx), True, (0, 0, 0))
                screen.blit(label, (x + tri_w // 2 - 8, 30))

            
            for i in range(12):
                idx = 11 - i
                x = margin + i * tri_w
                points = [(x, h - 60), (x + tri_w, h - 60), (x + tri_w // 2, h - 200)]
                pygame.draw.polygon(screen, (80, 40, 0) if (i % 2 == 0) else (220, 200, 150), points)
                label = font.render(str(idx), True, (0, 0, 0))
                screen.blit(label, (x + tri_w // 2 - 8, h - 30))

            
            for col, stack in enumerate(tablero_visual[12:24]):
                x = margin + col * tri_w + tri_w // 2
                for depth, f in enumerate(stack):
                    y = 100 + depth * 18
                    color = (255, 255, 255) if f.obtener_color() == "blanco" else (0, 0, 0)
                    pygame.draw.circle(screen, color, (x, y), 8)
          
            for col, stack in enumerate(reversed(tablero_visual[0:12])):
                x = margin + col * tri_w + tri_w // 2
                for depth, f in enumerate(stack):
                    y = h - 100 - depth * 18
                    color = (255, 255, 255) if f.obtener_color() == "blanco" else (0, 0, 0)
                    pygame.draw.circle(screen, color, (x, y), 8)

            status = f"Turno: {self.__obtener_jugador_actual__().obtener_nombre()} ({self.__obtener_jugador_actual__().obtener_color()})"
            screen.blit(font.render(status, True, (0, 0, 0)), (10, 10))
            screen.blit(font.render(mensaje, True, (0, 0, 0)), (10, 30))
            if tirada_actual:
                screen.blit(font.render(f"Tirada: {tirada_actual}", True, (0, 0, 0)), (10, 50))

            # Mostrar BAR en pantalla
            bar = self.__board__.obtener_bar()
            screen.blit(font.render(f"BAR - Blancas: {len(bar['blanco'])}  Negras: {len(bar['negro'])}", True, (0,0,0)), (10, 70))

            pygame.display.flip()

        running = True
        while running:
            jugador = self.__obtener_jugador_actual__()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tirada_actual = self.__dice__.tirar()
                        self.__ultima_tirada__ = tirada_actual
                        mensaje = f"Tiraste {tirada_actual}. Seleccioná origen."
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    # Convertir posición x a índice aproximado (very simple mapping)
                    margin = 40
                    tri_w = (ancho - 2 * margin) // 12
                    if my < alto // 2:
                        # zona superior: indices 12..23
                        col = (mx - margin) // tri_w
                        if 0 <= col < 12:
                            idx = 12 + col
                        else:
                            idx = None
                    else:
                        col = (mx - margin) // tri_w
                        if 0 <= col < 12:
                            idx = 11 - col
                        else:
                            idx = None

                    if idx is None:
                        continue

                    # Si hay fichas en bar, solo reingreso con la tirada
                    if self.__board__.jugador_tiene_fichas_en_bar(jugador.obtener_color()):
                        if tirada_actual is None:
                            mensaje = "Primero tirá el dado (SPACE) para reingresar."
                            continue
                        destino = tirada_actual if jugador.obtener_color() == "blanco" else 23 - tirada_actual
                        bar_before = self.__bar_snapshot__()
                        try:
                            self.__board__.reingresar_ficha(destino, jugador.obtener_color())
                            jugador.agregar_movimiento("bar", destino)
                            bar_after = self.__bar_snapshot__()
                            # detectar captura por reingreso
                            if self.__detectar_y_procesar_captura_por_bar__(jugador, bar_before, bar_after, modo="pygame"):
                                mensaje = f"{jugador.obtener_nombre()} capturó al reingresar."
                            else:
                                mensaje = "Ficha reingresada."
                            tirada_actual = None
                            self.__cambiar_turno__()
                        except Exception as e:
                            mensaje = f"No se pudo reingresar: {e}"
                        continue

                   
                    if seleccion_origen is None:
                        # seleccionar origen
                        # validar que en idx haya una ficha del jugador
                        tab = self.__board__.obtener_tablero()
                        if not (0 <= idx < 24) or not tab[idx]:
                            mensaje = "Origen vacío. Elegí otro."
                            continue
                        if tab[idx][-1].obtener_color() != jugador.obtener_color():
                            mensaje = "No puedes seleccionar ficha contraria."
                            continue
                        seleccion_origen = idx
                        mensaje = f"Origen seleccionado: {idx}. Ahora elegí destino (clic)."
                    else:
                    
                        if tirada_actual is None:
                            mensaje = "Primero tirá el dado (SPACE) para mover."
                            seleccion_origen = None
                            continue

                        origen = seleccion_origen
                        destino = seleccion_origen + tirada_actual if jugador.obtener_color() == "blanco" else seleccion_origen - tirada_actual

                        try:
                          
                            if not (0 <= destino < 24):
                                if self.__puede_bear_off__(origen, tirada_actual, jugador.obtener_color()):
                                    self.__hacer_bear_off__(origen, jugador)
                                    jugador.agregar_movimiento(origen, "off")
                                    mensaje = "Saque una ficha (bearing off)."
                                else:
                                    raise ValueError("No se puede sacar esa ficha (regla de bearing off).")
                            else:
                                bar_before = self.__bar_snapshot__()
                                self.__board__.mover_ficha(origen, destino, jugador.obtener_color())
                                jugador.agregar_movimiento(origen, destino)
                                bar_after = self.__bar_snapshot__()
                                if self.__detectar_y_procesar_captura_por_bar__(jugador, bar_before, bar_after, modo="pygame"):
                                    mensaje = f"{jugador.obtener_nombre()} capturó una ficha!"
                                else:
                                    mensaje = f"Moviste {origen} → {destino}."
                            
                            if self.__board__.juego_terminado(jugador.obtener_color()):
                                mensaje = f"¡{jugador.obtener_nombre()} ganó!"
                                running = False
                            tirada_actual = None
                            seleccion_origen = None
                            self.__cambiar_turno__()
                        except Exception as e:
                            mensaje = f"Error al mover: {e}"
                            seleccion_origen = None

            dibujar_tablero()
            clock.tick(30)

        pygame.quit()

    # ---------------------------
    # API pública simple: elije modo
    # ---------------------------
    def jugar(self, modo: str = "consola"):
        """
        Inicia el juego en el modo especificado:
        - "consola" (por defecto)
        - "pygame"
        """
        modo = modo.strip().lower()
        if modo == "pygame":
            self.jugar_pygame()
        else:
            self.jugar_consola()
