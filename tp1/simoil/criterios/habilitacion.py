from abc import ABCMeta, abstractmethod
import logging

class CriterioHabilitacionPozos(metaclass=ABCMeta):

    @abstractmethod
    def extraer(self, estado):
        pass

    def potencial(self, pozo, cantidad_habilitada, estado):
        a1 = estado.configuracion.alfa1
        a2 = estado.configuracion.alfa2
        p = pozo.presionActual
        ratio = p / cantidad_habilitada
        return a1 * ratio + a2 * (ratio ** 2)

    def logExtraccion(self, pozo, extraccion):
        logging.info('Se extrajeron %f m3 del pozo %d' % (extraccion, pozo.id))


class CriterioHabilitacionTotal(CriterioHabilitacionPozos):
    def extraer(self, estado):
        pozos = estado.yacimiento.pozosPerforados
        extraccion_total = 0
        n_pozos_habilitados = len(pozos)

        for pozo in pozos:
            extraccion = self.potencial(pozo, n_pozos_habilitados, estado)
            extraccion_total += extraccion
            self.logExtraccion(pozo, extraccion)

        a_separar = extraccion_total

        composicion = estado.yacimiento.composicion

        vol_agua_total = 0
        vol_petroleo_total = 0
        vol_gas_total = 0

        for planta in estado.plantasDisponibles:
            a_separar_en_planta = min(planta.volumenDiarioSeparable, a_separar)
            vol_agua, vol_petroleo, vol_gas = \
                planta.separar(a_separar_en_planta, composicion)
            vol_agua_total += vol_agua
            vol_petroleo_total += vol_petroleo
            vol_gas_total += vol_gas
            a_separar -= a_separar_en_planta

            if a_separar < 0: break

        estado.venderPetroleo(vol_petroleo_total)

        vol_gas_a_almacenar = vol_gas_total

        for tanque in estado.tanquesDeGasDisponibles:
            a_almacenar_en_tanque = min(tanque.capacidad, vol_gas_a_almacenar)
            tanque.almacenarVolumen(a_almacenar_en_tanque)
            vol_gas_a_almacenar -= a_almacenar_en_tanque
            if vol_gas_a_almacenar < 0: break

        vol_agua_a_almacenar = vol_agua_total

        for tanque in estado.tanquesDeAguaDisponibles:
            a_almacenar_en_tanque = min(tanque.capacidad, vol_agua_a_almacenar)
            tanque.almacenarVolumen(a_almacenar_en_tanque)
            vol_agua_a_almacenar -= a_almacenar_en_tanque
            if vol_agua_a_almacenar < 0: break

