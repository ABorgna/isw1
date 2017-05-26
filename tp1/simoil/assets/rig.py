class Rig(object):
    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

    @property
    def metrosDiariosExcavados(self):
        return self._modelo.metrosDiariosExcavados

    @property
    def consumoDiario(self):
        return self._modelo.consumoDiario

