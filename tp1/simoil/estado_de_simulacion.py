class EstadoDeSimulacion(object):
    def __init__(self, yacimiento, configuracion):
        self.excavaciones_actuales = {}
        self.rigs_contratados = []
        self.plantas_separadoras = []
        self.configuracion = configuracion
        self.yacimiento = yacimiento

    def avanzar_dia():
        self.configuracion.criterio_reinyeccion.decidir_venta_de_gas(self)

        self.configuracion.criterio_parcelas.decidir_proximas_parcelas(self)

        self.configuracion.criterio_de_rigs.contratar_rigs(self)
        self.configuracion.criterio_de_rigs.excavar(self)

        self.configuracion.criterio_plantas.construir_plantas(self)

        self.configuracion.criterio_tanques_de_agua.construir_tanques_de_agua(self)

        self.configuracion.criterio_tanques_de_gas.construir_tanques_de_gas(self)

        self.configuracion.criterio_habilitacion_pozos.extraer(self)

        self.configuracion.criterio_reinyeccion.decidir_reinyeccion(self)

    def terminar(self):
        return self.criterio_corte.terminar(self)

    def vender_petroleo(self, vol_petroleo):
        pass