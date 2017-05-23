class CriterioHabilitacionPozos(object):
    def extraer(self, estado_de_simulacion):
        raise('Not implemented')

    def potencial(self, pozo, cantidad_habilitada, estado_de_simulacion):
        a1 = estado_de_simulacion.configuracion.alfa1
        a2 = estado_de_simulacion.configuracion.alfa2
        p = pozo.presion_actual
        ratio = p / cantidad_habilitada
        return a1 * ratio + a2 * (ratio ** 2)

    def log(self, pozo, extraccion):
        print('Se extrajeron %f m3 del pozo %d' % (extraccion, pozo.id))


class CriterioHabilitacionTotal(CriterioHabilitacionPozos):
    def extraer(self, estado_de_simulacion):
        pozos = estado_de_simulacion.yacimiento.pozos
        extraccion_total = 0
        n_pozos_habilitados = len(pozos)
        for pozo in pozos:
            extraccion = self.potencial(pozo, n_pozos_habilitados, estado_de_simulacion)
            extraccion_total += extraccion
            self.log(pozo, extraccion)

        a_separar = extraccion_total

        composicion = estado_de_simulacion.yacimiento.composicion

        vol_agua_total = 0
        vol_petroleo_total = 0
        vol_gas_total = 0

        for planta in estado_de_simulacion.plantas_separadoras:
            a_separar_en_planta = min(planta.volumen_diario_separable, a_separar)
            vol_agua, vol_petroleo, vol_gas = planta.separar(a_separar_en_planta, composicion)
            vol_agua_total += vol_agua
            vol_petroleo_total += vol_petroleo
            vol_gas_total += vol_gas
            a_separar -= a_separar_en_planta
            if a_separar < 0: break

        estado_de_simulacion.vender_petroleo(vol_petroleo_total)

        vol_gas_a_almacenar = vol_gas_total

        for tanque in estado_de_simulacion.tanques_de_gas:
            a_almacenar_en_tanque = min(tanque.capacidad(), vol_gas_a_almacenar)
            tanque.almacenar(a_almacenar_en_tanque)
            vol_gas_a_almacenar -= a_almacenar_en_tanque
            if vol_gas_a_almacenar < 0: break

        vol_agua_a_almacenar = vol_agua_total

        for tanque in estado_de_simulacion.tanques_de_agua:
            a_almacenar_en_tanque = min(tanque.capacidad(), vol_agua_a_almacenar)
            tanque.almacenar(a_almacenar_en_tanque)
            vol_agua_a_almacenar -= a_almacenar_en_tanque
            if vol_agua_a_almacenar < 0: break
