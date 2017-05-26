from abc import ABCMeta, abstractmethod

class CriterioDeReinyeccion(metaclass=ABCMeta):

    @abstractmethod
    def decidir_venta_de_gas(self, estado):
        pass

    @abstractmethod
    def decidir_reinyeccion(self, estado):
        pass


class CriterioReinyeccionSoloAguaEnTanques(CriterioDeReinyeccion):
    def __init__(self, presion):
        self.presion_critica = presion

    def decidir_venta_de_gas(self, estado):
        for tanque in estado.tanquesDeGasDisponibles:
            estado.venderGas(tanque.volumenAlmacenado)

    def decidir_reinyeccion(self, estado):
        hay_que_reinyectar = False
        for pozo in estado.yacimiento.pozosPerforados:
            if pozo.presionActual < self.presion_critica:
                hay_que_reinyectar = True

        if hay_que_reinyectar:
            volumen_total_agua_almacenada = 0

            # TODO: checkear el limite de reinyeccion de agua

            for tanque in estado.tanquesDeAguaDisponibles:
                volumen_total_agua_almacenada += tanque.volumenAlmacenado
                tanque.retirarVolumen(tanque.volumenAlmacenado)

            estado.yacimiento.reinyectar( volumen_total_agua_almacenada, 0)

