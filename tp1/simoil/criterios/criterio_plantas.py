from abc import ABCMeta

class CriterioDeConstruccionDePlantasSeparadoras(metaclass=ABCMeta):

    @abstractmethod
    def construir_plantas(estado_de_simulacion):
        pass

class CriterioDeAhorroDePlantas(CriterioDeConstruccionDePlantasSeparadoras):
    def __init__(self):
        self._proximo_id_planta = 1

    def construir_plantas(estado_de_simulacion):


        '''- con funcion smart ahorro
        elegis modelo con mayor ratio poder / costo
        te fijas cuanto necesitas procesar al primer dia si extraes al maximo
        construis hasta la mitad de esa necesidad'''

        modelos = estado_de_simulacion.configuracion.modelos_de_planta_separadora
        modelo_mas_rendidor = max(modelos, key=lambda modelo: modelo.volumen_diario_separable/modelo.costo)

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
        modelos_necesarios = math.ceil(potencial_teorico/modelo_mas_rendidor.volumen_diario_separable)

        for i in range(modelos_necesarios):
            estado_de_simulacion.construir_planta_separadora(modelo_mas_rendidor, _proximo_id_planta)
            _proximo_id_planta += 1
