#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
import argparse
import random

# Carga aplicación Flask
app = Flask(__name__)

list_students = []
current = None


# Página principa.
@app.route('/')
def login():
    return render_template('home.html')


# Paǵina acerca de
@app.route('/about')
def about():
    return render_template('about.html')


# Paǵina acerca de
@app.route('/list')
def list():
    return render_template('list.html', list=list_students)


# Start presentations
@app.route('/presentations')
def presentations():
    return render_template('presentations.html')


def draw():
    not_draw = [s for s in list_students if s[2] == 0]
    current = random.choice(not_draw)
    return current


# Start presentations
@app.route('/start')
def start():
    global list_students, current
    list_students = [(s[0], s[1], 0) for s in list_students]
    return redirect(url_for('.next'))


# Start presentations
@app.route('/next')
@app.route('/next/<int:idd>/<int:status>')
def next(idd=None, status=None):
    global list_students, current
    if idd:
        s = list_students[idd]
        list_students[idd] = (s[0], s[1], status)
    if not current:
        current = draw()
    elif current[0] == idd:
        current = draw()

    missing = [s for s in list_students if s[2] == 2]
    return render_template('name.html', student=current, missing=missing)


# Start presentations
@app.route('/set/<int:idd>/<int:status>')
def set(idd=None, status=None):
    global list_students, current
    if idd is not None:
        s = list_students[idd]
        list_students[idd] = (s[0], s[1], status)
    return redirect(url_for('.list'))


# Función principal (interfaz con línea de comandos)
if __name__ == '__main__':
    p = argparse.ArgumentParser("lfya_webapp")
    p.add_argument("LISTA", help="List to use")
    p.add_argument("--host", default="127.0.0.1",
                   action="store", dest="host",
                   help="Root url [127.0.0.1]")
    p.add_argument("--port", default=5000, type=int,
                   action="store", dest="port",
                   help="Port url [500]")
    p.add_argument("--debug", default=False,
                   action="store_true", dest="debug",
                   help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
                   action="store_true", dest="verbose",
                   help="Verbose mode [Off]")

    opts = p.parse_args()

    with open(opts.LISTA, 'r') as f:
        list_students = f.readlines()

    list_students = [(i, s, 0) for i,s in enumerate(list_students)]

    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)
