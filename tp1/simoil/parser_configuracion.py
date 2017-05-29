import configparser
import inspect
import os
import sys

import criterios
from configuracion_de_simulacion import ConfiguracionDeSimulacion
from assets.modelos import *

class ParserDeConfiguracionDeSimulacion:
    def __init__(self):
        pass

    def _configuracion_default(self):
        config = configparser.ConfigParser()
        config.optionxform = str

        # Default values
        config["criterios"] = {}
        config["criterios"]["CriterioDeCorte"] = \
                "CortePorDiaFijo 120"
        config["criterios"]["CriterioHabilitacionPozos"] = \
                "CriterioHabilitacionTotal"
        config["criterios"]["CriterioEleccionParcelas"] = \
                "EleccionParcelasMayorPresion 10"
        config["criterios"]["CriterioDeReinyeccion"] = \
                "CriterioReinyeccionSoloAguaEnTanques 0.1"
        config["criterios"]["CriterioDeConstruccionDePlantasSeparadoras"] = \
                "CriterioDeAhorroDePlantas"
        config["criterios"]["CriterioContratacionYUsoDeRigs"] = \
                "CriterioContratacionYUsoDeRigsMinimoTiempo"
        config["criterios"]["CriterioConstruccionTanquesDeAgua"] = \
                "CriterioDeAhorroDeTanquesDeAgua"
        config["criterios"]["CriterioConstruccionTanquesDeGas"] = \
                "CriterioDeAhorroDeTanquesDeGas"

        config["parametros"] = {}
        config["parametros"]["alfa1"] = "0.1"
        config["parametros"]["alfa2"] = "0.01"
        config["parametros"]["maximoVolumenReinyectable"] = "100"
        config["parametros"]["costoLitroAgua"] = "10"
        config["parametros"]["costoLitroCombustible"] = "10"
        config["parametros"]["precioMetroCubicoDePetroleo"] = "100"
        config["parametros"]["precioMetroCubicoDeGas"] = "10"
        config["parametros"]["concentracionCritica"] = "0.35"

        config["rig.0"] = {}
        config["rig.0"]["metrosDiariosExcavados"] = "10"
        config["rig.0"]["consumoDiario"] = "25"
        config["rig.0"]["costoDeAlquilerPorDia"] = "2500"
        config["rig.0"]["diasDeAlquilerMinimo"] = "5"

        config["pSeparadora.0"] = {}
        config["pSeparadora.0"]["volumenDiarioSeparable"] = "1000"
        config["pSeparadora.0"]["diasDeConstruccion"] = "2"
        config["pSeparadora.0"]["costoDeConstruccion"] = "2500"

        config["tAgua.0"] = {}
        config["tAgua.0"]["volumenDeAlmacenamiento"] = "10000"
        config["tAgua.0"]["diasDeConstruccion"] = "2"
        config["tAgua.0"]["costoDeConstruccion"] = "2500"

        config["tGas.0"] = {}
        config["tGas.0"]["volumenDeAlmacenamiento"] = "10000"
        config["tGas.0"]["diasDeConstruccion"] = "2"
        config["tGas.0"]["costoDeConstruccion"] = "2500"

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

        crits = self._parse_criterios(config)
        params = self._parse_params(config)

        if crits is None or params is None:
            return None

        configuracionDeSimulacion = \
            ConfiguracionDeSimulacion(**crits, **params)

        return configuracionDeSimulacion

    # Metodos internos

    ''' Devuelve todos los parametros parseados
    '''
    def _parse_params(self, config):
        params = {}

        param_names = [
            "alfa1",
            "alfa2",
            "maximoVolumenReinyectable",
            "costoLitroAgua",
            "costoLitroCombustible",
            "precioMetroCubicoDePetroleo",
            "precioMetroCubicoDeGas",
            "concentracionCritica",
        ]

        params_rig = [
            "metrosDiariosExcavados",
            "consumoDiario",
            "costoDeAlquilerPorDia",
            "diasDeAlquilerMinimo",
        ]

        params_pSeparadora = [
            "volumenDiarioSeparable",
            "diasDeConstruccion",
            "costoDeConstruccion",
        ]

        params_tanque = [
            "volumenDeAlmacenamiento",
            "diasDeConstruccion",
            "costoDeConstruccion",
        ]

        for name in param_names:
            params[name] = config.getfloat("parametros", name)

        # Listas de objetos
        rigs = []
        separadoras = []
        tanques_agua = []
        tanques_gas = []

        for section in config.sections():
            if section.startswith("rig."):
                p = {}
                for key in params_rig:
                    p[key] = config.getint(section, key)
                rigs.append(ModeloDeRIG(**p))
            elif section.startswith("pSeparadora."):
                p = {}
                for key in params_pSeparadora:
                    p[key] = config.getint(section, key)
                separadoras.append(ModeloDePlantaSeparadora(**p))
            elif section.startswith("tAgua."):
                p = {}
                for key in params_tanque:
                    p[key] = config.getint(section, key)
                tanques_agua.append(ModeloDeTanque(**p))
            elif section.startswith("tGas."):
                p = {}
                for key in params_tanque:
                    p[key] = config.getint(section, key)
                tanques_gas.append(ModeloDeTanque(**p))

        params["tiposDeRig"] = rigs
        params["tiposDePlantaSeparadora"] = separadoras
        params["tiposDeTanqueDeAgua"] = tanques_agua
        params["tiposDeTanqueDeGas"] = tanques_gas

        return params

    ''' Crea los objetos correspondientes a partir de los nombres de clases
        y parametros de criterios leidos en la configuracion
    '''
    def _parse_criterios(self, config):
        error = False
        crits = {}

        for mod_name, module in inspect.getmembers(criterios, inspect.ismodule):
            filter_abs = lambda x: inspect.isclass(x) \
                                   and inspect.isabstract(x) \
                                   and x.__module__ == 'criterios.'+mod_name
            filter_conc = lambda x: inspect.isclass(x) \
                                   and not inspect.isabstract(x) \
                                   and x.__module__ == 'criterios.'+mod_name

            absClasses = inspect.getmembers(module, filter_abs)
            if not len(absClasses):
                print(mod_name, "does not have any abstract class",
                        file=sys.stderr)
                continue

            absClass_name, absClass = absClasses[0];
            if absClass_name not in config["criterios"]:
                print(absClass_name, "not found in config", file=sys.stderr)
                error = True
                continue

            concClasses = dict(inspect.getmembers(module, filter_conc));

            criterioYParams = config["criterios"][absClass_name].split()
            criterio = None
            if len(criterioYParams):
                criterio = criterioYParams.pop(0)
                params = map(float,criterioYParams)

            if criterio is not None and criterio in concClasses:
                crits[absClass_name] = concClasses[criterio](*params)
            else:
                concClassesNames = "[" + ", ".join(concClasses.keys()) + "]"
                print("invalid", absClass_name + ",",
                      "" if criterio is None else "'" + criterio + "'",
                      "choose one of", concClassesNames, file=sys.stderr)
                error = True
                continue

        return crits if not error else None

