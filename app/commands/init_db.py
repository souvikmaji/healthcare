import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User

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

    # Create all tables
    db.create_all()

    # Add users
    user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_user(first_name, last_name, email, password):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())

        db.session.add(user)
    return user
