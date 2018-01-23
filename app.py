import config
import datetime
import json
import time

from flask import Flask, url_for, render_template, redirect, request
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin


app = Flask(__name__)
app.config.from_object('config')
# app.config.from_pyfile(config_file)

#load extensions
db = MongoEngine(app)

class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)

    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    # Relationships
    roles = db.ListField(db.StringField(), default=[])
    def is_active(self):
      return self.is_enabled

# Setup Flask-User and specify the User data-model
user_manager = UserManager(User)

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('index'))


@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html', title='Home Page')


@app.route('/user/', methods=['GET'])
@login_required    # User must be authenticated
def user():
    return render_template('index.html', title='User Page')


@app.route('/user/add_med/', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        return 'add medicine'
    else:
        return render_template('form_sumbit.html')


@app.route('/user/meds/', methods=['GET'])
def meds():
    return 'get list of all medicines used by a user'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login'
    else:
        return 'show_the_login_form'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'register new user'
    else:
        return 'show_the_registration_form'


@app.route('/logout/', methods=['GET'])
def logout():
    return 'logout a user'


@app.route('/meds/', methods=['GET'])
def medicines():
    return 'get list of authenticated medicines'

# TODO: get info about a specific medicine
# @app.route('/meds', methods=[])
# def ():
#     return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# @autoreconnect_retry
    # @app.route('/get_info/', methods=['GET'])
    # def get_info():
    #     name = request.args.get('name')
    #     d = []
    #     for patient in collection.find({'name': name}):
    #         return json.loads(json_util.dumps(patient))
    #
    #     return "Not found"
    #
    #
    # @autoreconnect_retry
    # @app.route('/save/', methods=['POST'])
    # def save():
    #     # get data from form
    #     name = request.form['name']
    #     ph_no = request.form['ph_no']
    #     med_name = request.form['med_name']
    #     med_qty = request.form['med_qty']
    #     try:
    #         med_time = datetime.datetime.strptime(request.form['time'], '%H:%M')
    #         # construct document from data
    #         patient = {"name": name,
    #                    "ph_no": ph_no,
    #                    "medicines": [{"name": med_name,
    #                                   "qty": med_qty,
    #                                   "time": [med_time]
    #                                   }]
    #                    }
    #         collection.insert_one(patient)
    #
    #         sanitized = json.loads(json_util.dumps(patient))
    #     except ValueError:
    #         print("time field empty")
    #         sanitized = ""
    #
    #     return jsonify(sanitized)
    #
    #
    # @autoreconnect_retry
    # @app.route('/missed/', methods=['POST'])
    # def missed_med():
    #     userid = request.form['id_']
    #     miss_count = request.form['count']
    #     patient = collection.find_one_and_update(query={'name': userid}, update={'$set': {'count': miss_count}},
    #                                              return_document=ReturnDocument.AFTER)
    #     sanitized = json.loads(json_util.dumps(patient))
    #     return jsonify(sanitized)
