from abc import ABCMeta, abstractmethod
import logging

class CriterioHabilitacionPozos(metaclass=ABCMeta):

    @abstractmethod
    def extraer(self, estado):
        pass

    def potencial(self, pozo, cantidad_habilitada, estado):
        a1 = estado.configuracion.alfa1
        a2 = estado.configuracion.alfa2
        p = pozo.presionActual(estado)
        ratio = p / cantidad_habilitada
        return a1 * ratio + a2 * (ratio ** 2)

    def logExtraccion(self, pozo, extraccion):
        logging.info('Se extrajeron %f m3 del pozo %d' % (extraccion, pozo.id))


class CriterioHabilitacionTotal(CriterioHabilitacionPozos):

    def extraer(self, estado):
        yacimiento = estado.yacimiento
        pozos = yacimiento.pozosPerforados
        extraccion_total = 0
        n_pozos_habilitados = len(pozos)
        if n_pozos_habilitados == 0:
            return
        composicion = yacimiento.composicion

        capacidad_total_de_agua = 0
        for tanque in estado.tanquesDeAguaDisponibles:
            capacidad_total_de_agua += tanque.capacidad

        ratio_agua = composicion.ratioDeAgua
        for pozo in pozos:
            extraccion = self.potencial(pozo, n_pozos_habilitados, estado)
            agua_extraida = extraccion*ratio_agua

            if agua_extraida <= capacidad_total_de_agua:
                yacimiento.volumenExtraido += extraccion
                yacimiento.volumenActual -= extraccion
                capacidad_total_de_agua -= agua_extraida
                extraccion_total += extraccion
                self.logExtraccion(pozo, extraccion)

        a_separar = extraccion_total

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

        def almacenarEn(tanques, vol_a_almacenar, string_tipo):
            for tanque in tanques:
                a_almacenar_en_tanque = min(tanque.capacidad, vol_a_almacenar)
                tanque.almacenarVolumen(a_almacenar_en_tanque)
                logging.info('Se almacenaron %f m3 en el tanque de %s %d' % (a_almacenar_en_tanque, string_tipo, tanque.id))
                vol_a_almacenar -= a_almacenar_en_tanque
                if vol_a_almacenar < 0: break

        almacenarEn(estado.tanquesDeGasDisponibles, vol_gas_total, "gas")
        almacenarEn(estado.tanquesDeAguaDisponibles, vol_agua_total, "agua")

        volumen_inicial = yacimiento.volumenInicial
        volumen_actual = yacimiento.volumenExtraido

        yacimiento.terminarExtraccion(n_pozos_habilitados)
