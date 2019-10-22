#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, Response
import argparse
import random
import re
import os

# Carga aplicación Flask
app = Flask(__name__)

list_students = []
current = None
assignations = None

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

# Assign
@app.route('/asign')
def asign():
    asignations=[]
    return render_template('asign.html',asignations=asignations)

@app.route('/asign_list')
def asign_list():

    global assignations
    if request.args:
        names=[str(x) for x in request.args.getlist('n') if len(x) > 0]
        totals=[int(x) for x in request.args.getlist('t') if len(x) > 0]
        assignations=[]
        global list_students
        list_students_ = [(s[0], s[1], 0) for s in list_students]
        TOTAL=0
        for name,total in zip(names,totals):
            assignations.append([])
            for ii,lement in enumerate(list_students_):
                assignations[-1].append(random.choice(range(total))+TOTAL)
            TOTAL+=total
    return render_template('asign.html',list=list_students_,assignations=assignations,names=names,totals=totals)


@app.route('/save_asignation')
def save_asignation():
    global assignations
    csv=""
    if request.args:
        vals=['id']
        names=[str(x) for x in request.args.getlist('n') if len(x) > 0]
        for name in names:
            vals.append(name)
        csv+="{}\n".format(",".join(vals))
        for idd,student_name,status in list_students:
            vals=["{}".format(idd)]
            for iname,name in enumerate(names):
                vals.append("{}".format(assignations[iname][idd]))
            csv+="{}\n".format(",".join(vals))

        return Response(csv,mimetype="text/csv",headers={"Content-disposition":"attachment; filename=asignacion.csv"})


# Start presentations
@app.route('/presentations')
def presentations():
    return render_template('presentations.html')

@app.route('/groups')
@app.route('/groups/<int:n>')
def groups(n=4):
    global list_students
    list_students_ = [(s[0], s[1], 0) for s in list_students]
    random.shuffle(list_students_)
    groups=[[] for i in range(n)]
    for ii,element in enumerate(list_students_):
        try:
            groups[ii%n].append(element)
        except IndexError:
            groups[ii%n]=[element]
    return render_template('groups.html', groups=groups)




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
@app.route('/karaoke')
def karaoke():
    return render_template('karaoke.html')


re_file=re.compile(r".* (\d+)....$")

# Start presentations
@app.route('/karastart')
def karastart():
    global assignations, pres
    global list_students

    list_students = [(s[0], s[1], 0) for s in list_students]
    csv=""
    if request.args:
        assignations=dict()
        fst=True
        for line in open(request.args.get('file')):
            if fst:
                fst=False
                continue
            idd,*prom=[int(i) for i in  line.strip().split(",")]
            for p in prom:
                try:
                    assignations[p].append(idd)
                except KeyError:
                    assignations[p]=[idd]
        pres=[]
        for f in os.listdir(request.args.get('dir')):
            m=re_file.match(f)
            if m:
                pres.append((f,int(m.group(1))-1))
    return redirect(url_for('.karanext'))

# Start presentations
@app.route('/karanext')
@app.route('/karanext/<int:idd>/<pre>/<int:status>')
def karanext(idd=None,pre=None,status=None):
    global assignations, pres
    global list_students

    if idd and idd!=1000:
        s = list_students[idd]
        list_students[idd] = (s[0], s[1], status)
        for i,l in [a for a in assignations.items()]:
            if idd in assignations[i]:
                assignations[i].remove(idd)
  
    if pre:
        pres = [p for p in pres if not p[0] == pre]
    pre=random.choice(pres)
    if len(assignations[pre[1]])==0:
       ass=(1000,"Nadie",0) 
    else:
        ass=random.choice(assignations[pre[1]])
        ass=list_students[ass]
    return render_template('karacurr.html', pre=pre, student=ass)



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


# Start presentations
@app.route('/save')
def save(idd=None, status=None):
    global list_students, current
    with open("status.txt", 'w') as f:
        for num, name, status in list_students:
            print(name, ",", status, file=f)
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

    list_students = [(i, s.strip(), 0) for i,s in enumerate(list_students)]

    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)
