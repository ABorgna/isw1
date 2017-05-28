import logging

from estado_de_simulacion import EstadoDeSimulacion


class Simulacion(object):
    def __init__(self, yacimiento, config):
        self.estado = EstadoDeSimulacion(yacimiento, config)

    def simular(self):
        while self.estado.puedeSeguir():
            self.estado.avanzarDia()

        logging.info("Simulacion finalizada")
        logging.info("--------------------------------")
        logging.info("Costo bruto: " + str(self.estado.costosAcumulados))
        logging.info("Ganancia bruta: " + str(self.estado.gananciasAcumuladas))
        logging.info("Ganancia neta: " + str(self.estado.gananciaNeta()))
