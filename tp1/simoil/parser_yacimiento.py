import configparser
import inspect
import os
import sys

from yacimiento import *

class ParserDeYacimientos:
    def __init__(self):
        pass

    def _configuracion_default(self):
        config = configparser.ConfigParser()
        config.optionxform = str

        # Default values
        config["yacimiento"] = {}
        config["yacimiento"]["volumenInicial"] = "100000"
        config["yacimiento"]["composicion"] = "0" # TODO: definir composicion

        config["parcela.0"] = {}
        config["parcela.0"]["id"] = "10"
        config["parcela.0"]["presionInicial"] = "25"
        config["parcela.0"]["profundidad"] = "20"
        config["parcela.0"]["resistenciaAExcavacion"] = "0.1"

        return config

    def parsear_archivo(self, filename):
        config = self._configuracion_default()

        # Crear la configuracion por defecto
        if not os.path.isfile(filename):
            with open(filename, 'w') as h:
                config.write(h)

        with open(filename, 'r') as f:
            return self.parsear(f)

    def parsear(self, file):
        config = self._configuracion_default()

        # User values
        config.read_file(file)

        params_parcela = [
            "id",
            "presionInicial",
            "profundidad",
            "resistenciaAExcavacion",
        ]

        # Lista de parselas
        parcelas = []

        for section in config.sections():
            if section.startswith("parcela."):
                p = {}
                for key in params_parcela:
                    p[key] = config.getfloat(section, key)
                parcelas.append(Parcela(**p))

        if not len(parcelas):
            print("No se definieron parcelas!", file=sys.stderr)

        volInicial = config.getfloat("yacimiento", "volumenInicial")

        # TODO leer la composicion
        composicion = config.getfloat("yacimiento", "composicion")

        yacim = Yacimiento(parcelas=parcelas, volumenInicial=volInicial,
                           composicion=composicion)

        return yacim

