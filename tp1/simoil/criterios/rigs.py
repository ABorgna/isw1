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
            dias_necesarios = max(dias_necesarios,
                                  modelo_mas_rapido.diasDeAlquilerMinimo)

            rig_alquilado = estado.alquilarRIG(
                    modelo_mas_rapido, dias_necesarios, self._proximo_id_rig)

            for dia in range(1, dias_necesarios+1):
                self.plan.setdefault(dia, []).append((excavacion, rig_alquilado))


    def excavar(self, estado):
        dia = estado.diaNumero
        pozos = estado.yacimiento.pozosPerforados

        if dia in self.plan:
            plan_dia = self.plan[dia]

            for excavacion, rig in plan_dia:
                excavacion.excavar(rig)
                if excavacion.termino():
                    nuevo_pozo = Pozo(
                            excavacion.parcelaPerforada.presionInicial,
                            self._proximo_id_pozo)
                    self._proximo_id_pozo += 1
                    pozos.append(nuevo_pozo)

            estado.excavacionesActuales = [excavacion for excavacion in estado.excavacionesActuales if not excavacion.termino]
