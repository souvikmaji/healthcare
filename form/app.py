import datetime
import json
import time

import os
from bson import json_util
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, AutoReconnect

# MONGODB_HOST = "localhost"
MONGODB_HOST = os.environ['MONGODB_HOST']
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
for i in range(10):
    try:
        connection.admin.command('ismaster')
        break
    except ConnectionFailure:
        time.sleep(pow(2, i))
        connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
        print("Connection to db failed. Start MongoDB instance.")
        # sys.exit(1)

db = connection['healthcare']
collection = db['patient_collection']


def autoreconnect_retry(fn, retries=10):
    """decorator for connection retrial"""

    def db_op_wrapper(*args, **kwargs):
        tries = 0
        while tries < retries:
            try:
                return fn(*args, **kwargs)
            except AutoReconnect:
                time.sleep(pow(2, tries))
                tries += 1

        raise Exception("No luck even after %d retries. Start Mongodb \
                            instance" % retries)

    return db_op_wrapper


# TODO: make use of
def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        # must have %s in error format string to have mongokit place key in there
        raise ValidationError('%s must be at most {} characters long'.format(length))

    return validate


# TODO: make use of
# @connection.register
"""class Patient(Document):
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
"""


@app.route('/')
def form():
    return render_template('form_sumbit.html')


@autoreconnect_retry
@app.route('/get_info', methods=['GET'])
def get_info():
    name = request.args.get('name')
    d = []
    for patient in connection.Patient.find({'name': name}):
        for med in patient.medicines:
            d.append(med['time'])
    return dumps(d)


@autoreconnect_retry
@app.route('/save', methods=['POST'])
def save():
    # get data from form
    name = request.form['name']
    ph_no = request.form['ph_no']
    med_name = request.form['med_name']
    med_qty = request.form['med_qty']
    try:
        med_time = datetime.datetime.strptime(request.form['time'], '%H:%M')
    except ValueError:
        print("time field empty")

    # construct document from data
    patient = {"name": name,
               "ph_no": ph_no,
               "medicines": [{"name": med_name,
                              "qty": med_qty,
                              "time": [med_time]
                              }]
               }
    collection.insert_one(patient)

    sanitized = json.loads(json_util.dumps(patient))
    return jsonify(sanitized)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
