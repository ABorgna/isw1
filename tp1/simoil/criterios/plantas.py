from abc import ABCMeta, abstractmethod
import math

class CriterioDeConstruccionDePlantasSeparadoras(metaclass=ABCMeta):

    @abstractmethod
    def construir_plantas(self, estado_de_simulacion):
        pass

class CriterioDeAhorroDePlantas(CriterioDeConstruccionDePlantasSeparadoras):
    def __init__(self):
        self._proximo_id_planta = 1

    def construir_plantas(self, estado_de_simulacion):


        '''- con funcion smart ahorro
        elegis modelo con mayor ratio poder / costo
        te fijas cuanto necesitas procesar al primer dia si extraes al maximo
        construis hasta la mitad de esa necesidad'''

        if estado_de_simulacion.dia_actual == 1:
            configuracion = estado_de_simulacion.configuracion
            modelos = configuracion.tiposDePlantaSeparadora
            modelo_mas_rendidor = max(modelos, key=lambda modelo:
                    modelo.volumenDiarioSeparable /modelo.costoDeConstruccion)

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
            modelos_necesarios = math.ceil(potencial_teorico / \
                    modelo_mas_rendidor.volumenDiarioSeparable)

            for i in range(modelos_necesarios):
                estado_de_simulacion.construirPlantaSeparadora(
                        modelo_mas_rendidor, self._proximo_id_planta)
                self._proximo_id_planta += 1

        plantas_sin_terminar = estado_de_simulacion.plantasEnConstruccion

        for planta in plantas_sin_terminar:
            plantas_sin_terminar[planta] -= 1

            if plantas_sin_terminar[planta] == 0:
                estado_de_simulacion.plantas_separadoras.append(planta)
                del plantas_separadoras[planta]
