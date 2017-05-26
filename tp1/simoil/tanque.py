class Tanque:

    def __init__(self, modelo, id):
        self._modelo = modelo
        self.id = id

        self._volumenAlmacenado = 0

    @attribute
    def capacidad(self):
        return self._modelo.volumenDeAlmacenamiento

    @attribute
    def volumenAlmacenado(self):
        return self._volumenAlmacenado

    def almacenarVolumen(self, volumen):
        if volumen + self._volumenAlmacenado > self.capacidad:
            raise ValueError("Almacenado mas de lo que entra")
        return self._volumenAlmacenado += volumen

    def retirarVolumen(self, volumen):
        if volumen > self._volumenAlmacenado:
            raise ValueError("Retirando mas de lo que hay")
        return self._volumenAlmacenado -= volumen

