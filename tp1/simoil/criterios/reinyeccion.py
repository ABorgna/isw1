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
        max_vol_reinyectable = estado.configuracion.maximoVolumenReinyectable

        vol_a_reinyectar = 0

        for tanque in estado.tanquesDeAguaDisponibles:
            vol_a_sacar = min(max_vol_reinyectable - vol_a_reinyectar,
                              tanque.volumenAlmacenado)
            vol_a_reinyectar += vol_a_sacar
            tanque.retirarVolumen(vol_a_sacar)
            if vol_a_reinyectar >= max_vol_reinyectable:
                break

        estado.yacimiento.reinyectar(vol_a_reinyectar, 0)


class CriterioReinyeccionAguaYGas(CriterioDeReinyeccion):
    def __init__(self, presion):
        self.presion_critica = presion

    def decidir_venta_de_gas(self, estado):
        for tanque in estado.tanquesDeGasDisponibles:
            estado.venderGas(tanque.volumenAlmacenado / 2)

    def hay_que_reinyectar(self, estado):
        for pozo in estado.yacimiento.pozosPerforados:
            if pozo.presionActual(estado) < self.presion_critica:
                return True
        return False

    def reinyectar(self, estado):
        max_vol_reinyectable = estado.configuracion.maximoVolumenReinyectable

        vol_gas_a_reinyectar = 0

        for tanque in estado.tanquesDeGasDisponibles:
            vol_a_sacar = min(max_vol_reinyectable - vol_gas_a_reinyectar,
                              tanque.volumenAlmacenado)
            vol_gas_a_reinyectar += vol_a_sacar
            tanque.retirarVolumen(vol_a_sacar)
            if vol_gas_a_reinyectar >= max_vol_reinyectable:
                break

        vol_agua_a_reinyectar = 0

        for tanque in estado.tanquesDeAguaDisponibles:
            vol_a_sacar = min(max_vol_reinyectable - vol_gas_a_reinyectar -
                              vol_agua_a_reinyectar,
                              tanque.volumenAlmacenado)
            vol_agua_a_reinyectar += vol_a_sacar
            tanque.retirarVolumen(vol_a_sacar)
            if (vol_agua_a_reinyectar + vol_gas_a_reinyectar >=
                max_vol_reinyectable):
                break

        estado.yacimiento.reinyectar(vol_agua_a_reinyectar, vol_gas_a_reinyectar)
