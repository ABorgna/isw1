from abc import ABCMeta

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
        excavaciones = estado_de_simulacion.excavaciones_actuales
        if estado_de_simulacion.dia_actual != 0:
            return
        '''
        if excavaciones == {}:
            return
        '''
        rig_models = estado_de_simulacion.configuracion.modelos_de_rig

        '''agarras el modelo de rig con mas velocidad
        contratas un rig por parcela
        lo usas hasta terminar la parcela
        si sobra no importa'''

        modelo_mas_rapido = max(rig_models, key=lambda modelo: modelo.metros_por_dia)
        velocidad_del_modelo = modelo_mas_rapido.metros_por_dia
        for excavacion in excavaciones:
            dias_necesarios = math.ceil(excavacion.parcela_perforada.profundidad/velocidad_del_modelo)
            estado_de_simulacion.alquilar_rig(modelo_mas_rapido, dias_necesarios, _proximo_id_rig)
            # buscar el rig alquilado, se agrega al final de la lista por lo tanto es el último
            rig_alquilado = estado_de_simulacion.rigs_contratados[-1]
            for dia in range(1, dias_necesarios+1):
                plan[dia].append((excavacion, rig_alquilado))


    def excavar(self, estado_de_simulacion):
        dia = estado_de_simulacion.dia()
        pozos = estado_de_simulacion.yacimiento.pozos_perforados
        if dia in self.plan:
            plan_dia = plan[dia]
            for excavacion, rig in plan_dia:
                excavacion.excavar(rig)
                if excavacion.finalizada():
                    nuevo_pozo = Pozo(excavacion.parcela_perforada, _proximo_id_pozo)
                    _proximo_id_pozo += 1
                    pozos.append(nuevo_pozo)
