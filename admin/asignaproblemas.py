#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Asigna problemas a estudiantes
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
import random

if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Asigna problemas a alumnos aleatoriamente")
    p.add_argument('LISTA',
        help="Archivo con lista")
    p.add_argument("--problem",default=[],nargs=3,
            action="append", dest="problems",
            help="Agrega un tipo de problema []")
    p.add_argument("--random_off",default=True,
            action="store_false", dest="random",
            help="Apaga el uso de random [False]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Modo verbose [Off]")
    p.add_argument('--version', action='version', version='%(prog)s 0.1')
    opts = p.parse_args()

    # Opciones de configuración  -------------------------------------------
    if not opts.random:
        random.seed(9111978)

    # Prepara función de verbose  -----------------------------------------
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 

    # Lee lista
    students=[]
    verbose("Leyendo lista de:",opts.LISTA)
    for line in open(opts.LISTA):
        students.append(line.strip())

    assigned={}
    nameproblems=[]
    if len(opts.problems)==0:
        print("No hay problemas definidos")
    for name,number,offset in opts.problems:
        number=int(number)
        nameproblems=[]
        totalproblems=len(students)/number
        problems=range(number)*(totalproblems+1)
        random.shuffle(problems)
        for i,student in enumerate(students):
            try:
                assigned[student].append(problems[i]+int(offset))
            except KeyError:
                assigned[student]=[problems[i]+int(offset)]


    print("{:<50}".format("Nombre"),end="")
    for i,p in enumerate(opts.problems):
        print("{:<10}".format(p[0]),end="")
    print()
 
    for student in students:
        print("{:<50}".format(student),end="")
        for i,p in enumerate(opts.problems):
            print("{:>10}".format(assigned[student][i]),end="")
        print()

