from abc import ABCMeta, abstractmethod

class CriterioDeReinyeccion(metaclass=ABCMeta):

    @abstractmethod
    def decidir_venta_de_gas(self, estado_de_simulacion):
        pass

    @abstractmethod
    def decidir_reinyeccion(self, estado_de_simulacion):
        pass


class CriterioReinyeccionSoloAguaEnTanques(CriterioDeReinyeccion):
    def __init__(self, presion):
        self.presion_critica = presion

    def decidir_venta_de_gas(self, estado_de_simulacion):
        for tanque in estado_de_simulacion.tanquesDeGasDisponibles:
            estado_de_simulacion.venderGas(tanque.volumenAlmacenado)

    def decidir_reinyeccion(self, estado_de_simulacion):
        hay_que_reinyectar = False
        for pozo in estado_de_simulacion.yacimiento.pozosPerforados:
            if pozo.presionActual < self.presion_critica:
                hay_que_reinyectar = True

        if hay_que_reinyectar:
            volumen_total_agua_almacenada = 0

            # TODO: checkear el limite de reinyeccion de agua

            for tanque in estado_de_simulacion.tanquesDeAguaDisponibles:
                volumen_total_agua_almacenada += tanque.volumenAlmacenado
                tanque.retirarVolumen(tanque.volumenAlmacenado)

            estado_de_simulacion.yacimiento.reinyectar(
                    volumen_total_agua_almacenada, 0)

