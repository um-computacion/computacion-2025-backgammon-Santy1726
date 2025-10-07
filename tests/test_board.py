import unittest
from Core.board import Board
from Core.checker import Checker


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_inicializacion_correcta(self):
        self.assertEqual(len(self.board.__board__), 24)

        self.assertEqual(len(self.board.__board__[0]), 2)
        self.assertEqual(len(self.board.__board__[5]), 5)
        self.assertEqual(len(self.board.__board__[7]), 3)
        self.assertEqual(len(self.board.__board__[11]), 5)
        self.assertEqual(len(self.board.__board__[12]), 5)
        self.assertEqual(len(self.board.__board__[16]), 3)
        self.assertEqual(len(self.board.__board__[18]), 5)
        self.assertEqual(len(self.board.__board__[23]), 2)

    def test_mover_ficha_valido(self):
        self.board.__board__[2] = [Checker("blanco", 2)]
        self.board.mover_ficha(2, 3)

        self.assertEqual(len(self.board.__board__[2]), 0)
        self.assertEqual(len(self.board.__board__[3]), 1)
        self.assertEqual(self.board.__board__[3][0].obtener_posicion(), 3)

    def test_mover_ficha_sin_fichas(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(2, 3)

    def test_mover_ficha_fuera_de_rango(self):
        with self.assertRaises(IndexError):
            self.board.mover_ficha(-1, 2)

        with self.assertRaises(IndexError):
            self.board.mover_ficha(0, 25)

    def test_captura_simple(self):
        self.board.__board__[0] = [Checker("blanco", 0)]
        self.board.__board__[1] = [Checker("negro", 1)]

        self.board.mover_ficha(0, 1)

        bar_negro = self.board.__bar__["negro"]
        self.assertEqual(len(bar_negro), 1)
        self.assertEqual(bar_negro[0].obtener_color(), "negro")
        self.assertEqual(bar_negro[0].obtener_posicion(), "bar")

        self.assertEqual(len(self.board.__board__[1]), 1)
        self.assertEqual(self.board.__board__[1][0].obtener_color(), "blanco")

    def test_obtener_posicion_devuelve_copia(self):
        casilla = self.board.obtener_posicion(0)
        casilla.append("modificado")

        self.assertNotIn("modificado", self.board.__board__[0])

    def test_str_representacion(self):
        tablero_str = str(self.board)
        self.assertIn("0:", tablero_str)
        self.assertIn("23:", tablero_str)
        self.assertIsInstance(tablero_str, str)


if __name__ == "__main__":
    unittest.main()
