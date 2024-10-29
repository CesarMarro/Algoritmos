'''
Pokemon object class.
'''

class Pokemon:
    def __init__(self, nombre, tipo, legendario):
        """
        Inicializa un nuevo objeto Pokemon.
        """
        self.nombre = nombre
        self.tipo = tipo
        self.legendario = legendario

    def __repr__(self):
        """
        Representación oficial del objeto Pokemon.
        """
        return f'{self.nombre}'