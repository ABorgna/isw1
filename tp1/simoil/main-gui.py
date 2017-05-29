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

        self.init_menu_bar(self.container)

        self.panels = gui.Widget()
        self.panels.style["align-items"] = "top"
        self.container.append(self.panels)

        self.init_input_container(self.panels)
        self.init_output_container(self.panels)
        self.init_log_container(self.panels)

        self.show_menu_item("in")

        # returning the root widget
        return self.container

    def init_input_container(self, container):
        self.input_container = gui.Widget()
        container.append(self.input_container)

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

    def init_output_container(self, container):
        self.output_container_container = gui.VBox()
        container.append(self.output_container_container)

        control_container = gui.HBox()

        avanzar_dia_bt = gui.Button('Avanzar dia')
        avanzar_dia_bt.set_on_click_listener(self.on_avanzar_dia_bt_pressed)
        control_container.append(avanzar_dia_bt)

        avanzar_final_bt = gui.Button('Avanzar hasta el final')
        avanzar_final_bt.set_on_click_listener(self.on_avanzar_final_bt_pressed)
        control_container.append(avanzar_final_bt)

        self.output_container_container.append(control_container)

        self.output_container = gui.HBox()
        self.output_container_container.append(self.output_container)

    def init_log_container(self, container):
        self.log_container = gui.VBox()
        self.log_container.style["align-items"] = "left"
        container.append(self.log_container)

    # listener function
    def on_simu_button_pressed(self, widget):
        self.input_error_lbl.set_text("")

        try:
            yacim_parser = ParserDeYacimientos()
            yacim_file = self.input_yacim_file.get_value().strip()
            if not len(yacim_file):
                self.input_error_lbl.set_text("Ingrese un archivo de yacimiento")
                return
            yacimiento = yacim_parser.parsear_archivo(yacim_file)

            config_parser = ParserDeConfiguracionDeSimulacion()
            config_file = self.input_config_file.get_value().strip()
            if len(config_file):
                configuracion = config_parser.parsear_archivo(config_file)
            else:
                configuracion = None

            assert(yacimiento is not None)
            assert(configuracion is not None)
        except:
            self.input_error_lbl.set_text(
                    "Error al leer los archivos")
            raise

        try:
            crits = {}
            for crit, select in self.input_crits_selects.items():
                cls_name = select.get_value()
                cls = self.input_crits[crit][cls_name]

                cparams = self.input_crits_params[crit].get_value().split()
                cparams = map(float, cparams)

                try:
                    obj = cls(*cparams)
                except TypeError:
                    self.input_error_lbl.set_text(
                            "Parametros invalidos para el criterio " + crit)
                    return

                crits[crit] = obj

            params = {}
            for p, select in self.input_params_select.items():
                val = select.get_value()
                try:
                    val = float(val)
                except:
                    val = None
                params[p] = val

            # TODO
            tipos = {
                    "tiposDeRig": [ModeloDeRIG(20,1,1,2)],
                    "tiposDePlantaSeparadora": [ModeloDePlantaSeparadora(100,2,100)],
                    "tiposDeTanqueDeAgua": [ModeloDeTanque(100,2,100)],
                    "tiposDeTanqueDeGas": [ModeloDeTanque(100,2,100)]
            }

            if configuracion is None:
                configuracion = ConfiguracionDeSimulacion(**params, **crits, **tipos)
            else:
                for k,v in params.items():
                    if v is not None:
                        setattr(configuracion, k, v)

                for k,v in crits.items():
                    setattr(configuracion, k, v)

        except:
            self.input_error_lbl.set_text(
                    "Error al parsear la entrada")
            raise

        self.show_menu_item("out")
        self.comenzarSimulacion(yacimiento, configuracion)

    def comenzarSimulacion(self, yacimiento, configuracion):
        self.estado_de_simulacion = EstadoDeSimulacion(yacimiento, configuracion)

        self.input_container.set_enabled(False)
        self.output_container_container.set_enabled(True)

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

        # Metemos el log completo
        self.log_container.empty()
        log = self.log_stream.getvalue()
        for line in log.splitlines():
            self.log_container.append(gui.Label(line))

    def actualizarDibujo(self):
        log = self.log_stream.getvalue()
        estado = self.estado_de_simulacion
        log_del_dia = log.split('----')[-1]   # TODO: eficiencia luego
        self.dibujar(estado, log_del_dia)

        # Completar el panel del log completo
        for line in log_del_dia.splitlines():
            self.log_container.append(gui.Label(line))

    ### Cosas del input
    def init_input_yacimiento(self, container):
        row = gui.HBox()

        row.append(gui.Label("Archivo de configuracion del yacimiento"))

        self.input_yacim_file = gui.TextInput()
        self.input_yacim_file.set_value("./pruebas/grande/yacimiento.cfg")
        self.input_yacim_file.style["text-align"] = "right"
        row.append(self.input_yacim_file)

        container.append(row)

        row = gui.HBox()

        row.append(gui.Label("Archivo de configuración de parámetros (opcional)"))

        self.input_config_file = gui.TextInput()
        self.input_config_file.set_value("./pruebas/grande/config.cfg")
        self.input_config_file.style["text-align"] = "right"
        row.append(self.input_config_file)

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
        def dibujar_tanques(tanques, string_tipo):
            for tanque in tanques:
                ratio = tanque.volumenAlmacenado / tanque.capacidad
                perc = int(ratio * 100)
                barra = '['
                for i in range(100):
                    if i < perc:
                        barra += '='
                    else:
                        barra += '-'
                barra += ']'
                estado_container.append(gui.Label("Tanque de {} número {} ".format(string_tipo, tanque.id) + barra))

        dibujar_tanques(estado.tanquesDeAguaDisponibles, "agua")
        dibujar_tanques(estado.tanquesDeGasDisponibles, "gas")

        # Mapa de pozos habilitados
        pozos = estado.yacimiento.pozosPerforados
        def habilitado(pozo):
            for linea in log_del_dia.splitlines():
                if linea.startswith("Se extrajeron"):
                    if pozo.id == int(linea.split()[-1]):
                        return True
            return False
        str_pozos = 'Pozos habilitados: '
        for pozo in pozos:
            if habilitado(pozo):
                str_pozos += 'X '
            else:
                str_pozos += 'O '
        estado_container.append(gui.Label(str_pozos))


        # esta version no estaba andando, voy a empezar por una mas simple
        # perforados = {}

        # estado_container.append(gui.Label("-Pozos habilitados:"))
        # cantidad_de_pozos = len(estado.yacimiento.pozosPerforados)

        # for linea in log_del_dia.splitlines():
        #     if linea.startswith("Se extrajeron"):
        #         perforados[int(linea.split()[-1])] = "X "

        # for pozo_id in range(1,cantidad_de_pozos+1):
        #     if pozo_id not in perforados:
        #         perforados[pozo_id] = "O "

        # cantidad_filas = cantidad_columnas = m.ceil((m.sqrt(cantidad_de_pozos)))
        # contador_pozos = 0

        # for fila in range(cantidad_filas):
        #     string_fila = ""
        #     for columna in range(cantidad_columnas):
        #         string_fila += perforados[contador_pozos]
        #         contador_pozos += 1
        #         if contador_pozos == cantidad_de_pozos:
        #             break
        #     # truquito para salir de nested loops con break
        #     else:
        #         estado_container.append(gui.Label(string_fila))
        #         continue  # executed if the loop ended normally (no break)
        #     break # executed if 'continue' was skipped (break)

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

    # Menu de paneles
    def init_menu_bar(self, container):
        bar = gui.HBox()
        bar.style["border-bottom"] = "1px solid #ddd"
        bar.style["width"] = "100%"
        bar.style["align-items"] = "left"
        bar.style["margin-bottom"] = "20px"
        bar.style["justify-content"] = "start"
        container.append(bar)

        title = gui.Label("SimOil")
        title.style["font-size"] = "18px"
        title.style["margin-right"] = "18px"
        bar.append(title)

        menu = gui.Menu()
        menu.style["display"] = "flex"
        bar.append(menu)

        menu_in = gui.MenuItem("Nueva simulacion", id="in")
        menu_out = gui.MenuItem("Avanzar simulacion", id="out")
        menu_log = gui.MenuItem("Logs simulacion", id="log")

        menu.append(menu_in)
        menu.append(menu_out)
        menu.append(menu_log)

        menu_in.style["width"] = "350px"
        menu_out.style["width"] = "350px"
        menu_log.style["width"] = "350px"

        menu_in.set_on_click_listener(self.on_nav_menu_item_click)
        menu_out.set_on_click_listener(self.on_nav_menu_item_click)
        menu_log.set_on_click_listener(self.on_nav_menu_item_click)

    def on_nav_menu_item_click(self, widget):
        id = widget.attributes["id"]
        self.show_menu_item(id)

    def show_menu_item(self, item):
        self.input_container.style["display"] = "none"
        self.output_container_container.style["display"] = "none"
        self.log_container.style["display"] = "none"

        if item == "in":
            self.input_container.style["display"] = ""
        if item == "out":
            self.output_container_container.style["display"] = ""
        if item == "log":
            self.log_container.style["display"] = ""


# starts the webserver
#remi.start(SimOil, standalone=True)
remi.start(SimOil)
