class CriterioContratacionYUsoDeRigs(object):
    def contratar_rigs(self, estado_de_simulacion):
        raise('Not implemented')

    def excavar(self, estado_de_simulacion):
        raise('Not implemented')


class CriterioContratacionYUsoDeRigsMinimoTiempo(CriterioContratacionYUsoDeRigs):
    def __init__(self):
        self.plan = {}

    def contratar_rigs(self, estado_de_simulacion):
        if estado_de_simulacion.excavaciones_actuales == {}:
            return
        rig_models = estado_de_simulacion.conf

    def excavar(self, estado_de_simulacion):
        dia = estado_de_simulacion.dia()
        if dia in self.plan:
            plan_dia = plan[dia]
            for excavacion, rig in plan_dia:
                excavacion.excavar(rig)
                if excavacion.finalizada():
                    pass
                
                
