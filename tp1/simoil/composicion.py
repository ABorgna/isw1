class Composicion:

    def __init__(self, partes_gas, partes_agua, partes_petroleo):
        self._partes_gas = partes_gas
        self._partes_agua = partes_agua
        self._partes_petroleo = partes_petroleo

    @attribute
    def ratioDeGas(self):
        return self._partes_gas / self._total

    @attribute
    def ratioDeAgua(self):
        return self._partes_agua / self._total

    @attribute
    def ratioDePetroleo(self):
        return self._partes_petroleo / self._total

    @attribute
    def _total(self):
        return self._partes_gas + self._partes_agua + self._partes_petroleo

