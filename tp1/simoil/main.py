#!/bin/env python3

import argparse
import inspect
import logging
import sys

import criterios
from parser_configuracion import ParserDeConfiguracionDeSimulacion

def simular(estado_de_simulacion):
    pass

if __name__ == "__main__":

    # Parse any arguments
    parser = argparse.ArgumentParser(description="Simulador de yacimientos")

    parser.add_argument('-c', help='config file', nargs='?',
            type=str, default='config.cfg', dest='infile')
    parser.add_argument('-o', help='log file', nargs='?',
            type=argparse.FileType('w'),
            default=sys.stdout, dest='outfile')

    args = parser.parse_args()

    # Init the logger
    logging.basicConfig(stream=args.outfile, level=logging.INFO)

    configParser = ParserDeConfiguracionDeSimulacion()
    config = configParser.parsear_archivo(args.infile)

    if config is None:
        # :(
        sys.exit(1)

    critCorte = config.CriterioDeCorte
    print(critCorte)

