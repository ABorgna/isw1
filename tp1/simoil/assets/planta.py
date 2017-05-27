class PlantaSeparadora:

    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

    @property
    def volumenDiarioSeparable(self):
        return self._modelo.volumenDiarioSeparable

    def separar(self, volumen, composicion):
        if volumen > self.volumenDiarioSeparable:
            raise ValueError("Separando más que el volumen diario")
        return (volumen * composicion.ratioDeGas,
                volumen * composicion.ratioDeAgua,
                volumen * composicion.ratioDePetroleo)

