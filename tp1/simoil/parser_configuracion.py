import configparser
import inspect
import os
import sys

import criterios
from configuracion_de_simulacion import ConfiguracionDeSimulacion

class ParserDeConfiguracionDeSimulacion:
    def __init__(self):
        pass

    def _configuracion_default(self):
        config = configparser.ConfigParser()
        config.optionxform = str

        # Default values
        config["criterios"] = {}
        config["criterios"]["CriterioDeCorte"] = ""
        config["criterios"]["CriterioHabilitacionPozos"] = ""
        config["criterios"]["CriterioEleccionParcelas"] = ""
        config["criterios"]["CriterioDeReinyeccion"] = ""
        config["criterios"]["CriterioDeConstruccionDePlantasSeparadoras"] = ""
        config["criterios"]["CriterioContratacionYUsoDeRigs"] = ""
        config["criterios"]["CriterioConstruccionTanquesDeAgua"] = ""
        config["criterios"]["CriterioConstruccionTanquesDeGas"] = ""

        return config

    def parsear_archivo(self, filename):
        config = self._configuracion_default()

        # Crear la configuracion por defecto
        if not os.path.isfile(filename):
            with open(filename, 'w') as h:
                config.write(h)

        with open(filename, 'r') as f:
            self.parsear(f)

    def parsear(self, file):
        config = self._configuracion_default()

        # User values
        config.read_file(file)

        if(not self._parsed_crits_to_classes(config)):
            return None

        # TODO: parsear las demas variables

        return None

        configuracionDeSimulacion = \
            ConfiguracionDeSimulacion(**config['criterios'])

        return configuracionDeSimulacion

    # Metodos internos

    ''' Sobreescribe los nombres de clases y parametros de criterios
        leidos en la configuracion con los objetos ya creados
    '''
    def _parsed_crits_to_classes(self, config):
        error = False

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
            if len(criterioYParams):
                criterio = criterioYParams.pop()
                params = map(float,criterioYParams)

            if len(criterioYParams) and criterio in concClasses:
                config['criterios'][absClass_name] = criterio(*params)
            else:
                concClassesNames = "[" + ", ".join(concClasses.keys()) + "]"
                print("invalid", absClass_name + ",",
                      "choose one of", concClassesNames, file=sys.stderr)
                error = True
                continue

        crits = {k:v for k,v in config['criterios'].items()
                                           if v is not str}
        return not error

