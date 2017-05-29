from abc import ABCMeta, abstractmethod
import math

from yacimiento import Pozo

class CriterioContratacionYUsoDeRigs(metaclass=ABCMeta):

    @abstractmethod
    def contratar_rigs(self, estado):
        pass

    @abstractmethod
    def excavar(self, estado):
        pass


class CriterioContratacionYUsoDeRigsMinimoTiempo(CriterioContratacionYUsoDeRigs):
    def __init__(self):
        self.plan = {}
        self._proximo_id_pozo = 1
        self._proximo_id_rig = 1

    def contratar_rigs(self, estado):
        excavaciones = estado.excavacionesActuales
        if estado.diaNumero != 1:
            return

        '''
        if excavaciones == {}:
            return
        '''
        rig_models = estado.configuracion.tiposDeRig

        '''agarras el modelo de rig con mas velocidad
        contratas un rig por parcela
        lo usas hasta terminar la parcela
        si sobra no importa'''

        modelo_mas_rapido = max(rig_models,
                    key=lambda modelo: modelo.metrosDiariosExcavados)
        velocidad_del_modelo = modelo_mas_rapido.metrosDiariosExcavados

        for excavacion in excavaciones:
            resistencia = excavacion.parcelaPerforada.resistenciaAExcavacion
            coeficiente = (100 - resistencia)/100

            dias_necesarios = math.ceil(excavacion.parcelaPerforada.profundidad \
                    / (velocidad_del_modelo * coeficiente))
            total_dias = max(dias_necesarios,
                                  modelo_mas_rapido.diasDeAlquilerMinimo)

            rig_alquilado = estado.alquilarRIG(
                    modelo_mas_rapido, total_dias, self._proximo_id_rig)

            for dia in range(1, dias_necesarios+1):
                self.plan.setdefault(dia, []).append((excavacion, rig_alquilado))


    def excavar(self, estado):
        dia = estado.diaNumero

        if dia in self.plan:
            plan_dia = self.plan[dia]

            for excavacion, rig in plan_dia:
                excavacion.excavar(rig)
                if excavacion.termino():
                    nuevo_pozo = Pozo(
                            excavacion.parcelaPerforada.presionInicial,
                            self._proximo_id_pozo)
                    self._proximo_id_pozo += 1
                    estado.agregarPozo(nuevo_pozo)

            estado.excavacionesActuales = [excavacion for excavacion in estado.excavacionesActuales if not excavacion.termino]


class CriterioContratacionYUsoDeRigsMinimoCosto(CriterioContratacionYUsoDeRigs):
    def __init__(self):
        self.plan = {}
        self._proximo_id_pozo = 1

    def contratar_rigs(self, estado):
        ''' Agarras el modelo de rig con mejor rendimiento
        contratas un solo rig
        lo usas hasta terminar de excavar todo
        '''
        if estado.diaNumero != 1:
            return

        rig_models = estado.configuracion.tiposDeRig

        modelo = min(rig_models, key=lambda m: self._costo_final(m, estado))

        dias_alquiler = max(self._dias_necesarios(modelo, estado.excavacionesActuales),
                           modelo.diasDeAlquilerMinimo)
        rig_alquilado = estado.alquilarRIG(modelo, dias_alquiler, 1)

        counter_dia = 1
        for excavacion in estado.excavacionesActuales:
            dias = self._dias_necesarios(modelo, [excavacion])
            for dia in range(counter_dia, counter_dia + dias):
                self.plan.setdefault(dia, []).append((excavacion, rig_alquilado))
            counter_dia += dias

    def excavar(self, estado):
        dia = estado.diaNumero

        if dia in self.plan:
            plan_dia = self.plan[dia]

            for excavacion, rig in plan_dia:

                excavacion.excavar(rig)

                if excavacion.termino():
                    nuevo_pozo = Pozo(
                            excavacion.parcelaPerforada.presionInicial,
                            self._proximo_id_pozo)
                    self._proximo_id_pozo += 1
                    estado.agregarPozo(nuevo_pozo)

            estado.excavacionesActuales = [excavacion for excavacion
                    in estado.excavacionesActuales if not excavacion.termino]

    # Private helpers
    def _dias_necesarios(self, modelo, excavaciones):
        def diasExcavacion(e):
            r = (100 - e.parcelaPerforada.resistenciaAExcavacion) / 100
            return math.ceil(e.metrosRestantes / (modelo.metrosDiariosExcavados*r))

        return sum(diasExcavacion(e) for e in excavaciones)

    def _costo_final(self, modelo, estado):
        costoPorDia = modelo.costoDeAlquilerPorDia + \
                modelo.consumoDiario * estado.configuracion.costoLitroCombustible
        dias = max(self._dias_necesarios(modelo, estado.excavacionesActuales),
                   modelo.diasDeAlquilerMinimo)
        return dias * costoPorDia

