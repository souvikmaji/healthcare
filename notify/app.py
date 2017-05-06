import ConfigParser
import sched
import time
from datetime import datetime

import os
from pymongo import MongoClient

config = ConfigParser.RawConfigParser()
config.read('notify.cfg')

MONGODB_HOST = os.environ['MONGODB_HOST']
# MONGODB_HOST = '172.17.0.2'
MONGODB_PORT = config.getint('MONGODB', 'PORT_NO')
HSP_API_KEY = config.get('HSPSMS', 'API_KEY')
s = sched.scheduler(time.time, time.sleep)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[config.get('MONGODB', 'DATABASE_NAME')]
collection = db[config.get('MONGODB', 'DATABASE_NAME')]
hsp_user = config.get('HSPSMS', 'USERNAME')
hsp_sender = config.get('HSPSMS', 'SENDER_NAME')
sched_interval = config.getint('HSPSMS', 'INTERVAL')


def send_sms():
    print "Looking up db at: ", datetime.now()
    for patient in collection.find():
        for med in patient['medicines']:
            for t in med['time']:
                time_now = datetime.now()
                if time_now.hour == t.hour:
                    message = patient['name'] + ", time for " + med['name'] + " quantity:" + med[
                        'qty'] + " at time: " + str(t.hour) + ':' + str(t.minute)
                    url = "http://sms.hspsms.com/sendSMS?username=" + hsp_user + "&message="
                    + message + "&sendername=" + hsp_sender + "&smstype=TRANS&numbers=" + \
                    patient['ph_no'] + "&apikey=" + HSP_API_KEY
                    # r = requests.get(url)
                    print r.text
                    print message


if __name__ == "__main__":
    while (True):
        s.enter(sched_interval, 1, send_sms, ())
        s.run()
