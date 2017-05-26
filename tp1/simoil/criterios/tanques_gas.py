from abc import ABCMeta, abstractmethod

class CriterioConstruccionTanquesDeGas(metaclass=ABCMeta):

    @abstractmethod
    def construir_tanques_de_gas(self, estado_de_simulacion):
        pass

class CriterioDeAhorroDeTanquesDeGas(CriterioConstruccionTanquesDeGas):
    def _init_(self):
        self._proximo_id_tanque_de_gas = 1

    def construir_tanques_de_gas(self, estado_de_simulacion):
        '''elegis modelo con mayor ratio capacidad / costo
        estimas cantidad maxima de gas que vas a necesitar
        (volumen del primer dia pero con composicion critica)
        construis hasta la mitad de esa cantidad'''

        if estado_de_simulacion.diaNumero == 1:
            configuracion = estado_de_simulacion.configuracion
            modelos = configuracion.tiposDeTanqueDeGas
            modelo_mas_rendidor = max(modelos, key=lambda modelo:
                    modelo.volumenDeAlmacenamiento / modelo.costoDeConstruccion)

            potencial_teorico = 0
            excavaciones = estado_de_simulacion.excavacionesActuales
            alfa1 = configuracion.alfa1
            alfa2 = configuracion.alfa2

            def potencial_primer_dia(excavacion, cantidad_habilitada, alfa1, alfa2):
                ratio = excavacion.parcelaPerforada.presionInicial / cantidad_habilitada
                return alfa1 * ratio + alfa2 * (ratio ** 2)

            for excavacion in excavaciones:
                potencial_teorico += potencial_primer_dia(excavacion, len(excavaciones),
                        alfa1, alfa2)

            potencial_teorico = math.ceil(potencial_teorico/2)

            volumen_gas_teorico = estado_de_simulacion.configuracion.\
                    composicionCritica.porcentajeDeGas * potencial_teorico/100

            modelos_necesarios = math.ceil(
                    volumen_gas_teorico/modelo_mas_rendidor.volumenDeAlmacenamiento)

            for i in range(modelos_necesarios):
                estado_de_simulacion.construir_tanque_de_gas(
                        modelo_mas_rendidor, self._proximo_id_tanque_de_gas)
                self._proximo_id_tanque_de_gas += 1

        tanques_de_gas_sin_terminar = \
            estado_de_simulacion.tanquesDeGasEnConstruccion

        for tanque in tanques_de_gas_sin_terminar:
            tanques_de_gas_sin_terminar[tanque] -= 1
            if tanques_de_gas_sin_terminar[tanque] == 0:
                tanques_de_gas.append(tanque)
                del tanques_de_gas_sin_terminar[tanque]
