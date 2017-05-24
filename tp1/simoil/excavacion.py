class Excavacion(object):
    def __init__(parcela):
        self.mts_restantes = parcela.profundidad
        self.parcela_perforada = parcela

    def excavar(self, rig):
        mts_excavados = min(mts_restantes, rig.metros_por_dia)
        mts_restantes -= mts_excavados

    def finalizada(self):
        return mts_restantes == 0
