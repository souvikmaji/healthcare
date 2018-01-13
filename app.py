import config
import datetime
import json
import time

from bson import json_util
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure

from reconnect import autoreconnect_retry

# MONGODB_HOST = "localhost"
MONGODB_HOST = config.mongodb['host']
MONGODB_PORT = config.mongodb['port']

app = Flask(__name__)
app.config.from_object(__name__)

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
for i in range(100):
    try:
        connection.admin.command('ismaster')
        break
    except ConnectionFailure:
        time.sleep(pow(2, i))
        connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
        print("Connection to db failed. Start MongoDB instance.")

db = connection[config.mongodb['name']]
collection = "patients"


# TODO: server side form validation
def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        # must have %s in error format string to have mongokit place key in there
        raise ValidationError(
            '%s must be at most {} characters long'.format(length))

    return validate


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
    for patient in collection.find({'name': name}):
        return json.loads(json_util.dumps(patient))

    return "Not found"


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
    except ValueError:
        print("time field empty")
        sanitized = ""

    return jsonify(sanitized)


@autoreconnect_retry
@app.route('/missed', methods=['POST'])
def missed_med():
    userid = request.form['id_']
    miss_count = request.form['count']
    patient = collection.find_one_and_update(query={'name': userid}, update={'$set': {'count': miss_count}},
                                             return_document=ReturnDocument.AFTER)
    sanitized = json.loads(json_util.dumps(patient))
    return jsonify(sanitized)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
