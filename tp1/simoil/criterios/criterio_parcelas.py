from abc import ABCMeta

class CriterioEleccionParcelas(metaclass=ABCMeta):

    @abstractmethod
    def decidir_proximas_parcelas(self, estado_de_simulacion):
        pass


class EleccionParcelasMayorPresion(CriterioEleccionParcelas):
    def __init__(self, n_parcelas):
        self.n_parcelas = n_parcelas
        self.n_parcelas_seleccionadas = 0

    def decidir_proximas_parcelas(self, estado_de_simulacion):
        if n_parcelas_seleccionadas == n_parcelas:
            return
        parcelas_seleccionadas = sorted(estado_de_simulacion.yacimiento.parcelas(),
                                        key=lambda parcela: parcela.presion, reverse=True)[-n_parcelas:]
        n_parcelas_seleccionadas = len(parcelas_seleccionadas)

        for parcela in parcelas_seleccionadas:
            estado_de_simulacion.excavaciones_actuales.append(Excavacion(parcela))
