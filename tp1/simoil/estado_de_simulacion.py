class EstadoDeSimulacion(object):
    def __init__(self):
        self.excavaciones_actuales = {}
        self.plantas_separadoras = []

    def avanzar_dia():
        self.criterio_reinyeccion.decidir_ventas(self)

        self.criterio_parcelas.decidir_proximas_parcelas(self)

        self.criterio_de_rigs.contratar_rigs(self)
        self.criterio_de_rigs.excavar(self)

        self.criterio_plantas.construir_plantas(self)

        self.criterio_tanques_de_agua.construir_tanques_de_agua(self)

        self.criterio_tanques_de_gas.construir_tanques_de_gas(self)

        self.criterio_habilitacion_pozos.extraer(self)

        self.criterio_reinyeccion.decidir_reinyeccion(self)

    def terminar(self):
        return self.criterio_corte.terminar(self)

    def vender_petroleo(self, vol_petroleo):
        pass
