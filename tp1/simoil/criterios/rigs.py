from abc import ABCMeta, abstractmethod
import math

class CriterioContratacionYUsoDeRigs(metaclass=ABCMeta):

    @abstractmethod
    def contratar_rigs(self, estado_de_simulacion):
        pass

    @abstractmethod
    def excavar(self, estado_de_simulacion):
        pass


class CriterioContratacionYUsoDeRigsMinimoTiempo(CriterioContratacionYUsoDeRigs):
    def __init__(self):
        self.plan = {}
        self._proximo_id_pozo = 1
        self._proximo_id_rig = 1

    def contratar_rigs(self, estado_de_simulacion):
        excavaciones = estado_de_simulacion.excavacionesActuales
        if estado_de_simulacion.diaNumero != 1:
            return

        '''
        if excavaciones == {}:
            return
        '''
        rig_models = estado_de_simulacion.configuracion.tiposDeRig

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
            estado_de_simulacion.alquilarRIG(modelo_mas_rapido, dias_necesarios,
                    self._proximo_id_rig)

            # buscar el rig alquilado, se agrega al final de la lista
            # por lo tanto es el último
            rig_alquilado = estado_de_simulacion.rigsDisponibles[-1]
            for dia in range(1, dias_necesarios+1):
                self.plan[dia].append((excavacion, rig_alquilado))


    def excavar(self, estado_de_simulacion):
        dia = estado_de_simulacion.diaNumero()
        pozos = estado_de_simulacion.yacimiento.pozosPerforados

        if dia in self.plan:
            plan_dia = self.plan[dia]

            for excavacion, rig in plan_dia:
                excavacion.excavar(rig)
                if excavacion.finalizada():
                    nuevo_pozo = Pozo(excavacion.parcelaPerforada,
                            self._proximo_id_pozo)
                    self._proximo_id_pozo += 1
                    pozos.append(nuevo_pozo)

