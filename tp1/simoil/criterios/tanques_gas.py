from abc import ABCMeta, abstractmethod
import math

class CriterioConstruccionTanquesDeGas(metaclass=ABCMeta):

    @abstractmethod
    def construir_tanques_de_gas(self, estado):
        pass

class CriterioDeAhorroDeTanquesDeGas(CriterioConstruccionTanquesDeGas):
    def __init__(self):
        self._proximo_id = 1

    def construir_tanques_de_gas(self, estado):
        '''elegis modelo con mayor ratio capacidad / costo
        estimas cantidad maxima de gas que vas a necesitar
        (volumen del primer dia pero con composicion critica)
        construis hasta la mitad de esa cantidad'''

        if estado.diaNumero == 1:
            configuracion = estado.configuracion
            modelos = configuracion.tiposDeTanqueDeGas
            modelo_mas_rendidor = max(modelos, key=lambda modelo:
                    modelo.volumenDeAlmacenamiento / modelo.costoDeConstruccion)

            potencial_teorico = 0
            excavaciones = estado.excavacionesActuales
            alfa1 = configuracion.alfa1
            alfa2 = configuracion.alfa2

            def potencial_primer_dia(excavacion, cantidad_habilitada, alfa1, alfa2):
                ratio = excavacion.parcelaPerforada.presionInicial \
                        / cantidad_habilitada
                return alfa1 * ratio + alfa2 * (ratio ** 2)

            for excavacion in excavaciones:
                potencial_teorico += potencial_primer_dia(excavacion,
                        len(excavaciones), alfa1, alfa2)

            potencial_teorico = math.ceil(potencial_teorico/2)

            volumen_gas_teorico = (1 - estado.configuracion.\
                    concentracionCritica) * potencial_teorico

            modelos_necesarios = math.ceil(
                volumen_gas_teorico/modelo_mas_rendidor.volumenDeAlmacenamiento)

            for i in range(modelos_necesarios):
                estado.construirTanqueDeGas(
                        modelo_mas_rendidor, self._proximo_id)
                self._proximo_id += 1
