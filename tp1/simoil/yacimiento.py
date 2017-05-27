import math as m

class Yacimiento:

    def __init__(self, parcelas, volumenInicial, composicion):
        self.parcelasDelYacimiento = parcelas
        self.volumenInicial = volumenInicial
        self.composicion = composicion

        self.pozosPerforados = []
        self.volumenActual = volumenInicial
        self.volumenExtraido = 0

        self.ratioPresion = 1.0

    def terminarExtraccion(self, nPozos):
        self.ratioPresion *= self.proximoMultiplicador(nPozos)

    def proximoMultiplicador(self, nPozos):
        beta = 0.1*(self.volumenActual / self.volumenInicial) / (nPozos**(3/2))
        return (m.e**-beta)

    def reinyectar(self, volumenAgua, volumenGas):
        raise NotImplementedError

class Parcela:

    def __init__(self, presionInicial, id, profundidad, resistenciaAExcavacion):
        self.presionInicial = presionInicial
        self.id = id
        self.profundidad = profundidad
        self.resistenciaAExcavacion = resistenciaAExcavacion

class Pozo:

    def __init__(self, presionInicial, id):
        self.presionInicial = presionInicial
        self.id = id

    def presionActual(self, estado):
        return self.presionInicial * estado.yacimiento.ratioPresion