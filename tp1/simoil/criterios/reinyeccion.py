from abc import ABCMeta, abstractmethod

class CriterioDeReinyeccion(metaclass=ABCMeta):

    @abstractmethod
    def decidir_venta_de_gas(self, estado):
        pass

    @abstractmethod
    def hay_que_reinyectar(self, estado):
        pass

    @abstractmethod
    def reinyectar(self, estado):
        pass


class CriterioReinyeccionSoloAguaEnTanques(CriterioDeReinyeccion):
    def __init__(self, presion):
        self.presion_critica = presion

    def decidir_venta_de_gas(self, estado):
        for tanque in estado.tanquesDeGasDisponibles:
            estado.venderGas(tanque.volumenAlmacenado)

    def hay_que_reinyectar(self, estado):
        for pozo in estado.yacimiento.pozosPerforados:
            if pozo.presionActual(estado) < self.presion_critica:
                return True
        return False


    def reinyectar(self, estado):
        volumen_total_agua_almacenada = 0

        # TODO: checkear el limite de reinyeccion de agua

        for tanque in estado.tanquesDeAguaDisponibles:
            volumen_total_agua_almacenada += tanque.volumenAlmacenado
            tanque.retirarVolumen(tanque.volumenAlmacenado)

        estado.yacimiento.reinyectar( volumen_total_agua_almacenada, 0)
