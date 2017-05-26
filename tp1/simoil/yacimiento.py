class Yacimiento:

    def __init__(self, parcelas, volumenInicial, composicion):
        self.parcelasDelYacimiento = parcelas
        self.volumenInicial = volumenInicial
        self.composicion = composicion

        self.pozosPerforados = []
        self.volumenActual = volumenInicial
        self.pozosHabilitados = 0
        self.volumenExtraido = 0

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

        self.presionActual = presionInicial

    def actualizarPresion(self, presion):
        self.presionActual = presion

