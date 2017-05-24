class CriterioDeReinyeccion(object):

class CriterioReinyeccionSoloAguaEnTanques(CriterioEleccionParcelas):
    def __init__(self, presion):
        self.presion_critica = presion

    def decidir_venta_de_gas(estado_de_simulacion):
        for tanque in estado_de_simulacion.tanques_de_gas:
            estado_de_simulacion.vender_gas(tanque.volumen_almacenado)

    def decidir_reinyeccion(estado_de_simulacion):
        hay_que_reinyectar = False
        for pozo in estado_de_simulacion.yacimiento.pozos_perforados:
            if pozo.presion_actual < presion_critica:
                hay_que_reinyectar = True

        if hay_que_reinyectar:
            volumen_total_agua_almacenada = 0

            for tanque in estado_de_simulacion.tanques_de_agua:
                volumen_total_agua_almacenada += tanque.volumen_almacenado

            estado_de_simulacion.yacimiento.reinyectar(volumen_total_agua_almacenada, 0)
