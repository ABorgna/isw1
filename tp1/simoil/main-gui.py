#!/usr/bin/python3
import remi
import remi.gui as gui

from estado_de_simulacion import EstadoDeSimulacion

class SimOil(remi.App):
    def __init__(self, *args):
        super(SimOil, self).__init__(*args)

    def main(self):
        self.container = gui.VBox(width = 120, height = 400)

        # Se crea cuando se aprieta el boton
        self.estado_simulacion = None

        self.init_input_container()
        self.init_output_container()

        # returning the root widget
        return self.container

    def init_input_container(self):
        self.input_container = gui.Widget(width = 120, height = 400)
        self.container.append(self.input_container)

        self.run_bt = gui.Button('Simular')

        # setting the listener for the onclick event of the button
        self.run_bt.set_on_click_listener(self.on_run_button_pressed)

        self.input_container.append(self.run_bt)

    def init_output_container(self):
        self.output_container = gui.Widget(width = 120, height = 400)
        self.container.append(self.output_container)

    # listener function
    def on_run_button_pressed(self, widget):
        pass
        #self.lbl.set_text('Button pressed!')
        #self.bt.set_text('Hi!')

# starts the webserver
remi.start(SimOil, standalone=True)

