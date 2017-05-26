class Rig(object):
    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

    @attribute
    def metrosDiariosExcavados(self):
        return self._modelo.metrosDiariosExcavados

    @attribute
    def consumoDiario(self):
        return self._modelo.consumoDiario

    @attribute
    def costoDeAlquilerPorDia(self):
        return self._modelo.costoDeAlquilerPorDia

