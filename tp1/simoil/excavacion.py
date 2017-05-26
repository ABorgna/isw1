class Excavacion(object):
    def __init__(parcela):
        self.mts_restantes = parcela.profundidad
        self.parcela_perforada = parcela

    def excavar(self, rig):
        coeficiente = (100 - parcela_perforada.resistencia_a_excavacion)/100
        mts_excavados = min(mts_restantes, rig.metros_por_dia*coeficiente)
        mts_restantes -= mts_excavados

    def finalizada(self):
        return mts_restantes == 0
