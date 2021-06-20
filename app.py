#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd
import os
import csv

app = Flask(__name__, static_url_path='/static')

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
root = root_dir() + '/'

ab = [
    'Стрессоустойчивость',
    'Коммуникабельность',
    'Знание ПК',
    'Знание английского языкa',
    'Умение работать в команде',
]

def fmt(c):
    if c.startswith('https'):
        c = '<a href="%s" target=_blank>Ссылка</a>' % (c)
    return c


def filter_table(filename, search, ofs, total):
    f = open(root+filename, encoding="utf-8")
    rows = csv.DictReader(f, delimiter=',', quotechar='"')
    fields = rows.fieldnames

    data = {}

    data['headers'] = fields
    data['rows'] = []

    res = []
    for row in rows:
        if search=='' or any([search.lower() in str(x).lower() for x in row.values()]):
            res.append([fmt(x) for x in row.values()])

    data['rows'] = res[ofs:ofs+total]

    return data


@app.route('/', methods=['get'])
def index():
    q = request.args.get('q') or ''

    k = list(map(int,request.args.getlist('k')))

    ofs = 0
    per_page = 25

    vt = filter_table('vacancies.csv', q, ofs, per_page)
    ct = filter_table('resume.csv', q, ofs, per_page)

    tables = {'vt':{'data':vt}, 'ct':{'data':ct}}

    return render_template('index.html', ab=ab, q=q, k=k, tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
