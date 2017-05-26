class ConfiguracionDeSimulacion(object):

    CRITERIOS = [
        "CriterioDeCorte",
        "CriterioHabilitacionPozos",
        "CriterioEleccionParcelas",
        "CriterioDeReinyeccion",
        "CriterioDeConstruccionDePlantasSeparadoras",
        "CriterioContratacionYUsoDeRigs",
        "CriterioConstruccionTanquesDeAgua",
        "CriterioConstruccionTanquesDeGas",
    ]

    PARAMS = [
        "alfa1",
        "alfa2",
        "maximoVolumenReinyectable",
        "costoLitroAgua",
        "precioMetroCubicoDePetroleo",
        "precioMetroCubicoDeGas",
        "composicionCritica",
        "composicionCritica",
    ]

    OBJ_LISTS = [
        "tiposDeRig",
        "tiposDePlantaSeparadora",
        "tiposDeTanqueDeAgua",
        "tiposDeTanqueDeGas",
    ]

    def __init__(self, **kwargs):
        for key in self.CRITERIOS + self.PARAMS + self.OBJ_LISTS:
            setattr(self, key, kwargs.get(key))
            if kwargs.get(key) is None:
                raise ValueError("Invalid " + key)

