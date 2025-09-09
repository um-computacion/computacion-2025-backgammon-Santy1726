class Checker:
    def __init__(self, color, posicion):

        self.__color__ = color
        self.__posicion__ = posicion

    def mover(self, nueva_posicion):
    
        self.__posicion__ = nueva_posicion

    def esta_fuera(self):
        
        return self.__posicion__ == 'off'

    def obtener_color(self):
    
        return self.__color__

    def obtener_posicion(self):
  
        return self.__posicion__

    def __str__(self):
     
        return f"Ficha {self.__color__} en {self.__posicion__}"
