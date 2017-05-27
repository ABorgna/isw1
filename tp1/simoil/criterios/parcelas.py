from abc import ABCMeta, abstractmethod

from excavacion import Excavacion

class CriterioEleccionParcelas(metaclass=ABCMeta):

    @abstractmethod
    def decidir_proximas_parcelas(self, estado):
        pass


class EleccionParcelasMayorPresion(CriterioEleccionParcelas):
    def __init__(self, n_parcelas):
        self.n_parcelas = int(n_parcelas)

    def decidir_proximas_parcelas(self, estado):
        if estado.diaNumero == 1:
            parcelas_seleccionadas = sorted(
                estado.yacimiento.parcelasDelYacimiento,
                key=lambda parcela: parcela.presionInicial, reverse=True) \
                [:self.n_parcelas]

            for parcela in parcelas_seleccionadas:
                estado.agregarExcavacion(Excavacion(parcela))
