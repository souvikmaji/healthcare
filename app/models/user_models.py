from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    ph_no = db.Column(db.Unicode(12), nullable=False, server_default=u'')
    medicines = db.relationship('UserMedicine', backref='user', cascade="all, delete-orphan", lazy='dynamic')

class UserMedicine(db.Model):
    __tablename__ = 'user_medicine'
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    ph_no = StringField('Mobile Number', validators=[
        validators.DataRequired('Phone Number is required to send you notifications')])

# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    ph_no = StringField('Mobile Number', validators=[
        validators.DataRequired('Phone Number is required to send you notifications')])
    submit = SubmitField('Save')

class AddMedicineForm(FlaskForm):
    medicine_name = StringField('Name', validators=[
        validators.DataRequired('Medicine name is required')])
    submit = SubmitField('Save')
