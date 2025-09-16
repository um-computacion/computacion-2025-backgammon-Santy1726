import unittest

from Core.dice import Dice

class TestDice(unittest.TestCase):

    def test_creacion_valida(self):
        d = Dice(6)
        self.assertEqual(str(d), "Dado de 6 lados")

    def test_creacion_invalida(self):
        with self.assertRaises(ValueError):
            Dice(1) 

    def test_tirada_valida(self):
        d = Dice(6)
        resultado = d.tirar()
        self.assertTrue(1 <= resultado <= 6)

    def test_tirar_varias(self):
        d = Dice(6)
        resultados = d.tirar_varias(5)
        self.assertEqual(len(resultados), 5)
        for r in resultados:
            self.assertTrue(1 <= r <= 6)

    def test_tirar_varias_invalido(self):
        d = Dice(6)
        with self.assertRaises(ValueError):
            d.tirar_varias(0)

if __name__ == "__main__":
    unittest.main()
