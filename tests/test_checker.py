import unittest
from Core.checker import Checker  

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.checker = Checker("rojo", 5)

    def test_obtener_color(self):
        self.assertEqual(self.checker.obtener_color(), "rojo")

    def test_obtener_posicion(self):
        self.assertEqual(self.checker.obtener_posicion(), 5)

    def test_mover(self):
        self.checker.mover(10)
        self.assertEqual(self.checker.obtener_posicion(), 10)

    def test_esta_fuera_false(self):
        self.assertFalse(self.checker.esta_fuera())

    def test_esta_fuera_true(self):
        self.checker.mover("off")
        self.assertTrue(self.checker.esta_fuera())

    def test_str(self):
        self.assertEqual(str(self.checker), "Ficha rojo en 5")

if __name__ == "__main__":
    unittest.main()
