import logging

from estado_de_simulacion import EstadoDeSimulacion


class Simulacion(object):
    def __init__(self, yacimiento, config):
        self.estado = EstadoDeSimulacion(yacimiento, config)

    def simular(self):
        while self.estado.puedeSeguir():
            self.estado.avanzarDia()

        logging.getLogger("simoil").info("Simulacion finalizada")
        logging.getLogger("simoil").info("--------------------------------")
        logging.getLogger("simoil").info("Costo bruto: " + str(self.estado.costosAcumulados))
        logging.getLogger("simoil").info("Ganancia bruta: " + str(self.estado.gananciasAcumuladas))
        logging.getLogger("simoil").info("Ganancia neta: " + str(self.estado.gananciaNeta()))
