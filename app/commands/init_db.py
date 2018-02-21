import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User
from app.models.medicine_models import UserMedicine, MedicineSchedule

from datetime import datetime


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """
    db.create_all()  # Create all tables
    user = find_or_create_user(u'Member', u'Example', u'9999999999',
                               u'user@example.com', 'Password1', u'abc_medicine')
    db.session.commit()


def find_or_create_user(first_name, last_name, ph_no, email, password, medicine_name):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        morning = MedicineSchedule(time=datetime(2018, 12, 25, 7, 0))
        noon = MedicineSchedule(time=datetime(2018, 1, 1, 12, 0))
        night = MedicineSchedule(time=datetime(2019, 5, 2, 17, 0))

        medicine = UserMedicine(medicine_name=medicine_name, schedule=[morning, noon, night])
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    ph_no=ph_no,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.utcnow(),
                    medicines=[medicine])

        db.session.add(medicine)
        db.session.add(user)
    return user
