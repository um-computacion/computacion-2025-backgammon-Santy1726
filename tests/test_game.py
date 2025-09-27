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


if __name__ == "__main__":
    unittest.main()

