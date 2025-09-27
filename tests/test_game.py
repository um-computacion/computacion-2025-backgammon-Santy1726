import unittest
from unittest.mock import patch
from Core.game import Game
from Core.player import Player
from Core.checker import Checker


class TestGame(unittest.TestCase):

    def setUp(self):
        self.j1 = Player("Alice", "blanco")
        self.j2 = Player("Bob", "negro")
        self.game = Game(self.j1, self.j2)

    def test_inicializacion(self):
        self.assertIsNotNone(self.game.__dice__)
        self.assertIsNotNone(self.game.__board__)
        self.assertEqual(len(self.game.__jugadores__), 2)
        self.assertTrue(self.j1.__turno__)
        self.assertFalse(self.j2.__turno__)

    def test_obtener_jugador_actual(self):
        actual = self.game.__obtener_jugador_actual__()
        self.assertEqual(actual, self.j1)

        self.game.__cambiar_turno__()
        actual = self.game.__obtener_jugador_actual__()
        self.assertEqual(actual, self.j2)

    @patch("builtins.input", side_effect=["0"])
    @patch("Core.dice.Dice.tirar", return_value=1)
    def test_turno_realiza_movimiento(self, mock_dice, mock_input):
        self.game.__board__.__board__[0] = [Checker("blanco", 0)]

        self.game.__turno__()

        self.assertIn((0, 1), self.j1.__movimientos__)

        self.assertTrue(self.j2.__turno__)
        self.assertFalse(self.j1.__turno__)

    def test_mover_ficha_valido(self):
        self.game.__board__.__board__[0] = [Checker("blanco", 0)]
        self.game.__board__.mover_ficha(0, 3)

        self.assertEqual(len(self.game.__board__.__board__[0]), 0)
        self.assertEqual(len(self.game.__board__.__board__[3]), 1)
        self.assertEqual(self.game.__board__.__board__[3][0].obtener_posicion(), 3)

    def test_mover_ficha_fuera_de_rango(self):
        with self.assertRaises(IndexError):
            self.game.__board__.mover_ficha(-1, 30)

    def test_mover_ficha_sin_fichas(self):
        with self.assertRaises(ValueError):
            self.game.__board__.mover_ficha(2, 3)

    def test_str_de_jugador(self):
        texto = str(self.j1)
        self.assertIn("Jugador: Alice", texto)
        self.assertIn("Color: blanco", texto)

    def test_captura_y_devolucion_de_pieza(self):
        piezas_iniciales = self.j1.__piezas__
        self.j1.perder_pieza()
        self.assertEqual(self.j1.__piezas__, piezas_iniciales - 1)

        self.j1.devolver_pieza()
        self.assertEqual(self.j1.__piezas__, piezas_iniciales)

    def test_registrar_movimiento(self):
        self.j1.agregar_movimiento(5, 10)
        self.assertIn((5, 10), self.j1.__movimientos__)

    def test_dado(self):
        dado = self.game.__dice__
        valor = dado.tirar()
        self.assertTrue(1 <= valor <= 6)

        valores = dado.tirar_varias(5)
        self.assertEqual(len(valores), 5)
        for v in valores:
            self.assertTrue(1 <= v <= 6)



if __name__ == "__main__":
    unittest.main()

