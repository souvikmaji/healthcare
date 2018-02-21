from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, DateField, FieldList, validators, SubmitField
from app import db

class UserMedicine(db.Model):
    __tablename__ = 'user_medicine'
    id = db.Column(db.Integer, primary_key=True)

    medicine_name = db.Column(db.Unicode(
        50), nullable=False, server_default=u'')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule = db.relationship('MedicineSchedule', backref='medicine', cascade="all, delete-orphan", lazy='dynamic')


class MedicineSchedule(db.Model):
    __tablename__ = 'medicine_schedule'
    id = db.Column(db.Integer, primary_key=True)

    medicine_id = db.Column(db.Integer, db.ForeignKey(
        'user_medicine.id'), nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False)

class AddMedicineForm(FlaskForm):
    medicine_name = StringField('Name', validators=[validators.DataRequired('Medicine name is required')])
    medicine_schedule_from_date = DateField('From Date')
    medicine_schedule_to_date = DateField('To Date')
    medicine_schedule_time = DateTimeField('Time to take', format='%H:%M')
    submit = SubmitField('Save')
