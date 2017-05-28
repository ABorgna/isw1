import logging
import math as m

from composicion import Composicion


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
        self.volumenReinyectado += (volumenAgua + volumenGas)
        assert(self.volumenActual <= self.volumenInicial)

        vol_agua = self.composicion.ratioDeAgua * self.volumenActual
        vol_gas = self.composicion.ratioDeGas * self.volumenActual
        vol_petroleo = self.composicion.ratioDePetroleo * self.volumenActual
        nuevo_vol_agua = vol_agua + volumenAgua
        nuevo_vol_gas = vol_gas + volumenGas
        nuevo_vol_petroleo = vol_petroleo
        self.composicion = Composicion(nuevo_vol_gas, nuevo_vol_agua,
                                       nuevo_vol_petroleo)

        print("ratioPresión: {}".format(self.ratioPresion))
        self.ratioPresion = self.volumenActual / self.volumenInicial
        print("ratioPresión: {}".format(self.ratioPresion))
        logging.info('Se reinyectaron %f m3 de agua y %f m3 de gas' %
                     (volumenAgua, volumenGas))

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
