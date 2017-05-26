class PlantaSeparadora:

    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

    @property
    def volumenDiarioSeparable(self):
        return self._modelo.volumenDiarioSeparable

    def separar(self, volumen, composicion):
        # TODO checkear que no se separe mas del maximo
        return (volumen * composicion.ratioDeGas,
                volumen * composicion.ratioDeAgua,
                volumen * composicion.ratioDePetroleo)

