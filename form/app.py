import datetime
import sys

import os
from flask import Flask, request, render_template, jsonify
from mongokit import Connection, Document, ValidationError
from pymongo.errors import ConnectionFailure

MONGODB_HOST = os.environ['MONGODB_HOST']
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
try:
    connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
except ConnectionFailure:
    print("Connection to db failed. Start MongoDB instance.")
    sys.exit(1)


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        # must have %s in error format string to have mongokit place key in there
        raise ValidationError('%s must be at most {} characters long'.format(length))

    return validate


@connection.register
class Patient(Document):
    __collection__ = 'patient_collection'
    __database__ = 'healthcare'
    structure = {
        'name': unicode,
        'ph_no': unicode,
        'medicines': [
            {
                'name': unicode,
                'qty': unicode,
                'time': [datetime.datetime]
            }]
    }
    validators = {
        'name': max_length(50),
        'ph_no': max_length(12)
    }
    use_dot_notation = True

    def __repr__(self):
        return '<User %r,%r>' % (self.name, self.ph_no)


@app.route('/')
def form():
    return render_template('form_sumbit.html')


@app.route('/get_info', methods=['GET'])
def get_info():
    name = request.args.get('name')
    d = []
    for patient in connection.Patient.find({'name': name}):
        for med in patient.medicines:
            d.append(med['time'])
    return jsonify(d)


@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    ph_no = request.form['ph_no']
    med_name = request.form['med_name']
    med_qty = request.form['med_qty']
    try:
        med_time = datetime.datetime.strptime(request.form['time'], '%H:%M')
    except ValueError:
        print("time field empty")
        # raise
    # print med_time
    patient = connection.Patient()

    patient['name'] = name
    patient['ph_no'] = ph_no
    patient['medicines'].append({'name': med_name,
                                 'qty': med_qty,
                                 'time': [med_time]})

    patient.save()
    print "type: ", type(patient)

    #    for d in connection.Patient.find():
    #        return jsonify(d)

    return render_template('form_action.html', name=name, ph_no=ph_no, med_name=med_name, med_qty=med_qty,
                           time=med_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
