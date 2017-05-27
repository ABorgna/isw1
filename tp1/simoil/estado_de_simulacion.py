import logging
import math

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

        def decrementarDias(coleccion_en_progreso, coleccion_final):
            for item in coleccion_en_progreso:
                coleccion_en_progreso[item] -= 1
                if coleccion_en_progreso[item] == 0:
                    coleccion_final.append(item)
            coleccion_en_progreso = {k: v for k, v in coleccion_en_progreso.items() if v > 0}

        decrementarDias(self.tanquesDeGasEnConstruccion, self.tanquesDeGasDisponibles)
        decrementarDias(self.tanquesDeAguaEnConstruccion, self.tanquesDeAguaDisponibles)
        decrementarDias(self.plantasEnConstruccion, self.plantasDisponibles)

        for rigs in self.rigsAlquiladosActualmente:
            self.rigsAlquiladosActualmente[rigs] -= 1
        self.rigsAlquiladosActualmente = {k: v for k, v in self.rigsAlquiladosActualmente.items() if v > 0}

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

        if self.configuracion.CriterioDeReinyeccion.hayQueReinyectar(self):
            self.configuracion.CriterioDeReinyeccion.decidir_reinyeccion(self)
        else:
            self.configuracion.CriterioHabilitacionPozos.extraer(self, self.topeVolumenExtraccion())


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

    def almacenarAgua(self, volumen):
        self.almacenarEn(self.tanquesDeAguaDisponibles, volumen, "agua")

    def almacenarGas(self, volumen):
        self.almacenarEn(self.tanquesDeGasDisponibles, volumen, "gas")

    # Internals

    def volumenMaximoEn(self, tanques):
        return sum(t.capacidad for t in tanques)

    def volumenAlmacenadoEn(self, tanques):
        return sum(t.volumenAlmacenado for t in tanques)

    def volumenDisponibleEn(self, tanques):
        return sum(t.volumenDisponible for t in tanques)

    def volumenSeparableEn(self, plantas):
        return sum(p.volumenDiarioSeparable for p in plantas)

    def volumenDisponibleDeAgua(self):
        return self.volumenDisponibleEn(self.tanquesDeAguaDisponibles)

    def volumenDisponibleDeGas(self):
        return self.volumenDisponibleEn(self.tanquesDeGasDisponibles)

    def topeVolumenExtraccion(self):
        c = self.yacimiento.composicion
        volumen_disponible_de_agua_en_tanques = self.volumenDisponibleDeAgua()
        volumen_disponible_de_gas_en_tanques = self.volumenDisponibleDeGas()
        volumen_disponible_plantas_separadoras = self.volumenSeparableEn(self.plantasDisponibles)
        tope_agua = math.inf if c.ratioDeAgua == 0 else volumen_disponible_de_agua_en_tanques / c.ratioDeAgua
        tope_gas = math.inf if c.ratioDeGas == 0 else volumen_disponible_de_gas_en_tanques / c.ratioDeGas
        return min(volumen_disponible_plantas_separadoras, 
            tope_agua, 
            tope_gas)

    def almacenarEn(self, tanques, vol_a_almacenar, string_tipo):
        for tanque in tanques:
            a_almacenar_en_tanque = min(tanque.volumenDisponible, vol_a_almacenar)
            tanque.almacenarVolumen(a_almacenar_en_tanque)
            logging.info('Se almacenaron %f m3 en el tanque de %s %d' % (a_almacenar_en_tanque, string_tipo, tanque.id))
            vol_a_almacenar -= a_almacenar_en_tanque
            if vol_a_almacenar < 0: break
        if vol_a_almacenar > 0:
            raise ValueError("No se pudo almacenar todo el " + string_tipo)
