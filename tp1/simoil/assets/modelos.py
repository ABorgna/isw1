
class ModeloDeTanque():

    def __init__(self, volumenDeAlmacenamiento, diasDeConstruccion,
            costoDeConstruccion):
        self.volumenDeAlmacenamiento = volumenDeAlmacenamiento
        self.diasDeConstruccion = diasDeConstruccion
        self.costoDeConstruccion = costoDeConstruccion

class ModeloDePlantaSeparadora():

    def __init__(self, volumenDiarioSeparable, diasDeConstruccion,
            costoDeConstruccion):
        self.volumenDiarioSeparable = volumenDiarioSeparable
        self.diasDeConstruccion = diasDeConstruccion
        self.costoDeConstruccion = costoDeConstruccion

class ModeloDeRIG():

    def __init__(self, metrosDiariosExcavados, consumoDiario,
            costoDeAlquilerPorDia, diasDeAlquilerMinimo):
        self.metrosDiariosExcavados = metrosDiariosExcavados
        self.consumoDiario = consumoDiario
        self.costoDeAlquilerPorDia = costoDeAlquilerPorDia
        self.diasDeAlquilerMinimo = diasDeAlquilerMinimo

