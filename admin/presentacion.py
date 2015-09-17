#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Controla orden de presentación
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------
# presentacion.py is free software: you can redistribute it and/or modify
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

prog="presentacion"

# System libraries
import argparse
import sys
import os
import random
import presentacion
import cmd


class AuthorIdCLI(cmd.Cmd):
    def __init__(self,students):
        cmd.Cmd.__init__(self)
        self.promtp = "> "
        self.intro  = "Bienvenido a la consola para cordinar las presentaciones!"
        self.students = students
        self.random = range(len(students))
        self.presented = [False for s in students]
        self.cur=-1

    def do_reset(self,args):
        self.random = range(len(students))
        self.presented = [False for s in students]
        self.cur=-1

    def do_ls(self,args):
        'Prints the list'
        self.do_list(args)

    def do_list(self,args):
        'Prints the list, with random print random order'
        args=args.strip().split()
        if len(args)==0:
            students=range(len(self.students))
        else:
            if args[0]=='random':
                students=self.random
            else:
                students=range(len(students))
 
        for i,student in enumerate(students):
            print("{0:2d} {1} {2}".format(i,self.presented[student], self.students[student]))
        
    def do_random(self,args):
        "Randomizes the list"
        random.shuffle(self.random)


    def do_check(self,args):
        'Checa al siguiente estudiante que no ha presentado'
        found=False
        for i,student in enumerate(self.random):
            if not self.presented[self.random[i]]:
                self.cur=i
                found=True
                break
        if found:
            print(self.students[self.random[self.cur]]) 
        else:
            print("Todos han presentado") 


    def do_next(self,args):
        'Presenta el siguiente estudiante que no ha presentado'
        if self.cur>=0:
            self.presented[self.random[self.cur]]=True
        self.cur+=1
        while self.cur<len(self.students) and self.presented[self.random[self.cur]]:
                self.cur+=1
        if self.cur>=len(self.students):
            print('No más estudiantes')
            self.cur=len(students)-1
        else:
            print(self.students[self.random[self.cur]])

    def do_skip(self,args):
        'Brinca a este estudiante que no ha presentado'
        self.cur+=1
        while self.cur<len(self.students) and self.presented[self.random[self.cur]]:
                self.cur+=1
        if self.cur>=len(self.students):
            print('No más estudiantes')
            self.cur=len(students)-1
        else:
            print(self.students[self.random[self.cur]]) 

    def do_current(self,args):
        'Presenta el estudiante actual'
        print(self.students[self.random[self.cur]]) 


    def do_save(self,args):
        'Guarda el estado de la lista en un archivo'
        if len(args)==0:
            print("Error: no filename provided")

        args=args.strip().split()
        output=open(args[0],'w')
        for student in self.random:
            print("{0} {1}".format(self.presented[student],
                self.students[student]),file=output)
        output.close()

    def do_set(self,args):
        'Cambia el estado de uno de los estudiantes'
        if len(args)==0:
            print("Error: no filename provided")

        args=args.strip().split()
        self.presented[int(args[0])]=not self.presented[int(args[0])]


    def do_EOF(self, arg):                                                     
        'Exit'
        print('Saliendo')
        return True  


    def do_bye(self, arg):                                                     
        'Exit'                                                                 
        print('Saliendo')
        return True  

if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Asigna problemas a alumnos aleatoriamente")
    p.add_argument('LISTA',
        help="Archivo con lista")
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

    console=AuthorIdCLI(students)
    console.cmdloop()

