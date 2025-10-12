import unittest
from Core.checker import Checker  

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.checker = Checker("blanco", 5)  # color válido

    def test_obtener_color(self):
        self.assertEqual(self.checker.obtener_color(), "blanco")

    def test_obtener_posicion(self):
        self.assertEqual(self.checker.obtener_posicion(), 5)

    def test_mover_valido(self):
        self.checker.mover(10)
        self.assertEqual(self.checker.obtener_posicion(), 10)

    def test_mover_fuera_del_tablero(self):
        with self.assertRaises(TypeError):
            self.checker.mover("casa")

    def test_esta_fuera_false(self):
        self.assertFalse(self.checker.esta_fuera())

    def test_esta_fuera_true(self):
        self.checker.mover("off")
        self.assertTrue(self.checker.esta_fuera())

    def test_str(self):
        self.assertEqual(str(self.checker), "Ficha blanco en 5")

    def test_int_conversion(self):
        self.assertEqual(int(self.checker), 5)

    def test_color_invalido(self):
        with self.assertRaises(ValueError):
            Checker("rojo", 3)  # color no permitido

    def test_posicion_invalida(self):
        with self.assertRaises(TypeError):
            Checker("blanco", "inicio")  # posición no válida


if __name__ == "__main__":
    unittest.main()
