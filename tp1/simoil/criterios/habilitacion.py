from abc import ABCMeta, abstractmethod
import logging

class CriterioHabilitacionPozos(metaclass=ABCMeta):

    def extraer(self, estado, topeExtraccion):
        pozos = self.elegirPozos(estado)
        yacimiento = estado.yacimiento
        extraccion_total = 0
        n_pozos_habilitados = len(pozos)
        if n_pozos_habilitados == 0:
            return
        composicion = yacimiento.composicion

        for pozo in pozos:
            potencial = pozo.potencial(n_pozos_habilitados, estado)
            potencial = min(potencial, topeExtraccion - extraccion_total)
            self.logExtraccion(pozo, potencial)
            extraccion_total += potencial

        if (extraccion_total > topeExtraccion):
            raise ValueError("Extrayendo más volumen que el tope permitido")

        a_separar = extraccion_total
        vol_gas_total = 0
        vol_agua_total = 0
        vol_petroleo_total = 0

        for planta in estado.plantasDisponibles:
            a_separar_en_planta = min(planta.volumenDiarioSeparable, a_separar)
            vol_gas, vol_agua, vol_petroleo = planta.separar(a_separar_en_planta, composicion)
            vol_gas_total += vol_gas
            vol_agua_total += vol_agua
            vol_petroleo_total += vol_petroleo
            a_separar -= a_separar_en_planta
            self.logSeparacion(planta, a_separar_en_planta)
            if a_separar <= 0: break

        if (a_separar > 0):
            raise ValueError("No se pudo separar todo el producto")

        yacimiento.terminarExtraccion(extraccion_total, n_pozos_habilitados)
        estado.venderPetroleo(vol_petroleo_total)
        estado.almacenarAgua(vol_agua_total)
        estado.almacenarGas(vol_gas_total)

    def logExtraccion(self, pozo, extraccion):
        logging.info('Se extrajeron %f m3 del pozo %d' % (extraccion, pozo.id))

    def logSeparacion(self, planta, volumen):
        logging.info('Se separaron %f m3 en la planta %d' % (volumen, planta.id))

    @abstractmethod
    def elegirPozos(self, estado):
        pass

class CriterioHabilitacionTotal(CriterioHabilitacionPozos):

    def elegirPozos(self, estado):
        return estado.yacimiento.pozosPerforados
