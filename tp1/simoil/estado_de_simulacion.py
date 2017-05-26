class EstadoDeSimulacion(object):
    def __init__(self, yacimiento, configuracion):
        self.yacimiento = yacimiento
        self.configuracion = configuracion

        self.diaNumero = 1
        self.costosAcumulados = 0
        self.gananciasAcumuladas = 0

        self.rigsDisponibles = []
        self.plantasDisponibles = []
        self.tanquesDeAguaDisponibles = []
        self.tanquesDeGasDisponibles = []

        self.excavacionesActuales = []

        self.rigsAlquiladosActualmente = {}
        self.plantasEnConstruccion = {}
        self.tanquesDeAguaEnConstruccion = {}
        self.tanquesDeGasEnConstruccion = {}

    def avanzarDia(self):
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
        # y simular todo lo que falte

    def puedeSeguir(self):
        return not self.configuracion.CriterioDeCorte.cortar(self)

    def alquilarRIG(self, modeloDeRIG, diasDeAlquiler, id):
        raise NotImplementedError

    def construirPlantaSeparadora(self, modeloPlanta, id):
        raise NotImplementedError

    def construirTanqueDeAgua(self, modeloTanque, id):
        raise NotImplementedError

    def construirTanqueDeGas(self, modeloTanque, id):
        raise NotImplementedError

    def agregarExcavacion(self, excavacion):
        raise NotImplementedError

    def comprarAgua(self, volumen):
        raise NotImplementedError

    def venderPetroleo(self, volumen):
        raise NotImplementedError

    def venderGas(self, volumen):
        raise NotImplementedError

