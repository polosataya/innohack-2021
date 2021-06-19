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

ab = ['Стрессоустойчивость',
    'Коммуникабельность',
    'Знание ПК',
    'Знание английского языкa',
]

df = pd.DataFrame({'Фамилия Имя': ['Иванов Иван', 'Петров Петр', 'Иванов Сергей', 'Петрова Галина', 'Сидоров Петр'],
                   'Ключевые навыки': ['стрессоустойчивость', 'стрессоустойчивость', 'стрессоустойчивость', 'стрессоустойчивость', 'стрессоустойчивость'],
                   'Город': ['Москва', 'Санкт Петербург', 'Екатеринбург', 'Москва', 'Москва'],
                   'Стаж': ['1', '5', '2', '1', '0']})

@app.route('/', methods=['get'])
def index():
    q = request.args.get('q')

    f = open('resume.csv', encoding="utf-8")
    rows = csv.DictReader(f, delimiter=',', quotechar='"')
    fields = rows.fieldnames

    data = {}
    data['headers'] = fields
    data['rows'] = []

    for row in rows:
        data['rows'].append( [str(x) for x in row.values()] )

    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, ab=ab, data=data, q=q)

if __name__ == '__main__':
    app.run(debug=True)
