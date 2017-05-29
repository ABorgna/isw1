from abc import ABCMeta, abstractmethod
import math

class CriterioDeConstruccionDePlantasSeparadoras(metaclass=ABCMeta):

    @abstractmethod
    def construir_plantas(self, estado):
        pass

    def potencial_teorico(self, estado):
        res = 0
        configuracion = estado.configuracion
        excavaciones = estado.excavacionesActuales
        alfa1 = configuracion.alfa1
        alfa2 = configuracion.alfa2

        def potencial_primer_dia(excavacion, cantidad_habilitada, alfa1, alfa2):
            ratio = (excavacion.parcelaPerforada.presionInicial /
                     cantidad_habilitada)
            return alfa1 * ratio + alfa2 * (ratio ** 2)

        for excavacion in excavaciones:
            res += potencial_primer_dia(excavacion, len(excavaciones), alfa1,
                                        alfa2)

        return res


class CriterioDeAhorroDePlantas(CriterioDeConstruccionDePlantasSeparadoras):
    def __init__(self):
        self._proximo_id_planta = 1

    def construir_plantas(self, estado):
        '''- con funcion smart ahorro
        elegis modelo con mayor ratio poder / costo
        te fijas cuanto necesitas procesar al primer dia si extraes al maximo
        construis hasta la mitad de esa necesidad'''

        if estado.diaNumero == 1:
            configuracion = estado.configuracion
            modelos = configuracion.tiposDePlantaSeparadora
            modelo_mas_rendidor = max(modelos, key=lambda modelo:
                    modelo.volumenDiarioSeparable / modelo.costoDeConstruccion)

            mitad_potencial = math.ceil(self.potencial_teorico(estado) / 2)

            modelos_necesarios = math.ceil(
                mitad_potencial / modelo_mas_rendidor.volumenDiarioSeparable)

            for i in range(modelos_necesarios):
                estado.construirPlantaSeparadora(
                        modelo_mas_rendidor, self._proximo_id_planta)
                self._proximo_id_planta += 1


class CriterioPlantasParaMaximaCapacidad(
        CriterioDeConstruccionDePlantasSeparadoras):
    def __init__(self):
        self._proximo_id_planta = 1

    def construir_plantas(self, estado):
        '''
        elegis modelo con mayor capacidad de procesamiento
        te fijas cuanto necesitas procesar al primer dia si extraes al maximo
        construis hasta cubrir esa necesidad'''

        if estado.diaNumero == 1:
            configuracion = estado.configuracion
            modelos = configuracion.tiposDePlantaSeparadora
            modelo_mayor_capacidad = max(modelos, key=lambda modelo:
                    modelo.volumenDiarioSeparable)

            potencial = self.potencial_teorico(estado)

            modelos_necesarios = math.ceil(
                potencial / modelo_mayor_capacidad.volumenDiarioSeparable)

            for i in range(modelos_necesarios):
                estado.construirPlantaSeparadora(
                        modelo_mayor_capacidad, self._proximo_id_planta)
                self._proximo_id_planta += 1
