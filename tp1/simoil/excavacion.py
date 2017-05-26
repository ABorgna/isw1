class Excavacion(object):
    def __init__(self, parcela):
        self.parcelaPerforada = parcela
        self.metrosRestantes = parcela.profundidad

    def excavar(self, rig):
        coeficiente = (100 - self.parcelaPerforada.resistenciaAExcavacion)/100
        mts_excavados = min(self.metrosRestantes,
                rig.metrosDiariosExcavados*coeficiente)
        self.metrosRestantes -= mts_excavados

    def termino(self):
        return self.metrosRestantes == 0
