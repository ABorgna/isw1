from abc import ABCMeta, abstractmethod

class CriterioDeCorte(metaclass=ABCMeta):

    @abstractmethod
    def cortar(self, estado):
        pass


class CortePorDiaFijo(CriterioDeCorte):
    def __init__(self, dia_de_corte):
        self._dia_de_corte = dia_de_corte

    def cortar(self, estado):
        return estado.diaNumero >= self._dia_de_corte and estado.configuracion.concentracionCritica <= estado.yacimiento.composicion.ratioDePetroleo
