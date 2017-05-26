from abc import ABCMeta, abstractmethod

from excavacion import Excavacion

class CriterioEleccionParcelas(metaclass=ABCMeta):

    @abstractmethod
    def decidir_proximas_parcelas(self, estado):
        pass


class EleccionParcelasMayorPresion(CriterioEleccionParcelas):
    def __init__(self, n_parcelas):
        self.n_parcelas = int(n_parcelas)
        self.n_parcelas_seleccionadas = 0

    def decidir_proximas_parcelas(self, estado):
        if self.n_parcelas_seleccionadas == self.n_parcelas:
            return

        parcelas_seleccionadas = sorted(
                estado.yacimiento.parcelasDelYacimiento,
                key=lambda parcela: parcela.presionInicial, reverse=True) \
            [:self.n_parcelas]

        self.n_parcelas_seleccionadas = len(parcelas_seleccionadas)

        for parcela in parcelas_seleccionadas:
            estado.excavacionesActuales.append(Excavacion(parcela))

