class Tanque:

    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

        self._volumenAlmacenado = 0

    @property
    def capacidad(self):
        return self._modelo.volumenDeAlmacenamiento

    @property
    def volumenAlmacenado(self):
        return self._volumenAlmacenado

    @property
    def volumenDisponible(self):
        return self.capacidad - self.volumenAlmacenado

    def almacenarVolumen(self, volumen):
        if volumen + self._volumenAlmacenado > self.capacidad:
            raise ValueError("Almacenado mas de lo que entra")
        self._volumenAlmacenado += volumen

    def retirarVolumen(self, volumen):
        if volumen > self._volumenAlmacenado:
            raise ValueError("Retirando mas de lo que hay")
        self._volumenAlmacenado -= volumen

