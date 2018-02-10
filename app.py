@app.route('/user/add_med/', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        return 'add medicine'
    else:
        return render_template('form_sumbit.html')


@app.route('/user/meds/', methods=['GET'])
def meds():
    return 'get list of all medicines used by a user'


# @autoreconnect_retry
# @app.route('/missed/', methods=['POST'])
# def missed_med():
#     userid = request.form['id_']
#     miss_count = request.form['count']
#     patient = collection.find_one_and_update(query={'name': userid}, update={'$set': {'count': miss_count}},
#                                              return_document=ReturnDocument.AFTER)
#     sanitized = json.loads(json_util.dumps(patient))
#     return jsonify(sanitized)
