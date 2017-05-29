#!/usr/bin/python3
import inspect
import remi
import remi.gui as gui
import sys

from configuracion_de_simulacion import ConfiguracionDeSimulacion
import criterios
from estado_de_simulacion import EstadoDeSimulacion
from yacimiento import Yacimiento

class SimOil(remi.App):
    def __init__(self, *args):
        super(SimOil, self).__init__(*args)

    def main(self):
        self.container = gui.VBox()

        # Se crea cuando se aprieta el boton
        self.estado_simulacion = None

        self.init_input_container()
        self.init_output_container()

        # returning the root widget
        return self.container

    def init_input_container(self):
        self.input_container = gui.Widget()
        self.container.append(self.input_container)

        self.init_input_params(self.input_container)
        self.init_input_criterios(self.input_container)

        self.input_simular_bt = gui.Button('Simular')

        # setting the listener for the onclick event of the button
        self.input_simular_bt.set_on_click_listener(self.on_simu_button_pressed)

        self.input_container.append(self.input_simular_bt)

    def init_output_container(self):
        self.output_container = gui.VBox()
        self.container.append(self.output_container)

    # listener function
    def on_simu_button_pressed(self, widget):
        try:
            crits = {}
            for crit, select in self.input_crits_selects.items():
                cls_name = select.get_value()
                cls = self.input_crits[crit][cls_name]
                cparams = self.input_crits_params[crit].split()
                cparams = map(float, cparams)

                obj = cls(*cparams)
                crits[crit] = obj

            print(crits.keys())

            params = {}
            for p, select in self.input_params_select.items():
                params[p] = select.get_value()

            # TODO
            tipos = {
                    "tiposDeRig": [],
                    "tiposDePlantaSeparadora": [],
                    "tiposDeTanqueDeAgua": [],
                    "tiposDeTanqueDeGas": []
            }

            configuracion = ConfiguracionDeSimulacion(**params, **crits, **tipos)

            # TODO
            yacimiento = None

            estado = EstadoDeSimulacion(yacimiento, configuracion)

            ## llamar a algo con el estado

        except Exception as e:
            print("Error parsing input", file=sys.stderr)
            print(e, file=sys.stderr)

    ### Cosas del input
    def init_input_params(self, container):
        self.input_params_select = {}

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

        for p in param_names:
            row = gui.HBox()
            row.append(gui.Label(p))

            input = gui.TextInput(hint=p)
            self.input_params_select[p] = input
            row.append(input)

            container.append(row)

    def init_input_criterios(self, container):
        self.input_crits_selects = {}
        self.input_crits = {}
        self.input_crits_params = {}

        for mod_name, module in inspect.getmembers(criterios, inspect.ismodule):
            row = gui.HBox()

            filter_abs = lambda x: inspect.isclass(x) \
                                   and inspect.isabstract(x) \
                                   and x.__module__ == 'criterios.'+mod_name
            filter_conc = lambda x: inspect.isclass(x) \
                                   and not inspect.isabstract(x) \
                                   and x.__module__ == 'criterios.'+mod_name

            absClasses = inspect.getmembers(module, filter_abs)
            absClass_name, absClass = absClasses[0];
            concClasses = dict(inspect.getmembers(module, filter_conc));

            row.append(gui.Label(absClass_name))

            dropdown = gui.DropDown()
            self.input_crits_selects[absClass_name] = dropdown
            row.append(dropdown)

            critParams = gui.TextInput(hint="Crit params")
            self.input_crits_params[absClass_name] = critParams
            row.append(critParams)

            self.input_crits[absClass_name] = {}
            for critName, critClass in concClasses.items():
                dropdown.append(critName)
                self.input_crits[absClass_name][critName] = critClass

            container.append(row)

# starts the webserver
#remi.start(SimOil, standalone=True)
remi.start(SimOil)

