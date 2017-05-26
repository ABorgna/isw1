class ConfiguracionDeSimulacion(object):

    def __init__(self, *,
            CriterioDeCorte,
            CriterioHabilitacionPozos,
            CriterioEleccionParcelas,
            CriterioDeReinyeccion,
            CriterioDeConstruccionDePlantasSeparadoras,
            CriterioContratacionYUsoDeRigs,
            CriterioConstruccionTanquesDeAgua,
            CriterioConstruccionTanquesDeGas,
            alfa1,
            alfa2,
            maximoVolumenReinyectable,
            costoLitroAgua,
            precioMetroCubicoDePetroleo,
            precioMetroCubicoDeGas,
            concentracionCritica,
            tiposDeRig,
            tiposDePlantaSeparadora,
            tiposDeTanqueDeAgua,
            tiposDeTanqueDeGas):

        self.CriterioDeCorte = CriterioDeCorte
        self.CriterioHabilitacionPozos = CriterioHabilitacionPozos
        self.CriterioEleccionParcelas = CriterioEleccionParcelas
        self.CriterioDeReinyeccion = CriterioDeReinyeccion
        self.CriterioDeConstruccionDePlantasSeparadoras = \
                CriterioDeConstruccionDePlantasSeparadoras
        self.CriterioContratacionYUsoDeRigs = CriterioContratacionYUsoDeRigs
        self.CriterioConstruccionTanquesDeAgua = CriterioConstruccionTanquesDeAgua
        self.CriterioConstruccionTanquesDeGas = CriterioConstruccionTanquesDeGas
        self.alfa1 = alfa1
        self.alfa2 = alfa2
        self.maximoVolumenReinyectable = maximoVolumenReinyectable
        self.costoLitroAgua = costoLitroAgua
        self.precioMetroCubicoDePetroleo = precioMetroCubicoDePetroleo
        self.precioMetroCubicoDeGas = precioMetroCubicoDeGas
        self.concentracionCritica = concentracionCritica
        self.tiposDeRig = tiposDeRig
        self.tiposDePlantaSeparadora = tiposDePlantaSeparadora
        self.tiposDeTanqueDeAgua = tiposDeTanqueDeAgua
        self.tiposDeTanqueDeGas = tiposDeTanqueDeGas
