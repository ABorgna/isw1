#!/usr/bin/python3

import argparse
import inspect
import logging
import sys

import criterios
from parser_configuracion import ParserDeConfiguracionDeSimulacion
from parser_yacimiento import ParserDeYacimientos
from simulacion import Simulacion


if __name__ == "__main__":

    # Parse any arguments
    parser = argparse.ArgumentParser(description="Simulador de yacimientos")

    parser.add_argument('-c', help='archivo de configuracion de parámetros',
            nargs='?', type=str, default='config.cfg', dest='configfile')
    parser.add_argument('-y', help='archivo de configuracion de yacimiento',
            nargs='?', type=str, default='yacimiento.cfg', dest='yacimfile')
    parser.add_argument('-o', help='log file', nargs='?',
            type=argparse.FileType('w'),
            default=sys.stdout, dest='outfile')

    args = parser.parse_args()

    # Init the logger
    fmt = "%(message)s"
    logging.basicConfig(stream=args.outfile, level=logging.INFO, format=fmt)

    configParser = ParserDeConfiguracionDeSimulacion()
    config = configParser.parsear_archivo(args.configfile)

    yacimParser = ParserDeYacimientos()
    yacim = yacimParser.parsear_archivo(args.yacimfile)

    if config is None:
        # :(
        print("Configuracion de parámetros inválida, terminando", file=sys.stderr)
        sys.exit(1)

    if yacim is None:
        # :(
        print("Configuracion de yacimiento inválida, terminando", file=sys.stderr)
        sys.exit(2)

    simulacion = Simulacion(yacim, config)
    simulacion.simular()
