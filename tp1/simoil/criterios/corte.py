from abc import ABCMeta, abstractmethod

class CriterioDeCorte(metaclass=ABCMeta):

    @abstractmethod
    def cortar(self, estado_de_simulacion):
        pass


class CortePorDiaFijo(CriterioDeCorte):
    def __init__(self, dia_de_corte):
        self._dia_de_corte = dia_de_corte

    def cortar(self, estado_de_simulacion):
        return estado_de_simulacion.diaNumero() >= dia_de_corte
