import random

class Dice:
    def __init__(self, lados: int = 6):
        if lados < 2:
            raise ValueError("Un dado debe tener al menos 2 lados.")
        self._lados = lados

    def tirar(self) -> int:
        return random.randint(1, self._lados)

    def tirar_varias(self, n: int) -> list[int]:
    
        if n < 1:
            raise ValueError("El número de tiradas debe ser al menos 1.")
        return [self.tirar() for _ in range(n)]

    def __str__(self) -> str:
        return f"Dado de {self._lados} lados"
