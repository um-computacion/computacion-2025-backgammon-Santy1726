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
        self.assertIsNotNone(self.game._Game__dice__)
        self.assertIsNotNone(self.game._Game__board__)
        self.assertEqual(len(self.game._Game__jugadores__), 2)
        self.assertTrue(self.j1.obtener_turno())
        self.assertFalse(self.j2.obtener_turno())

    def test_obtener_jugador_actual(self):
        actual = self.game._Game__obtener_jugador_actual__()
        self.assertEqual(actual, self.j1)

        self.game._Game__cambiar_turno__()
        actual = self.game._Game__obtener_jugador_actual__()
        self.assertEqual(actual, self.j2)

    @patch("Core.dice.Dice.tirar", return_value=1)   # 👈 Patch corregido
    @patch("builtins.input", side_effect=["0"])      # 👈 Simulamos origen=0
    def test_turno_realiza_movimiento(self, mock_input, mock_dice):
        # Metemos una ficha Checker en la posición 0
        self.game._Game__board__._Board__board__[0] = [Checker("blanco", 0)]

        # Ejecutamos un turno
        self.game._Game__turno__()

        # El jugador 1 debería haber movido de 0 a 1
        self.assertIn((0, 1), self.j1.obtener_movimientos())

        # Y ahora debería ser turno del jugador 2
        self.assertTrue(self.j2.obtener_turno())
        self.assertFalse(self.j1.obtener_turno())

if __name__ == "__main__":
    unittest.main()

