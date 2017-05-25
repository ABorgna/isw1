from abc import ABCMeta, abstractmethod

class CriterioConstruccionTanquesDeAgua(metaclass=ABCMeta):

    @abstractmethod
    def construir_tanques_de_agua(estado_de_simulacion):
        pass

class CriterioDeAhorroDeTanquesDeAgua(CriterioConstruccionTanquesDeAgua):
    def _init_(self):
        self._proximo_id_tanque_de_agua = 1

    def construir_tanques_de_agua(estado_de_simulacion):

        '''elegis modelo con mayor ratio capacidad / costo
        estimas cantidad maxima de agua que vas a necesitar
        (volumen del primer dia pero con composicion critica)
        construis hasta la mitad de esa cantidad'''

        if estado_de_simulacion.dia_actual == 1
            modelos = estado_de_simulacion.configuracion.modelos_de_tanque
            modelo_mas_rendidor = max(modelos, key=lambda modelo: modelo.capacidad/modelo.costo)

            potencial_teorico = 0
            parcelas = estado_de_simulacion.yacimiento.parcelas
            alfa1 = estado_de_simulacion.configuracion.alfa1
            alfa2 = estado_de_simulacion.configuracion.alfa2

            def potencial_primer_dia(parcela, cantidad_habilitada, alfa1, alfa2):
                ratio = presion / cantidad_habilitada
                return alfa1 * ratio + alfa2 * (ratio ** 2)

            for parcela in parcelas:
                potencial_teorico += potencial_primer_dia(parcela, len(parcelas), alfa1, alfa2)

            potencial_teorico = math.ceil(potencial_teorico/2)
            volumen_agua_teorico = estado_de_simulacion.configuracion.composicion_critica.porcentaje_agua * potencial_teorico
            modelos_necesarios = math.ceil(volumen_agua_teorico/modelo_mas_rendidor.capacidad)

            for i in range(modelos_necesarios):
                estado_de_simulacion.construir_tanque_de_agua(modelo_mas_rendidor, _proximo_id_tanque_de_agua)
                _proximo_id_tanque_de_agua += 1

        tanques_de_agua_sin_terminar = estado_de_simulacion.tanques_de_agua_en_construccion
        for tanque in tanques_de_agua_sin_terminar:
            tanques_de_agua_sin_terminar[tanque] -= 1
            if tanques_de_agua_sin_terminar[tanque] == 0:
                tanques_de_agua.append(tanque)
