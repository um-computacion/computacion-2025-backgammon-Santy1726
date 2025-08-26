import random

class Dice:
    def __init__(self, lados=6):
        self.__lados__ = lados

    def tirar(self):
        return random.randint(1, self.__lados__)