import sched
import time
from datetime import datetime

import os
from pymongo import MongoClient

MONGODB_HOST = os.environ['MONGODB_HOST']
# MONGODB_HOST = '172.17.0.2'
MONGODB_PORT = 27017
HSP_API_KEY = "8b6dc2b0-9671-4eba-b136-9532affec325"
s = sched.scheduler(time.time, time.sleep)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client['healthcare']
collection = db['patient_collection']


# connection = Connection(MONGODB_HOST, MONGODB_PORT)


def send_sms():
    print "Looking up db at: ", datetime.now()
    for patient in collection.find():
        for med in patient['medicines']:
            for t in med['time']:
                time_now = datetime.now()
                if time_now.hour == t.hour:
                    message = patient['name'] + ", time for " + med['name'] + " quantity:" + med[
                        'qty'] + " at time: " + str(t.hour) + ':' + str(t.minute)
                    url = "http://sms.hspsms.com/sendSMS?username=souvikmaji94&message=" + message + "&sendername=mdREMt&smstype=TRANS&numbers=" + \
                          patient['ph_no'] + "&apikey=" + HSP_API_KEY
                    # r = requests.get(url)
                    print r.text
                    print message


if __name__ == "__main__":
    while (True):
        s.enter(6, 1, send_sms, ())
        s.run()
