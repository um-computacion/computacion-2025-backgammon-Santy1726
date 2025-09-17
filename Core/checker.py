class Checker:
    def __init__(self, color: str, posicion: int):

        self.__color__ = color
        self.__posicion__ = posicion

    def mover(self, nueva_posicion: int):
    
        self.__posicion__ = nueva_posicion

    def esta_fuera(self) -> bool:   
        
        return self.__posicion__ == 'off'

    def obtener_color(self) -> str:
    
        return self.__color__

    def obtener_posicion(self) -> int:
  
        return self.__posicion__

    def __str__(self):
     
        return f"Ficha {self.__color__} en {self.__posicion__}"
