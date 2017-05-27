from abc import ABCMeta, abstractmethod
import logging

class CriterioHabilitacionPozos(metaclass=ABCMeta):

    def almacenarEn(self, tanques, vol_a_almacenar, string_tipo):
        for tanque in tanques:
            a_almacenar_en_tanque = min(tanque.capacidad, vol_a_almacenar)
            tanque.almacenarVolumen(a_almacenar_en_tanque)
            logging.info('Se almacenaron %f m3 en el tanque de %s %d' % (a_almacenar_en_tanque, string_tipo, tanque.id))
            vol_a_almacenar -= a_almacenar_en_tanque
            if vol_a_almacenar < 0: break

    def extraer(self, estado):
        yacimiento = estado.yacimiento
        pozos = self.elegirPozos(estado)
        extraccion_total = 0
        n_pozos_habilitados = len(pozos)
        if n_pozos_habilitados == 0:
            return
        composicion = yacimiento.composicion

        volumen_disponible_de_agua_en_tanques = estado.volumenDisponibleEn(estado.tanquesDeAguaDisponibles)
        volumen_disponible_de_gas_en_tanques = estado.volumenDisponibleEn(estado.tanquesDeGasDisponibles)

        ratio_agua = composicion.ratioDeAgua
        for pozo in pozos:
            extraccion = pozo.potencial(n_pozos_habilitados, estado)
            agua_extraida = extraccion*ratio_agua

            if agua_extraida <= volumen_disponible_de_agua_en_tanques:
                volumen_disponible_de_agua_en_tanques -= agua_extraida
                extraccion_total += extraccion
                self.logExtraccion(pozo, extraccion)

        a_separar = extraccion_total

        vol_gas_total = 0
        vol_agua_total = 0
        vol_petroleo_total = 0

        for planta in estado.plantasDisponibles:
            a_separar_en_planta = min(planta.volumenDiarioSeparable, a_separar)
            vol_agua, vol_petroleo, vol_gas = \
                planta.separar(a_separar_en_planta, composicion)
            vol_gas_total += vol_gas
            vol_agua_total += vol_agua
            vol_petroleo_total += vol_petroleo
            a_separar -= a_separar_en_planta

            if a_separar < 0: break

        estado.venderPetroleo(vol_petroleo_total)

        self.almacenarEn(estado.tanquesDeGasDisponibles, vol_gas_total, "gas")
        self.almacenarEn(estado.tanquesDeAguaDisponibles, vol_agua_total, "agua")

        yacimiento.terminarExtraccion(extraccion_total, n_pozos_habilitados)

    def logExtraccion(self, pozo, extraccion):
        logging.info('Se extrajeron %f m3 del pozo %d' % (extraccion, pozo.id))

    @abstractmethod
    def elegirPozos(self, estado):
        pass

class CriterioHabilitacionTotal(CriterioHabilitacionPozos):

    def elegirPozos(self, estado):
        return estado.yacimiento.pozosPerforados
