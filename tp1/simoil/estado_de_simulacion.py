import logging

from assets.planta import PlantaSeparadora
from assets.rig import Rig
from assets.tanque import Tanque

class EstadoDeSimulacion(object):
    def __init__(self, yacimiento, configuracion):
        self.yacimiento = yacimiento
        self.configuracion = configuracion

        self.diaNumero = 0
        self.costosAcumulados = 0
        self.gananciasAcumuladas = 0

        self.plantasDisponibles = []
        self.tanquesDeAguaDisponibles = []
        self.tanquesDeGasDisponibles = []

        self.excavacionesActuales = []

        self.rigsAlquiladosActualmente = {}
        self.plantasEnConstruccion = {}
        self.tanquesDeAguaEnConstruccion = {}
        self.tanquesDeGasEnConstruccion = {}

    def avanzarDia(self):
        self.diaNumero += 1
        logging.info("---- dia número: "+ str(self.diaNumero))

        self.configuracion.CriterioDeReinyeccion.decidir_venta_de_gas(self)

        self.configuracion.CriterioEleccionParcelas.decidir_proximas_parcelas(self)

        self.configuracion.CriterioContratacionYUsoDeRigs.contratar_rigs(self)

        self.configuracion.CriterioContratacionYUsoDeRigs.excavar(self)

        self.configuracion.CriterioDeConstruccionDePlantasSeparadoras.\
                construir_plantas(self)

        self.configuracion.CriterioConstruccionTanquesDeAgua.\
                construir_tanques_de_agua(self)

        self.configuracion.CriterioConstruccionTanquesDeGas.\
                construir_tanques_de_gas(self)

        self.configuracion.CriterioHabilitacionPozos.extraer(self)

        self.configuracion.CriterioDeReinyeccion.decidir_reinyeccion(self)

        # TODO: extraer el petroleo si no se reinyectó,
        # checkear si terminaron las construcciones,
        # y simular todo lo que falte

    def puedeSeguir(self):
        cortePorCriterio = self.configuracion.CriterioDeCorte.cortar(self)

        bajaConcentracion = self.yacimiento.composicion.ratioDePetroleo <= \
                            self.configuracion.concentracionCritica

        return not cortePorCriterio and not bajaConcentracion

    def alquilarRIG(self, modelo, diasDeAlquiler, id):
        assert(diasDeAlquiler >= modelo.diasDeAlquilerMinimo)

        rig = Rig(modelo, id)

        self.rigsAlquiladosActualmente[rig] = diasDeAlquiler
        self.costosAcumulados += modelo.costoDeAlquilerPorDia * diasDeAlquiler

        return rig

    def construirPlantaSeparadora(self, modeloPlanta, id):
        planta = PlantaSeparadora(modeloPlanta, id)

        self.plantasEnConstruccion[planta] = modeloPlanta.diasDeConstruccion
        self.costosAcumulados += modeloPlanta.costoDeConstruccion

        return planta

    def construirTanqueDeAgua(self, modeloTanque, id):
        tanque = Tanque(modeloTanque, id)

        self.tanquesDeAguaEnConstruccion[tanque] = modeloTanque.diasDeConstruccion
        self.costosAcumulados += modeloTanque.costoDeConstruccion

        return tanque

    def construirTanqueDeGas(self, modeloTanque, id):
        tanque = Tanque(modeloTanque, id)

        self.tanquesDeGasEnConstruccion[tanque] = modeloTanque.diasDeConstruccion
        self.costosAcumulados += modeloTanque.costoDeConstruccion

        return tanque

    def agregarExcavacion(self, excavacion):
        self.excavacionesActuales.append(excavacion)

    def comprarAgua(self, volumen):
        self.costosAcumulados += volumen * self.configuracion.costoLitroAgua

        for t in self.tanquesDeAguaDisponibles:
            dVol = min(volumen, t.capacidad - t.volumenAlmacenado)
            t.almacenarVolumen(dVol)
            volumen -= dVol

            if volumen == 0:
                break

        assert(volumen == 0)

    def venderPetroleo(self, volumen):
        self.gananciasAcumuladas += \
            volumen * self.configuracion.precioMetroCubicoDePetroleo

    def venderGas(self, volumen):
        self.gananciasAcumuladas += \
            volumen * self.configuracion.precioMetroCubicoDeGas

        for t in self.tanquesDeGasDisponibles:
            dVol = min(volumen, t.volumenAlmacenado)
            t.retirarVolumen(dVol)
            volumen -= dVol

            if volumen == 0:
                break

        assert(volumen == 0)

    # Internals

    def _volumenMaximo(self, tanques):
        return sum(t.capacidad for t in tanques)

    def _volumenAlmacenado(self, tanques):
        return sum(t.volumenAlmacenado for t in tanques)

