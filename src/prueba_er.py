#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Prueba una expresión regular 
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------
# asignaproblemas.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------
from __future__ import print_function

prog="asignaproblemas"

# System libraries
import argparse
import sys
import os
import re

if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Asigna problemas a alumnos aleatoriamente")
    p.add_argument('ER',
        help="Expresión regular a probar")
    p.add_argument('Archivo',
        help="Archivo para probar la expresión regular")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Modo verbose [Off]")
    p.add_argument('--version', action='version', version='%(prog)s 0.1')
    opts = p.parse_args()

    # Prepara función de verbose  -----------------------------------------
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 

    verbose("Abriendo archivo:",opts.Archivo)

    re_test=re.compile(opts.ER)

    for line in open(opts.Archivo):
        line=line.strip()
        m=re_test.match(line)
        if m:
            print(line)
