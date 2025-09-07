import unittest
from Core.player import Player

class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = Player("Jose", "Rojo")

    def test_initial_values(self):
        self.assertEqual(self.player.obtener_nombre(), "Jose")
        self.assertEqual(self.player.obtener_color(), "Rojo")
        self.assertEqual(self.player.obtener_piezas(), 15)
        self.assertFalse(self.player.obtener_turno())
        self.assertEqual(self.player.obtener_movimientos(), [])
        self.assertEqual(self.player.obtener_capturadas(), 0)

    def test_asignar_turno(self):
        self.player.asignar_turno(True)
        self.assertTrue(self.player.obtener_turno())
        self.player.asignar_turno(False)
        self.assertFalse(self.player.obtener_turno())

    def test_agregar_movimiento(self):
        self.player.agregar_movimiento(1, 5)
        self.assertIn((1, 5), self.player.obtener_movimientos())

    def test_perder_pieza(self):
        initial_piezas = self.player.obtener_piezas()
        self.player.perder_pieza()
        self.assertEqual(self.player.obtener_piezas(), initial_piezas - 1)

    def test_perder_pieza_no_negative(self):
        for _ in range(15):
            self.player.perder_pieza()
        with self.assertRaises(ValueError):
            self.player.perder_pieza()

    def test_capturar(self):
        initial_capturadas = self.player.obtener_capturadas()
        self.player.capturar()
        self.assertEqual(self.player.obtener_capturadas(), initial_capturadas + 1)

    def test_devolver_pieza(self):
        initial_piezas = self.player.obtener_piezas()
        self.player.devolver_pieza()
        self.assertEqual(self.player.obtener_piezas(), initial_piezas + 1)

    def test_str_representation(self):
        expected_str = ("Jugador: Jose | Color: Rojo | Piezas: 15 | Capturadas: 0 | Turno: No")
        self.assertEqual(str(self.player), expected_str)

if __name__ == '__main__':
    unittest.main()