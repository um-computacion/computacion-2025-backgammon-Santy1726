import unittest
from Core.board import Board

class TestTablero(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_crear_board(self):
        board_esperado = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        self.assertEqual(self.board.obtener_board(), board_esperado)

    def test_establecer_posicion(self):
        self.board.establecer_posicion(0, 3)
        self.assertEqual(self.board.obtener_posicion(0), 3)
        self.board.establecer_posicion(5, -2)
        self.assertEqual(self.board.obtener_posicion(5), -2)