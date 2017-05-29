#!/usr/bin/python3
import inspect
import io
import logging
import remi
import remi.gui as gui
import sys
import math as m

from assets.modelos import *
from configuracion_de_simulacion import ConfiguracionDeSimulacion
import criterios
from estado_de_simulacion import EstadoDeSimulacion
from simulacion import Simulacion
from parser_configuracion import ParserDeConfiguracionDeSimulacion
from parser_yacimiento import ParserDeYacimientos
from yacimiento import Yacimiento

class SimOil(remi.App):
    def __init__(self, *args):
        super(SimOil, self).__init__(*args)

    def main(self):
        self.container = gui.VBox()
        self.container.style["align-items"] = "top"

        # Se crea cuando se aprieta el boton
        self.estado_simulacion = None

        self.init_input_container()

        # returning the root widget
        return self.container

    def init_input_container(self):
        self.input_container = gui.Widget()
        self.container.append(self.input_container)

        self.init_input_yacimiento(self.input_container)
        self.init_input_params(self.input_container)
        self.init_input_criterios(self.input_container)

        row = gui.HBox()
        self.input_simular_bt = gui.Button('Simular')
        self.input_simular_bt.set_on_click_listener(self.on_simu_button_pressed)
        row.append(self.input_simular_bt)

        self.input_error_lbl = gui.Label("")
        self.input_error_lbl.style["color"] = '#770c0c'
        row.append(self.input_error_lbl)

        self.input_container.append(row)

    # listener function
    def on_simu_button_pressed(self, widget):
        self.input_error_lbl.set_text("")

        # try:
        #     crits = {}
        #     for crit, select in self.input_crits_selects.items():
        #         cls_name = select.get_value()
        #         cls = self.input_crits[crit][cls_name]

        #         cparams = self.input_crits_params[crit].get_value().split()
        #         cparams = map(float, cparams)

        #         try:
        #             obj = cls(*cparams)
        #         except TypeError:
        #             self.input_error_lbl.set_text(
        #                     "Parametros invalidos para el criterio " + crit)
        #             return

        #         crits[crit] = obj

        #     params = {}
        #     for p, select in self.input_params_select.items():
        #         val = select.get_value()
        #         try:
        #             val = float(val)
        #         except:
        #             val = 1
        #         params[p] = val

        #     # TODO
        #     tipos = {
        #             "tiposDeRig": [ModeloDeRIG(20,1,1,2)],
        #             "tiposDePlantaSeparadora": [ModeloDePlantaSeparadora(100,2,100)],
        #             "tiposDeTanqueDeAgua": [ModeloDeTanque(100,2,100)],
        #             "tiposDeTanqueDeGas": [ModeloDeTanque(100,2,100)]
        #     }

        #     configuracion = ConfiguracionDeSimulacion(**params, **crits, **tipos)

        #     yacim_parser = ParserDeYacimientos()
        #     yacimFile = self.input_yacim_file.get_value()
        #     yacimiento = yacim_parser.parsear_archivo(yacimFile)

        # except:
        #     self.input_error_lbl.set_text(
        #             "Error al parsear la entrada")
        #     raise

        configuracion = ParserDeConfiguracionDeSimulacion().parsear_archivo('config.cfg')
        yacimiento = ParserDeYacimientos().parsear_archivo('yacimiento.cfg')

        self.comenzarSimulacion(yacimiento, configuracion)

    def comenzarSimulacion(self, yacimiento, configuracion):
        self.estado_de_simulacion = EstadoDeSimulacion(yacimiento, configuracion)

        self.container.empty()

        control_container = gui.HBox()

        avanzar_dia_bt = gui.Button('Avanzar dia')
        avanzar_dia_bt.set_on_click_listener(self.on_avanzar_dia_bt_pressed)
        control_container.append(avanzar_dia_bt)

        avanzar_final_bt = gui.Button('Avanzar hasta el final')
        avanzar_final_bt.set_on_click_listener(self.on_avanzar_final_bt_pressed)
        control_container.append(avanzar_final_bt)

        self.container.append(control_container)
        self.output_container = gui.HBox()
        self.container.append(self.output_container)

        # Setear el logger con nuestro stream
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger = logging.getLogger("simoil")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        self.log_stream = log_stream
        self.actualizarDibujo()

    def on_avanzar_dia_bt_pressed(self, widget):
        self.estado_de_simulacion.avanzarDia()
        self.actualizarDibujo()

    def on_avanzar_final_bt_pressed(self, widget):
        while self.estado_de_simulacion.puedeSeguir():
            self.estado_de_simulacion.avanzarDia()
        self.actualizarDibujo()

    def actualizarDibujo(self):
        log = self.log_stream.getvalue()
        estado = self.estado_de_simulacion
        log_del_dia = log.split('----')[-1]   # TODO: eficiencia luego
        self.dibujar(estado, log_del_dia)

    ### Cosas del input
    def init_input_yacimiento(self, container):
        row = gui.HBox()

        row.append(gui.Label("Archivo de configuracion del yacimiento"))

        self.input_yacim_file = gui.TextInput()
        self.input_yacim_file.set_value("yacimiento.cfg")
        self.input_yacim_file.style["text-align"] = "right"
        row.append(self.input_yacim_file)

        container.append(row)

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
            input.style["text-align"] = "right"
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

            label = gui.Label(absClass_name)
            label.style["flex-grow"] = "100"
            label.style["width"] = "auto"
            row.append(label)

            dropdown = gui.DropDown()
            dropdown.style["flex-grow"] = "1"
            dropdown.style["width"] = "auto"
            self.input_crits_selects[absClass_name] = dropdown
            row.append(dropdown)

            critParams = gui.TextInput(hint="Crit params")
            critParams.style["text-align"] = "right"
            critParams.style["width"] = "80px"
            self.input_crits_params[absClass_name] = critParams
            row.append(critParams)

            self.input_crits[absClass_name] = {}
            for critName, critClass in concClasses.items():
                dropdown.append(critName)
                self.input_crits[absClass_name][critName] = critClass

            dropdown.set_value(next(iter(concClasses.keys())))

            container.append(row)

    def dibujar(self, estado, log_del_dia):
        self.output_container.empty()

        estado_container = gui.VBox()
        log_container = gui.VBox()
        self.output_container.append(estado_container)
        self.output_container.append(log_container)

        # muestro el log del dia
        log_container.style["align-items"] = "left"
        self.output_container.append(log_container)
        for line in log_del_dia.splitlines():
            log_container.append(gui.Label(line))

        # informacion financiera
        estado_container.append(
            gui.Label('Ingresos: $%d Costos: $%d Balance: $%d' %
                      (estado.gananciasAcumuladas, estado.costosAcumulados,
                       estado.gananciaNeta())))

        # Dibujar tanques
        estado_container.append(gui.Label("Estado de tanques al finalizar el día:"))

        def dibujar_tanques(tanques, string_tipo):
            for tanque in tanques:
                carga = int(10*tanque.volumenAlmacenado/tanque.capacidad)
                barra = "["
                for x in range(carga):
                    barra += "█ "
                for x in range(10-carga):
                    barra += "  "
                barra += "]"
                estado_container.append(gui.Label("Tanque de {} número {} cargado en {}/10: ".format(string_tipo, tanque.id, carga) + barra))

        dibujar_tanques(estado.tanquesDeAguaDisponibles, "agua")
        dibujar_tanques(estado.tanquesDeGasDisponibles, "gas")

        return


        # Mapa de pozos habilitados
        self.output_textbox.append(gui.Label("-Pozos habilitados:"))
        cantidad_de_pozos = len(estado.yacimiento.pozosPerforados)

        for linea in log_del_dia.splitlines():
            if linea.startswith("Se extrajeron"):
                perforados[int(linea.split[-1])] = "X "

        for pozo_id in range(1,cantidad_de_pozos+1):
            if pozo_id not in perforados:
                perforados[pozo_id] = "O "

        cantidad_filas = cantidad_columnas = m.ceil((m.sqrt(cantidad_de_pozos)))
        contador_pozos = 0

        for fila in range(cantidad_filas):
            string_fila = ""
            for columna in range(cantidad_columnas):
                string_fila += perforados[contador_pozos]
                contador_pozos += 1
                if contador_pozos == cantidad_de_pozos:
                    break
            # truquito para salir de nested loops con break
            else:
                self.output_textbox.append(gui.Label(string_fila))
                continue  # executed if the loop ended normally (no break)
            break # executed if 'continue' was skipped (break)

    ### Simular hasta el final
    def simularTodo(self, yacimiento, configuracion):
        # Setear el logger con nuestro stream
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger = logging.getLogger("simoil")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Correr la simulacion
        sim = Simulacion(yacimiento, configuracion)
        sim.simular()

        # Mostrar la salida
        log = log_stream.getvalue()
        self.output_textbox.empty()
        for line in log.splitlines():
            self.output_textbox.append(gui.Label(line))

# starts the webserver
#remi.start(SimOil, standalone=True)
remi.start(SimOil)
