import math as m

class Yacimiento:

    def __init__(self, parcelas, volumenInicial, composicion):
        self.parcelasDelYacimiento = parcelas
        self.volumenInicial = volumenInicial
        self.composicion = composicion

        self.pozosPerforados = []
        self.volumenExtraido = 0
        self.volumenReinyectado = 0

        self.ratioPresion = 1.0

    def terminarExtraccion(self, extraido, nPozos):
        self.volumenExtraido += extraido
        self.ratioPresion *= self.proximoMultiplicador(nPozos)

    def proximoMultiplicador(self, nPozos):
        beta = 0.1*(self.volumenActual / self.volumenInicial) / (nPozos**(3/2))
        return (m.e**-beta)

    def reinyectar(self, volumenAgua, volumenGas):
        raise NotImplementedError

    @property
    def volumenActual(self):
        return self.volumenInicial - self.volumenExtraido + self.volumenReinyectado

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

    def potencial(self, cantidad_habilitada, estado):
        a1 = estado.configuracion.alfa1
        a2 = estado.configuracion.alfa2
        p = self.presionActual(estado)
        ratio = p / cantidad_habilitada
        return a1 * ratio + a2 * (ratio ** 2)
